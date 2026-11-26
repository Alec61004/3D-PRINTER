---
task_id: TASK-062-LIGHT-RIG-GLASS-CLOSEOUT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T09:49:25+07:00
created_at: 2026-11-26T12:35:00+07:00
request: >-
  Continue the improving light-rig path from TASK-061. Current errors are rail
  dMax=22.4, turbine dMax=16.5 and right-window glass dMax=20.2. Perform one
  controlled closeout calibration of local light intensity/range/placement and
  right-glass alpha/color so all three reach dMax <= 15. Preserve v29 geometry,
  PBR shading and fixed camera/exposure; no emission or unlit materials.
result_path: assets/models/raw/deltrol_p2s_explorer_v30.glb
---

# TASK-062 — Light-rig/glass closeout

## Owner boundary

Antigravity owns the final GLB light/material calibration and evidence. Do not
edit Codex website source. Start from v29 and preserve its geometry.

## Required calibration

1. Keep the two real `KHR_lights_punctual` chamber lights. Tune intensity,
   range, size/position and warm color only enough to move rail/turbine toward
   the reference without washing the chamber or skylight.
2. Keep rail/turbine/toolhead/bed as shaded PBR, zero emissive, no
   `KHR_materials_unlit`.
3. Tune the right-window glass independently toward the reference warm-smoked
   RGB; do not use a global exposure/world change.
4. Do not add geometry, move the camera, change the fixed fixture, or change the
   outer shell/pillar/console.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v30.glb`
- `reports/task062-explorer-front.png`
- `reports/task062-explorer-left20.png`
- `reports/task062-explorer-right20.png`
- `reports/task062-explorer-elevated.png`
- `reports/task062-explorer-4view-sheet.png`
- `reports/task062-reference-candidate-contact-sheet.png`
- `reports/task062-light-glass-before-after.png`
- `reports/task062-light-rig-diagnostic.png`
- `reports/task062-silhouette-overlay.png`
- `reports/TASK-062-antigravity-light-rig-glass-closeout.md`
- `bridge/outbox/TASK-062-LIGHT-RIG-GLASS-CLOSEOUT-antigravity-response.md`

The diagnostic must show v29 baseline and v30 final with the light parameters,
glass parameters and sampled RGB for ROI 13, ROI 14 and ROI 07. Report old/new
hash and inventory, exact GLB light/material JSON, fixed-fixture bbox/IoU, all 15
ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- contact sheet visibly retains PBR depth and approaches the reference.

If this controlled calibration no longer improves all three regions, report
`PIVOT_REQUIRED` with the measured ceiling; do not blindly raise intensity.
