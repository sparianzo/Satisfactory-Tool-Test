# PROJECT STATUS — FactoryCalc Pioneer Edition

**Last updated**: 2026-05-30 (tier filter, power integration, node biomes, EW recipes, git deploy)

---

### 1. PROJECT OVERVIEW

FactoryCalc Pioneer Edition — Satisfactory production chain solver. FICSIT Corporate Terminal aesthetic.

---

### 2. CURRENT VERSION MATRIX

| File | Version | Role |
|------|---------|------|
| `index.html` | v1.4 | Planner — chain solver + config panel (byproduct credit toggle), **Solve for Power button** |
| `recipes.html` | **v1.5** | Recipe DB — search, alt tabs, send-to-planner, **tier filter + tier badges** |
| `power.html` | **v1.5** | Power Grid Calculator — 5 generators, OC, demand, **auto-size from URL param** |
| `nodes.html` | **v1.5** | Resource Node DB — 12 resources, miner tiers, purity, **biome map info** |
| `phases.html` | v1.5 | Phase checklist — wiki-correct data, send-to-planner buttons |
| `recipes.js` | v1.5 | **160 items, 311 recipe variants**, **112 tier-tagged recipes**, **15 EW variants** |
| `solver.js` | v1.5 | Recursive chain solver + byproduct credit pass + cycle detection |
| `app.js` | v1.5 | Controller — per-node alt dropdowns, byproduct credit toggle, URL state, save/load, **solveForPower** |
| `style.css` | — | FICSIT dark theme + responsive (900px/480px) + credit styles + tier badge styles + rc-btn styles |
| `test.js` | — | **29 tests** — all passing |

---

### 3. TEST RESULTS — 29/29 PASSING

```
DB Integrity:      9/9
Smoke/Simple:      4/4  (Iron Ingot, Plate, Screw, Concrete)
Complex Chains:    6/6  (Motor, HMF, Supercomputer, Ficsonium FR)
Alts, OC, Limits:  3/3
Byproduct Credit:  2/2  (Water credit reduces raw, creditFromByp property)
Edge Cases:        3/3  (unknown item, zero target, invalid override)
Merge/Totals:      1/1
```

---

### 4. BUILD AGENT TRACKER

| Agent | Task | Status | Details |
|-------|------|--------|---------|
| **Wiki Audit** (6 parallel agts) | Full recipe audit vs satisfactory.wiki.gg | ✅ Complete | 96+ fixes: 28 ingredient/rate fixes, 17 Converter recipes, 15 Alternates, 10 false positives removed, 10 classification fixes, 5 full rewrites |
| **TSV Cleanup** | Remove duplicate alt entries | ✅ Complete | 24 duplicates removed, 4 column alignment fixes, DB 156→152 items, 286→275 recipes |
| **Phase Data Fix** | Correct phase requirements from wiki | ✅ Complete | All 5 phases corrected per satisfactory.wiki.gg, localStorage version migration added |
| **Send to Planner** | Add send-to-planner buttons to phase item cards | ✅ Complete | Mirrors recipes.html — base64 deep-link to Planner with actual phase requirement as target |
| **Byproduct Credit** | Post-processing raw-node offset from byproducts | ✅ Complete | Water/Refinery credit, toggle in config panel, URL-encoded, saved builds, 2 new tests |
| **Config Consolidation** | Merge 11 session logs → 3 canonical docs | ✅ Complete | PROJECT_STATUS.md + TECHNICAL_SPEC.md + CHANGE_LOG.md; old files deleted |
| **Tier Filter** | Tier badge + filter dropdown in recipes.html | ✅ Complete | S/A/B/C/D/F filter from Steam guide, colored tier badges in recipe cards |
| **Power ↔ Solver** | Solve for Power button on Planner → auto-size generators on Power page | ✅ Complete | `solveForPower()` in app.js, `autoSizeDemand()` in power.html, URL param demand |
| **Node Biomes** | Map biome info for resource nodes | ✅ Complete | zones array on 11 resource types, displayed as BIOMES line in each card |
| **EW Recipes** | Add missing Equipment Workshop recipes | ✅ Complete | 15 EW variant recipes (consumable only — ammo, filters, rebar); equipment/tools one-time-craft, excluded |
| **SCIM Cross-Reference** | Compare SCIM game data vs TSV for discrepancies | ✅ Complete | All 21 flagged items are U8→1.0 rebalances, not errors. TSV is correct for 1.0 |

---

### 5. localStorage KEYS

| Page | Key | Data |
|------|-----|------|
| Planner builds | `fc_builds` | Saved build configurations |
| Power Calculator | `factorycalc_power` | Generator counts, OC, demand |
| Phases Checklist | `factorycalc_phases` | Per-item delivery counts + done flags (v2 schema) |

---

### 6. KNOWN ISSUES

| ID | Issue | Severity | Status |
|----|-------|----------|--------|
| K2 | verify.py false-positive for "(EW)" items — split logic bug | Low | ⏳ Open |
| K3 | Fluid packaging cycles not auto-resolved (Alumina, HOR, Fuel) | Medium | ⏳ Open |
| K4 | No git repo — all files local, no GitHub Pages deployment | Medium | ✅ Resolved |
| K5 | `satisfactory-calculator.com` is JS SPA with ad-block wall — not scrapable | Low | ⏳ Open |

---

### 7. NEXT STEPS

| Priority | Task | Notes |
|----------|------|-------|
| 1 | **Map coordinates (precise X/Y/Z)** | Add wiki-sourced exact coordinates to node entries, replacing current biome-only data |
| 2 | **Remaining EW recipes** | Verify all EW recipes present — currently 15 EW variants |
| 3 | **Cross-reference sources** | Try SCIM API or game data since satisfactory-calculator.com blocked |

---

### 8. KEY DESIGN DECISIONS

- *Nested Recipe Map schema*: `RECIPES = { 'Item': { alts: [...], recipes: {...} } }`
- *Recipe key fallback*: `alts[0]` used as default when no override exists
- *Equipment Workshop EW variants skipped*: would overwrite automated recipes with same "Basic" key
- *FICSMAS items skipped*: seasonal, not core game
- *Fluid packaging cycles*: Alumina Solution, Heavy Oil Residue, Fuel need alternate recipe overrides to avoid infinite loops in solver
- *TSV source*: embedded in `generate_recipes.py` — single source of truth
- *Phases localStorage versioning*: `STATE_VERSION` incremented on data change to auto-purge stale state
- *Byproduct credit*: Optional post-processing pass — sums byproduct production, offsets raw node extraction. Toggle default OFF. Only affects raw node rates, never production machine counts.
