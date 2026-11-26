# Codex audit — TASK-050

- **Task:** `TASK-050-UV-BAKED-INTERIOR-MATERIAL-PIVOT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v18.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected `task050-rail-turbine-before-after.png`, the direct front render and the reference/candidate contact sheet.
- Confirmed the fixed fixture still frames the candidate at `423x404`, centered IoU `0.9073`.

## Findings

1. The UV-baked low-metallic material pivot did not solve the failing regions: rail `dMax=35.3`, turbine `dMax=20.1`; only 12/15 ROIs pass.
2. `07_Right_Win_Glass` regressed to `dMax=25.5`, so the material change damaged an already accepted exterior/glass region.
3. The direct before/after still shows a pale, generic interior assembly rather than the reference's warm dark rails, compact toolhead and clearly readable printed object. The issue is now a combined interior-geometry/visibility problem, not a missing roughness tweak.
4. Framing remains acceptable, but the contact sheet and direct render contradict any visual-pass interpretation.

## Decision

Retire the v18 UV-bake-only approach. Continue with a new interior reconstruction pass that changes the actual rail/toolhead/bed/turbine geometry and controls front-glass visibility deliberately. Do not spend another iteration only changing metallic, emission, exposure or camera constants.
