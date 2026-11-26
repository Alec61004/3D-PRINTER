---
task_id: TASK-046-RAIL-TURBINE-CONTRAST-FINAL
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T08:40:45+07:00
---

# TASK-046 Antigravity Response

- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v14.glb` (`3262824` bytes, SHA-256 `DA59578C7CB2365E7DE3ACC5799616FF8741187F188FB76754DD2C8FC5E85DFF`, `64` nodes, `56` meshes).
- **Fixed-fixture framing**: `423x404`, `Centered IoU = 0.9073` (`>= 0.90`).
- **Photometric ROIs**: `13/15 PASS` (`01..12` + `15` within `1.2–7.2 RGB/ch`). `13_Steel_Rail` (`dMax=34.0`) and `14_Turbine_Arch` (`dMax=18.8`) remain `FAIL`.
- **Report**: `reports/TASK-046-antigravity-rail-turbine-contrast-final.md`
- **Renders**: `reports/task046-explorer-{front,left20,right20,elevated,4view-sheet}.png`, `reports/task046-silhouette-overlay.png`, `reports/task046-reference-candidate-contact-sheet.png`.
