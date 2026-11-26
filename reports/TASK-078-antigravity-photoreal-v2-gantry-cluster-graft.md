# TASK-078: `photoreal_v2` Gantry Cluster Graft Audit

- **Task ID**: `TASK-078-PHOTOREAL-V2-GANTRY-CLUSTER-GRAFT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Result GLB**: `assets/models/raw/deltrol_p2s_photoreal_v2_gantry_cluster.glb` (`2998156` bytes, SHA-256 `56946AB76E773CCBDDBAD85B9614A9172C7E465EADDDBDE59BA4E0A7DFEC2373`)
- **Audit Script**: `audit_task078.py` (`task-6430`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`)
  - `Centered IoU=0.9073` (gate `>= 0.90`)
  - **ROI Pass Rate**: `13/15 PASS`, max channel error `34.7`

## Conclusion

- Grafting `photoreal_v2` gantry cluster (`meshes 49..65, 69..72`) into `v33` preserved `Centered IoU=0.9073`, but `12_Chamber_Upper_C` regressed to `dMax=15.5 [FAIL]` and `13_Steel_Rail` remained at `dMax=34.7 [FAIL]`. Reporting `PIVOT_REQUIRED`.

## Evidence

- `reports/task078-explorer-front.png`, `left20`, `right20`, `elevated`, `4view-sheet`
- `reports/task078-reference-candidate-contact-sheet.png`
- `reports/task078-gantry-cluster-diagnostic.png`
- `reports/task078-source-node-map.md`
- `reports/task078-before-after.png`
- `reports/task078-silhouette-overlay.png`
