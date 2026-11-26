# Codex audit — TASK-069

- **Task:** `TASK-069-ROOF-CEILING-CLEARANCE-BLENDER-PIVOT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v37.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the roof/rail clearance diagnostic, before/after, direct contact
  sheet, and fresh v37 front render.
- Verified v37 is a new binary and contains the raised liner and rail assembly.

## Findings

1. The source-geometry edit is real: the ceiling liner moved `+0.015m` and
   clearance is reported as `0.052m`; the rail assembly has mounts and an
   isolated PBR material.
2. It produces no measurable visual improvement. ROI 13 remains exactly
   `(79.6,64.5,54.2)`, `dMax=34.7 FAIL`; overall remains `14/15 PASS`, IoU
   `0.9073`.
3. The direct diagnostic confirms the rail is still behind `top_roof_glass`
   and inside the roof shadow. Increasing the gap alone cannot make this
   screen-space landmark visible.
4. The contact sheet still says `CANDIDATE v31` instead of v37, so evidence
   labeling is still invalid for acceptance.

## Decision

Retire the “raise ceiling / place rail behind roof glass” placement. The next
task must calibrate the real rail assembly against camera depth and place it
inside the visible chamber layer (closer than the roof-glass hit but still
behind the front glass), with real mounts connected to the gantry. Preserve
the intact glass and v33 lighting/material baseline; do not add another
material-only or clearance-only patch.

