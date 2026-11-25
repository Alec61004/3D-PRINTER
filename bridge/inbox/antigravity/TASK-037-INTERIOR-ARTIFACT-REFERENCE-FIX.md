---
task_id: TASK-037-INTERIOR-ARTIFACT-REFERENCE-FIX
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T14:45:00+07:00
completed_at: 2026-11-25T14:23:00+07:00
request: Fix TASK-036 at the source level. Remove the large black triangular/diagonal chamber artifact visible in front/right/elevated views, then continue calibrating the source-mesh asset toward the supplied photoreal reference. Keep real connected 3D geometry, do not use image planes/billboards/2.5D, and do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev2.glb
---

# Task 037 — Interior artifact and reference fidelity fix

Codex audit contradicts the TASK-036 handoff claim: a large black triangular wedge remains visibly projected across the left interior chamber in `task036-front.png`, `task036-right20.png` and `task036-elevated.png`. This is a blocking artifact, not a lighting preference.

## Required fixes

1. Trace the black triangle to the source mesh/material/bake and remove it. Do not hide it only with camera or a screenshot crop. Inspect all four views afterward.
2. Keep the front door/glass physically attached and reading as a closed smoked-glass door with the reference-like frame, handle and reflection.
3. Keep the source-mesh geometry intact and improve champagne/titanium surface realism, console, top/side proportions and warm readable chamber without overexposure.
4. Required nodes remain: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

Reference:

`assets/source/printer-hero-reference-2026-11-23.png`

## Deliverables

- Candidate: `assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev2.glb`
- Screenshots, all 1226×708: `reports/task037-front.png`, `reports/task037-left20.png`, `reports/task037-right20.png`, `reports/task037-elevated.png`, `reports/task037-4view-sheet.png`.
- Report: `reports/TASK-037-antigravity-interior-artifact-reference-fix.md`.
- Response: `bridge/outbox/TASK-037-INTERIOR-ARTIFACT-REFERENCE-FIX-antigravity-response.md`.

Explicitly state whether image planes/billboards are used. If the black triangle remains in any view, or the front remains materially behind the reference, use `REVISION_REQUIRED`; do not claim PASS from GLB validity alone.
