# TASK-067: Rail Primitive Identification Pivot Audit (`deltrol_p2s_explorer_v35.glb`)

- **Task ID**: `TASK-067-RAIL-PRIMITIVE-IDENTIFICATION-PIVOT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v35.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Audit Script**: `audit_task067.py` (`task-6188`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `14/15 PASS`, max channel error `34.7`

## ROI 13 `(493,300)-(518,305)` Object-ID & Depth Raycast

Exact ray-triangle intersection at the mandated fixture camera (`1226x708`, FOV `27°`, `eye=[0.86, 0.22, 1.50]`, `target=[0, -0.01, 0]`):

- **Pixel `(495, 302)`**:
  1. `t=1.6345`: `node=40 (top_roof_glass)`, `mesh=38`, `prim=0`, `mat=2 (Smoked Glass)`
  2. `t=1.6716`: `node=19 (interior_ceiling_liner)`, `mesh=18`, `prim=0`, `mat=5 (Warm Chamber Anodized Interior)`
  3. `t=1.8129`: `node=22 (interior_rear_electronics_box)`, `mesh=21`, `prim=0`, `mat=4 (Machined Dark Alloy)`
- **Pixel `(505, 302)`**:
  1. `t=1.6270`: `node=40 (top_roof_glass)`, `mesh=38`, `prim=0`, `mat=2 (Smoked Glass)`
  2. `t=1.6640`: `node=19 (interior_ceiling_liner)`, `mesh=18`, `prim=0`, `mat=5 (Warm Chamber Anodized Interior)`
  3. `t=1.8310`: `node=22 (interior_rear_electronics_box)`, `mesh=21`, `prim=0`, `mat=4 (Machined Dark Alloy)`
- **Pixel `(515, 302)`**:
  1. `t=1.6196`: `node=40 (top_roof_glass)`, `mesh=38`, `prim=0`, `mat=2 (Smoked Glass)`
  2. `t=1.6564`: `node=19 (interior_ceiling_liner)`, `mesh=18`, `prim=0`, `mat=5 (Warm Chamber Anodized Interior)`
  3. `t=1.8923`: `node=21 (interior_left_back_baffle)`, `mesh=20`, `prim=0`, `mat=5 (Warm Chamber Anodized Interior)`

**Proven Owner**: ROI 13 is **not** a steel rail surface—there is no rail mesh at `(493, 300)-(518, 305)`. The pixels hit `top_roof_glass` (`node=40, mat=2`) over `interior_ceiling_liner` (`node=19, mat=5`).

## 15-ROI Matrix (`v35`)

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

## Next Real-Geometry Pivot

Add/position a real 3D mechanical steel rail mesh (with its own isolated warm steel PBR material) under `top_roof_glass` at the world-space coordinates intersecting ROI 13 `(493, 300)-(518, 305)` (`t ≈ 1.66`), rather than editing `x_gantry_crossbeam` / `mech_gantry_rail_bot` or `interior_ceiling_liner`.

## Visual Evidence

- `reports/task067-explorer-front.png`
- `reports/task067-explorer-left20.png`
- `reports/task067-explorer-right20.png`
- `reports/task067-explorer-elevated.png`
- `reports/task067-explorer-4view-sheet.png`
- `reports/task067-reference-candidate-contact-sheet.png`
- `reports/task067-rail-object-id-diagnostic.png`
- `reports/task067-before-after.png`
- `reports/task067-silhouette-overlay.png`
