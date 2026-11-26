---
task_id: TASK-057-PHOTOMETRIC-MATERIAL-THROUGH-GLASS
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T09:27:45+07:00
created_at: 2026-11-26T10:50:00+07:00
request: >-
  Continue from TASK-056 using v24 geometry. The ROI coverage overlay proves the
  intended rail/turbine primitives own the sampled screen regions, but final
  pixels remain rail dMax=35.1, turbine dMax=20.4 and right glass dMax=26.0.
  Do not add or reposition more geometry. Calibrate the actual non-emissive
  material and smoked-glass path so the fixed viewer produces the reference
  rail/turbine/glass colors.
result_path: assets/models/raw/deltrol_p2s_explorer_v25.glb
---

# TASK-057 — Photometric material-through-glass calibration

## Owner boundary

Antigravity owns the GLB material calibration and evidence. Do not edit Codex
website source. Keep v24 geometry and ROI ownership unless an occlusion defect is
proven by the diagnostic.

## Calibration requirements

1. Start from the v24 geometry/coverage. Do not add pale bars, black disks or new
   screen-space geometry as a substitute for material correction.
2. For the exact primitives owning ROI 13 and ROI 14, calibrate base color and
   roughness against three measured stages:
   - material rendered without front glass;
   - same material viewed through the actual front glass;
   - final fixed-fixture output.
3. Use non-emissive materials. A `KHR_materials_unlit` material is allowed only
   as a controlled fallback on the actual rail/turbine mesh if PBR cannot match
   through the glass; it must remain genuine 3D geometry and cannot use an image
   or billboard. Do not use emission.
4. Calibrate the right-window glass separately so its final ROI returns to the
   reference warm-smoked value instead of v24's dark regression.
5. Preserve v24 ROI ownership and exterior framing; do not change camera,
   exposure or global lighting to hide the mismatch.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v25.glb`
- `reports/task057-explorer-front.png`
- `reports/task057-explorer-left20.png`
- `reports/task057-explorer-right20.png`
- `reports/task057-explorer-elevated.png`
- `reports/task057-explorer-4view-sheet.png`
- `reports/task057-reference-candidate-contact-sheet.png`
- `reports/task057-material-through-glass-diagnostic.png`
- `reports/task057-interior-before-after.png`
- `reports/task057-silhouette-overlay.png`
- `reports/TASK-057-antigravity-photometric-material-through-glass.md`
- `bridge/outbox/TASK-057-PHOTOMETRIC-MATERIAL-THROUGH-GLASS-antigravity-response.md`

The diagnostic must show raw-material, glass-on and final pixels for ROI 13,
ROI 14 and ROI 07, with exact node/primitive/material mapping. The report must
include GLB JSON proof of zero emissive rail/turbine materials, fixed-fixture
bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- diagnostic proves the final pixels changed because of the intended material/
  glass path, not a camera or exposure change;
- contact sheet visibly improves the warm-dark mechanical hierarchy.

If the material-through-glass diagnostic cannot move the intended pixels, report
`PIVOT_REQUIRED` and identify the exact renderer/asset limitation. Do not add
another geometry patch without evidence of occlusion.
