# FactoryCalc — Chronological Change Log

---

### SECTION: 2026-05-29 — Byproduct Credit Feature (v1.5)

**Files**: `solver.js` v1.5, `app.js` v1.5, `index.html` v1.4, `style.css`, `test.js`
**Type**: Feature addition

**Summary**: Added optional byproduct credit post-processing pass to the solver. When enabled, the solver sums all byproduct production across the chain (e.g., Water from Aluminum Scrap, Heavy Oil Residue from Plastic) and reduces matching raw node extraction rates. Toggle in config panel, URL-encoded as `bc` field, persisted in saved builds.

**Implementation**:
- **`solver.js`**: New optional `byproductCredit` param in `solve()`. Post-`calcFromMerged` pass sums `byproductRate` per item across all non-raw nodes, then reduces `rate` and `outputRate` on matching raw nodes by `Math.min(totalByp[name], data.rate)`. Nodes receive `creditFromByp` and `rateBeforeCredit` properties. Result returns `byproductCredits` map `{ needed, credit, net }`.
- **`app.js`**: Added `byproductCredit: false` to state, `readInputs()` reads toggle, `solve()` passes to Solver, URL state includes `bc`, save/load preserves setting, export plan shows credit info.
- **`index.html`**: New `<select id="byproductCredit">` (OFF/ON) in config panel global settings.
- **`style.css`**: `.credit-badge`, `.ns-credit`, `.rs-credit` classes — green-tinted for raw-resource aesthetic.
- **`test.js`**: 2 new tests (29 total) — Water credit reduces raw node, `creditFromByp` property exists.

**UI behavior**:
- Raw node card: "X/min from byproduct credit" badge replaces "No Somersloop" line; NODES stat column replaced with BYPRODUCT CREDIT stat; output rate shows "(net)" annotation
- Raw summary bar: "(X credited)" shown inline after rate
- Export plan: "(X/min credited)" appended to raw node lines
- No change to machine counts, power, or production chain layout

**Key Decisions**:
- Default OFF — byproduct credit is a user opt-in, not silently applied
- Post-processing only — credits never affect machine count or power calculation; they only reduce raw node extraction rates
- Capped at need — `Math.min(byproductTotal, needed)` prevents negative extraction rates
- Creditable byproducts = any item in `RAW_RESOURCES` that is also produced as a byproduct (e.g., Water, Dark Matter Residue)

---

### SECTION: 2026-05-29 — Phase Data Correction + Send to Planner (v1.5)

**Version**: v1.5 (phases.html), v1.4 (other pages)
**Source**: `2026-05-29_1701.md`, `session_progress.md`

**Summary**: All 5 Space Elevator phase requirements corrected against `satisfactory.wiki.gg/wiki/Space_Elevator` — previous data was entirely fabricated from memory. "Send to Planner" deep-link buttons added to every item card. localStorage version migration introduced.

**Key Metrics**:
- 5 phases corrected (wrong items, wrong quantities, wrong tiers across all 5)
- 12 project part ingredient tables sourced from `recipes.js` Basic entries
- "⬡ SEND TO PLANNER" button on each item card → base64 deep-link to Planner
- `STATE_VERSION = 2` introduced — old state auto-discarded on mismatch
- `phases.html` bumped from v1.4 → v1.5 (338 lines)
- 27/27 tests passing

**Notable Corrections**:
- Phase 1: Had Versatile Framework (not a Phase 1 item), inflated quantities (500 each → 50)
- Phase 2: Wrong items entirely (Automated Wiring + Modular Engine instead of Smart Plating + Versatile Framework + Automated Wiring)
- Phase 3: Had ACU/ADS/MFG which are not Phase 3 items
- Phase 4: Had made-up "Magnetic Field Generator (T9)" item; all quantities set to 5000
- Phase 5: Generic single item replaced with 4 specific parts (Nuclear Pasta, Biochemical Sculptor, AI Expansion Server, Ballistic Warp Drive)
- CSS additions: `.phc-btn-row`, `.phc-btn`, `.phc-btn.primary` classes

**Key Decisions**:
- localStorage versioning to auto-purge stale phase state on data schema changes
- Send-to-planner uses base64 encoding with no overrides (`or: {}`) — user switches alts at Planner

---

### SECTION: 2026-05-29 — TSV Cleanup & Database Consolidation

**Version**: v1.4 (recipes.js), v1.5 (solver.js, app.js)
**Source**: `2026-05-29_1626.md`

**Summary**: Audited and removed all duplicate Alternate recipe entries from the `generate_recipes.py` TSV source. Fixed column alignment issues in 3-input recipes. Regenerated `recipes.js` with cleaned data.

**Key Metrics**:
- 24 duplicate TSV lines removed (identically-valued Alt entries, debug lines, misnamed entries)
- 4 TSV column alignment fixes (missing tab separators in Computer, Uranium Fuel Rod, Caterium Computer, Fabric lines)
- Items: 156 → **152**
- Recipe variants: 286 → **275**
- TSV data lines: ~330 → **298** (excluding header)
- Raw resources: **32**
- EW manual-crafted variants: **5**
- All inputs mapped: ✅
- 27/27 tests passing

**Notable Corrections**:
- "Alt: Iron Wire" removed — identical to "Iron Wire" Basic
- "Alt: Heavy Oil Residue" removed — identical to Basic
- "Alt: Smart Plating" removed — identical to Basic
- "Stator (Alt check)" — leftover debug entry removed
- "Packaged Ionized Fuel (basic)" — second duplicate entry removed
- "Concentrated Silica" — misnamed, duplicated Quartz Purification
- "Bolted Modular Frame" vs "Bolted Frame" — duplicate with different labels, identical data
- Column alignment: missing tab made Q_4 read OUT_1 item name in 3-input recipes

**Key Decisions**:
- Prefer Basic over Alternate when I/O values are identical
- Keep first-encountered for same-class duplicates
- Preserve all EW variants (intentionally distinct manual-crafted recipes)
- Remove debug/misnamed entries entirely

---

### SECTION: 2026-05-29 — Nav Pages Overhaul (v1.4)

**Version**: v1.4 (all HTML pages), v1.5 (solver.js, app.js)
**Source**: `2026-05-29_1539.md`

**Summary**: Converted 3 placeholder nav pages into fully interactive JS-driven tools. Added per-node alt recipe dropdowns in the Planner chain view. Implemented mobile-responsive CSS at 900px and 480px breakpoints. Fixed nav link placeholders.

**Key Metrics**:
- `power.html`: Static → JS-driven Power Grid Calculator (5 generator types, OC, demand/margin, localStorage)
- `nodes.html`: Static → JS-driven Resource Node Database (12 resources, Mk.1/2/3 miners, purity, search, grand total)
- `phases.html`: Static → JS-driven Space Elevator Phase Checklist (5 phases, 12 items, progress bars, localStorage)
- `app.js`: v1.4 → v1.5 — per-node inline `<select>` alt dropdowns in node cards
- `solver.js`: v1.4 → v1.5 — minor version bump
- `style.css`: Responsive media queries at 900px (tablet) and 480px (phone) breakpoints
- `.nojekyll` and `.gitignore` files created for GitHub Pages prep
- 27/27 tests passing

**Notable Corrections**:
- Nav links `href="#"` → `href="power.html"`, `href="nodes.html"`, `href="phases.html"`
- Version tags standardized (all pages bumped to v1.4)
- Per-node alt switching moved from swap panel to inline in node cards

**Key Decisions**:
- Each nav page is self-contained (IIFE pattern, no cross-page coupling, no framework dependencies)
- Pages embed own data rather than importing solver/recipes.js — keeps them independent and fast
- Separate localStorage keys per page: `fc_builds`, `factorycalc_power`, `factorycalc_phases`

---

### SECTION: 2026-05-29 — Solver Override Resolution & Architecture

**Version**: v1.5 (solver.js, app.js)
**Source**: `session_progress.md` Build Agents table

**Summary**: Tested all 4 major solver chains to verify override logic and cycle detection. All resolved successfully.

**Key Metrics**:
| Chain | Machines | Power | Stages | Raw Resources |
|---|---|---|---|---|
| Motor @10/min | 62 | 393 MW | 4 | 3 |
| HMF @5/min | 179 | 1,332 MW | 4 | 3 |
| Supercomputer @2/min | 164 | 2,623 MW | 4 | 4 |
| Ficsonium FR @2.5/min | 259 | 6,930 MW | 9 | 14 |

**Notable Corrections**:
- All 4 chains resolve with correct machine counts and power draw
- Cycle detection (`_visiting` Set) correctly flags fluid packaging loops (Alumina, HOR, Fuel)
- Override logic applies recipe swaps to individual branches without global side effects
- Equipment Workshop EW variants intentionally skipped (would overwrite automated Basic recipes)

---

### SECTION: 2026-05-29 — Recipe Data Audit Fixes

**Version**: v1.4 (recipes.js)
**Source**: `session_progress.md` Build Agents table

**Summary**: Batch 2 audit corrections applied across `recipes.js` and `generate_recipes.py`. Fixed naming, output rates, missing recipes, and missing items.

**Key Metrics**:
- Rocket Fuel output: 150 → **100** (corrected)
- "Encoder" → "Quantum Encoder": **8 fixes** in `recipes.js`, **7 fixes** in TSV source
- "Neural Processor" → "Neural-Quantum Processor": **3 fixes** in `recipes.js`, **6 fixes** in TSV source
- Beacon entry removed entirely (deprecated item)
- HIGH severity fixes: DMR, Ficsonium, FFR, DMC, Cooling Device, APM, EPM, Dark Matter Trap
- 8 missing automated recipes added (Black Powder Assembler, Nobelisk/Gas/Pulse Assembler, Nuke Nobelisk MFR, Explosive Rebar MFR, Shatter/Stun Rebar Assembler)
- 9 missing items added (4 Medicinal Inhaler variants, Gas Mask, Nobelisk Detonator, Rebar Gun, Factory Cart, Golden Factory Cart)
- `python3 generate_recipes.py` run to sync `recipes.js` from fixed TSV

---

### SECTION: 2026-05-28 — Initial Development & v1.1

**Version**: v1.1 (Pioneer Edition)
**Sources**: `2026-05-28.md`, `2026-05-28-update.md`, `Session_Summary_2026-05-28.md`

**Summary**: Project inception. Phase 1 single-item full-chain solver implemented in `solver.js` with two-pass recursive accumulation and merged calculation. 3 critical bugs identified and fixed in a 51-minute session. URL state audit completed (9.4/10). OpenCode API configuration established.

**Key Metrics**:
- 3 critical bugs fixed (Byproduct Sloop multiplication, Alt Recipe Web Lookup, Sloop Machine Count Stability)
- AltRecipeFetcher module created with 3-tier lookup: cache → web API → estimation
- URL State Audit: 7 test categories passed, security score 9.4/10
- Total fix time: 51 minutes (4 min ahead of 55-min estimate)
- Files modified: 3 (solver.js, recipes.js, app.js)
- Lines changed: 90+
- Session stats: 15+ test cases, 2 code reviews, 2 audit reports
- OpenCode API config: `~/.config/opencode/opencode.jsonc` with env variable substitution

**Notable Corrections**:
- **Bug #1**: Byproduct missing `outputMult` factor — `machines * qty` → `machines * qty * ocMult * sloopMult`
- **Bug #2**: Alt recipes only updated label, not data — added full web fetch + cache + apply + re-solve pipeline
- **Bug #3**: Sloop was changing machine count — separated concerns: machine count = `target / (baseOutput × oc)`, actual output = `machines × baseOutput × oc × sloop`
- Sloop math overhaul: sloop amplifies output only (does not reduce machines needed)
- Web sources verified: satisfactory-calculator.com (primary API) + satisfactory.wiki.gg (fallback HTML)
- `"test"` string on index.html:11 removed

**Key Decisions**:
- Depth over breadth: polish Phase 1 with 306 recipes before Phase 2 multi-item work
- Cache-first, web-fallback, graceful degradation for alt recipe lookup
- localStorage cache (`fc_alt_recipes`) with 7-day TTL

---

### APPENDIX: Legacy State (pre-May 28)

**Version**: v3 (save state)
**Source**: `save_state.md`

**Summary**: Original project architecture and design decisions documented as "Save State v3". Earliest conceptual foundations derived from Google Sheets Plant Builder.

**Architecture**:
- Palette: Amber & Obsidian (`#0C0A06`, `#FFB300`, `#FFD54F`)
- Fonts: Rajdhani (headers), Share Tech Mono (data), Barlow (body)
- Tone: 80% FICSIT game lore, 20% no-nonsense
- Solver: Pass 1 recursive accumulation → Pass 2 merge + calculate
- Shared resources merged (Option B) — Iron Rod calculated once for combined demand
- Raw nodes (ore, oil, water) = chain stop point

**Code of Conduct**:
- Never delete without reading first
- Always ask authorization before deletion
- Undo actions when requested
- Config directory changes require explicit confirmation

**JS Layers Planned**:
1. Full 306-recipe JSON data object
2. Central AppState store
3. URL state encoder/decoder (was NEXT)
4. localStorage build persistence
5. REST API calls (Phase 2)
6. Web Workers for large chains
7. D3.js node graph visualization

**Google Sheets Reference**:
- Config tab layout: CLASS / RECIPE_NAME / BUILDING / MW / IN/Q pairs
- VLOOKUP range: `Config!$C:$AU`
- Named ranges: PreSort, RecipeDropdown
- Recipe database: `Satisfactory_1.1_All_Recipes.tsv` — 306 recipes (159 Basic, 128 Alt, 19 Quantum)

**Site Pages Planned**:
`/` (Landing), `/planner`, `/recipes`, `/power`, `/nodes`, `/trains`, `/phases`

---
