---
task_id: TASK-060-INTERIOR-LIGHT-RIG-CALIBRATION
owner: antigravity
status: pending
created_at: 2026-11-26T11:55:00+07:00
request: >-
  Continue after TASK-059. PBR materials preserve shading but fixed viewer light
  behind smoked glass cannot lift the rail/turbine ROIs: rail dMax=35.5, turbine
  dMax=19.6 and right glass dMax=32.2. Add a physically plausible local warm
  interior light rig inside the true-3D chamber, keeping PBR materials and
  geometry. Do not use emission, unlit materials, global exposure or camera
  changes. Calibrate the right-window glass separately.
result_path: assets/models/raw/deltrol_p2s_explorer_v28.glb
---

# TASK-060 — Interior light-rig calibration

## Owner boundary

Antigravity owns the visual/light rig and GLB evidence. Do not edit Codex website
source. Use v27 PBR geometry/materials as the base; do not add another pale
geometry patch.

## Lighting requirements

1. Add real local lights in the chamber, for example a low-intensity warm area
   light near the upper chamber/rail direction and a weaker warm fill near the
   bed/turbine. Light positions, color temperature, intensity and size must be
   reported and embedded in a verifiable GLB/scene representation used by the
   render.
2. Keep rail, turbine, toolhead and bed as shaded PBR materials. No emissive
   factor/texture and no `KHR_materials_unlit` for the final interior.
3. Do not modify the fixed camera, exposure, world background or exterior shell
   to fake a pass.
4. Tune right-window glass transmission/alpha so ROI 07 returns to the reference
   warm-smoked value without hiding the right-side structure.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v28.glb`
- `reports/task060-explorer-front.png`
- `reports/task060-explorer-left20.png`
- `reports/task060-explorer-right20.png`
- `reports/task060-explorer-elevated.png`
- `reports/task060-explorer-4view-sheet.png`
- `reports/task060-reference-candidate-contact-sheet.png`
- `reports/task060-light-rig-before-after.png`
- `reports/task060-light-rig-diagnostic.png`
- `reports/task060-silhouette-overlay.png`
- `reports/TASK-060-antigravity-interior-light-rig-calibration.md`
- `bridge/outbox/TASK-060-INTERIOR-LIGHT-RIG-CALIBRATION-antigravity-response.md`

The diagnostic must show world-only, light-rig-on and final fixed-fixture panels,
with light parameters, exact primitive/material mapping and sampled RGB for ROI
13, ROI 14 and ROI 07. The report must include old/new hash and inventory,
fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct contact sheet keeps real PBR depth and visibly approaches the reference;
- no emission/unlit materials and no global camera/exposure trick.

If local lights cannot move the intended pixels, report `PIVOT_REQUIRED` with the
measured limitation; do not revert to emission or a flat unlit silhouette.
