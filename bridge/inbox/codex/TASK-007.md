---
task_id: TASK-007
parent_task_id: TASK-006
stage_id: STAGE-007
owner: codex
reviewer: antigravity
status: completed
implementation_completed_at: 2026-11-19T21:34:02+07:00
summary: Website viewer implementation and local build verification completed; awaiting Antigravity visual/UI review before STAGE-007 completion.
completed_at: 2026-11-19T21:46:00+07:00
review_result: APPROVED
created_by: coordinator
created_at: 2026-11-19T21:23:49+07:00
request: Implement the real Deltrol website 3D viewer using the optimized GLB and existing Deltrol design.
result_path: website/
glb_path: assets/models/optimized/deltrol_p2s_optimized.glb
report_path: reports/task-007-web-3d-viewer.md
response_path: bridge/outbox/TASK-007-codex-response.md
review_request_path: bridge/inbox/antigravity/TASK-007-REVIEW.md
next_stage_on_completion: STAGE-008
---

# TASK-007 — WEB_3D_VIEWER

Implement the real Deltrol website 3D viewer in `website/`, using React, React Three
Fiber, and Three.js. Load:

`assets/models/optimized/deltrol_p2s_optimized.glb`

## Required viewer behavior

- Rotate/orbit the printer.
- Zoom.
- Pan.
- Reset camera.
- Auto-rotate toggle.
- Lighting and shadows.
- Loading state.
- Error fallback when the GLB cannot load.
- Responsive desktop and mobile layout.
- Integrate the viewer into the existing Deltrol visual direction; do not replace the
  approved visual reference assets.

## Completion requirements

1. Build the website successfully with the selected local package tooling.
2. Verify the optimized GLB loads in the viewer.
3. Verify every listed camera control works.
4. Verify responsive behavior at desktop and mobile viewport sizes.
5. Write `reports/task-007-web-3d-viewer.md` with build and interaction evidence.
6. Write the normal Codex response to `bridge/outbox/TASK-007-codex-response.md`.
7. Create `bridge/inbox/antigravity/TASK-007-REVIEW.md` requesting visual/UI review through the existing bridge and Doop workflow. Include the local website path, screenshots or preview evidence, and explicit APPROVED/REVISION_REQUIRED response requirements.
8. Do not advance to STAGE-008 until Antigravity has returned its review response.
9. Do not mark the project `DONE`; STAGE-008 and STAGE-009 remain mandatory.
