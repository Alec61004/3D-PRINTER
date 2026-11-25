---
task_id: TASK-029-TRUE-3D-MESH-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T00:00:00+07:00
completed_at: 2026-11-25T12:15:00+07:00
request: Pivot away from the current 2.5D billboard/depth-rig asset. Deliver a genuinely rotatable 3D printer mesh or a materially more complete Blender/equivalent reconstruction that keeps the enclosure, door, glass, base and feet physically connected from multiple viewing angles. Do not edit website source files. Use the reference at assets/source/printer-hero-reference-2026-11-23.png and do not use paid services.
result_path: assets/models/raw/deltrol_p2s_true3d_candidate.glb
---

# Task 029 — True 3D mesh pivot

The current `deltrol_p2s_photoreal_2p5d_depth.glb` is not acceptable as a 3D asset: it is a textured facade with thin depth geometry. When the camera rotates, a large front panel and the base/feet detach from the printer. The latest screenshots are direct evidence of this failure.

## Deliverable

Create a new candidate at:

`assets/models/raw/deltrol_p2s_true3d_candidate.glb`

You may use Blender or another local/free pipeline and may reuse the source/reference assets, but the primary silhouette must be real connected geometry. Do not replace the problem with another billboard or a single front-facing image plane.

## Acceptance evidence required

1. Keep the front 3/4 composition close to the reference.
2. Produce fresh screenshots at 1226x708 for: front reference angle, ~20° left, ~20° right, and a slightly elevated angle. Save them under `reports/task029-*.png`.
3. In every view, the door/panel must stay attached to the enclosure, the base and feet must stay attached/aligned, and no large rectangular image plane may protrude from the body.
4. Validate the GLB structure and list node/mesh/material counts in the report. The report must explicitly state whether the result is true geometry or still 2.5D.
5. If the target cannot be met with this method, set `verdict: REVISION_REQUIRED` or `verdict: BLOCKED` and explain the pivot needed. Do not claim PASS from build/load success alone.

Write the detailed report to:

`reports/TASK-029-antigravity-true-3d-mesh-pivot.md`

Write the handoff response to:

`bridge/outbox/TASK-029-TRUE-3D-MESH-PIVOT-antigravity-response.md`

Do not modify `website/src/**`; Codex will integrate and audit the candidate after handoff.
