# Codex audit — TASK-049

- **Task:** `TASK-049-RAIL-TURBINE-REFERENCE-COLOR-FIX`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v17.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected `task049-rail-turbine-before-after.png`, the direct front render, the four-view sheet and the reference/candidate contact sheet.
- Verified the reported fixed-fixture framing: `423x404`, centered IoU `0.9073`.

## Findings

1. The two failing gates remain unchanged: steel rail `dMax=33.9`, turbine arch `dMax=18.7`; only 13/15 ROIs pass.
2. The before/after crop shows minimal visible change from v16 to v17 in the exact rail/turbine regions. This confirms the selected material/projection path is not controlling the rendered pixels that the fixture samples.
3. The direct candidate remains visibly wrong in the key interior hierarchy: gantry/rails/toolhead/turbine are pale and low-contrast, while the reference has dark warm metallic components with readable specular separation.
4. Framing is acceptable but does not rescue the visual mismatch. The report's `PIVOT_REQUIRED` verdict is corroborated by direct image evidence.

## Decision

Retire the v12–v17 emission-baked/high-metallicity projection family. Continue the project loop through a different material construction method: clean UVs, low-metallic viewer-driven materials, and Cycles-baked base-color/roughness maps. The next task must include an actual before/after render proving that rail and turbine pixels change, not just a material table or unchanged ROI metrics.
