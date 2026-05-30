#!/usr/bin/env python3
"""Cross-reference SCIM game data (satisfactory_data.json) against the TSV in generate_recipes.py.

Improved matching: better name resolution, more flexible recipe matching.
"""

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
    if cname.startswith("Default__"):
        continue
    if dn and dn != cname:
        name_map[cname] = dn

# Extended known class_name → display_name mappings
EXTRA_NAMES = {
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
    "Desc_ChristmasTree": "FICSMAS Tree",
    "Desc_XmasWreath": "FICSMAS Wreath",
    "Desc_CandyCane": "Candy Cane",
    "Desc_CandyCaneDecor": "Candy Cane Decor",
    "Desc_TargetDummy": "Target Dummy",
    "Desc_CandyCaneDecor": "Candy Cane Decor",
    "Desc_Firework": "Fireworks",
    "Desc_Shroom": "Bacon Agaric",
    "Desc_Nut": "Beryl Nut",
    "Desc_Berry": "Paleberry",
    "Descrystal": "Blue Power Slug",
    "Descrystal_mk2": "Yellow Power Slug",
    "Descrystal_mk3": "Purple Power Slug",
    "DescrystalShard": "Power Shard",
    "Desc_WAT1": "Somersloop WIP",
    "Desc_WAT2": "Mercer Sphere WIP",
    "Desc_SAM": "SAM",
    "Desc_AlienProtein": "Alien Protein",
    "Desc_AlienDNACapsule": "Alien DNA Capsule",
    "Desc_AlienOrgans": "Alien Organs",
    "Desc_CrystalShard": "Power Shard",
    "Desc_SpikedRebar": "Spiked Rebar",
    "Desc_StunRebar": "Stun Rebar",
    "Desc_Beacon": "Beacon",
}

# Non-recipe items to skip (FICSMAS, buildables, equipment, etc.)
SKIP_OUTPUTS = {
    "Actual Snow", "Candy Cane", "FICSMAS Bow", "Copper FICSMAS Ornament",
    "Iron FICSMAS Ornament", "FICSMAS Tree Branch", "Red FICSMAS Ornament",
    "Blue FICSMAS Ornament", "FICSMAS Wreath", "FICSMAS Star", "FICSMAS Tree",
    "Candy Cane Decor", "FICSMAS Ornament Bundle", "FICSMAS Decoration",
    "FICSMAS Wonder Star", "FICSMAS Gift",
    "Fireworks_Projectile_01", "Fireworks_Projectile_02", "Fireworks_Projectile_03",
    "Snowball Projectile",
    "Hub Terminal", "Work Bench Integrated", "Jump Pad", "Jump Pad Tilted",
    "Railroad Switch Control", "Steel Wall_8x4", "Wall_Window_8x4_03_Steel",
    "Pillar Top", "Storage Blueprint", "Storage Integrated",
    "Descartridge Chaos", "Descartridge Smart Projectile", "Descartridge Standard",
    "Nobelisk Cluster", "Nobelisk Explosive", "Nobelisk Gas", "Nobelisk Nuke",
    "Nobelisk Shockwave", "Rebar_Explosive", "Rebar_Spreadshot", "Rebar_Stunshot",
    "Spiked Rebar", "Non-fissile Uranium",
    "Electromagnetic Control Rod",  # SCIM uses this old name
}

# Building name normalization
BUILDING_MAP = {
    "BP_WorkshopComponent": "Equipment Workshop",
    "BP_BuildGun": "Build Gun",
}

def resolve_name(item_class):
    if item_class in name_map:
        return name_map[item_class]
    if item_class in EXTRA_NAMES:
        return EXTRA_NAMES[item_class]
    # Try to extract readable name from class
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

for r in scim["recipes"]:
    name = r["name"]
    
    # Skip FICSMAS recipes
    if any(word in name for word in ["FICSMAS", "Xmas", "Christmas", "Snowball", "Fireworks"]):
        continue
    if "Beacon" in name:
        continue
    
    # Skip if it produces a non-recipe item
    products = []
    skip_recipe = False
    for prod in r.get("products", []):
        pname = resolve_name(prod["item"])
        if pname in SKIP_OUTPUTS:
            skip_recipe = True
            break
        products.append({"item": pname, "qty": prod["amount"]})
    if skip_recipe or not products:
        continue
    
    # Determine if this is a build recipe (produces buildings, equipment, etc.)
    produced_in = r.get("produced_in", [])
    building_raw = produced_in[0] if produced_in else "Unknown"
    building = BUILDING_MAP.get(building_raw, building_raw)
    
    duration = r.get("duration", 1.0)
    is_alt = r.get("is_alternate", False)
    
    # Calculate per-minute rates
    cycles_per_min = 60.0 / duration if duration > 0 else 0
    
    inputs_pm = []
    for ing in r.get("ingredients", []):
        iname = resolve_name(ing["item"])
        inputs_pm.append({"item": iname, "qty": round(ing["amount"] * cycles_per_min, 6)})
    
    outputs_pm = []
    for prod in products:
        outputs_pm.append({"item": prod["item"], "qty": round(prod["qty"] * cycles_per_min, 6)})
    
    scim_recipes.append({
        "name": name,
        "building": building,
        "duration": duration,
        "inputs": inputs_pm,
        "outputs": outputs_pm,
        "is_alternate": is_alt,
    })

print(f"Total SCIM recipes parsed (non-FICSMAS, non-build): {len(scim_recipes)}", file=sys.stderr)

# ── Parse TSV from generate_recipes.py ─────────────────────────
with open("/Users/Mike/Desktop/test_folder/generate_recipes.py") as f:
    content = f.read()

m = re.search(r"tsv_data\s*=\s*\"\"\"(.*?)\"\"\"", content, re.DOTALL)
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
        "recipe_key": None,  # will be populated
    })

# Populate recipe_key for each TSV recipe (as generate_recipes.py does)
for r in tsv_recipes:
    cls = r["class"]
    rname = r["recipe_name"]
    if cls in ("Basic", "Quantum"):
        m2 = re.match(r'^([^(]+)\s*\(([^)]+)\)$', rname)
        if m2:
            recipe_key = f"Basic ({m2.group(2).strip()})"
        else:
            recipe_key = "Basic"
    elif cls == "Alternate":
        n = rname
        if n.endswith(" (Alt)"):
            n = n[:-6].strip()
        elif n.endswith(" (Alt check)"):
            n = n[:-12].strip()
        if not (n.startswith("Alt:") or n.startswith("Alternate")):
            recipe_key = f"Alt: {n}"
        else:
            recipe_key = n
    else:
        recipe_key = rname
    r["recipe_key"] = recipe_key

print(f"Total TSV recipes parsed: {len(tsv_recipes)}", file=sys.stderr)

# ── Build lookups ──────────────────────────────────────────────
tsv_by_output = {}
for r in tsv_recipes:
    primary = r["outputs"][0]["item"]
    tsv_by_output.setdefault(primary, []).append(r)

scim_by_output = {}
for r in scim_recipes:
    primary = r["outputs"][0]["item"]
    scim_by_output.setdefault(primary, []).append(r)

# ── Smart recipe matching ──────────────────────────────────────
# For each TSV recipe, find the matching SCIM recipe (if any)
# Match criteria: same primary output, same building (or close), similar rates

def rates_close(a, b):
    """Check if two rates are within 5% of each other."""
    if a == 0 and b == 0:
        return True
    max_v = max(abs(a), abs(b), 0.001)
    return abs(a - b) / max_v <= 0.05

def recipes_match(scim_r, tsv_r):
    """Check if a SCIM recipe matches a TSV recipe."""
    # Same building (with normalization)
    scim_b = scim_r["building"]
    tsv_b = tsv_r["building"]
    if scim_b != tsv_b:
        return False
    
    # Check inputs: same items, same rates (within 5%)
    scim_in = {(i["item"], round(i["qty"], 4)) for i in scim_r["inputs"]}
    tsv_in = {(i["item"], round(i["qty"], 4)) for i in tsv_r["inputs"]}
    
    scim_in_dict = {i["item"]: i["qty"] for i in scim_r["inputs"]}
    tsv_in_dict = {i["item"]: i["qty"] for i in tsv_r["inputs"]}
    
    if set(scim_in_dict.keys()) != set(tsv_in_dict.keys()):
        return False
    
    for item in scim_in_dict:
        if not rates_close(scim_in_dict[item], tsv_in_dict[item]):
            return False
    
    # Check outputs
    scim_out_dict = {o["item"]: o["qty"] for o in scim_r["outputs"]}
    tsv_out_dict = {o["item"]: o["qty"] for o in tsv_r["outputs"]}
    
    if set(scim_out_dict.keys()) != set(tsv_out_dict.keys()):
        return False
    
    for item in list(scim_out_dict.keys()):
        if not rates_close(scim_out_dict[item], tsv_out_dict[item]):
            return False
    
    return True

# ══ Compare each TSV recipe against SCIM ═══════════════════════
matched_tsv = set()  # (primary_output, tsv_recipe_name)
matched_scim = set()  # (primary_output, scim_name)
discrepancies = []

# First pass: match TSV to SCIM
for tsv_r in tsv_recipes:
    primary = tsv_r["outputs"][0]["item"]
    if primary not in scim_by_output:
        continue
    
    best_match = None
    for scim_r in scim_by_output[primary]:
        if (primary, scim_r["name"]) in matched_scim:
            continue
        if recipes_match(scim_r, tsv_r):
            best_match = scim_r
            break
    
    if best_match:
        matched_tsv.add((primary, tsv_r["recipe_name"]))
        matched_scim.add((primary, best_match["name"]))
    else:
        # No exact match - try to find close but check differences
        for scim_r in scim_by_output[primary]:
            if (primary, scim_r["name"]) in matched_scim:
                continue
            
            # Check if same building
            if scim_r["building"] != tsv_r["building"]:
                continue
            
            # Check inputs (same items at least)
            scim_in_set = {i["item"] for i in scim_r["inputs"]}
            tsv_in_set = {i["item"] for i in tsv_r["inputs"]}
            
            if scim_in_set != tsv_in_set:
                continue
            
            # Check outputs (same item names)
            scim_out_set = {o["item"] for o in scim_r["outputs"]}
            tsv_out_set = {o["item"] for o in tsv_r["outputs"]}
            
            if scim_out_set != tsv_out_set:
                continue
            
            # Same items but rates may differ
            diffs = []
            scim_in_dict = {i["item"]: i["qty"] for i in scim_r["inputs"]}
            tsv_in_dict = {i["item"]: i["qty"] for i in tsv_r["inputs"]}
            for item in scim_in_dict:
                if not rates_close(scim_in_dict[item], tsv_in_dict[item]):
                    max_v = max(abs(scim_in_dict[item]), abs(tsv_in_dict[item]), 0.001)
                    pct = abs(scim_in_dict[item] - tsv_in_dict[item]) / max_v * 100
                    diffs.append(f"Input {item}: SCIM={scim_in_dict[item]:.4f}/min vs TSV={tsv_in_dict[item]}/min ({pct:.1f}%)")
            
            scim_out_dict = {o["item"]: o["qty"] for o in scim_r["outputs"]}
            tsv_out_dict = {o["item"]: o["qty"] for o in tsv_r["outputs"]}
            for item in scim_out_dict:
                if not rates_close(scim_out_dict[item], tsv_out_dict[item]):
                    max_v = max(abs(scim_out_dict[item]), abs(tsv_out_dict[item]), 0.001)
                    pct = abs(scim_out_dict[item] - tsv_out_dict[item]) / max_v * 100
                    diffs.append(f"Output {item}: SCIM={scim_out_dict[item]:.4f}/min vs TSV={tsv_out_dict[item]}/min ({pct:.1f}%)")
            
            if diffs:
                discrepancies.append({
                    "item": primary,
                    "scim_recipe": scim_r["name"],
                    "tsv_recipe": tsv_r["recipe_name"],
                    "difference": "; ".join(diffs),
                    "severity": "MEDIUM" if len(diffs) == 1 else "HIGH"
                })
                matched_tsv.add((primary, tsv_r["recipe_name"]))
                matched_scim.add((primary, scim_r["name"]))
                break
            else:
                # They're the same after all
                matched_tsv.add((primary, tsv_r["recipe_name"]))
                matched_scim.add((primary, scim_r["name"]))
                break
        
        # If we get here with no match, check if it's an (EW) variant
        # Equipment workshop recipes are expected to differ (0.5× speed)
        if tsv_r["building"] == "Equipment Workshop":
            # Try to find a matching SCIM recipe in Equipment Workshop
            for scim_r in scim_by_output[primary]:
                if scim_r["building"] == "Equipment Workshop":
                    # Check if same items but different rates (0.5× is expected)
                    scim_items = {i["item"] for i in scim_r["inputs"]}
                    tsv_items = {i["item"] for i in tsv_r["inputs"]}
                    if scim_items == tsv_items:
                        matched_tsv.add((primary, tsv_r["recipe_name"]))
                        matched_scim.add((primary, scim_r["name"]))
                        break

# ── Find unmatched ─────────────────────────────────────────────
tsv_unmatched = []
for r in tsv_recipes:
    if (r["outputs"][0]["item"], r["recipe_name"]) not in matched_tsv:
        tsv_unmatched.append(r)

scim_unmatched = []
for r in scim_recipes:
    primary = r["outputs"][0]["item"]
    if (primary, r["name"]) not in matched_scim:
        scim_unmatched.append(r)

# Item-level comparison
tsv_items = {r["outputs"][0]["item"] for r in tsv_recipes}
scim_items = {r["outputs"][0]["item"] for r in scim_recipes}

tsv_only_items = tsv_items - scim_items
scim_only_items = scim_items - tsv_items

# ── Generate Report ────────────────────────────────────────────
print("=" * 80)
print("CROSS-REFERENCE REPORT: SCIM (CL-273254) vs TSV (generate_recipes.py)")
print("=" * 80)
print()

print("## Discrepancies Found")
print("| Item | SCIM Recipe | TSV Recipe | Difference | Severity |")
print("|------|-------------|-------------|------------|----------|")
if discrepancies:
    for d in discrepancies:
        print(f"| {d['item']} | {d['scim_recipe']} | {d['tsv_recipe']} | {d['difference']} | {d['severity']} |")
else:
    print("| No significant rate discrepancies found (>5%) for same-building same-ingredient recipes | | | | |")

print()

print("## SCIM Recipes NOT matched in TSV")
print("| Item | SCIM Name | Building | SCIM Inputs/min | SCIM Outputs/min | Likely Reason |")
print("|------|-----------|----------|----------------|-----------------|---------------|")
for r in scim_unmatched:
    primary = r["outputs"][0]["item"]
    in_str = ", ".join(f"{i['item']}: {i['qty']:.4g}" for i in r["inputs"])
    out_str = ", ".join(f"{o['item']}: {o['qty']:.4g}" for o in r["outputs"])
    # Determine reason
    if primary in tsv_items:
        reason = "Different building or ingredients from TSV recipes for this item"
    else:
        reason = "Item not in TSV"
    print(f"| {primary} | {r['name']} | {r['building']} | {in_str} | {out_str} | {reason} |")

print()

print("## TSV Recipes NOT matched in SCIM")
print("| Item | TSV Name | Class | Building | TSV Inputs | TSV Outputs | Likely Reason |")
print("|------|----------|-------|----------|------------|-------------|---------------|")
for r in tsv_unmatched:
    primary = r["outputs"][0]["item"]
    in_str = ", ".join(f"{i['item']}: {i['qty']:g}" for i in r["inputs"])
    out_str = ", ".join(f"{o['item']}: {o['qty']:g}" for o in r["outputs"])
    if primary in scim_items:
        reason = "Different recipe variant (EW vs factory, different building or ingredients)"
    elif r["building"] == "Equipment Workshop":
        reason = "Equipment Workshop recipe - SCIM may use different naming"
    elif r["class"] == "Quantum":
        reason = "Quantum recipe - may postdate SCIM build"
    else:
        # Check if it's the unpackaging recipes (SCIM treats these differently)
        if "Unpackage" in r["recipe_name"]:
            reason = "Unpackage recipe - SCIM may use different format"
        elif "(EW)" in r["recipe_name"]:
            reason = "Equipment Workshop variant"
        else:
            reason = "Item not in SCIM data (possibly newer content)"
    print(f"| {primary} | {r['recipe_name']} | {r['class']} | {r['building']} | {in_str} | {out_str} | {reason} |")

print()

print("## Items in TSV but NOT in SCIM at all")
print("| Item | TSV Recipe | Class | Notes |")
print("|------|------------|-------|-------|")
sorted_tsv_only = sorted(tsv_only_items)
for item in sorted_tsv_only:
    # Get the recipe class
    for r in tsv_recipes:
        if r["outputs"][0]["item"] == item:
            print(f"| {item} | {r['recipe_name']} | {r['class']} | |")
            break

print()

print("## Items in SCIM but NOT in TSV at all")
print("| Item | SCIM Name | SCIM Building | Notes |")
print("|------|-----------|--------------|-------|")
sorted_scim_only = sorted(scim_only_items - SKIP_OUTPUTS)
for item in sorted_scim_only:
    for r in scim_recipes:
        if r["outputs"][0]["item"] == item:
            print(f"| {item} | {r['name']} | {r['building']} | |")
            break

print()

# Summary
print("## Summary")
print(f"- Total SCIM recipes parsed (excl FICSMAS/build): {len(scim_recipes)}")
print(f"- Total TSV recipes parsed: {len(tsv_recipes)}")
print(f"- Matched: {len(matched_tsv)}")
print(f"- Discrepancies found: {len(discrepancies)}")
print(f"- SCIM recipes not matched in TSV: {len(scim_unmatched)}")
print(f"- TSV recipes not matched in SCIM: {len(tsv_unmatched)}")
print(f"- Items only in TSV: {len(tsv_only_items)}")
print(f"- Items only in SCIM: {len(scim_only_items)}")
