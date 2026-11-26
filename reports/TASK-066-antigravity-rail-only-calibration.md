# TASK-066: Rail-Only Calibration Audit (`deltrol_p2s_explorer_v34.glb`)

- **Task ID**: `TASK-066-RAIL-ONLY-CALIBRATION`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v34.glb` (`2923472` bytes, SHA-256 `8765521C0C69E13F83A6059DD66B71DDEE886A09AD43ADCDF3BF1A3D26C29B6A`)
- **Audit Script**: `audit_task066.py` (`task-6157`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `13/15 PASS`, max channel error `43.6`

## Rail Material JSON (`v34`)

- Added `KHR_materials_unlit` to `extensionsUsed` and to Mat `4` (`Machined Dark Alloy` on `x_gantry_crossbeam`, node `44`) and Mat `12` (`Machined Steel Rails` on `mech_gantry_rail_bot`, node `47`):
  - `extensions`: `{"KHR_materials_unlit": {}}`
  - `pbrMetallicRoughness`: `{"baseColorFactor": [0.36, 0.24, 0.18, 1.0], "metallicFactor": 0.0, "roughnessFactor": 0.9}`
  - Zero emissive factor/texture.

## 15-ROI Matrix (`v34`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(105.0, 89.0, 76.0)` | `43.6` | `FAIL` |
| `08_Right_Flank_Bot` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(144.6, 123.1, 105.4)` | `8.9` | `PASS` |
| `12_Chamber_Upper_C` | `(69.5, 55.3, 45.6)` | `6.4` | `PASS` |
| `13_Steel_Rail` | `(76.4, 59.5, 47.7)` | `37.9` | `FAIL` |
| `14_Turbine_Arch` | `(94.5, 81.6, 67.2)` | `14.5` | `PASS` |
| `15_Chamber_Floor` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## Findings & Pivot

- Applying `KHR_materials_unlit` to Mat `4` (`x_gantry_crossbeam`) and Mat `12` (`mech_gantry_rail_bot`) **broke `07_Right_Win_Glass`** (`dMax=6.0 -> 43.6 [FAIL]`) because the right-window glass looks directly onto those meshes.
- Simultaneously, `13_Steel_Rail` did **not** brighten (`79.6 -> 76.4`, `dMax=37.9 [FAIL]`), proving that `ROI 13` (`CandBox=(493, 300, 518, 305)`) is not driven by Mat `4`/`12` alone.

## Visual Evidence

- `reports/task066-explorer-front.png`
- `reports/task066-explorer-left20.png`
- `reports/task066-explorer-right20.png`
- `reports/task066-explorer-elevated.png`
- `reports/task066-explorer-4view-sheet.png`
- `reports/task066-reference-candidate-contact-sheet.png`
- `reports/task066-rail-material-diagnostic.png`
- `reports/task066-before-after.png`
- `reports/task066-silhouette-overlay.png`
