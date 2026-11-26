# Codex audit — TASK-066

- **Task:** `TASK-066-RAIL-ONLY-CALIBRATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v34.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected `task066-rail-material-diagnostic.png`, `task066-before-after.png`,
  the direct reference/candidate contact sheet, and the fresh v34 front render.
- Verified v34 SHA-256 differs from v33.
- Inspected the GLB JSON: v34 changes materials 4 and 12 to
  `KHR_materials_unlit`; mesh 43 and mesh 44 both still use material 12.

## Findings

1. The fixed fixture still gives `Centered IoU=0.9073`, but only `13/15`
   ROIs pass. The rail remains the hard failure at `dMax=37.9`; its sampled
   RGB is `(76.4,59.5,47.7)` versus the reference `(114.3,96.3,85.6)`.
2. The rail-only material edit did not move ROI 13 toward the reference. It
   also regressed `07_Right_Win_Glass` from v33 `dMax=6.0` to `43.6`, so the
   edited material is visible through the right-window region.
3. The before/after diagnostic visibly changes broad interior silhouettes and
   the right window, not just the sampled rail. This violates the rail-only
   isolation objective.
4. The contact sheet caption says `CANDIDATE v31` while the handoff is v34.
   That evidence-integrity error is independently disqualifying.

## Decision

Keep v33 as the best numeric base and retire the guessed material-index path.
The next task must identify the actual primitive covering ROI 13 in the fixed
front render using an object/depth or material-ID pass, then split or assign
only that real mechanical mesh/material. It must restore v33's glass pass and
regenerate correctly labeled v34+ evidence. No unlit global/interior edit,
emission, exposure, camera change, billboard, image plane, or 2.5D overlay.

