// ============================================================
//  FACTORYCALC — CHAIN SOLVER  v1.5
//  - Fixed: Somersloop never applied to raw/extraction nodes
//  - Added: per-node input/output rates for card display
//  - Added: nested recipe-map resolution with override support
//  - Added: byproduct credit pass — offsets raw nodes from byproducts
// ============================================================

const Solver = (() => {

  // ── PASS 1: Recursive accumulation ──────────────────────────
  // Walk the recipe tree, sum required rates per item across all branches.
  // Sloop rule: production buildings only — never extraction/raw nodes.
  function accumulate(itemName, requiredRate, depth, fedBy, acc, oc, sloop, overrides, _visiting) {
    _visiting = _visiting || new Set();
    if (_visiting.has(itemName)) return;
    _visiting.add(itemName);

    const isRaw = RAW_RESOURCES.has(itemName);
    const rec   = RECIPES[itemName];

    // ── Raw / unknown → extraction node, no sloop, no recipe ──
    if (isRaw || !rec) {
      if (!acc[itemName]) {
        acc[itemName] = {
          rate: 0, depth,
          building: 'Extraction Node',
          mw: 0, isRaw: true,
          feeds: [], merged: false,
          outputPerMachine: null,
          inputs: [], recipe: '—',
        };
      }
      acc[itemName].rate += requiredRate;
      if (fedBy && !acc[itemName].feeds.includes(fedBy))
        acc[itemName].feeds.push(fedBy);
      _visiting.delete(itemName);
      return;
    }

    // ── Resolve active recipe from nested map ──────────────────
    const overriddenKey = overrides?.[itemName];
    const activeKey     = (overriddenKey && rec.recipes[overriddenKey])
      ? overriddenKey
      : rec.alts[0];
    const activeRec     = rec.recipes[activeKey];

    // ── Production machine ─────────────────────────────────────
    const sloopMult  = sloop ? 2 : 1;
    const outputMult = (oc / 100) * sloopMult;

    if (!acc[itemName]) {
      acc[itemName] = {
        rate: 0, depth,
        building: activeRec.building,
        mw: activeRec.mw,
        outputPerMachine: activeRec.output,
        inputs: activeRec.inputs,
        byproduct: activeRec.byproduct || null,
        isRaw: false,
        feeds: [], merged: false,
        recipe: activeKey,
        alts: rec.alts || ['Basic'],
      };
    } else {
      acc[itemName].merged = true;
      if (depth < acc[itemName].depth) acc[itemName].depth = depth;
    }

    acc[itemName].rate += requiredRate;
    if (fedBy && !acc[itemName].feeds.includes(fedBy))
      acc[itemName].feeds.push(fedBy);

    const machines = Math.ceil(requiredRate / (activeRec.output * outputMult));

    activeRec.inputs.forEach(inp => {
      const inputRate = machines * inp.qty * (oc / 100);
      accumulate(inp.item, inputRate, depth + 1, itemName, acc, oc, sloop, overrides, _visiting);
    });

    _visiting.delete(itemName);
  }

  // ── PASS 2: Calculate machines + I/O from merged totals ─────
  // Now that every item has its total required rate (merged across all branches),
  // calculate machines, power, belts, and exact I/O rates from those totals.
  function calcFromMerged(acc, oc, sloop, beltLimit, pipeLimit) {
    const result = {};

    Object.entries(acc).forEach(([name, data]) => {

      // ── Raw node — no machines, just show required rate ──────
      if (data.isRaw) {
        result[name] = {
          ...data,
          machines:     null,
          power:        0,
          belts:        null,
          pipes:        null,
          strLen:       null,
          rows:         null,
          inputRates:   [],   // no inputs — comes from the ground
          outputRate:   data.rate,
          byproductRate: 0,
        };
        return;
      }

      // ── Production machine ────────────────────────────────────
      // Sloop doubles output → fewer machines needed for same rate.
      // Inputs are NOT doubled — sloop only affects output quantity.
      const sloopMult  = sloop ? 2 : 1;
      const outputMult = (oc / 100) * sloopMult;

      const machines   = Math.ceil(data.rate / (data.outputPerMachine * outputMult));
      const power      = machines * data.mw;

      // Belt/pipe counts based on output rate
      const actualOutputRate = machines * data.outputPerMachine * outputMult;
      const belts  = Math.ceil(actualOutputRate / beltLimit);
      const pipes  = Math.ceil(actualOutputRate / pipeLimit);

      // Row × string layout
      const strLen = Math.max(1, Math.floor(beltLimit / (data.outputPerMachine * outputMult)));
      const rows   = Math.ceil(machines / strLen);

      // ── Input rates (per minute, total factory) ──────────────
      // Inputs are NOT sloop-affected — only outputs double.
      const inputRates = (data.inputs || []).map(inp => ({
        item: inp.item,
        rate: +(machines * inp.qty * (oc / 100)).toFixed(4),
      }));

      // ── Output rates ─────────────────────────────────────────
      const outputRate    = +(actualOutputRate).toFixed(4);
      const byproductRate = data.byproduct
        ? +(machines * data.byproduct.qty).toFixed(4)
        : 0;

      result[name] = {
        ...data,
        machines,
        power,
        belts,
        pipes,
        strLen,
        rows,
        inputRates,
        outputRate,
        byproductRate,
        byproductItem: data.byproduct ? data.byproduct.item : null,
      };
    });

    return result;
  }

  // ── PUBLIC: solve ────────────────────────────────────────────
  function solve({ item, target, oc = 100, sloop = false, beltLimit = 780, pipeLimit = 600, overrides = {}, byproductCredit = false }) {
    const acc = {};
    accumulate(item, target, 0, null, acc, oc, sloop, overrides);

    const nodes = calcFromMerged(acc, oc, sloop, beltLimit, pipeLimit);

    // ── Byproduct credit pass ─────────────────────────────────
    // Sum all byproduct production; reduce raw node rates by matching byproduct.
    const byproductCredits = {};
    if (byproductCredit) {
      const totalByp = {};
      Object.values(nodes).forEach(n => {
        if (!n.isRaw && n.byproductItem && n.byproductRate > 0) {
          totalByp[n.byproductItem] = (totalByp[n.byproductItem] || 0) + n.byproductRate;
        }
      });
      Object.entries(nodes).forEach(([name, data]) => {
        if (data.isRaw && totalByp[name] > 0) {
          const credit = Math.min(totalByp[name], data.rate);
          data.creditFromByp = credit;
          data.rateBeforeCredit = data.rate;
          data.rate -= credit;
          data.outputRate = data.rate;
          byproductCredits[name] = { needed: data.rateBeforeCredit, credit, net: data.rate };
        }
      });
    }

    // Group by stage depth
    const byDepth  = {};
    const rawNodes = [];

    Object.entries(nodes).forEach(([name, data]) => {
      if (data.isRaw) {
        rawNodes.push({ name, ...data });
        return;
      }
      const d = data.depth;
      if (!byDepth[d]) byDepth[d] = [];
      byDepth[d].push({ name, ...data });
    });

    // Totals
    const nonRaw        = Object.values(nodes).filter(n => !n.isRaw);
    const totalMachines = nonRaw.reduce((s, n) => s + (n.machines || 0), 0);
    const totalPower    = nonRaw.reduce((s, n) => s + n.power, 0);
    const stages        = Object.keys(byDepth).length;

    return { nodes, byDepth, rawNodes, totalMachines, totalPower, stages, byproductCredits };
  }

  return { solve };
})();
