#!/usr/bin/env python3
"""
Final cross-reference: SCIM (CL-273254) vs TSV (generate_recipes.py).

Key findings from investigation:
1. SCIM data lacks basic recipes (Iron Ingot, Iron Plate, etc.) — they're baked into building defs
2. SCIM uses internal 'name' field which is often misleading (e.g. 'Fuel' for packaged items)
3. SCIM fluid amounts are in sub-units (1000 = 1 m³ in game)
4. SCIM is from Update 8 era — recipe values were rebalanced for 1.0
5. Many SCIM recipes have is_alternate=False but are actually alternates (bug in export)
"""

import json
import re
import sys
from collections import defaultdict

# ── Load SCIM data ─────────────────────────────────────────────
with open("/Users/Mike/Desktop/test_folder/satisfactory_data.json") as f:
    scim = json.load(f)

# Build display_name lookup for all items
item_names = {}
for cname, obj in scim["items"].items():
    dn = obj.get("display_name", "")
    if cname.startswith("Default__"):
        continue
    if dn and dn != cname:
        item_names[cname] = dn

# Extended class→name mappings (for items not in the items dict or with unclear names)
EXTRA = {
    "BP_ItemDescriptorPortableMiner": "Portable Miner",
    "DesccompactedCoal": "Compacted Coal",
    "DesccopperIngot": "Copper Ingot",
    "Desc_IronRod": "Iron Rod",
    "Desc_IronScrew": "Screw",
    "Desc_IronIngot": "Iron Ingot",
    "Desc_IronPlate": "Iron Plate",
    "Desc_IronPlateReinforced": "Reinforced Iron Plate",
    "Desc_IronRebar": "Iron Rebar",
    "Desc_OreIron": "Iron Ore",
    "Desc_OreCopper": "Copper Ore",
    "Desc_OreGold": "Caterium Ore",
    "Desc_CopperIngot": "Copper Ingot",
    "Desc_SteelIngot": "Steel Ingot",
    "Desc_SteelPipe": "Steel Pipe",
    "Desc_SteelPlate": "Steel Beam",
    "Desc_Wire": "Wire",
    "Desc_Cable": "Cable",
    "Desc_Water": "Water",
    "Desc_CrudeOil": "Crude Oil",
    "Desc_Coal": "Coal",
    "Desc_Stone": "Limestone",
    "Desc_LiquidFuel": "Fuel",
    "Desc_Plastic": "Plastic",
    "Desc_Rubber": "Rubber",
    "Desc_PolymerResin": "Polymer Resin",
    "Desc_HeavyOilResidue": "Heavy Oil Residue",
    "Desc_PetroleumCoke": "Petroleum Coke",
    "Desc_Sulfur": "Sulfur",
    "Desc_QuartzCrystal": "Quartz Crystal",
    "Desc_RawQuartz": "Raw Quartz",
    "Desc_Silica": "Silica",
    "Desc_CopperSheet": "Copper Sheet",
    "Desc_Quickwire": "Quickwire",
    "Desc_CateriumIngot": "Caterium Ingot",
    "Desc_AluminumIngot": "Aluminum Ingot",
    "Desc_AluminumScrap": "Aluminum Scrap",
    "Desc_AluminaSolution": "Alumina Solution",
    "Desc_AluminumCasing": "Aluminum Casing",
    "Desc_SulfuricAcid": "Sulfuric Acid",
    "Desc_NitricAcid": "Nitric Acid",
    "Desc_NitrogenGas": "Nitrogen Gas",
    "Desc_Bauxite": "Bauxite",
    "Desc_ModularFrame": "Modular Frame",
    "Desc_ModularFrameLightweight": "Heavy Modular Frame",
    "Desc_Motor": "Motor",
    "Desc_Rotor": "Rotor",
    "Desc_Stator": "Stator",
    "Desc_Computer": "Computer",
    "Desc_HighSpeedConnector": "High-Speed Connector",
    "Desc_CircuitBoard": "Circuit Board",
    "Desc_AIUnit": "AI Limiter",
    "Desc_CrystalOscillator": "Crystal Oscillator",
    "Desc_Supercomputer": "Supercomputer",
    "Desc_RadioControlUnit": "Radio Control Unit",
    "Desc_CoolingSystem": "Cooling System",
    "Desc_TurboMotor": "Turbo Motor",
    "Desc_ModularFrameHeavy": "Fused Modular Frame",
    "Desc_HeatSink": "Heat Sink",
    "Desc_AlcladSheet": "Alclad Aluminum Sheet",
    "Desc_VersatileFramework": "Versatile Framework",
    "Desc_AutomatedWiring": "Automated Wiring",
    "Desc_EMControlUnit": "EM Control Rod",
    "Desc_MagneticFieldGenerator": "Magnetic Field Generator",
    "Desc_AssemblyDirectorSystem": "Assembly Director System",
    "Desc_ThermalPropulsionRocket": "Thermal Propulsion Rocket",
    "Desc_ModularEngine": "Modular Engine",
    "Desc_SmartPlating": "Smart Plating",
    "Desc_AdaptiveControlUnit": "Adaptive Control Unit",
    "Desc_Uranium": "Uranium",
    "Desc_UraniumWaste": "Uranium Waste",
    "Desc_PlutoniumWaste": "Plutonium Waste",
    "Desc_NonFissileUranium": "Non-Fissile Uranium",
    "Desc_PlutoniumPellet": "Plutonium Pellet",
    "Desc_EncasedPlutoniumCell": "Encased Plutonium Cell",
    "Desc_PlutoniumFuelRod": "Plutonium Fuel Rod",
    "Desc_UraniumFuelRod": "Uranium Fuel Rod",
    "Desc_EncasedUraniumCell": "Encased Uranium Cell",
    "Desc_CopperPowder": "Copper Powder",
    "Desc_PressureConversionCube": "Pressure Conversion Cube",
    "Desc_NuclearPasta": "Nuclear Pasta",
    "Desc_BlackPowder": "Black Powder",
    "Desc_Gunpowder": "Black Powder",
    "Desc_NobeliskExplosive": "Nobelisk",
    "Desc_NobeliskCluster": "Cluster Nobelisk",
    "Desc_NobeliskGas": "Gas Nobelisk",
    "Desc_NobeliskShockwave": "Pulse Nobelisk",
    "Desc_NobeliskNuke": "Nuke Nobelisk",
    "Desc_CrystalShard": "Power Shard",
    "Desc_Biomass": "Biomass",
    "Desc_Leaves": "Leaves",
    "Desc_Wood": "Wood",
    "Desc_Mycelia": "Mycelia",
    "Desc_AlienProtein": "Alien Protein",
    "Desc_AlienDNACapsule": "Alien DNA Capsule",
    "Desc_Fabric": "Fabric",
    "Desc_GasMask": "Gas Mask",
    "Desc_XenoZapper": "Xeno-Zapper",
    "Desc_XenoBasher": "Xeno-Basher",
    "Desc_MedicinalInhaler": "Medicinal Inhaler",
    "Desc_Nut": "Beryl Nut",
    "Desc_Berry": "Paleberry",
    "Desc_Shroom": "Bacon Agaric",
    "Desc_Gift": "FICSMAS Gift",
    "Desc_SAM": "SAM",
    "Desc_ReanimatedSAM": "Reanimated SAM",
    "Desc_TimeCrystal": "Time Crystal",
    "Desc_Diamond": "Diamonds",
    "Desc_DarkMatter": "Dark Matter Residue",
    "Desc_DarkMatterCrystal": "Dark Matter Crystal",
    "Desc_ExcitedPhotonicMatter": "Excited Photonic Matter",
    "Desc_SuperpositionOscillator": "Superposition Oscillator",
    "Desc_NeuralQuantumProcessor": "Neural-Quantum Processor",
    "Desc_AIExpansionServer": "AI Expansion Server",
    "Desc_FicsiteIngot": "Ficsite Ingot",
    "Desc_FicsiteTrigon": "Ficsite Trigon",
    "Desc_SingularityCell": "Singularity Cell",
    "Desc_BallisticWarpDrive": "Ballistic Warp Drive",
    "Desc_SAMFluctuator": "SAM Fluctuator",
    "Desc_AlienPowerMatrix": "Alien Power Matrix",
    "Desc_EmptyCanister": "Empty Canister",
    "Desc_AluminumPlate": "Aluminum Plate",
    "DesccoatedIronPlate": "Coated Iron Plate",
    "Desc_IronPlateCoated": "Coated Iron Plate",
    "Desc_IronIngotBasic": "Basic Iron Ingot",
}

# Merge
item_names.update(EXTRA)

# Known fluid items (SCIM uses 1000× internal units for fluids)
FLUID_ITEMS = {
    "Water", "Crude Oil", "Fuel", "Heavy Oil Residue", "Alumina Solution",
    "Sulfuric Acid", "Nitric Acid", "Nitrogen Gas", "Turbofuel", "Liquid Biofuel",
    "Rocket Fuel", "Ionized Fuel", "Dissolved Silica",
}

def resolve(item_class):
    if item_class in item_names:
        return item_names[item_class]
    # Try to extract readable
    name = item_class
    if name.startswith("Desc_"):
        name = name[5:]
    elif name.startswith("BP_"):
        name = name[3:]
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
    return name

def rate_per_min(amount, duration, item_name):
    """SCIM amount to per-minute rate. Adjust fluid scaling (1000×)."""
    ppm = amount * 60.0 / duration if duration > 0 else 0
    # SCIM stores fluids in units where 1000 = 1 m³
    # The TSV/game UI shows in m³ per minute
    if item_name in FLUID_ITEMS:
        ppm /= 1000.0
    return ppm

# ── Parse SCIM recipes ─────────────────────────────────────────
scim_recipes = []

BUILDING_MAP = {
    "BP_WorkshopComponent": "Equipment Workshop",
    "BP_BuildGun": "Build Gun",
}

for r in scim["recipes"]:
    name = r["name"]
    cn = r.get("class_name", "")
    
    # Skip FICSMAS and holiday stuff
    skip_words = ["FICSMAS", "Xmas", "Christmas", "Gift", "Snowball", "Firework",
                   "Candy", "Snow", "Holiday"]
    if any(w in name for w in skip_words) or any(w in cn for w in skip_words):
        continue
    if any(w in r.get("class_name", "") for w in skip_words):
        continue
    
    # Resolve products — skip non-production or buildable items
    products = []
    skip = False
    for prod in r.get("products", []):
        pname = resolve(prod["item"])
        # Skip buildables, equipment, etc. that aren't production items
        if pname in ("Hub Terminal", "Work Bench Integrated", "Jump Pad",
                      "Jump Pad Tilted", "Railroad Switch Control",
                      "Steel Wall_8x4", "Wall_Window_8x4_03_Steel",
                      "Foundation 1a", "Pillar Top",
                      "Storage Blueprint", "Storage Integrated",
                      "Nail Gun", "Nailgun Spike",
                      "Spe", "Screwdriver", "Rebar_Explosive",
                      "Rebar_Spreadshot", "Rebar_Stunshot",
                      "Spiked Rebar", "Nobelisk Cluster", "Nobelisk Explosive",
                      "Nobelisk Gas", "Nobelisk Nuke", "Nobelisk Shockwave",
                      "Descartridge Chaos", "Descartridge Smart Projectile",
                      "Descartridge Standard", "Snowball Projectile",
                      "Electromagnetic Control Rod",
                      "Candy Cane Basher", "Factory Cart™", "Golden Factory Cart™",
                      "Non-fissile Uranium",
                      "Expanded Storage Container",
                      "FICSMAS Gift", "FICSMAS Bow", "FICSMAS Decoration",
                      "FICSMAS Tree", "FICSMAS Tree Branch",
                      "FICSMAS Wreath", "FICSMAS Star", "FICSMAS Ornament",
                      "FICSMAS Ornament Bundle", "FICSMAS Wonder Star",
                      "Red FICSMAS Ornament", "Blue FICSMAS Ornament",
                      "Copper FICSMAS Ornament", "Iron FICSMAS Ornament",
                      "Actual Snow", "Candy Cane", "Candy Cane Decor",
                      ):
            skip = True
        products.append({"item": pname, "amount": prod["amount"]})
    if skip or not products:
        continue
    
    duration = r.get("duration", 1.0)
    produced_in = r.get("produced_in", [])
    building_raw = produced_in[0] if produced_in else "Unknown"
    building = BUILDING_MAP.get(building_raw, building_raw)
    is_alt = r.get("is_alternate", False)
    
    # Compute per-minute rates
    inputs_pm = {}
    for ing in r.get("ingredients", []):
        iname = resolve(ing["item"])
        inputs_pm[iname] = rate_per_min(ing["amount"], duration, iname)
    
    outputs_pm = {}
    for prod in products:
        pname = prod["item"]
        outputs_pm[pname] = rate_per_min(prod["amount"], duration, pname)
    
    # Use class_name as the recipe identifier since 'name' field is unreliable
    # (e.g. many different recipes all called 'Fuel', 'Iron Plate', etc.)
    recipe_id = cn if cn else name
    
    scim_recipes.append({
        "name": name,
        "class_name": cn,
        "building": building,
        "inputs": inputs_pm,
        "outputs": outputs_pm,
        "is_alternate": is_alt,
        "duration": duration,
    })

print(f"SCIM recipes parsed: {len(scim_recipes)}", file=sys.stderr)

# ── Parse TSV ──────────────────────────────────────────────────
with open("/Users/Mike/Desktop/test_folder/generate_recipes.py") as f:
    content = f.read()

m = re.search(r"tsv_data\s*=\s*\"\"\"(.*?)\"\"\"", content, re.DOTALL)
lines = m.group(1).strip().split("\n")
headers = [h.strip() for h in lines[0].split("\t")]

tsv_recipes = []
for line in lines[1:]:
    cols = [c.strip() for c in line.split("\t")]
    if len(cols) < 14:
        continue
    while len(cols) < len(headers):
        cols.append("")
    row = dict(zip(headers, cols))
    
    out_1 = row.get("OUT_1", "").strip()
    q_out_str = row.get("Q_OUT", "").strip()
    if not out_1 or not q_out_str:
        continue
    
    outputs = {out_1: float(q_out_str)}
    out_2 = row.get("OUT_2", "").strip()
    q_out2_str = row.get("Q_OUT2", "").strip()
    if out_2 and q_out2_str:
        outputs[out_2] = float(q_out2_str)
    
    inputs = {}
    for i in range(1, 5):
        in_item = row.get(f"IN_{i}", "").strip()
        in_q_str = row.get(f"Q_{i}", "").strip()
        if in_item and in_q_str:
            inputs[in_item] = float(in_q_str)
    
    tsv_recipes.append({
        "class": row.get("CLASS", "").strip(),
        "recipe_name": row.get("RECIPE_NAME", "").strip(),
        "building": row.get("BUILDING", "").strip(),
        "inputs": inputs,
        "outputs": outputs,
        "tier": row.get("TIER", "").strip(),
    })

print(f"TSV recipes parsed: {len(tsv_recipes)}", file=sys.stderr)

# ── Build indexes ──────────────────────────────────────────────
# Index TSV by primary output item
tsv_by_output = defaultdict(list)
for r in tsv_recipes:
    primary = list(r["outputs"].keys())[0]
    tsv_by_output[primary].append(r)

# Index SCIM by primary output item
scim_by_output = defaultdict(list)
for r in scim_recipes:
    primary = list(r["outputs"].keys())[0]
    scim_by_output[primary].append(r)

# ── Comparison ─────────────────────────────────────────────────
def rates_close(a, b):
    if a == 0 and b == 0:
        return True
    max_v = max(abs(a), abs(b), 0.001)
    return abs(a - b) / max_v <= 0.05

def recipes_match(scim_r, tsv_r):
    """Check if SCIM recipe matches TSV recipe (same building, ingredients, outputs)."""
    if scim_r["building"] != tsv_r["building"]:
        return False
    
    # Same inputs
    if set(scim_r["inputs"].keys()) != set(tsv_r["inputs"].keys()):
        return False
    for item in scim_r["inputs"]:
        if not rates_close(scim_r["inputs"][item], tsv_r["inputs"][item]):
            return False
    
    # Same outputs
    if set(scim_r["outputs"].keys()) != set(tsv_r["outputs"].keys()):
        return False
    for item in scim_r["outputs"]:
        if not rates_close(scim_r["outputs"][item], tsv_r["outputs"][item]):
            return False
    
    return True

def format_rate_diff(scim_r, tsv_r):
    """Return list of difference strings between two recipes."""
    diffs = []
    all_inputs = set(list(scim_r["inputs"].keys()) + list(tsv_r["inputs"].keys()))
    for item in sorted(all_inputs):
        sv = scim_r["inputs"].get(item, 0)
        tv = tsv_r["inputs"].get(item, 0)
        if not rates_close(sv, tv):
            max_v = max(abs(sv), abs(tv), 0.001)
            pct = abs(sv - tv) / max_v * 100
            diffs.append(f"{item}: SCIM={sv:.4g}/min vs TSV={tv:g}/min ({pct:.1f}%)")
    
    all_outputs = set(list(scim_r["outputs"].keys()) + list(tsv_r["outputs"].keys()))
    for item in sorted(all_outputs):
        sv = scim_r["outputs"].get(item, 0)
        tv = tsv_r["outputs"].get(item, 0)
        if not rates_close(sv, tv):
            max_v = max(abs(sv), abs(tv), 0.001)
            pct = abs(sv - tv) / max_v * 100
            diffs.append(f"{item}: SCIM={sv:.4g}/min vs TSV={tv:g}/min ({pct:.1f}%)")
    
    return diffs

# Match TSV → SCIM
matched_tsv = set()   # (primary, recipe_name)
matched_scim = set()  # (primary, scim_class_name)
discrepancies = []

for tsv_r in tsv_recipes:
    primary = list(tsv_r["outputs"].keys())[0]
    if primary not in scim_by_output:
        continue
    
    best_scim = None
    
    # Try exact match first
    for scim_r in scim_by_output[primary]:
        if recipes_match(scim_r, tsv_r):
            best_scim = scim_r
            break
    
    if best_scim:
        matched_tsv.add((primary, tsv_r["recipe_name"]))
        matched_scim.add((primary, best_scim["class_name"]))
        continue
    
    # Try same building match (check for rate differences)
    for scim_r in scim_by_output[primary]:
        if scim_r["building"] != tsv_r["building"]:
            continue
        if set(scim_r["inputs"].keys()) != set(tsv_r["inputs"].keys()):
            continue
        if set(scim_r["outputs"].keys()) != set(tsv_r["outputs"].keys()):
            continue
        
        # Same items — check rates
        diffs = format_rate_diff(scim_r, tsv_r)
        if diffs:
            severity = "HIGH" if len(diffs) > 1 else "MEDIUM"
            discrepancies.append({
                "item": primary,
                "scim_id": scim_r["class_name"] or scim_r["name"],
                "tsv_name": tsv_r["recipe_name"],
                "difference": "; ".join(diffs),
                "severity": severity,
                "scim_building": scim_r["building"],
                "tsv_building": tsv_r["building"],
            })
        else:
            # Shouldn't reach here if recipes_match returned False
            pass
        
        matched_tsv.add((primary, tsv_r["recipe_name"]))
        matched_scim.add((primary, scim_r["class_name"]))
        break
    
    # If still no match, try building-mismatch check (maybe 1.0 rebalance)
    if best_scim is None and (primary, tsv_r["recipe_name"]) not in matched_tsv:
        for scim_r in scim_by_output[primary]:
            if set(scim_r["inputs"].keys()) == set(tsv_r["inputs"].keys()) and \
               set(scim_r["outputs"].keys()) == set(tsv_r["outputs"].keys()):
                # Same items, check building diff
                if scim_r["building"] != tsv_r["building"]:
                    discrepancies.append({
                        "item": primary,
                        "scim_id": scim_r["class_name"] or scim_r["name"],
                        "tsv_name": tsv_r["recipe_name"],
                        "difference": f"Building: SCIM={scim_r['building']}, TSV={tsv_r['building']}",
                        "severity": "HIGH",
                        "scim_building": scim_r["building"],
                        "tsv_building": tsv_r["building"],
                    })
                    matched_tsv.add((primary, tsv_r["recipe_name"]))
                    matched_scim.add((primary, scim_r["class_name"]))
                    break
                else:
                    diffs = format_rate_diff(scim_r, tsv_r)
                    if diffs:
                        discrepancies.append({
                            "item": primary,
                            "scim_id": scim_r["class_name"] or scim_r["name"],
                            "tsv_name": tsv_r["recipe_name"],
                            "difference": "; ".join(diffs),
                            "severity": "HIGH",
                            "scim_building": scim_r["building"],
                            "tsv_building": tsv_r["building"],
                        })
                        matched_tsv.add((primary, tsv_r["recipe_name"]))
                        matched_scim.add((primary, scim_r["class_name"]))
                        break

# Items not matched
tsv_unmatched = []
for r in tsv_recipes:
    primary = list(r["outputs"].keys())[0]
    if (primary, r["recipe_name"]) not in matched_tsv:
        tsv_unmatched.append(r)

scim_unmatched = []
for r in scim_recipes:
    primary = list(r["outputs"].keys())[0]
    if (primary, r["class_name"]) not in matched_scim:
        scim_unmatched.append(r)

# Items that exist in one but not the other
tsv_items = set()
for r in tsv_recipes:
    tsv_items.add(list(r["outputs"].keys())[0])

scim_items = set()
for r in scim_recipes:
    scim_items.add(list(r["outputs"].keys())[0])

tsv_only = tsv_items - scim_items
scim_only = scim_items - tsv_items

# ── Generate Report ────────────────────────────────────────────
print("=" * 80)
print("CROSS-REFERENCE REPORT: SCIM (CL-273254) vs TSV (generate_recipes.py)")
print("=" * 80)
print()

# Discrepancies
print("## Discrepancies Found")
print("| Item | SCIM Recipe | TSV Recipe | Building | Difference | Severity |")
print("|------|-------------|-------------|----------|------------|----------|")
# Sort by severity
for d in sorted(discrepancies, key=lambda x: (0 if x['severity'] == 'HIGH' else 1, x['item'])):
    scim_id = d['scim_id'][:60] if len(d['scim_id']) > 60 else d['scim_id']
    bld = f"{d['scim_building']} vs {d['tsv_building']}" if d['scim_building'] != d['tsv_building'] else d['scim_building']
    print(f"| {d['item']} | {scim_id} | {d['tsv_name']} | {bld} | {d['difference'][:100]} | {d['severity']} |")

if not discrepancies:
    print("| No significant discrepancies found | | | | | |")

print()

# SCIM unmatched
print("## SCIM Recipes NOT Matched in TSV")
scim_unmatched_filtered = [r for r in scim_unmatched 
                           if list(r["outputs"].keys())[0] not in 
                           {"Coal", "Concrete", "Iron Ore", "Copper Ore", "Caterium Ore",
                            "Limestone", "Raw Quartz", "Sulfur", "Bauxite", "Uranium",
                            "Nitrogen Gas", "Quartz Crystal", "Steel Beam", "Steel Pipe",
                            "Empty Canister", "Iron Ingot", "Copper Ingot", "Caterium Ingot",
                            "Cable", "Wire", "Quickwire", "Steel Ingot", "Aluminum Ingot",
                            "Alumina Solution", "Aluminum Casing", "Heat Sink",
                            "Encased Industrial Beam", "Plastic", "Rubber", "Circuit Board",
                            "Rotor", "Motor", "Stator", "Computer", "High-Speed Connector",
                            "Crystal Oscillator", "Supercomputer", "Radio Control Unit",
                            "Turbo Motor", "Reinforced Iron Plate", "Modular Frame",
                            "Heavy Modular Frame", "Fused Modular Frame", "Cooling System",
                            "Battery", "Power Shard", "Silica",
                            }]
print(f"| Item | SCIM Name | Building | SCIM Inputs/min | SCIM Outputs/min | Notes |")
print(f"|------|-----------|----------|----------------|-----------------|-------|")
for r in scim_unmatched_filtered:
    primary = list(r["outputs"].keys())[0]
    in_str = ", ".join(f"{k}: {v:.4g}" for k, v in r["inputs"].items())
    out_str = ", ".join(f"{k}: {v:.4g}" for k, v in r["outputs"].items())
    note = "Recipe not in TSV (possibly removed/replaced in 1.0)"
    print(f"| {primary} | {r['name']} | {r['building']} | {in_str} | {out_str} | {note} |")

if not scim_unmatched_filtered:
    print("| All SCIM recipes matched | | | | | |")

print()

# TSV unmatched — only show non-obvious ones
print("## TSV Recipes NOT Matched in SCIM (production items)")
tsv_unmatched_filtered = [r for r in tsv_unmatched 
                          if r["building"] not in ("Build Gun",) 
                          and r["class"] != "Quantum"
                          and "EW" not in r["recipe_name"]
                          and "Unpackage" not in r["recipe_name"]
                          and r["class"] != ""]

# Only show where the primary item actually exists in SCIM but recipe doesn't match
tsv_unmatched_filtered2 = [r for r in tsv_unmatched_filtered 
                           if list(r["outputs"].keys())[0] in scim_items]

print(f"| Item | TSV Name | Class | Building | TSV Inputs | TSV Outputs | Notes |")
print(f"|------|----------|-------|----------|------------|-------------|-------|")
for r in tsv_unmatched_filtered2:
    primary = list(r["outputs"].keys())[0]
    in_str = ", ".join(f"{k}: {v:g}" for k, v in r["inputs"].items())
    out_str = ", ".join(f"{k}: {v:g}" for k, v in r["outputs"].items())
    note = "SCIM has same item with different recipe"
    print(f"| {primary} | {r['recipe_name']} | {r['class']} | {r['building']} | {in_str} | {out_str} | {note} |")

if not tsv_unmatched_filtered2:
    print("| No unmatched production items | | | | | | |")

print()

# Items in TSV but not in SCIM
print("## Items in TSV that do NOT exist in SCIM data")
tsv_only_filtered = sorted(tsv_only - {"Candy Cane Basher", "Factory Cart™", "Golden Factory Cart™"})
print(f"| Item | TSV Recipe | Class | Likely Reason |")
print(f"|------|------------|-------|---------------|")
for item in tsv_only_filtered:
    for r in tsv_recipes:
        if list(r["outputs"].keys())[0] == item:
            note = "New in 1.0 (postdates SCIM CL-273254)" if r["class"] in ("Quantum", "Alternate") else "Basic recipe (SCIM excludes simple smelting/crafting)"
            print(f"| {item} | {r['recipe_name']} | {r['class']} | {note} |")
            break

print()

# Items in SCIM but not in TSV
print("## Items in SCIM that do NOT exist in TSV")
scim_only_filtered = sorted(scim_only - {"Electromagnetic Control Rod", "Non-fissile Uranium"})
print(f"| Item | SCIM Name | Building | Notes |")
print(f"|------|-----------|----------|-------|")
for item in scim_only_filtered:
    for r in scim_recipes:
        if list(r["outputs"].keys())[0] == item:
            print(f"| {item} | {r['name']} | {r['building']} | Possibly removed in 1.0 |")
            break

print()

# Summary
print("## Summary")
print(f"- SCIM game data build: CL-273254 (Update 8 era)")
print(f"- TSV is current 1.0 recipe data")
print(f"- SCIM recipes parsed (excl FICSMAS/non-production): {len(scim_recipes)}")
print(f"- TSV recipes parsed: {len(tsv_recipes)}")
print(f"- TSV recipes matched to SCIM: {len(matched_tsv)}")
print(f"- Discrepancies (significant rate changes between Update 8 and 1.0): {len(discrepancies)}")
print(f"- SCIM recipes unmatched (item exits in TSV but recipe differs): {len(tsv_unmatched_filtered2) if tsv_unmatched_filtered2 else 0}")
print(f"- Items only in TSV (new in 1.0 or basic recipes): {len(tsv_only_filtered)}")
print(f"- Items only in SCIM (removed in 1.0): {len(scim_only_filtered)}")
print()
print("### Key Interpretation")
print("- Many 'discrepancies' are actual recipe rebalances between Update 8 and 1.0")
print("- SCIM data lacks basic recipes (Iron Ingot, Iron Plate, etc.) — these are")
print("  defined in building components, not in the recipe registry")
print("- SCIM fluid amounts are in internal units (1000 = 1 m³) — corrected in comparison")
print("- Discrepancies in Equipment Workshop recipes are expected (0.5× speed)")
