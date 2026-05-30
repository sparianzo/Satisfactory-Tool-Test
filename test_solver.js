const fs = require('fs');

// ── Load recipes.js (convert const→var so evaled vars leak to our scope) ──
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

/** Recursively build a tree from root item using each node's inputRates */
function buildTree(itemName, nodes, visited = new Set()) {
  if (visited.has(itemName)) return { name: itemName, children: [], loop: true };
  visited.add(itemName);
  const node = nodes[itemName];
  if (!node || node.isRaw) return { name: itemName, children: [], isRaw: true, node };
  const children = [];
  if (node.inputRates) {
    for (const inp of node.inputRates) {
      children.push(buildTree(inp.item, nodes, new Set(visited)));
    }
  }
  return { name: itemName, children, isRaw: false, node };
}

/** Print a tree with box‑drawing chars */
function printTree(tree, nodes, indent = '', isLast = true) {
  const node = tree.node || nodes[tree.name];
  const prefix = indent + (isLast ? '  \u2514\u2500 ' : '  \u251C\u2500 ');
  const childPrefix = indent + (isLast ? '    ' : '  \u2502  ');

  if (tree.loop) {
    console.log(`${prefix}${tree.name}  (cycle — skipped)`);
    return;
  }

  if (!node || tree.isRaw) {
    const rate = node ? node.outputRate.toFixed(2) : '?';
    console.log(`${prefix}${tree.name}  (RAW)  ${rate}/min`);
    return;
  }

  const rateStr = node.outputRate.toFixed(2);
  const machineStr = `${node.machines} \u00d7 ${node.building}`;
  const powerStr = `${node.power} MW`;
  const bypStr = node.byproductItem
    ? `  \u21b3 ${node.byproductRate.toFixed(2)} ${node.byproductItem}/min`
    : '';
  const recipeStr = `[${node.recipe}]`;

  console.log(`${prefix}${tree.name}  ${rateStr}/min  ${machineStr}  ${powerStr}  ${recipeStr}${bypStr}`);

  if (node.inputRates && node.inputRates.length > 0) {
    const inStr = node.inputRates.map(i => `${i.rate.toFixed(2)} ${i.item}/min`).join(', ');
    console.log(`${childPrefix}inputs: ${inStr}`);
  }

  for (let i = 0; i < tree.children.length; i++) {
    printTree(tree.children[i], nodes, childPrefix, i === tree.children.length - 1);
  }
}

// ── Test chains ──

// Many fluid items have "Basic" recipes that are just unpackaging (Packager)
// but require the packaged version, creating infinite loops:
//   e.g. Alumina Solution Basic → Packaged Alumina Solution → Alumina Solution
// Overrides break these cycles by using the direct-production alt recipes.
const FLUID_OVERRIDES = {
  'Alumina Solution': 'Alt: Sloppy Alumina',
  'Heavy Oil Residue': 'Alt: Heavy Oil Residue',
  'Fuel': 'Alt: Diluted Fuel',
};

const chains = [
  { name: 'Motor', target: 10 },
  { name: 'Heavy Modular Frame', target: 5 },
  { name: 'Ficsonium Fuel Rod', target: 2.5, overrides: FLUID_OVERRIDES },
  { name: 'Supercomputer', target: 2, overrides: FLUID_OVERRIDES },
];

for (const { name, target, overrides = {} } of chains) {
  console.log(`\n${'\u2550'.repeat(72)}`);
  console.log(`  ${name}  @  ${target}/min`);
  if (Object.keys(overrides).length > 0) {
    console.log(`  overrides: ${JSON.stringify(overrides)}`);
  }
  console.log(`${'\u2550'.repeat(72)}`);

  try {
    const result = Solver.solve({
      item: name, target,
      oc: 100, sloop: false,
      beltLimit: 780, pipeLimit: 600,
      overrides,
    });

    const nodes = result.nodes;
    const nonRaw = Object.values(nodes).filter(n => !n.isRaw);
    const uniqueItems = nonRaw.length;

    console.log(`\n  TOTALS`);
    console.log(`    Machines:      ${result.totalMachines}`);
    console.log(`    Power:         ${result.totalPower} MW`);
    console.log(`    Stages:        ${result.stages}`);
    console.log(`    Unique items:  ${uniqueItems}`);

    console.log(`\n  RAW RESOURCES`);
    const sortedRaw = [...result.rawNodes].sort((a, b) => b.outputRate - a.outputRate);
    if (sortedRaw.length === 0) {
      console.log('    (none)');
    } else {
      for (const r of sortedRaw) {
        console.log(`    ${r.name.padEnd(28)} ${r.outputRate.toFixed(2)}/min`);
      }
    }

    console.log(`\n  CHAIN TREE`);
    const tree = buildTree(name, nodes);
    if (tree.isRaw || tree.loop) {
      console.log(`    Target not found in solution`);
    } else {
      printTree(tree, nodes);
    }

  } catch (err) {
    console.log(`\n  ERROR: ${err.message}`);
    console.log(`  ${err.stack ? err.stack.split('\n').slice(0, 3).join('\n  ') : ''}`);
  }
}

console.log(`\n${'\u2550'.repeat(72)}`);
console.log('  ALL TESTS COMPLETE');
console.log(`${'\u2550'.repeat(72)}\n`);
