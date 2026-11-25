---
task_id: TASK-036-SOURCE-MESH-REFERENCE-CALIBRATION
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T14:15:00+07:00
completed_at: 2026-11-25T14:14:00+07:00
request: Revise the TASK-035 Blender/source-geometry true-3D model for strict reference fidelity. Keep the connected hard-surface mesh, but make the front read as the reference's closed smoked-glass printer with darker champagne/titanium finish, correct front 3/4 proportions, warm dense chamber, side panel, top enclosure, console and handle. Do not use image planes/billboards/2.5D and do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev1.glb
---

# Task 036 — Source mesh reference calibration

Codex audit finds TASK-035 structurally promising but visually wrong in the front hero: pale/overexposed body, open-looking front aperture instead of a closed smoked-glass door, generic CAD interior, and mismatched silhouette/console proportions.

Reference:

`assets/source/printer-hero-reference-2026-11-23.png`

## Required changes

1. Keep the Blender/source true-3D geometry; no front-facing photo plane, billboard, facade quad or 2.5D depth-rig.
2. Make the front door a clearly attached closed smoked-glass door with the reference-like dark frame, diagonal reflection behavior and visible right-side handle. It must remain attached in all views.
3. Darken/calibrate the exterior to the reference's champagne/titanium studio finish; avoid white/overexposed plastic/CAD appearance.
4. Match the reference front 3/4 silhouette: rounded front-right post, correct side depth and top enclosure, lower console position/shape, feet and base.
5. Increase the readable warm interior detail: rails, toolhead, PEI bed, printed object and warm chamber light, while retaining real geometry.
6. Preserve required nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

## Deliverable/evidence

- Candidate: `assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev1.glb`
- Screenshots: `reports/task036-front.png`, `reports/task036-left20.png`, `reports/task036-right20.png`, `reports/task036-elevated.png`, `reports/task036-4view-sheet.png`.
- Report: `reports/TASK-036-antigravity-source-mesh-reference-calibration.md`.
- Response: `bridge/outbox/TASK-036-SOURCE-MESH-REFERENCE-CALIBRATION-antigravity-response.md`.

All screenshots must be 1226×708. Explicitly state whether image planes are used. If the front still looks open/generic or is materially behind the reference, report `REVISION_REQUIRED`; do not claim PASS from mesh validity alone.
