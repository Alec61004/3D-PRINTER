# TASK-053 Antigravity CAD Interior Source Rebuild (`deltrol_p2s_explorer_v21.glb`)

- **Task**: `TASK-053-CAD-INTERIOR-SOURCE-REBUILD`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v21.glb`
- **Size / SHA-256**: `2911424` bytes / `84641D7DA27FE993186002694F868F9190528902257C544BAB66394C57B9E4F8`
- **Verdict**: `PIVOT_REQUIRED` (`12/15 PASS`; `13_Steel_Rail dMax=35.1`, `14_Turbine_Arch dMax=20.4`, `07_Right_Win_Glass dMax=26.0`).

## 1. GLB Material JSON & Node Mapping

- `x_gantry_crossbeam`, `toolhead_chassis`, `toolhead_fan_rotor`, `toolhead_hotend_sock` -> `Machined Dark Alloy` (`metallicFactor=0.20`, zero `emissiveFactor` / `emissiveTexture`)
- `bracket_swept_arch` -> `Sculpted Metallic Turbine Arch` (`metallicFactor=0.25`, zero `emissiveFactor` / `emissiveTexture`)
- `toolhead_front_cowl` -> `Anodized Copper Toolhead` (`metallicFactor=0.25`, zero `emissiveFactor` / `emissiveTexture`)
- Horizontal & vertical rails -> `Machined Steel Rails` (`metallicFactor=0.25`, zero `emissiveFactor` / `emissiveTexture`)

## 2. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Before/After Crop**: `reports/task053-interior-before-after.png` (`REF` vs `v20` vs `v21`).
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task053-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(37.7, 25.0, 15.2)` | `26.0` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(154.5, 134.4, 115.8)` | `3.8` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(82.8, 62.0, 41.5)` | `6.9` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(79.3, 65.0, 55.2)` | `35.1` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(88.5, 75.3, 62.1)` | `20.4` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 4. External/Source-Asset Strategy

A fresh external CAD/Blender source asset for the interior gantry, toolhead, and turbine arch (replacing the `v12-v21` procedural mesh) is required to achieve reference proportions and lighting response.

## 5. Renders & Artifacts

- `reports/task053-explorer-front.png`
- `reports/task053-explorer-left20.png`
- `reports/task053-explorer-right20.png`
- `reports/task053-explorer-elevated.png`
- `reports/task053-explorer-4view-sheet.png`
- `reports/task053-silhouette-overlay.png`
- `reports/task053-reference-candidate-contact-sheet.png`
- `reports/task053-interior-before-after.png`
