# TASK-058 Antigravity Explicit Interior Material Patch (`deltrol_p2s_explorer_v26.glb`)

- **Task**: `TASK-058-EXPLICIT-INTERIOR-MATERIAL-PATCH`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v26.glb`
- **Size / SHA-256**: `2922936` bytes / `7F8C9F3CF95381559C2DFFD0735E597D8217FB47C63387211D5D6D3B8734EE53`
- **Old SHA-256 (`v24`)**: `820F896C198A86D4B79B5B1EAE16C54E1A648123E831D17CE55B5A37D817690E`
- **Verdict**: `REVISION_REQUIRED` (`12/15 PASS`; `KHR_materials_unlit` visibly changed ROI 13/14/07, but `13_Steel_Rail` `dMax=37.9`, `14_Turbine_Arch` `dMax=18.6`, and `07_Right_Win_Glass` `dMax=41.6` still need calibration).

## 1. GLB Material JSON Patch (Zero Emissive, `KHR_materials_unlit`)

- `Machined Dark Alloy` (ROI 13 `x_gantry_crossbeam`) & `Machined Steel Rails` (ROI 13 `mech_gantry_rail_bot`): `KHR_materials_unlit: {}`, `baseColorFactor: [0.36, 0.24, 0.17, 1.0]`, zero `emissiveFactor` / `emissiveTexture`.
- `Sculpted Metallic Turbine Arch` (ROI 14 `bracket_swept_arch`): `KHR_materials_unlit: {}`, `baseColorFactor: [0.32, 0.21, 0.14, 1.0]`, zero `emissiveFactor` / `emissiveTexture`.
- `Right Glass Warm Sheen` (ROI 07): `baseColorFactor: [0.55, 0.36, 0.22, 0.42]`.

## 2. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Diagnostic / Before-After**: `reports/task058-material-through-glass-diagnostic.png`, `reports/task058-interior-before-after.png`.
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task058-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(104.0, 87.0, 72.0)` | `41.6` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(144.6, 123.1, 105.0)` | `9.3` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(69.5, 55.3, 45.0)` | `6.4` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(76.4, 59.5, 47.4)` | `37.9` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(90.4, 76.9, 63.7)` | `18.6` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 4. Renders & Artifacts

- `reports/task058-explorer-front.png`
- `reports/task058-explorer-left20.png`
- `reports/task058-explorer-right20.png`
- `reports/task058-explorer-elevated.png`
- `reports/task058-explorer-4view-sheet.png`
- `reports/task058-silhouette-overlay.png`
- `reports/task058-reference-candidate-contact-sheet.png`
- `reports/task058-material-through-glass-diagnostic.png`
- `reports/task058-interior-before-after.png`
