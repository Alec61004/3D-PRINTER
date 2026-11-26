---
task_id: TASK-059-PBR-CALIBRATION-GRID
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T09:36:30+07:00
created_at: 2026-11-26T11:30:00+07:00
request: >-
  TASK-058 executed but the KHR_materials_unlit fallback flattened the interior
  and worsened the match: rail dMax=37.9, turbine dMax=18.6 and right glass
  dMax=41.6. Roll back to the v24 PBR geometry/coverage basis and run a
  constrained per-material calibration grid for the actual rail, turbine and
  right-window glass primitives. Preserve physically shaded depth and change the
  final sampled pixels without using emission or unlit materials.
result_path: assets/models/raw/deltrol_p2s_explorer_v27.glb
---

# TASK-059 — PBR calibration grid

## Owner boundary

Antigravity owns the GLB material calibration and visual evidence. Do not edit
Codex website source. Use v24 geometry/ROI ownership as the starting point; do
not add new geometry.

## Material rules

1. Roll back `KHR_materials_unlit` for the interior. Rail, turbine, toolhead and
   chamber must use shaded PBR materials with visible directional/specular depth.
2. No emissive factor or emissive texture on rail/turbine materials.
3. Calibrate each region independently using a small parameter grid over
   base-color factor, metallic, roughness and glass transmission/alpha. Select
   the candidate minimizing the actual post-ACES RGB error at the fixed ROI,
   not a guessed material value.
4. Do not change camera, exposure, global lighting or exterior geometry.
5. Preserve readable rail cylinders, the toolhead intake, the printed turbine
   form and the accepted shell/pillar/console.

## Required calibration evidence

Produce `reports/task059-pbr-calibration-grid.png` showing, for ROI 13, ROI 14
and ROI 07, at least three parameter candidates and the selected candidate's
post-ACES RGB values. Also produce a final before/after crop against v24.

## Required output

- `assets/models/raw/deltrol_p2s_explorer_v27.glb`
- `reports/task059-explorer-front.png`
- `reports/task059-explorer-left20.png`
- `reports/task059-explorer-right20.png`
- `reports/task059-explorer-elevated.png`
- `reports/task059-explorer-4view-sheet.png`
- `reports/task059-reference-candidate-contact-sheet.png`
- `reports/task059-pbr-calibration-grid.png`
- `reports/task059-interior-before-after.png`
- `reports/task059-silhouette-overlay.png`
- `reports/TASK-059-antigravity-pbr-calibration-grid.md`
- `bridge/outbox/TASK-059-PBR-CALIBRATION-GRID-antigravity-response.md`

The report must include old/new hashes, exact material JSON snippets, exact
primitive mapping, fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB
validation. The final GLB must differ from v24/v26.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- contact sheet preserves photoreal shading and is visibly closer to reference;
- no emission and no unlit materials in the final interior.

If the PBR grid cannot move the intended pixels without destroying shading,
report `PIVOT_REQUIRED` with the measured limitation; do not submit another
unlit silhouette.
