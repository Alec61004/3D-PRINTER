# Codex audit — TASK-058

- **Task:** `TASK-058-EXPLICIT-INTERIOR-MATERIAL-PATCH`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v26.glb`
- **Codex verdict:** `REVISION_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified v26 has a new hash and material JSON change using `KHR_materials_unlit`.
- Inspected `task058-material-through-glass-diagnostic.png`, the direct front render and the contact sheet.

## Findings

1. The patch executed, but the unlit fallback flattened the interior into a silhouette-like brown/gray block. It destroyed the photoreal mechanical shading and is not acceptable for the reference.
2. All three target regions still fail: rail `dMax=37.9`, turbine `dMax=18.6`, right-window glass `dMax=41.6`; only 12/15 ROIs pass.
3. The direct contact sheet is materially worse than v24: rails and turbine lose readable specular depth, the printed object becomes a flat wedge, and the right glass is far too light.
4. The report proves that a JSON/material change alone is insufficient; the chosen unlit strategy is retired for this asset.

## Decision

Do not integrate v26. Roll back to the v24 PBR geometry/coverage basis and perform a constrained PBR calibration grid separately for rail, turbine and right glass. Preserve directional shading and tune only the per-material base color/roughness/transmission parameters.
