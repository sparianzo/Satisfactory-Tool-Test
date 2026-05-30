// ============================================================
//  FACTORYCALC — RECIPE DATABASE  v1.2
//  All rates are per minute at 100% clock speed, single machine
//  Auto-generated from verified spreadsheet data.
// ============================================================

const RAW_RESOURCES = new Set([
  'Iron Ore',
  'Copper Ore',
  'Limestone',
  'Coal',
  'Caterium Ore',
  'Raw Quartz',
  'Sulfur',
  'Bauxite',
  'Uranium',
  'SAM',
  'Crude Oil',
  'Water',
  'Nitrogen Gas',
  'Leaves',
  'Wood',
  'Mycelia',
  'Blue Power Slug',
  'Yellow Power Slug',
  'Purple Power Slug',
  'Hatcher Remains',
  'Hog Remains',
  'Plasma Spitter Remains',
  'Stinger Remains',
  'Flower Petals',
  'Beryl Nut',
  'Paleberry',
  'Bacon Agaric',
  'Ficsite Ore',
  'Diamonds',
  'Dark Matter Residue',
  'Uranium Waste',
  'Plutonium Waste',
]);

const RECIPES = {
  'AI Expansion Server': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 500.0,
        output: 4.0,
        inputs: [{"item": "Magnetic Field Generator", "qty": 4.0}, {"item": "Neural-Quantum Processor", "qty": 4.0}, {"item": "Superposition Oscillator", "qty": 4.0}, {"item": "Excited Photonic Matter", "qty": 100.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 100.0}
      },
    }
  },
  'AI Limiter': {
    alts: ["Basic", "Alt: Plastic AI Limiter"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Copper Sheet", "qty": 25.0}, {"item": "Quickwire", "qty": 100.0}]
      },
      'Alt: Plastic AI Limiter': {
        building: 'Assembler',
        mw: 15.0,
        output: 8.0,
        inputs: [{"item": "Quickwire", "qty": 120.0}, {"item": "Plastic", "qty": 28.0}],
        tier: 'S'
      },
    }
  },
  'Adaptive Control Unit': {
    alts: ["Basic", "Basic (Mfr)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 1.0,
        inputs: [{"item": "Automated Wiring", "qty": 7.5}, {"item": "Circuit Board", "qty": 5.0}]
      },
      'Basic (Mfr)': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.0,
        inputs: [{"item": "Automated Wiring", "qty": 5.0}, {"item": "Circuit Board", "qty": 5.0}, {"item": "Heavy Modular Frame", "qty": 2.0}, {"item": "Computer", "qty": 1.0}]
      },
    }
  },
  'Alclad Aluminum Sheet': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 30.0,
        inputs: [{"item": "Aluminum Ingot", "qty": 30.0}, {"item": "Copper Ingot", "qty": 10.0}]
      },
    }
  },
  'Alien DNA Capsule': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 10.0,
        inputs: [{"item": "Alien Protein", "qty": 10.0}]
      },
    }
  },
  'Alien Power Matrix': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 500.0,
        output: 2.5,
        inputs: [{"item": "SAM Fluctuator", "qty": 12.5}, {"item": "Power Shard", "qty": 7.5}, {"item": "Superposition Oscillator", "qty": 7.5}, {"item": "Excited Photonic Matter", "qty": 60.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 60.0}
      },
    }
  },
  'Alien Protein': {
    alts: ["Basic (Hatcher)", "Basic (Hog)", "Basic (Plasma Spitter)", "Basic (Stinger)"],
    recipes: {
      'Basic (Hatcher)': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Hatcher Remains", "qty": 20.0}]
      },
      'Basic (Hog)': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Hog Remains", "qty": 20.0}]
      },
      'Basic (Plasma Spitter)': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Plasma Spitter Remains", "qty": 20.0}]
      },
      'Basic (Stinger)': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Stinger Remains", "qty": 20.0}]
      },
    }
  },
  'Alumina Solution': {
    alts: ["Basic", "Alt: Sloppy Alumina"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 120.0,
        inputs: [{"item": "Packaged Alumina Solution", "qty": 120.0}],
        byproduct: {"item": "Empty Canister", "qty": 120.0}
      },
      'Alt: Sloppy Alumina': {
        building: 'Refinery',
        mw: 30.0,
        output: 240.0,
        inputs: [{"item": "Bauxite", "qty": 200.0}, {"item": "Water", "qty": 200.0}],
        tier: 'S'
      },
    }
  },
  'Aluminum Casing': {
    alts: ["Basic", "Alt: Alclad Casing"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Aluminum Ingot", "qty": 90.0}]
      },
      'Alt: Alclad Casing': {
        building: 'Assembler',
        mw: 15.0,
        output: 112.5,
        inputs: [{"item": "Aluminum Ingot", "qty": 150.0}, {"item": "Copper Ingot", "qty": 75.0}],
        tier: 'F'
      },
    }
  },
  'Aluminum Ingot': {
    alts: ["Basic", "Alt: Pure Aluminum Ingot"],
    recipes: {
      'Basic': {
        building: 'Foundry',
        mw: 16.0,
        output: 60.0,
        inputs: [{"item": "Aluminum Scrap", "qty": 90.0}, {"item": "Silica", "qty": 75.0}]
      },
      'Alt: Pure Aluminum Ingot': {
        building: 'Smelter',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Aluminum Scrap", "qty": 60.0}],
        tier: 'C'
      },
    }
  },
  'Aluminum Scrap': {
    alts: ["Basic", "Alt: Electrode Aluminum Scrap", "Alt: Instant Scrap"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 360.0,
        inputs: [{"item": "Alumina Solution", "qty": 240.0}, {"item": "Coal", "qty": 120.0}],
        byproduct: {"item": "Water", "qty": 120.0}
      },
      'Alt: Electrode Aluminum Scrap': {
        building: 'Refinery',
        mw: 30.0,
        output: 300.0,
        inputs: [{"item": "Alumina Solution", "qty": 180.0}, {"item": "Petroleum Coke", "qty": 60.0}],
        tier: 'B',
        byproduct: {"item": "Water", "qty": 105.0}
      },
      'Alt: Instant Scrap': {
        building: 'Blender',
        mw: 75.0,
        output: 300.0,
        inputs: [{"item": "Bauxite", "qty": 150.0}, {"item": "Coal", "qty": 100.0}, {"item": "Sulfuric Acid", "qty": 50.0}, {"item": "Water", "qty": 60.0}],
        tier: 'F',
        byproduct: {"item": "Water", "qty": 50.0}
      },
    }
  },
  'Assembly Director System': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 0.75,
        inputs: [{"item": "Adaptive Control Unit", "qty": 1.5}, {"item": "Supercomputer", "qty": 0.75}]
      },
    }
  },
  'Automated Wiring': {
    alts: ["Basic", "Alt: Automated Speed Wiring"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 2.5,
        inputs: [{"item": "Stator", "qty": 2.5}, {"item": "Cable", "qty": 50.0}]
      },
      'Alt: Automated Speed Wiring': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 7.5,
        inputs: [{"item": "Stator", "qty": 3.75}, {"item": "Wire", "qty": 75.0}, {"item": "High-Speed Connector", "qty": 1.875}],
        tier: 'S'
      },
    }
  },
  'Ballistic Warp Drive': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.0,
        inputs: [{"item": "Thermal Propulsion Rocket", "qty": 1.0}, {"item": "Singularity Cell", "qty": 5.0}, {"item": "Superposition Oscillator", "qty": 2.0}, {"item": "Dark Matter Crystal", "qty": 40.0}]
      },
    }
  },
  'Battery': {
    alts: ["Basic", "Alt: Classic Battery"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 20.0,
        inputs: [{"item": "Sulfuric Acid", "qty": 50.0}, {"item": "Alumina Solution", "qty": 40.0}, {"item": "Aluminum Casing", "qty": 20.0}],
        byproduct: {"item": "Water", "qty": 30.0}
      },
      'Alt: Classic Battery': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 30.0,
        inputs: [{"item": "Sulfur", "qty": 45.0}, {"item": "Alclad Aluminum Sheet", "qty": 52.5}, {"item": "Plastic", "qty": 60.0}, {"item": "Wire", "qty": 90.0}],
        tier: 'F'
      },
    }
  },
  'Bauxite': {
    alts: ["Basic (Caterium)", "Basic (Copper)"],
    recipes: {
      'Basic (Caterium)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Caterium Ore", "qty": 150.0}]
      },
      'Basic (Copper)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Copper Ore", "qty": 180.0}]
      },
    }
  },
  'Biochemical Sculptor': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 2.0,
        inputs: [{"item": "Assembly Director System", "qty": 0.5}, {"item": "Ficsite Trigon", "qty": 40.0}, {"item": "Water", "qty": 10.0}]
      },
    }
  },
  'Biomass': {
    alts: ["Basic (Alien Protein)", "Basic (Leaves)", "Basic (Mycelia)", "Basic (Wood)"],
    recipes: {
      'Basic (Alien Protein)': {
        building: 'Constructor',
        mw: 4.0,
        output: 1500.0,
        inputs: [{"item": "Alien Protein", "qty": 15.0}]
      },
      'Basic (Leaves)': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Leaves", "qty": 120.0}]
      },
      'Basic (Mycelia)': {
        building: 'Constructor',
        mw: 4.0,
        output: 150.0,
        inputs: [{"item": "Mycelia", "qty": 15.0}]
      },
      'Basic (Wood)': {
        building: 'Constructor',
        mw: 4.0,
        output: 300.0,
        inputs: [{"item": "Wood", "qty": 60.0}]
      },
    }
  },
  'Black Powder': {
    alts: ["Basic", "Basic (EW)", "Alt: Fine Black Powder"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 30.0,
        inputs: [{"item": "Coal", "qty": 15.0}, {"item": "Sulfur", "qty": 15.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 15.0,
        inputs: [{"item": "Coal", "qty": 7.5}, {"item": "Sulfur", "qty": 5.0}]
      },
      'Alt: Fine Black Powder': {
        building: 'Assembler',
        mw: 15.0,
        output: 45.0,
        inputs: [{"item": "Sulfur", "qty": 7.5}, {"item": "Compacted Coal", "qty": 15.0}],
        tier: 'D'
      },
    }
  },
  'Blade Runners': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Silica", "qty": 20.0}, {"item": "Modular Frame", "qty": 3.0}, {"item": "Rotor", "qty": 3.0}]
      },
    }
  },
  'Cable': {
    alts: ["Basic", "Alt: Coated Cable", "Alt: Insulated Cable", "Alt: Quickwire Cable"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Wire", "qty": 60.0}]
      },
      'Alt: Coated Cable': {
        building: 'Refinery',
        mw: 30.0,
        output: 67.5,
        inputs: [{"item": "Wire", "qty": 37.5}, {"item": "Heavy Oil Residue", "qty": 15.0}],
        tier: 'D'
      },
      'Alt: Insulated Cable': {
        building: 'Assembler',
        mw: 15.0,
        output: 100.0,
        inputs: [{"item": "Wire", "qty": 45.0}, {"item": "Rubber", "qty": 30.0}],
        tier: 'D'
      },
      'Alt: Quickwire Cable': {
        building: 'Assembler',
        mw: 15.0,
        output: 27.5,
        inputs: [{"item": "Quickwire", "qty": 7.5}, {"item": "Rubber", "qty": 5.0}],
        tier: 'D'
      },
    }
  },
  'Caterium Ingot': {
    alts: ["Basic", "Alt: Leached Caterium Ingot", "Alt: Pure Caterium Ingot", "Alt: Tempered Caterium Ingot"],
    recipes: {
      'Basic': {
        building: 'Smelter',
        mw: 4.0,
        output: 15.0,
        inputs: [{"item": "Caterium Ore", "qty": 45.0}]
      },
      'Alt: Leached Caterium Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 36.0,
        inputs: [{"item": "Caterium Ore", "qty": 54.0}, {"item": "Sulfuric Acid", "qty": 30.0}],
        tier: 'D'
      },
      'Alt: Pure Caterium Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 12.0,
        inputs: [{"item": "Caterium Ore", "qty": 24.0}, {"item": "Water", "qty": 24.0}],
        tier: 'S'
      },
      'Alt: Tempered Caterium Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 22.5,
        inputs: [{"item": "Caterium Ore", "qty": 45.0}, {"item": "Petroleum Coke", "qty": 15.0}],
        tier: 'D'
      },
    }
  },
  'Caterium Ore': {
    alts: ["Basic (Copper)", "Basic (Quartz)"],
    recipes: {
      'Basic (Copper)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Copper Ore", "qty": 150.0}]
      },
      'Basic (Quartz)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Raw Quartz", "qty": 120.0}]
      },
    }
  },
  'Chainsaw': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 5.0}, {"item": "Iron Rod", "qty": 25.0}, {"item": "Screw", "qty": 160.0}, {"item": "Cable", "qty": 15.0}]
      },
    }
  },
  'Circuit Board': {
    alts: ["Basic", "Alt: Caterium Circuit Board", "Alt: Electrode Circuit Board", "Alt: Silicon Circuit Board"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 7.5,
        inputs: [{"item": "Copper Sheet", "qty": 15.0}, {"item": "Plastic", "qty": 30.0}]
      },
      'Alt: Caterium Circuit Board': {
        building: 'Assembler',
        mw: 15.0,
        output: 8.75,
        inputs: [{"item": "Plastic", "qty": 12.5}, {"item": "Quickwire", "qty": 37.5}],
        tier: 'B'
      },
      'Alt: Electrode Circuit Board': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Rubber", "qty": 20.0}, {"item": "Petroleum Coke", "qty": 40.0}],
        tier: 'S'
      },
      'Alt: Silicon Circuit Board': {
        building: 'Assembler',
        mw: 15.0,
        output: 12.5,
        inputs: [{"item": "Copper Sheet", "qty": 27.5}, {"item": "Silica", "qty": 27.5}],
        tier: 'B'
      },
    }
  },
  'Cluster Nobelisk': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 2.5,
        inputs: [{"item": "Nobelisk", "qty": 7.5}, {"item": "Smokeless Powder", "qty": 10.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.25,
        inputs: [{"item": "Nobelisk", "qty": 3.75}, {"item": "Smokeless Powder", "qty": 5.0}]
      },
    }
  },
  'Coal': {
    alts: ["Basic", "Basic (Biocoal)", "Basic (Iron)", "Basic (Limestone)"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 150.0,
        inputs: [{"item": "Wood", "qty": 15.0}],
        tier: 'F'
      },
      'Basic (Biocoal)': {
        building: 'Constructor',
        mw: 4.0,
        output: 45.0,
        inputs: [{"item": "Biomass", "qty": 37.5}],
        tier: 'F'
      },
      'Basic (Iron)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Iron Ore", "qty": 180.0}]
      },
      'Basic (Limestone)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Limestone", "qty": 360.0}]
      },
    }
  },
  'Color Cartridge': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 100.0,
        inputs: [{"item": "Flower Petals", "qty": 50.0}]
      },
    }
  },
  'Compacted Coal': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 25.0,
        inputs: [{"item": "Coal", "qty": 25.0}, {"item": "Sulfur", "qty": 25.0}],
        tier: 'S'
      },
    }
  },
  'Computer': {
    alts: ["Basic", "Alt: Caterium Computer", "Alt: Crystal Computer"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.5,
        inputs: [{"item": "Circuit Board", "qty": 10.0}, {"item": "Cable", "qty": 20.0}, {"item": "Plastic", "qty": 40.0}]
      },
      'Alt: Caterium Computer': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Circuit Board", "qty": 15.0}, {"item": "Quickwire", "qty": 52.5}, {"item": "Rubber", "qty": 22.5}],
        tier: 'C'
      },
      'Alt: Crystal Computer': {
        building: 'Assembler',
        mw: 15.0,
        output: 3.33333,
        inputs: [{"item": "Circuit Board", "qty": 5.0}, {"item": "Crystal Oscillator", "qty": 1.66667}],
        tier: 'A'
      },
    }
  },
  'Concrete': {
    alts: ["Basic", "Alt: Fine Concrete", "Alt: Rubber Concrete", "Alt: Wet Concrete"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 15.0,
        inputs: [{"item": "Limestone", "qty": 45.0}]
      },
      'Alt: Fine Concrete': {
        building: 'Assembler',
        mw: 15.0,
        output: 50.0,
        inputs: [{"item": "Silica", "qty": 15.0}, {"item": "Limestone", "qty": 60.0}],
        tier: 'B'
      },
      'Alt: Rubber Concrete': {
        building: 'Assembler',
        mw: 15.0,
        output: 90.0,
        inputs: [{"item": "Limestone", "qty": 100.0}, {"item": "Rubber", "qty": 20.0}],
        tier: 'D'
      },
      'Alt: Wet Concrete': {
        building: 'Refinery',
        mw: 30.0,
        output: 80.0,
        inputs: [{"item": "Limestone", "qty": 120.0}, {"item": "Water", "qty": 100.0}],
        tier: 'A'
      },
    }
  },
  'Cooling System': {
    alts: ["Basic", "Alt: Cooling Device"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 6.0,
        inputs: [{"item": "Heat Sink", "qty": 12.0}, {"item": "Rubber", "qty": 12.0}, {"item": "Water", "qty": 30.0}, {"item": "Nitrogen Gas", "qty": 150.0}]
      },
      'Alt: Cooling Device': {
        building: 'Blender',
        mw: 75.0,
        output: 5.0,
        inputs: [{"item": "Heat Sink", "qty": 10.0}, {"item": "Motor", "qty": 2.5}, {"item": "Nitrogen Gas", "qty": 60.0}],
        tier: 'C'
      },
    }
  },
  'Copper Ingot': {
    alts: ["Basic", "Alt: Copper Alloy Ingot", "Alt: Leached Copper Ingot", "Alt: Pure Copper Ingot", "Alt: Tempered Copper Ingot"],
    recipes: {
      'Basic': {
        building: 'Smelter',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Copper Ore", "qty": 30.0}]
      },
      'Alt: Copper Alloy Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 100.0,
        inputs: [{"item": "Copper Ore", "qty": 50.0}, {"item": "Iron Ore", "qty": 50.0}],
        tier: 'D'
      },
      'Alt: Leached Copper Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 110.0,
        inputs: [{"item": "Copper Ore", "qty": 45.0}, {"item": "Sulfuric Acid", "qty": 25.0}],
        tier: 'D'
      },
      'Alt: Pure Copper Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 37.5,
        inputs: [{"item": "Copper Ore", "qty": 15.0}, {"item": "Water", "qty": 10.0}],
        tier: 'S'
      },
      'Alt: Tempered Copper Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 60.0,
        inputs: [{"item": "Copper Ore", "qty": 25.0}, {"item": "Petroleum Coke", "qty": 40.0}],
        tier: 'D'
      },
    }
  },
  'Copper Ore': {
    alts: ["Basic (Quartz)", "Basic (Sulfur)"],
    recipes: {
      'Basic (Quartz)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Raw Quartz", "qty": 100.0}]
      },
      'Basic (Sulfur)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Sulfur", "qty": 120.0}]
      },
    }
  },
  'Copper Powder': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 50.0,
        inputs: [{"item": "Copper Ingot", "qty": 300.0}]
      },
    }
  },
  'Copper Sheet': {
    alts: ["Basic", "Alt: Steamed Copper Sheet"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 10.0,
        inputs: [{"item": "Copper Ingot", "qty": 20.0}]
      },
      'Alt: Steamed Copper Sheet': {
        building: 'Refinery',
        mw: 30.0,
        output: 22.5,
        inputs: [{"item": "Copper Ingot", "qty": 22.5}, {"item": "Water", "qty": 22.5}],
        tier: 'C'
      },
    }
  },
  'Crude Oil': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Packaged Oil", "qty": 60.0}],
        byproduct: {"item": "Empty Canister", "qty": 60.0}
      },
    }
  },
  'Crystal Oscillator': {
    alts: ["Basic", "Alt: Insulated Crystal Oscillator"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.0,
        inputs: [{"item": "Quartz Crystal", "qty": 18.0}, {"item": "Cable", "qty": 14.0}, {"item": "Reinforced Iron Plate", "qty": 2.5}]
      },
      'Alt: Insulated Crystal Oscillator': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.875,
        inputs: [{"item": "Quartz Crystal", "qty": 18.75}, {"item": "Rubber", "qty": 13.125}, {"item": "AI Limiter", "qty": 1.875}],
        tier: 'S'
      },
    }
  },
  'Dark Matter Crystal': {
    alts: ["Basic", "Alt: Dark Matter Crystallization", "Alt: Dark Matter Trap"],
    recipes: {
      'Basic': {
        building: 'Particle Accelerator',
        mw: 1000.0,
        output: 30.0,
        inputs: [{"item": "Diamonds", "qty": 30.0}, {"item": "Dark Matter Residue", "qty": 150.0}]
      },
      'Alt: Dark Matter Crystallization': {
        building: 'Particle Accelerator',
        mw: 1000.0,
        output: 20.0,
        inputs: [{"item": "Dark Matter Residue", "qty": 200.0}],
        tier: 'C'
      },
      'Alt: Dark Matter Trap': {
        building: 'Particle Accelerator',
        mw: 1000.0,
        output: 60.0,
        inputs: [{"item": "Time Crystal", "qty": 30.0}, {"item": "Dark Matter Residue", "qty": 150.0}],
        tier: 'S'
      },
    }
  },
  'Dark Matter Residue': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Converter',
        mw: 250.0,
        output: 100.0,
        inputs: [{"item": "Reanimated SAM", "qty": 50.0}]
      },
    }
  },
  'Diamonds': {
    alts: ["Basic", "Alt: Cloudy Diamond", "Alt: Oil-Based Diamonds", "Alt: Petroleum Diamonds", "Alt: Pink Diamonds", "Alt: Turbo Diamonds"],
    recipes: {
      'Basic': {
        building: 'Particle Accelerator',
        mw: 250.0,
        output: 30.0,
        inputs: [{"item": "Coal", "qty": 600.0}]
      },
      'Alt: Cloudy Diamond': {
        building: 'Particle Accelerator',
        mw: 250.0,
        output: 20.0,
        inputs: [{"item": "Coal", "qty": 240.0}, {"item": "Limestone", "qty": 480.0}],
        tier: 'D'
      },
      'Alt: Oil-Based Diamonds': {
        building: 'Particle Accelerator',
        mw: 250.0,
        output: 40.0,
        inputs: [{"item": "Crude Oil", "qty": 200.0}],
        tier: 'B'
      },
      'Alt: Petroleum Diamonds': {
        building: 'Particle Accelerator',
        mw: 250.0,
        output: 30.0,
        inputs: [{"item": "Petroleum Coke", "qty": 720.0}],
        tier: 'F'
      },
      'Alt: Pink Diamonds': {
        building: 'Converter',
        mw: 250.0,
        output: 15.0,
        inputs: [{"item": "Coal", "qty": 120.0}, {"item": "Quartz Crystal", "qty": 45.0}],
        tier: 'C'
      },
      'Alt: Turbo Diamonds': {
        building: 'Particle Accelerator',
        mw: 250.0,
        output: 60.0,
        inputs: [{"item": "Coal", "qty": 600.0}, {"item": "Packaged Turbofuel", "qty": 40.0}],
        tier: 'C'
      },
    }
  },
  'Dissolved Silica': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 70.0,
        inputs: [{"item": "Silica", "qty": 40.0}, {"item": "Nitric Acid", "qty": 10.0}]
      },
    }
  },
  'EM Control Rod': {
    alts: ["Basic", "Alt: Electromagnetic Connection Rod"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 4.0,
        inputs: [{"item": "Stator", "qty": 6.0}, {"item": "AI Limiter", "qty": 4.0}]
      },
      'Alt: Electromagnetic Connection Rod': {
        building: 'Assembler',
        mw: 15.0,
        output: 8.0,
        inputs: [{"item": "Stator", "qty": 8.0}, {"item": "High-Speed Connector", "qty": 4.0}],
        tier: 'D'
      },
    }
  },
  'Electromagnetic Turbine': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 2.5,
        inputs: [{"item": "Wire", "qty": 12.0}, {"item": "Rotor", "qty": 2.5}]
      },
    }
  },
  'Empty Canister': {
    alts: ["Basic", "Alt: Coated Iron Canister", "Alt: Steel Canister"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Plastic", "qty": 30.0}]
      },
      'Alt: Coated Iron Canister': {
        building: 'Assembler',
        mw: 15.0,
        output: 60.0,
        inputs: [{"item": "Iron Plate", "qty": 30.0}, {"item": "Copper Sheet", "qty": 15.0}],
        tier: 'D'
      },
      'Alt: Steel Canister': {
        building: 'Constructor',
        mw: 4.0,
        output: 40.0,
        inputs: [{"item": "Steel Ingot", "qty": 40.0}],
        tier: 'D'
      },
    }
  },
  'Empty Fluid Tank': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Aluminum Ingot", "qty": 60.0}]
      },
    }
  },
  'Encased Industrial Beam': {
    alts: ["Basic", "Alt: Encased Industrial Pipe"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 6.0,
        inputs: [{"item": "Steel Beam", "qty": 18.0}, {"item": "Concrete", "qty": 36.0}]
      },
      'Alt: Encased Industrial Pipe': {
        building: 'Assembler',
        mw: 15.0,
        output: 4.0,
        inputs: [{"item": "Steel Pipe", "qty": 24.0}, {"item": "Concrete", "qty": 20.0}],
        tier: 'B'
      },
    }
  },
  'Encased Plutonium Cell': {
    alts: ["Basic", "Alt: Instant Plutonium Cell"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Plutonium Pellet", "qty": 10.0}, {"item": "Concrete", "qty": 20.0}]
      },
      'Alt: Instant Plutonium Cell': {
        building: 'Particle Accelerator',
        mw: 500.0,
        output: 10.0,
        inputs: [{"item": "Non-Fissile Uranium", "qty": 75.0}, {"item": "Aluminum Casing", "qty": 10.0}],
        tier: 'F'
      },
    }
  },
  'Encased Uranium Cell': {
    alts: ["Basic", "Alt: Infused Uranium Cell"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 25.0,
        inputs: [{"item": "Uranium", "qty": 50.0}, {"item": "Concrete", "qty": 15.0}, {"item": "Sulfuric Acid", "qty": 40.0}],
        byproduct: {"item": "Sulfuric Acid", "qty": 10.0}
      },
      'Alt: Infused Uranium Cell': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 20.0,
        inputs: [{"item": "Uranium", "qty": 25.0}, {"item": "Silica", "qty": 15.0}, {"item": "Sulfur", "qty": 25.0}, {"item": "Quickwire", "qty": 75.0}],
        tier: 'B'
      },
    }
  },
  'Excited Photonic Matter': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Converter',
        mw: 250.0,
        output: 200.0,
        inputs: []
      },
    }
  },
  'Explosive Rebar': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 5.0,
        inputs: [{"item": "Iron Rebar", "qty": 10.0}, {"item": "Smokeless Powder", "qty": 10.0}, {"item": "Steel Pipe", "qty": 10.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 2.5,
        inputs: [{"item": "Iron Rebar", "qty": 5.0}, {"item": "Smokeless Powder", "qty": 5.0}, {"item": "Steel Pipe", "qty": 5.0}]
      },
    }
  },
  'Fabric': {
    alts: ["Basic", "Basic (Polyester)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 15.0,
        inputs: [{"item": "Mycelia", "qty": 15.0}, {"item": "Biomass", "qty": 75.0}]
      },
      'Basic (Polyester)': {
        building: 'Refinery',
        mw: 30.0,
        output: 30.0,
        inputs: [{"item": "Polymer Resin", "qty": 30.0}, {"item": "Water", "qty": 30.0}],
        tier: 'A'
      },
    }
  },
  'Factory Cart': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 12.0}, {"item": "Iron Rod", "qty": 12.0}, {"item": "Rotor", "qty": 6.0}]
      },
    }
  },
  'Ficsite Ingot': {
    alts: ["Basic (Aluminum)", "Basic (Caterium)", "Basic (Iron)"],
    recipes: {
      'Basic (Aluminum)': {
        building: 'Converter',
        mw: 250.0,
        output: 30.0,
        inputs: [{"item": "Reanimated SAM", "qty": 60.0}, {"item": "Aluminum Ingot", "qty": 120.0}]
      },
      'Basic (Caterium)': {
        building: 'Converter',
        mw: 250.0,
        output: 15.0,
        inputs: [{"item": "Reanimated SAM", "qty": 45.0}, {"item": "Caterium Ingot", "qty": 60.0}]
      },
      'Basic (Iron)': {
        building: 'Converter',
        mw: 250.0,
        output: 10.0,
        inputs: [{"item": "Reanimated SAM", "qty": 40.0}, {"item": "Iron Ingot", "qty": 240.0}]
      },
    }
  },
  'Ficsite Trigon': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Ficsite Ingot", "qty": 10.0}]
      },
    }
  },
  'Ficsonium': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Particle Accelerator',
        mw: 1000.0,
        output: 10.0,
        inputs: [{"item": "Plutonium Waste", "qty": 10.0}, {"item": "Singularity Cell", "qty": 10.0}, {"item": "Dark Matter Residue", "qty": 200.0}]
      },
    }
  },
  'Ficsonium Fuel Rod': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 1000.0,
        output: 2.5,
        inputs: [{"item": "Ficsonium", "qty": 5.0}, {"item": "EM Control Rod", "qty": 5.0}, {"item": "Ficsite Trigon", "qty": 100.0}, {"item": "Excited Photonic Matter", "qty": 50.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 50.0}
      },
    }
  },
  'Fuel': {
    alts: ["Basic", "Alt: Diluted Fuel"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Packaged Fuel", "qty": 60.0}],
        byproduct: {"item": "Empty Canister", "qty": 60.0}
      },
      'Alt: Diluted Fuel': {
        building: 'Blender',
        mw: 75.0,
        output: 100.0,
        inputs: [{"item": "Heavy Oil Residue", "qty": 50.0}, {"item": "Water", "qty": 100.0}],
        tier: 'S'
      },
    }
  },
  'Fused Modular Frame': {
    alts: ["Basic", "Alt: Heat Fused Frame"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 1.5,
        inputs: [{"item": "Heavy Modular Frame", "qty": 1.5}, {"item": "Aluminum Casing", "qty": 75.0}, {"item": "Nitrogen Gas", "qty": 37.5}]
      },
      'Alt: Heat Fused Frame': {
        building: 'Blender',
        mw: 75.0,
        output: 3.0,
        inputs: [{"item": "Heavy Modular Frame", "qty": 3.0}, {"item": "Aluminum Ingot", "qty": 150.0}, {"item": "Nitric Acid", "qty": 24.0}, {"item": "Fuel", "qty": 30.0}],
        tier: 'D'
      },
    }
  },
  'Gas Filter': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 7.5,
        inputs: [{"item": "Coal", "qty": 30.0}, {"item": "Iron Plate", "qty": 15.0}, {"item": "Fabric", "qty": 15.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.75,
        inputs: [{"item": "Fabric", "qty": 7.5}, {"item": "Coal", "qty": 15.0}, {"item": "Iron Plate", "qty": 7.5}]
      },
    }
  },
  'Gas Mask': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Fabric", "qty": 50.0}, {"item": "Copper Sheet", "qty": 10.0}, {"item": "Steel Pipe", "qty": 10.0}]
      },
    }
  },
  'Gas Nobelisk': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Nobelisk", "qty": 5.0}, {"item": "Biomass", "qty": 50.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 2.5,
        inputs: [{"item": "Nobelisk", "qty": 2.5}, {"item": "Biomass", "qty": 25.0}]
      },
    }
  },
  'Golden Factory Cart': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Caterium Ingot", "qty": 45.0}, {"item": "Iron Rod", "qty": 12.0}, {"item": "Rotor", "qty": 6.0}]
      },
    }
  },
  'Hazmat Suit': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.5,
        inputs: [{"item": "Rubber", "qty": 25.0}, {"item": "Plastic", "qty": 25.0}, {"item": "Alclad Aluminum Sheet", "qty": 25.0}, {"item": "Fabric", "qty": 25.0}]
      },
    }
  },
  'Heat Sink': {
    alts: ["Basic", "Alt: Heat Exchanger"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 7.5,
        inputs: [{"item": "Alclad Aluminum Sheet", "qty": 37.5}, {"item": "Copper Sheet", "qty": 22.5}]
      },
      'Alt: Heat Exchanger': {
        building: 'Assembler',
        mw: 15.0,
        output: 10.0,
        inputs: [{"item": "Aluminum Casing", "qty": 30.0}, {"item": "Rubber", "qty": 30.0}],
        tier: 'A'
      },
    }
  },
  'Heavy Modular Frame': {
    alts: ["Basic", "Alt: Heavy Encased Frame", "Alt: Heavy Flexible Frame"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.0,
        inputs: [{"item": "Modular Frame", "qty": 10.0}, {"item": "Steel Pipe", "qty": 40.0}, {"item": "Encased Industrial Beam", "qty": 10.0}, {"item": "Screw", "qty": 240.0}]
      },
      'Alt: Heavy Encased Frame': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.8125,
        inputs: [{"item": "Modular Frame", "qty": 7.5}, {"item": "Encased Industrial Beam", "qty": 9.375}, {"item": "Steel Pipe", "qty": 33.75}, {"item": "Concrete", "qty": 20.625}],
        tier: 'S'
      },
      'Alt: Heavy Flexible Frame': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Modular Frame", "qty": 18.75}, {"item": "Encased Industrial Beam", "qty": 11.25}, {"item": "Rubber", "qty": 75.0}, {"item": "Screw", "qty": 390.0}],
        tier: 'F'
      },
    }
  },
  'Heavy Oil Residue': {
    alts: ["Basic", "Alt: Heavy Oil Residue"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 20.0,
        inputs: [{"item": "Packaged Heavy Oil Residue", "qty": 20.0}],
        byproduct: {"item": "Empty Canister", "qty": 20.0}
      },
      'Alt: Heavy Oil Residue': {
        building: 'Refinery',
        mw: 30.0,
        output: 40.0,
        inputs: [{"item": "Crude Oil", "qty": 30.0}],
        tier: 'S',
        byproduct: {"item": "Polymer Resin", "qty": 20.0}
      },
    }
  },
  'High-Speed Connector': {
    alts: ["Basic", "Alt: Silicon High-Speed Connector"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Quickwire", "qty": 210.0}, {"item": "Cable", "qty": 37.5}, {"item": "Circuit Board", "qty": 3.75}]
      },
      'Alt: Silicon High-Speed Connector': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.0,
        inputs: [{"item": "Quickwire", "qty": 90.0}, {"item": "Silica", "qty": 37.5}, {"item": "Circuit Board", "qty": 3.0}],
        tier: 'S'
      },
    }
  },
  'Homing Rifle Ammo': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 25.0,
        inputs: [{"item": "Rifle Ammo", "qty": 50.0}, {"item": "High-Speed Connector", "qty": 2.5}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 12.5,
        inputs: [{"item": "Rifle Ammo", "qty": 25.0}, {"item": "High-Speed Connector", "qty": 1.25}]
      },
    }
  },
  'Hover Pack': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.5,
        inputs: [{"item": "Motor", "qty": 4.0}, {"item": "Heavy Modular Frame", "qty": 2.0}, {"item": "Computer", "qty": 4.0}, {"item": "Alclad Aluminum Sheet", "qty": 20.0}]
      },
    }
  },
  'Iodine Infused Filter': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Gas Filter", "qty": 3.75}, {"item": "Quickwire", "qty": 30.0}, {"item": "Aluminum Casing", "qty": 3.75}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.875,
        inputs: [{"item": "Gas Filter", "qty": 1.875}, {"item": "Quickwire", "qty": 15.0}, {"item": "Aluminum Casing", "qty": 1.875}]
      },
    }
  },
  'Ionized Fuel': {
    alts: ["Basic", "Basic (Unpackage)", "Alt: Dark-Ion Fuel"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 40.0,
        inputs: [{"item": "Rocket Fuel", "qty": 40.0}, {"item": "Power Shard", "qty": 2.5}],
        tier: 'S',
        byproduct: {"item": "Compacted Coal", "qty": 5.0}
      },
      'Basic (Unpackage)': {
        building: 'Packager',
        mw: 10.0,
        output: 80.0,
        inputs: [{"item": "Packaged Ionized Fuel", "qty": 40.0}],
        byproduct: {"item": "Empty Fluid Tank", "qty": 40.0}
      },
      'Alt: Dark-Ion Fuel': {
        building: 'Converter',
        mw: 250.0,
        output: 200.0,
        inputs: [{"item": "Packaged Rocket Fuel", "qty": 240.0}, {"item": "Dark Matter Crystal", "qty": 80.0}],
        tier: 'F',
        byproduct: {"item": "Compacted Coal", "qty": 40.0}
      },
    }
  },
  'Iron Ingot': {
    alts: ["Basic", "Alt: Basic Iron Ingot", "Alt: Iron Alloy Ingot", "Alt: Leached Iron Ingot", "Alt: Pure Iron Ingot"],
    recipes: {
      'Basic': {
        building: 'Smelter',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Iron Ore", "qty": 30.0}]
      },
      'Alt: Basic Iron Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 50.0,
        inputs: [{"item": "Iron Ore", "qty": 25.0}, {"item": "Limestone", "qty": 40.0}],
        tier: 'D'
      },
      'Alt: Iron Alloy Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 75.0,
        inputs: [{"item": "Iron Ore", "qty": 40.0}, {"item": "Copper Ore", "qty": 10.0}],
        tier: 'A'
      },
      'Alt: Leached Iron Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 100.0,
        inputs: [{"item": "Iron Ore", "qty": 50.0}, {"item": "Sulfuric Acid", "qty": 10.0}],
        tier: 'D'
      },
      'Alt: Pure Iron Ingot': {
        building: 'Refinery',
        mw: 30.0,
        output: 65.0,
        inputs: [{"item": "Iron Ore", "qty": 35.0}, {"item": "Water", "qty": 20.0}],
        tier: 'S'
      },
    }
  },
  'Iron Ore': {
    alts: ["Basic (Limestone)"],
    recipes: {
      'Basic (Limestone)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Limestone", "qty": 240.0}]
      },
    }
  },
  'Iron Plate': {
    alts: ["Basic", "Alt: Coated Iron Plate", "Alt: Steel Cast Plate"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Iron Ingot", "qty": 30.0}]
      },
      'Alt: Coated Iron Plate': {
        building: 'Assembler',
        mw: 15.0,
        output: 75.0,
        inputs: [{"item": "Iron Ingot", "qty": 37.5}, {"item": "Plastic", "qty": 7.5}],
        tier: 'A'
      },
      'Alt: Steel Cast Plate': {
        building: 'Foundry',
        mw: 16.0,
        output: 45.0,
        inputs: [{"item": "Iron Ingot", "qty": 15.0}, {"item": "Steel Ingot", "qty": 15.0}],
        tier: 'B'
      },
    }
  },
  'Iron Rebar': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 15.0,
        inputs: [{"item": "Iron Rod", "qty": 15.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 7.5,
        inputs: [{"item": "Iron Rod", "qty": 7.5}]
      },
    }
  },
  'Iron Rod': {
    alts: ["Basic", "Alt: Aluminum Rod", "Alt: Steel Rod"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 15.0,
        inputs: [{"item": "Iron Ingot", "qty": 15.0}]
      },
      'Alt: Aluminum Rod': {
        building: 'Constructor',
        mw: 4.0,
        output: 52.5,
        inputs: [{"item": "Aluminum Ingot", "qty": 7.5}],
        tier: 'D'
      },
      'Alt: Steel Rod': {
        building: 'Constructor',
        mw: 4.0,
        output: 48.0,
        inputs: [{"item": "Steel Ingot", "qty": 12.0}],
        tier: 'B'
      },
    }
  },
  'Jetpack': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Motor", "qty": 5.0}, {"item": "Steel Pipe", "qty": 10.0}, {"item": "Iron Plate", "qty": 25.0}, {"item": "Wire", "qty": 50.0}]
      },
    }
  },
  'Limestone': {
    alts: ["Basic (Sulfur)"],
    recipes: {
      'Basic (Sulfur)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Sulfur", "qty": 20.0}]
      },
    }
  },
  'Liquid Biofuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Packaged Liquid Biofuel", "qty": 60.0}],
        byproduct: {"item": "Empty Canister", "qty": 60.0}
      },
    }
  },
  'Magnetic Field Generator': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 1.0,
        inputs: [{"item": "Versatile Framework", "qty": 2.5}, {"item": "EM Control Rod", "qty": 1.0}]
      },
    }
  },
  'Medicinal Inhaler': {
    alts: ["Basic (Alien)", "Basic (Berries)", "Basic (Mushrooms)", "Basic (Nutritional)", "Basic (Protein)", "Basic (Therapeutic)", "Basic (Vitamin)"],
    recipes: {
      'Basic (Alien)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 5.0,
        inputs: [{"item": "Alien Protein", "qty": 1.0}, {"item": "Beryl Nut", "qty": 10.0}, {"item": "Paleberry", "qty": 10.0}, {"item": "Bacon Agaric", "qty": 5.0}]
      },
      'Basic (Berries)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Beryl Nut", "qty": 10.0}, {"item": "Paleberry", "qty": 5.0}]
      },
      'Basic (Mushrooms)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Bacon Agaric", "qty": 10.0}]
      },
      'Basic (Nutritional)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Bacon Agaric", "qty": 3.0}, {"item": "Paleberry", "qty": 6.0}, {"item": "Beryl Nut", "qty": 15.0}]
      },
      'Basic (Protein)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Alien Protein", "qty": 3.0}, {"item": "Beryl Nut", "qty": 30.0}]
      },
      'Basic (Therapeutic)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Mycelia", "qty": 45.0}, {"item": "Alien Protein", "qty": 3.0}, {"item": "Bacon Agaric", "qty": 3.0}]
      },
      'Basic (Vitamin)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Mycelia", "qty": 30.0}, {"item": "Paleberry", "qty": 15.0}]
      },
    }
  },
  'Modular Engine': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.0,
        inputs: [{"item": "Motor", "qty": 2.0}, {"item": "Rubber", "qty": 15.0}, {"item": "Smart Plating", "qty": 2.0}]
      },
    }
  },
  'Modular Frame': {
    alts: ["Basic", "Alt: Bolted Frame", "Alt: Steeled Frame"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 2.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 3.0}, {"item": "Iron Rod", "qty": 12.0}]
      },
      'Alt: Bolted Frame': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 7.5}, {"item": "Screw", "qty": 140.0}],
        tier: 'D'
      },
      'Alt: Steeled Frame': {
        building: 'Assembler',
        mw: 15.0,
        output: 3.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 2.0}, {"item": "Steel Pipe", "qty": 10.0}],
        tier: 'B'
      },
    }
  },
  'Motor': {
    alts: ["Basic", "Alt: Electric Motor", "Alt: Rigour Motor"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Rotor", "qty": 10.0}, {"item": "Stator", "qty": 10.0}]
      },
      'Alt: Electric Motor': {
        building: 'Assembler',
        mw: 15.0,
        output: 7.5,
        inputs: [{"item": "EM Control Rod", "qty": 3.75}, {"item": "Rotor", "qty": 7.5}],
        tier: 'D'
      },
      'Alt: Rigour Motor': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 7.5,
        inputs: [{"item": "Rotor", "qty": 3.75}, {"item": "Stator", "qty": 3.75}, {"item": "Crystal Oscillator", "qty": 1.25}],
        tier: 'A'
      },
    }
  },
  'Neural-Quantum Processor': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 500.0,
        output: 3.0,
        inputs: [{"item": "Time Crystal", "qty": 15.0}, {"item": "Supercomputer", "qty": 3.0}, {"item": "Ficsite Trigon", "qty": 45.0}, {"item": "Excited Photonic Matter", "qty": 75.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 75.0}
      },
    }
  },
  'Nitric Acid': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 20.0,
        inputs: [{"item": "Packaged Nitric Acid", "qty": 20.0}],
        byproduct: {"item": "Empty Fluid Tank", "qty": 20.0}
      },
    }
  },
  'Nitrogen Gas': {
    alts: ["Basic", "Basic (Bauxite)", "Basic (Caterium)"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 240.0,
        inputs: [{"item": "Packaged Nitrogen Gas", "qty": 60.0}],
        byproduct: {"item": "Empty Fluid Tank", "qty": 60.0}
      },
      'Basic (Bauxite)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Bauxite", "qty": 100.0}]
      },
      'Basic (Caterium)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Caterium Ore", "qty": 120.0}]
      },
    }
  },
  'Nobelisk': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 10.0,
        inputs: [{"item": "Black Powder", "qty": 20.0}, {"item": "Steel Pipe", "qty": 20.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 3.0,
        inputs: [{"item": "Black Powder", "qty": 7.5}, {"item": "Steel Pipe", "qty": 10.0}]
      },
    }
  },
  'Nobelisk Detonator': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.75,
        inputs: [{"item": "Object Scanner", "qty": 0.75}, {"item": "Steel Beam", "qty": 7.5}, {"item": "Cable", "qty": 37.5}]
      },
    }
  },
  'Non-Fissile Uranium': {
    alts: ["Basic", "Alt: Fertile Uranium"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 50.0,
        inputs: [{"item": "Uranium Waste", "qty": 37.5}, {"item": "Silica", "qty": 25.0}, {"item": "Nitric Acid", "qty": 15.0}, {"item": "Sulfuric Acid", "qty": 15.0}],
        byproduct: {"item": "Water", "qty": 15.0}
      },
      'Alt: Fertile Uranium': {
        building: 'Blender',
        mw: 75.0,
        output: 100.0,
        inputs: [{"item": "Uranium", "qty": 25.0}, {"item": "Uranium Waste", "qty": 25.0}, {"item": "Nitric Acid", "qty": 15.0}, {"item": "Sulfuric Acid", "qty": 25.0}],
        tier: 'F',
        byproduct: {"item": "Water", "qty": 40.0}
      },
    }
  },
  'Nuclear Pasta': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Particle Accelerator',
        mw: 500.0,
        output: 0.5,
        inputs: [{"item": "Copper Powder", "qty": 100.0}, {"item": "Pressure Conversion Cube", "qty": 0.5}]
      },
    }
  },
  'Nuke Nobelisk': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 0.5,
        inputs: [{"item": "Nobelisk", "qty": 2.5}, {"item": "Encased Uranium Cell", "qty": 10.0}, {"item": "Smokeless Powder", "qty": 5.0}, {"item": "AI Limiter", "qty": 3.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.5,
        inputs: [{"item": "Nobelisk", "qty": 2.5}, {"item": "Encased Uranium Cell", "qty": 10.0}, {"item": "Smokeless Powder", "qty": 5.0}]
      },
    }
  },
  'Object Scanner': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.5,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 6.0}, {"item": "Wire", "qty": 30.0}, {"item": "Screw", "qty": 75.0}]
      },
    }
  },
  'Packaged Alumina Solution': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 120.0,
        inputs: [{"item": "Alumina Solution", "qty": 120.0}, {"item": "Empty Canister", "qty": 120.0}]
      },
    }
  },
  'Packaged Fuel': {
    alts: ["Basic", "Alt: Diluted Packaged Fuel"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 40.0,
        inputs: [{"item": "Fuel", "qty": 40.0}, {"item": "Empty Canister", "qty": 40.0}]
      },
      'Alt: Diluted Packaged Fuel': {
        building: 'Refinery',
        mw: 30.0,
        output: 60.0,
        inputs: [{"item": "Heavy Oil Residue", "qty": 30.0}, {"item": "Packaged Water", "qty": 60.0}],
        tier: 'C'
      },
    }
  },
  'Packaged Heavy Oil Residue': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 30.0,
        inputs: [{"item": "Heavy Oil Residue", "qty": 30.0}, {"item": "Empty Canister", "qty": 30.0}]
      },
    }
  },
  'Packaged Ionized Fuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 40.0,
        inputs: [{"item": "Ionized Fuel", "qty": 80.0}, {"item": "Empty Fluid Tank", "qty": 40.0}]
      },
    }
  },
  'Packaged Liquid Biofuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 40.0,
        inputs: [{"item": "Liquid Biofuel", "qty": 40.0}, {"item": "Empty Canister", "qty": 40.0}]
      },
    }
  },
  'Packaged Nitric Acid': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 30.0,
        inputs: [{"item": "Nitric Acid", "qty": 30.0}, {"item": "Empty Fluid Tank", "qty": 30.0}]
      },
    }
  },
  'Packaged Nitrogen Gas': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Nitrogen Gas", "qty": 240.0}, {"item": "Empty Fluid Tank", "qty": 60.0}]
      },
    }
  },
  'Packaged Oil': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 30.0,
        inputs: [{"item": "Crude Oil", "qty": 30.0}, {"item": "Empty Canister", "qty": 30.0}]
      },
    }
  },
  'Packaged Rocket Fuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Rocket Fuel", "qty": 120.0}, {"item": "Empty Fluid Tank", "qty": 60.0}]
      },
    }
  },
  'Packaged Sulfuric Acid': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 40.0,
        inputs: [{"item": "Sulfuric Acid", "qty": 40.0}, {"item": "Empty Canister", "qty": 40.0}]
      },
    }
  },
  'Packaged Turbofuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 20.0,
        inputs: [{"item": "Turbofuel", "qty": 20.0}, {"item": "Empty Canister", "qty": 20.0}]
      },
    }
  },
  'Packaged Water': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Water", "qty": 60.0}, {"item": "Empty Canister", "qty": 60.0}]
      },
    }
  },
  'Parachute': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.5,
        inputs: [{"item": "Fabric", "qty": 30.0}, {"item": "Cable", "qty": 15.0}]
      },
    }
  },
  'Petroleum Coke': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 120.0,
        inputs: [{"item": "Heavy Oil Residue", "qty": 40.0}]
      },
    }
  },
  'Plastic': {
    alts: ["Basic", "Alt: Recycled Plastic"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 20.0,
        inputs: [{"item": "Polymer Resin", "qty": 60.0}, {"item": "Water", "qty": 20.0}]
      },
      'Alt: Recycled Plastic': {
        building: 'Refinery',
        mw: 30.0,
        output: 60.0,
        inputs: [{"item": "Rubber", "qty": 30.0}, {"item": "Fuel", "qty": 30.0}],
        tier: 'A'
      },
    }
  },
  'Plutonium Fuel Rod': {
    alts: ["Basic", "Alt: Plutonium Fuel Unit"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 0.25,
        inputs: [{"item": "Encased Plutonium Cell", "qty": 7.5}, {"item": "Steel Beam", "qty": 4.5}, {"item": "EM Control Rod", "qty": 1.5}, {"item": "Heat Sink", "qty": 2.5}]
      },
      'Alt: Plutonium Fuel Unit': {
        building: 'Assembler',
        mw: 15.0,
        output: 0.5,
        inputs: [{"item": "Encased Plutonium Cell", "qty": 10.0}, {"item": "Pressure Conversion Cube", "qty": 0.5}],
        tier: 'D'
      },
    }
  },
  'Plutonium Pellet': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Particle Accelerator',
        mw: 500.0,
        output: 30.0,
        inputs: [{"item": "Non-Fissile Uranium", "qty": 100.0}, {"item": "Uranium Waste", "qty": 25.0}]
      },
    }
  },
  'Plutonium Waste': {
    alts: ["Basic (burning)"],
    recipes: {
      'Basic (burning)': {
        building: 'Nuclear Power Plant',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Plutonium Fuel Rod", "qty": 0.1}, {"item": "Water", "qty": 240.0}]
      },
    }
  },
  'Polymer Resin': {
    alts: ["Alt: Polymer Resin"],
    recipes: {
      'Alt: Polymer Resin': {
        building: 'Refinery',
        mw: 30.0,
        output: 130.0,
        inputs: [{"item": "Crude Oil", "qty": 60.0}],
        tier: 'D',
        byproduct: {"item": "Heavy Oil Residue", "qty": 20.0}
      },
    }
  },
  'Portable Miner': {
    alts: ["Basic", "Alt: Automated Miner"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.5,
        inputs: [{"item": "Iron Plate", "qty": 3.0}, {"item": "Iron Rod", "qty": 6.0}]
      },
      'Alt: Automated Miner': {
        building: 'Assembler',
        mw: 15.0,
        output: 1.0,
        inputs: [{"item": "Steel Pipe", "qty": 4.0}, {"item": "Iron Plate", "qty": 4.0}],
        tier: 'D'
      },
    }
  },
  'Power Shard': {
    alts: ["Basic", "Basic (Tier 1)", "Basic (Tier 2)", "Basic (Tier 3)"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 250.0,
        output: 5.0,
        inputs: [{"item": "Time Crystal", "qty": 10.0}, {"item": "Dark Matter Crystal", "qty": 10.0}, {"item": "Quartz Crystal", "qty": 60.0}, {"item": "Excited Photonic Matter", "qty": 60.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 60.0}
      },
      'Basic (Tier 1)': {
        building: 'Constructor',
        mw: 4.0,
        output: 7.5,
        inputs: [{"item": "Blue Power Slug", "qty": 7.5}]
      },
      'Basic (Tier 2)': {
        building: 'Constructor',
        mw: 4.0,
        output: 10.0,
        inputs: [{"item": "Yellow Power Slug", "qty": 5.0}]
      },
      'Basic (Tier 3)': {
        building: 'Constructor',
        mw: 4.0,
        output: 12.5,
        inputs: [{"item": "Purple Power Slug", "qty": 2.5}]
      },
    }
  },
  'Pressure Conversion Cube': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 1.0,
        inputs: [{"item": "Fused Modular Frame", "qty": 1.0}, {"item": "Radio Control Unit", "qty": 2.0}]
      },
    }
  },
  'Pulse Nobelisk': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Nobelisk", "qty": 5.0}, {"item": "Crystal Oscillator", "qty": 1.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 2.5,
        inputs: [{"item": "Nobelisk", "qty": 2.5}, {"item": "Crystal Oscillator", "qty": 0.5}]
      },
    }
  },
  'Quartz Crystal': {
    alts: ["Basic", "Alt: Fused Quartz Crystal", "Alt: Pure Quartz Crystal", "Alt: Quartz Purification"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 22.5,
        inputs: [{"item": "Raw Quartz", "qty": 37.5}]
      },
      'Alt: Fused Quartz Crystal': {
        building: 'Foundry',
        mw: 16.0,
        output: 54.0,
        inputs: [{"item": "Raw Quartz", "qty": 75.0}, {"item": "Coal", "qty": 36.0}],
        tier: 'D'
      },
      'Alt: Pure Quartz Crystal': {
        building: 'Refinery',
        mw: 30.0,
        output: 52.5,
        inputs: [{"item": "Raw Quartz", "qty": 67.5}, {"item": "Water", "qty": 37.5}],
        tier: 'B'
      },
      'Alt: Quartz Purification': {
        building: 'Refinery',
        mw: 30.0,
        output: 75.0,
        inputs: [{"item": "Raw Quartz", "qty": 120.0}, {"item": "Nitric Acid", "qty": 10.0}],
        tier: 'B',
        byproduct: {"item": "Dissolved Silica", "qty": 60.0}
      },
    }
  },
  'Quickwire': {
    alts: ["Basic", "Alt: Fused Quickwire"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Caterium Ingot", "qty": 12.0}]
      },
      'Alt: Fused Quickwire': {
        building: 'Assembler',
        mw: 15.0,
        output: 90.0,
        inputs: [{"item": "Caterium Ingot", "qty": 7.5}, {"item": "Copper Ingot", "qty": 37.5}],
        tier: 'D'
      },
    }
  },
  'Radio Control Unit': {
    alts: ["Basic", "Alt: Radio Connection Unit", "Alt: Radio Control System"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.5,
        inputs: [{"item": "Aluminum Casing", "qty": 40.0}, {"item": "Crystal Oscillator", "qty": 1.25}, {"item": "Computer", "qty": 2.5}]
      },
      'Alt: Radio Connection Unit': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Heat Sink", "qty": 15.0}, {"item": "High-Speed Connector", "qty": 7.5}, {"item": "Quartz Crystal", "qty": 45.0}],
        tier: 'B'
      },
      'Alt: Radio Control System': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 4.5,
        inputs: [{"item": "Crystal Oscillator", "qty": 1.5}, {"item": "Circuit Board", "qty": 15.0}, {"item": "Aluminum Casing", "qty": 90.0}, {"item": "Rubber", "qty": 45.0}],
        tier: 'A'
      },
    }
  },
  'Raw Quartz': {
    alts: ["Basic (Bauxite)", "Basic (Coal)"],
    recipes: {
      'Basic (Bauxite)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Bauxite", "qty": 100.0}]
      },
      'Basic (Coal)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Coal", "qty": 240.0}]
      },
    }
  },
  'Reanimated SAM': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "SAM", "qty": 120.0}]
      },
    }
  },
  'Rebar Gun': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 6.0}, {"item": "Iron Rod", "qty": 16.0}, {"item": "Screw", "qty": 100.0}]
      },
    }
  },
  'Reinforced Iron Plate': {
    alts: ["Basic", "Alt: Adhered Iron Plate", "Alt: Bolted Iron Plate", "Alt: Stitched Iron Plate"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Iron Plate", "qty": 30.0}, {"item": "Screw", "qty": 60.0}]
      },
      'Alt: Adhered Iron Plate': {
        building: 'Assembler',
        mw: 15.0,
        output: 3.75,
        inputs: [{"item": "Iron Plate", "qty": 11.25}, {"item": "Rubber", "qty": 3.75}],
        tier: 'C'
      },
      'Alt: Bolted Iron Plate': {
        building: 'Assembler',
        mw: 15.0,
        output: 15.0,
        inputs: [{"item": "Iron Plate", "qty": 90.0}, {"item": "Screw", "qty": 250.0}],
        tier: 'F'
      },
      'Alt: Stitched Iron Plate': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.625,
        inputs: [{"item": "Iron Plate", "qty": 18.75}, {"item": "Wire", "qty": 37.5}],
        tier: 'B'
      },
    }
  },
  'Rifle': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.5,
        inputs: [{"item": "Motor", "qty": 1.0}, {"item": "Rubber", "qty": 5.0}, {"item": "Steel Pipe", "qty": 12.5}, {"item": "Screw", "qty": 125.0}]
      },
    }
  },
  'Rifle Ammo': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 75.0,
        inputs: [{"item": "Copper Sheet", "qty": 15.0}, {"item": "Smokeless Powder", "qty": 10.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 37.5,
        inputs: [{"item": "Copper Sheet", "qty": 7.5}, {"item": "Smokeless Powder", "qty": 5.0}]
      },
    }
  },
  'Rocket Fuel': {
    alts: ["Basic", "Alt: Nitro Rocket Fuel"],
    recipes: {
      'Basic': {
        building: 'Blender',
        mw: 75.0,
        output: 100.0,
        inputs: [{"item": "Turbofuel", "qty": 60.0}, {"item": "Nitric Acid", "qty": 10.0}],
        byproduct: {"item": "Compacted Coal", "qty": 10.0}
      },
      'Alt: Nitro Rocket Fuel': {
        building: 'Blender',
        mw: 75.0,
        output: 150.0,
        inputs: [{"item": "Fuel", "qty": 100.0}, {"item": "Nitrogen Gas", "qty": 75.0}, {"item": "Sulfur", "qty": 100.0}, {"item": "Coal", "qty": 50.0}],
        tier: 'S',
        byproduct: {"item": "Compacted Coal", "qty": 25.0}
      },
    }
  },
  'Rotor': {
    alts: ["Basic", "Alt: Copper Rotor", "Alt: Steel Rotor"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 4.0,
        inputs: [{"item": "Iron Rod", "qty": 20.0}, {"item": "Screw", "qty": 100.0}]
      },
      'Alt: Copper Rotor': {
        building: 'Assembler',
        mw: 15.0,
        output: 11.25,
        inputs: [{"item": "Copper Sheet", "qty": 22.5}, {"item": "Screw", "qty": 195.0}],
        tier: 'D'
      },
      'Alt: Steel Rotor': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Steel Pipe", "qty": 10.0}, {"item": "Wire", "qty": 30.0}],
        tier: 'B'
      },
    }
  },
  'Rubber': {
    alts: ["Basic", "Alt: Recycled Rubber"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 20.0,
        inputs: [{"item": "Polymer Resin", "qty": 40.0}, {"item": "Water", "qty": 40.0}]
      },
      'Alt: Recycled Rubber': {
        building: 'Refinery',
        mw: 30.0,
        output: 60.0,
        inputs: [{"item": "Plastic", "qty": 30.0}, {"item": "Fuel", "qty": 30.0}],
        tier: 'A'
      },
    }
  },
  'SAM Fluctuator': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 10.0,
        inputs: [{"item": "Reanimated SAM", "qty": 60.0}, {"item": "Wire", "qty": 50.0}, {"item": "Steel Pipe", "qty": 30.0}]
      },
    }
  },
  'Screw': {
    alts: ["Basic", "Alt: Cast Screw", "Alt: Steel Screw"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 40.0,
        inputs: [{"item": "Iron Rod", "qty": 10.0}]
      },
      'Alt: Cast Screw': {
        building: 'Constructor',
        mw: 4.0,
        output: 50.0,
        inputs: [{"item": "Iron Ingot", "qty": 12.5}],
        tier: 'F'
      },
      'Alt: Steel Screw': {
        building: 'Constructor',
        mw: 4.0,
        output: 260.0,
        inputs: [{"item": "Steel Beam", "qty": 5.0}],
        tier: 'B'
      },
    }
  },
  'Shatter Rebar': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Iron Rebar", "qty": 10.0}, {"item": "Quartz Crystal", "qty": 15.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 5.0,
        inputs: [{"item": "Iron Rebar", "qty": 10.0}, {"item": "Quartz Crystal", "qty": 5.0}]
      },
    }
  },
  'Silica': {
    alts: ["Basic", "Alt: Cheap Silica", "Alt: Distilled Silica"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 37.5,
        inputs: [{"item": "Raw Quartz", "qty": 22.5}]
      },
      'Alt: Cheap Silica': {
        building: 'Assembler',
        mw: 15.0,
        output: 52.5,
        inputs: [{"item": "Raw Quartz", "qty": 22.5}, {"item": "Limestone", "qty": 37.5}],
        tier: 'B'
      },
      'Alt: Distilled Silica': {
        building: 'Blender',
        mw: 75.0,
        output: 270.0,
        inputs: [{"item": "Dissolved Silica", "qty": 120.0}, {"item": "Limestone", "qty": 50.0}, {"item": "Water", "qty": 100.0}],
        tier: 'B',
        byproduct: {"item": "Water", "qty": 80.0}
      },
    }
  },
  'Singularity Cell': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 10.0,
        inputs: [{"item": "Nuclear Pasta", "qty": 1.0}, {"item": "Dark Matter Crystal", "qty": 20.0}, {"item": "Iron Plate", "qty": 100.0}, {"item": "Concrete", "qty": 200.0}]
      },
    }
  },
  'Smart Plating': {
    alts: ["Basic", "Alt: Plastic Smart Plating"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 2.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 2.0}, {"item": "Rotor", "qty": 2.0}]
      },
      'Alt: Plastic Smart Plating': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 5.0,
        inputs: [{"item": "Reinforced Iron Plate", "qty": 2.5}, {"item": "Rotor", "qty": 2.5}, {"item": "Plastic", "qty": 7.5}],
        tier: 'A'
      },
    }
  },
  'Smokeless Powder': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 20.0,
        inputs: [{"item": "Black Powder", "qty": 20.0}, {"item": "Heavy Oil Residue", "qty": 10.0}]
      },
    }
  },
  'Solid Biofuel': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 60.0,
        inputs: [{"item": "Biomass", "qty": 120.0}]
      },
    }
  },
  'Stator': {
    alts: ["Basic", "Alt: Quickwire Stator"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Steel Pipe", "qty": 15.0}, {"item": "Wire", "qty": 40.0}]
      },
      'Alt: Quickwire Stator': {
        building: 'Assembler',
        mw: 15.0,
        output: 8.0,
        inputs: [{"item": "Steel Pipe", "qty": 16.0}, {"item": "Quickwire", "qty": 60.0}],
        tier: 'F'
      },
    }
  },
  'Steel Beam': {
    alts: ["Basic", "Alt: Aluminum Beam", "Alt: Molded Beam"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 15.0,
        inputs: [{"item": "Steel Ingot", "qty": 60.0}]
      },
      'Alt: Aluminum Beam': {
        building: 'Constructor',
        mw: 4.0,
        output: 22.5,
        inputs: [{"item": "Aluminum Ingot", "qty": 22.5}],
        tier: 'B'
      },
      'Alt: Molded Beam': {
        building: 'Foundry',
        mw: 16.0,
        output: 45.0,
        inputs: [{"item": "Steel Ingot", "qty": 120.0}, {"item": "Concrete", "qty": 80.0}],
        tier: 'D'
      },
    }
  },
  'Steel Ingot': {
    alts: ["Basic", "Alt: Coke Steel Ingot", "Alt: Compacted Steel Ingot", "Alt: Solid Steel Ingot"],
    recipes: {
      'Basic': {
        building: 'Foundry',
        mw: 16.0,
        output: 45.0,
        inputs: [{"item": "Iron Ore", "qty": 45.0}, {"item": "Coal", "qty": 45.0}]
      },
      'Alt: Coke Steel Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 100.0,
        inputs: [{"item": "Iron Ore", "qty": 75.0}, {"item": "Petroleum Coke", "qty": 75.0}],
        tier: 'C'
      },
      'Alt: Compacted Steel Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 10.0,
        inputs: [{"item": "Iron Ore", "qty": 5.0}, {"item": "Compacted Coal", "qty": 2.5}],
        tier: 'B'
      },
      'Alt: Solid Steel Ingot': {
        building: 'Foundry',
        mw: 16.0,
        output: 60.0,
        inputs: [{"item": "Iron Ingot", "qty": 40.0}, {"item": "Coal", "qty": 40.0}],
        tier: 'S'
      },
    }
  },
  'Steel Pipe': {
    alts: ["Basic", "Alt: Iron Pipe", "Alt: Molded Steel Pipe"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 20.0,
        inputs: [{"item": "Steel Ingot", "qty": 30.0}]
      },
      'Alt: Iron Pipe': {
        building: 'Constructor',
        mw: 4.0,
        output: 25.0,
        inputs: [{"item": "Iron Ingot", "qty": 100.0}],
        tier: 'C'
      },
      'Alt: Molded Steel Pipe': {
        building: 'Foundry',
        mw: 16.0,
        output: 50.0,
        inputs: [{"item": "Steel Ingot", "qty": 50.0}, {"item": "Concrete", "qty": 30.0}],
        tier: 'S'
      },
    }
  },
  'Stun Rebar': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 10.0,
        inputs: [{"item": "Iron Rebar", "qty": 10.0}, {"item": "Quickwire", "qty": 50.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 10.0,
        inputs: [{"item": "Iron Rebar", "qty": 10.0}, {"item": "Quickwire", "qty": 15.0}]
      },
    }
  },
  'Sulfur': {
    alts: ["Basic (Coal)", "Basic (Iron)"],
    recipes: {
      'Basic (Coal)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Coal", "qty": 200.0}]
      },
      'Basic (Iron)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Iron Ore", "qty": 300.0}]
      },
    }
  },
  'Sulfuric Acid': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 60.0,
        inputs: [{"item": "Packaged Sulfuric Acid", "qty": 60.0}],
        byproduct: {"item": "Empty Canister", "qty": 60.0}
      },
    }
  },
  'Supercomputer': {
    alts: ["Basic", "Alt: OC Supercomputer", "Alt: Super-State Computer"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.875,
        inputs: [{"item": "Computer", "qty": 7.5}, {"item": "AI Limiter", "qty": 3.75}, {"item": "High-Speed Connector", "qty": 5.625}, {"item": "Plastic", "qty": 52.5}]
      },
      'Alt: OC Supercomputer': {
        building: 'Assembler',
        mw: 15.0,
        output: 3.0,
        inputs: [{"item": "Radio Control Unit", "qty": 6.0}, {"item": "Cooling System", "qty": 6.0}],
        tier: 'A'
      },
      'Alt: Super-State Computer': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.4,
        inputs: [{"item": "Computer", "qty": 7.2}, {"item": "EM Control Rod", "qty": 2.4}, {"item": "Battery", "qty": 24.0}, {"item": "Wire", "qty": 60.0}],
        tier: 'D'
      },
    }
  },
  'Superposition Oscillator': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Quantum Encoder',
        mw: 500.0,
        output: 5.0,
        inputs: [{"item": "Dark Matter Crystal", "qty": 30.0}, {"item": "Crystal Oscillator", "qty": 5.0}, {"item": "Alclad Aluminum Sheet", "qty": 45.0}, {"item": "Excited Photonic Matter", "qty": 125.0}],
        byproduct: {"item": "Dark Matter Residue", "qty": 125.0}
      },
    }
  },
  'Thermal Propulsion Rocket': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.0,
        inputs: [{"item": "Cooling System", "qty": 3.0}, {"item": "Fused Modular Frame", "qty": 1.0}, {"item": "Modular Engine", "qty": 2.5}, {"item": "Turbo Motor", "qty": 1.0}]
      },
    }
  },
  'Time Crystal': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Converter',
        mw: 250.0,
        output: 6.0,
        inputs: [{"item": "Diamonds", "qty": 12.0}]
      },
    }
  },
  'Turbo Motor': {
    alts: ["Basic", "Alt: Turbo Electric Motor", "Alt: Turbo Pressure Motor"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 1.875,
        inputs: [{"item": "Cooling System", "qty": 7.5}, {"item": "Radio Control Unit", "qty": 3.75}, {"item": "Motor", "qty": 7.5}, {"item": "Rubber", "qty": 45.0}]
      },
      'Alt: Turbo Electric Motor': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 2.8125,
        inputs: [{"item": "Motor", "qty": 6.5625}, {"item": "Radio Control Unit", "qty": 8.4375}, {"item": "EM Control Rod", "qty": 4.6875}, {"item": "Rotor", "qty": 6.5625}],
        tier: 'D'
      },
      'Alt: Turbo Pressure Motor': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 3.75,
        inputs: [{"item": "Motor", "qty": 7.5}, {"item": "Pressure Conversion Cube", "qty": 1.875}, {"item": "Packaged Nitrogen Gas", "qty": 45.0}, {"item": "Stator", "qty": 15.0}],
        tier: 'A'
      },
    }
  },
  'Turbo Rifle Ammo': {
    alts: ["Basic", "Basic (EW)"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 250.0,
        inputs: [{"item": "Rifle Ammo", "qty": 125.0}, {"item": "Aluminum Casing", "qty": 15.0}, {"item": "Packaged Turbofuel", "qty": 15.0}]
      },
      'Basic (EW)': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 125.0,
        inputs: [{"item": "Rifle Ammo", "qty": 62.5}, {"item": "Aluminum Casing", "qty": 7.5}, {"item": "Packaged Turbofuel", "qty": 7.5}]
      },
    }
  },
  'Turbofuel': {
    alts: ["Basic", "Basic (Unpackage)", "Alt: Turbo Blend Fuel", "Alt: Turbo Heavy Fuel"],
    recipes: {
      'Basic': {
        building: 'Refinery',
        mw: 30.0,
        output: 18.75,
        inputs: [{"item": "Fuel", "qty": 22.5}, {"item": "Compacted Coal", "qty": 15.0}],
        tier: 'S'
      },
      'Basic (Unpackage)': {
        building: 'Packager',
        mw: 10.0,
        output: 20.0,
        inputs: [{"item": "Packaged Turbofuel", "qty": 20.0}],
        byproduct: {"item": "Empty Canister", "qty": 20.0}
      },
      'Alt: Turbo Blend Fuel': {
        building: 'Blender',
        mw: 75.0,
        output: 45.0,
        inputs: [{"item": "Fuel", "qty": 15.0}, {"item": "Heavy Oil Residue", "qty": 30.0}, {"item": "Sulfur", "qty": 22.5}, {"item": "Petroleum Coke", "qty": 22.5}],
        tier: 'D'
      },
      'Alt: Turbo Heavy Fuel': {
        building: 'Refinery',
        mw: 30.0,
        output: 30.0,
        inputs: [{"item": "Heavy Oil Residue", "qty": 37.5}, {"item": "Compacted Coal", "qty": 30.0}],
        tier: 'F'
      },
    }
  },
  'Uranium': {
    alts: ["Basic (Bauxite)"],
    recipes: {
      'Basic (Bauxite)': {
        building: 'Converter',
        mw: 250.0,
        output: 120.0,
        inputs: [{"item": "Reanimated SAM", "qty": 10.0}, {"item": "Bauxite", "qty": 480.0}]
      },
    }
  },
  'Uranium Fuel Rod': {
    alts: ["Basic", "Alt: Uranium Fuel Unit"],
    recipes: {
      'Basic': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 0.4,
        inputs: [{"item": "Encased Uranium Cell", "qty": 20.0}, {"item": "Encased Industrial Beam", "qty": 1.2}, {"item": "EM Control Rod", "qty": 2.0}]
      },
      'Alt: Uranium Fuel Unit': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 0.6,
        inputs: [{"item": "Encased Uranium Cell", "qty": 20.0}, {"item": "EM Control Rod", "qty": 2.0}, {"item": "Crystal Oscillator", "qty": 0.6}, {"item": "Rotor", "qty": 2.0}],
        tier: 'B'
      },
    }
  },
  'Uranium Waste': {
    alts: ["Basic (burning)"],
    recipes: {
      'Basic (burning)': {
        building: 'Nuclear Power Plant',
        mw: 0.0,
        output: 10.0,
        inputs: [{"item": "Uranium Fuel Rod", "qty": 0.2}, {"item": "Water", "qty": 240.0}]
      },
    }
  },
  'Versatile Framework': {
    alts: ["Basic", "Alt: Flexible Framework"],
    recipes: {
      'Basic': {
        building: 'Assembler',
        mw: 15.0,
        output: 5.0,
        inputs: [{"item": "Modular Frame", "qty": 2.5}, {"item": "Steel Beam", "qty": 30.0}]
      },
      'Alt: Flexible Framework': {
        building: 'Manufacturer',
        mw: 55.0,
        output: 7.5,
        inputs: [{"item": "Modular Frame", "qty": 3.75}, {"item": "Steel Beam", "qty": 22.5}, {"item": "Rubber", "qty": 30.0}],
        tier: 'A'
      },
    }
  },
  'Water': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Packager',
        mw: 10.0,
        output: 120.0,
        inputs: [{"item": "Packaged Water", "qty": 120.0}],
        byproduct: {"item": "Empty Canister", "qty": 120.0}
      },
    }
  },
  'Wire': {
    alts: ["Basic", "Alt: Caterium Wire", "Alt: Fused Wire", "Alt: Iron Wire"],
    recipes: {
      'Basic': {
        building: 'Constructor',
        mw: 4.0,
        output: 30.0,
        inputs: [{"item": "Copper Ingot", "qty": 15.0}]
      },
      'Alt: Caterium Wire': {
        building: 'Constructor',
        mw: 4.0,
        output: 120.0,
        inputs: [{"item": "Caterium Ingot", "qty": 15.0}],
        tier: 'S'
      },
      'Alt: Fused Wire': {
        building: 'Assembler',
        mw: 15.0,
        output: 90.0,
        inputs: [{"item": "Copper Ingot", "qty": 12.0}, {"item": "Caterium Ingot", "qty": 3.0}],
        tier: 'D'
      },
      'Alt: Iron Wire': {
        building: 'Constructor',
        mw: 4.0,
        output: 22.5,
        inputs: [{"item": "Iron Ingot", "qty": 12.5}],
        tier: 'C'
      },
    }
  },
  'Xeno-Basher': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 0.75,
        inputs: [{"item": "Xeno-Zapper", "qty": 1.5}, {"item": "Modular Frame", "qty": 3.75}, {"item": "Iron Rod", "qty": 18.75}, {"item": "Wire", "qty": 375.0}]
      },
    }
  },
  'Xeno-Zapper': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.5,
        inputs: [{"item": "Iron Rod", "qty": 15.0}, {"item": "Reinforced Iron Plate", "qty": 3.0}, {"item": "Cable", "qty": 22.5}, {"item": "Wire", "qty": 75.0}]
      },
    }
  },
  'Zipline': {
    alts: ["Basic"],
    recipes: {
      'Basic': {
        building: 'Equipment Workshop',
        mw: 0.0,
        output: 1.5,
        inputs: [{"item": "Xeno-Zapper", "qty": 1.5}, {"item": "Quickwire", "qty": 45.0}, {"item": "Iron Rod", "qty": 4.5}, {"item": "Cable", "qty": 15.0}]
      },
    }
  },
};

const ITEM_LIST = Object.keys(RECIPES).sort();
