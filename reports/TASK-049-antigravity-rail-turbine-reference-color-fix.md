# TASK-049 Antigravity Rail/Turbine Reference-Color Fix (`deltrol_p2s_explorer_v17.glb`)

- **Task**: `TASK-049-RAIL-TURBINE-REFERENCE-COLOR-FIX`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v17.glb`
- **Size / SHA-256**: `3451824` bytes / `C8C5BDADB6794DDD2099FFE0DC323843E4D4676D0C1A9807459601AA81F1F8D8`
- **Verdict**: `PIVOT_REQUIRED` (Pivot Guard triggered: second projection/material attempt in `v15-v17` family left `13_Steel_Rail` at `dMax=33.9` and `14_Turbine_Arch` at `dMax=18.7`, with before/after crop `reports/task049-rail-turbine-before-after.png` showing minimal ROI change).

## 1. Exact Node / Mesh / Primitive / Material Index Mapping

- `x_gantry_crossbeam` -> material `4` (`Machined Dark Alloy`)
- `bracket_swept_arch` -> material `14` (`Sculpted Metallic Turbine Arch`)
- `toolhead_chassis`, `toolhead_fan_rotor`, `toolhead_hotend_sock` -> material `4` (`Machined Dark Alloy`)
- `toolhead_front_cowl` -> material `16` (`Anodized Copper Toolhead`)
- `toolhead_nozzle` -> material `17` (`Brass Nozzle`)
- Horizontal & vertical rails -> material `12` (`Machined Steel Rails`)
- `door_bottom_rail`, `door_console_arch_hood`, `door_top_rail` -> material `0` (`Graphite Door Frame`)

## 2. Before/After & Fixed-Fixture Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Before/After Crop**: `reports/task049-rail-turbine-before-after.png` (`REF` vs `v16` vs `v17`).
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task049-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9073` (`>= 0.90` PASS)
- **Contact Shadow**: `Ref Y=236.9 (236.5,236.9,237.3)` vs `Cand Y=236.0 (234.8,236.2,237.7)`

## 3. Post-ACES sRGB ROI Table (`<= 15 RGB/ch` gate, `13/15 PASS`)

| ROI | Ref RGB | Cand RGB | dMax | Status |
|---|---|---|---:|---|
| `01_Forehead_L` | `(229.8, 228.2, 222.6)` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(149.8, 140.9, 132.7)` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(69.5, 61.0, 48.8)` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(142.9, 134.2, 123.4)` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(67.4, 56.9, 44.4)` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(54.0, 45.5, 34.6)` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(57.5, 40.1, 25.9)` | `6.6` | `PASS` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(155.5, 135.3, 116.9)` | `4.7` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(76.1, 54.8, 36.4)` | `6.6` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(80.4, 65.8, 55.6)` | `33.9` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(90.3, 77.7, 65.0)` | `18.7` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 4. Proposed Pivot

Pivot away from the `v12-v17` 8-bit PNG emission-baked high-metallicity pipeline (`metallic=0.72..0.88`), which clamps `emit_col` to `[0, 1]` and loses diffuse response behind `door_glass`. Instead, rebuild the interior gantry/rail/turbine sub-assembly with clean UV-unwrapped low-metallicity (`0.0–0.25`) Cycles-baked `Base Color` + `Roughness` maps so the viewer's directional + IBL lighting directly drives the warm metallic contrast without 8-bit emission clamping.

## 5. Renders & Artifacts

- `reports/task049-explorer-front.png`
- `reports/task049-explorer-left20.png`
- `reports/task049-explorer-right20.png`
- `reports/task049-explorer-elevated.png`
- `reports/task049-explorer-4view-sheet.png`
- `reports/task049-silhouette-overlay.png`
- `reports/task049-reference-candidate-contact-sheet.png`
- `reports/task049-rail-turbine-before-after.png`
