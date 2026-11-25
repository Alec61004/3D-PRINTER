---
task_id: TASK-032-ASSET-PIPELINE-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T13:00:00+07:00
completed_at: 2026-11-25T12:46:00+07:00
request: Pivot away from the TASK-029/030/031 primitive procedural mesh method. Build a new reference-derived true 3D asset using a different local/free method (multi-view reconstruction, Blender hard-surface reconstruction, or a materially better existing free asset with reference-derived surface maps). The result must be a connected rotatable printer and must match the supplied reference much more closely in the front 3/4 view. Do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_asset_pivot_v4.glb
---

# Task 032 — Asset/construction pipeline pivot

Codex audit has reached the three-revision limit for the current primitive/procedural unibody method. TASK-029, TASK-030 and TASK-031 are technically connected 3D, but the front result remains a generic dark/beige box and does not approach the photoreal reference. Do not continue the same builder with another shader/camera/light tweak.

## Required pivot

Use a materially different construction approach, for example:

- reference-derived multi-view reconstruction followed by mesh cleanup;
- Blender hard-surface reconstruction from the reference with curved/chamfered enclosure surfaces and reference-derived material maps;
- a substantially better free/local source mesh adapted to the reference.

The result must be real connected geometry. Surface textures may be used on real mesh surfaces, but do not use a front-facing photo plane, billboard, or 2.5D depth-rig as the body or silhouette.

Reference:

`assets/source/printer-hero-reference-2026-11-23.png`

## Deliverable and evidence

- Candidate: `assets/models/raw/deltrol_p2s_asset_pivot_v4.glb`
- Screenshots at 1226×708: `reports/task032-front.png`, `reports/task032-left20.png`, `reports/task032-right20.png`, `reports/task032-elevated.png`.
- Composite: `reports/task032-4view-sheet.png`.
- Report: `reports/TASK-032-antigravity-asset-pipeline-pivot.md`.
- Response: `bridge/outbox/TASK-032-ASSET-PIPELINE-PIVOT-antigravity-response.md`.

## Acceptance bar

1. Front 3/4 must visibly resemble the reference: champagne/titanium enclosure, rounded front-right post, correct side depth and top, framed smoked door with visible handle, warm readable chamber, gantry/toolhead/PEI bed, console and feet.
2. All parts remain physically attached in the three rotated/elevated views; no detached panel/base/feet.
3. Preserve the required nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
4. State explicitly whether any image plane is used. If the new method still produces a generic box or is not materially closer, report `REVISION_REQUIRED`/`BLOCKED` and explain the next pivot; do not claim PASS from GLB loadability.
