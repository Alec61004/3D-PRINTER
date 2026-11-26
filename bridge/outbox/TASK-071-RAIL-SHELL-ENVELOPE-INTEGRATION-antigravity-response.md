# TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION — Antigravity Response

- **task_id**: `TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_explorer_v39.glb`
- **report_path**: `reports/TASK-071-antigravity-rail-shell-envelope-integration.md`

## Summary

- Built `v39` (`SHA-256 6785F8BDC8D83B5CBBA8DB7D28F18388C6009824B38AF34DC5498EEEA780F300`) with compact `upper_gantry_rail_assembly` at `t=1.600` (`z=[0.163, 0.187]`).
- `audit_task071.py` (`task-6274`): `Centered IoU=0.9126`, `11/15 PASS`.
- Even the compact rail at `t=1.600` shifts `Cand bbox` top edge `174 -> 167` (`+7px`), breaking ROIs `03, 08, 12`. Reporting `PIVOT_REQUIRED` for a new source mesh / reference-derived upper roof reconstruction.
