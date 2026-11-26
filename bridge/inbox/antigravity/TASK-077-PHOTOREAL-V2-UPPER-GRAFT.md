---
task_id: TASK-077-PHOTOREAL-V2-UPPER-GRAFT
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:32:10+07:00
created_at: 2026-11-26T11:18:00+07:00
request: >-
  Use the bake-off evidence to graft only the upper chamber/gantry/rail source
  geometry from assets/models/raw/deltrol_p2s_photoreal_v2.glb onto the v33
  lower/exterior shell baseline. photoreal_v2 has the closest measured rail
  ROI (dMax=24.3) but poor whole-model IoU; preserve v33 shell, glass,
  turbine, bed, console, materials and camera while importing only its better
  upper mechanical geometry.
result_path: assets/models/raw/deltrol_p2s_photoreal_v2_upper_graft.glb
---

# TASK-077 — photoreal_v2 upper mechanical graft

## Owner boundary

Antigravity owns the asset graft and visual evidence. Do not edit Codex website
source. Codex will audit the combined GLB after terminal handoff.

## Required graft

1. Use v33 as the complete baseline. Inspect `deltrol_p2s_photoreal_v2.glb`
   and identify the actual upper chamber/gantry/rail/printhead nodes that drive
   its better ROI 13. Record source node/mesh/material names and hashes.
2. Graft only those real mechanical meshes into the v33 shell. Do not import
   photoreal_v2's exterior shell, front/right glass, console, global lights or
   camera. Remove conflicting v33 upper mechanical nodes so there is one
   connected assembly, not z-fighting duplicates.
3. Fit the graft inside the v33 exterior envelope using the fixed camera. The
   reference rail must be visible in the chamber without protruding above the
   shell or relying on v33's old roof-shadow path. Keep front/top glass real.
4. Use normal PBR materials; no billboard, image plane, screenshot texture,
   projected reference, emission, global unlit, camera or exposure trick.
5. Validate front/left20/right20/elevated continuity and prove ROI 13 ray hits
   the grafted rail/mechanical surface, not a shell shadow.

## Required evidence

- `assets/models/raw/deltrol_p2s_photoreal_v2_upper_graft.glb`
- `reports/task077-explorer-front.png`
- `reports/task077-explorer-left20.png`
- `reports/task077-explorer-right20.png`
- `reports/task077-explorer-elevated.png`
- `reports/task077-explorer-4view-sheet.png`
- `reports/task077-reference-candidate-contact-sheet.png`
- `reports/task077-upper-graft-diagnostic.png`
- `reports/task077-source-node-map.md`
- `reports/task077-before-after.png`
- `reports/task077-silhouette-overlay.png`
- `reports/TASK-077-antigravity-photoreal-v2-upper-graft.md`
- `bridge/outbox/TASK-077-PHOTOREAL-V2-UPPER-GRAFT-antigravity-response.md`

Every image must be rendered from the graft artifact. The contact sheet must
say `CANDIDATE PHOTOREAL-V2-UPPER-GRAFT` and include its SHA-256; never use a
stale v31/v33 label.

## Acceptance gates

- ROI 13 improves materially from v33 and reaches `dMax <= 15`;
- ROIs 01–12, 14 and 15 remain `PASS` and no worse than v33;
- bbox/silhouette/framing remain within reference tolerance;
- grafted upper assembly is real, connected and stable in all four views;
- source node map and raycast proof identify the actual graft;
- no mislabeled evidence or analytic visual trick.

If photoreal_v2's upper geometry cannot be separated cleanly, report the
measured node/material conflict and try the next component source; do not
claim PASS.
