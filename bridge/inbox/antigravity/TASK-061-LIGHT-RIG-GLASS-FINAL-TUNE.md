---
task_id: TASK-061-LIGHT-RIG-GLASS-FINAL-TUNE
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T09:45:00+07:00
created_at: 2026-11-26T12:15:00+07:00
request: >-
  Continue from TASK-060, which showed real improvement with local lights:
  rail dMax 35.5->30.3 and turbine 19.6->18.4. Tune the existing PBR/light-rig
  path further so rail and turbine reach dMax <= 15 while restoring the
  right-window glass from dMax 31.1 to <= 15. Do not change geometry, camera,
  exposure, global lighting, emission or unlit materials.
result_path: assets/models/raw/deltrol_p2s_explorer_v29.glb
---

# TASK-061 — Light-rig and glass final tune

## Owner boundary

Antigravity owns the GLB light/material tuning and evidence. Do not edit Codex
website source. Start from v28 and preserve its geometry and local light rig.

## Required changes

1. Keep the two local warm lights as real `KHR_lights_punctual` lights. Tune their
   intensity, range, position and/or size so the upper rail and lower turbine
   receive more reference-like warm highlights without washing the chamber.
2. Keep all rail/turbine/toolhead/bed materials shaded PBR, non-emissive and not
   `KHR_materials_unlit`.
3. Independently tune right-window glass color/alpha/transmission so ROI 07
   returns to the reference warm-smoked value while retaining visible structure.
4. Do not change the fixed camera, exposure, world background, exterior shell or
   geometry. Do not use global lighting changes to hide a local failure.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v29.glb`
- `reports/task061-explorer-front.png`
- `reports/task061-explorer-left20.png`
- `reports/task061-explorer-right20.png`
- `reports/task061-explorer-elevated.png`
- `reports/task061-explorer-4view-sheet.png`
- `reports/task061-reference-candidate-contact-sheet.png`
- `reports/task061-light-glass-before-after.png`
- `reports/task061-light-rig-diagnostic.png`
- `reports/task061-silhouette-overlay.png`
- `reports/TASK-061-antigravity-light-rig-glass-final-tune.md`
- `bridge/outbox/TASK-061-LIGHT-RIG-GLASS-FINAL-TUNE-antigravity-response.md`

The diagnostic must show v28 world-only, v28 light-rig-on and v29 final, with
light parameters and RGB values for ROI 13, ROI 14 and ROI 07. Report exact GLB
material/light JSON, fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB
validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct contact sheet preserves PBR depth and visibly approaches reference;
- no emission, unlit materials, global camera/exposure changes or geometry patch.

If the light/glass path stops improving after this controlled tune, report
`PIVOT_REQUIRED` with measured evidence rather than increasing intensity blindly.
