---
task_id: TASK-070-DEPTH-CALIBRATED-RAIL-PLACEMENT
owner: antigravity
status: pending
created_at: 2026-11-26T10:30:00+07:00
request: >-
  Pivot from v37's still-occluded rail. Use the fixed camera ray/depth data to
  place the real upper gantry rail assembly in the visible chamber layer: it
  must be closer to the camera than the top_roof_glass hit at ROI 13 while
  remaining behind the front glass and mechanically connected to the gantry.
  Preserve v33's 14 passing ROI values and exterior silhouette.
result_path: assets/models/raw/deltrol_p2s_explorer_v38.glb
---

# TASK-070 — depth-calibrated real rail placement

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Required placement pivot

1. Start from v33's material/light baseline. Do not carry v34 unlit edits or
   v37's roof-liner raise unless the report proves they are reverted or needed.
2. At ROI 13 `(493,300)-(518,305)`, use the fixed fixture ray hits from
   TASK-067 (`top_roof_glass t≈1.627`, ceiling liner `t≈1.664`) and place the
   real rail assembly at a measured depth in the visible chamber layer, e.g.
   between the front glass and the roof-glass occluder. Record exact new depth,
   world-space AABB and the front-glass/roof-glass clearances.
3. Keep the rail as genuine connected mechanical geometry: a horizontal bar,
   mounts/end blocks, and connection to the gantry/printhead assembly. It must
   remain coherent in left20, right20 and elevated views. No floating box,
   billboard, image plane, screenshot texture, projected reference, emission,
   global unlit material, camera change or exposure trick.
4. Keep `top_roof_glass` and front glass as real intact glass. Do not remove,
   opaque, globally recolor or bypass the glass. The rail must be visible by
   correct physical placement and normal PBR shading.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v38.glb`
- `reports/task070-explorer-front.png`
- `reports/task070-explorer-left20.png`
- `reports/task070-explorer-right20.png`
- `reports/task070-explorer-elevated.png`
- `reports/task070-explorer-4view-sheet.png`
- `reports/task070-reference-candidate-contact-sheet.png`
- `reports/task070-rail-depth-diagnostic.png`
- `reports/task070-before-after.png`
- `reports/task070-silhouette-overlay.png`
- `reports/TASK-070-antigravity-depth-calibrated-rail-placement.md`
- `bridge/outbox/TASK-070-DEPTH-CALIBRATED-RAIL-PLACEMENT-antigravity-response.md`

Every image must be rendered from v38. The contact sheet must say
`CANDIDATE v38` and include the v38 SHA-256. The report must include old/new
hashes, exact ray/depth placement, node/mesh/material details, all 15 ROIs,
12 landmarks and GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15` with visible rail pixels moving toward reference;
- ROIs 01–12, 14 and 15 remain `PASS` and no worse than v33;
- centered IoU `>= 0.90`, exterior silhouette/framing unchanged;
- rail/printhead upper landmark visibly approaches reference;
- all four views show one coherent real 3D asset;
- no mislabeled evidence or analytic visual trick.

If this depth placement is physically incompatible with the current source
mesh, report the measured conflict and pivot to a new source mesh/rebuild;
do not claim PASS.
