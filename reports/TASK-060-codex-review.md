# Codex audit — TASK-060

- **Task:** `TASK-060-INTERIOR-LIGHT-RIG-CALIBRATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v28.glb`
- **Codex verdict:** `REVISION_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the light-rig diagnostic, direct front render and contact sheet.
- Verified the report's embedded `KHR_lights_punctual` rig and its before/after values.

## Findings

1. The local light rig is a valid improvement: rail `dMax 35.5 → 30.3` and turbine `19.6 → 18.4`. The diagnostic proves the lights affect the intended interior.
2. Acceptance still fails: rail `30.3`, turbine `18.4`, right-window glass `31.1`; only 12/15 ROIs pass.
3. Direct contact sheet is still too pale/low-contrast in the upper assembly, and the right window is darker than the reference.
4. This is a meaningful improvement, so continue the light-rig path rather than retiring it. Tune light placement/intensity and glass separately; do not alter geometry or revert to emission/unlit.
