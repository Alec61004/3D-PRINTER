# Codex audit — TASK-054

- **Task:** `TASK-054-VERIFIED-NEW-INTERIOR-ASSET`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v22.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified that v22 is a genuine artifact change: `68` nodes/`60` meshes versus v20/v21 `64` nodes/`56` meshes, with a different SHA-256.
- Inspected `task054-interior-before-after.png`, the direct front render and the reference/candidate contact sheet.

## Findings

1. The source-asset preflight passes, but visual acceptance fails: rail `dMax=35.1`, turbine `dMax=20.4`, right-window glass `dMax=26.0`; only 12/15 ROIs pass.
2. The new geometry adds pale upper rails and a dark circular detail, but the direct screenshot still does not match the reference's compact warm-dark carriage/rail assembly. The changed mesh is not yet the correct source geometry.
3. The right-window glass regression remains, so the v22 material/visibility changes cannot be integrated as-is.
4. Framing remains acceptable, but the fixed bbox/IoU does not compensate for the interior mismatch.

## Decision

Keep v22 as evidence only; do not integrate it. Continue with a new independent mechanical assembly pass that controls the actual rail/turbine ROI appearance and restores the right-window glass. The next handoff must prove an ROI pixel change, not merely add nodes.
