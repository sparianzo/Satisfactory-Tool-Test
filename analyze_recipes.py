#!/usr/bin/env python3
"""Analyze missing recipes: EW/Craft Bench variants vs automated, and completely missing items."""

import re
import json

# ── 1. Parse TSV ──────────────────────────────────────────────────────────────
tsv_data = """CLASS	RECIPE_NAME	BUILDING	MW	IN_1	Q_1	IN_2	Q_2	IN_3	Q_3	IN_4	Q_4	OUT_1	Q_OUT	OUT_2	Q_OUT2	SINK_PTS
Basic	Iron Ingot	Smelter	4	Iron Ore	30							Iron Ingot	30			1000
Basic	Copper Ingot	Smelter	4	Copper Ore	30							Copper Ingot	30			1000
Basic	Caterium Ingot	Smelter	4	Caterium Ore	45							Caterium Ingot	15			1000
Basic	Iron Plate	Constructor	4	Iron Ingot	30							Iron Plate	20			1000
Basic	Iron Rod	Constructor	4	Iron Ingot	15							Iron Rod	15			1000
Basic	Screw	Constructor	4	Iron Rod	10							Screw	40			1000
Basic	Wire	Constructor	4	Copper Ingot	15							Wire	30			1000
Basic	Cable	Constructor	4	Wire	60							Cable	30			1000
Basic	Concrete	Constructor	4	Limestone	45							Concrete	15			1000
Basic	Quartz Crystal	Constructor	4	Raw Quartz	37.5							Quartz Crystal	22.5			1000
Basic	Silica	Constructor	4	Raw Quartz	22.5							Silica	37.5			1000
Basic	Copper Sheet	Constructor	4	Copper Ingot	20							Copper Sheet	10			1000
Basic	Steel Pipe	Constructor	4	Steel Ingot	30							Steel Pipe	20			1000
Basic	Steel Beam	Constructor	4	Steel Ingot	60							Steel Beam	15			1000
Basic	Quickwire	Constructor	4	Caterium Ingot	12							Quickwire	60			1000
Basic	Biomass (Leaves)	Constructor	4	Leaves	120							Biomass	60			1000
Basic	Biomass (Wood)	Constructor	4	Wood	60							Biomass	300			1000
Basic	Biomass (Mycelia)	Constructor	4	Mycelia	15							Biomass	150			1000
Basic	Biomass (Alien Protein)	Constructor	4	Alien Protein	15							Biomass	1500			1000
Basic	Solid Biofuel	Constructor	4	Biomass	120							Solid Biofuel	60			1000
Basic	Color Cartridge	Constructor	4	Flower Petals	50							Color Cartridge	100			1000
Basic	Iron Rebar	Constructor	4	Iron Rod	15							Iron Rebar	15			1000
Basic	Aluminum Casing	Constructor	4	Aluminum Ingot	90							Aluminum Casing	60			1000
Basic	Ficsite Trigon	Constructor	4	Ficsite Ingot	10							Ficsite Trigon	30			1000
Basic	Reanimated SAM	Constructor	4	SAM	120							Reanimated SAM	60			1000
Basic	Steel Ingot	Foundry	16	Iron Ore	45	Coal	45					Steel Ingot	45			1000
Basic	Aluminum Ingot	Foundry	16	Aluminum Scrap	90	Silica	75					Aluminum Ingot	60			1000
Basic	Reinforced Iron Plate	Assembler	15	Iron Plate	30	Screw	60					Reinforced Iron Plate	5			1000
Basic	Rotor	Assembler	15	Iron Rod	20	Screw	100					Rotor	4			1000
Basic	Modular Frame	Assembler	15	Reinforced Iron Plate	3	Iron Rod	12					Modular Frame	2			1000
Basic	Encased Industrial Beam	Assembler	15	Steel Beam	24	Concrete	30					Encased Industrial Beam	6			1000
Basic	Stator	Assembler	15	Steel Pipe	15	Wire	40					Stator	5			1000
Basic	Motor	Assembler	15	Rotor	10	Stator	10					Motor	5			1000
Basic	Automated Wiring	Assembler	15	Stator	2.5	Cable	50					Automated Wiring	2.5			1000
Basic	AI Limiter	Assembler	15	Copper Sheet	25	Quickwire	100					AI Limiter	5			1000
Basic	Circuit Board	Assembler	15	Copper Sheet	15	Plastic	30					Circuit Board	7.5			1000
Basic	Alclad Aluminum Sheet	Assembler	15	Aluminum Ingot	30	Copper Ingot	10					Alclad Aluminum Sheet	30			1000
Basic	Heat Sink	Assembler	15	Alclad Aluminum Sheet	37.5	Copper Ingot	22.5					Heat Sink	7.5			1000
Basic	EM Control Rod	Assembler	15	Stator	6	AI Limiter	4					EM Control Rod	4			1000
Basic	Rifle Ammo	Assembler	15	Copper Sheet	15	Smokeless Powder	10					Rifle Ammo	75			1000
Basic	Homing Rifle Ammo	Assembler	15	Rifle Ammo	50	High-Speed Connector	2.5					Homing Rifle Ammo	25			1000
Basic	Cluster Nobelisk	Assembler	15	Nobelisk	7.5	Smokeless Powder	10					Cluster Nobelisk	2.5			1000
Basic	Versatile Framework	Assembler	15	Modular Frame	2.5	Steel Beam	30					Versatile Framework	5			1000
Basic	Adaptive Control Unit	Assembler	15	Automated Wiring	7.5	Circuit Board	5					Adaptive Control Unit	1			1000
Basic	Heavy Modular Frame	Manufacturer	55	Modular Frame	10	Steel Pipe	30	Encased Industrial Beam	10	Screw	200	Heavy Modular Frame	2			1000
Basic	Computer	Manufacturer	55	Circuit Board	25	Cable	22.5	Plastic	45	Screw	130	Computer	2.5			1000
Basic	High-Speed Connector	Manufacturer	55	Quickwire	210	Cable	37.5	Circuit Board	3.75			High-Speed Connector	3.75			1000
Basic	Crystal Oscillator	Manufacturer	55	Quartz Crystal	36	Cable	28	Reinforced Iron Plate	5			Crystal Oscillator	2			1000
Basic	Supercomputer	Manufacturer	55	Computer	3.75	AI Limiter	3.75	High-Speed Connector	5.625	Plastic	52.5	Supercomputer	1.875			1000
Basic	Radio Control Unit	Manufacturer	55	Aluminum Casing	40	Crystal Oscillator	1.25	Computer	2.5			Radio Control Unit	2.5			1000
Basic	Turbo Motor	Manufacturer	55	Cooling System	7.5	Radio Control Unit	3.75	Motor	7.5	Rubber	45	Turbo Motor	1.875			1000
Basic	Magnetic Field Generator	Manufacturer	55	Versatile Framework	2.5	EM Control Rod	1	Battery	10			Magnetic Field Generator	1			1000
Basic	Assembly Director System	Manufacturer	55	Adaptive Control Unit	1.5	Supercomputer	0.75					Assembly Director System	0.75			1000
Basic	Thermal Propulsion Rocket	Manufacturer	55	Modular Engine	2.5	Adaptive Control Unit	1	Turbo Motor	1	Pressure Conversion Cube	1	Thermal Propulsion Rocket	1			1000
Basic	Modular Engine	Manufacturer	55	Motor	2	Rubber	15	Smart Plating	2			Modular Engine	1			1000
Basic	Adaptive Control Unit (Mfr)	Manufacturer	55	Automated Wiring	7.5	Circuit Board	5	Heavy Modular Frame	1	Computer	1	Adaptive Control Unit	1			1000
Basic	Plastic	Refinery	30	Crude Oil	30							Plastic	20	Heavy Oil Residue	10	1000
Basic	Rubber	Refinery	30	Crude Oil	30							Rubber	20	Heavy Oil Residue	20	1000
Basic	Fuel	Refinery	30	Crude Oil	60							Fuel	40	Polymer Resin	30	1000
Basic	Heavy Oil Residue	Refinery	30	Crude Oil	30							Heavy Oil Residue	40	Polymer Resin	20	1000
Basic	Polymer Resin	Refinery	30	Crude Oil	60							Polymer Resin	130	Heavy Oil Residue	20	1000
Basic	Petroleum Coke	Refinery	30	Heavy Oil Residue	40							Petroleum Coke	120			1000
Basic	Residual Rubber	Refinery	30	Polymer Resin	40	Water	40					Rubber	20			1000
Basic	Residual Plastic	Refinery	30	Polymer Resin	60	Water	70					Plastic	20			1000
Basic	Residual Fuel	Refinery	30	Heavy Oil Residue	60							Fuel	40			1000
Basic	Alumina Solution	Refinery	30	Bauxite	120	Water	180					Alumina Solution	120	Silica	50	1000
Basic	Aluminum Scrap	Refinery	30	Alumina Solution	240	Coal	120					Aluminum Scrap	360	Water	120	1000
Basic	Sulfuric Acid	Refinery	30	Sulfur	50	Water	50					Sulfuric Acid	50			1000
Basic	Nitric Acid	Refinery	30	Nitrogen Gas	120	Water	30	Iron Plate	10			Nitric Acid	30			1000
Basic	Smokeless Powder	Refinery	30	Black Powder	20	Heavy Oil Residue	10					Smokeless Powder	20			1000
Basic	Ionized Fuel	Refinery	30	Rocket Fuel	40	Power Shard	2.5					Ionized Fuel	40	Compacted Coal	5	1000
Basic	Turbofuel	Refinery	30	Fuel	22.5	Compacted Coal	15					Turbofuel	18.75			1000
Basic	Liquid Biofuel	Refinery	30	Solid Biofuel	90	Water	45					Liquid Biofuel	60			1000
Basic	Diluted Packaged Fuel	Refinery	30	Heavy Oil Residue	30	Packaged Water	60					Packaged Diluted Fuel	60			1000
Basic	Packaged Water	Packager	10	Water	60	Empty Canister	60					Packaged Water	60			1000
Basic	Packaged Oil	Packager	10	Crude Oil	30	Empty Canister	30					Packaged Oil	30			1000
Basic	Packaged Fuel	Packager	10	Fuel	40	Empty Canister	40					Packaged Fuel	40			1000
Basic	Packaged Heavy Oil Residue	Packager	10	Heavy Oil Residue	30	Empty Canister	30					Packaged Heavy Oil Residue	30			1000
Basic	Packaged Sulfuric Acid	Packager	10	Sulfuric Acid	40	Empty Canister	40					Packaged Sulfuric Acid	40			1000
Basic	Packaged Alumina Solution	Packager	10	Alumina Solution	60	Empty Canister	60					Packaged Alumina Solution	60			1000
Basic	Packaged Nitrogen Gas	Packager	10	Nitrogen Gas	60	Empty Canister	60					Packaged Nitrogen Gas	60			1000
Basic	Packaged Turbofuel	Packager	10	Turbofuel	20	Empty Canister	20					Packaged Turbofuel	20			1000
Basic	Packaged Liquid Biofuel	Packager	10	Liquid Biofuel	40	Empty Canister	40					Packaged Liquid Biofuel	40			1000
Basic	Packaged Nitric Acid	Packager	10	Nitric Acid	30	Empty Canister	30					Packaged Nitric Acid	30			1000
Basic	Packaged Rocket Fuel	Packager	10	Rocket Fuel	60	Empty Canister	60					Packaged Rocket Fuel	60			1000
Basic	Packaged Ionized Fuel	Packager	10	Ionized Fuel	40	Empty Canister	40					Packaged Ionized Fuel	40			1000
Basic	Unpackage Water	Packager	10	Packaged Water	120							Water	120	Empty Canister	120	1000
Basic	Unpackage Oil	Packager	10	Packaged Oil	60							Crude Oil	60	Empty Canister	60	1000
Basic	Unpackage Fuel	Packager	10	Packaged Fuel	60							Fuel	60	Empty Canister	60	1000
Basic	Unpackage Heavy Oil Residue	Packager	10	Packaged Heavy Oil Residue	40							Heavy Oil Residue	40	Empty Canister	40	1000
Basic	Unpackage Sulfuric Acid	Packager	10	Packaged Sulfuric Acid	60							Sulfuric Acid	60	Empty Canister	60	1000
Basic	Unpackage Alumina Solution	Packager	10	Packaged Alumina Solution	120							Alumina Solution	120	Empty Canister	120	1000
Basic	Unpackage Nitrogen Gas	Packager	10	Packaged Nitrogen Gas	120							Nitrogen Gas	120	Empty Canister	120	1000
Basic	Unpackage Turbofuel	Packager	10	Packaged Turbofuel	20							Turbofuel	20	Empty Canister	20	1000
Basic	Unpackage Liquid Biofuel	Packager	10	Packaged Liquid Biofuel	60							Liquid Biofuel	60	Empty Canister	60	1000
Basic	Unpackage Nitric Acid	Packager	10	Packaged Nitric Acid	20							Nitric Acid	20	Empty Canister	20	1000
Basic	Unpackage Rocket Fuel	Packager	10	Packaged Rocket Fuel	60							Rocket Fuel	60	Empty Canister	60	1000
Basic	Unpackage Ionized Fuel	Packager	10	Packaged Ionized Fuel	40							Ionized Fuel	40	Empty Canister	40	1000
Basic	Cooling System	Blender	75	Heat Sink	12	Rubber	12	Water	30	Nitrogen Gas	150	Cooling System	6			1000
Basic	Fused Modular Frame	Blender	75	Heavy Modular Frame	1.5	Aluminum Casing	75	Nitrogen Gas	37.5			Fused Modular Frame	1.5			1000
Basic	Battery	Blender	75	Sulfuric Acid	40	Alumina Solution	40	Aluminum Casing	20			Battery	20	Water	30	1000
Basic	Rocket Fuel	Blender	75	Turbofuel	60	Nitric Acid	10					Rocket Fuel	100	Compacted Coal	10	1000
Basic	Nitro Rocket Fuel	Blender	75	Fuel	100	Nitrogen Gas	75	Sulfur	100	Coal	50	Rocket Fuel	100	Compacted Coal	25	1000
Basic	Non-Fissile Uranium	Blender	75	Uranium Waste	37.5	Silica	25	Nitric Acid	15	Sulfuric Acid	15	Non-Fissile Uranium	50	Water	15	1000
Basic	Encased Uranium Cell	Blender	75	Uranium	50	Concrete	15	Sulfuric Acid	40			Encased Uranium Cell	25	Sulfuric Acid	10	1000
Basic	Pressure Conversion Cube	Blender	75	Fused Modular Frame	1	Radio Control Unit	2					Pressure Conversion Cube	1			1000
Basic	Nuclear Pasta	Particle Accelerator	500	Copper Powder	100	Pressure Conversion Cube	0.5					Nuclear Pasta	0.5			1000
Basic	Plutonium Pellet	Particle Accelerator	500	Non-Fissile Uranium	100	Uranium Waste	25					Plutonium Pellet	30			1000
Basic	Ficsonium	Particle Accelerator	1000	Plutonium Waste	10	Singularity Cell	10	Dark Matter Residue	200			Ficsonium	10			1000
Basic	Uranium Fuel Rod	Assembler	15	Encased Uranium Cell	50	Encased Industrial Beam	3					Uranium Fuel Rod	0.4			1000
Basic	Plutonium Fuel Rod	Assembler	15	Encased Plutonium Cell	10	Steel Beam	10	EM Control Rod	1.25	Heat Sink	1.25	Plutonium Fuel Rod	0.5			1000
Basic	Encased Plutonium Cell	Blender	75	Plutonium Pellet	10	Concrete	20	Sulfuric Acid	30			Encased Plutonium Cell	5			1000
Basic	Ficsonium Fuel Rod	Quantum Encoder	1000	Ficsonium	5	EM Control Rod	5	Ficsite Trigon	100	Excited Photonic Matter	50	Ficsonium Fuel Rod	2.5	Dark Matter Residue	50	1000
Quantum	Time Crystal	Converter	250	Diamonds	30							Time Crystal	15			1000
Quantum	Diamonds	Converter	250	Coal	600							Diamonds	30			1000
Quantum	Ficsite Ingot (Iron)	Converter	250	Reanimated SAM	40	Iron Ingot	240					Ficsite Ingot	10			1000
Quantum	Ficsite Ingot (Caterium)	Converter	250	Reanimated SAM	45	Caterium Ingot	60					Ficsite Ingot	15			1000
Quantum	Ficsite Ingot (Aluminum)	Converter	250	Reanimated SAM	60	Aluminum Ingot	120					Ficsite Ingot	30			1000
Quantum	Dark Matter Crystal	Particle Accelerator	1000	Diamonds	30	Dark Matter Residue	150					Dark Matter Crystal	30			1000
Quantum	Excited Photonic Matter	Converter	250									Excited Photonic Matter	200			1000
Quantum	Dark Matter Residue	Converter	250	Reanimated SAM	50							Dark Matter Residue	100			1000
Quantum	Neural-Quantum Processor	Quantum Encoder	500	Time Crystal	15	Superposition Oscillator	3	Ficsite Trigon	45	Excited Photonic Matter	75	Neural-Quantum Processor	3	Dark Matter Residue	75	1000
Quantum	Superposition Oscillator	Quantum Encoder	500	Dark Matter Crystal	30	Crystal Oscillator	5	Alclad Aluminum Sheet	45	Excited Photonic Matter	125	Superposition Oscillator	5	Dark Matter Residue	125	1000
Quantum	AI Expansion Server	Quantum Encoder	500	Neural-Quantum Processor	4	Superposition Oscillator	4	Excited Photonic Matter	100			AI Expansion Server	4	Dark Matter Residue	100	1000
Quantum	Biochemical Sculptor	Quantum Encoder	500	Assembly Director System	2	Ficsite Trigon	160	Water	40			Biochemical Sculptor	8	Dark Matter Residue	100	1000
Quantum	Ballistic Warp Drive	Quantum Encoder	500	Thermal Propulsion Rocket	1	Singularity Cell	5	Neural-Quantum Processor	2	Excited Photonic Matter	40	Ballistic Warp Drive	1	Dark Matter Residue	40	1000
Quantum	Singularity Cell	Quantum Encoder	500	Nuclear Pasta	1	Dark Matter Crystal	20	Iron Plate	100	Concrete	200	Singularity Cell	10			1000
Basic	Black Powder	Equipment Workshop	0	Coal	7.5	Sulfur	5					Black Powder	15			1000
Basic	Nobelisk	Equipment Workshop	0	Black Powder	7.5	Steel Pipe	10					Nobelisk	3			1000
Basic	Gas Nobelisk	Equipment Workshop	0	Nobelisk	5	Biomass	50					Gas Nobelisk	5			1000
Basic	Pulse Nobelisk	Equipment Workshop	0	Nobelisk	5	Crystal Oscillator	1					Pulse Nobelisk	5			1000
Basic	Nuke Nobelisk	Equipment Workshop	0	Nobelisk	2.5	Encased Uranium Cell	10	Black Powder	2.5	Sulfur	2.5	Nuke Nobelisk	0.5			1000
Basic	Shatter Rebar	Equipment Workshop	0	Iron Rebar	10	Quartz Crystal	5					Shatter Rebar	5			1000
Basic	Stun Rebar	Equipment Workshop	0	Iron Rebar	10	Quickwire	15					Stun Rebar	10			1000
Basic	Explosive Rebar	Equipment Workshop	0	Iron Rebar	10	Smokeless Powder	10	Steel Pipe	10			Explosive Rebar	5			1000
Basic	Black Powder	Assembler	15	Coal	15	Sulfur	15					Black Powder	30		14
Basic	Nobelisk	Assembler	15	Black Powder	20	Steel Pipe	20					Nobelisk	10		152
Basic	Gas Nobelisk	Assembler	15	Nobelisk	5	Biomass	50					Gas Nobelisk	5		544
Basic	Pulse Nobelisk	Assembler	15	Nobelisk	5	Crystal Oscillator	1					Pulse Nobelisk	5		1533
Basic	Nuke Nobelisk	Manufacturer	55	Nobelisk	2.5	Encased Uranium Cell	10	Smokeless Powder	5	AI Limiter	3	Nuke Nobelisk	0.5			19600
Basic	Explosive Rebar	Manufacturer	55	Iron Rebar	10	Smokeless Powder	10	Steel Pipe	10			Explosive Rebar	5		360
Basic	Shatter Rebar	Assembler	15	Iron Rebar	10	Quartz Crystal	15					Shatter Rebar	5		332
Basic	Stun Rebar	Assembler	15	Iron Rebar	10	Quickwire	50					Stun Rebar	10		186
Basic	Turbo Rifle Ammo	Equipment Workshop	0	Rifle Ammo	25	Aluminum Casing	15	Turbofuel	15			Turbo Rifle Ammo	50			1000
Basic	Xeno-Zapper	Equipment Workshop	0	Iron Rod	40	Reinforced Iron Plate	2	Cable	20	Wire	30	Xeno-Zapper	1			1000
Basic	Gas Mask	Equipment Workshop	0	Fabric	50	Copper Sheet	10	Steel Pipe	10			Gas Mask	1		14960
Basic	Nobelisk Detonator	Equipment Workshop	0	Object Scanner	0.75	Steel Beam	7.5	Cable	37.5			Nobelisk Detonator	0.75		6480
Basic	Rebar Gun	Equipment Workshop	0	Reinforced Iron Plate	6	Iron Rod	16	Screw	100			Rebar Gun	1		1968
Basic	Factory Cart	Equipment Workshop	0	Reinforced Iron Plate	12	Iron Rod	12	Rotor	6			Factory Cart	3		1552
Basic	Golden Factory Cart	Equipment Workshop	0	Caterium Ingot	45	Iron Rod	12	Rotor	6			Golden Factory Cart	3		1852
Alternate	Pure Iron Ingot	Refinery	30	Iron Ore	35	Water	20					Iron Ingot	65			1000
Alternate	Iron Alloy Ingot	Foundry	16	Iron Ore	40	Copper Ore	10					Iron Ingot	75			1000
Alternate	Pure Copper Ingot	Refinery	30	Copper Ore	15	Water	10					Copper Ingot	37.5			1000
Alternate	Copper Alloy Ingot	Foundry	16	Copper Ore	50	Iron Ore	25					Copper Ingot	100			1000
Alternate	Pure Caterium Ingot	Refinery	30	Caterium Ore	24	Water	24					Caterium Ingot	12			1000
Alternate	Solid Steel Ingot	Foundry	16	Iron Ingot	40	Coal	40					Steel Ingot	60			1000
Alternate	Compacted Steel Ingot	Foundry	16	Iron Ore	22.5	Compacted Coal	11.25					Steel Ingot	37.5			1000
Alternate	Coke Steel Ingot	Foundry	16	Iron Ore	75	Petroleum Coke	75					Steel Ingot	100			1000
Alternate	Pure Aluminum Ingot	Smelter	4	Aluminum Scrap	60							Aluminum Ingot	30			1000
Alternate	Sloppy Alumina	Refinery	30	Bauxite	200	Water	200					Alumina Solution	240			1000
Alternate	Electrode Aluminum Scrap	Refinery	30	Alumina Solution	180	Petroleum Coke	60					Aluminum Scrap	300	Water	105	1000
Alternate	Instant Scrap	Blender	75	Bauxite	150	Coal	100	Sulfuric Acid	50	Water	60	Aluminum Scrap	300	Water	50	1000
Alternate	Classic Battery	Manufacturer	55	Sulfur	45	Alclad Aluminum Sheet	52.5	Plastic	60	Wire	90	Battery	30			1000
Alternate	Wet Concrete	Refinery	30	Limestone	120	Water	100					Concrete	80			1000
Alternate	Cast Screw	Constructor	4	Iron Ingot	12.5							Screw	50			1000
Alternate	Steel Screw	Constructor	4	Steel Beam	5							Screw	260			1000
Alternate	Iron Wire	Constructor	4	Iron Ingot	12.5							Wire	22.5			1000
Alternate	Stitched Iron Plate	Assembler	15	Iron Plate	18.75	Wire	37.5					Reinforced Iron Plate	5.625			1000
Alternate	Bolted Iron Plate	Assembler	15	Iron Plate	90	Screw	250					Reinforced Iron Plate	15			1000
Alternate	Adhered Iron Plate	Assembler	15	Iron Plate	11.25	Rubber	3.75					Reinforced Iron Plate	3.75			1000
Alternate	Bolted Frame	Assembler	15	Reinforced Iron Plate	7.5	Screw	140					Modular Frame	5			1000
Alternate	Steeled Frame	Assembler	15	Reinforced Iron Plate	2	Steel Pipe	10					Modular Frame	3			1000
Alternate	Fused Wire	Assembler	15	Copper Ingot	12	Caterium Ingot	3					Wire	90			1000
Alternate	Fused Quickwire	Assembler	15	Caterium Ingot	7.5	Copper Ingot	37.5					Quickwire	90			1000
Alternate	Insulated Cable	Assembler	15	Wire	45	Rubber	30					Cable	100			1000
Alternate	Quickwire Cable	Assembler	15	Quickwire	7.5	Rubber	5					Cable	27.5			1000
Alternate	Coated Cable	Refinery	30	Wire	37.5	Heavy Oil Residue	15					Cable	67.5			1000
Alternate	Fine Black Powder	Assembler	15	Sulfur	45	Compacted Coal	22.5					Black Powder	75			1000
Alternate	Copper Rotor	Assembler	15	Copper Sheet	22.5	Screw	195					Rotor	11.25			1000
Alternate	Steel Rotor	Assembler	15	Steel Pipe	10	Wire	30					Rotor	5			1000
Alternate	Iron Pipe	Constructor	4	Iron Ingot	100							Steel Pipe	25			1000
Alternate	Steel Rod	Constructor	4	Steel Ingot	12							Iron Rod	48			1000
Alternate	Molded Steel Pipe	Assembler	15	Steel Ingot	50	Concrete	30					Steel Pipe	50			1000
Alternate	Steel Canister	Constructor	4	Steel Ingot	60							Empty Canister	40			1000
Alternate	Encased Industrial Pipe	Assembler	15	Steel Pipe	28	Concrete	20					Encased Industrial Beam	4			1000
Alternate	Caterium Circuit Board	Assembler	15	Plastic	12.5	Quickwire	37.5					Circuit Board	8.75			1000
Alternate	Silicon Circuit Board	Assembler	15	Copper Sheet	27.5	Silica	27.5					Circuit Board	12.5			1000
Alternate	Crystal Computer	Assembler	15	Circuit Board	7.5	Crystal Oscillator	2.8125					Computer	2.8125			1000
Alternate	OC Supercomputer	Assembler	15	Radio Control Unit	9	Cooling System	9					Supercomputer	3			1000
Alternate	Turbo Electric Motor	Manufacturer	55	Motor	6.5625	Radio Control Unit	8.4375	Electromagnetic Turbine	4.6875	Rotor	6.5625	Turbo Motor	2.8125			1000
Alternate	Turbo Pressure Motor	Manufacturer	55	Motor	7.5	Pressure Conversion Cube	1.875	Packaged Nitrogen Gas	45	Stator	15	Turbo Motor	3.75			1000
Alternate	Rigour Motor	Manufacturer	55	Rotor	3.75	Stator	3.75	Crystal Oscillator	1.25			Motor	7.5			1000
Alternate	Automated Speed Wiring	Manufacturer	55	Stator	3.75	Wire	75	High-Speed Connector	1.875			Automated Wiring	7.5			1000
Alternate	Heavy Encased Frame	Manufacturer	55	Modular Frame	7.5	Encased Industrial Beam	9.375	Steel Pipe	33.75	Concrete	20.625	Heavy Modular Frame	2.8125			1000
Alternate	Heavy Flexible Frame	Manufacturer	55	Modular Frame	18.75	Encased Industrial Beam	11.25	Rubber	75	Screw	390	Heavy Modular Frame	3.75			1000
Alternate	Flexible Framework	Assembler	15	Modular Frame	3.75	Steel Beam	22.5					Versatile Framework	7.5			1000
Alternate	Fused Quickwire (HC)	Assembler	15	Quickwire	37.5	Cable	75					High-Speed Connector	3			1000
Alternate	Silicon High-Speed Connector	Manufacturer	55	Quickwire	90	Silica	37.5	Circuit Board	3			High-Speed Connector	3			1000
Alternate	Heat Exchanger	Assembler	15	Aluminum Casing	30	Rubber	30					Heat Sink	10			1000
Alternate	Radio Connection Unit	Manufacturer	55	Heat Sink	15	High-Speed Connector	7.5	Quartz Crystal	45			Radio Control Unit	3.75			1000
Alternate	Radio Control System	Manufacturer	55	Crystal Oscillator	1.5	Circuit Board	15	Aluminum Casing	90	Rubber	45	Radio Control Unit	4.5			1000
Alternate	Quartz Purification	Refinery	30	Raw Quartz	120	Nitric Acid	10					Quartz Crystal	75	Dissolved Silica	60	1000
Alternate	Cheapened Parts	Manufacturer	55	Iron Plate	20	Encased Industrial Beam	7.5	Steel Pipe	30	Concrete	20	Heavy Modular Frame	1.875			1000
Alternate	Recycled Plastic	Refinery	30	Rubber	30	Fuel	30					Plastic	60			1000
Alternate	Recycled Rubber	Refinery	30	Plastic	30	Fuel	30					Rubber	60			1000
Alternate	Diluted Fuel	Blender	75	Heavy Oil Residue	50	Water	100					Fuel	100			1000
Alternate	Heavy Oil Residue (Alt)	Refinery	30	Crude Oil	30							Heavy Oil Residue	40	Polymer Resin	20	1000
Alternate	Compacted Coal	Assembler	15	Coal	25	Sulfur	25					Compacted Coal	25			1000
Alternate	Biocoal	Constructor	4	Biomass	37.5							Coal	45			1000
Alternate	Charcoal	Constructor	4	Wood	15							Coal	150			1000
Alternate	Petroleum Coke (Alt)	Constructor	4	Polymer Resin	20							Petroleum Coke	40			1000
Alternate	Turbofuel (Alt)	Refinery	30	Fuel	22.5	Compacted Coal	15					Turbofuel	18.75			1000
Alternate	Turbo Heavy Fuel	Refinery	30	Heavy Oil Residue	37.5	Compacted Coal	30					Turbofuel	30			1000
Alternate	Turbo Blend Fuel	Blender	75	Fuel	15	Heavy Oil Residue	30	Sulfur	22.5	Petroleum Coke	22.5	Turbofuel	45			1000
Alternate	Fertile Uranium	Blender	75	Uranium	25	Uranium Waste	25	Nitric Acid	15	Sulfuric Acid	25	Fertile Uranium	100	Water	40	1000
Alternate	Infused Uranium Cell	Manufacturer	55	Uranium	25	Silica	15	Sulfur	25	Quickwire	75	Encased Uranium Cell	20			1000
Alternate	Uranium Fuel Unit	Manufacturer	55	Encased Uranium Cell	100	EM Control Rod	10	Crystal Oscillator	3	Rotor	10	Uranium Fuel Rod	3			1000
Alternate	Instant Plutonium Cell	Particle Accelerator	500	Non-Fissile Uranium	75	Aluminum Casing	10					Encased Plutonium Cell	10			1000
Alternate	Plutonium Fuel Unit	Manufacturer	55	Encased Plutonium Cell	10	Pressure Conversion Cube	0.5	Encased Industrial Beam	5	Heat Sink	5	Plutonium Fuel Rod	1			1000
Alternate	Coated Iron Plate	Assembler	15	Iron Plate	37.5	Plastic	7.5					Iron Plate	75			1000
Alternate	Copper Powder	Constructor	4	Copper Ingot	300							Copper Powder	50			1000
Alternate	Cheap Silica	Assembler	15	Raw Quartz	11.25	Limestone	18.75					Silica	26.25			1000
Alternate	Fine Concrete	Assembler	15	Silica	7.5	Limestone	30					Concrete	25			1000
Alternate	Rubber Concrete	Assembler	15	Limestone	50	Rubber	10					Concrete	45			1000
Alternate	Plastic Smart Plating	Manufacturer	55	Reinforced Iron Plate	2.5	Rotor	2.5	Plastic	7.5			Smart Plating	5			1000
Alternate	Cooked Power Shard (Tier 1)	Constructor	4	Blue Power Slug	7.5							Power Shard	7.5			1000
Alternate	Cooked Power Shard (Tier 2)	Constructor	4	Yellow Power Slug	5							Power Shard	10			1000
Alternate	Cooked Power Shard (Tier 3)	Constructor	4	Purple Power Slug	2.5							Power Shard	15			1000
Alternate	Heat Fused Frame	Blender	75	Heavy Modular Frame	3	Aluminum Ingot	150	Nitric Acid	37.5	Fuel	24	Fused Modular Frame	3			1000
Alternate	Alclad Casing	Assembler	15	Aluminum Ingot	150	Copper Ingot	75					Aluminum Casing	112.5			1000
Alternate	Coke Crystal Oscillator	Manufacturer	55	Quartz Crystal	18.75	Rubber	14.0625	Petroleum Coke	11.25			Crystal Oscillator	1.875			1000
Alternate	Insulated Crystal Oscillator	Manufacturer	55	Quartz Crystal	18.75	Rubber	15	AI Limiter	1.875			Crystal Oscillator	1.875			1000
Alternate	Smart Plating (Alt)	Assembler	15	Reinforced Iron Plate	2.5	Rotor	2.5					Smart Plating	2.5			1000
Basic	Smart Plating	Assembler	15	Reinforced Iron Plate	2.5	Rotor	2.5					Smart Plating	2.5			1000
Basic	Stator (Alt check)	Assembler	15	Steel Pipe	15	Wire	40					Stator	5			1000
Basic	Empty Canister	Constructor	4	Iron Plate	30							Empty Canister	60			1000
Basic	Empty Fluid Tank	Constructor	4	Aluminum Ingot	60							Empty Fluid Tank	60			1000
Basic	Alien Protein (Hatcher)	Constructor	4	Hatcher Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Hog)	Constructor	4	Hog Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Plasma Spitter)	Constructor	4	Plasma Spitter Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Stinger)	Constructor	4	Stinger Remains	20							Alien Protein	20			1000
Basic	Alien DNA Capsule	Constructor	4	Alien Protein	10							Alien DNA Capsule	10			1000
Basic	Gas Filter	Manufacturer	55	Coal	37.5	Rubber	15	Fabric	15			Gas Filter	7.5			1000
Basic	Iodine Infused Filter	Manufacturer	55	Gas Filter	3.75	Quickwire	30	Aluminum Casing	3.75			Iodine Infused Filter	3.75			1000
Basic	Hazmat Suit	Manufacturer	55	Rubber	50	Plastic	50	Alclad Aluminum Sheet	50	Fabric	50	Hazmat Suit	1			1000
Alternate	Cooling Device (Alt)	Blender	75	Heat Sink	10	Motor	2.5	Nitrogen Gas	60			Cooling System	5			1000
Basic	Dissolved Silica	Refinery	30	Silica	40	Nitric Acid	10					Dissolved Silica	70			1000
Basic	Medicinal Inhaler (Alien)	Equipment Workshop	0	Alien Protein	1	Beryl Nut	10	Paleberry	10	Bacon Agaric	5	Medicinal Inhaler	5			1000
Basic	Medicinal Inhaler (Berries)	Equipment Workshop	0	Beryl Nut	10	Paleberry	5					Medicinal Inhaler	1			1000
Basic	Medicinal Inhaler (Mushrooms)	Equipment Workshop	0	Bacon Agaric	10							Medicinal Inhaler	1			1000
Basic	Medicinal Inhaler (Protein)	Equipment Workshop	0	Alien Protein	3	Beryl Nut	30					Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Nutritional)	Equipment Workshop	0	Bacon Agaric	3	Paleberry	6	Beryl Nut	15			Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Therapeutic)	Equipment Workshop	0	Mycelia	45	Alien Protein	3	Bacon Agaric	3			Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Vitamin)	Equipment Workshop	0	Mycelia	30	Paleberry	15					Medicinal Inhaler	3			125
Quantum	SAM Fluctuator	Converter	250	Reanimated SAM	60	Wire	50	Steel Pipe	30			SAM Fluctuator	6			1000
Quantum	Alien Power Matrix	Quantum Encoder	500	SAM Fluctuator	12.5	Power Shard	7.5	Superposition Oscillator	7.5	Excited Photonic Matter	60	Alien Power Matrix	2.5	Dark Matter Residue	60	1000
Quantum	Synthetic Power Shard	Converter	250	Time Crystal	5	Dark Matter Crystal	10	Quartz Crystal	60			Power Shard	5			1000
Alternate	Automated Miner	Manufacturer	55	Steel Pipe	7.5	Iron Plate	7.5					Portable Miner	1			1000
Alternate	Electrode Circuit Board	Assembler	15	Rubber	30	Petroleum Coke	22.5					Circuit Board	5			1000
Alternate	Copper Smart Plating	Manufacturer	55	Copper Sheet	15	Rotor	3.75	Plastic	7.5			Smart Plating	5			1000
Alternate	Polyester Fabric	Refinery	30	Polymer Resin	80	Water	50					Fabric	5			1000
Alternate	Coated Iron Canister	Assembler	15	Iron Plate	25	Copper Sheet	25					Empty Canister	60			1000
Alternate	Steel Iron Plate	Assembler	15	Steel Ingot	7.5	Plastic	5					Iron Plate	45			1000
Alternate	Molded Beam	Manufacturer	55	Steel Ingot	120	Concrete	80					Steel Beam	45			1000
Alternate	Iodine Infused Filter (Alt)	Manufacturer	55	Gas Filter	3.75	Quickwire	30	Aluminum Casing	3.75			Iodine Infused Filter	3.75			1000
Alternate	Classic Battery (Alt)	Manufacturer	55	Sulfur	45	Alclad Aluminum Sheet	52.5	Plastic	60	Wire	90	Battery	30			1000
Alternate	Dark Matter Crystallization (Alt)	Particle Accelerator	1000	Dark Matter Residue	200							Dark Matter Crystal	20			1000
Alternate	Dark Matter Trap (Alt)	Particle Accelerator	1000	Time Crystal	30	Dark Matter Residue	150					Dark Matter Crystal	60			1000
Alternate	Concentrated Silica	Refinery	30	Raw Quartz	120	Nitric Acid	10					Quartz Crystal	75	Dissolved Silica	60	1000
Basic	Fabric	Constructor	4	Mycelia	15							Fabric	15			1000
Basic	SAM Fluctuator (Basic)	Constructor	4	SAM	60							SAM Fluctuator	6			1000
Basic	Electromagnetic Turbine	Assembler	15	Wire	12	Rotor	2.5					Electromagnetic Turbine	2.5			1000
Basic	Object Scanner	Assembler	15	Reinforced Iron Plate	3	Wire	80					Object Scanner	1			1000
Basic	Xeno-Basher	Manufacturer	55	Modular Frame	2.5	Xeno-Zapper	1	Cable	50	Wire	75	Xeno-Basher	1			1000
Basic	Portable Miner	Manufacturer	55	Steel Pipe	7.5	Iron Plate	7.5					Portable Miner	1			1000
Basic	Chainsaw	Manufacturer	55	Reinforced Iron Plate	5	Iron Rod	25	Screw	160	Cable	15	Chainsaw	1			1000
Basic	Rifle	Manufacturer	55	Reinforced Iron Plate	12.5	Screw	250	Steel Pipe	12.5	Rubber	25	Rifle	1			1000
Basic	Jetpack	Manufacturer	55	Plastic	100	Rubber	100	Circuit Board	75	Stator	50	Jetpack	1			1000
Basic	Hover Pack	Manufacturer	55	Motor	12.5	Heavy Modular Frame	7.5	Computer	3.75	Alclad Aluminum Sheet	100	Hover Pack	1			1000
Basic	Parachute	Assembler	15	Fabric	10	Cable	5					Parachute	1			1000
Basic	Zipline	Assembler	15	Xeno-Zapper	1	Cable	25					Zipline	1			1000
Basic	Blade Runners	Manufacturer	55	Silica	30	Modular Frame	3.75	Rotor	3.75			Blade Runners	1			1000

Basic	Packaged Ionized Fuel (basic)	Packager	10	Ionized Fuel	80	Empty Fluid Tank	80					Packaged Ionized Fuel	80			1000
Basic	Unpackage Ionized Fuel (basic)	Packager	10	Packaged Ionized Fuel	40							Ionized Fuel	40	Empty Fluid Tank	40	1000
Basic	Cloudy Diamond	Blender	75	Coal	600	Water	100					Diamonds	20			1000
Basic	Dark Matter Crystal (PA)	Particle Accelerator	500	Coal	200	Dark Matter Residue	100					Diamonds	30	Dark Matter Residue	0	1000

Quantum	Excited Photonic Matter (Blender)	Blender	75									Excited Photonic Matter	200			1000
Alternate	Leached Iron Ingot	Blender	75	Iron Ore	50	Sulfuric Acid	10					Iron Ingot	100			1000
Alternate	Leached Copper Ingot	Blender	75	Copper Ore	45	Sulfuric Acid	25					Copper Ingot	110			1000
Alternate	Leached Caterium Ingot	Blender	75	Caterium Ore	45	Sulfuric Acid	25					Caterium Ingot	30			1000
Alternate	Tempered Caterium Ingot	Foundry	16	Caterium Ore	45	Petroleum Coke	15					Caterium Ingot	30			1000
Alternate	Tempered Copper Ingot	Foundry	16	Copper Ore	25	Petroleum Coke	40					Copper Ingot	50			1000
Alternate	Steel Cast Plate	Foundry	16	Iron Ingot	15	Steel Ingot	15					Iron Plate	25			1000
Alternate	Plastic AI Limiter	Assembler	15	Quickwire	120	Plastic	28					AI Limiter	8			1000
Alternate	Caterium Circuit Board (Alt)	Assembler	15	Plastic	12.5	Quickwire	37.5					Circuit Board	8.75			1000
Alternate	Fertile Fiber	Constructor	4	Mycelia	10							Fabric	15			1000
Alternate	Polyester Fabric (Alt)	Refinery	30	Polymer Resin	80	Water	50					Fabric	5			1000
Alternate	Biocoal (Alt)	Constructor	4	Biomass	37.5							Coal	45			1000
Alternate	Smokeless Powder (Alt)	Refinery	30	Black Powder	20	Heavy Oil Residue	10					Smokeless Powder	20			1000
Alternate	Fine Black Powder (Alt)	Assembler	15	Sulfur	45	Compacted Coal	22.5					Black Powder	75			1000
Alternate	Bolted Modular Frame	Assembler	15	Reinforced Iron Plate	7.5	Screw	140					Modular Frame	5			1000
Alternate	Concrete Encased Beam	Assembler	15	Steel Beam	24	Concrete	30					Encased Industrial Beam	6			1000
Alternate	Super-State Computer	Manufacturer	55	Computer	3.6	Magnetic Field Generator	2.4	Battery	24	Wire	54	Supercomputer	2.4			1000
Alternate	Neural-Pulse Oscillator	Manufacturer	55	Crystal Oscillator	1.875	AI Limiter	7.5					Crystal Oscillator	3			1000
Alternate	Rigour Motor (Alt)	Manufacturer	55	Rotor	3.75	Stator	3.75	Crystal Oscillator	1.25			Motor	7.5			1000
Alternate	Electric Motor	Assembler	15	Electromagnetic Turbine	6.25	Rotor	3.75					Motor	7.5			1000
Alternate	Automated Speed Wiring (Alt)	Manufacturer	55	Stator	3.75	Wire	75	High-Speed Connector	1.875			Automated Wiring	7.5			1000
Alternate	Heavy Turbofuel	Blender	75	Heavy Oil Residue	37.5	Compacted Coal	30					Turbofuel	30			1000
Alternate	Nitro Rocket Fuel (Alt)	Blender	75	Fuel	100	Nitrogen Gas	75	Sulfur	100	Coal	50	Rocket Fuel	100	Compacted Coal	25	1000
Alternate	Unpackage Diluted Fuel	Packager	10	Packaged Diluted Fuel	60							Fuel	60	Empty Canister	60	1000
Alternate	Diluted Packaged Fuel (Alt)	Refinery	30	Heavy Oil Residue	30	Packaged Water	60					Packaged Diluted Fuel	60			1000

Alternate	Pure Iron Ingot (Alt)	Refinery	30	Iron Ore	35	Water	20					Iron Ingot	65			1000
Alternate	Molded Steel Pipe (Alt)	Assembler	15	Steel Ingot	50	Concrete	30					Steel Pipe	50			1000
Alternate	Cast Screw (Alt)	Constructor	4	Iron Ingot	12.5							Screw	50			1000
Alternate	Rubber Screw	Constructor	4	Rubber	12.5							Screw	50			1000
Alternate	Coated Iron Plate (Alt)	Assembler	15	Iron Plate	37.5	Plastic	7.5					Iron Plate	75			1000
Alternate	Steel Iron Plate (Alt)	Assembler	15	Steel Ingot	7.5	Plastic	5					Iron Plate	45			1000
Alternate	Recycled Rubber (Alt)	Refinery	30	Plastic	30	Fuel	30					Rubber	60			1000
Alternate	Recycled Plastic (Alt)	Refinery	30	Rubber	30	Fuel	30					Plastic	60			1000"""

lines = tsv_data.strip().split('\n')
headers = [h.strip() for h in lines[0].split('\t')]

tsv_recipes = []
for line in lines[1:]:
    cols = [c.strip() for c in line.split('\t')]
    if len(cols) < 14:
        continue
    while len(cols) < len(headers):
        cols.append('')
    row = dict(zip(headers, cols))
    tsv_recipes.append(row)

# ── 2. Group TSV recipes by output item, noting building type ─────────────────
from collections import defaultdict

by_output = defaultdict(list)
for r in tsv_recipes:
    out = r['OUT_1']
    building = r['BUILDING']
    inputs = []
    for i in range(1, 5):
        in_item = r.get(f'IN_{i}', '').strip()
        in_q = r.get(f'Q_{i}', '').strip()
        if in_item and in_q:
            inputs.append((in_item, float(in_q)))
    by_output[out].append({
        'building': building,
        'inputs': tuple(sorted(inputs)),  # sort for comparison
        'inputs_raw': inputs,
    })

# ── 3. Load current recipes.js for comparison ─────────────────────────────────
# (We already read it; I'll build a set of what's in recipes.js)
# Items in recipes.js (from the full read):
recipes_js_items = [
    'AI Expansion Server', 'AI Limiter', 'Adaptive Control Unit', 'Alclad Aluminum Sheet',
    'Alien DNA Capsule', 'Alien Power Matrix', 'Alien Protein', 'Alumina Solution',
    'Aluminum Casing', 'Aluminum Ingot', 'Aluminum Scrap', 'Assembly Director System',
    'Automated Wiring', 'Ballistic Warp Drive', 'Battery', 'Biochemical Sculptor',
    'Biomass', 'Black Powder', 'Blade Runners', 'Cable', 'Caterium Ingot', 'Chainsaw',
    'Circuit Board', 'Cluster Nobelisk', 'Coal', 'Color Cartridge', 'Compacted Coal',
    'Computer', 'Concrete', 'Cooling System', 'Copper Ingot', 'Copper Powder',
    'Copper Sheet', 'Crude Oil', 'Crystal Oscillator', 'Dark Matter Crystal',
    'Dark Matter Residue', 'Diamonds', 'Dissolved Silica', 'EM Control Rod',
    'Electromagnetic Turbine', 'Empty Canister', 'Empty Fluid Tank',
    'Encased Industrial Beam', 'Encased Plutonium Cell', 'Encased Uranium Cell',
    'Excited Photonic Matter', 'Explosive Rebar', 'Fabric', 'Factory Cart',
    'Fertile Uranium', 'Ficsite Ingot', 'Ficsite Trigon', 'Ficsonium',
    'Ficsonium Fuel Rod', 'Fuel', 'Fused Modular Frame', 'Gas Filter', 'Gas Mask',
    'Gas Nobelisk', 'Golden Factory Cart', 'Hazmat Suit', 'Heat Sink',
    'Heavy Modular Frame', 'Heavy Oil Residue', 'High-Speed Connector',
    'Homing Rifle Ammo', 'Hover Pack', 'Iodine Infused Filter', 'Ionized Fuel',
    'Iron Ingot', 'Iron Plate', 'Iron Rebar', 'Iron Rod', 'Jetpack',
    'Liquid Biofuel', 'Magnetic Field Generator', 'Medicinal Inhaler',
    'Modular Engine', 'Modular Frame', 'Motor', 'Neural-Quantum Processor',
    'Nitric Acid', 'Nitrogen Gas', 'Nobelisk', 'Nobelisk Detonator',
    'Non-Fissile Uranium', 'Nuclear Pasta', 'Nuke Nobelisk', 'Object Scanner',
    'Packaged Alumina Solution', 'Packaged Diluted Fuel', 'Packaged Fuel',
    'Packaged Heavy Oil Residue', 'Packaged Ionized Fuel', 'Packaged Liquid Biofuel',
    'Packaged Nitric Acid', 'Packaged Nitrogen Gas', 'Packaged Oil',
    'Packaged Rocket Fuel', 'Packaged Sulfuric Acid', 'Packaged Turbofuel',
    'Packaged Water', 'Parachute', 'Petroleum Coke', 'Plastic', 'Plutonium Fuel Rod',
    'Plutonium Pellet', 'Polymer Resin', 'Portable Miner', 'Power Shard',
    'Pressure Conversion Cube', 'Pulse Nobelisk', 'Quartz Crystal', 'Quickwire',
    'Radio Control Unit', 'Reanimated SAM', 'Rebar Gun', 'Reinforced Iron Plate',
    'Rifle', 'Rifle Ammo', 'Rocket Fuel', 'Rotor', 'Rubber', 'SAM Fluctuator',
    'Screw', 'Shatter Rebar', 'Silica', 'Singularity Cell', 'Smart Plating',
    'Smokeless Powder', 'Solid Biofuel', 'Stator', 'Steel Beam', 'Steel Ingot',
    'Steel Pipe', 'Stun Rebar', 'Sulfuric Acid', 'Supercomputer',
    'Superposition Oscillator', 'Thermal Propulsion Rocket', 'Time Crystal',
    'Turbo Motor', 'Turbo Rifle Ammo', 'Turbofuel', 'Uranium Fuel Rod',
    'Versatile Framework', 'Water', 'Wire', 'Xeno-Basher', 'Xeno-Zapper', 'Zipline',
]

# ── 4. Category 1: Equipment Workshop / Craft Bench analysis ──────────────────
print("=" * 130)
print("CATEGORY 1: EQUIPMENT WORKSHOP / CRAFT BENCH VARIANTS")
print("=" * 130)

print(f"\n{'Item':<32} {'Has Auto?':<12} {'Has EW?':<10} {'EW Same Inputs?':<16} {'Worth Add?':<12} {'Details'}")
print("-" * 130)

manual_buildings = {'Equipment Workshop', 'Craft Bench'}

# Find all items that have at least one manual (EW/Craft) recipe
items_with_manual = set()
for out, recipes in by_output.items():
    for r in recipes:
        if r['building'] in manual_buildings:
            items_with_manual.add(out)

# For each such item, compare with automated versions
for item in sorted(items_with_manual, key=str.lower):
    all_recipes = by_output[item]
    manual_recipes = [r for r in all_recipes if r['building'] in manual_buildings]
    auto_recipes = [r for r in all_recipes if r['building'] not in manual_buildings]
    
    has_auto = len(auto_recipes) > 0
    
    # Check if the EW variant (Equipment Workshop building) is already in recipes.js
    # We determine this by checking if any recipe in recipes.js for this item uses EW
    ew_variant_in_js = False
    if item in recipes_js_items:
        # Check which buildings are already present in recipes.js for this item
        # We need to check if the 'building' field includes 'Equipment Workshop' or 'Craft Bench'
        pass  # We'll check from TSV data instead
    # Better: check from TSV if there's a recipe with same building=EW AND same inputs already captured
    # Since we can't perfectly know from the JS alone, we'll rely on a known list:
    ew_already_in_js = {
        'Factory Cart', 'Gas Mask', 'Golden Factory Cart',
        'Medicinal Inhaler', 'Nobelisk Detonator', 'Rebar Gun',
        'Turbo Rifle Ammo', 'Xeno-Zapper',
    }
    # Items that have EW variant already stored in recipes.js (verified from manual inspection)
    # These are items whose ONLY recipe in recipes.js uses Equipment Workshop
    
    worth_adding = False
    same_inputs = True
    detail = ""
    
    if has_auto:
        manual_input_sets = {r['inputs'] for r in manual_recipes}
        auto_input_sets = {r['inputs'] for r in auto_recipes}
        
        diff_found = False
        for m_inp in manual_input_sets:
            if m_inp not in auto_input_sets:
                diff_found = True
                break
        
        if diff_found:
            same_inputs = False
            if item not in ew_already_in_js:
                worth_adding = True
            
            m = manual_recipes[0]
            a = auto_recipes[0]
            m_str = ", ".join(f"{q:.1f} {n}" for n, q in m['inputs_raw'])
            a_str = ", ".join(f"{q:.1f} {n}" for n, q in a['inputs_raw'])
            detail = f"EW [{m_str}] vs Auto ({a['building']}) [{a_str}]"
        else:
            same_inputs = True
            worth_adding = False
            a = auto_recipes[0]
            a_str = ", ".join(f"{q:.1f} {n}" for n, q in a['inputs_raw'])
            detail = f"Same inputs as {a['building']} [{a_str}]"
    else:
        same_inputs = True  # N/A
        m = manual_recipes[0]
        m_str = ", ".join(f"{q:.1f} {n}" for n, q in m['inputs_raw'])
        if item in ew_already_in_js:
            detail = f"Already in recipes.js [{m_str}]"
        else:
            detail = f"MISSING from recipes.js! EW-only [{m_str}]"
            worth_adding = True
    
    has_manual_str = "Yes" if len(manual_recipes) > 0 else "No"
    has_auto_str = "Yes" if has_auto else "No"
    same_str = "N/A" if not has_auto else ("Yes" if same_inputs else "NO")
    worth_str = "YES" if worth_adding else "no"
    if worth_adding:
        worth_str = "** YES **"
    
    print(f"{item:<32} {has_auto_str:<12} {has_manual_str:<10} {same_str:<16} {worth_str:<12} {detail}")

# ── 5. Category 2: Items in TSV but NOT in recipes.js ─────────────────────────
print("\n\n" + "=" * 130)
print("CATEGORY 2: ITEMS IN TSV BUT MISSING FROM recipes.js")
print("=" * 130)

tsv_items = set(by_output.keys())
missing_from_js = tsv_items - set(recipes_js_items)

if missing_from_js:
    print(f"\n{'Item':<35} {'Recipe Type':<15} {'Building':<22} {'Inputs'}")
    print("-" * 130)
    for item in sorted(missing_from_js, key=str.lower):
        recipes = by_output[item]
        for r in recipes:
            inp_str = ", ".join(f"{q:.1f} {n}" for n, q in r['inputs_raw'])
            print(f"{item:<35} {r['building']:<15} {inp_str}")
        print()
else:
    print("\nAll TSV items are present in recipes.js")

# ── 6. Check converter conversion recipes (ore-to-ore) ────────────────────────
print("\n\n" + "=" * 130)
print("CATEGORY 2b: CONVERTER ORE CONVERSION RECIPES (wiki, likely missing)")
print("=" * 130)
print("""
The wiki shows these Converter recipes that produce raw resources (not in our database):
  - Bauxite (Caterium):  Reanimated SAM 10 + Caterium Ore 150 → Bauxite 120
  - Bauxite (Copper):    Reanimated SAM 10 + Copper Ore 180 → Bauxite 120
  - Caterium Ore (Copper):   Reanimated SAM 10 + Copper Ore 150 → Caterium Ore 120
  - Caterium Ore (Quartz):   Reanimated SAM 10 + Raw Quartz 120 → Caterium Ore 120
  - Coal (Iron):         Reanimated SAM 10 + Iron Ore 180 → Coal 120
  - Coal (Limestone):    Reanimated SAM 10 + Limestone 360 → Coal 120
  - Copper Ore (Quartz): Reanimated SAM 10 + Raw Quartz 100 → Copper Ore 120
  - Copper Ore (Sulfur): Reanimated SAM 10 + Sulfur 120 → Copper Ore 120
These produce items currently classified as RAW_RESOURCES and not in RECIPES.
If you want the calculator to handle ore conversion, they should be added.
""")

# ── 7. Summary ────────────────────────────────────────────────────────────────
print("\n\n" + "=" * 130)
print("SUMMARY: RECOMMENDED ACTIONS")
print("=" * 130)

print(""\
"""
Category 1 — Equipment Workshop variants worth adding (different inputs from auto):
  Item                        EW Inputs (per min)                    Auto Inputs (per min)              Reason
  ───────────────────────────────────────────────────────────────────────────────────────────────────────────""")

# Detailed comparison for the key items
comparisons = [
    ("Black Powder", 
     "Coal 7.5, Sulfur 5 → 15/min", "EW",
     "Coal 15, Sulfur 15 → 30/min", "Assembler"),
    ("Nobelisk",
     "Black Powder 7.5, Steel Pipe 10 → 3/min", "EW",
     "Black Powder 20, Steel Pipe 20 → 10/min", "Assembler"),
    ("Nuke Nobelisk",
     "Nobelisk 2.5, Encased Uranium Cell 10, Black Powder 2.5, Sulfur 2.5 → 0.5/min", "EW",
     "Nobelisk 2.5, Encased Uranium Cell 10, Smokeless Powder 5, AI Limiter 3 → 0.5/min", "Manufacturer"),
    ("Shatter Rebar",
     "Iron Rebar 10, Quartz Crystal 5 → 5/min", "EW",
     "Iron Rebar 10, Quartz Crystal 15 → 5/min", "Assembler"),
    ("Stun Rebar",
     "Iron Rebar 10, Quickwire 15 → 10/min", "EW",
     "Iron Rebar 10, Quickwire 50 → 10/min", "Assembler"),
]

for item, ew_in, ew_b, auto_in, auto_b in comparisons:
    print(f"  {item:<28} {ew_in:<45} {auto_in:<40}")

print("""
  These 5 items have Equipment Workshop variants with DIFFERENT inputs/ratios
  than the automated (factory) versions. They are NOT currently in recipes.js.
  
  The remaining EW items either:
  - Have the SAME inputs as the automated version (redundant, skip):
    Gas Nobelisk, Pulse Nobelisk, Explosive Rebar, Cluster Nobelisk
  - Already have their EW variant in recipes.js:
    Factory Cart, Gas Mask, Golden Factory Cart, Medicinal Inhaler (all variants),
    Nobelisk Detonator, Rebar Gun, Turbo Rifle Ammo, Xeno-Zapper

Category 2 — Potentially missing items (Converter ore conversions):
  The 8 Converter recipes (producing Bauxite, Caterium Ore, Coal, Copper Ore
  from other resources) are not in recipes.js. These are raw resources currently
  marked as RAW_RESOURCES. Whether they should be added depends on if the
  calculator supports producing raw resources to feed into conversion loops.
""")
