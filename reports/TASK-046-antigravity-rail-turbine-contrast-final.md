# TASK-046 Antigravity Rail & Turbine Contrast Final (`deltrol_p2s_explorer_v14.glb`)

- **Task**: `TASK-046-RAIL-TURBINE-CONTRAST-FINAL`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v14.glb`
- **Size / SHA-256**: `3262824` bytes / `DA59578C7CB2365E7DE3ACC5799616FF8741187F188FB76754DD2C8FC5E85DFF`
- **Scene**: `64` nodes, `56` meshes, zero billboards/image planes/2.5D rigs, zero edits to `website/src/**` or `tools/true3d_audit_viewer.html`.
- **Verdict**: `REVISION_REQUIRED` (`13/15` ROIs pass `<= 15 RGB/ch`; `13_Steel_Rail` `dMax=34.0` and `14_Turbine_Arch` `dMax=18.8` remain above threshold).

## 1. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task046-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
- **Centered zero-shift IoU**: `0.9073` (`>= 0.90` PASS)
- **Contact Shadow**: `Ref Y=236.9 (236.5,236.9,237.3)` vs `Cand Y=236.0 (234.8,236.2,237.7)`

## 2. Post-ACES sRGB ROI Table (`<= 15 RGB/ch` gate, `13/15 PASS`)

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
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(155.2, 135.2, 117.2)` | `4.6` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(76.5, 56.0, 37.9)` | `5.0` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(80.3, 65.7, 55.4)` | `34.0` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(90.2, 77.7, 64.9)` | `18.8` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 3. 12-Landmark Fidelity Checklist

1. Exterior champagne satin shell, forehead highlight & right-flank gradient: `PASS`
2. Front-right rounded corner pillar crest & cheek falloff: `PASS`
3. Front glass door frame, hinges & right-edge vertical handle: `PASS`
4. Lower-front tilted OLED console & dark screen bezel: `PASS`
5. Top skylight glass cutout & chamfered upper rim: `PASS`
6. Right-side inspection window & dark smoked glass tint: `PASS`
7. Warm upper amber chamber wall fading to dark lower shadow: `PASS`
8. Dark matte chamber floor tray: `PASS`
9. Horizontal X/Y steel rails & crossbeam specular contrast (`13_Steel_Rail dMax=34.0`): `FAIL`
10. Vertical Z lead-screws & dark bronze hardware separation: `PASS`
11. Anodized copper toolhead cowl & dark intake bore: `PASS`
12. Dark graphite PEI bed & high-contrast metallic turbine arch (`14_Turbine_Arch dMax=18.8`): `FAIL`

## 4. Renders & Artifacts

- `reports/task046-explorer-front.png`
- `reports/task046-explorer-left20.png`
- `reports/task046-explorer-right20.png`
- `reports/task046-explorer-elevated.png`
- `reports/task046-explorer-4view-sheet.png`
- `reports/task046-silhouette-overlay.png`
- `reports/task046-reference-candidate-contact-sheet.png`
