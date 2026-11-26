---
task_id: TASK-056-SCREENSPACE-INTERIOR-CALIBRATION
owner: antigravity
status: pending
created_at: 2026-11-26T10:30:00+07:00
request: >-
  Continue after TASK-055. v23 changed mesh inventory but the fixed ROI 13/14
  pixels stayed exactly at rail dMax=35.1 and turbine dMax=20.4, proving the new
  parts were placed outside the sampled screen regions. Use the fixed camera
  projection to calibrate a new true-3D interior assembly so the actual rail and
  turbine primitives occupy the reference ROI 13/14 screen-space locations. Also
  restore the right-window glass to dMax <= 15.
result_path: assets/models/raw/deltrol_p2s_explorer_v24.glb
---

# TASK-056 — Screen-space calibrated interior

## Owner boundary

Antigravity owns the visual/mesh/material asset. Do not edit Codex-owned website
source. Use the fixed fixture and reference criteria.

## Calibration contract

1. Render with the exact fixed camera: `1226x708`, FOV `27°`, camera
   `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure
   `1.05`.
2. Use the fixture projection/raycast to identify the 2D location and visible
   depth of ROI 13 (`Steel_Rail`) and ROI 14 (`Turbine_Arch`). Place the actual
   rail and turbine geometry so it covers those locations in the rendered front
   view. Do not move only a material or add geometry outside the sampled region.
3. Produce a coverage/ownership overlay that labels the screen pixels of ROI 13
   and ROI 14 with the exact mesh node/primitive that supplies them. The overlay
   must be accompanied by a before/after crop showing changed pixels versus v23.
4. Keep the geometry true 3D and usable from left/right/elevated views. No
   billboard, image plane, projected screenshot, camera-facing card or 2.5D
   replacement.

## Visual target

- upper rails: three compact dark warm metal rails with reference thickness and
  spacing, not pale floating bars;
- toolhead: centered at the reference's upper-chamber position with dark intake
  and warm metal face;
- lower bed/turbine: same visible placement, width and warm dark contrast as the
  reference;
- right-window glass: restore accepted warm smoked appearance without hiding the
  outer shell or changing framing.

## Hard material constraints

- no emissive factor or emissive texture on rail/turbine materials;
- no global exposure/camera trick used to pass the ROI;
- report exact material JSON and node/primitive mapping.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v24.glb`
- `reports/task056-explorer-front.png`
- `reports/task056-explorer-left20.png`
- `reports/task056-explorer-right20.png`
- `reports/task056-explorer-elevated.png`
- `reports/task056-explorer-4view-sheet.png`
- `reports/task056-reference-candidate-contact-sheet.png`
- `reports/task056-roi-coverage-overlay.png`
- `reports/task056-interior-before-after.png`
- `reports/task056-silhouette-overlay.png`
- `reports/TASK-056-antigravity-screenspace-interior-calibration.md`
- `bridge/outbox/TASK-056-SCREENSPACE-INTERIOR-CALIBRATION-antigravity-response.md`

The report must include old/new hash and inventory, ROI coverage ownership,
fixed-fixture bbox/IoU, all 15 ROI values, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- coverage overlay proves ROI 13/14 are supplied by the intended true-3D
  primitives;
- direct contact sheet visibly resembles the reference.

If the intended primitives still do not own the sampled pixels, report
`PIVOT_REQUIRED` with the projection evidence instead of claiming material work.
