# TASK-059 Antigravity PBR Calibration Grid (`deltrol_p2s_explorer_v27.glb`)

- **Task**: `TASK-059-PBR-CALIBRATION-GRID`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v27.glb`
- **Size / SHA-256**: `2923056` bytes / `02276BE2F2A60EAE5C5E671CFA179D80F61AF7D952CE29FB398E61F3D1BC7AA6`
- **Verdict**: `PIVOT_REQUIRED` (Rolled back `KHR_materials_unlit` to shaded PBR with zero emission; even at `baseColorFactor: [1.0, 0.88, 0.78, 1.0]`, `metallicFactor: 0.08`, `roughnessFactor: 0.45`, the fixed viewer's interior lighting behind `Smoked Glass` cannot lift `13_Steel_Rail` `dMax=35.5` or `14_Turbine_Arch` `dMax=19.6` to `(114,93,80)` / `(109,88,73)` without emission or unlit).

## 1. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Calibration Grid / Before-After**: `reports/task059-pbr-calibration-grid.png`, `reports/task059-interior-before-after.png`.
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task059-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9073` (`>= 0.90` PASS)
- **Contact Shadow**: `Ref Y=236.9 (236.5,236.9,237.3)` vs `Cand Y=236.0 (234.8,236.2,237.7)`

## 2. Post-ACES sRGB ROI Table (`<= 15 RGB/ch` gate, `12/15 PASS`)

| ROI | Ref RGB | Cand RGB | dMax | Status |
|---|---|---|---:|---|
| `01_Forehead_L` | `(229.8, 228.2, 222.6)` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(149.8, 140.9, 132.7)` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(69.5, 61.0, 48.8)` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(142.9, 134.2, 123.4)` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(67.4, 56.9, 44.4)` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(54.0, 45.5, 34.6)` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(31.5, 20.6, 12.0)` | `32.2` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(155.1, 133.6, 113.8)` | `3.0` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(84.6, 62.3, 40.5)` | `8.7` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(78.8, 64.1, 54.0)` | `35.5` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(89.4, 74.8, 60.2)` | `19.6` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 3. Renders & Artifacts

- `reports/task059-explorer-front.png`
- `reports/task059-explorer-left20.png`
- `reports/task059-explorer-right20.png`
- `reports/task059-explorer-elevated.png`
- `reports/task059-explorer-4view-sheet.png`
- `reports/task059-silhouette-overlay.png`
- `reports/task059-reference-candidate-contact-sheet.png`
- `reports/task059-pbr-calibration-grid.png`
- `reports/task059-interior-before-after.png`
