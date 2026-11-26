# TASK-062 Antigravity Light-Rig/Glass Closeout (`deltrol_p2s_explorer_v30.glb`)

- **Task**: `TASK-062-LIGHT-RIG-GLASS-CLOSEOUT`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v30.glb`
- **Size / SHA-256**: `2923580` bytes / `10638F8F784BE2FC117C6B447A7737874189D361AD08D7D3AF194ED43121C84F`
- **Old SHA-256 (`v29`)**: `76737FE47D847E9ABF452C9525D613ED5B50BA2994E046D04EC48CFE895F4049`
- **Embedded `KHR_lights_punctual` Rig**:
  - `chamber_upper_rail_light`: `point`, pos `[-0.04, 0.08, 0.08]`, color `[1.0, 0.82, 0.62]`, intensity `2.15`, range `0.35`
  - `chamber_turbine_fill_light`: `point`, pos `[0.04, -0.04, 0.12]`, color `[1.0, 0.80, 0.58]`, intensity `1.15`, range `0.35`
- **Right Glass**: `Right Glass Warm Sheen` `baseColorFactor: [0.62, 0.42, 0.28, 0.42]`
- **Verdict**: `REVISION_REQUIRED` (`12/15 PASS`; `13_Steel_Rail` **PASS** `dMax=12.9`, `07_Right_Win_Glass` **PASS** `dMax=13.5`, `14_Turbine_Arch` `dMax=15.6`, `11_Glass_Skylight` `dMax=19.0`, `12_Chamber_Upper_C` `dMax=15.6`).

## 1. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Diagnostic / Before-After**: `reports/task062-light-rig-diagnostic.png`, `reports/task062-light-glass-before-after.png`.
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task062-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9074` (`>= 0.90` PASS)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(50.2, 37.9, 27.7)` | `13.5` | `PASS` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(165.9, 149.2, 133.3)` | `19.0` | `FAIL` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(91.5, 69.8, 47.4)` | `15.6` | `FAIL` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(101.4, 84.7, 70.8)` | `12.9` | `PASS` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(93.4, 80.6, 66.6)` | `15.6` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 3. Renders & Artifacts

- `reports/task062-explorer-front.png`
- `reports/task062-explorer-left20.png`
- `reports/task062-explorer-right20.png`
- `reports/task062-explorer-elevated.png`
- `reports/task062-explorer-4view-sheet.png`
- `reports/task062-silhouette-overlay.png`
- `reports/task062-reference-candidate-contact-sheet.png`
- `reports/task062-light-rig-diagnostic.png`
- `reports/task062-light-glass-before-after.png`
