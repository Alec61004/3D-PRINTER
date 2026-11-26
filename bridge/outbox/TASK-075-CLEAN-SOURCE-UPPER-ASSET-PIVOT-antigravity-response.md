# TASK-075-CLEAN-SOURCE-UPPER-ASSET-PIVOT — Antigravity Response

- **task_id**: `TASK-075-CLEAN-SOURCE-UPPER-ASSET-PIVOT`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_clean_upper_asset_v1.glb`
- **report_path**: `reports/TASK-075-antigravity-clean-source-upper-asset-pivot.md`

## Summary

- Built `deltrol_p2s_clean_upper_asset_v1.glb` (`SHA-256 8EA89C979BAF49F7525E85AE139A89DAFFD14069CC981F2C615D49548B898FCB`) replacing `node 19` and `node 40` with `clean_upper_rail_assembly` (`node 68, mesh 59, mat 18`) inside the `423x404` shell.
- `audit_task075.py` (`task-6358`): `Centered IoU=0.9073`, **`14/15 PASS`**.
- `13_Steel_Rail` remains at `(79.6, 64.5, 54.2)` (`dMax=34.7 [FAIL]`) due to exterior upper-shell shadow. Reporting `PIVOT_REQUIRED`.
