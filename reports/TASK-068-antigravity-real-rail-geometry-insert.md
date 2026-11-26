# TASK-068: Real 3D Rail Geometry Insert Audit (`deltrol_p2s_explorer_v36.glb`)

- **Task ID**: `TASK-068-REAL-RAIL-GEOMETRY-INSERT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v36.glb` (`2925180` bytes, SHA-256 `EE146641B5D8D915D59B501E5548733634C7D3A2284BC6A32DF48E9E8E9C0006`)
- **Audit Script**: `audit_task068.py` (`task-6212`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `14/15 PASS`, max channel error `34.7`

## Inserted Rail Geometry (`v36`)

- **Node `68` (`upper_steel_rail_bar`)**, **Mesh `59`**, **Material `18` (`Upper Steel Rail PBR`)**:
  - **World-space AABB**: `x=[-0.082, -0.036]`, `y=[0.056, 0.065]`, `z=[0.122, 0.152]` (`24` vertices, `36` indices, `t ≈ 1.650` at ROI 13).
  - **Material `18`**: `baseColorFactor=[0.75, 0.62, 0.52, 1.0]`, `metallicFactor=0.12`, `roughnessFactor=0.35`, `doubleSided=true`, zero emissive, no `KHR_materials_unlit`.

## 15-ROI Matrix (`v36`)

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

## Measured Obstruction & Next Pivot

- `upper_steel_rail_bar` (`t ≈ 1.650`) sits inside the `0.037m` gap between `top_roof_glass` (`t=1.6270`, `Smoked Glass`) and `interior_ceiling_liner` (`t=1.6640`), where `Smoked Glass` and the upper roof shadow keep ROI 13 at `(79.6, 64.5, 54.2)` (`dMax=34.7 [FAIL]`).
- **Next Pivot**: Re-model the upper roof/ceiling clearance in Blender so the steel rail sits in an unobstructed, directly lit chamber zone below `top_roof_glass`.

## Visual Evidence

- `reports/task068-explorer-front.png`
- `reports/task068-explorer-left20.png`
- `reports/task068-explorer-right20.png`
- `reports/task068-explorer-elevated.png`
- `reports/task068-explorer-4view-sheet.png`
- `reports/task068-reference-candidate-contact-sheet.png`
- `reports/task068-rail-geometry-diagnostic.png`
- `reports/task068-before-after.png`
- `reports/task068-silhouette-overlay.png`
