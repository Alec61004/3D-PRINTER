# TASK-061 Antigravity Light-Rig and Glass Final Tune (`deltrol_p2s_explorer_v29.glb`)

- **Task**: `TASK-061-LIGHT-RIG-GLASS-FINAL-TUNE`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v29.glb`
- **Size / SHA-256**: `2923580` bytes / `76737FE47D847E9ABF452C9525D613ED5B50BA2994E046D04EC48CFE895F4049`
- **Embedded `KHR_lights_punctual` Rig**:
  - `chamber_upper_rail_light`: `point`, pos `[0.0, 0.08, 0.06]`, color `[1.0, 0.82, 0.62]`, intensity `1.25`, range `0.55`
  - `chamber_turbine_fill_light`: `point`, pos `[0.04, -0.02, 0.14]`, color `[1.0, 0.80, 0.58]`, intensity `0.75`, range `0.45`
- **Right Glass**: `Right Glass Warm Sheen` `baseColorFactor: [0.55, 0.38, 0.24, 0.34]`
- **Verdict**: `REVISION_REQUIRED` (`12/15 PASS`; `13_Steel_Rail` improved `30.3 -> 22.4`, `14_Turbine_Arch` `18.4 -> 16.5`, `07_Right_Win_Glass` `31.1 -> 20.2`).

## 1. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Diagnostic / Before-After**: `reports/task061-light-rig-diagnostic.png`, `reports/task061-light-glass-before-after.png`.
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task061-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9075` (`>= 0.90` PASS)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(43.5, 31.6, 21.8)` | `20.2` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.3, 68.7, 53.9)` | `3.4` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(162.5, 143.9, 125.9)` | `13.3` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(88.2, 66.4, 44.6)` | `12.3` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(92.0, 75.8, 63.4)` | `22.4` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(92.5, 79.3, 65.0)` | `16.5` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 3. Renders & Artifacts

- `reports/task061-explorer-front.png`
- `reports/task061-explorer-left20.png`
- `reports/task061-explorer-right20.png`
- `reports/task061-explorer-elevated.png`
- `reports/task061-explorer-4view-sheet.png`
- `reports/task061-silhouette-overlay.png`
- `reports/task061-reference-candidate-contact-sheet.png`
- `reports/task061-light-rig-diagnostic.png`
- `reports/task061-light-glass-before-after.png`
