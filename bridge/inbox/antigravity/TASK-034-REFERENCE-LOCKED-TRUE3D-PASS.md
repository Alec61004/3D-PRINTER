---
task_id: TASK-034-REFERENCE-LOCKED-TRUE3D-PASS
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T13:30:00+07:00
completed_at: 2026-11-25T13:03:00+07:00
request: Continue from TASK-033. Keep the clean connected true-3D geometry and improve the candidate's front 3/4 visual match to the supplied reference until it is genuinely presentation-ready. Increase warm interior readability, reflective smoked-glass behavior, champagne/titanium material realism, and reference-correct proportions/detail for the top, door frame/handle, console, feet, gantry, toolhead, PEI bed and printed object. Do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_asset_pivot_v4_rev2.glb
---

# Task 034 — Reference-locked true-3D fidelity pass

TASK-033 fixed the white wedge and lower-shell gap, but Codex audit still finds the model too dark/generic compared with `assets/source/printer-hero-reference-2026-11-23.png`. This is not a geometry-validity task only; the front 3/4 image must become convincingly close to the reference while preserving stable real geometry.

## Deliverable

Write:

`assets/models/raw/deltrol_p2s_asset_pivot_v4_rev2.glb`

Do not use a billboard, front-facing photo plane or 2.5D depth rig. Use textures only on real mesh surfaces. Do not edit `website/src/**`.

## Required visual changes

1. Make the warm chamber, gantry, print head, PEI bed and printed object clearly readable through the smoked door without turning the door into a flat image.
2. Match the reference's champagne/titanium highlights and dark graphite/glass contrast; remove the generic brown/CAD appearance.
3. Refine the front 3/4 silhouette and proportions: upper enclosure, rounded front-right post, side depth, framed door and handle, lower console and feet.
4. Preserve the fix from TASK-033: no white wedge, background bleed, open seam, detached shell or floating foot in any view.

## Required evidence

- `reports/task034-front.png`
- `reports/task034-left20.png`
- `reports/task034-right20.png`
- `reports/task034-elevated.png`
- `reports/task034-4view-sheet.png`
- `reports/TASK-034-antigravity-reference-locked-true3d-pass.md`
- `bridge/outbox/TASK-034-REFERENCE-LOCKED-TRUE3D-PASS-antigravity-response.md`

All screenshots must be 1226×708. Explicitly state whether any image plane/billboard is used. Report `REVISION_REQUIRED` if visual fidelity is still materially behind the reference; do not claim PASS from GLB loadability or connected nodes alone.
