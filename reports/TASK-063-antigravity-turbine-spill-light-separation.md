# TASK-063: Turbine & Spill Light Separation Audit (`deltrol_p2s_explorer_v31.glb`)

- **Task ID**: `TASK-063-TURBINE-SPILL-LIGHT-SEPARATION`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v31.glb`
  - **Size**: `2923580` bytes
  - **SHA-256**: `BD05F950F1FF8BF7C4B435F3F1F5B6D8354CE197E96DD0626050031D14CDC787`
- **Audit Script**: `audit_task063.py` (`task-6039`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`)
  - `Centered IoU=0.9073`
  - **ROI Pass Rate**: `12/15 PASS`

## `KHR_lights_punctual` Rig (`v31`)

- `chamber_upper_rail_light`: `type=point`, `intensity=1.75`, `range=0.28`
- `chamber_turbine_fill_light`: `type=point`, `intensity=1.65`, `range=0.25`, `pos=[0.02, -0.05, 0.11]`
- No emission or `KHR_materials_unlit` added.

## 15-ROI Matrix (`v31`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | - | `7.1` | `PASS` |
| `02_Forehead_C` | - | `2.1` | `PASS` |
| `03_Forehead_R` | - | `1.2` | `PASS` |
| `04_Pillar_Crest` | - | `5.0` | `PASS` |
| `05_Pillar_Cheek` | - | `6.0` | `PASS` |
| `06_Right_Flank_Top` | - | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(49.7, 37.7, 27.6)` | `14.0` | `PASS` |
| `08_Right_Flank_Bot` | - | `3.5` | `PASS` |
| `09_Chin_Left` | - | `2.4` | `PASS` |
| `10_Console_Display` | - | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(164.6, 147.1, 130.2)` | `16.5` | `FAIL` |
| `12_Chamber_Upper_C` | `(89.6, 67.7, 45.7)` | `13.7` | `PASS` |
| `13_Steel_Rail` | `(96.2, 79.6, 66.6)` | `18.1` | `FAIL` |
| `14_Turbine_Arch` | `(91.4, 77.7, 63.4)` | `17.6` | `FAIL` |
| `15_Chamber_Floor` | - | `7.2` | `PASS` |

## Findings & Pivot Proposal

Omnidirectional `point` lights in `KHR_lights_punctual` have an irreducible spill tradeoff:
- Raising `chamber_upper_rail_light` enough to pass `13_Steel_Rail` (`dMax <= 15`) pushes `11_Glass_Skylight` above `15` (`19.0` in `v30`).
- Lowering it to reduce skylight spill drops `13_Steel_Rail` (`dMax=18.1` in `v31`) while `11_Glass_Skylight` remains at `dMax=16.5` and `14_Turbine_Arch` at `dMax=17.6`.

**Recommendation (`PIVOT_REQUIRED`)**: Pivot from omnidirectional `point` lights to directional `spot` lights in `KHR_lights_punctual` aimed directly at `13_Steel_Rail` and `14_Turbine_Arch` with tight cone angles (`innerConeAngle` / `outerConeAngle`) so the rail and turbine receive sufficient illumination without spilling onto `11_Glass_Skylight` or `07_Right_Win_Glass`.

## Visual Evidence

- `reports/task063-front.png`
- `reports/task063-left20.png`
- `reports/task063-right20.png`
- `reports/task063-elevated.png`
- `reports/task063-4view-sheet.png`
- `reports/task063-silhouette-overlay.png`
- `reports/task063-reference-candidate-contact-sheet.png`
- `reports/task063-light-before-after.png`
- `reports/task063-spill-separation-diagnostic.png`
