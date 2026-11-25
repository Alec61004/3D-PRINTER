---
task_id: TASK-031-TRUE-3D-PHOTOREAL-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T12:45:00+07:00
completed_at: 2026-11-25T12:32:00+07:00
request: Continue from TASK-030. Keep the connected true-3D mesh, but make the front 3/4 result visually match the supplied printer reference: photoreal champagne enclosure, framed smoked glass door with visible warm chamber, correct asymmetric side depth, console, feet, gantry, print head, PEI bed and printed object. Do not use a billboard, a front-facing photo plane or a 2.5D depth rig, and do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb
---

# Task 031 — Reference-locked photoreal true-3D fidelity

Codex audit of TASK-030 confirms that the mesh stays connected, but it still looks like a generic beige CAD enclosure and is not close enough to the supplied reference for the hero. The next revision must improve the actual visual match, not just node counts or geometric complexity.

Reference:

`assets/source/printer-hero-reference-2026-11-23.png`

## Deliverable

Write the candidate to:

`assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb`

Keep the model as true connected geometry. Use local/free Blender or procedural methods and texture maps only on real surfaces. Do not create a single image plane, billboard, facade quad, or depth-rig substitute for the printer body. Do not edit `website/src/**`.

## Non-negotiable visual targets

1. Front 3/4 silhouette must match the reference's narrow champagne frame, rounded front-right post, asymmetric right side depth, sloped/rounded top and lower base/feet.
2. The front door must read as a framed smoked-glass door attached to the body, with the right-side vertical handle visible and the warm chamber/gantry visible through it.
3. Match the reference material hierarchy and lighting: satin champagne/titanium exterior, dark graphite frame, warm interior, reflective glass, gold PEI bed, detailed CoreXY rails/toolhead and visible printed object.
4. Keep all parts physically attached at front, ~20° left, ~20° right and elevated views. No protruding rectangular panel, detached base or floating foot.

## Evidence required

- Fresh 1226×708 screenshots: `reports/task031-front.png`, `reports/task031-left20.png`, `reports/task031-right20.png`, `reports/task031-elevated.png`.
- Composite: `reports/task031-4view-sheet.png`.
- Detailed report: `reports/TASK-031-antigravity-true-3d-photoreal-fidelity.md`.
- Handoff response: `bridge/outbox/TASK-031-TRUE-3D-PHOTOREAL-FIDELITY-antigravity-response.md`.
- Explicitly state that no image plane/billboard/2.5D facade is used. If the front view remains visibly generic or materially different from the reference, report `REVISION_REQUIRED` and explain the remaining gap; do not claim PASS from build/load success.
