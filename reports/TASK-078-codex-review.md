# Codex audit — TASK-078

- **Task:** `TASK-078-PHOTOREAL-V2-GANTRY-CLUSTER-GRAFT`
- **Artifact:** `assets/models/raw/deltrol_p2s_photoreal_v2_gantry_cluster.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the cluster-graft report, source node map and outbox response.
- Inspected the cluster diagnostic, before/after, direct contact sheet and
  front render.
- Verified the graft is a binary change and the reported meshes were imported.

## Findings

1. The actual photoreal_v2 mechanical cluster was imported, but the fixed
   render still leaves ROI 13 unchanged at `dMax=34.7`; the v33 upper shadow
   path remains the owner of the sampled pixels.
2. The imported toolhead/cluster produces a visibly incorrect large pale block
   inside the chamber and regresses ROI 12 to `dMax=15.5`, leaving only
   `13/15 PASS`. This is not a reference-fidelity improvement.
3. IoU remains `0.9073`, so the shell is preserved, but the interior landmark
   is not solved. The source cluster is not suitable for grafting without a
   larger reconstruction.
4. The contact sheet still uses the stale `CANDIDATE v31` caption instead of
   the cluster-graft name.

## Decision

Retire the current legacy-GLB graft strategy. The next step must use a
different physical source: a free/redistributable CAD or photogrammetry source
with explicit license evidence, then convert and calibrate that source under
the fixed fixture. Do not continue importing individual v33/v2 nodes.

