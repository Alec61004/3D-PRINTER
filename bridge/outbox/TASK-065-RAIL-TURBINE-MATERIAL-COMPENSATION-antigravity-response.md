# TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION — Antigravity Response

- **task_id**: `TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_explorer_v33.glb`
- **report_path**: `reports/TASK-065-antigravity-rail-turbine-material-compensation.md`

## Summary

- Built `assets/models/raw/deltrol_p2s_explorer_v33.glb` (`2923760` bytes, SHA-256 `80C1DCC21C64EC7E4CE81508B2B0656DBB3E6563E04727061301638464E052BB`) with PBR compensation on Mat `4` (`x_gantry_crossbeam`), Mat `12` (`mech_gantry_rail_bot`), and Mat `15` (`bracket_swept_arch`), preserving `v32` spotlight rig and geometry.
- `audit_task065.py` (`task-6136`): `Centered IoU=0.9073`, **`14/15 PASS`**.
- `14_Turbine_Arch` (`dMax=14.5`), `07_Right_Win_Glass` (`dMax=6.0`), `11_Glass_Skylight` (`dMax=6.6`), and `12_Chamber_Upper_C` (`dMax=12.5`) all pass.
- `13_Steel_Rail` (`dMax=34.7`) remains `FAIL` because `baseColorFactor` > 1.0 is clamped or the recessed rail receives near-zero direct light. Reporting `PIVOT_REQUIRED`.
