---
task_id: TASK-041-PRODUCT-SILHOUETTE-LIGHTING-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T19:45:00+07:00
completed_at: 2026-11-25T19:35:00+07:00
request: Correct the remaining product silhouette and reference lighting/material mismatch. Pivot away from simply tinting the v8 pane; deliver a photoreal true-3D candidate that passes the fixed front gate.
result_path: assets/models/raw/deltrol_p2s_explorer_v9.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-040-codex-review.md`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v8.glb`

# Why another revision is required

V8 improved the closed-door reading, but Codex audit still rejects it. The centered silhouette IoU is `0.8986` (< `0.90`), the top/right shell form is too generic and flat, and 9/15 photometric regions remain outside the ≤15 RGB/channel gate. Do not claim success from GLB validity, node count, rotation, or bbox alone.

# Required pivot

Produce `assets/models/raw/deltrol_p2s_explorer_v9.glb` as real connected 3D geometry. This must be a geometry-and-lighting correction, not another uniform alpha/tint pass:

1. Rebuild or materially reshape the top cap, front-right rounded pillar, right-side depth and lower corner arches to follow the reference contour at the fixed camera.
2. Keep a genuinely closed smoked front door, but use a spatially varying glass treatment: dark frame/edge, readable warm chamber, and visible printhead/bed/object without a uniformly brown overlay.
3. Rebalance the studio lighting/material response so the reference's light forehead, darker cheek/right flank, warm interior, and controlled side reflection are reproduced without inverting the pillar/flank relationship.
4. Preserve the compact low centered console, attached handle/hinges, integrated base/feet and all required logical nodes.
5. Do not use a photo plane, billboard, 2.5D rig, detached facade, camera cheating, or website changes.

# Fixed acceptance evidence

Use `tools/true3d_audit_viewer.html` unchanged: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`. Produce fresh `front`, `left20`, `right20`, `elevated (+18°)` images and a reference/candidate overlay.

The front must meet all of these:

- bbox `425×408`, ratio `1.042`, tolerance ±3% and ±0.03;
- centered (zero-shift) silhouette IoU ≥ `0.90`;
- all 12 landmarks PASS;
- every key photometric ROI ≤15 RGB/channel mean error;
- no visible top/right/bottom contour mismatch or visual artifact.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v9.glb`
- `reports/TASK-041-antigravity-product-silhouette-lighting-pivot.md`
- `reports/task041-explorer-front.png`
- `reports/task041-explorer-left20.png`
- `reports/task041-explorer-right20.png`
- `reports/task041-explorer-elevated.png`
- `reports/task041-explorer-4view-sheet.png`
- `reports/task041-silhouette-overlay.png`
- `bridge/outbox/TASK-041-PRODUCT-SILHOUETTE-LIGHTING-PIVOT-antigravity-response.md`

Include GLB validation, SHA-256, centered bbox/IoU, the 12-landmark matrix, and all 15 ROI values with honest PASS/FAIL. Codex decides final acceptance after independently viewing the evidence.
