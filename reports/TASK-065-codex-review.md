# Codex audit — TASK-065

- **Task:** `TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v33.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the material-compensation diagnostic and before/after crop.
- Verified v33 hash differs from v32 and the turbine moved to PASS.

## Findings

1. v33 achieves `14/15` ROI passes: turbine `dMax=14.5`, right glass `6.0`, skylight `6.6`, chamber upper `12.5`.
2. The rail is the only remaining hard failure at `dMax=34.7`; its sampled RGB moved only `78.8 → 79.6`, confirming the >1 base-color compensation is clamped or the recessed surface receives no useful direct light.
3. The diagnostic proves turbine compensation changed the intended crop, but the rail crop barely changed.
4. The contact sheet is still mislabeled `CANDIDATE v31` even though the handoff is v33. This evidence-integrity defect prevents final acceptance.

## Decision

Keep v33 as the best numeric base, but pivot only the failing rail primitive to a controlled calibrated material path. Preserve v33 turbine/PBR/spot/glass settings. Regenerate all evidence with the actual candidate label/hash.
