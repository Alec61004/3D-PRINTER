---
task_id: TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:29:30+07:00
created_at: 2026-11-26T11:10:00+07:00
request: >-
  Pivot away from the v33-derived upper-asset workflow. Perform a fixed-fixture
  bake-off of the existing physical source candidates
  (assets/models/raw/deltrol_p2s_source.glb,
  assets/models/raw/deltrol_p2s_photoreal_v2.glb,
  assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb,
  assets/models/optimized/deltrol_p2s_optimized.glb and any other materially
  different source). Select the best real 3D source for the Deltrol reference,
  then produce a candidate from that source only if it materially improves the
  upper rail/chamber landmark.
result_path: assets/models/raw/deltrol_p2s_legacy-source-bakeoff.glb
---

# TASK-076 — legacy physical source bake-off

## Owner boundary

Antigravity owns visual/source-asset selection and evidence. Do not edit Codex
website source. Codex will audit the bake-off and selected artifact.

## Required bake-off

1. Render each materially different existing GLB under the fixed fixture:
   1226x708, FOV 27°, eye `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white
   background, ACES, exposure 1.05. Do not normalize all candidates into the
   same v33 geometry before comparison.
2. Build a contact sheet labeled with the exact candidate basename and SHA-256
   for every source. Include a short table of nodes/meshes, bbox/IoU, ROI 13
   dMax, all-ROI pass count, and whether the rail/chamber is real 3D.
3. Select the source with the strongest genuine upper rail/chamber geometry.
   If a small material/light adjustment is necessary for a selected source,
   record it separately and keep it local; do not import v33's shadow path.
4. The selected candidate must remain a connected 3D asset in front/left20/
   right20/elevated views. No billboard, image plane, screenshot texture,
   projected reference, emission, global unlit, camera or exposure trick.

## Required evidence

- `assets/models/raw/deltrol_p2s_legacy-source-bakeoff.glb`
- `reports/task076-source-bakeoff-sheet.png`
- `reports/task076-source-bakeoff-metrics.md`
- `reports/task076-selected-front.png`
- `reports/task076-selected-left20.png`
- `reports/task076-selected-right20.png`
- `reports/task076-selected-elevated.png`
- `reports/task076-selected-4view-sheet.png`
- `reports/task076-reference-candidate-contact-sheet.png`
- `reports/task076-before-after.png`
- `reports/task076-silhouette-overlay.png`
- `reports/TASK-076-antigravity-legacy-source-asset-bakeoff.md`
- `bridge/outbox/TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF-antigravity-response.md`

Every selected image must name the actual selected source and SHA-256. Do not
use the stale `CANDIDATE v31` caption.

## Acceptance gates

- Selected source is materially different from v33 and proven by hash/node
  manifest;
- selected source improves the upper rail/chamber landmark or proves a better
  starting point than v33;
- exterior bbox/silhouette remains within reference tolerance;
- real 3D continuity holds across all four views;
- if no existing source is viable, report that concrete blocker and identify
  the next external source/reconstruction method; do not claim PASS.
