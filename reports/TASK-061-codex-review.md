# Codex audit — TASK-061

- **Task:** `TASK-061-LIGHT-RIG-GLASS-FINAL-TUNE`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v29.glb`
- **Codex verdict:** `REVISION_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the light-rig diagnostic, direct front render and contact sheet.
- Verified the light parameters increased from v28 and the GLB hash changed.

## Findings

1. The light-rig path continues to produce measurable improvement: rail `30.3 → 22.4`, turbine `18.4 → 16.5`, and right glass `31.1 → 20.2`.
2. Acceptance still fails on all three target regions: rail `22.4`, turbine `16.5`, right glass `20.2`; only 12/15 ROIs pass.
3. Direct contact sheet retains PBR depth but the upper mechanics are still too pale and the right window too dark compared with the reference.
4. Because all three target errors improved, keep this path for one controlled final calibration. Do not change geometry or switch to emission/unlit.
