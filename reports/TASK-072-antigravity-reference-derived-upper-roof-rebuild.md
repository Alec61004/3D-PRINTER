# TASK-072: Reference-Derived Upper Roof Rebuild Audit (`deltrol_p2s_explorer_v40.glb`)

- **Task ID**: `TASK-072-REFERENCE-DERIVED-UPPER-ROOF-REBUILD`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v40.glb` (`2926528` bytes, SHA-256 `95EFD8D0C711EFFD6BE117AD111BA23B402A9F3C9728C8EB948DD0DA97316359`)
- **Audit Script**: `audit_task072.py` (`task-6295`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `14/15 PASS`, max channel error `34.7`

## Rebuilt Roof/Rail Manifest (`v40`)

- **Node `40` (`top_roof_glass`)**: recessed `-0.025m` in `Z` into the upper roof opening.
- **Node `68` (`upper_gantry_rail_assembly`)**, **Mesh `59`**, **Material `18` (`Upper Gantry Rail Steel PBR`)**:
  - World AABB: `x=[-0.080, -0.037]`, `y=[0.054, 0.066]`, `z=[0.123, 0.150]` (`t ≈ 1.650`).
  - Material `18`: `baseColorFactor=[0.55, 0.44, 0.36, 1.0]`, `metallicFactor=0.12`, `roughnessFactor=0.38`, zero emissive, no `KHR_materials_unlit`.

## 15-ROI Matrix (`v40`)

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

## Pivot Conclusion

- `v40` preserves `Cand bbox=(396,174,819,578)` (`Centered IoU=0.9073`) and `14/15 PASS`, but `13_Steel_Rail` remains at `(79.6, 64.5, 54.2)` (`dMax=34.7 [FAIL]`) due to the upper roof overhang shadow inside the shell envelope.
- A full new source mesh / reference-derived reconstruction is required to achieve `15/15 PASS`.

## Visual Evidence

- `reports/task072-explorer-front.png`
- `reports/task072-explorer-left20.png`
- `reports/task072-explorer-right20.png`
- `reports/task072-explorer-elevated.png`
- `reports/task072-explorer-4view-sheet.png`
- `reports/task072-reference-candidate-contact-sheet.png`
- `reports/task072-upper-roof-rebuild-diagnostic.png`
- `reports/task072-before-after.png`
- `reports/task072-silhouette-overlay.png`
