---
task_id: TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION
owner: antigravity
status: in_progress
created_at: 2026-11-26T13:45:00+07:00
request: >-
  Continue from TASK-064. Spot lights solved spill but not the recessed rail and
  turbine: rail dMax=35.5, turbine dMax=15.8. Preserve the v32 spotlight rig
  and geometry, then apply controlled compensation only to the actual primitive
  materials supplying ROI 13 and ROI 14. Do not use global exposure, emission or
  a whole-scene unlit fallback. Regenerate all screenshots/contact sheets from
  the actual v33 artifact and correct every label/hash.
result_path: assets/models/raw/deltrol_p2s_explorer_v33.glb
---

# TASK-065 — Rail/turbine material compensation

## Owner boundary

Antigravity owns the GLB material patch and visual evidence. Do not edit Codex
website source. Start from v32 and preserve its spotlight rig, geometry and
spill-suppression behavior.

## Required implementation

1. Keep v32's narrow spot lights or an equivalent aimed rig that passes skylight,
   chamber upper and right glass.
2. Modify only the materials on the actual primitives supplying ROI 13 and ROI
   14 (`x_gantry_crossbeam`/`mech_gantry_rail_bot` and `bracket_swept_arch`).
   Use calibrated base color/roughness/specular compensation so the recessed
   surfaces reach the reference through the glass.
3. Do not use emissive factor/texture, global exposure, camera changes or a
   whole-scene `KHR_materials_unlit` fallback. If unlit is experimentally used,
   it may be used only on the two failing primitives and must be documented.
4. Preserve the v32 right-window glass and spill-pass values.

## Evidence integrity preflight

- v33 hash must differ from v32.
- The GLB JSON material values for the named primitives must differ from v32 and
  be printed in the report.
- Every screenshot filename below must be rendered from v33. The contact sheet
  title must say `CANDIDATE v33` and include the v33 SHA-256; no v31/v32 label is
  acceptable.
- The before/after and diagnostic files must have different content and show the
  material change; do not duplicate one file under two names.

## Required output

- `assets/models/raw/deltrol_p2s_explorer_v33.glb`
- `reports/task065-explorer-front.png`
- `reports/task065-explorer-left20.png`
- `reports/task065-explorer-right20.png`
- `reports/task065-explorer-elevated.png`
- `reports/task065-explorer-4view-sheet.png`
- `reports/task065-reference-candidate-contact-sheet.png`
- `reports/task065-material-compensation-diagnostic.png`
- `reports/task065-before-after.png`
- `reports/task065-silhouette-overlay.png`
- `reports/TASK-065-antigravity-rail-turbine-material-compensation.md`
- `bridge/outbox/TASK-065-RAIL-TURBINE-MATERIAL-COMPENSATION-antigravity-response.md`

The report must include old/new hashes, exact material JSON and primitive mapping,
fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass, skylight and chamber upper each `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct v33 contact sheet visibly approaches the reference;
- no emission/global exposure/camera trick and no mislabeled evidence.

If compensation cannot move the intended primitive pixels without breaking the
spill passes, report `PIVOT_REQUIRED` with direct evidence.
