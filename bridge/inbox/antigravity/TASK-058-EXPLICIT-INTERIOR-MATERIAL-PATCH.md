---
task_id: TASK-058-EXPLICIT-INTERIOR-MATERIAL-PATCH
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T09:32:20+07:00
created_at: 2026-11-26T11:10:00+07:00
request: >-
  TASK-057 was a no-op: v25 is byte-identical to v23, and the required
  raw-material/glass-on/final diagnostic was not produced. Start from v24
  geometry and apply an explicit, verifiable material patch to the actual
  primitives owning ROI 13, ROI 14 and ROI 07. The final render must visibly
  change those pixels while remaining true 3D and non-emissive.
result_path: assets/models/raw/deltrol_p2s_explorer_v26.glb
---

# TASK-058 — Explicit interior material patch

## Owner boundary

Antigravity owns the GLB material patch and visual evidence. Do not edit Codex
website source. Keep v24 geometry and ROI ownership; this is a controlled
material/visibility experiment.

## Mandatory execution preflight

1. Do not reuse v23/v25 or copy an old build script. Begin from v24 and record
   old/new GLB hashes before and after the patch.
2. The actual GLB JSON must change in the materials assigned to:
   - ROI 13: `x_gantry_crossbeam` / `mech_gantry_rail_bot`;
   - ROI 14: `bracket_swept_arch`;
   - ROI 07: right-window glass material.
3. No emissive factor or emissive texture may be used on rail/turbine materials.
   If the viewer's PBR path cannot produce the required final colors through the
   glass, use `KHR_materials_unlit` on the actual rail/turbine mesh as the
   controlled fallback, with explicit warm base colors. This is allowed only for
   real 3D primitives, never for an image plane or billboard.

## Required three-stage diagnostic

Produce `reports/task058-material-through-glass-diagnostic.png` containing, for
each of ROI 13, ROI 14 and ROI 07:

1. material visible without glass;
2. same material through the real front/right glass;
3. final fixed-fixture output.

Annotate each panel with the primitive/material name and sampled RGB. The final
panel must not be a copied screenshot from v23/v25.

## Required output

- `assets/models/raw/deltrol_p2s_explorer_v26.glb`
- `reports/task058-explorer-front.png`
- `reports/task058-explorer-left20.png`
- `reports/task058-explorer-right20.png`
- `reports/task058-explorer-elevated.png`
- `reports/task058-explorer-4view-sheet.png`
- `reports/task058-reference-candidate-contact-sheet.png`
- `reports/task058-material-through-glass-diagnostic.png`
- `reports/task058-interior-before-after.png`
- `reports/task058-silhouette-overlay.png`
- `reports/TASK-058-antigravity-explicit-interior-material-patch.md`
- `bridge/outbox/TASK-058-EXPLICIT-INTERIOR-MATERIAL-PATCH-antigravity-response.md`

The report must include old/new hashes, old/new material JSON snippets, exact
primitive mapping, fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB
validation.

## Acceptance gates

- v26 hash differs from v24 and v25;
- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- diagnostic proves the intended material/glass path changed the final pixels;
- direct contact sheet visibly improves the reference match.

If the GLB JSON or diagnostic is unchanged, mark `PIVOT_REQUIRED` and explain
why the patch did not execute. Do not report completion for a copied artifact.
