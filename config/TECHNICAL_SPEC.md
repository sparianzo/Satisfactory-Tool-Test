# FactoryCalc — Pioneer Edition — Technical Specification

> Consolidated technical reference document.
> FICSIT Incorporated — Internal Use — PROPRIETARY

---

### 1. DESIGN PHILOSOPHY

**FICSIT Corporate / Industrial Terminal Aesthetic** — utilitarian, data-dense interface styled as a Pioneer's build station aboard the HUB.

| Token | Hex | Usage |
|-------|-----|-------|
| Dark Obsidian | `#0C0A06` | Primary background, card surfaces |
| Warm Cream | `#FFF8E1` | Body text, primary foreground |
| Gold | `#FFD54F` | Accents, headers, borders |
| Amber | `#FFB300` | Interactive states, hover highlights |
| Grid Overlay | `repeating-linear-gradient` | Background texture simulating FICSIT blueprints |

**Typography:**

| Font | Role | Fallback |
|------|------|----------|
| Rajdhani (700) | Headers | sans-serif |
| Share Tech Mono | Data tables, machine stats, rates | monospace |
| Barlow | Body copy, descriptions | sans-serif |

**Tagline:** *"Efficiency. Compliance. Profit."* — displayed across all pages.

**Nav Page Pattern:** Each nav page is a self-contained static HTML file with an inline `<script>` IIFE module (e.g., `PowerCalc`, `NodesApp`, `PhasesApp`). State persists via per-page `localStorage` keys. No cross-page state coupling and no shared dependencies — pages open directly without going through the Planner. No frameworks; pure vanilla JS.

---

### 2. DATA ARCHITECTURE

**Source of Truth:** All recipe data originates in an embedded 17-column TSV inside `generate_recipes.py` (487 lines). The Python script parses the TSV, validates columns, and emits `recipes.js` with the nested RECIPES structure. Manual edits to `recipes.js` are forbidden.

**TSV Column Specification (17 columns):**

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | CLASS | String | `Basic`, `Alternate`, or (EW) marker |
| 2 | RECIPE_NAME | String | Human-readable recipe name |
| 3 | BUILDING | String | Machine class (e.g., Constructor, Smelter, Refinery) |
| 4 | MW | Float | Power draw at 100% clock speed |
| 5–12 | IN_1–IN_4, Q_1–Q_4 | String/Float | Input items and rates (blank if N/A) |
| 13–14 | OUT_1, Q_OUT | String/Float | Primary output item and rate |
| 15–16 | OUT_2, Q_OUT2 | String/Float | Secondary/byproduct output (blank if N/A) |
| 17 | SINK_PTS | Integer | AWESOME Sink points per item (default 1000) |

**Nested Recipe Map Schema:**

```javascript
RECIPES = {
  'Item Name': {
    alts: ['Basic', 'Alt: Some Alt', ...],  // [0] = default
    recipes: {
      'Basic': { building, mw, output, inputs, byproduct? },
      'Alt: Some Alt': { ... },
    }
  }
}
```

- **Recipe key fallback:** `alts[0]` used as default when no override exists.
- **Equipment Workshop (EW) key strategy:** Manual-crafted recipes use key `"Basic (EW)"` to coexist with automated `"Basic"` recipes for the same item. Items with EW variants: Black Powder, Nobelisk, Nuke Nobelisk, Shatter Rebar, Stun Rebar (5 total).

**Database metrics (v1.4):** 151 items, 279 recipe variants (180 Basic + 106 Alternate + 34 Quantum — reduced from 152/275 post wiki audit), 32 raw resources, 139 unique input items.

---

### 3. SOLVER ARCHITECTURE

**Engine:** `solver.js` v1.5 — 211 lines. Recursive chain solver with four primary functions:

- **`accumulate(item, rate, chain)`** — Recursively resolves recipe dependencies visiting child items. Uses a `_visiting` Set for runtime cycle detection. For each recipe input, computes `machines * inp.qty * ocMult` and passes total rate downstream.
- **`calcFromMerged()`** — Post-accumulation pass that merges identical items from different recipe branches and resolves multi-output recipe splits.
- **`byproductCredit pass`** — Optional post-processing step in `solve()`: sums all `byproductRate` across non-raw production nodes, then reduces matching raw node `rate` and `outputRate` by the lesser of byproduct total and needed amount. Raw nodes receive `creditFromByp` and `rateBeforeCredit` metadata. Does not affect machine counts or power.
- **`solve(config)`** — Orchestrates PASS 1 (accumulate) + PASS 2 (calcFromMerged) + optional byproduct credit pass. Returns `{ nodes, byDepth, rawNodes, totalMachines, totalPower, stages, byproductCredits }`.

**Solver formula:** `machines * input.qty * ocMult` — where `ocMult = (100 / overclockPercent)`.

**Somersloop Rules:**
- **Allowed:** Production buildings only (Assembler, Manufacturer, Refinery, Blender, Particle Accelerator, Quantum Encoder, Converter, Constructor, Foundry, Packager).
- **Forbidden:** Extraction nodes (Miner, Oil Extractor, Water Extractor, Resource Well Pressurizer).
- **Implementation:** `isRaw` flag prevents sloop multiplier from being applied to extraction-type nodes.

**Fluid Packaging Cycle Detection:**
Detected via `_visiting` Set at runtime. Cycles involve Alumina Solution, Heavy Oil Residue, and Fuel — where a fluid's unpackaged form depends on the packaged form and vice versa. Cycles are **not auto-resolved**; user must configure alternate recipe overrides (e.g., "Alt: Sloppy Alumina") via the UI or `FLUID_OVERRIDES` in tests.

**Byproduct handling:** Byproducts display on machine cards (dashed separator, dimmed styling). When **Byproduct Credit** is enabled (config panel toggle, URL field `bc: 0|1`), the solver sums all byproduct production per item and offsets matching raw node extraction rates. Example: Aluminum Scrap produces 120 Water/min as byproduct — with credit ON, Water Extractors are reduced by that amount. Credit never increases machine counts; it only reduces raw node rates. Fully offset items show `0/min` net with full credit amount visible in the node card.

**Benchmarks:**

| Chain | Rate | Machines | Power |
|-------|------|----------|-------|
| Motor | 10/min | 62 | 393 MW |
| Heavy Modular Frame | 5/min | 179 | 1,332 MW |
| Ficsonium Fuel Rod | 2.5/min | 259 | 6,930 MW |
| Supercomputer | 2/min | 164 | 2,623 MW |

**Test suite:** 29/29 tests passing (DB integrity, chain resolution, byproducts, overrides, overclock scaling, belt limits, error handling, merge/totals, byproduct credit).

---

### 4. URL STATE SYSTEM

**Encoding Pattern:**

```javascript
btoa(unescape(encodeURIComponent(JSON.stringify(payload))))
```

**Decoding Pattern:**

```javascript
JSON.parse(decodeURIComponent(escape(atob(encoded))))
```

**Payload Schema:**

```javascript
{
  i:  string,   // item name (e.g., 'Motor')
  t:  number,   // target rate (items/min)
  oc: number,   // overclock percent
  sl: 0|1,      // somersloop enabled
  bl: number,   // belt limit (items/min)
  pl: number,   // pipe limit (items/min)
  or: object,   // recipe overrides { 'Item': 'Alt: Name', ... }
  bc: 0|1       // byproduct credit (added v1.5)
}
```

**Security Assessment: 9.4/10**

| Category | Score |
|----------|-------|
| Encoding | 10/10 |
| Decoding | 10/10 |
| Security (no injection vectors) | 10/10 |
| Compatibility | 9/10 |
| Error Handling | 7/10 |
| Edge Cases | 10/10 |
| Performance | 10/10 |

**localStorage Persistence Keys:**

| Page | Key | Content |
|------|-----|---------|
| Planner builds | `fc_builds` | Array of saved build configurations |
| Power Calculator | `factorycalc_power` | Generator counts, OC, demand |
| Phases Checklist | `factorycalc_phases` | Per-item delivery counts + done flags |
| Phases version | `STATE_VERSION` | Incremented on schema changes to auto-purge stale state (current: v2) |

URL is stored via `history.replaceState(null, '', '?plan=${encoded}')`. Browser URL length support: Chrome 32KB+, Firefox 65KB+, Safari 80KB+, Edge 32KB+.

---

### 5. UI/UX PATTERNS

**Responsive Breakpoints:**

| Breakpoint | Target | Behavior |
|------------|--------|----------|
| ≤900px | Tablet / small laptop | App grid collapses to 1-column; config panel max-height 50vh; nav compact; all grids (`.power-grid`, `.phase-grid`, `.recipe-grid`, `.nodes-grid`) → `1fr` single column; share button hidden |
| ≤480px | Phone | Tiny nav (44px height, 8px font); phase badges shrink; `.fi-row` and `.save-row` stack vertically; table padding reduced |

**Per-Node Alt Recipe Dropdowns:** When `node.alts.length > 1`, the chain view renders an inline `<select class="inline-alt-sel">` on the node card. Changing the selection calls `App.setRecipe(itemName, newValue)`, updates `state.overrides`, and re-solves the chain. Replaces the previous swap-panel-only workflow.

**Nav Link Convention:** All `<a href="#">` placeholders replaced with real page references (e.g., `href="power.html"`). No hash-only links.

**CSS Variable System:** The FICSIT color palette is applied directly in `style.css` (~279 lines). Grid overlay uses `repeating-linear-gradient` as `background-image` across all pages.

**Button Patterns:**
- `.phc-btn` / `.phc-btn.primary` — Rajdhani, uppercase, amber background with obsidian text and gold hover. Used in phases page for "SEND TO PLANNER" buttons.
- `.rc-btn` — Recipe-card buttons in recipes.html with matching amber/gold scheme.

**Page-Specific CSS:** Each nav page includes inline `<style>` blocks for page-specific styles, while `style.css` provides the shared FICSIT terminal base and responsive overrides.

---

### 6. API KEY CONFIGURATION

**Environment Variable Substitution:** OpenCode's global configuration (`~/.config/opencode/opencode.jsonc`) uses `{env:VARIABLE_NAME}` syntax to reference environment variables:

```json
{
  "provider": {
    "openai":    { "options": { "apiKey": "{env:OPENAI_API_KEY}" } },
    "anthropic": { "options": { "apiKey": "{env:ANTHROPIC_API_KEY}" } },
    "google":    { "options": { "apiKey": "{env:GOOGLE_API_KEY}" } }
  }
}
```

**Setup:** Keys exported in `~/.zshrc` via `export ANTHROPIC_API_KEY="sk-..."` (etc.), then sourced with `source ~/.zshrc`. This is the "Secret Vault + Master Settings" combo — highest security, no re-entry required across sessions.

---

*FICSIT Incorporated does not guarantee the accuracy of this document. All recipe data subject to change pending Pioneer field reports.*

*"Efficiency. Compliance. Profit."*
