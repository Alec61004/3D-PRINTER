# TASK-063-TURBINE-SPILL-LIGHT-SEPARATION — Antigravity Response

- **task_id**: `TASK-063-TURBINE-SPILL-LIGHT-SEPARATION`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_explorer_v31.glb`
- **report_path**: `reports/TASK-063-antigravity-turbine-spill-light-separation.md`

## Summary

- Built `assets/models/raw/deltrol_p2s_explorer_v31.glb` (`2923580` bytes, SHA-256 `BD05F950F1FF8BF7C4B435F3F1F5B6D8354CE197E96DD0626050031D14CDC787`) with `chamber_upper_rail_light` (`intensity=1.75, range=0.28`) and `chamber_turbine_fill_light` (`intensity=1.65, range=0.25, pos=[0.02, -0.05, 0.11]`), without emission or `KHR_materials_unlit`.
- `audit_task063.py` (`task-6039`): `Cand bbox=(396,174,819,578)` (`423x404`), `Centered IoU=0.9073`, **`12/15 PASS`**.
- `07_Right_Win_Glass` (`dMax=14.0`) and `12_Chamber_Upper_C` (`dMax=13.7`) pass, but `11_Glass_Skylight` (`dMax=16.5`), `13_Steel_Rail` (`dMax=18.1`), and `14_Turbine_Arch` (`dMax=17.6`) fail.
- Omnidirectional `point` lights cannot satisfy both `13_Steel_Rail` / `14_Turbine_Arch` and `11_Glass_Skylight` without spill. Recommend pivoting to aimed `KHR_lights_punctual` `spot` lights.
