# TASK-065: Rail/Turbine Material Compensation Audit (`deltrol_p2s_explorer_v33.glb`)

- **Task ID**: `TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v32.glb` (`2923756` bytes, SHA-256 `76C65B927D97A8EFFEB48A58F28A4D707D40F3F81E52C3FCF0725DA2DB045D43`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Audit Script**: `audit_task065.py` (`task-6136`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `14/15 PASS`, max channel error `34.7`

## Material Compensation JSON & Primitive Mapping (`v33`)

- **Node 44 (`x_gantry_crossbeam`, mesh `41`, Mat `4` `Machined Dark Alloy`)**:
  - `baseColorFactor`: `[1.0, 0.88, 0.78, 1.0]` -> `[1.65, 1.45, 1.32, 1.0]`
  - `roughnessFactor`: `0.45` -> `0.35`
- **Node 47 (`mech_gantry_rail_bot`, mesh `43`, Mat `12` `Machined Steel Rails`)**:
  - `baseColorFactor`: `[1.0, 0.88, 0.78, 1.0]` -> `[1.75, 1.52, 1.38, 1.0]`
  - `roughnessFactor`: `0.45` -> `0.35`
- **Node 57 (`bracket_swept_arch`, mesh `52`, Mat `15` `Sculpted Metallic Turbine Arch`)**:
  - `baseColorFactor`: `[1.0, 0.86, 0.74, 1.0]` -> `[1.28, 1.08, 0.92, 1.0]`
  - `roughnessFactor`: `0.45` -> `0.38`
- Preserved `v32` `KHR_lights_punctual` `spot` rig, geometry, zero emissive, and no `KHR_materials_unlit`.

## 15-ROI Matrix (`v33`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(57.8, 42.9, 30.9)` | `6.0` | `PASS` |
| `08_Right_Flank_Bot` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(157.1, 137.2, 118.2)` | `6.6` | `PASS` |
| `12_Chamber_Upper_C` | `(88.2, 70.4, 50.6)` | `12.5` | `PASS` |
| `13_Steel_Rail` | `(79.6, 64.5, 54.2)` | `34.7` | `FAIL` |
| `14_Turbine_Arch` | `(94.5, 81.6, 67.2)` | `14.5` | `PASS` |
| `15_Chamber_Floor` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## Findings & Pivot

- **14/15 PASS achieved**: `14_Turbine_Arch` (`dMax=14.5`), `07_Right_Win_Glass` (`dMax=6.0`), `11_Glass_Skylight` (`dMax=6.6`), and `12_Chamber_Upper_C` (`dMax=12.5`) all pass.
- **Remaining blocker**: `13_Steel_Rail` moved only `+0.8` (`78.8 -> 79.6`, `dMax=34.7 [FAIL]`) because `baseColorFactor` > 1.0 is clamped or the recessed rail receives near-zero direct light from the `spot` rig.

## Visual Evidence

- `reports/task065-explorer-front.png`
- `reports/task065-explorer-left20.png`
- `reports/task065-explorer-right20.png`
- `reports/task065-explorer-elevated.png`
- `reports/task065-explorer-4view-sheet.png`
- `reports/task065-reference-candidate-contact-sheet.png`
- `reports/task065-material-compensation-diagnostic.png`
- `reports/task065-before-after.png`
- `reports/task065-silhouette-overlay.png`
