# TASK-050 Antigravity UV-Baked Interior Material Pivot (`deltrol_p2s_explorer_v18.glb`)

- **Task**: `TASK-050-UV-BAKED-INTERIOR-MATERIAL-PIVOT`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v18.glb`
- **Size / SHA-256**: `2911404` bytes / `F8910E5A4298FCE34CB7B71429774EB5EEEE484CC0C9410B3605D5E753F79110`
- **Verdict**: `PIVOT_REQUIRED` (Low-metallicity `0.15–0.25` + `emissive_scale=0.0` did not move `13_Steel_Rail` `dMax=35.3` or `14_Turbine_Arch` `dMax=20.1` toward `(114,93,80)` / `(109,88,73)`, and `07_Right_Win_Glass` regressed to `dMax=25.5`).

## 1. Exact Node / Mesh / Primitive / Material Mapping & Texture Slots

- `x_gantry_crossbeam`, `toolhead_chassis`, `toolhead_fan_rotor`, `toolhead_hotend_sock` -> material `4` (`Machined Dark Alloy`, `metallic=0.15, emissive_scale=0.0`)
- `bracket_swept_arch` -> material `14` (`Sculpted Metallic Turbine Arch`, `metallic=0.20, emissive_scale=0.0`)
- `toolhead_front_cowl` -> material `16` (`Anodized Copper Toolhead`, `metallic=0.25, emissive_scale=0.0`)
- `toolhead_nozzle` -> material `17` (`Brass Nozzle`)
- Horizontal & vertical rails -> material `12` (`Machined Steel Rails`, `metallic=0.22, emissive_scale=0.0`)
- **Texture dimensions & UV**: `512x512` packed PNGs (`Base Color`, `Roughness`), `UVMap` (`cube_project`).

## 2. Before/After & Fixed-Fixture Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Before/After Crop**: `reports/task050-rail-turbine-before-after.png` (`REF` vs `v17` vs `v18`).
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task050-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9073` (`>= 0.90` PASS)
- **Contact Shadow**: `Ref Y=236.9 (236.5,236.9,237.3)` vs `Cand Y=236.0 (234.8,236.2,237.7)`

## 3. Post-ACES sRGB ROI Table (`<= 15 RGB/ch` gate, `12/15 PASS`)

| ROI | Ref RGB | Cand RGB | dMax | Status |
|---|---|---|---:|---|
| `01_Forehead_L` | `(229.8, 228.2, 222.6)` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(149.8, 140.9, 132.7)` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(69.5, 61.0, 48.8)` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(142.9, 134.2, 123.4)` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(67.4, 56.9, 44.4)` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(54.0, 45.5, 34.6)` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(38.2, 25.2, 15.3)` | `25.5` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(154.6, 134.6, 115.9)` | `4.0` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(83.4, 63.0, 42.5)` | `7.5` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(79.0, 64.7, 54.8)` | `35.3` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(88.8, 75.6, 62.3)` | `20.1` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 4. Blocker Explanation

Removing emission and lowering metallic to `0.15–0.25` confirmed that the fixed viewer's interior lighting behind `Smoked Glass` (`door_glass`) is too attenuated to lift `13_Steel_Rail` and `14_Turbine_Arch` to `(114,93,80)` / `(109,88,73)`, and also darkened `07_Right_Win_Glass` (`dMax=25.5`).

## 5. Renders & Artifacts

- `reports/task050-explorer-front.png`
- `reports/task050-explorer-left20.png`
- `reports/task050-explorer-right20.png`
- `reports/task050-explorer-elevated.png`
- `reports/task050-explorer-4view-sheet.png`
- `reports/task050-silhouette-overlay.png`
- `reports/task050-reference-candidate-contact-sheet.png`
- `reports/task050-rail-turbine-before-after.png`
