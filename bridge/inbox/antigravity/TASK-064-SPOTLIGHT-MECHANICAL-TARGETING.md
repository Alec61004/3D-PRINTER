---
task_id: TASK-064-SPOTLIGHT-MECHANICAL-TARGETING
owner: antigravity
status: in_progress
created_at: 2026-11-26T13:15:00+07:00
request: >-
  Pivot TASK-063's omnidirectional point lights to aimed narrow-cone
  KHR_lights_punctual spot lights. Preserve v31 geometry and PBR materials. Aim
  one warm spot at the upper rail ROI and one at the lower turbine ROI so rail
  dMax <= 15 and turbine dMax <= 15 without spilling skylight/chamber/right
  glass beyond dMax 15.
result_path: assets/models/raw/deltrol_p2s_explorer_v32.glb
---

# TASK-064 — Spotlight mechanical targeting

## Owner boundary

Antigravity owns the light-rig GLB and evidence. Do not edit Codex website source.
Start from v31; preserve geometry, PBR materials, shell, camera and exposure.

## Required implementation

1. Replace the two omnidirectional point lights with real
   `KHR_lights_punctual` `spot` lights, or add narrowly aimed spot lights while
   disabling the broad point contribution.
2. Aim the upper spot at the actual rail screen/depth region and the lower spot
   at `bracket_swept_arch`/turbine. Report positions, directions, color,
   intensity, range, `innerConeAngle` and `outerConeAngle`.
3. Keep all interior materials shaded PBR, zero emissive and no
   `KHR_materials_unlit`.
4. Keep the v31 right-window glass configuration and preserve its pass if
   possible. Do not change camera, global exposure/world, geometry or exterior
   shell.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v32.glb`
- `reports/task064-explorer-front.png`
- `reports/task064-explorer-left20.png`
- `reports/task064-explorer-right20.png`
- `reports/task064-explorer-elevated.png`
- `reports/task064-explorer-4view-sheet.png`
- `reports/task064-reference-candidate-contact-sheet.png`
- `reports/task064-spotlight-diagnostic.png`
- `reports/task064-light-before-after.png`
- `reports/task064-silhouette-overlay.png`
- `reports/TASK-064-antigravity-spotlight-mechanical-targeting.md`
- `bridge/outbox/TASK-064-SPOTLIGHT-MECHANICAL-TARGETING-antigravity-response.md`

The diagnostic must show v31 point-light baseline and v32 spotlight final, with
light cones/parameters and sampled RGB for ROI 07, 11, 12, 13 and 14. Report
old/new hash, exact GLB light/material JSON, fixed-fixture bbox/IoU, all 15 ROIs,
12 landmarks and GLB validation.

## Acceptance gates

- rail ROI `dMax <= 15`;
- turbine ROI `dMax <= 15`;
- right-window glass `dMax <= 15`;
- skylight ROI `dMax <= 15`;
- chamber upper ROI `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct contact sheet keeps PBR depth and visibly approaches the reference;
- no emission, unlit materials, camera or global exposure tricks.

If spot targeting cannot separate the regions, report `PIVOT_REQUIRED` with the
measured cone/lighting limitation rather than reverting to point intensity.
