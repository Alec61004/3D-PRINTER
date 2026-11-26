---
task_id: TASK-051-INTERIOR-MECHANICS-REFERENCE-REBUILD
owner: antigravity
status: pending
created_at: 2026-11-26T09:20:00+07:00
request: >-
  Continue the Deltrol P2S fidelity loop after TASK-050. The UV-baked material
  pivot failed: rail dMax=35.3, turbine dMax=20.1 and right-window glass regressed
  to dMax=25.5. Rebuild the visible interior mechanics from the reference rather
  than making another shader-only pass. The new true-3D model must reproduce the
  reference's compact dark warm rail/gantry/toolhead/bed/turbine arrangement and
  preserve the accepted exterior silhouette and camera framing.
result_path: assets/models/raw/deltrol_p2s_explorer_v19.glb
---

# TASK-051 — Interior mechanics reference rebuild

## Owner boundary

Antigravity owns the visual/mesh/material implementation and new GLB. Do not edit
Codex-owned website source. Read the fixed reference criteria before rendering.

## Geometry contract

Build a real connected 3D interior, with geometry—not cards or projected images—
for the visible regions:

- three readable horizontal gantry/rail members across the upper chamber;
- a compact central carriage/toolhead with a dark circular/rectangular intake and
  warm metal face, located like the reference rather than a generic white beam;
- vertical supports/lead screws that remain visible but subordinate;
- a lower dark bed with the printed metallic turbine/arch object in the same
  position, scale and warm dark contrast as the reference;
- the back chamber panel and floor shadow hierarchy needed to separate those
  parts behind the front glass.

Do not use a billboard, image plane, camera-facing card, or 2.5D replacement.
Keep the accepted shell, rounded front-right pillar, right flank, door/handle,
console and overall silhouette unless a small occlusion correction is necessary.

## Visibility/material contract

- Tune front-glass transmission/opacity so the mechanical assembly is readable
  like the reference while the glass remains physically plausible.
- Use dark warm bronze/steel materials with directional highlights and local
  contrast. Do not use global emission to fake the ROI values.
- Keep the right inspection window close to its accepted v16/v17 appearance; do
  not regress it while fixing the interior.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v19.glb`
- `reports/task051-explorer-front.png`
- `reports/task051-explorer-left20.png`
- `reports/task051-explorer-right20.png`
- `reports/task051-explorer-elevated.png`
- `reports/task051-explorer-4view-sheet.png`
- `reports/task051-reference-candidate-contact-sheet.png`
- `reports/task051-interior-before-after.png`
- `reports/task051-silhouette-overlay.png`
- `reports/TASK-051-antigravity-interior-mechanics-reference-rebuild.md`
- `bridge/outbox/TASK-051-INTERIOR-MECHANICS-REFERENCE-REBUILD-antigravity-response.md`

The report must list exact node/mesh/primitive/material assignments for the
rails, carriage/toolhead, bed, turbine and glass, then report the fixed-fixture
bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation. The before/after image
must show visible interior change; numeric tables alone are insufficient.

## Acceptance gates

- rail ROI near `(114,93,80)` and `dMax <= 15`;
- turbine ROI near `(109,88,73)` and `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90` and accepted exterior silhouette retained;
- direct contact sheet must visually resemble the reference, especially the upper
  rails/toolhead and lower printed object.

If the geometry/visibility rebuild does not materially improve the direct image,
mark `PIVOT_REQUIRED` and propose a different source asset or construction method;
do not repeat a shader-only revision.
