---
task_id: TASK-038-HYBRID-REFERENCE-3D-EXPLORER-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T15:15:00+07:00
completed_at: 2026-11-25T14:29:00+07:00
request: Pivot after three source-mesh revisions that still cannot reproduce the single reference image closely enough as arbitrary true 3D. Prepare a transparent hybrid handoff: keep the exact supplied reference as the reference-locked hero presentation asset, and provide the best stable true-3D explorer candidate as a separate asset/mode. Do not claim the 3D model is pixel-identical to the reference. Do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_explorer_v6.glb
---

# Task 038 — Hybrid reference-locked hero + true-3D explorer pivot

Three source-mesh revisions (TASK-035/036/037) now show that one single reference image does not provide enough hidden geometry to produce a pixel-identical arbitrary-view 3D model with the current local pipeline. Continuing to tune the same mesh would repeat the failure.

Prepare an honest two-asset handoff for Codex:

1. **Reference-locked hero:** use the supplied `assets/source/printer-hero-reference-2026-11-23.png` unchanged as the exact default hero visual. Do not repaint, distort or pretend it is 3D.
2. **True-3D explorer:** deliver the best stable connected 3D model at:
   `assets/models/raw/deltrol_p2s_explorer_v6.glb`
   It must be free of wedges, detached panels, floating feet and black bake artifacts and should be used only when the user enters exploration/rotation mode.

Do not use a billboard or 2.5D facade inside the explorer GLB. Do not edit `website/src/**`; Codex will implement the mode switch.

## Evidence required

- Explorer screenshots at 1226×708: `reports/task038-explorer-front.png`, `reports/task038-explorer-left20.png`, `reports/task038-explorer-right20.png`, `reports/task038-explorer-elevated.png`.
- Composite: `reports/task038-explorer-4view-sheet.png`.
- Report: `reports/TASK-038-antigravity-hybrid-reference-3d-explorer.md`.
- Response: `bridge/outbox/TASK-038-HYBRID-REFERENCE-3D-EXPLORER-PIVOT-antigravity-response.md`.

The report must state clearly:

- the hero is the exact reference image, not a 3D reconstruction;
- the explorer is real connected geometry with required nodes `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`;
- the remaining visual differences in explorer mode.

This task is a pipeline pivot, not a PASS. Codex will audit both assets before integration.
