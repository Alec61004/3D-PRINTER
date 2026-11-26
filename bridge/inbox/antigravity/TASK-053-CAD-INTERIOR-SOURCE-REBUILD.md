---
task_id: TASK-053-CAD-INTERIOR-SOURCE-REBUILD
owner: antigravity
status: pending
created_at: 2026-11-26T09:40:00+07:00
request: >-
  Pivot away from the procedural interior family v12-v20. TASK-052 proved the
  no-emissive materials but still failed visually: rail dMax=35.1, turbine
  dMax=20.4 and right-window glass dMax=26.0. Build a fresh CAD/Blender-style
  true-3D interior source mesh with reference-matched proportions for the
  upper rails/gantry/toolhead and lower bed/turbine. Preserve the accepted outer
  shell and glass silhouette.
result_path: assets/models/raw/deltrol_p2s_explorer_v21.glb
---

# TASK-053 — CAD interior source rebuild

## Owner boundary

Antigravity owns the new visual/mesh/material source. Do not edit Codex-owned
website source. Read the fixed fixture and reference criteria before rendering.

## Required pivot

This must be a genuinely new interior source mesh built in Blender/CAD-style
geometry or an equivalent clean modeling workflow. Do not copy the procedural
interior nodes or textures from v20 and adjust shaders. The outer shell may be
reused only if it remains the accepted silhouette.

Model the visible reference proportions:

- three compact horizontal rails/rods across the upper chamber;
- a smaller central carriage/toolhead with the dark round intake and warm metal
  face in the reference position;
- two vertical lead screws/supports with correct spacing and thickness;
- a low dark bed with the printed metallic turbine/arch object matching the
  reference's position, width and height;
- a dark rear panel and warm chamber gradient that separates the assembly through
  the front glass.

## Hard constraints

- true connected 3D geometry only; no billboard, image plane, projected screenshot
  or camera-facing card;
- rail/turbine materials must have no emissive factor or emissive texture;
- keep right-window glass close to the accepted v19 result and do not darken it;
- preserve exterior shell, pillar, door/handle, console, camera and bbox framing.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v21.glb`
- `reports/task053-explorer-front.png`
- `reports/task053-explorer-left20.png`
- `reports/task053-explorer-right20.png`
- `reports/task053-explorer-elevated.png`
- `reports/task053-explorer-4view-sheet.png`
- `reports/task053-reference-candidate-contact-sheet.png`
- `reports/task053-interior-before-after.png`
- `reports/task053-silhouette-overlay.png`
- `reports/TASK-053-antigravity-cad-interior-source-rebuild.md`
- `bridge/outbox/TASK-053-CAD-INTERIOR-SOURCE-REBUILD-antigravity-response.md`

The report must include:

- source method and what was newly modeled;
- exact node/mesh/primitive/material mapping;
- GLB JSON proof that rail/turbine materials have no emissive contribution;
- fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation;
- a direct before/after crop that visibly proves the upper interior changed.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90` and exterior silhouette retained;
- direct contact sheet must show the reference-like dark warm mechanical hierarchy,
  not the pale generic gantry seen in v20.

If this fresh source mesh still does not materially improve the direct image,
report `PIVOT_REQUIRED` and identify a different external/source-asset strategy;
do not repeat the v20 procedural construction.
