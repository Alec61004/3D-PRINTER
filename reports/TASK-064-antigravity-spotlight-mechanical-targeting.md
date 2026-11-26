# TASK-064: Spotlight Mechanical Targeting Audit (`deltrol_p2s_explorer_v32.glb`)

- **Task ID**: `TASK-064-SPOTLIGHT-MECHANICAL-TARGETING`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Base GLB**: `assets/models/raw/deltrol_p2s_explorer_v31.glb` (`2923580` bytes, SHA-256 `BD05F950F1FF8BF7C4B435F3F1F5B6D8354CE197E96DD0626050031D14CDC787`)
- **Result GLB**: `assets/models/raw/deltrol_p2s_explorer_v32.glb` (`2923756` bytes, SHA-256 `76C65B927D97A8EFFEB48A58F28A4D707D40F3F81E52C3FCF0725DA2DB045D43`)
- **Audit Script**: `audit_task064.py` (`task-6105`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`, `dW=-0.70%`, `dH=-1.22%`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `13/15 PASS`, max channel error `35.5`

## `KHR_lights_punctual` Rig (`v32`)

- `chamber_upper_rail_light` (node `66`): `type="spot"`, `pos=[-0.04, 0.08, 0.14]`, `dir=[0, 0, -1]`, `rot=[0.0, 0.0, 0.0, 1.0]`, `color=[1.0, 0.82, 0.62]`, `intensity=12.0`, `range=0.25`, `innerConeAngle=0.25`, `outerConeAngle=0.50`
- `chamber_turbine_fill_light` (node `67`): `type="spot"`, `pos=[0.02, -0.05, 0.11]`, `tgt=[0.0, -0.06, 0.02]`, `rot=[-0.054319, 0.108637, 0.0, 0.992596]`, `color=[1.0, 0.80, 0.58]`, `intensity=13.5`, `range=0.25`, `innerConeAngle=0.28`, `outerConeAngle=0.55`
- Zero emissive materials and no `KHR_materials_unlit`.

## 15-ROI Matrix (`v32`)

| ROI | Cand RGB | dMax | Result |
| --- | --- | --- | --- |
| `01_Forehead_L` | `(226.3, 222.8, 215.4)` | `7.1` | `PASS` |
| `02_Forehead_C` | `(150.4, 143.0, 132.4)` | `2.1` | `PASS` |
| `03_Forehead_R` | `(70.0, 60.7, 50.0)` | `1.2` | `PASS` |
| `04_Pillar_Crest` | `(140.8, 130.5, 118.4)` | `5.0` | `PASS` |
| `05_Pillar_Cheek` | `(61.4, 51.2, 40.7)` | `6.0` | `PASS` |
| `06_Right_Flank_Top` | `(51.5, 43.0, 32.0)` | `2.6` | `PASS` |
| `07_Right_Win_Glass` | `(49.4, 37.4, 27.5)` | `14.3` | `PASS` |
| `08_Right_Flank_Bot` | `(80.2, 68.6, 53.8)` | `3.5` | `PASS` |
| `09_Chin_Left` | `(110.5, 98.3, 82.4)` | `2.4` | `PASS` |
| `10_Console_Display` | `(51.7, 43.9, 35.6)` | `3.2` | `PASS` |
| `11_Glass_Skylight` | `(155.1, 133.6, 113.8)` | `3.0` | `PASS` |
| `12_Chamber_Upper_C` | `(84.6, 62.3, 40.5)` | `8.7` | `PASS` |
| `13_Steel_Rail` | `(78.8, 64.1, 54.0)` | `35.5` | `FAIL` |
| `14_Turbine_Arch` | `(93.2, 80.0, 65.5)` | `15.8` | `FAIL` |
| `15_Chamber_Floor` | `(20.5, 16.3, 12.0)` | `7.2` | `PASS` |

## Findings & Pivot Limitation

- **Spill eliminated**: Switching from `point` (`v31`) to `spot` (`v32`) dropped `11_Glass_Skylight` from `dMax=16.5 [FAIL]` to `dMax=3.0 [PASS]`, and `12_Chamber_Upper_C` from `13.7` to `8.7 [PASS]`, while keeping `07_Right_Win_Glass` at `14.3 [PASS]`.
- **Measured cone/lighting limitation**: `13_Steel_Rail` remained invariant at `(78.8, 64.1, 54.0)` (`dMax=35.5`) across spot intensities `2.4`, `6.5`, and `12.0` (and `z=0.08..0.14`), and `14_Turbine_Arch` saturated at `dMax=15.8` (`intensity=13.5`). Narrow-cone `KHR_lights_punctual` `spot` lights cannot illuminate the recessed/grazing-angle `13_Steel_Rail` surface to `dMax <= 15`.
- **Recommendation (`PIVOT_REQUIRED`)**: Pivot to adjusting the base PBR albedo/metallic/roughness of `13_Steel_Rail` and `14_Turbine_Arch` (or adding subtle local IBL/reflection) rather than relying solely on `KHR_lights_punctual` spot intensity.

## Visual Evidence

- `reports/task064-explorer-front.png`
- `reports/task064-explorer-left20.png`
- `reports/task064-explorer-right20.png`
- `reports/task064-explorer-elevated.png`
- `reports/task064-explorer-4view-sheet.png`
- `reports/task064-reference-candidate-contact-sheet.png`
- `reports/task064-spotlight-diagnostic.png`
- `reports/task064-light-before-after.png`
- `reports/task064-silhouette-overlay.png`
