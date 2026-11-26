# TASK-066-RAIL-ONLY-CALIBRATION — Antigravity Response

- **task_id**: `TASK-066-RAIL-ONLY-CALIBRATION`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_explorer_v34.glb`
- **report_path**: `reports/TASK-066-antigravity-rail-only-calibration.md`

## Summary

- Built `assets/models/raw/deltrol_p2s_explorer_v34.glb` (`2923472` bytes, SHA-256 `8765521C0C69E13F83A6059DD66B71DDEE886A09AD43ADCDF3BF1A3D26C29B6A`) with `KHR_materials_unlit` on Mat `4` (`x_gantry_crossbeam`) and Mat `12` (`mech_gantry_rail_bot`).
- `audit_task066.py` (`task-6157`): `Centered IoU=0.9073`, `13/15 PASS`.
- `07_Right_Win_Glass` regressed from `dMax=6.0` (`v33`) to `dMax=43.6 [FAIL]` because the right window views Mat `4`/`12`, while `13_Steel_Rail` stayed at `dMax=37.9 [FAIL]`. Reporting `PIVOT_REQUIRED`.
