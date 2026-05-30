import json
import re

# Parse TSV data
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
Basic	Reanimated SAM	Constructor	4	SAM	120							Reanimated SAM	30			1000
Basic	Steel Ingot	Foundry	16	Iron Ore	45	Coal	45					Steel Ingot	45			1000
Basic	Aluminum Ingot	Foundry	16	Aluminum Scrap	90	Silica	75					Aluminum Ingot	60			1000
Basic	Reinforced Iron Plate	Assembler	15	Iron Plate	30	Screw	60					Reinforced Iron Plate	5			1000
Basic	Rotor	Assembler	15	Iron Rod	20	Screw	100					Rotor	4			1000
Basic	Modular Frame	Assembler	15	Reinforced Iron Plate	3	Iron Rod	12					Modular Frame	2			1000
Basic	Encased Industrial Beam	Assembler	15	Steel Beam	18	Concrete	36					Encased Industrial Beam	6			1000
Basic	Stator	Assembler	15	Steel Pipe	15	Wire	40					Stator	5			1000
Basic	Motor	Assembler	15	Rotor	10	Stator	10					Motor	5			1000
Basic	Automated Wiring	Assembler	15	Stator	2.5	Cable	50					Automated Wiring	2.5			1000
Basic	AI Limiter	Assembler	15	Copper Sheet	25	Quickwire	100					AI Limiter	5			1000
Basic	Circuit Board	Assembler	15	Copper Sheet	15	Plastic	30					Circuit Board	7.5			1000
Basic	Alclad Aluminum Sheet	Assembler	15	Aluminum Ingot	30	Copper Ingot	10					Alclad Aluminum Sheet	30			1000
Basic	Heat Sink	Assembler	15	Copper Sheet	37.5	Copper Ingot	22.5				Heat Sink	7.5			1000
Basic	EM Control Rod	Assembler	15	Stator	6	AI Limiter	4					EM Control Rod	4			1000
Basic	Rifle Ammo	Assembler	15	Copper Sheet	15	Smokeless Powder	10					Rifle Ammo	75			1000
Basic	Homing Rifle Ammo	Assembler	15	Rifle Ammo	50	High-Speed Connector	2.5					Homing Rifle Ammo	25			1000
Basic	Cluster Nobelisk	Assembler	15	Nobelisk	7.5	Smokeless Powder	10					Cluster Nobelisk	2.5			1000
Basic	Versatile Framework	Assembler	15	Modular Frame	2.5	Steel Beam	30					Versatile Framework	5			1000
Basic	Adaptive Control Unit	Assembler	15	Automated Wiring	7.5	Circuit Board	5					Adaptive Control Unit	1			1000
Basic	Heavy Modular Frame	Manufacturer	55	Modular Frame	10	Steel Pipe	40	Encased Industrial Beam	10	Screw	240	Heavy Modular Frame	2			1000
Basic	Computer	Manufacturer	55	Circuit Board	10	Cable	20	Plastic	40			Computer	2.5			1000
Basic	High-Speed Connector	Manufacturer	55	Quickwire	210	Cable	37.5	Circuit Board	3.75			High-Speed Connector	3.75			1000
Basic	Crystal Oscillator	Manufacturer	55	Quartz Crystal	18	Cable	14	Reinforced Iron Plate	2.5			Crystal Oscillator	1			1000
Basic	Supercomputer	Manufacturer	55	Computer	7.5	AI Limiter	3.75	High-Speed Connector	5.625	Plastic	52.5	Supercomputer	1.875			1000
Basic	Radio Control Unit	Manufacturer	55	Aluminum Casing	40	Crystal Oscillator	1.25	Computer	2.5			Radio Control Unit	2.5			1000
Basic	Turbo Motor	Manufacturer	55	Cooling System	7.5	Radio Control Unit	3.75	Motor	7.5	Rubber	45	Turbo Motor	1.875			1000
Basic	Magnetic Field Generator	Assembler	15	Versatile Framework	2.5	EM Control Rod	1					Magnetic Field Generator	1			1000
Basic	Assembly Director System	Assembler	15	Adaptive Control Unit	1.5	Supercomputer	0.75					Assembly Director System	0.75			1000
Basic	Thermal Propulsion Rocket	Manufacturer	55	Cooling System	3	Fused Modular Frame	1	Modular Engine	2.5	Turbo Motor	1	Thermal Propulsion Rocket	1			1000
Basic	Modular Engine	Manufacturer	55	Motor	2	Rubber	15	Smart Plating	2			Modular Engine	1			1000
Basic	Adaptive Control Unit (Mfr)	Manufacturer	55	Automated Wiring	5	Circuit Board	5	Heavy Modular Frame	2	Computer	1	Adaptive Control Unit	1			1000
Basic	Plastic	Refinery	30	Crude Oil	30							Plastic	20	Heavy Oil Residue	10	1000
Basic	Rubber	Refinery	30	Crude Oil	30							Rubber	20	Heavy Oil Residue	20	1000
Basic	Fuel	Refinery	30	Crude Oil	60							Fuel	40	Polymer Resin	30	1000
Alternate	Heavy Oil Residue	Refinery	30	Crude Oil	30							Heavy Oil Residue	40	Polymer Resin	20	1000
Alternate	Polymer Resin	Refinery	30	Crude Oil	60							Polymer Resin	130	Heavy Oil Residue	20	1000
Basic	Petroleum Coke	Refinery	30	Heavy Oil Residue	40							Petroleum Coke	120			1000
Basic	Residual Rubber	Refinery	30	Polymer Resin	40	Water	40					Rubber	20			1000
Basic	Residual Plastic	Refinery	30	Polymer Resin	60	Water	20					Plastic	20			1000
Basic	Residual Fuel	Refinery	30	Heavy Oil Residue	60							Fuel	40			1000
Basic	Alumina Solution	Refinery	30	Bauxite	120	Water	180					Alumina Solution	120	Silica	50	1000
Basic	Aluminum Scrap	Refinery	30	Alumina Solution	240	Coal	120					Aluminum Scrap	360	Water	120	1000
Basic	Sulfuric Acid	Refinery	30	Sulfur	50	Water	50					Sulfuric Acid	50			1000
Basic	Nitric Acid	Blender	75	Nitrogen Gas	120	Water	30	Iron Plate	10			Nitric Acid	30			1000
Basic	Smokeless Powder	Refinery	30	Black Powder	20	Heavy Oil Residue	10					Smokeless Powder	20			1000
Basic	Ionized Fuel	Refinery	30	Rocket Fuel	40	Power Shard	2.5					Ionized Fuel	40	Compacted Coal	5	1000
Basic	Turbofuel	Refinery	30	Fuel	22.5	Compacted Coal	15					Turbofuel	18.75			1000
Basic	Liquid Biofuel	Refinery	30	Solid Biofuel	90	Water	45					Liquid Biofuel	60			1000
Alternate	Diluted Packaged Fuel	Refinery	30	Heavy Oil Residue	30	Packaged Water	60					Packaged Fuel	60			1000
Basic	Packaged Water	Packager	10	Water	60	Empty Canister	60					Packaged Water	60			1000
Basic	Packaged Oil	Packager	10	Crude Oil	30	Empty Canister	30					Packaged Oil	30			1000
Basic	Packaged Fuel	Packager	10	Fuel	40	Empty Canister	40					Packaged Fuel	40			1000
Basic	Packaged Heavy Oil Residue	Packager	10	Heavy Oil Residue	30	Empty Canister	30					Packaged Heavy Oil Residue	30			1000
Basic	Packaged Sulfuric Acid	Packager	10	Sulfuric Acid	40	Empty Canister	40					Packaged Sulfuric Acid	40			1000
Basic	Packaged Alumina Solution	Packager	10	Alumina Solution	120	Empty Canister	120					Packaged Alumina Solution	120			1000
Basic	Packaged Nitrogen Gas	Packager	10	Nitrogen Gas	240	Empty Fluid Tank	60					Packaged Nitrogen Gas	60			1000
Basic	Packaged Turbofuel	Packager	10	Turbofuel	20	Empty Canister	20					Packaged Turbofuel	20			1000
Basic	Packaged Liquid Biofuel	Packager	10	Liquid Biofuel	40	Empty Canister	40					Packaged Liquid Biofuel	40			1000
Basic	Packaged Nitric Acid	Packager	10	Nitric Acid	30	Empty Fluid Tank	30					Packaged Nitric Acid	30			1000
Basic	Packaged Rocket Fuel	Packager	10	Rocket Fuel	120	Empty Canister	60					Packaged Rocket Fuel	60			1000
Basic	Packaged Ionized Fuel	Packager	10	Ionized Fuel	80	Empty Fluid Tank	40					Packaged Ionized Fuel	40			1000
Basic	Unpackage Water	Packager	10	Packaged Water	120							Water	120	Empty Canister	120	1000
Basic	Unpackage Oil	Packager	10	Packaged Oil	60							Crude Oil	60	Empty Canister	60	1000
Basic	Unpackage Fuel	Packager	10	Packaged Fuel	60							Fuel	60	Empty Canister	60	1000
Basic	Unpackage Heavy Oil Residue	Packager	10	Packaged Heavy Oil Residue	20							Heavy Oil Residue	20	Empty Canister	20	1000
Basic	Unpackage Sulfuric Acid	Packager	10	Packaged Sulfuric Acid	60							Sulfuric Acid	60	Empty Canister	60	1000
Basic	Unpackage Alumina Solution	Packager	10	Packaged Alumina Solution	120							Alumina Solution	120	Empty Canister	120	1000
Basic	Unpackage Nitrogen Gas	Packager	10	Packaged Nitrogen Gas	60							Nitrogen Gas	240	Empty Canister	60	1000
Basic	Unpackage Turbofuel	Packager	10	Packaged Turbofuel	20							Turbofuel	20	Empty Canister	20	1000
Basic	Unpackage Liquid Biofuel	Packager	10	Packaged Liquid Biofuel	60							Liquid Biofuel	60	Empty Canister	60	1000
Basic	Unpackage Nitric Acid	Packager	10	Packaged Nitric Acid	20							Nitric Acid	20	Empty Fluid Tank	20	1000
Basic	Unpackage Rocket Fuel	Packager	10	Packaged Rocket Fuel	60							Rocket Fuel	120	Empty Fluid Tank	60	1000
Basic	Cooling System	Blender	75	Heat Sink	12	Rubber	12	Water	30	Nitrogen Gas	150	Cooling System	6			1000
Basic	Fused Modular Frame	Blender	75	Heavy Modular Frame	1.5	Aluminum Casing	75	Nitrogen Gas	37.5			Fused Modular Frame	1.5			1000
Basic	Battery	Blender	75	Sulfuric Acid	40	Alumina Solution	50	Aluminum Casing	20			Battery	20	Water	30	1000
Basic	Rocket Fuel	Blender	75	Turbofuel	60	Nitric Acid	10					Rocket Fuel	100	Compacted Coal	10	1000
Alternate	Nitro Rocket Fuel	Blender	75	Fuel	100	Nitrogen Gas	75	Sulfur	100	Coal	50	Rocket Fuel	150	Compacted Coal	25	1000
Basic	Non-Fissile Uranium	Blender	75	Uranium Waste	37.5	Silica	25	Nitric Acid	15	Sulfuric Acid	15	Non-Fissile Uranium	50	Water	15	1000
Basic	Encased Uranium Cell	Blender	75	Uranium	50	Concrete	15	Sulfuric Acid	40			Encased Uranium Cell	25	Sulfuric Acid	10	1000
Basic	Pressure Conversion Cube	Assembler	15	Fused Modular Frame	1	Radio Control Unit	2					Pressure Conversion Cube	1			1000
Basic	Nuclear Pasta	Particle Accelerator	500	Copper Powder	100	Pressure Conversion Cube	0.5					Nuclear Pasta	0.5			1000
Basic	Plutonium Pellet	Particle Accelerator	500	Non-Fissile Uranium	100	Uranium Waste	25					Plutonium Pellet	30			1000
Basic	Ficsonium	Particle Accelerator	1000	Plutonium Waste	10	Singularity Cell	10	Dark Matter Residue	200			Ficsonium	10			1000
Basic	Uranium Fuel Rod	Manufacturer	55	Encased Uranium Cell	20	Encased Industrial Beam	1.2	EM Control Rod	2			Uranium Fuel Rod	0.4			1000
Basic	Plutonium Fuel Rod	Manufacturer	55	Encased Plutonium Cell	7.5	Steel Beam	4.5	EM Control Rod	1.5	Heat Sink	2.5	Plutonium Fuel Rod	0.25			1000
Basic	Encased Plutonium Cell	Assembler	15	Plutonium Pellet	10	Concrete	20					Encased Plutonium Cell	5			1000
Basic	Ficsonium Fuel Rod	Quantum Encoder	1000	Ficsonium	5	EM Control Rod	5	Ficsite Trigon	100	Excited Photonic Matter	50	Ficsonium Fuel Rod	2.5	Dark Matter Residue	50	1000
Quantum	Time Crystal	Converter	250	Diamonds	12							Time Crystal	6			1000
Quantum	Diamonds	Particle Accelerator	250	Coal	600							Diamonds	30			1000
Quantum	Ficsite Ingot (Iron)	Converter	250	Reanimated SAM	40	Iron Ingot	240					Ficsite Ingot	10			1000
Quantum	Ficsite Ingot (Caterium)	Converter	250	Reanimated SAM	45	Caterium Ingot	60					Ficsite Ingot	15			1000
Quantum	Ficsite Ingot (Aluminum)	Converter	250	Reanimated SAM	60	Aluminum Ingot	120					Ficsite Ingot	30			1000
Quantum	Dark Matter Crystal	Particle Accelerator	1000	Diamonds	30	Dark Matter Residue	150					Dark Matter Crystal	30			1000
Quantum	Excited Photonic Matter	Converter	250									Excited Photonic Matter	200			1000
Quantum	Dark Matter Residue	Converter	250	Reanimated SAM	50							Dark Matter Residue	100			1000
Quantum	Neural-Quantum Processor	Quantum Encoder	500	Time Crystal	15	Supercomputer	3	Ficsite Trigon	45	Excited Photonic Matter	75	Neural-Quantum Processor	3	Dark Matter Residue	75	1000
Quantum	Superposition Oscillator	Quantum Encoder	500	Dark Matter Crystal	30	Crystal Oscillator	5	Alclad Aluminum Sheet	45	Excited Photonic Matter	125	Superposition Oscillator	5	Dark Matter Residue	125	1000
Quantum	AI Expansion Server	Quantum Encoder	500	Magnetic Field Generator	4	Neural-Quantum Processor	4	Superposition Oscillator	4	Excited Photonic Matter	100	AI Expansion Server	4	Dark Matter Residue	100	1000
Quantum	Biochemical Sculptor	Blender	75	Assembly Director System	0.5	Ficsite Trigon	40	Water	10			Biochemical Sculptor	2			1000
Quantum	Ballistic Warp Drive	Manufacturer	55	Thermal Propulsion Rocket	1	Singularity Cell	5	Superposition Oscillator	2	Dark Matter Crystal	40	Ballistic Warp Drive	1			1000
Quantum	Singularity Cell	Manufacturer	55	Nuclear Pasta	1	Dark Matter Crystal	20	Iron Plate	100	Concrete	200	Singularity Cell	10			1000
Basic	Black Powder	Equipment Workshop	0	Coal	7.5	Sulfur	5					Black Powder	15			1000
Basic	Black Powder (EW)	Equipment Workshop	0	Coal	7.5	Sulfur	5					Black Powder	15			500
Basic	Nobelisk	Equipment Workshop	0	Black Powder	7.5	Steel Pipe	10					Nobelisk	3			1000
Basic	Nobelisk (EW)	Equipment Workshop	0	Black Powder	7.5	Steel Pipe	10					Nobelisk	3			900
Basic	Gas Nobelisk	Equipment Workshop	0	Nobelisk	5	Biomass	50					Gas Nobelisk	5			1000
Basic	Pulse Nobelisk	Equipment Workshop	0	Nobelisk	5	Crystal Oscillator	1					Pulse Nobelisk	5			1000
Basic	Nuke Nobelisk	Equipment Workshop	0	Nobelisk	2.5	Encased Uranium Cell	10	Black Powder	2.5	Sulfur	2.5	Nuke Nobelisk	0.5			1000
Basic	Nuke Nobelisk (EW)	Equipment Workshop	0	Nobelisk	2.5	Encased Uranium Cell	10	Smokeless Powder	5			Nuke Nobelisk	0.5			1500
Basic	Shatter Rebar	Equipment Workshop	0	Iron Rebar	10	Quartz Crystal	5					Shatter Rebar	5			1000
Basic	Shatter Rebar (EW)	Equipment Workshop	0	Iron Rebar	10	Quartz Crystal	5					Shatter Rebar	5			600
Basic	Stun Rebar	Equipment Workshop	0	Iron Rebar	10	Quickwire	15					Stun Rebar	10			1000
Basic	Stun Rebar (EW)	Equipment Workshop	0	Iron Rebar	10	Quickwire	15					Stun Rebar	10			300
Basic	Explosive Rebar	Equipment Workshop	0	Iron Rebar	10	Smokeless Powder	10	Steel Pipe	10			Explosive Rebar	5			1000
Basic	Black Powder	Assembler	15	Coal	15	Sulfur	15					Black Powder	30		14
Basic	Nobelisk	Assembler	15	Black Powder	20	Steel Pipe	20					Nobelisk	10		152
Basic	Gas Nobelisk	Assembler	15	Nobelisk	5	Biomass	50					Gas Nobelisk	5		544
Basic	Pulse Nobelisk	Assembler	15	Nobelisk	5	Crystal Oscillator	1					Pulse Nobelisk	5		1533
Basic	Nuke Nobelisk	Manufacturer	55	Nobelisk	2.5	Encased Uranium Cell	10	Smokeless Powder	5	AI Limiter	3	Nuke Nobelisk	0.5			19600
Basic	Explosive Rebar	Manufacturer	55	Iron Rebar	10	Smokeless Powder	10	Steel Pipe	10			Explosive Rebar	5		360
Basic	Shatter Rebar	Assembler	15	Iron Rebar	10	Quartz Crystal	15					Shatter Rebar	5		332
Basic	Stun Rebar	Assembler	15	Iron Rebar	10	Quickwire	50					Stun Rebar	10		186
Basic	Turbo Rifle Ammo	Equipment Workshop	0	Rifle Ammo	125	Aluminum Casing	15	Packaged Turbofuel	15			Turbo Rifle Ammo	250			1000
Basic	Turbo Rifle Ammo	Blender	75	Rifle Ammo	125	Aluminum Casing	15	Turbofuel	15			Turbo Rifle Ammo	250			1000
Basic	Turbo Rifle Ammo	Manufacturer	55	Rifle Ammo	125	Aluminum Casing	15	Packaged Turbofuel	15			Turbo Rifle Ammo	250			1000
Basic	Xeno-Zapper	Equipment Workshop	0	Iron Rod	15	Reinforced Iron Plate	3	Cable	22.5	Wire	75	Xeno-Zapper	1.5			1000
Basic	Gas Mask	Equipment Workshop	0	Fabric	50	Copper Sheet	10	Steel Pipe	10			Gas Mask	1		14960
Basic	Nobelisk Detonator	Equipment Workshop	0	Object Scanner	0.75	Steel Beam	7.5	Cable	37.5			Nobelisk Detonator	0.75		6480
Basic	Rebar Gun	Equipment Workshop	0	Reinforced Iron Plate	6	Iron Rod	16	Screw	100			Rebar Gun	1		1968
Basic	Factory Cart	Equipment Workshop	0	Reinforced Iron Plate	12	Iron Rod	12	Rotor	6			Factory Cart	3		1552
Basic	Golden Factory Cart	Equipment Workshop	0	Caterium Ingot	45	Iron Rod	12	Rotor	6			Golden Factory Cart	3		1852
Alternate	Pure Iron Ingot	Refinery	30	Iron Ore	35	Water	20					Iron Ingot	65			1000
Alternate	Iron Alloy Ingot	Foundry	16	Iron Ore	40	Copper Ore	10					Iron Ingot	75			1000
Alternate	Pure Copper Ingot	Refinery	30	Copper Ore	15	Water	10					Copper Ingot	37.5			1000
Alternate	Copper Alloy Ingot	Foundry	16	Copper Ore	50	Iron Ore	50					Copper Ingot	100			1000
Alternate	Pure Caterium Ingot	Refinery	30	Caterium Ore	24	Water	24					Caterium Ingot	12			1000
Alternate	Solid Steel Ingot	Foundry	16	Iron Ingot	40	Coal	40					Steel Ingot	60			1000
Alternate	Compacted Steel Ingot	Foundry	16	Iron Ore	5	Compacted Coal	2.5					Steel Ingot	10			1000
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
Alternate	Fine Black Powder	Assembler	15	Sulfur	7.5	Compacted Coal	15					Black Powder	45			1000
Alternate	Copper Rotor	Assembler	15	Copper Sheet	22.5	Screw	195					Rotor	11.25			1000
Alternate	Steel Rotor	Assembler	15	Steel Pipe	10	Wire	30					Rotor	5			1000
Alternate	Iron Pipe	Constructor	4	Iron Ingot	100							Steel Pipe	25			1000
Alternate	Steel Rod	Constructor	4	Steel Ingot	12							Iron Rod	48			1000
Alternate	Molded Steel Pipe	Foundry	16	Steel Ingot	50	Concrete	30					Steel Pipe	50			1000
Alternate	Steel Canister	Constructor	4	Steel Ingot	40							Empty Canister	40			1000
Alternate	Encased Industrial Pipe	Assembler	15	Steel Pipe	24	Concrete	20					Encased Industrial Beam	4			1000
Alternate	Caterium Circuit Board	Assembler	15	Plastic	12.5	Quickwire	37.5					Circuit Board	8.75			1000
Alternate	Silicon Circuit Board	Assembler	15	Copper Sheet	27.5	Silica	27.5					Circuit Board	12.5			1000
Alternate	Crystal Computer	Assembler	15	Circuit Board	5	Crystal Oscillator	1.66667					Computer	3.33333			1000
Alternate	OC Supercomputer	Assembler	15	Radio Control Unit	6	Cooling System	6					Supercomputer	3			1000
Alternate	Caterium Computer	Manufacturer	55	Circuit Board	15	Quickwire	52.5	Rubber	22.5			Computer	3.75		1000
Alternate	Turbo Electric Motor	Manufacturer	55	Motor	6.5625	Radio Control Unit	8.4375	EM Control Rod	4.6875	Rotor	6.5625	Turbo Motor	2.8125			1000
Alternate	Turbo Pressure Motor	Manufacturer	55	Motor	7.5	Pressure Conversion Cube	1.875	Packaged Nitrogen Gas	45	Stator	15	Turbo Motor	3.75			1000
Alternate	Rigour Motor	Manufacturer	55	Rotor	3.75	Stator	3.75	Crystal Oscillator	1.25			Motor	7.5			1000
Alternate	Automated Speed Wiring	Manufacturer	55	Stator	3.75	Wire	75	High-Speed Connector	1.875			Automated Wiring	7.5			1000
Alternate	Heavy Encased Frame	Manufacturer	55	Modular Frame	7.5	Encased Industrial Beam	9.375	Steel Pipe	33.75	Concrete	20.625	Heavy Modular Frame	2.8125			1000
Alternate	Heavy Flexible Frame	Manufacturer	55	Modular Frame	18.75	Encased Industrial Beam	11.25	Rubber	75	Screw	390	Heavy Modular Frame	3.75			1000
Alternate	Flexible Framework	Manufacturer	55	Modular Frame	3.75	Steel Beam	22.5	Rubber	30			Versatile Framework	7.5			1000
Alternate	Silicon High-Speed Connector	Manufacturer	55	Quickwire	90	Silica	37.5	Circuit Board	3			High-Speed Connector	3			1000
Alternate	Heat Exchanger	Assembler	15	Aluminum Casing	30	Rubber	30					Heat Sink	10			1000
Alternate	Radio Connection Unit	Manufacturer	55	Heat Sink	15	High-Speed Connector	7.5	Quartz Crystal	45			Radio Control Unit	3.75			1000
Alternate	Radio Control System	Manufacturer	55	Crystal Oscillator	1.5	Circuit Board	15	Aluminum Casing	90	Rubber	45	Radio Control Unit	4.5			1000
Alternate	Quartz Purification	Refinery	30	Raw Quartz	120	Nitric Acid	10					Quartz Crystal	75	Dissolved Silica	60	1000
Alternate	Recycled Plastic	Refinery	30	Rubber	30	Fuel	30					Plastic	60			1000
Alternate	Recycled Rubber	Refinery	30	Plastic	30	Fuel	30					Rubber	60			1000
Alternate	Diluted Fuel	Blender	75	Heavy Oil Residue	50	Water	100					Fuel	100			1000
Basic	Compacted Coal	Assembler	15	Coal	25	Sulfur	25					Compacted Coal	25			1000
Basic	Biocoal	Constructor	4	Biomass	37.5							Coal	45			1000
Basic	Charcoal	Constructor	4	Wood	15							Coal	150			1000
Alternate	Turbo Heavy Fuel	Refinery	30	Heavy Oil Residue	37.5	Compacted Coal	30					Turbofuel	30			1000
Alternate	Turbo Blend Fuel	Blender	75	Fuel	15	Heavy Oil Residue	30	Sulfur	22.5	Petroleum Coke	22.5	Turbofuel	45			1000
Alternate	Fertile Uranium	Blender	75	Uranium	25	Uranium Waste	25	Nitric Acid	15	Sulfuric Acid	25	Fertile Uranium	100	Water	40	1000
Alternate	Infused Uranium Cell	Manufacturer	55	Uranium	25	Silica	15	Sulfur	25	Quickwire	75	Encased Uranium Cell	20			1000
Alternate	Uranium Fuel Unit	Manufacturer	55	Encased Uranium Cell	100	EM Control Rod	10	Crystal Oscillator	3	Rotor	10	Uranium Fuel Rod	3			1000
Alternate	Instant Plutonium Cell	Particle Accelerator	500	Non-Fissile Uranium	75	Aluminum Casing	10					Encased Plutonium Cell	10			1000
Alternate	Plutonium Fuel Unit	Assembler	15	Encased Plutonium Cell	10	Pressure Conversion Cube	0.5					Plutonium Fuel Rod	0.5			1000
Alternate	Coated Iron Plate	Assembler	15	Iron Ingot	37.5	Plastic	7.5					Iron Plate	75			1000
Basic	Copper Powder	Constructor	4	Copper Ingot	300							Copper Powder	50			1000
Alternate	Cheap Silica	Assembler	15	Raw Quartz	22.5	Limestone	37.5					Silica	52.5			1000
Alternate	Fine Concrete	Assembler	15	Silica	15	Limestone	60					Concrete	50			1000
Alternate	Rubber Concrete	Assembler	15	Limestone	100	Rubber	20					Concrete	90			1000
Alternate	Plastic Smart Plating	Manufacturer	55	Reinforced Iron Plate	2.5	Rotor	2.5	Plastic	7.5			Smart Plating	5			1000
Basic	Cooked Power Shard (Tier 1)	Constructor	4	Blue Power Slug	7.5							Power Shard	7.5			1000
Basic	Cooked Power Shard (Tier 2)	Constructor	4	Yellow Power Slug	5							Power Shard	10			1000
Basic	Cooked Power Shard (Tier 3)	Constructor	4	Purple Power Slug	2.5							Power Shard	12.5			1000
Alternate	Heat Fused Frame	Blender	75	Heavy Modular Frame	3	Aluminum Ingot	150	Nitric Acid	24	Fuel	30	Fused Modular Frame	3			1000
Alternate	Alclad Casing	Assembler	15	Aluminum Ingot	150	Copper Ingot	75					Aluminum Casing	112.5			1000
Alternate	Insulated Crystal Oscillator	Manufacturer	55	Quartz Crystal	18.75	Rubber	13.125	AI Limiter	1.875			Crystal Oscillator	1.875			1000
Basic	Smart Plating	Assembler	15	Reinforced Iron Plate	2.5	Rotor	2.5					Smart Plating	2.5			1000
Basic	Empty Canister	Constructor	4	Plastic	30							Empty Canister	60			1000
Basic	Empty Fluid Tank	Constructor	4	Aluminum Ingot	60							Empty Fluid Tank	60			1000
Basic	Alien Protein (Hatcher)	Constructor	4	Hatcher Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Hog)	Constructor	4	Hog Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Plasma Spitter)	Constructor	4	Plasma Spitter Remains	20							Alien Protein	20			1000
Basic	Alien Protein (Stinger)	Constructor	4	Stinger Remains	20							Alien Protein	20			1000
Basic	Alien DNA Capsule	Constructor	4	Alien Protein	10							Alien DNA Capsule	10			1000
Basic	Gas Filter	Manufacturer	55	Coal	30	Iron Plate	15	Fabric	15			Gas Filter	7.5			1000
Basic	Iodine Infused Filter	Manufacturer	55	Gas Filter	3.75	Quickwire	30	Aluminum Casing	3.75			Iodine Infused Filter	3.75			1000
Basic	Hazmat Suit	Equipment Workshop	0	Rubber	25	Plastic	25	Alclad Aluminum Sheet	25	Fabric	25	Hazmat Suit	0.5			1000
Alternate	Cooling Device (Alt)	Blender	75	Heat Sink	10	Motor	2.5	Nitrogen Gas	60			Cooling System	5			1000
Basic	Dissolved Silica	Refinery	30	Silica	40	Nitric Acid	10					Dissolved Silica	70			1000
Basic	Medicinal Inhaler (Alien)	Equipment Workshop	0	Alien Protein	1	Beryl Nut	10	Paleberry	10	Bacon Agaric	5	Medicinal Inhaler	5			1000
Basic	Medicinal Inhaler (Berries)	Equipment Workshop	0	Beryl Nut	10	Paleberry	5					Medicinal Inhaler	1			1000
Basic	Medicinal Inhaler (Mushrooms)	Equipment Workshop	0	Bacon Agaric	10							Medicinal Inhaler	1			1000
Basic	Medicinal Inhaler (Protein)	Equipment Workshop	0	Alien Protein	3	Beryl Nut	30					Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Nutritional)	Equipment Workshop	0	Bacon Agaric	3	Paleberry	6	Beryl Nut	15			Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Therapeutic)	Equipment Workshop	0	Mycelia	45	Alien Protein	3	Bacon Agaric	3			Medicinal Inhaler	3			125
Basic	Medicinal Inhaler (Vitamin)	Equipment Workshop	0	Mycelia	30	Paleberry	15					Medicinal Inhaler	3			125
Quantum	SAM Fluctuator	Manufacturer	55	Reanimated SAM	60	Wire	50	Steel Pipe	30			SAM Fluctuator	10			1000
Quantum	Alien Power Matrix	Quantum Encoder	500	SAM Fluctuator	12.5	Power Shard	7.5	Superposition Oscillator	7.5	Excited Photonic Matter	60	Alien Power Matrix	2.5	Dark Matter Residue	60	1000
Quantum	Synthetic Power Shard	Quantum Encoder	250	Time Crystal	10	Dark Matter Crystal	10	Quartz Crystal	60	Excited Photonic Matter	60	Power Shard	5	Dark Matter Residue	60	1000
Alternate	Automated Miner	Assembler	15	Steel Pipe	4	Iron Plate	4					Portable Miner	1			1000
Alternate	Electrode Circuit Board	Assembler	15	Rubber	20	Petroleum Coke	40					Circuit Board	5			1000
Basic	Polyester Fabric	Refinery	30	Polymer Resin	30	Water	30					Fabric	30			1000
Alternate	Coated Iron Canister	Assembler	15	Iron Plate	30	Copper Sheet	15					Empty Canister	60			1000
Alternate	Molded Beam	Foundry	16	Steel Ingot	120	Concrete	80					Steel Beam	45			1000
Alternate	Dark Matter Crystallization (Alt)	Particle Accelerator	1000	Dark Matter Residue	200							Dark Matter Crystal	20			1000
Alternate	Dark Matter Trap (Alt)	Particle Accelerator	1000	Time Crystal	30	Dark Matter Residue	150					Dark Matter Crystal	60			1000
Basic	Fabric	Assembler	15	Mycelia	15	Biomass	75					Fabric	15			1000
Basic	Electromagnetic Turbine	Assembler	15	Wire	12	Rotor	2.5					Electromagnetic Turbine	2.5			1000
Basic	Object Scanner	Equipment Workshop	0	Reinforced Iron Plate	6	Wire	30	Screw	75			Object Scanner	1.5			1000
Basic	Xeno-Basher	Equipment Workshop	0	Xeno-Zapper	1.5	Modular Frame	3.75	Iron Rod	18.75	Wire	375	Xeno-Basher	0.75			1000
Basic	Portable Miner	Equipment Workshop	0	Iron Plate	3	Iron Rod	6					Portable Miner	1.5			1000
Basic	Chainsaw	Equipment Workshop	0	Reinforced Iron Plate	5	Iron Rod	25	Screw	160	Cable	15	Chainsaw	1			1000
Basic	Rifle	Equipment Workshop	0	Motor	1	Rubber	5	Steel Pipe	12.5	Screw	125	Rifle	0.5			1000
Basic	Jetpack	Equipment Workshop	0	Motor	5	Steel Pipe	10	Iron Plate	25	Wire	50	Jetpack	1			1000
Basic	Hover Pack	Equipment Workshop	0	Motor	4	Heavy Modular Frame	2	Computer	4	Alclad Aluminum Sheet	20	Hover Pack	0.5			1000
Basic	Parachute	Equipment Workshop	0	Fabric	30	Cable	15					Parachute	1.5			1000
Basic	Zipline	Equipment Workshop	0	Xeno-Zapper	1.5	Quickwire	45	Iron Rod	4.5	Cable	15	Zipline	1.5			1000
Basic	Blade Runners	Equipment Workshop	0	Silica	20	Modular Frame	3	Rotor	3			Blade Runners	1			1000
Basic	Unpackage Ionized Fuel (basic)	Packager	10	Packaged Ionized Fuel	80							Ionized Fuel	80	Empty Fluid Tank	40	1000
Alternate	Cloudy Diamond	Particle Accelerator	250	Coal	240	Limestone	480					Diamonds	20			1000
Alternate	Leached Iron Ingot	Refinery	30	Iron Ore	50	Sulfuric Acid	10					Iron Ingot	100			1000
Alternate	Leached Copper Ingot	Refinery	30	Copper Ore	45	Sulfuric Acid	25					Copper Ingot	110			1000
Alternate	Leached Caterium Ingot	Refinery	30	Caterium Ore	54	Sulfuric Acid	30					Caterium Ingot	36			1000
Alternate	Tempered Caterium Ingot	Foundry	16	Caterium Ore	45	Petroleum Coke	15					Caterium Ingot	22.5			1000
Alternate	Tempered Copper Ingot	Foundry	16	Copper Ore	25	Petroleum Coke	40					Copper Ingot	60			1000
Alternate	Steel Cast Plate	Foundry	16	Iron Ingot	15	Steel Ingot	15					Iron Plate	45			1000
Alternate	Plastic AI Limiter	Assembler	15	Quickwire	120	Plastic	28					AI Limiter	8			1000
Alternate	Super-State Computer	Manufacturer	55	Computer	7.2	EM Control Rod	2.4	Battery	24	Wire	60	Supercomputer	2.4			1000
Alternate	Electric Motor	Assembler	15	EM Control Rod	3.75	Rotor	7.5					Motor	7.5			1000
Quantum	Bauxite (Caterium)	Converter	250	Reanimated SAM	10	Caterium Ore	150	Bauxite	120	1000
Quantum	Bauxite (Copper)	Converter	250	Reanimated SAM	10	Copper Ore	180	Bauxite	120	1000
Quantum	Caterium Ore (Copper)	Converter	250	Reanimated SAM	10	Copper Ore	150	Caterium Ore	120	1000
Quantum	Caterium Ore (Quartz)	Converter	250	Reanimated SAM	10	Raw Quartz	120	Caterium Ore	120	1000
Quantum	Coal (Iron)	Converter	250	Reanimated SAM	10	Iron Ore	180	Coal	120	1000
Quantum	Coal (Limestone)	Converter	250	Reanimated SAM	10	Limestone	360	Coal	120	1000
Quantum	Copper Ore (Quartz)	Converter	250	Reanimated SAM	10	Raw Quartz	100	Copper Ore	120	1000
Quantum	Copper Ore (Sulfur)	Converter	250	Reanimated SAM	10	Sulfur	120	Copper Ore	120	1000
Quantum	Iron Ore (Limestone)	Converter	250	Reanimated SAM	10	Limestone	240	Iron Ore	120	1000
Quantum	Limestone (Sulfur)	Converter	250	Reanimated SAM	10	Sulfur	20	Limestone	120	1000
Quantum	Nitrogen Gas (Bauxite)	Converter	250	Reanimated SAM	10	Bauxite	100	Nitrogen Gas	120	1000
Quantum	Nitrogen Gas (Caterium)	Converter	250	Reanimated SAM	10	Caterium Ore	120	Nitrogen Gas	120	1000
Quantum	Raw Quartz (Bauxite)	Converter	250	Reanimated SAM	10	Bauxite	100	Raw Quartz	120	1000
Quantum	Raw Quartz (Coal)	Converter	250	Reanimated SAM	10	Coal	240	Raw Quartz	120	1000
Quantum	Sulfur (Coal)	Converter	250	Reanimated SAM	10	Coal	200	Sulfur	120	1000
Quantum	Sulfur (Iron)	Converter	250	Reanimated SAM	10	Iron Ore	300	Sulfur	120	1000
Quantum	Uranium Ore (Bauxite)	Converter	250	Reanimated SAM	10	Bauxite	480	Uranium	120	1000
Alternate	Aluminum Beam	Constructor	4	Aluminum Ingot	22.5							Steel Beam	22.5			1000
Alternate	Aluminum Rod	Constructor	4	Aluminum Ingot	7.5							Iron Rod	52.5			1000
Alternate	Basic Iron Ingot	Foundry	16	Iron Ore	25	Limestone	40					Iron Ingot	50			1000
Alternate	Caterium Wire	Constructor	4	Caterium Ingot	15							Wire	120			1000
Alternate	Electromagnetic Connection Rod	Assembler	15	Stator	8	High-Speed Connector	4					EM Control Rod	8			1000
Alternate	Fused Quartz Crystal	Foundry	16	Raw Quartz	75	Coal	36					Quartz Crystal	54			1000
Alternate	Oil-Based Diamonds	Particle Accelerator	250	Crude Oil	200							Diamonds	40			1000
Alternate	Petroleum Diamonds	Particle Accelerator	250	Petroleum Coke	720							Diamonds	30			1000
Alternate	Pink Diamonds	Converter	250	Coal	120	Quartz Crystal	45					Diamonds	15			1000
Alternate	Pure Quartz Crystal	Refinery	30	Raw Quartz	67.5	Water	37.5					Quartz Crystal	52.5			1000
Alternate	Quickwire Stator	Assembler	15	Steel Pipe	16	Quickwire	60					Stator	8			1000
Alternate	Steamed Copper Sheet	Refinery	30	Copper Ingot	22.5	Water	22.5					Copper Sheet	22.5			1000
Alternate	Turbo Diamonds	Particle Accelerator	250	Coal	600	Packaged Turbofuel	40					Diamonds	60			1000
Alternate	Dark-Ion Fuel	Converter	250	Packaged Rocket Fuel	240	Dark Matter Crystal	80					Ionized Fuel	200	Compacted Coal	40	1000
Alternate	Distilled Silica	Blender	75	Dissolved Silica	120	Limestone	50	Water	100			Silica	270	Water	80	1000
Basic	Uranium Fuel Rod (burning)	Nuclear Power Plant	0	Uranium Fuel Rod	0.2	Water	240			Uranium Waste	10			1000		
Basic	Plutonium Fuel Rod (burning)	Nuclear Power Plant	0	Plutonium Fuel Rod	0.1	Water	240			Plutonium Waste	1			1000
"""

# Parse wiki JSON
with open('/Users/Mike/Desktop/test_folder/satisfactory_recipes.json') as f:
    wiki = json.load(f)

# Build TSV recipe records
tsv_records = []
lines = tsv_data.strip().split('\n')
headers = [h.strip() for h in lines[0].split('\t')]
for line in lines[1:]:
    cols = [c.strip() for c in line.split('\t')]
    if len(cols) < 14:
        continue
    while len(cols) < len(headers):
        cols.append('')
    row = dict(zip(headers, cols))
    recipe_name = row.get('RECIPE_NAME', '').strip()
    building = row.get('BUILDING', '').strip()
    mw_str = row.get('MW', '').strip()
    mw = float(mw_str) if mw_str else 0
    out_1 = row.get('OUT_1', '').strip()
    q_out = float(row.get('Q_OUT', '').strip() or 0)
    out_2 = row.get('OUT_2', '').strip()
    q_out2 = float(row.get('Q_OUT2', '').strip() or 0)
    ins = {}
    for i in range(1, 5):
        in_item = row.get(f'IN_{i}', '').strip()
        in_q = row.get(f'Q_{i}', '').strip()
        if in_item and in_q:
            ins[in_item] = float(in_q)
    outs = {out_1: q_out}
    if out_2 and q_out2:
        outs[out_2] = q_out2
    tsv_records.append({
        'name': recipe_name,
        'building': building,
        'mw': mw,
        'inputs': ins,
        'outputs': outs
    })

# Build normalized lookup keyed by (name_normalized, building)
def norm_name(n):
    n = n.lower().strip()
    n = n.replace('electromagnetic control rod', 'em control rod')
    n = n.replace('screws', 'screw')
    n = n.replace('hoverpack', 'hover pack')
    n = n.replace('iodine-infused filter', 'iodine infused filter')
    return n

def wiki_to_tsv_output_name(wiki_out_name):
    """Map wiki output item names to TSV conventions"""
    m = {
        'Screws': 'Screw',
        'Electromagnetic Control Rod': 'EM Control Rod',
        'Hoverpack': 'Hover Pack',
        'Iodine-Infused Filter': 'Iodine Infused Filter',
    }
    return m.get(wiki_out_name, wiki_out_name)

def tsv_to_wiki_input_name(tsv_name):
    m = {
        'Screw': 'Screws',
        'EM Control Rod': 'Electromagnetic Control Rod',
        'Hover Pack': 'Hoverpack',
    }
    return m.get(tsv_name, tsv_name)

# Collect all wiki recipe records
wiki_records = []
for section_name, section_recipes in wiki['recipes'].items():
    for r in section_recipes:
        building = r.get('building', '')
        ins = r.get('inputs', {})
        outs = r.get('outputs', {})
        # Skip empty/invalid
        if not outs:
            continue
        wiki_records.append({
            'name': r['name'],
            'building': building,
            'inputs': ins,
            'outputs': outs,
            'section': section_name
        })

# Find wiki Equipment Workshop recipes
wiki_ew = [r for r in wiki_records if r['building'] == 'Equipment Workshop']
tsv_ew = [r for r in tsv_records if r['building'] == 'Equipment Workshop']

print("=" * 70)
print("EQUIPMENT WORKSHOP RECIPES: WIKI vs TSV")
print("=" * 70)

# Check every wiki EW recipe exists in TSV EW
wiki_ew_names = set(r['name'] for r in wiki_ew)
tsv_ew_names = set(r['name'] for r in tsv_ew)

# Normalize names for comparison
wiki_ew_norm = set()
for r in wiki_ew:
    n = r['name'].lower().replace(' ', '')
    wiki_ew_norm.add(n)

tsv_ew_norm = set()
for r in tsv_ew:
    n = r['name'].lower().replace(' ', '')
    tsv_ew_norm.add(n)

print(f"\nWiki EW recipes ({len(wiki_ew)}): {[r['name'] for r in wiki_ew]}")
print(f"\nTSV EW recipes ({len(tsv_ew)}): {list(tsv_ew_names)}")

# Check each wiki EW recipe
for w_r in wiki_ew:
    # Find matching TSV recipe
    w_norm = w_r['name'].lower().replace(' ', '')
    matched = False
    for t_r in tsv_ew:
        t_norm = t_r['name'].lower().replace(' ', '')
        if w_norm == t_norm:
            matched = True
            # Compare quantities
            issues = []
            # Compare inputs
            w_in = w_r['inputs']
            t_in = t_r['inputs']
            all_keys = set(list(w_in.keys()) + list(t_in.keys()))
            for k in all_keys:
                wv = w_in.get(k, 0)
                tv = t_in.get(k, 0)
                if abs(wv - tv) > 0.01:
                    issues.append(f"  INPUT '{k}': wiki={wv}, tsv={tv}")
            # Compare outputs
            w_out = w_r['outputs']
            t_out = t_r['outputs']
            all_ok = set(list(w_out.keys()) + list(t_out.keys()))
            for k in all_ok:
                wv = w_out.get(k, 0)
                tv = t_out.get(k, 0)
                if abs(wv - tv) > 0.01:
                    issues.append(f"  OUTPUT '{k}': wiki={wv}, tsv={tv}")
            if issues:
                print(f"\n  ** MISMATCH: {w_r['name']} **")
                for i in issues:
                    print(i)
            break
    if not matched:
        print(f"\n  ** MISSING from TSV EW: {w_r['name']} **")

# Check for TSV EW recipes not in wiki
for t_r in tsv_ew:
    t_norm = t_r['name'].lower().replace(' ', '')
    found = False
    for w_n in wiki_ew_norm:
        if t_norm == w_n:
            found = True
            break
    if not found:
        print(f"\n  ** EXTRA in TSV EW (not in wiki): {t_r['name']} **")
        ins_str = ', '.join(f"{k} {v}" for k,v in t_r['inputs'].items())
        outs_str = ', '.join(f"{k} {v}" for k,v in t_r['outputs'].items())
        print(f"     [{t_r['building']}] IN: {ins_str} -> OUT: {outs_str}")

print("\n\n" + "=" * 70)
print("KEY RECIPE CHECKS")
print("=" * 70)

# Check Medicinal Inhalers
print("\n--- Medicinal Inhaler Variants ---")
wiki_inhalers = [r for r in wiki_records if 'Inhaler' in r['name'] or 'inhaler' in r['name'].lower()]
tsv_inhalers = [r for r in tsv_records if 'Inhaler' in r['name'] or 'inhaler' in r['name'].lower()]
print(f"Wiki inhaler recipes: {len(wiki_inhalers)}")
for r in wiki_inhalers:
    ins = ', '.join(f"{k}:{v}" for k,v in r['inputs'].items())
    outs = ', '.join(f"{k}:{v}" for k,v in r['outputs'].items())
    print(f"  {r['name']} [{r['building']}] IN({ins}) OUT({outs})")
print(f"TSV inhaler recipes: {len(tsv_inhalers)}")
for r in tsv_inhalers:
    ins = ', '.join(f"{k}:{v}" for k,v in r['inputs'].items())
    outs = ', '.join(f"{k}:{v}" for k,v in r['outputs'].items())
    print(f"  {r['name']} [{r['building']}] IN({ins}) OUT({outs})")

# Check Factory Cart
print("\n--- Factory Cart / Golden Factory Cart ---")
for t_r in tsv_ew:
    if 'Factory Cart' in t_r['name'] or 'factory cart' in t_r['name'].lower():
        ins = ', '.join(f"{k}:{v}" for k,v in t_r['inputs'].items())
        outs = ', '.join(f"{k}:{v}" for k,v in t_r['outputs'].items())
        print(f"  TSV: {t_r['name']} [{t_r['building']}] IN({ins}) OUT({outs})")
for w_r in wiki_ew:
    if 'Factory Cart' in w_r['name'] or 'factory cart' in w_r['name'].lower():
        ins = ', '.join(f"{k}:{v}" for k,v in w_r['inputs'].items())
        outs = ', '.join(f"{k}:{v}" for k,v in w_r['outputs'].items())
        print(f"  Wiki: {w_r['name']} [{w_r['building']}] IN({ins}) OUT({outs})")

# Check Rifle
print("\n--- Rifle ---")
for t_r in tsv_ew:
    if t_r['name'] == 'Rifle':
        ins = ', '.join(f"{k}:{v}" for k,v in t_r['inputs'].items())
        outs = ', '.join(f"{k}:{v}" for k,v in t_r['outputs'].items())
        print(f"  TSV: {t_r['name']} [{t_r['building']}] IN({ins}) OUT({outs})")
for w_r in wiki_ew:
    if w_r['name'] == 'Rifle':
        ins = ', '.join(f"{k}:{v}" for k,v in w_r['inputs'].items())
        outs = ', '.join(f"{k}:{v}" for k,v in w_r['outputs'].items())
        print(f"  Wiki: {w_r['name']} [{w_r['building']}] IN({ins}) OUT({outs})")

# Full cross-section comparison - all recipes
print("\n\n" + "=" * 70)
print("ALL RECIPES: WIKI vs TSV QUANTITY DIFFERENCES")
print("(comparing by building + normalized name)")
print("=" * 70)

def canonical_key(r):
    name = r['name'].lower().strip()
    name = name.replace('electromagnetic control rod', 'em control rod')
    name = name.replace('screws', 'screw')
    name = name.replace('hoverpack', 'hover pack')
    name = name.replace('iodine-infused filter', 'iodine infused filter')
    name = name.replace('nutritional inhaler', 'medicinal inhaler (nutritional)')
    name = name.replace('protein inhaler', 'medicinal inhaler (protein)')
    name = name.replace('therapeutic inhaler', 'medicinal inhaler (therapeutic)')
    name = name.replace('vitamin inhaler', 'medicinal inhaler (vitamin)')
    name = re.sub(r'\(alt build\)', '', name).strip()
    return (name, r['building'])

wiki_by_key = {}
for r in wiki_records:
    key = canonical_key(r)
    if key not in wiki_by_key:
        wiki_by_key[key] = []
    wiki_by_key[key].append(r)

tsv_by_key = {}
for r in tsv_records:
    key = (r['name'].lower().strip(), r['building'])
    tsv_by_key[key] = r

# Compare all wiki records against TSV
diff_count = 0
for key, w_rs in sorted(wiki_by_key.items()):
    for w_r in w_rs:
        t_key = (w_r['name'].lower().strip(), w_r['building'])
        if t_key in tsv_by_key:
            t_r = tsv_by_key[t_key]
            issues = []
            w_in = w_r['inputs']
            t_in = t_r['inputs']
            all_ink = set(list(w_in.keys()) + list(t_in.keys()))
            for k in all_ink:
                wv = w_in.get(k, 0)
                tv = t_in.get(k, 0)
                if abs(wv - tv) > 0.01:
                    issues.append(f"IN '{k}' wiki={wv} tsv={tv}")
            w_out = w_r['outputs']
            t_out = t_r['outputs']
            all_outk = set(list(w_out.keys()) + list(t_out.keys()))
            for k in all_outk:
                wv = w_out.get(k, 0)
                tv = t_out.get(k, 0)
                if abs(wv - tv) > 0.01:
                    issues.append(f"OUT '{k}' wiki={wv} tsv={tv}")
            if issues:
                diff_count += 1
                print(f"\n  [{w_r['section']}] {w_r['name']} ({w_r['building']}):")
                for i in issues:
                    print(f"    {i}")
        else:
            # Try matching with norm_name
            alt_found = False
            for tk, tr in tsv_by_key.items():
                if norm_name(tk[0]) == norm_name(w_r['name'].lower()) and tk[1] == w_r['building']:
                    alt_found = True
                    issues = []
                    w_in = w_r['inputs']
                    t_in = tr['inputs']
                    all_ink = set(list(w_in.keys()) + list(t_in.keys()))
                    for k in all_ink:
                        wv = w_in.get(k, 0)
                        tv = t_in.get(k, 0)
                        if abs(wv - tv) > 0.01:
                            issues.append(f"IN '{k}' wiki={wv} tsv={tv}")
                    w_out = w_r['outputs']
                    t_out = tr['outputs']
                    all_outk = set(list(w_out.keys()) + list(t_out.keys()))
                    for k in all_outk:
                        wv = w_out.get(k, 0)
                        tv = t_out.get(k, 0)
                        if abs(wv - tv) > 0.01:
                            issues.append(f"OUT '{k}' wiki={wv} tsv={tv}")
                    if issues:
                        diff_count += 1
                        print(f"\n  [{w_r['section']}] {w_r['name']} ({w_r['building']}) [matched alt name: {tr['name']}]")
                        for i in issues:
                            print(f"    {i}")
                    break
            if not alt_found:
                print(f"\n  ** Wiki recipe NOT in TSV: [{w_r['section']}] {w_r['name']} ({w_r['building']})")
                ins = ', '.join(f"{k}:{v}" for k,v in w_r['inputs'].items())
                outs = ', '.join(f"{k}:{v}" for k,v in w_r['outputs'].items())
                print(f"     IN({ins}) OUT({outs})")

if diff_count == 0:
    print("\n  All wiki recipes match TSV quantities.")
else:
    print(f"\n  Total quantity differences found: {diff_count}")
