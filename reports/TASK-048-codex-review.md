# Codex audit — TASK-048

- **Task:** `TASK-048-DEBUG-REFERENCE-PROJECTION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v16.glb`
- **Codex verdict:** `REVISION_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified the GLB is glTF 2.0 with 63 nodes, 56 meshes, 18 materials, 40 PNG images and 40 textures.
- Verified the named rail/turbine/toolhead nodes and the claimed material names exist in the GLB JSON.
- Verified SHA-256: `7A2B456F3423DB677E336436DCDAD65052AED215CB09ACEFDE95C590A29FD3A2`.
- Inspected the direct diagnostic, front render, 4-view sheet and reference/candidate contact sheet.

## Findings

1. The report's own hard gates fail: `13_Steel_Rail` has `dMax=33.9` and `14_Turbine_Arch` has `dMax=18.7`; only 13/15 ROIs pass.
2. The v15 and v16 panels in `task048-projection-diagnostic.png` are visually near-identical in the failing mechanical regions. The claimed projection pass therefore did not materially change the rendered rail/turbine appearance.
3. The contact sheet shows the global mismatch that the ROI table does not capture: the candidate's gantry, rails, toolhead and turbine/bed assembly remain pale and low-contrast, while the reference has dark warm metallic parts with clear specular separation and a readable printed object.
4. Framing is acceptable (`423x404`, centered IoU `0.9073`), but framing is not a substitute for geometry/material fidelity.

## Required next action

Continue the loop with TASK-049. The next revision must prove that the exact rail and turbine primitives receive the intended rendered color/material change, using an explicit before/after render and node-to-primitive/material/texture mapping. If the next attempt produces no visible change in those regions, retire the current projection/material path and pivot rather than adding more shader tweaks.
