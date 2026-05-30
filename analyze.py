#!/usr/bin/env python3
"""Cross-reference SCIM game data (satisfactory_data.json) against the TSV in generate_recipes.py."""

import json
import re
import sys

# ── Load SCIM data ─────────────────────────────────────────────
with open("/Users/Mike/Desktop/test_folder/satisfactory_data.json") as f:
    scim = json.load(f)

# Build class_name → display_name map from items
name_map = {}
for cname, obj in scim["items"].items():
    dn = obj.get("display_name", "")
    # Skip Default__ duplicates and non-items
    if cname.startswith("Default__"):
        continue
    if dn and dn != cname:
        name_map[cname] = dn

# Also fix known class_name patterns that don't match item entries
# e.g. BP_ItemDescriptorPortableMiner → "Portable Miner"
# We'll handle these as we encounter them.

def scim_item_name(item_class):
    """Resolve a class_name reference to a display name."""
    if item_class in name_map:
        return name_map[item_class]
    # Known special cases
    special = {
        "BP_ItemDescriptorPortableMiner": "Portable Miner",
        "BP_HealthGainDescriptor": "Health",
        "Desc_Gift": "FICSMAS Gift",
        "DescandyCane": "Candy Cane",
        "Desc_Snow": "Actual Snow",
        "Desc_XmasBow": "FICSMAS Bow",
        "Desc_XmasBall3": "Copper FICSMAS Ornament",
        "Desc_XmasBall4": "Iron FICSMAS Ornament",
        "Desc_XmasBranch": "FICSMAS Tree Branch",
        "Desc_XmasBall1": "Red FICSMAS Ornament",
        "Desc_XmasBall2": "Blue FICSMAS Ornament",
        "Desc_XmasBall5": "FICSMAS Wreath",
        "Desc_XmasStar": "FICSMAS Star",
        "Desc_XmasOrnament": "FICSMAS Ornament",
        "Desc_ChristmasTree": "FICSMAS Tree",
        "Desc_XmasWreath": "FICSMAS Wreath",
        "Desc_CandyCane": "Candy Cane",
        "Desc_CandyCaneDecor": "Candy Cane Decor",
    }
    if item_class in special:
        return special[item_class]
    # Strip Desc_ prefix, try to produce readable name
    name = item_class
    if name.startswith("Desc_"):
        name = name[5:]
    elif name.startswith("BP_"):
        name = name[3:]
    # CamelCase to readable
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
    return name

# ── Parse SCIM recipes ─────────────────────────────────────────
scim_recipes = []
ficmas_names = {"FICSMAS Gift", "Candy Cane", "Actual Snow", "FICSMAS Bow",
                "Copper FICSMAS Ornament", "Iron FICSMAS Ornament",
                "FICSMAS Tree Branch", "Red FICSMAS Ornament", "Blue FICSMAS Ornament",
                "FICSMAS Wreath", "FICSMAS Star", "FICSMAS Tree",
                "FICSMAS Wreath", "Candy Cane Decor", "FICSMAS Ornament",
                "FICSMAS Decoration", }

for r in scim["recipes"]:
    name = r["name"]
    # Skip FICSMAS
    if "FICSMAS" in name or "Xmas" in name or "Christmas" in name:
        continue
    # Skip known removed items
    if "Beacon" in name:
        continue
    
    ingredients = []
    for ing in r.get("ingredients", []):
        iname = scim_item_name(ing["item"])
        ingredients.append({"item": iname, "qty": ing["amount"]})
    
    products = []
    for prod in r.get("products", []):
        pname = scim_item_name(prod["item"])
        products.append({"item": pname, "qty": prod["amount"]})
    
    produced_in = r.get("produced_in", [])
    building = produced_in[0] if produced_in else "Unknown"
    duration = r.get("duration", 1.0)
    is_alt = r.get("is_alternate", False)
    is_build = r.get("is_build_recipe", False)
    
    # Calculate per-minute rates from per-cycle amounts
    cycles_per_min = 60.0 / duration if duration > 0 else 0
    
    inputs_pm = []
    for ing in ingredients:
        inputs_pm.append({"item": ing["item"], "qty": round(ing["qty"] * cycles_per_min, 4)})
    
    outputs_pm = []
    for prod in products:
        outputs_pm.append({"item": prod["item"], "qty": round(prod["qty"] * cycles_per_min, 4)})
    
    scim_recipes.append({
        "name": name,
        "building": building,
        "duration": duration,
        "inputs": inputs_pm,
        "outputs": outputs_pm,
        "is_alternate": is_alt,
        "is_build_recipe": is_build,
    })

print(f"Total SCIM recipes parsed: {len(scim_recipes)}", file=sys.stderr)

# ── Parse TSV from generate_recipes.py ─────────────────────────
with open("/Users/Mike/Desktop/test_folder/generate_recipes.py") as f:
    content = f.read()

# Extract the TSV between the triple-quoted string
m = re.search(r"tsv_data\s*=\s*\"\"\"(.*?)\"\"\"", content, re.DOTALL)
if not m:
    print("ERROR: Could not find TSV data in generate_recipes.py", file=sys.stderr)
    sys.exit(1)

tsv_text = m.group(1).strip()
lines = tsv_text.split("\n")
headers = [h.strip() for h in lines[0].split("\t")]

tsv_recipes = []
for line in lines[1:]:
    cols = [c.strip() for c in line.split("\t")]
    if len(cols) < 14:
        continue
    while len(cols) < len(headers):
        cols.append("")
    row = dict(zip(headers, cols))
    
    recipe_class = row.get("CLASS", "").strip()
    recipe_name = row.get("RECIPE_NAME", "").strip()
    building = row.get("BUILDING", "").strip()
    mw_str = row.get("MW", "").strip()
    mw = float(mw_str) if mw_str else 0
    
    out_1 = row.get("OUT_1", "").strip()
    q_out_str = row.get("Q_OUT", "").strip()
    q_out = float(q_out_str) if q_out_str else 0
    
    out_2 = row.get("OUT_2", "").strip()
    q_out2_str = row.get("Q_OUT2", "").strip()
    q_out2 = float(q_out2_str) if q_out2_str else 0
    
    if not out_1:
        continue
    
    inputs = []
    for i in range(1, 5):
        in_item = row.get(f"IN_{i}", "").strip()
        in_q_str = row.get(f"Q_{i}", "").strip()
        if in_item and in_q_str:
            inputs.append({"item": in_item, "qty": float(in_q_str)})
    
    outputs = [{"item": out_1, "qty": q_out}]
    if out_2 and q_out2:
        outputs.append({"item": out_2, "qty": q_out2})
    
    tier = row.get("TIER", "").strip()
    
    tsv_recipes.append({
        "class": recipe_class,
        "recipe_name": recipe_name,
        "building": building,
        "mw": mw,
        "inputs": inputs,
        "outputs": outputs,
        "tier": tier,
    })

print(f"Total TSV recipes parsed: {len(tsv_recipes)}", file=sys.stderr)

# ── Build lookup by primary output item ─────────────────────────
# For each primary output item, collect all TSV recipes
tsv_by_output = {}
for r in tsv_recipes:
    primary = r["outputs"][0]["item"]
    if primary not in tsv_by_output:
        tsv_by_output[primary] = []
    tsv_by_output[primary].append(r)

# For SCIM, we need to match recipe + item
# Build a set of (primary_output, recipe_name) keys
scim_recipe_keys = set()
scim_by_output = {}
for r in scim_recipes:
    if not r["outputs"]:
        continue
    primary = r["outputs"][0]["item"]
    # Skip build recipes
    if r["is_build_recipe"]:
        continue
    if primary not in scim_by_output:
        scim_by_output[primary] = []
    scim_by_output[primary].append(r)
    scim_recipe_keys.add((primary, r["name"]))

# ── Comparison ──────────────────────────────────────────────────
discrepancies = []
missing_from_tsv = []
missing_from_scim_items = set()

# First, check which TSV recipes have a corresponding SCIM entry
tsv_seen = set()
tsv_item_primary = {}  # item -> list of tsv recipe names

for r in tsv_recipes:
    primary = r["outputs"][0]["item"]
    if primary not in tsv_item_primary:
        tsv_item_primary[primary] = []
    tsv_item_primary[primary].append(r["recipe_name"])

scim_primary_items = set()
for r in scim_recipes:
    if r["outputs"] and not r["is_build_recipe"]:
        scim_primary_items.add(r["outputs"][0]["item"])

tsv_primary_items = set()
for r in tsv_recipes:
    tsv_primary_items.add(r["outputs"][0]["item"])

# Items in TSV but not in SCIM
tsv_only_items = tsv_primary_items - scim_primary_items
# Items in SCIM but not in TSV
scim_only_items = scim_primary_items - tsv_primary_items

# ── Detailed recipe comparison ──────────────────────────────────
def normalize_building(b):
    """Normalize building names for comparison."""
    mapping = {
        "Assembler": "Assembler",
        "Blender": "Blender",
        "Constructor": "Constructor",
        "Converter": "Converter",
        "Equipment Workshop": "Equipment Workshop",
        "Foundry": "Foundry",
        "Manufacturer": "Manufacturer",
        "Packager": "Packager",
        "Particle Accelerator": "Particle Accelerator",
        "Quantum Encoder": "Quantum Encoder",
        "Refinery": "Refinery",
        "Smelter": "Smelter",
        "Nuclear Power Plant": "Nuclear Power Plant",
        "Miner": "Miner",
    }
    return mapping.get(b, b)

def find_matching_tsv(scim_rec, tsv_list, item_name):
    """Find a matching TSV recipe for a SCIM recipe."""
    scim_name = scim_rec["name"]
    scim_building = normalize_building(scim_rec["building"])
    scim_inputs = sorted([(i["item"], i["qty"]) for i in scim_rec["inputs"]])
    scim_outputs = sorted([(o["item"], o["qty"]) for o in scim_rec["outputs"]])
    
    # Try to match by recipe name similarity first
    for tsv_r in tsv_list:
        # Build TSV recipe key as the generate_recipes.py would
        recipe_class = tsv_r["class"]
        rname = tsv_r["recipe_name"]
        
        # Generate the recipe_key used in recipes.js from TSV
        if recipe_class in ("Basic", "Quantum"):
            m2 = re.match(r'^([^(]+)\s*\(([^)]+)\)$', rname)
            if m2:
                base_name, subtype = m2.groups()
                recipe_key = f"Basic ({subtype.strip()})"
            else:
                recipe_key = "Basic"
        elif recipe_class == "Alternate":
            name_clean = rname
            if name_clean.endswith(" (Alt)"):
                name_clean = name_clean[:-6].strip()
            elif name_clean.endswith(" (Alt check)"):
                name_clean = name_clean[:-12].strip()
            if not (name_clean.startswith("Alt:") or name_clean.startswith("Alternate")):
                recipe_key = f"Alt: {name_clean}"
            else:
                recipe_key = name_clean
        else:
            recipe_key = rname
        
        tsv_building = normalize_building(tsv_r["building"])
        tsv_inputs = sorted([(i["item"], i["qty"]) for i in tsv_r["inputs"]])
        tsv_outputs = sorted([(o["item"], o["qty"]) for o in tsv_r["outputs"]])
        
        # Check if we have a reasonable match - same primary output is guaranteed
        # Now check if recipe keys are related
        # The SCIM name might be like "Alternate: Adhered Iron Plate" and TSV recipe_key is "Alt: Adhered Iron Plate"
        # or SCIM name might be like "Iron Ingot" and TSV recipe_key is "Basic"
        
        # Let's try a more flexible matching approach:
        # For basic recipes, SCIM names are usually just the item name
        # For alternate recipes, SCIM names start with "Alternate:"
        
        # Strip "Alternate: " prefix from SCIM name
        scim_clean = scim_name
        if scim_clean.startswith("Alternate: "):
            scim_clean = scim_clean[11:]
        
        # Check if the recipe_key contains or matches the scim_clean name
        # For basic recipes: TSV key is "Basic", SCIM name is item name or "Alternate: ..."
        # We need to be smarter about this.
        
        # Simple approach: check if the building matches and inputs/outputs are close
        # For each TSV recipe under this item, compare inputs/outputs
        
        # Extract the base item name from recipe name
        # SCIM: "Alternate: Adhered Iron Plate" -> produces Reinforced Iron Plate
        # TSV: recipe_key = "Alt: Adhered Iron Plate", class=Alternate
        
        if recipe_class == "Basic" and not scim_rec["is_alternate"]:
            # Both are basic, check building + inputs/outputs match
            if tsv_building != scim_building:
                continue
            # Compare rates
            match = True
            for (si_name, si_qty), (ti_name, ti_qty) in zip(scim_inputs, tsv_inputs):
                if si_name != ti_name:
                    match = False
                    break
                if abs(si_qty - ti_qty) / max(si_qty, 0.001) > 0.05:
                    match = False
                    break
            if not match:
                continue
            for (so_name, so_qty), (to_name, to_qty) in zip(scim_outputs, tsv_outputs):
                if so_name != to_name:
                    match = False
                    break
                if abs(so_qty - to_qty) / max(so_qty, 0.001) > 0.05:
                    match = False
                    break
            if match:
                return tsv_r, recipe_key
        
        elif recipe_class == "Alternate" and scim_rec["is_alternate"]:
            # Both are alternate - check name similarity
            # TSV recipe name might be "Adhered Iron Plate", SCIM is "Alternate: Adhered Iron Plate"
            alt_name = rname
            if alt_name.endswith(" (Alt)"):
                alt_name = alt_name[:-6].strip()
            
            # Compare names
            if alt_name.lower() == scim_clean.lower():
                # Check building + rates
                if tsv_building != scim_building:
                    continue
                match = True
                if len(scim_inputs) != len(tsv_inputs) or len(scim_outputs) != len(tsv_outputs):
                    continue
                for (si_name, si_qty), (ti_name, ti_qty) in zip(scim_inputs, tsv_inputs):
                    if si_name != ti_name:
                        match = False
                        break
                    if abs(si_qty - ti_qty) / max(si_qty, 0.001) > 0.05:
                        match = False
                        break
                if not match:
                    continue
                for (so_name, so_qty), (to_name, to_qty) in zip(scim_outputs, tsv_outputs):
                    if so_name != to_name:
                        match = False
                        break
                    if abs(so_qty - to_qty) / max(so_qty, 0.001) > 0.05:
                        match = False
                        break
                if match:
                    return tsv_r, recipe_key
        
        elif recipe_class == "Quantum":
            # Quantum recipes
            if scim_rec["is_alternate"]:
                continue
            # Check name match
            if rname.lower() in scim_name.lower() or scim_name.lower() in rname.lower():
                if tsv_building != scim_building:
                    continue
                match = True
                if len(scim_inputs) != len(tsv_inputs) or len(scim_outputs) != len(tsv_outputs):
                    continue
                for (si_name, si_qty), (ti_name, ti_qty) in zip(scim_inputs, tsv_inputs):
                    if si_name != ti_name:
                        match = False
                        break
                    if abs(si_qty - ti_qty) / max(si_qty, 0.001) > 0.05:
                        match = False
                        break
                if not match:
                    continue
                for (so_name, so_qty), (to_name, to_qty) in zip(scim_outputs, tsv_outputs):
                    if so_name != to_name:
                        match = False
                        break
                    if abs(so_qty - to_qty) / max(so_qty, 0.001) > 0.05:
                        match = False
                        break
                if match:
                    return tsv_r, recipe_key
        
        # Also try: match by recipe_key directly
        # SCIM "Alternate: Adhered Iron Plate" → recipe_key should be "Alt: Adhered Iron Plate"
        # Let's see if the TSV's recipe_key matches the SCIM name
        
        if scim_rec["is_alternate"] and recipe_class == "Alternate":
            # Generate expected TSV recipe_key from SCIM name
            expected_key = f"Alt: {scim_clean}"
            if recipe_key == expected_key:
                if tsv_building != scim_building:
                    discrepancies.append({
                        "item": item_name,
                        "scim_recipe": scim_name,
                        "tsv_recipe": rname,
                        "difference": f"Building: SCIM={scim_building}, TSV={tsv_building}",
                        "severity": "HIGH"
                    })
                    continue
                # Compare rates
                diffs = []
                scim_in_dict = {i["item"]: i["qty"] for i in scim_rec["inputs"]}
                tsv_in_dict = {i["item"]: i["qty"] for i in tsv_r["inputs"]}
                
                all_in_items = set(list(scim_in_dict.keys()) + list(tsv_in_dict.keys()))
                for item in sorted(all_in_items):
                    sv = scim_in_dict.get(item, 0)
                    tv = tsv_in_dict.get(item, 0)
                    if abs(sv - tv) > 0.01:
                        max_v = max(abs(sv), abs(tv), 0.001)
                        pct = abs(sv - tv) / max_v * 100
                        if pct > 5:
                            diffs.append(f"{item}: SCIM={sv:.4f}/min, TSV={tv}/min ({pct:.1f}% diff)")
                
                scim_out_dict = {o["item"]: o["qty"] for o in scim_rec["outputs"]}
                tsv_out_dict = {o["item"]: o["qty"] for o in tsv_r["outputs"]}
                
                all_out_items = set(list(scim_out_dict.keys()) + list(tsv_out_dict.keys()))
                for item in sorted(all_out_items):
                    sv = scim_out_dict.get(item, 0)
                    tv = tsv_out_dict.get(item, 0)
                    if abs(sv - tv) > 0.01:
                        max_v = max(abs(sv), abs(tv), 0.001)
                        pct = abs(sv - tv) / max_v * 100
                        if pct > 5:
                            diffs.append(f"{item}: SCIM={sv:.4f}/min, TSV={tv}/min ({pct:.1f}% diff)")
                
                if diffs:
                    discrepancies.append({
                        "item": item_name,
                        "scim_recipe": scim_name,
                        "tsv_recipe": rname,
                        "difference": "; ".join(diffs),
                        "severity": "HIGH" if any("building" in d for d in diffs) else "MEDIUM"
                    })
                    return tsv_r, recipe_key
                else:
                    return tsv_r, recipe_key
    
    return None, None

# ── Do detailed comparison ──────────────────────────────────────
matched_tsv_keys = set()
matched_scim_names = set()

for r in scim_recipes:
    if r["is_build_recipe"]:
        continue
    if not r["outputs"]:
        continue
    primary = r["outputs"][0]["item"]
    
    if primary not in tsv_by_output:
        # Item not in TSV at all
        missing_from_tsv.append(r)
        continue
    
    tsv_list = tsv_by_output[primary]
    matched, key = find_matching_tsv(r, tsv_list, primary)
    
    if matched:
        matched_tsv_keys.add((primary, matched["recipe_name"]))
        matched_scim_names.add((primary, r["name"]))
    else:
        # No exact match found, flag as missing
        missing_from_tsv.append(r)

# Check for TSV recipes not matched in SCIM
unmatched_tsv = []
for r in tsv_recipes:
    primary = r["outputs"][0]["item"]
    if (primary, r["recipe_name"]) not in matched_tsv_keys:
        unmatched_tsv.append(r)

# ── Generate report ─────────────────────────────────────────────
print("=" * 80)
print("CROSS-REFERENCE REPORT: SCIM vs TSV")
print("=" * 80)
print()

# Discrepancies
print("## Discrepancies Found")
print("| Item | SCIM Recipe | TSV Recipe | Difference | Severity |")
print("|------|-------------|-------------|------------|----------|")
if discrepancies:
    for d in discrepancies:
        print(f"| {d['item']} | {d['scim_recipe']} | {d['tsv_recipe']} | {d['difference']} | {d['severity']} |")
else:
    print("| No significant discrepancies found | | | | |")

print()

# Items in SCIM but not in TSV (missing recipes)
print("## Items in SCIM but NOT fully matched in TSV")
print("| Item | SCIM Recipe Name | Building | Inputs (per min) | Outputs (per min) |")
print("|------|------------------|----------|-----------------|-------------------|")
if missing_from_tsv:
    for r in missing_from_tsv:
        if not r["outputs"]:
            continue
        primary = r["outputs"][0]["item"]
        in_str = ", ".join(f"{i['item']}: {i['qty']}" for i in r["inputs"])
        out_str = ", ".join(f"{o['item']}: {o['qty']}" for o in r["outputs"])
        print(f"| {primary} | {r['name']} | {r['building']} | {in_str} | {out_str} |")
else:
    print("| All SCIM recipes matched in TSV | | | | |")

print()

# Items in TSV but not matched in SCIM (TSV-only)
print("## Items in TSV but NOT matched in SCIM")
print("| Item | TSV Recipe Name | Class | Building | Inputs | Outputs |")
print("|------|-----------------|-------|----------|--------|---------|")
if unmatched_tsv:
    for r in unmatched_tsv:
        primary = r["outputs"][0]["item"]
        in_str = ", ".join(f"{i['item']}: {i['qty']}" for i in r["inputs"])
        out_str = ", ".join(f"{o['item']}: {o['qty']}" for o in r["outputs"])
        print(f"| {primary} | {r['recipe_name']} | {r['class']} | {r['building']} | {in_str} | {out_str} |")
else:
    print("| All TSV recipes matched in SCIM | | | | | |")

print()

# Items in TSV but not in SCIM at all
print("## Items in TSV that do NOT exist in SCIM data")
print("| Item | TSV Recipe Name | Class |")
print("|------|-----------------|-------|")
if tsv_only_items:
    for item in sorted(tsv_only_items):
        for r in tsv_recipes:
            if r["outputs"][0]["item"] == item:
                print(f"| {item} | {r['recipe_name']} | {r['class']} |")
                break
else:
    print("| All TSV items found in SCIM | | |")

print()

# Items in SCIM but not in TSV at all
print("## Items in SCIM that do NOT exist in TSV")
print("| Item | SCIM Recipe Name |")
print("|------|------------------|")
if scim_only_items:
    for item in sorted(scim_only_items):
        # Check if it's a known non-recipe item
        for r in scim_recipes:
            if r["outputs"] and r["outputs"][0]["item"] == item and not r["is_build_recipe"]:
                print(f"| {item} | {r['name']} |")
                break
else:
    print("| All SCIM items found in TSV | |")

print()

# Summary
print("## Summary")
scim_non_build = [r for r in scim_recipes if not r["is_build_recipe"]]
print(f"- Total SCIM recipes parsed: {len(scim_recipes)} (non-build: {len(scim_non_build)})")
print(f"- Total TSV recipes parsed: {len(tsv_recipes)}")
print(f"- Discrepancies found: {len(discrepancies)}")
print(f"- SCIM recipes not found in TSV: {len(missing_from_tsv)}")
print(f"- TSV recipes not matched in SCIM: {len(unmatched_tsv)}")
print(f"- Items only in TSV: {len(tsv_only_items)}")
print(f"- Items only in SCIM: {len(scim_only_items)}")
