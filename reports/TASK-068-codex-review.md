# Codex audit — TASK-068

- **Task:** `TASK-068-REAL-RAIL-GEOMETRY-INSERT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v36.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the rail geometry diagnostic, before/after, direct contact sheet,
  and fresh v36 front render.
- Verified v36 is a real binary change from v33 and contains the reported new
  node/mesh/material.

## Findings

1. The new `upper_steel_rail_bar` is genuine 3D geometry (`node 68`, `mesh
   59`, isolated PBR `material 18`) and v36 hash differs from v33.
2. The placement is not visually effective. The rail sits at `t≈1.650` inside
   the `0.037m` gap between `top_roof_glass` (`t=1.6270`) and
   `interior_ceiling_liner` (`t=1.6640`), so smoked-glass attenuation and roof
   shadow occlude it in the fixed render.
3. ROI 13 remains exactly `(79.6,64.5,54.2)`, `dMax=34.7 FAIL`; the overall
   result remains `14/15 PASS`, IoU `0.9073`. Therefore the inserted mesh did
   not improve the reference image.
4. The contact sheet still says `CANDIDATE v31` rather than v36. Evidence
   labeling remains a mandatory correction.

## Decision

The material-only and isolated-rail insertion attempts are retired. The next
revision must use a source-geometry/Blender pivot: remodel the roof/ceiling
clearance and rail mounting relationship so the rail is physically visible
through the intact glass, while preserving the shell, camera, glass, turbine,
and the 14 passing ROI values. This is a new geometry method, not another
shader/light patch.

