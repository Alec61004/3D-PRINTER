---
task_id: TASK-078-PHOTOREAL-V2-GANTRY-CLUSTER-GRAFT
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:34:40+07:00
created_at: 2026-11-26T11:26:00+07:00
request: >-
  Correct TASK-077 by grafting the actual photoreal_v2 upper gantry/mechanical
  cluster, not door_top_rail. Import x_guide_front/rear, x_belt_front/rear,
  toolhead_body/face, fan/nozzle and relevant structural spar/cantilever meshes
  from assets/models/raw/deltrol_p2s_photoreal_v2.glb into the v33 shell/lower
  baseline. Remove overlapping v33 upper mechanics so one real assembly remains.
result_path: assets/models/raw/deltrol_p2s_photoreal_v2_gantry_cluster.glb
---

# TASK-078 — photoreal_v2 gantry cluster graft

## Owner boundary

Antigravity owns the asset graft and evidence. Do not edit Codex website source.
Codex will audit the final combined GLB.

## Required source cluster

1. Start from v33 as shell/lower-body/material/light baseline. From
   `photoreal_v2.glb`, import the actual upper mechanical cluster:
   `x_guide_front` mesh 49, `x_guide_rear` mesh 50,
   `x_belt_front/rear` meshes 51/52, `toolhead_body/face` meshes 53/54,
   fan meshes 55–58, nozzle mesh 59, PTFE meshes 60–65, and only the relevant
   structural spar/cantilever meshes 69–72 if they are part of the same
   connected gantry.
2. Do not import photoreal_v2's shell, glass, console, camera, global lights,
   or door frame. Remove or replace the overlapping v33 gantry/rail/toolhead
   nodes so there is no z-fighting or duplicate assembly.
3. Align the imported cluster to v33's fixed chamber and reference front view.
   It must remain real connected 3D geometry in front/left20/right20/elevated
   views, with the upper rail visible and inside the exterior envelope.
4. Preserve v33's shell bbox/silhouette, glass, turbine, bed, console and
   material hierarchy. Use normal PBR materials; no billboard, image plane,
   projected reference, emission, global unlit, camera or exposure trick.
5. Produce a raycast/object map proving ROI 13 hits the imported gantry/rail
   cluster rather than a shell shadow.

## Required evidence

- `assets/models/raw/deltrol_p2s_photoreal_v2_gantry_cluster.glb`
- `reports/task078-explorer-front.png`
- `reports/task078-explorer-left20.png`
- `reports/task078-explorer-right20.png`
- `reports/task078-explorer-elevated.png`
- `reports/task078-explorer-4view-sheet.png`
- `reports/task078-reference-candidate-contact-sheet.png`
- `reports/task078-gantry-cluster-diagnostic.png`
- `reports/task078-source-node-map.md`
- `reports/task078-before-after.png`
- `reports/task078-silhouette-overlay.png`
- `reports/TASK-078-antigravity-photoreal-v2-gantry-cluster-graft.md`
- `bridge/outbox/TASK-078-PHOTOREAL-V2-GANTRY-CLUSTER-GRAFT-antigravity-response.md`

Every image must be rendered from the cluster-graft artifact. The contact
sheet must say `CANDIDATE PHOTOREAL-V2-GANTRY-CLUSTER` and include its SHA-256.

## Acceptance gates

- ROI 13 materially improves and reaches `dMax <= 15`;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing remain within reference tolerance;
- imported cluster is connected and stable across all four views;
- node map and raycast identify the real imported rail/gantry;
- no mislabeled evidence or analytic visual trick.

If the cluster cannot align without collateral damage, report the exact source
node conflict and move to a different source/reconstruction method; do not
claim PASS.
