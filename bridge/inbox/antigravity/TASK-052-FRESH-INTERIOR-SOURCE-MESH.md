---
task_id: TASK-052-FRESH-INTERIOR-SOURCE-MESH
owner: antigravity
status: pending
created_at: 2026-11-26T09:30:00+07:00
request: >-
  Pivot after TASK-051. The v19 report violates the no-emission contract
  (rail/gantry/turbine emissive_scale=1.0), the upper rail ROI still fails at
  dMax=33.4, and the direct before/after is nearly unchanged. Build a fresh
  source interior mesh/material assembly, not a copy of v19, that matches the
  reference's dark warm upper rails, compact toolhead and lower printed turbine
  while preserving the accepted exterior shell and right-window glass.
result_path: assets/models/raw/deltrol_p2s_explorer_v20.glb
---

# TASK-052 — Fresh interior source-mesh pivot

## Owner boundary

Antigravity owns the new interior visual/mesh/material asset. Do not edit
Codex-owned website source. Use the fixed fixture and reference criteria.

## Non-negotiable implementation rules

1. Build a new interior source assembly. Do not duplicate v19 and only change
   material constants. The visible rails, gantry carriage/toolhead and turbine
   arch must be newly constructed or sourced from a different mesh method.
2. Keep it true 3D: no billboard, image plane, camera-facing card, projected
   screenshot or 2.5D replacement.
3. For every rail, gantry and turbine material, GLB JSON must contain no emissive
   factor/texture contribution. The report must show the exact material JSON
   fields and prove emissive is zero/absent. Do not use emission to force ROI
   colors.
4. Use dark warm bronze/steel albedo with viewer-driven highlights. The upper
   rails must be visibly darker and more contrasty than the pale v19 gantry.
5. Preserve the accepted outer shell, front-right pillar, door/handle, console,
   camera framing and the v19 right-window glass result.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v20.glb`
- `reports/task052-explorer-front.png`
- `reports/task052-explorer-left20.png`
- `reports/task052-explorer-right20.png`
- `reports/task052-explorer-elevated.png`
- `reports/task052-explorer-4view-sheet.png`
- `reports/task052-reference-candidate-contact-sheet.png`
- `reports/task052-interior-before-after.png`
- `reports/task052-silhouette-overlay.png`
- `reports/TASK-052-antigravity-fresh-interior-source-mesh.md`
- `bridge/outbox/TASK-052-FRESH-INTERIOR-SOURCE-MESH-antigravity-response.md`

The report must include:

- exact node/mesh/primitive/material mapping;
- the GLB material JSON excerpt or machine-readable proof for rail/turbine
  emissive absence/zero;
- a before/after crop with clearly changed rail pixels;
- fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation;
- honest verdict based on the direct contact sheet.

## Acceptance gates

- steel rail ROI target near `(114,93,80)`, `dMax <= 15`;
- turbine ROI target near `(109,88,73)`, `dMax <= 15`;
- right-window glass remains `dMax <= 15`;
- centered IoU `>= 0.90` and exterior silhouette retained;
- direct screenshot must show a dark, warm, mechanically readable upper assembly;
- no emissive rail/turbine materials in the actual GLB.

If the fresh source mesh does not materially improve the direct image, mark
`PIVOT_REQUIRED` and name the next source-asset strategy. Do not repeat v19.
