# TASK-051 Antigravity Interior Mechanics Reference Rebuild (`deltrol_p2s_explorer_v19.glb`)

- **Task**: `TASK-051-INTERIOR-MECHANICS-REFERENCE-REBUILD`
- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v19.glb`
- **Size / SHA-256**: `3485916` bytes / `2144C1586105D66BAD9E00F6DC09FE70960A98DAFE09200D105A2665B5E232AC`
- **Verdict**: `PIVOT_REQUIRED` (`13/15 PASS`, `07_Right_Win_Glass` restored to `dMax=5.5`, `14_Turbine_Arch` improved to `dMax=15.8`, `13_Steel_Rail` at `dMax=33.4`).

## 1. Exact Node / Mesh / Primitive / Material Assignments

- `x_gantry_crossbeam`, `toolhead_chassis`, `toolhead_fan_rotor`, `toolhead_hotend_sock` -> material `4` (`Machined Dark Alloy`, `metallic=0.30, emissive_scale=1.0`)
- `bracket_swept_arch` -> material `14` (`Sculpted Metallic Turbine Arch`, `metallic=0.35, emissive_scale=1.0`)
- `toolhead_front_cowl` -> material `16` (`Anodized Copper Toolhead`, `metallic=0.35, emissive_scale=1.0`)
- `toolhead_nozzle` -> material `17` (`Brass Nozzle`)
- Horizontal & vertical rails -> material `12` (`Machined Steel Rails`, `metallic=0.35, emissive_scale=1.0`)
- Bed -> material `13` (`Dark Graphite PEI Bed`)
- Glass -> material `2` (`Smoked Glass`), material `3` (`Ref Glass Specular Sheen`), material `10` (`Right Glass Warm Sheen`)

## 2. Fixed-Fixture Silhouette & BBox Audit (`1226x708`, `FOV 27°`, `[0.86, 0.22, 1.50]`, `[0, -0.01, 0]`, ACES `1.05`)

- **Before/After Crop**: `reports/task051-interior-before-after.png` (`REF` vs `v18` vs `v19`).
- **Ref bbox (`ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
- **Cand bbox (`task051-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423, H=404, W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`)
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
| `07_Right_Win_Glass` | `(63.7, 45.4, 32.6)` | `(59.4, 41.5, 27.0)` | `5.5` | `PASS` |
| `08_Right_Flank_Bot` | `(83.7, 70.1, 52.0)` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(112.8, 100.5, 84.0)` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(54.9, 46.3, 35.3)` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(153.2, 130.6, 114.3)` | `(156.7, 137.5, 119.8)` | `6.9` | `PASS` |
| `12_Chamber_Upper_C` | `(75.9, 58.0, 42.9)` | `(83.2, 64.3, 45.5)` | `7.3` | `PASS` |
| `13_Steel_Rail` | `(114.3, 93.3, 80.4)` | `(80.9, 66.4, 56.2)` | `33.4` | `FAIL` |
| `14_Turbine_Arch` | `(109.0, 88.1, 72.7)` | `(93.2, 80.9, 68.1)` | `15.8` | `FAIL` |
| `15_Chamber_Floor` | `(27.7, 23.2, 16.9)` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## 4. 12-Landmark Fidelity Checklist

1. Exterior champagne satin shell, forehead highlight & right-flank gradient: `PASS`
2. Front-right rounded corner pillar crest & cheek falloff: `PASS`
3. Front glass door frame, hinges & right-edge vertical handle: `PASS`
4. Lower-front tilted OLED console & dark screen bezel: `PASS`
5. Top skylight glass cutout & chamfered upper rim: `PASS`
6. Right-side inspection window & dark smoked glass tint: `PASS`
7. Warm upper amber chamber wall fading to dark lower shadow: `PASS`
8. Dark matte chamber floor tray: `PASS`
9. Horizontal X/Y steel rails & crossbeam specular contrast (`13_Steel_Rail dMax=33.4`): `FAIL`
10. Vertical Z lead-screws & dark bronze hardware separation: `PASS`
11. Anodized copper toolhead cowl & dark intake bore: `PASS`
12. Dark graphite PEI bed & high-contrast metallic turbine arch (`14_Turbine_Arch dMax=15.8`): `FAIL`

## 5. Renders & Artifacts

- `reports/task051-explorer-front.png`
- `reports/task051-explorer-left20.png`
- `reports/task051-explorer-right20.png`
- `reports/task051-explorer-elevated.png`
- `reports/task051-explorer-4view-sheet.png`
- `reports/task051-silhouette-overlay.png`
- `reports/task051-reference-candidate-contact-sheet.png`
- `reports/task051-interior-before-after.png`
