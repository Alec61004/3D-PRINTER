# Codex audit — TASK-052

- **Task:** `TASK-052-FRESH-INTERIOR-SOURCE-MESH`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v20.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified the reported GLB-level no-emissive proof for the four interior metal materials.
- Inspected `task052-interior-before-after.png`, the direct front render and the reference/candidate contact sheet.
- Verified fixed-fixture framing: `423x404`, centered IoU `0.9073`.

## Findings

1. The no-emissive requirement is now satisfied, but visual acceptance still fails: rail `dMax=35.1`, turbine `dMax=20.4`, and only 12/15 ROIs pass.
2. The right-window glass regressed again to `dMax=26.0`, so the accepted exterior/glass state was not preserved.
3. The direct before/after crop shows v19 and v20 are effectively the same visible interior. The candidate remains a generic pale gantry with incorrect proportions and mechanical hierarchy compared with the reference.
4. The report itself identifies the remaining root cause: the procedural vertex-baked interior source needs replacement by a clean CAD/Blender source mesh. This is a valid pipeline pivot, not a reason to stop the project.

## Decision

Retire the procedural interior family v12–v20. Continue with a fresh CAD/Blender-built interior source mesh, preserving the accepted exterior shell and glass while rebuilding the visible rails, carriage/toolhead, bed and turbine geometry from the reference proportions.
