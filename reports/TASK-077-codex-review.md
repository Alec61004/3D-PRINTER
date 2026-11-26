# Codex audit — TASK-077

- **Task:** `TASK-077-PHOTOREAL-V2-UPPER-GRAFT`
- **Artifact:** `assets/models/raw/deltrol_p2s_photoreal_v2_upper_graft.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the graft report, source node map and outbox response.
- Inspected the graft diagnostic, before/after, direct contact sheet and front
  render.
- Inspected the full photoreal_v2 node/material manifest.

## Findings

1. The task grafted only `door_top_rail` (`photoreal_v2` node 44 / mesh 38),
   which is a door frame element, not the upper gantry responsible for ROI 13.
2. The actual photoreal_v2 upper mechanical source is represented by
   `x_guide_front` (mesh 49), `x_guide_rear` (mesh 50), `x_belt_front/rear`
   (meshes 51/52), `toolhead_body/face` (meshes 53/54), fan/nozzle meshes
   55–59, and structural spar/cantilever meshes 69–72.
3. The grafted result leaves ROI 13 unchanged at `dMax=34.7`, drops IoU to
   `0.8976`, and breaks ROI 02 (`dMax=24.9`), producing only `13/15 PASS`.
4. The contact sheet still says `CANDIDATE v31` instead of the graft label,
   another evidence-integrity failure.

## Decision

Discard the door-rail-only graft. The next task must import the actual
photoreal_v2 upper gantry/mechanical cluster, align it to the v33 chamber and
remove overlapping v33 upper mechanics so the rail is not duplicated.

