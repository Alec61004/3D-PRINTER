# Codex audit — TASK-059

- **Task:** `TASK-059-PBR-CALIBRATION-GRID`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v27.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified v27 has a new hash and PBR/no-emission material configuration.
- Inspected the claimed calibration grid, direct front render and contact sheet.
- Compared file hashes: `task059-pbr-calibration-grid.png` and
  `task059-interior-before-after.png` are byte-identical, so the required
  multi-candidate grid evidence was not produced.

## Findings

1. PBR rollback preserves shading but still fails the target regions: rail `dMax=35.5`, turbine `dMax=19.6`, right glass `dMax=32.2`; only 12/15 ROIs pass.
2. The direct candidate remains pale/low-contrast in the upper assembly and the right window is too dark.
3. The material grid claim is not supported by the evidence file; the supposed grid is just the same before/after crop.
4. The report identifies a real renderer limitation: fixed viewer lighting behind the smoked glass cannot lift the PBR interior enough. More base-color guessing is not the next useful pivot.

## Decision

Retain PBR materials and pivot to a physically plausible local interior-light rig. Add controlled warm area/point lights inside the chamber to restore the reference's warm mechanical highlights without emission, unlit materials, global exposure or camera changes. Keep right-window glass independently calibrated.
