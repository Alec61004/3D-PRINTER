---
task_id: TASK-042-FRESH-REFERENCE-DERIVED-MESH-PIVOT
owner: antigravity
status: pending
created_at: 2026-11-25T20:00:00+07:00
request: Retire the procedural v7-v9 construction family and rebuild a fresh photoreal true-3D Deltrol P2S mesh/material asset from the supplied reference crop. Continue until the fixed front fidelity gate passes; do not reuse the same generic box recipe.
result_path: assets/models/raw/deltrol_p2s_explorer_v10.glb
---

# Mandatory context

Read:

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-041-codex-review.md`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `reports/ref_printer_box.png`

# Pivot reason

The v7-v9 procedural/reference-baked family has now had three iterations. V9 passes framing and centered IoU (`0.9154`) but still looks like a generic CAD box rather than the supplied product image. Only 6/15 photometric ROIs pass and the largest errors are the pillar/cheek, chamber mid, toolhead, front glass and shell lighting. Do not make another small tint/alpha or camera-only revision of v9.

# New approach

Build `assets/models/raw/deltrol_p2s_explorer_v10.glb` from a fresh reference-derived reconstruction. It must be a real connected 3D asset, but it may use a materially different Blender/equivalent modeling and material workflow than v9. Start from the reference crop's product-specific exterior proportions and value hierarchy rather than copying v9's generic shell recipe.

The front view must visibly match the reference before adding exploration details:

1. Product-specific closed enclosure silhouette: light champagne forehead, tapered top-to-side transition, dominant rounded front-right pillar, slim left edge, correct lower corner arches/base.
2. Closed smoked glass door with a spatially varying neutral smoke/reflection treatment; readable warm interior, not a uniform brown/black pane and not an open-frame appearance.
3. Reference-like photographic material response: dark-but-not-black right side, darker cheek than forehead, warm amber chamber with controlled falloff, readable rails/toolhead/bed/object, compact dark console.
4. Correct placement and scale of handle, hinges, printhead, rails, bed, printed object and console.
5. No image plane, billboard, 2.5D rig, detached facade, floating parts, white wedge, black bake triangle, open seam or z-fighting.

# Fixed audit and acceptance

Use the unchanged audit viewer fixture: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`. Produce fresh `front`, `left20`, `right20`, `elevated (+18°)` screenshots and an overlay with the reference.

The front must pass every hard gate in `reports/reference-fidelity-criteria.md`:

- bbox target `425×408`, ratio `1.042` within tolerance;
- centered, zero-shift silhouette IoU ≥ `0.90`;
- all 12 landmarks PASS;
- every key photometric ROI ≤15 RGB/channel mean error;
- no visible contour or artifact mismatch.

# Required handoff

- `assets/models/raw/deltrol_p2s_explorer_v10.glb`
- `reports/TASK-042-antigravity-fresh-reference-derived-mesh-pivot.md`
- `reports/task042-explorer-front.png`
- `reports/task042-explorer-left20.png`
- `reports/task042-explorer-right20.png`
- `reports/task042-explorer-elevated.png`
- `reports/task042-explorer-4view-sheet.png`
- `reports/task042-silhouette-overlay.png`
- `bridge/outbox/TASK-042-FRESH-REFERENCE-DERIVED-MESH-PIVOT-antigravity-response.md`

Include GLB validation, SHA-256, centered bbox/IoU, the 12-landmark matrix, all 15 ROI values, and honest remaining deltas. Do not edit `website/src`; Codex audits the artifact before integration.
