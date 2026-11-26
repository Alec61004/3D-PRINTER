# Codex audit — TASK-062

- **Task:** `TASK-062-LIGHT-RIG-GLASS-CLOSEOUT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v30.glb`
- **Codex verdict:** `REVISION_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the light-rig diagnostic, direct front render and contact sheet.
- Verified the fixed-fixture framing and the v29→v30 light/glass changes.

## Findings

1. Rail now passes at `dMax=12.9` and right-window glass passes at `13.5`.
2. Turbine narrowly misses at `15.6`; skylight `19.0` and chamber upper `15.6` are over-lit by the stronger rig. Only 12/15 ROIs pass.
3. The contact sheet is materially closer and retains PBR depth, so the light-rig path is working. The remaining problem is spill separation between the upper rail light and the turbine fill.

## Decision

Continue with one targeted light-rig pass: preserve the passing rail/glass values, direct more fill toward the turbine, and reduce spill onto the skylight/chamber upper. Do not change geometry, camera, global exposure, emission or unlit materials.
