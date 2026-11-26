# Codex audit — TASK-064

- **Task:** `TASK-064-SPOTLIGHT-MECHANICAL-TARGETING`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v32.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the spotlight diagnostic, direct front render and contact sheet.
- Verified v32 has a new hash relative to v31.

## Findings

1. Narrow spot lights successfully suppress spill: skylight `dMax=3.0`, chamber upper `8.7`, right glass `14.3` all pass.
2. They do not solve the target mechanical regions: rail `dMax=35.5`, turbine `15.8`; only 13/15 ROIs pass.
3. The contact sheet is mislabeled as `CANDIDATE v31` even though the handoff is for v32. Because evidence integrity requires the displayed artifact to match the audited artifact, this sheet cannot support acceptance.
4. The direct v32 diagnostic confirms the spotlight-only path is not enough for the recessed/grazing rail and turbine surfaces.

## Decision

Retire spotlight-only targeting. Preserve the successful spill suppression as a base, then use a controlled per-primitive color/material compensation for only the rail and turbine while keeping the rest PBR. The next task must regenerate every screenshot with the correct v33 artifact/hash and corrected labels.
