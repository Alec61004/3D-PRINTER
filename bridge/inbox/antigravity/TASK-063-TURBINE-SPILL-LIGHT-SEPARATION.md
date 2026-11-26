---
task_id: TASK-063-TURBINE-SPILL-LIGHT-SEPARATION
owner: antigravity
status: pending
created_at: 2026-11-26T12:55:00+07:00
request: >-
  Continue from TASK-062. Rail dMax=12.9 and right-window glass dMax=13.5 now
  pass. Turbine is narrowly high at dMax=15.6, while skylight dMax=19.0 and
  chamber upper dMax=15.6 are over-lit. Decouple the local light rig: preserve
  rail/glass passes, direct more warm fill onto the turbine, and reduce spill onto
  skylight/chamber upper. Keep PBR geometry/materials and fixed camera/exposure.
result_path: assets/models/raw/deltrol_p2s_explorer_v31.glb
---

# TASK-063 — Turbine fill and spill separation

## Owner boundary

Antigravity owns the local light-rig tuning and GLB evidence. Do not edit Codex
website source. Start from v30 and preserve geometry, PBR materials and the
passing rail/glass configuration.

## Required tuning

1. Keep the upper rail light as the source that produced the rail pass, changing
   it only enough to reduce skylight/chamber spill if necessary.
2. Reposition/narrow/aim the turbine fill light or replace it with a small local
   area/spot light that illuminates the printed turbine without washing the upper
   chamber. Report exact light type, position, color, intensity, range/size and
   direction.
3. Keep rail/turbine/toolhead/bed materials shaded PBR, with no emissive factor,
   emissive texture or `KHR_materials_unlit`.
4. Keep right-window glass at or better than the v30 pass. Do not change camera,
   world, exposure, outer shell or geometry.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v31.glb`
- `reports/task063-explorer-front.png`
- `reports/task063-explorer-left20.png`
- `reports/task063-explorer-right20.png`
- `reports/task063-explorer-elevated.png`
- `reports/task063-explorer-4view-sheet.png`
- `reports/task063-reference-candidate-contact-sheet.png`
- `reports/task063-spill-separation-diagnostic.png`
- `reports/task063-light-before-after.png`
- `reports/task063-silhouette-overlay.png`
- `reports/TASK-063-antigravity-turbine-spill-light-separation.md`
- `bridge/outbox/TASK-063-TURBINE-SPILL-LIGHT-SEPARATION-antigravity-response.md`

The diagnostic must show v30 baseline and v31 final with light influence and
sampled RGB for ROI 13, ROI 14, ROI 07, ROI 11 and ROI 12. Report old/new hash,
exact light/material JSON, fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and
GLB validation.

## Acceptance gates

- rail ROI `dMax <= 15` and not worse than v30;
- turbine ROI `dMax <= 15`;
- right-window glass `dMax <= 15` and not worse than v30;
- skylight ROI `dMax <= 15`;
- chamber upper ROI `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct contact sheet preserves PBR depth and approaches reference.

If this spill-separation pass cannot improve turbine without breaking the passing
regions, report `PIVOT_REQUIRED` with the measured tradeoff instead of changing
global exposure or adding emission.
