---
task_id: TASK-048-DEBUG-REFERENCE-PROJECTION
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T08:49:15+07:00
---

# TASK-048 Antigravity Response

- **Candidate GLB**: `assets/models/raw/deltrol_p2s_explorer_v16.glb` (`3374784` bytes, SHA-256 `7A2B456F3423DB677E336436DCDAD65052AED215CB09ACEFDE95C590A29FD3A2`).
- **Fixed-fixture framing**: `423x404`, `Centered IoU = 0.9073` (`>= 0.90`).
- **Photometric ROIs**: `13/15 PASS` (`01..12` + `15` within `1.2–7.2 RGB/ch`). `13_Steel_Rail` (`dMax=33.9`) and `14_Turbine_Arch` (`dMax=18.7`) remain `FAIL`.
- **Report**: `reports/TASK-048-antigravity-debug-reference-projection.md`
- **Diagnostic**: `reports/task048-projection-diagnostic.png`
- **Renders**: `reports/task048-explorer-{front,left20,right20,elevated,4view-sheet}.png`, `reports/task048-silhouette-overlay.png`, `reports/task048-reference-candidate-contact-sheet.png`.
