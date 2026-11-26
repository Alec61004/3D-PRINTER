---
task_id: TASK-066-RAIL-ONLY-CALIBRATION
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:03:25+07:00
created_at: 2026-11-26T14:10:00+07:00
request: >-
  Continue from v33, which has 14/15 ROI passes and turbine dMax=14.5. Only the
  rail ROI fails at dMax=34.7 because PBR baseColor compensation is clamped or
  receives no direct light. Calibrate only the actual rail primitive/material to
  reach dMax <= 15 while preserving v33 turbine, right glass, skylight and
  chamber passes. Regenerate every evidence image from v34 with correct labels.
result_path: assets/models/raw/deltrol_p2s_explorer_v34.glb
---

# TASK-066 — Rail-only calibration

## Owner boundary

Antigravity owns the rail material calibration and evidence. Do not edit Codex
website source. Start from v33; do not change geometry, camera, exposure, light
rig, turbine, glass or other materials.

## Required rail calibration

1. Target only the actual mesh supplying ROI 13: `x_gantry_crossbeam` /
   `mech_gantry_rail_bot` and its assigned rail material.
2. Use a controlled rail-only material solution. A `KHR_materials_unlit` fallback
   is allowed only on that real rail mesh if PBR cannot illuminate the recessed
   surface; it must use calibrated warm base color, remain true 3D, and must not
   flatten the rest of the interior. No billboard, image plane, screenshot or
   emission is allowed.
3. Preserve v33's turbine pass, right-window glass pass, skylight pass and
   chamber-upper pass within the same thresholds.

## Evidence integrity preflight

- v34 hash must differ from v33.
- Report old/new material JSON for the rail primitive and prove zero emissive.
- Every image must be rendered from v34. The contact sheet must say
  `CANDIDATE v34` and include the v34 SHA-256; never reuse a v31/v32/v33 label.
- The rail before/after crop must have different pixels and show the sampled RGB
  moving toward `(114,93,80)`.

## Required output

- `assets/models/raw/deltrol_p2s_explorer_v34.glb`
- `reports/task066-explorer-front.png`
- `reports/task066-explorer-left20.png`
- `reports/task066-explorer-right20.png`
- `reports/task066-explorer-elevated.png`
- `reports/task066-explorer-4view-sheet.png`
- `reports/task066-reference-candidate-contact-sheet.png`
- `reports/task066-rail-material-diagnostic.png`
- `reports/task066-before-after.png`
- `reports/task066-silhouette-overlay.png`
- `reports/TASK-066-antigravity-rail-only-calibration.md`
- `bridge/outbox/TASK-066-RAIL-ONLY-CALIBRATION-antigravity-response.md`

The report must include old/new hashes, exact rail primitive/material JSON,
fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI `dMax <= 15`;
- turbine ROI `dMax <= 15` and not worse than v33;
- right glass, skylight and chamber upper each `dMax <= 15` and not worse than
  v33;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct v34 contact sheet visibly approaches the reference;
- no emission/global exposure/camera trick and no mislabeled evidence.

If the rail-only path cannot move ROI 13 without breaking the other passes,
report `PIVOT_REQUIRED` with direct evidence instead of changing unrelated parts.
