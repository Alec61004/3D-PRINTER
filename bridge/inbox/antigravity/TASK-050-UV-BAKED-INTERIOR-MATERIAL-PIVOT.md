---
task_id: TASK-050-UV-BAKED-INTERIOR-MATERIAL-PIVOT
owner: antigravity
status: pending
created_at: 2026-11-26T09:10:00+07:00
request: >-
  Pivot the Deltrol P2S interior material pipeline after TASK-049. The v12-v17
  emission-baked/high-metallicity projection family is retired because v16 and
  v17 produced nearly identical rail/turbine pixels. Build a new true-3D
  candidate with clean UV-unwrapped interior gantry/rails/turbine materials,
  low metallic response and Cycles-baked base-color/roughness maps so the fixed
  viewer lighting produces the reference's dark warm metallic contrast.
result_path: assets/models/raw/deltrol_p2s_explorer_v18.glb
---

# TASK-050 — UV-baked interior material pivot

## Owner boundary

Antigravity owns the visual/material implementation and new GLB. Do not edit
Codex-owned website source. Use the fixed fixture and reference criteria from
`reports/reference-fidelity-criteria.md`.

## Required implementation

1. Produce `assets/models/raw/deltrol_p2s_explorer_v18.glb` as a real connected
   3D mesh. No billboard, image plane, camera-facing card or 2.5D replacement.
2. Rebuild the interior rail/gantry/turbine material path rather than copying the
   v17 emission textures. Use clean UVs and actual PNG base-color/roughness maps
   baked from a controlled Cycles scene, or an equivalently verifiable physically
   based bake.
3. Keep metallic values low enough for the viewer lighting to affect the parts
   (target `0.0–0.25` for the rail/turbine base materials unless a documented
   exception is necessary). Do not use emission to force the ROI color.
4. Preserve the accepted exterior silhouette, door, pillar, console, glass and
   camera framing while improving only the failed interior contrast first.

## Required evidence

Create all of the following:

- `reports/task050-explorer-front.png`
- `reports/task050-explorer-left20.png`
- `reports/task050-explorer-right20.png`
- `reports/task050-explorer-elevated.png`
- `reports/task050-explorer-4view-sheet.png`
- `reports/task050-reference-candidate-contact-sheet.png`
- `reports/task050-rail-turbine-before-after.png`
- `reports/task050-silhouette-overlay.png`
- `reports/TASK-050-antigravity-uv-baked-interior-material-pivot.md`
- `bridge/outbox/TASK-050-UV-BAKED-INTERIOR-MATERIAL-PIVOT-antigravity-response.md`

The report must include:

- exact node/mesh/primitive/material mapping for rails, gantry, turbine, toolhead
  and bed;
- texture image names, dimensions, UV set and material texture slots;
- before/after crop showing the selected primitive pixels actually changed;
- fixed-fixture bbox/IoU, all 15 ROI values, 12 landmarks and GLB validation;
- an honest verdict. Load/build success alone is not visual acceptance.

## Target gates

- rail ROI near `(114,93,80)`;
- turbine ROI near `(109,88,73)`;
- both failed ROIs `dMax <= 15`;
- contact sheet must visibly show the dark warm mechanical hierarchy of the
  reference, not a pale white gantry;
- retain centered IoU `>= 0.90` and the accepted exterior silhouette.

If this pivot cannot materially change the direct rail/turbine pixels, report
`PIVOT_REQUIRED` and explain the blocker; do not spend another turn changing only
camera, exposure or generic shader constants.
