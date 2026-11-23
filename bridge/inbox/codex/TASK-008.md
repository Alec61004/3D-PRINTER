---
task_id: TASK-008
parent_task_id: TASK-007
stage_id: STAGE-008
owner: codex
reviewer: antigravity
status: completed
implementation_completed_at: 2026-11-19T21:56:10+07:00
summary: Printer animation and accessible controls implemented and browser-tested; awaiting Antigravity visual/UI review before STAGE-008 completion.
completed_at: 2026-11-19T22:04:00+07:00
review_result: APPROVED
created_by: coordinator
created_at: 2026-11-19T21:46:49+07:00
request: Implement the printer animation stage using the optimized GLB and the existing Deltrol viewer.
result_path: website/
glb_path: assets/models/optimized/deltrol_p2s_optimized.glb
report_path: reports/task-008-printer-animation.md
response_path: bridge/outbox/TASK-008-codex-response.md
review_request_path: bridge/inbox/antigravity/TASK-008-REVIEW.md
next_stage_on_completion: STAGE-009
---

# TASK-008 — PRINTER_ANIMATION

Add a technically legible printer animation to the existing Deltrol website viewer.
Use the optimized GLB at:

`assets/models/optimized/deltrol_p2s_optimized.glb`

Do not replace the approved website visual direction or the optimized source model.

## Required animation behavior

- Animate a believable print cycle with a clear idle state.
- Move `printHead` through a bounded XY path above the bed.
- Animate `printBed` or its carriage with a constrained Z progression.
- Keep `gantryX` and `gantryY` motion mechanically coherent with the toolhead.
- Keep `enclosure` and `door` stable during the cycle.
- Keep `printedObject` visually consistent as the print result.
- Add accessible play/pause and reset animation controls.
- Preserve rotate, zoom, pan, reset camera, auto-rotate, loading, and error behavior.
- Respect reduced-motion preferences where practical.
- Keep desktop/mobile layout responsive.

## Completion requirements

1. Implement and test the animation in `website/`.
2. Verify the optimized GLB still loads successfully.
3. Verify play/pause/reset animation controls and camera controls.
4. Write `reports/task-008-printer-animation.md` with evidence and limitations.
5. Write the normal Codex response to `bridge/outbox/TASK-008-codex-response.md`.
6. Create `bridge/inbox/antigravity/TASK-008-REVIEW.md` for visual/UI review through the
   existing bridge and Doop workflow.
7. Do not create TASK-009 manually; the coordinator advances one stage only after the
   Antigravity review returns `APPROVED`.
8. Do not mark the project `DONE`; STAGE-009 final QA is mandatory.
