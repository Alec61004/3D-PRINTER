# TASK-076: Legacy Source Asset Bake-Off Audit

- **Task ID**: `TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Selected Bake-Off Artifact**: `assets/models/raw/deltrol_p2s_legacy-source-bakeoff.glb` (copy of `deltrol_p2s_true3d_candidate_v3.glb`, `898956` bytes, SHA-256 `667BFA398CF760C774C9C05BA2FA73C06DDCBDA6A8B0BE551ADAEF9489A6BE7E`)

## Bake-Off Conclusion

- None of the 4 existing legacy source GLBs (`deltrol_p2s_source.glb`, `deltrol_p2s_photoreal_v2.glb`, `deltrol_p2s_true3d_candidate_v3.glb`, `deltrol_p2s_optimized.glb`) is viable as a better starting point than `v33` (`Centered IoU=0.9073`, `14/15 PASS`):
  - `deltrol_p2s_true3d_candidate_v3.glb` has the highest legacy IoU (`0.8364`), but only `2/15 PASS` and `13_Steel_Rail dMax=57.1 [FAIL]`.
  - `deltrol_p2s_optimized.glb` has `IoU=0.7066`, `2/15 PASS`, `max channel error=203.1`.
  - `deltrol_p2s_photoreal_v2.glb` has `IoU=0.7674`, `2/15 PASS`, `13_Steel_Rail dMax=24.3 [FAIL]`.
  - `deltrol_p2s_source.glb` has `IoU=0.6711`, `1/15 PASS`, `13_Steel_Rail dMax=90.2 [FAIL]`.
- **Next Pivot**: An external CAD/photogrammetry/multi-view 3D reconstruction source asset (outside the current legacy GLB pool) is required.

## Evidence

- `reports/task076-source-bakeoff-sheet.png`
- `reports/task076-source-bakeoff-metrics.md`
- `reports/task076-selected-front.png`
- `reports/task076-selected-left20.png`
- `reports/task076-selected-right20.png`
- `reports/task076-selected-elevated.png`
- `reports/task076-selected-4view-sheet.png`
- `reports/task076-reference-candidate-contact-sheet.png`
- `reports/task076-before-after.png`
- `reports/task076-silhouette-overlay.png`
