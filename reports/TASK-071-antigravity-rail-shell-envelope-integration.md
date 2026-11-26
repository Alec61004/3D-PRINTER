# TASK-071: Rail/Shell Envelope Integration Audit (`deltrol_p2s_explorer_v39.glb`)

- **Task ID**: `TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v39.glb` (`2926496` bytes, SHA-256 `6785F8BDC8D83B5CBBA8DB7D28F18388C6009824B38AF34DC5498EEEA780F300`)
- **Audit Script**: `audit_task071.py` (`task-6274`)
- **Fixture Metrics**:
  - `Cand bbox=(396,167,819,578)` (`423x411`, `W/H=1.0292`, `dW=-0.70%`, `dH=+0.49%`)
  - `Centered IoU=0.9126` (gate `>= 0.90`)
  - **ROI Pass Rate**: `11/15 PASS`, max channel error `20.1`

## Compact Rail & Shell-Envelope Measurements (`v39`)

- **Node `68` (`upper_gantry_rail_assembly`)**, **Mesh `59`**, **Material `18` (`Upper Gantry Rail Steel PBR`)**:
  - Compact world AABB at `t=1.600`: `x=[-0.052, -0.011]`, `y=[0.060, 0.070]`, `z=[0.163, 0.187]`.
  - Material `18`: `baseColorFactor=[0.55, 0.44, 0.36, 1.0]`, `metallicFactor=0.12`, `roughnessFactor=0.38`, zero emissive, no `KHR_materials_unlit`.

## 15-ROI Matrix (`v39`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | `(228.9, 225.7, 218.5)` | `4.1` | `PASS` |
| `02_Forehead_C` | `(151.5, 144.2, 133.7)` | `3.3` | `PASS` |
| `03_Forehead_R` | `(83.7, 74.9, 65.0)` | `16.2` | `FAIL` |
| `04_Pillar_Crest` | `(141.0, 130.7, 118.6)` | `4.7` | `PASS` |
| `05_Pillar_Cheek` | `(61.6, 51.4, 41.0)` | `5.8` | `PASS` |
| `06_Right_Flank_Top` | `(51.1, 42.6, 31.7)` | `2.9` | `PASS` |
| `07_Right_Win_Glass` | `(58.1, 43.4, 31.4)` | `5.6` | `PASS` |
| `08_Right_Flank_Bot` | `(64.8, 56.3, 45.8)` | `18.9` | `FAIL` |
| `09_Chin_Left` | `(110.6, 98.4, 82.6)` | `2.2` | `PASS` |
| `10_Console_Display` | `(50.0, 42.1, 33.5)` | `4.9` | `PASS` |
| `11_Glass_Skylight` | `(153.4, 132.5, 112.9)` | `1.9` | `PASS` |
| `12_Chamber_Upper_C` | `(95.4, 76.2, 56.3)` | `19.5` | `FAIL` |
| `13_Steel_Rail` | `(130.7, 113.4, 97.5)` | `20.1` | `FAIL` |
| `14_Turbine_Arch` | `(98.2, 84.9, 70.1)` | `10.8` | `PASS` |
| `15_Chamber_Floor` | `(20.4, 16.2, 12.0)` | `7.3` | `PASS` |

## Measured Conflict & Next Pivot

- Any depth `t < 1.6270` along ROI 13's ray protrudes outside the current exterior shell contour (`Cand bbox` top edge shifts `174 -> 167`, `+7px`), breaking `03_Forehead_R`, `08_Right_Flank_Bot`, and `12_Chamber_Upper_C`; any depth `t > 1.6270` is occluded by `top_roof_glass` (`Smoked Glass`).
- **Next Pivot**: New source mesh / reference-derived reconstruction of the upper roof & chamber opening so the rail sits inside the shell envelope without colliding with `top_roof_glass`.

## Visual Evidence

- `reports/task071-explorer-front.png`
- `reports/task071-explorer-left20.png`
- `reports/task071-explorer-right20.png`
- `reports/task071-explorer-elevated.png`
- `reports/task071-explorer-4view-sheet.png`
- `reports/task071-reference-candidate-contact-sheet.png`
- `reports/task071-rail-shell-fit-diagnostic.png`
- `reports/task071-before-after.png`
- `reports/task071-silhouette-overlay.png`
