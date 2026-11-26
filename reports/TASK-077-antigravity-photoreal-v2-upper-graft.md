# TASK-077: `photoreal_v2` Upper Mechanical Graft Audit

- **Task ID**: `TASK-077-PHOTOREAL-V2-UPPER-GRAFT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Result GLB**: `assets/models/raw/deltrol_p2s_photoreal_v2_upper_graft.glb` (`2925288` bytes, SHA-256 `BF3239D2C21E0DE96443962B08DD9B5183D6B120720BDA0290BEBEB71073B657`)
- **Audit Script**: `audit_task077.py` (`task-6408`)
- **Fixture Metrics**:
  - `Cand bbox=(396,174,819,578)` (`423x404`, `W/H=1.0470`)
  - `Centered IoU=0.8976` (below `0.90` gate)
  - **ROI Pass Rate**: `13/15 PASS`, max channel error `34.7`

## Conclusion

- Grafting `photoreal_v2` `door_top_rail` (`mesh 38`) into `v33` dropped `Centered IoU` to `0.8976` and broke `02_Forehead_C` (`dMax=24.9 [FAIL]`) while `13_Steel_Rail` remained at `dMax=34.7 [FAIL]`. Reporting `PIVOT_REQUIRED`.

## Evidence

- `reports/task077-explorer-front.png`, `left20`, `right20`, `elevated`, `4view-sheet`
- `reports/task077-reference-candidate-contact-sheet.png`
- `reports/task077-upper-graft-diagnostic.png`
- `reports/task077-source-node-map.md`
- `reports/task077-before-after.png`
- `reports/task077-silhouette-overlay.png`
