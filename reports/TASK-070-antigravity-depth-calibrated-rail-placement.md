# TASK-070: Depth-Calibrated Rail Placement Audit (`deltrol_p2s_explorer_v38.glb`)

- **Task ID**: `TASK-070-DEPTH-CALIBRATED-RAIL-PLACEMENT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v38.glb` (`2926496` bytes, SHA-256 `AAF00EED0A8475832A9D40DD67726FF17F0A22F8A5840533388F61FBD63AA412`)
- **Audit Script**: `audit_task070.py` (`task-6253`)
- **Fixture Metrics**:
  - `Cand bbox=(396,155,819,578)` (`423x423`, `W/H=1.0000`, `dW=-0.70%`, `dH=+3.42%`)
  - `Centered IoU=0.9114` (gate `>= 0.90`)
  - **ROI Pass Rate**: `10/15 PASS`, max channel error `206.2`

## Depth-Calibrated Rail Placement (`v38`)

- **Node `68` (`upper_gantry_rail_assembly`)**, **Mesh `59`**, **Material `18` (`Upper Gantry Rail Steel PBR`)**:
  - Placed at `t=1.600` (in front of `top_roof_glass` `t=1.6270`): world AABB `x=[-0.060, -0.010]`, `y=[0.059, 0.078]`, `z=[0.161, 0.199]`.
  - Material `18`: `baseColorFactor=[0.55, 0.44, 0.36, 1.0]`, `metallicFactor=0.12`, `roughnessFactor=0.38`, zero emissive, no `KHR_materials_unlit`.

## 15-ROI Matrix (`v38`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | `(234.0, 231.3, 225.2)` | `4.2` | `PASS` |
| `02_Forehead_C` | `(214.1, 211.0, 207.0)` | `74.3` | `FAIL` |
| `03_Forehead_R` | `(255.0, 255.0, 255.0)` | `206.2` | `FAIL` |
| `04_Pillar_Crest` | `(141.0, 130.8, 118.7)` | `4.7` | `PASS` |
| `05_Pillar_Cheek` | `(61.8, 51.6, 41.2)` | `5.6` | `PASS` |
| `06_Right_Flank_Top` | `(48.9, 40.4, 30.3)` | `5.1` | `PASS` |
| `07_Right_Win_Glass` | `(59.0, 44.3, 32.4)` | `4.7` | `PASS` |
| `08_Right_Flank_Bot` | `(49.5, 44.1, 37.9)` | `34.2` | `FAIL` |
| `09_Chin_Left` | `(110.9, 98.7, 82.8)` | `1.9` | `PASS` |
| `10_Console_Display` | `(49.4, 41.0, 31.8)` | `5.5` | `PASS` |
| `11_Glass_Skylight` | `(142.8, 119.2, 97.5)` | `16.8` | `FAIL` |
| `12_Chamber_Upper_C` | `(103.6, 87.7, 72.5)` | `29.7` | `FAIL` |
| `13_Steel_Rail` | `(124.5, 102.8, 85.6)` | `10.2` | `PASS` |
| `14_Turbine_Arch` | `(107.2, 96.5, 84.3)` | `11.6` | `PASS` |
| `15_Chamber_Floor` | `(20.1, 16.1, 12.0)` | `7.5` | `PASS` |

## Measured Conflict & Pivot

- Placing the rail at `t=1.600` (`z=[0.161, 0.199]`) in front of `top_roof_glass` (`t=1.6270`) **passes `13_Steel_Rail`** (`dMax=10.2 [PASS]`), but `z=0.199` protrudes outside the exterior shell envelope, expanding `Cand bbox` height from `404` to `423` (`dH=+3.42%`) and shifting `02_Forehead_C`, `03_Forehead_R`, `08_Right_Flank_Bot`, `11_Glass_Skylight`, and `12_Chamber_Upper_C` to `FAIL`.
- **Next Pivot**: Rebuild the upper roof/chamber source mesh in Blender so `top_roof_glass` sits recessed/higher and the rail fits inside the shell envelope without protruding.

## Visual Evidence

- `reports/task070-explorer-front.png`
- `reports/task070-explorer-left20.png`
- `reports/task070-explorer-right20.png`
- `reports/task070-explorer-elevated.png`
- `reports/task070-explorer-4view-sheet.png`
- `reports/task070-reference-candidate-contact-sheet.png`
- `reports/task070-rail-depth-diagnostic.png`
- `reports/task070-before-after.png`
- `reports/task070-silhouette-overlay.png`
