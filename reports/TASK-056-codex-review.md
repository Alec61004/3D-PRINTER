# Codex audit — TASK-056

- **Task:** `TASK-056-SCREENSPACE-INTERIOR-CALIBRATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v24.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified v24 hash differs from v23.
- Inspected `task056-roi-coverage-overlay.png`, `task056-interior-before-after.png` and the reference/candidate contact sheet.

## Findings

1. The coverage overlay is useful evidence: ROI 13 is supplied by `x_gantry_crossbeam`/`mech_gantry_rail_bot`, ROI 14 by `bracket_swept_arch`, and ROI 07 by the right-window glass. The intended primitives now own the sampled screen regions.
2. Despite correct ownership, the output pixels remain unchanged: rail `dMax=35.1`, turbine `dMax=20.4`, right glass `dMax=26.0`; only 12/15 ROIs pass.
3. The direct before/after and contact sheet show the same pale upper assembly and overly dark right window. Adding or repositioning more geometry is not the next useful move.
4. Framing passes, but the photometric path through the smoked glass is still wrong.

## Decision

Keep the v24 geometry/coverage as the current base and pivot to a controlled material-through-glass calibration. The next task must change the actual rendered rail/turbine/glass pixels, with a diagnostic separating raw material color, glass-on color and final fixed-fixture color. No new geometry is needed unless the diagnostic proves occlusion.
