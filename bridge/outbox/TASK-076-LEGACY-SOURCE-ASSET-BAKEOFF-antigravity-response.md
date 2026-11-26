# TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF — Antigravity Response

- **task_id**: `TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF`
- **status**: `completed`
- **verdict**: `PIVOT_REQUIRED`
- **result_path**: `assets/models/raw/deltrol_p2s_legacy-source-bakeoff.glb`
- **report_path**: `reports/TASK-076-antigravity-legacy-source-asset-bakeoff.md`

## Summary

- Ran fixed-fixture bake-off on `deltrol_p2s_source.glb` (`0.6711 IoU, 1/15`), `deltrol_p2s_photoreal_v2.glb` (`0.7674 IoU, 2/15`), `deltrol_p2s_true3d_candidate_v3.glb` (`0.8364 IoU, 2/15`), and `deltrol_p2s_optimized.glb` (`0.7066 IoU, 2/15`).
- None of the legacy sources is viable compared to `v33` (`0.9073 IoU, 14/15`). Reporting `PIVOT_REQUIRED` for an external source/reconstruction asset.
