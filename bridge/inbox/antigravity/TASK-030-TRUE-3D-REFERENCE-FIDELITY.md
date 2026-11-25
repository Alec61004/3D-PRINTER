---
task_id: TASK-030-TRUE-3D-REFERENCE-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T12:30:00+07:00
completed_at: 2026-11-25T12:24:00+07:00
request: Revise the TASK-029 true connected mesh so its front 3/4 appearance matches the supplied printer reference much more closely while preserving real connected geometry at every viewing angle. Do not return to billboard/2.5D construction and do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_true3d_candidate_v2.glb
---

# Task 030 — True 3D reference-fidelity revision

Codex audit confirms that TASK-029 solved the detached-panel failure with real connected geometry, but the result is still far from the reference: it looks like a beige CAD box and does not match the reference's proportions, champagne-metal material, dark framed glass door, side panel, top enclosure, interior gantry, console and photoreal detail.

## Deliverable

Create the revised candidate at:

`assets/models/raw/deltrol_p2s_true3d_candidate_v2.glb`

Use the reference:

`assets/source/printer-hero-reference-2026-11-23.png`

Keep the mesh genuinely 3D. You may use Blender or another local/free pipeline, procedural/material textures, and the existing TASK-029 mesh as a starting point. Do not use a single front-facing photo plane, billboard, or depth-rig as the primary body. Do not edit `website/src/**`.

## Fidelity priorities

1. Match the reference front 3/4 silhouette and framing first: overall width/height/depth, rounded champagne-metal enclosure, top and side structure, dark framed glass door, bottom console and feet.
2. Match the reference material hierarchy: satin champagne/titanium body, dark smoked glass, dark interior, warm interior light, gold PEI bed, visible CoreXY gantry and printed object.
3. Keep all major parts physically attached and aligned when viewed from front, ~20° left, ~20° right and elevated angle. No floating panel, detached base, disconnected feet or giant rectangular facade may appear.
4. Preserve/emit the required contract nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

## Evidence required

- Fresh 1226×708 screenshots under `reports/task030-front.png`, `reports/task030-left20.png`, `reports/task030-right20.png`, and `reports/task030-elevated.png`.
- A composite under `reports/task030-4view-sheet.png`.
- Detailed report at `reports/TASK-030-antigravity-true-3d-reference-fidelity.md`.
- Handoff response at `bridge/outbox/TASK-030-TRUE-3D-REFERENCE-FIDELITY-antigravity-response.md`.
- Explicitly state whether any image plane is used. If the result is still materially 2.5D or the reference fidelity remains low, use `verdict: REVISION_REQUIRED`; do not claim PASS from GLB validity or loadability alone.
