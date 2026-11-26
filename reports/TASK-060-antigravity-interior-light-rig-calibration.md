# TASK-060 Antigravity Interior Light-Rig Calibration (`deltrol_p2s_explorer_v28.glb`)

- **Task**: `TASK-060-INTERIOR-LIGHT-RIG-CALIBRATION`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v28.glb`
- **Size / SHA-256**: `2923580` bytes / `193C44ADB67153525B9DDAF10BE3AEE4F98819B90DF65BB1EBA427F3190EB29A`
- **Embedded `KHR_lights_punctual` Rig**:
  - `chamber_upper_rail_light`: `point`, pos `[0.0, 0.08, 0.04]`, color `[1.0, 0.82, 0.62]` (~3400K), intensity `0.45`, range `0.45`
  - `chamber_turbine_fill_light`: `point`, pos `[0.04, -0.02, 0.14]`, color `[1.0, 0.80, 0.58]`, intensity `0.28`, range `0.35`
- **Verdict**: `REVISION_REQUIRED` (`12/15 PASS`; `KHR_lights_punctual` improved `13_Steel_Rail` `dMax=35.5 -> 30.3` and `14_Turbine_Arch` `dMax=19.6 -> 18.4`, `07_Right_Win_Glass` `dMax=31.1`; needs higher light intensity).

## 1. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Diagnostic / Before-After**: `reports/task060-light-rig-diagnostic.png`, `reports/task060-light-rig-before-after.png`.
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task060-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(32.6, 22.6, 14.7)` | `31.1` | `FAIL` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(158.0, 137.3, 117.7)` | `6.7` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(86.0, 63.9, 42.0)` | `10.1` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(84.0, 68.9, 57.9)` | `30.3` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(90.6, 76.5, 62.1)` | `18.4` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 3. Renders & Artifacts

- `reports/task060-explorer-front.png`
- `reports/task060-explorer-left20.png`
- `reports/task060-explorer-right20.png`
- `reports/task060-explorer-elevated.png`
- `reports/task060-explorer-4view-sheet.png`
- `reports/task060-silhouette-overlay.png`
- `reports/task060-reference-candidate-contact-sheet.png`
- `reports/task060-light-rig-diagnostic.png`
- `reports/task060-light-rig-before-after.png`
