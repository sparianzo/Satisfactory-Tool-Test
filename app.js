// ============================================================
//  FACTORYCALC — APP CONTROLLER  v1.5
//  - Updated: node cards show calculated I/O rates
//  - Updated: raw nodes marked as sloop-ineligible in UI
// ============================================================

const App = (() => {

  let state = {
    item:      'Motor',
    target:    10,
    oc:        100,
    sloop:     false,
    beltLimit: 780,
    pipeLimit: 600,
    overrides: {},
    view:      'stages',
    result:    null,
    byproductCredit: false,
  };

  let toastTimer = null;

  // ── INIT ────────────────────────────────────────────────────
  function init() {
    populateItemSelect();
    loadFromURL();
    renderSavedList();
    solve();
  }

  function populateItemSelect() {
    const sel = document.getElementById('itemSelect');
    ITEM_LIST.forEach(name => {
      const opt      = document.createElement('option');
      opt.value      = name;
      opt.textContent = name;
      if (name === state.item) opt.selected = true;
      sel.appendChild(opt);
    });
  }

  // ── READ INPUTS ─────────────────────────────────────────────
  function readInputs() {
    state.item      = document.getElementById('itemSelect').value;
    state.target    = parseFloat(document.getElementById('targetInput').value) || 10;
    state.oc        = parseFloat(document.getElementById('overclock').value) || 100;
    state.sloop          = parseInt(document.getElementById('sloopGlobal').value) === 1;
    state.beltLimit      = parseFloat(document.getElementById('beltLimit').value) || 780;
    state.pipeLimit      = parseFloat(document.getElementById('pipeLimit').value) || 600;
    state.byproductCredit = parseInt(document.getElementById('byproductCredit').value) === 1;
  }

  // ── SOLVE ───────────────────────────────────────────────────
  function solve() {
    readInputs();
    state.result = Solver.solve({
      item:      state.item,
      target:    state.target,
      oc:        state.oc,
      sloop:     state.sloop,
      beltLimit: state.beltLimit,
      pipeLimit: state.pipeLimit,
      overrides: state.overrides,
      byproductCredit: state.byproductCredit,
    });
    render();
    updateURL();
  }

  // ── RENDER ──────────────────────────────────────────────────
  function render() {
    const { result } = state;
    if (!result) return;

    document.getElementById('chainTitle').textContent =
      `${state.item.toUpperCase()} — FULL PRODUCTION CHAIN`;
    document.getElementById('chainSub').textContent =
      `// Target: ${state.target}/min · OC: ${state.oc}% · Sloop: ${state.sloop ? 'ON (production only)' : 'OFF'} · Credit: ${state.byproductCredit ? 'ON' : 'OFF'} · Merged nodes`;

    if (state.view === 'stages') renderStages(result);
    else renderFlat(result);

    renderRawSummary(result.rawNodes);
    renderTotals(result);
    renderSwapControls(result.nodes);
  }

  // ── STAGES VIEW ─────────────────────────────────────────────
  function renderStages({ byDepth, rawNodes }) {
    const scroll = document.getElementById('chainScroll');
    const depths = Object.keys(byDepth).map(Number).sort((a, b) => a - b);
    let html = '';

    depths.forEach(d => {
      const nodes  = byDepth[d];
      const isOut  = d === 0;
      const label  = isOut
        ? '// OUTPUT'
        : `// STAGE ${d + 1}  ·  ${nodes.length} item${nodes.length > 1 ? 's' : ''}`;

      html += `<div class="stage-group">
        <div class="stage-label">
          <div class="stage-line"></div>
          <div class="stage-tag ${isOut ? 'output' : 'intermediate'}">${label}</div>
          <div class="stage-line"></div>
        </div>
        <div class="nodes-grid">
          ${nodes.map(n => nodeCard(n, isOut)).join('')}
        </div>
      </div>`;
    });

    if (rawNodes.length) {
      html += `<div class="stage-group">
        <div class="stage-label">
          <div class="stage-line"></div>
          <div class="stage-tag raw">// RAW NODES  ·  ${rawNodes.length} resource${rawNodes.length > 1 ? 's' : ''}</div>
          <div class="stage-line"></div>
        </div>
        <div class="nodes-grid">
          ${rawNodes.map(n => nodeCard(n, false)).join('')}
        </div>
      </div>`;
    }

    scroll.innerHTML = html;
  }

  // ── FLAT VIEW ───────────────────────────────────────────────
  function renderFlat({ nodes }) {
    const scroll = document.getElementById('chainScroll');
    const sorted = Object.entries(nodes).sort((a, b) => {
      if (a[1].isRaw && !b[1].isRaw) return 1;
      if (!a[1].isRaw && b[1].isRaw) return -1;
      return a[1].depth - b[1].depth;
    });

    const rows = sorted.map(([name, data]) => {
      const fmt = n => typeof n === 'number' ? (n % 1 === 0 ? n : n.toFixed(2)) : '—';
      const cls = data.isRaw ? 'raw-row' : '';
      const inStr  = data.inputRates && data.inputRates.length
        ? data.inputRates.map(i => `${fmt(i.rate)} ${i.item}`).join(', ')
        : '—';
      const outStr = data.isRaw ? `${fmt(data.outputRate)}/min` : `${fmt(data.outputRate)}/min`;
      return `<tr class="${cls}">
        <td>${name}${data.merged ? ' <small style="color:rgba(150,180,255,0.7)">⊕</small>' : ''}</td>
        <td>${data.isRaw ? 'Raw Node' : data.building}</td>
        <td class="mono">${data.machines ?? '—'}</td>
        <td class="mono in-col">${inStr}</td>
        <td class="mono out-col">${outStr}${data.byproductItem ? ` + ${fmt(data.byproductRate)} ${data.byproductItem}` : ''}</td>
        <td class="mono">${data.power ? data.power + ' MW' : '—'}</td>
        <td class="mono">${data.rows && data.strLen ? `${data.rows} × ${data.strLen}` : '—'}</td>
        <td>${data.recipe || '—'}</td>
      </tr>`;
    }).join('');

    scroll.innerHTML = `<table class="flat-table">
      <thead><tr>
        <th>ITEM</th><th>BUILDING</th><th>MACHINES</th>
        <th>INPUTS / MIN</th><th>OUTPUT / MIN</th>
        <th>POWER</th><th>ROWS×STR</th><th>RECIPE</th>
      </tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
  }

  // ── NODE CARD ───────────────────────────────────────────────
  function nodeCard(node, isOutput) {
    const fmt = v => typeof v === 'number'
      ? (v % 1 === 0 ? v.toLocaleString() : parseFloat(v.toFixed(2)).toLocaleString())
      : v;

    // ── RAW NODE CARD ──────────────────────────────────────────
    if (node.isRaw) {
      const creditNote = node.creditFromByp
        ? `<span class="credit-badge">${fmt(node.creditFromByp)}/min from byproduct</span>`
        : '<span style="color:var(--dim)">No Somersloop — extraction only</span>';
      const creditStat = node.creditFromByp
        ? `<div class="ns ns-credit">
            <div class="ns-k">BYPRODUCT CREDIT</div>
            <div class="ns-v">${fmt(node.creditFromByp)}</div>
            <div class="ns-u">/min offset</div>
          </div>`
        : `<div class="ns">
            <div class="ns-k">NODES</div>
            <div class="ns-v" style="font-size:10px;color:var(--dim)">TBD</div>
            <div class="ns-u">from map</div>
          </div>`;
      return `<div class="node raw-node">
        <div class="node-head">
          <div class="node-class">RAW RESOURCE // EXTRACTION NODE</div>
          <div class="node-name">${node.name}</div>
          <div class="node-recipe">${creditNote}</div>
        </div>
        <div class="node-stats">
          <div class="ns">
            <div class="ns-k">REQUIRED</div>
            <div class="ns-v">${fmt(node.outputRate)}</div>
            <div class="ns-u">/min net</div>
          </div>
          ${creditStat}
          <div class="ns">
            <div class="ns-k">SLOOP</div>
            <div class="ns-v" style="font-size:10px;color:var(--dim)">N/A</div>
            <div class="ns-u">not eligible</div>
          </div>
        </div>
        <div class="node-io">
          <div class="node-io-row out">
            <div class="io-dir out">OUT</div>
            <div class="io-items">
              <div class="io-item">
                <span class="io-name">${node.name}</span>
                <span class="io-rate out-rate">${fmt(node.outputRate)}<span class="io-unit">/min${node.creditFromByp ? ' (net)' : ''}</span></span>
              </div>
            </div>
          </div>
        </div>
        ${node.feeds.length
          ? `<div class="node-feeds"><div class="nf-text">FEEDS <span>${node.feeds.join(', ')}</span></div></div>`
          : ''}
      </div>`;
    }

    // ── PRODUCTION NODE CARD ───────────────────────────────────
    const mergedTag = node.merged
      ? '<div class="merged-tag">⊕ MERGED NODE</div>' : '';
    const rowStr    = node.rows && node.strLen
      ? `${node.rows} × ${node.strLen}` : '—';
    const sloopNote = state.sloop
      ? '<span class="sloop-on">SLOOP ×2</span>' : '';

    // Build input rows
    const inputRows = (node.inputRates || []).map(inp => `
      <div class="io-item">
        <span class="io-name">${inp.item}</span>
        <span class="io-rate in-rate">${fmt(inp.rate)}<span class="io-unit">/min</span></span>
      </div>`).join('');

    // Build output rows
    const outputRows = `
      <div class="io-item">
        <span class="io-name">${node.name}</span>
        <span class="io-rate out-rate">${fmt(node.outputRate)}<span class="io-unit">/min</span></span>
      </div>
      ${node.byproductItem ? `
      <div class="io-item byproduct">
        <span class="io-name">↳ ${node.byproductItem}</span>
        <span class="io-rate byp-rate">${fmt(node.byproductRate)}<span class="io-unit">/min</span></span>
      </div>` : ''}`;

    return `<div class="node ${isOutput ? 'output-node' : ''} ${node.merged ? 'merged-node' : ''}">
      <div class="node-head">
        <div class="node-class">${node.building.toUpperCase()} // ${node.mw} MW / MACHINE</div>
        <div class="node-name">${node.name}</div>
        <div class="node-recipe">Recipe: ${node.alts && node.alts.length > 1
          ? `<select class="inline-alt-sel" onchange="App.setRecipe('${node.name.replace(/'/g, "\\'")}', this.value)" onclick="event.stopPropagation()">
              ${node.alts.map(a => `<option value="${a}" ${a === node.recipe ? 'selected' : ''}>${a}</option>`).join('')}
            </select>`
          : `<span>${node.recipe}</span>`} ${sloopNote}</div>
        ${mergedTag}
      </div>

      <div class="node-stats">
        <div class="ns">
          <div class="ns-k">MACHINES</div>
          <div class="ns-v">${node.machines}</div>
          <div class="ns-u">${node.building}s</div>
        </div>
        <div class="ns">
          <div class="ns-k">POWER</div>
          <div class="ns-v">${node.power.toLocaleString()}</div>
          <div class="ns-u">MW total</div>
        </div>
        <div class="ns">
          <div class="ns-k">ROWS×STR</div>
          <div class="ns-v">${rowStr}</div>
          <div class="ns-u">belt layout</div>
        </div>
      </div>

      <div class="node-io">
        ${inputRows.length ? `
        <div class="node-io-row in">
          <div class="io-dir in">IN</div>
          <div class="io-items">${inputRows}</div>
        </div>` : ''}
        <div class="node-io-row out">
          <div class="io-dir out">OUT</div>
          <div class="io-items">${outputRows}</div>
        </div>
      </div>

      ${node.feeds.length
        ? `<div class="node-feeds"><div class="nf-text">FEEDS <span>${node.feeds.join(', ')}</span></div></div>`
        : ''}
    </div>`;
  }

  // ── RAW SUMMARY ─────────────────────────────────────────────
  function renderRawSummary(rawNodes) {
    const bar   = document.getElementById('rawSummary');
    const items = document.getElementById('rawItems');
    if (!rawNodes.length) { bar.style.display = 'none'; return; }
    bar.style.display = 'flex';
    const fmt = n => n % 1 === 0 ? n.toLocaleString() : parseFloat(n.toFixed(2)).toLocaleString();
    items.innerHTML = rawNodes.map(n => {
      const creditStr = n.creditFromByp
        ? ` <span class="rs-credit">(${fmt(n.creditFromByp)} credited)</span>`
        : '';
      return `<div class="rs-item">
        <span class="rs-name">${n.name}</span>
        <span class="rs-val">${fmt(n.outputRate)}/min${creditStr}</span>
      </div>`;
    }).join('');
  }

  // ── TOTALS ──────────────────────────────────────────────────
  function renderTotals({ totalMachines, totalPower, stages, rawNodes, nodes }) {
    document.getElementById('totalsBar').style.display = 'block';
    document.getElementById('totM').textContent = totalMachines.toLocaleString();
    document.getElementById('totP').textContent = totalPower.toLocaleString() + ' MW';
    document.getElementById('totS').textContent = stages;
    document.getElementById('totR').textContent = rawNodes.length;
    document.getElementById('totI').textContent = Object.values(nodes).filter(n => !n.isRaw).length;
  }

  // ── RECIPE SWAP CONTROLS ─────────────────────────────────────
  function renderSwapControls(nodes) {
    const section   = document.getElementById('swapSection');
    const controls  = document.getElementById('swapControls');
    const swappable = Object.entries(nodes)
      .filter(([, v]) => !v.isRaw && v.alts && v.alts.length > 1);

    section.style.display = swappable.length ? 'block' : 'none';
    controls.innerHTML = swappable.map(([name, data]) => `
      <div class="swap-item">
        <div class="swap-name">${name}</div>
        <select class="swap-sel" onchange="App.setRecipe('${name}', this.value)">
          ${data.alts.map(a =>
            `<option value="${a}" ${(state.overrides[name] || 'Basic') === a ? 'selected' : ''}>${a}</option>`
          ).join('')}
        </select>
      </div>`).join('');
  }

  // ── VIEW TOGGLE ─────────────────────────────────────────────
  function setView(view, btn) {
    state.view = view;
    document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
    if (state.result) render();
  }

  // ── RECIPE OVERRIDE ─────────────────────────────────────────
  function setRecipe(item, recipe) {
    state.overrides[item] = recipe;
    if (state.result) solve();
  }

  function onItemChange() {
    state.overrides = {};
    document.getElementById('chainTitle').textContent = 'CLICK CALCULATE CHAIN';
    document.getElementById('chainSub').textContent   = '// Ready to solve';
  }

  // ── URL STATE ───────────────────────────────────────────────
  function updateURL() {
    try {
      const payload = {
        i: state.item, t: state.target, oc: state.oc,
        sl: state.sloop ? 1 : 0, bl: state.beltLimit,
        pl: state.pipeLimit, or: state.overrides,
        bc: state.byproductCredit ? 1 : 0,
      };
      const encoded = btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
      history.replaceState(null, '', `?plan=${encoded}`);
    } catch (e) {}
  }

  function loadFromURL() {
    try {
      const params = new URLSearchParams(window.location.search);
      if (!params.has('plan')) return;
      const d = JSON.parse(decodeURIComponent(escape(atob(params.get('plan')))));
      if (d.i)  { state.item = d.i;      document.getElementById('itemSelect').value  = d.i; }
      if (d.t != null)  { state.target = d.t;    document.getElementById('targetInput').value = d.t; }
      if (d.oc != null) { state.oc = d.oc;       document.getElementById('overclock').value   = d.oc; }
      if (d.bl) { state.beltLimit = d.bl; document.getElementById('beltLimit').value  = d.bl; }
      if (d.pl) { state.pipeLimit = d.pl; document.getElementById('pipeLimit').value  = d.pl; }
      if (d.sl != null) document.getElementById('sloopGlobal').value = d.sl;
      if (d.bc != null) document.getElementById('byproductCredit').value = d.bc;
      if (d.or) state.overrides = d.or;
    } catch (e) {}
  }

  function shareURL() {
    updateURL();
    const url = window.location.href;
    if (navigator.clipboard) {
      navigator.clipboard.writeText(url).then(() => toast('URL COPIED TO CLIPBOARD'));
    } else {
      prompt('Copy this URL:', url);
    }
  }

  // ── SAVE / LOAD ─────────────────────────────────────────────
  function saveBuild() {
    const name = document.getElementById('buildName').value.trim();
    if (!name) { toast('ENTER A BUILD NAME FIRST'); return; }
    readInputs();
    const builds = JSON.parse(localStorage.getItem('fc_builds') || '[]');
    builds.unshift({
      id: Date.now(), name,
      item: state.item, target: state.target,
      oc: state.oc, sloop: state.sloop,
      beltLimit: state.beltLimit, pipeLimit: state.pipeLimit,
      overrides: state.overrides,
      byproductCredit: state.byproductCredit,
      saved: new Date().toLocaleDateString(),
    });
    localStorage.setItem('fc_builds', JSON.stringify(builds.slice(0, 20)));
    document.getElementById('buildName').value = '';
    renderSavedList();
    toast(`BUILD "${name}" SAVED`);
  }

  function loadBuild(id) {
    const builds = JSON.parse(localStorage.getItem('fc_builds') || '[]');
    const entry  = builds.find(b => b.id === id);
    if (!entry) return;
    Object.assign(state, {
      item: entry.item, target: entry.target, oc: entry.oc,
      sloop: entry.sloop, beltLimit: entry.beltLimit,
      pipeLimit: entry.pipeLimit, overrides: entry.overrides || {},
    });
    document.getElementById('itemSelect').value  = entry.item;
    document.getElementById('targetInput').value = entry.target;
    document.getElementById('overclock').value   = entry.oc;
    document.getElementById('beltLimit').value   = entry.beltLimit;
    document.getElementById('pipeLimit').value   = entry.pipeLimit;
    document.getElementById('sloopGlobal').value = entry.sloop ? 1 : 0;
    if (entry.byproductCredit != null) {
      state.byproductCredit = entry.byproductCredit;
      document.getElementById('byproductCredit').value = entry.byproductCredit ? 1 : 0;
    }
    solve();
    toast(`LOADED: ${entry.name}`);
  }

  function deleteBuild(id) {
    let builds = JSON.parse(localStorage.getItem('fc_builds') || '[]');
    builds = builds.filter(b => b.id !== id);
    localStorage.setItem('fc_builds', JSON.stringify(builds));
    renderSavedList();
  }

  function renderSavedList() {
    const builds = JSON.parse(localStorage.getItem('fc_builds') || '[]');
    const el     = document.getElementById('savedList');
    if (!builds.length) { el.innerHTML = ''; return; }
    el.innerHTML = builds.map(b => `
      <div class="saved-item" onclick="App.loadBuild(${b.id})">
        <div>
          <div class="si-name">${b.name}</div>
          <div class="si-meta">${b.item} · ${b.target}/min · ${b.saved}</div>
        </div>
        <button class="si-del" onclick="event.stopPropagation();App.deleteBuild(${b.id})">✕</button>
      </div>`).join('');
  }

  // ── EXPORT ──────────────────────────────────────────────────
  function exportPlan() {
    if (!state.result) { toast('SOLVE A CHAIN FIRST'); return; }
    const { nodes, rawNodes, totalMachines, totalPower } = state.result;
    const fmt  = n => typeof n === 'number' ? (n % 1 === 0 ? n : n.toFixed(2)) : n;
    const lines = [
      `FACTORYCALC — PRODUCTION PLAN`,
      `Item: ${state.item} @ ${state.target}/min`,
      `OC: ${state.oc}% | Belt: ${state.beltLimit}/min | Sloop: ${state.sloop ? 'ON (production only)' : 'OFF'} | Byproduct Credit: ${state.byproductCredit ? 'ON' : 'OFF'}`,
      `Total Machines: ${totalMachines} | Total Power: ${totalPower} MW`,
      `Generated: ${new Date().toLocaleString()}`,
      '', '══ PRODUCTION STAGES ══',
    ];

    Object.entries(nodes)
      .filter(([, v]) => !v.isRaw)
      .sort((a, b) => a[1].depth - b[1].depth)
      .forEach(([name, data]) => {
        lines.push(`\n${name} — ${data.machines} × ${data.building} | ${data.power} MW | ${data.rows}×${data.strLen} layout${data.merged ? ' [MERGED]' : ''}`);
        (data.inputRates || []).forEach(i => lines.push(`  IN:  ${fmt(i.rate)}/min  ${i.item}`));
        lines.push(`  OUT: ${fmt(data.outputRate)}/min  ${name}`);
        if (data.byproductItem) lines.push(`  BY:  ${fmt(data.byproductRate)}/min  ${data.byproductItem}`);
      });

    lines.push('', '══ RAW NODES ══');
    rawNodes.forEach(n => {
      const creditStr = n.creditFromByp ? ` (${fmt(n.creditFromByp)}/min credited)` : '';
      lines.push(`${n.name.padEnd(30)} ${fmt(n.outputRate)}/min${creditStr}`);
    });

    const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `factorycalc_${state.item.replace(/\s+/g,'_')}_${state.target}pm.txt`;
    a.click();
    URL.revokeObjectURL(url);
    toast('PLAN EXPORTED');
  }

  // ── TOAST ───────────────────────────────────────────────────
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2500);
  }

  return { init, solve, setView, setRecipe, onItemChange, shareURL, saveBuild, loadBuild, deleteBuild, exportPlan };
})();

document.addEventListener('DOMContentLoaded', App.init);
