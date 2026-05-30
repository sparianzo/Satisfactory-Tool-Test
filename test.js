const fs = require('fs');

// ── Load recipes.js ──
var RAW_RESOURCES, RECIPES, ITEM_LIST;
let rCode = fs.readFileSync('recipes.js', 'utf8');
rCode = rCode.replace(/^const (RAW_RESOURCES|RECIPES|ITEM_LIST)\s*=/gm, '$1 =');
eval(rCode);

// ── Load solver.js ──
var Solver;
let sCode = fs.readFileSync('solver.js', 'utf8');
sCode = sCode.replace(/^const (Solver)\s*=/gm, '$1 =');
eval(sCode);

// ── Helpers ──
const PASS = '\u2713 PASS';
const FAIL = '\u2717 FAIL';
let passed = 0, failed = 0, testNum = 0;

function test(name, fn) {
  testNum++;
  try {
    fn();
    console.log(`  ${PASS}  Test ${testNum}: ${name}`);
    passed++;
  } catch (e) {
    console.log(`  ${FAIL}  Test ${testNum}: ${name}`);
    console.log(`         ${e.message}`);
    failed++;
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg || 'Assertion failed');
}

// Overrides to break packager cycles (unpackaging→repackaging loops)
const FLUID_OVERRIDES = {
  'Alumina Solution': 'Alt: Sloppy Alumina',
  'Fuel': 'Alt: Diluted Fuel',
};

function solve(item, target, opts = {}) {
  return Solver.solve({
    item,
    target,
    oc: opts.oc ?? 100,
    sloop: opts.sloop ?? false,
    beltLimit: opts.beltLimit ?? 780,
    pipeLimit: opts.pipeLimit ?? 600,
    overrides: opts.overrides ?? {},
    byproductCredit: opts.byproductCredit ?? false,
  });
}

// ═══════════════════════════════════════════════════════════════
//  TEST 1: Recipe Database Integrity
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 1: Recipe Database Integrity');
console.log(`${'='.repeat(60)}`);

test('RECIPES is a non-null object', () => {
  assert(RECIPES && typeof RECIPES === 'object' && !Array.isArray(RECIPES));
});

test('Every item has a non-empty alts array', () => {
  Object.keys(RECIPES).forEach(item => {
    const entry = RECIPES[item];
    assert(entry.alts && Array.isArray(entry.alts) && entry.alts.length > 0,
      `Item "${item}" missing or empty alts`);
  });
});

test('Every alt key name exists in the item\'s recipes map', () => {
  Object.keys(RECIPES).forEach(item => {
    const entry = RECIPES[item];
    entry.alts.forEach(alt => {
      assert(entry.recipes[alt], `Item "${item}" alt "${alt}" missing from recipes map`);
    });
  });
});

test('Every recipe has valid building, mw, output, and inputs', () => {
  Object.keys(RECIPES).forEach(item => {
    const entry = RECIPES[item];
    Object.entries(entry.recipes).forEach(([name, rec]) => {
      assert(typeof rec.building === 'string' && rec.building.length > 0,
        `Item "${item}" recipe "${name}" invalid building`);
      assert(typeof rec.mw === 'number' && rec.mw >= 0,
        `Item "${item}" recipe "${name}" invalid mw: ${rec.mw}`);
      assert(typeof rec.output === 'number' && rec.output >= 0,
        `Item "${item}" recipe "${name}" invalid output: ${rec.output}`);
      assert(Array.isArray(rec.inputs),
        `Item "${item}" recipe "${name}" inputs not an array`);
      rec.inputs.forEach((inp, i) => {
        assert(typeof inp.item === 'string' && typeof inp.qty === 'number',
          `Item "${item}" recipe "${name}" input[${i}] invalid: ${JSON.stringify(inp)}`);
      });
    });
  });
});

test('No input references an item absent from RECIPES and RAW_RESOURCES', () => {
  const allKnown = new Set([...RAW_RESOURCES, ...Object.keys(RECIPES)]);
  Object.keys(RECIPES).forEach(item => {
    const entry = RECIPES[item];
    Object.entries(entry.recipes).forEach(([name, rec]) => {
      rec.inputs.forEach(inp => {
        assert(allKnown.has(inp.item),
          `Item "${item}" recipe "${name}" input "${inp.item}" not in RECIPES or RAW_RESOURCES`);
      });
    });
  });
});

test('Print item/recipe count summary', () => {
  const itemCount = Object.keys(RECIPES).length;
  let recipeCount = 0;
  Object.values(RECIPES).forEach(entry => { recipeCount += Object.keys(entry.recipes).length; });
  console.log(`         Total items: ${itemCount}, Total recipes: ${recipeCount}`);
  assert(itemCount > 0 && recipeCount > 0, 'No items or recipes found');
});

// ═══════════════════════════════════════════════════════════════
//  TEST 2: Raw Resources
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 2: Raw Resources');
console.log(`${'='.repeat(60)}`);

test('RAW_RESOURCES is a Set containing known resources', () => {
  assert(RAW_RESOURCES instanceof Set, 'RAW_RESOURCES is not a Set');
  ['Iron Ore', 'Copper Ore', 'Limestone', 'Coal', 'Water', 'Crude Oil',
   'Sulfur', 'Raw Quartz', 'Caterium Ore', 'Bauxite', 'Nitrogen Gas', 'SAM'].forEach(name => {
    assert(RAW_RESOURCES.has(name), `Missing expected raw resource: "${name}"`);
  });
});

test('Raw resources in RECIPES are production alts, not consumption recipes', () => {
  const both = [...RAW_RESOURCES].filter(name => name in RECIPES);
  // Items can appear in both: e.g. Coal has Biocoal/Charcoal alts for producing it.
  // The solver treats them as raw first (stops recursion at RAW_RESOURCES check).
  // Verify the dual entries are production-oriented (not loops that consume themselves).
  both.forEach(name => {
    const entry = RECIPES[name];
    Object.values(entry.recipes).forEach(rec => {
      rec.inputs.forEach(inp => {
        assert(inp.item !== name,
          `Raw resource "${name}" recipe consumes itself: ${JSON.stringify(inp)}`);
      });
    });
  });
  if (both.length > 0) {
    console.log(`         Items in both RAW_RESOURCES and RECIPES: ${both.join(', ')}`);
  }
});

test('Print raw resource count', () => {
  console.log(`         Total raw resource types: ${RAW_RESOURCES.size}`);
  assert(RAW_RESOURCES.size >= 20, 'Expected at least 20 raw resources');
});

// ═══════════════════════════════════════════════════════════════
//  TEST 3: Smoke Tests — Basic Chain Resolution
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 3: Smoke Tests — Basic Chain Resolution');
console.log(`${'='.repeat(60)}`);

const BASIC_CHAINS = [
  ['Iron Ingot', 100],
  ['Iron Plate', 50],
  ['Screw', 200],
  ['Concrete', 100],
];

BASIC_CHAINS.forEach(([item, target]) => {
  test(`"${item}" @ ${target}/min resolves with sensible totals`, () => {
    const result = solve(item, target);
    const nonRaw = Object.values(result.nodes).filter(n => !n.isRaw);
    assert(result.totalMachines > 0, 'Machines must be > 0');
    assert(result.totalPower > 0, 'Power must be > 0');
    assert(nonRaw.length > 0, 'Must have unique production items');
    assert(result.rawNodes.length > 0, 'Must have raw resources');
  });
});

// ═══════════════════════════════════════════════════════════════
//  TEST 4: Complex Chain Resolution
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 4: Complex Chain Resolution');
console.log(`${'='.repeat(60)}`);

const COMPLEX_CHAINS = [
  { item: 'Motor',           target: 10, minMachines: 8,  label: '~10+' },
  { item: 'Heavy Modular Frame', target: 5,  minMachines: 20, label: '~30+' },
  { item: 'Supercomputer',   target: 2,  minMachines: 30, label: '~50+', overrides: FLUID_OVERRIDES },
];

COMPLEX_CHAINS.forEach(({ item, target, minMachines, label, overrides }) => {
  test(`"${item}" @ ${target}/min resolves without error`, () => {
    const result = solve(item, target, { overrides: overrides || {} });
    assert(result.totalMachines > 0, 'No machines');
    assert(result.totalPower > 0, 'No power');
    assert(result.stages > 0, 'No stages');
    const nonRaw = Object.values(result.nodes).filter(n => !n.isRaw);
    assert(nonRaw.length > 0, 'No unique items');
    assert(result.rawNodes.length > 0, 'No raw resources');
  });

  test(`"${item}" @ ${target}/min has ${label} machines`, () => {
    const result = solve(item, target, { overrides: overrides || {} });
    console.log(`         ${item}: ${result.totalMachines} machines, ${result.totalPower} MW, ${result.stages} stages, ${result.rawNodes.length} raw resources`);
    assert(result.totalMachines >= minMachines,
      `Expected >= ${minMachines} machines, got ${result.totalMachines}`);
  });
});

// ═══════════════════════════════════════════════════════════════
//  TEST 5: Byproduct Handling
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 5: Byproduct Handling');
console.log(`${'='.repeat(60)}`);

test('"Ficsonium Fuel Rod" @ 2.5/min has byproducts in the chain', () => {
  const result = solve('Ficsonium Fuel Rod', 2.5, { overrides: FLUID_OVERRIDES });
  const nodes = Object.values(result.nodes);
  const bypNodes = nodes.filter(n => n.byproductItem);
  assert(bypNodes.length > 0, 'No byproducts found in chain');
  console.log(`         Machines: ${result.totalMachines}, Power: ${result.totalPower} MW`);
  console.log(`         Stages: ${result.stages}, Raw resources: ${result.rawNodes.length}`);
  bypNodes.forEach(n => {
    console.log(`         Byproduct: ${n.byproductItem} @ ${n.byproductRate}/min (from ${n.name})`);
  });
  // Ficsonium Fuel Rod itself has Dark Matter Residue byproduct
  const targetNode = result.nodes['Ficsonium Fuel Rod'];
  assert(targetNode, 'Target node missing');
  assert(targetNode.byproductItem === 'Dark Matter Residue',
    `Expected Dark Matter Residue byproduct, got ${targetNode.byproductItem}`);
  assert(targetNode.byproductRate > 0, 'Byproduct rate should be > 0');
});

test('"Aluminum Scrap" @ 360/min with byproductCredit reduces Water raw node', () => {
  const resultOff = solve('Aluminum Scrap', 360);
  const resultOn  = solve('Aluminum Scrap', 360, { byproductCredit: true });
  const waterOff  = resultOff.rawNodes.find(r => r.name === 'Water');
  const waterOn   = resultOn.rawNodes.find(r => r.name === 'Water');
  assert(waterOff, 'No Water raw node without credit');
  assert(waterOn, 'No Water raw node with credit');
  console.log(`         Water raw: ${waterOff.outputRate.toFixed(2)}/min (credit off), ${waterOn.outputRate.toFixed(2)}/min (credit on)`);
  assert(waterOn.outputRate < waterOff.outputRate,
    `Expected Water rate to drop with credit, stayed at ${waterOn.outputRate} vs ${waterOff.outputRate}`);
  const credit = resultOn.byproductCredits;
  assert(credit && credit['Water'], 'Expected byproductCredits.Water in result');
  console.log(`         Water credit: ${credit['Water'].credit.toFixed(2)}/min (needed ${credit['Water'].needed.toFixed(2)}, net ${credit['Water'].net.toFixed(2)})`);
  assert(credit['Water'].credit > 0, 'Water credit should be > 0');
});

test('"Aluminum Scrap" @ 360/min with byproductCredit has creditFromByp on raw node', () => {
  const result = solve('Aluminum Scrap', 360, { byproductCredit: true });
  const waterNode = result.nodes['Water'];
  assert(waterNode, 'No Water node');
  assert(waterNode.creditFromByp !== undefined, 'Water node missing creditFromByp');
  assert(waterNode.creditFromByp > 0, 'creditFromByp should be > 0');
  assert(waterNode.rateBeforeCredit !== undefined, 'Water node missing rateBeforeCredit');
  assert(waterNode.rateBeforeCredit > waterNode.outputRate,
    `rateBeforeCredit (${waterNode.rateBeforeCredit}) should exceed outputRate (${waterNode.outputRate})`);
});

// ═══════════════════════════════════════════════════════════════
//  TEST 6: Alternate Recipe Selection
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 6: Alternate Recipe Selection');
console.log(`${'='.repeat(60)}`);

test('"Motor" @ 10/min with Pure Iron Ingot override reduces Iron Ore usage', () => {
  const resultDefault = solve('Motor', 10);
  const ironDefault = resultDefault.rawNodes.find(r => r.name === 'Iron Ore');
  assert(ironDefault, 'No Iron Ore in default chain');

  const resultAlt = solve('Motor', 10, { overrides: { 'Iron Ingot': 'Alt: Pure Iron Ingot' } });
  const ironAlt = resultAlt.rawNodes.find(r => r.name === 'Iron Ore');
  assert(ironAlt, 'No Iron Ore in alt chain');

  console.log(`         Iron Ore: default=${ironDefault.outputRate.toFixed(2)}/min, pure alt=${ironAlt.outputRate.toFixed(2)}/min`);
  assert(ironAlt.outputRate < ironDefault.outputRate,
    `Expected less Iron Ore with alt, got ${ironAlt.outputRate} vs ${ironDefault.outputRate}`);

  const ingotNode = resultAlt.nodes['Iron Ingot'];
  assert(ingotNode, 'Iron Ingot node missing in alt');
  assert(ingotNode.recipe === 'Alt: Pure Iron Ingot',
    `Expected "Alt: Pure Iron Ingot", got "${ingotNode.recipe}"`);
});

// ═══════════════════════════════════════════════════════════════
//  TEST 7: Overclock Settings
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 7: Overclock Settings');
console.log(`${'='.repeat(60)}`);

test('"Iron Plate" @ 50/min at 200% OC uses fewer machines than at 100%', () => {
  const result100 = solve('Iron Plate', 50, { oc: 100 });
  const result200 = solve('Iron Plate', 50, { oc: 200 });
  console.log(`         Machines: ${result100.totalMachines} @ 100%, ${result200.totalMachines} @ 200%`);
  assert(result200.totalMachines < result100.totalMachines,
    `Expected fewer machines at 200%, got ${result200.totalMachines} >= ${result100.totalMachines}`);
});

// ═══════════════════════════════════════════════════════════════
//  TEST 8: Belt Limit
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 8: Belt Limit');
console.log(`${'='.repeat(60)}`);

test('"Motor" @ 10/min with belt limit 60 (Mk2) still resolves', () => {
  const result = solve('Motor', 10, { beltLimit: 60 });
  assert(result.totalMachines > 0, 'No machines with belt limit 60');
  assert(result.totalPower > 0, 'No power with belt limit 60');
  const hasBelts = Object.values(result.nodes).some(n => n.belts !== undefined && n.belts !== null);
  assert(hasBelts, 'No belt counts computed');
  console.log(`         Machines: ${result.totalMachines}, Power: ${result.totalPower} MW`);
});

// ═══════════════════════════════════════════════════════════════
//  TEST 9: Error Handling
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 9: Error Handling');
console.log(`${'='.repeat(60)}`);

test('Unknown item not in RECIPES is treated as raw/extraction node', () => {
  const result = solve('NonExistentItem', 10);
  const node = result.nodes['NonExistentItem'];
  assert(node, 'Missing node in result');
  assert(node.isRaw === true, 'Unknown item should be treated as raw');
});

test('Target quantity of 0 returns zero machines and power', () => {
  const result = solve('Iron Ingot', 0);
  assert(result.totalMachines === 0, `Expected 0 machines, got ${result.totalMachines}`);
  assert(result.totalPower === 0, `Expected 0 power, got ${result.totalPower}`);
});

test('Invalid override name falls back to default (first alt) recipe', () => {
  const result = solve('Iron Ingot', 100, { overrides: { 'Iron Ingot': 'Alt: NonExistentRecipe' } });
  const node = result.nodes['Iron Ingot'];
  assert(node, 'Missing Iron Ingot node');
  assert(node.recipe !== 'Alt: NonExistentRecipe', 'Should have fallen back');
  assert(node.recipe === 'Basic', `Expected fallback to "Basic", got "${node.recipe}"`);
});

// ═══════════════════════════════════════════════════════════════
//  TEST 10: Result Structure via Solver.solve()
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  TEST 10: Merge & Totals');
console.log(`${'='.repeat(60)}`);

test('Solver.solve returns correct totals structure with Motor @ 10/min', () => {
  const result = solve('Motor', 10);
  assert(typeof result.totalMachines === 'number' && result.totalMachines > 0, 'totalMachines invalid');
  assert(typeof result.totalPower === 'number' && result.totalPower > 0, 'totalPower invalid');
  assert(typeof result.stages === 'number' && result.stages > 0, 'stages invalid');
  assert(Array.isArray(result.rawNodes) && result.rawNodes.length > 0, 'rawNodes invalid');
  assert(result.nodes && typeof result.nodes === 'object', 'nodes invalid');
  assert(result.byDepth && typeof result.byDepth === 'object', 'byDepth invalid');

  const nonRaw = Object.values(result.nodes).filter(n => !n.isRaw);
  const uniqueItems = nonRaw.length;

  console.log(`         Machines: ${result.totalMachines}`);
  console.log(`         Power: ${result.totalPower} MW`);
  console.log(`         Stages: ${result.stages}`);
  console.log(`         Unique production items: ${uniqueItems}`);
  console.log(`         Raw resources: ${result.rawNodes.length}`);

  assert(uniqueItems > 0, 'No unique production items');
  assert(result.rawNodes.length > 0, 'No raw resources');
});

// ═══════════════════════════════════════════════════════════════
//  SUMMARY
// ═══════════════════════════════════════════════════════════════
console.log(`\n${'='.repeat(60)}`);
console.log('  FINAL SUMMARY');
console.log(`${'='.repeat(60)}`);
console.log(`  ${passed}/${passed + failed} tests passed`);
if (failed > 0) {
  console.log(`  ${FAIL}  ${failed} test(s) FAILED`);
  process.exit(1);
} else {
  console.log(`  ${PASS}  ALL TESTS PASSED`);
}
