---
task_id: TASK-033-BASE-GEOMETRY-FIDELITY-FIX
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T13:15:00+07:00
completed_at: 2026-11-25T12:54:00+07:00
request: Revise TASK-032's reference-derived true 3D asset. Remove the visible white triangular/wedge artifact and any lower-shell gap or detached geometry, then improve front 3/4 fidelity and warm interior readability while preserving real connected geometry. Do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb
---

# Task 033 — Base geometry integrity and fidelity fix

Codex audit found real improvement in TASK-032's material/reference direction, but the evidence contains a blocking visual defect: a large white wedge/triangle protrudes from the lower-right base and the lower shell appears open or disconnected in front/right views. The candidate cannot be integrated in this state.

## Deliverable

Write the revised candidate to:

`assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb`

Keep the reference-derived true-3D pipeline. Do not revert to a billboard or 2.5D facade, and do not edit `website/src/**`.

## Required fixes

1. Remove the white wedge, stray triangles, missing faces, open seams and any detached lower-base geometry. Inspect front, left, right and elevated views specifically for these defects.
2. Keep the base, feet, console and right-side shell physically connected and aligned.
3. Improve the front 3/4 match to the reference: champagne body, dark framed smoked door, visible warm chamber, gantry/toolhead/PEI bed, correct console and rounded right post.
4. Keep the required nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

## Evidence required

- `reports/task033-front.png`
- `reports/task033-left20.png`
- `reports/task033-right20.png`
- `reports/task033-elevated.png`
- `reports/task033-4view-sheet.png`
- `reports/TASK-033-antigravity-base-geometry-fidelity-fix.md`
- `bridge/outbox/TASK-033-BASE-GEOMETRY-FIDELITY-FIX-antigravity-response.md`

All screenshots must be 1226×708. Explicitly state whether any image plane/billboard is used. If any wedge/gap remains, or the front still is not materially closer, return `REVISION_REQUIRED`; do not claim PASS from GLB validity alone.
