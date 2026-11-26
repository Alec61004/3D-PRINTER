# Codex audit — TASK-063

- **Task:** `TASK-063-TURBINE-SPILL-LIGHT-SEPARATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v31.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the spill-separation diagnostic, direct front render and contact sheet.
- Verified the local light rig changes and fixed-fixture metrics.

## Findings

1. Point-light separation improved ROI 07 glass to `14.0` and ROI 12 chamber upper to `13.7`, but it lost the mechanical targets: rail `18.1`, turbine `17.6`, skylight `16.5`.
2. The diagnostic and contact sheet confirm the expected omnidirectional spill tradeoff; increasing point intensity brightens the wrong regions.
3. Framing remains acceptable (`IoU 0.9073`), and no emission/unlit shortcut was introduced.

## Decision

Pivot the light rig from omnidirectional points to aimed narrow-cone spot lights. Preserve the v31 PBR materials and geometry, and retain the right-glass/chamber values where possible while aiming light directly at rail/turbine surfaces.
