---
task_id: TASK-068-REAL-RAIL-GEOMETRY-INSERT
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:10:45+07:00
created_at: 2026-11-26T10:18:00+07:00
request: >-
  Continue from v33/v35 baseline. TASK-067 object/depth raycast proved that
  ROI 13 is not a steel rail: the reference rail region is currently occupied
  by top_roof_glass over interior_ceiling_liner and rear_electronics_box.
  Add the missing real mechanical rail geometry at that proven location so
  the fixed front render matches the reference landmark and ROI 13 moves
  toward the reference without damaging the 14 existing ROI passes.
result_path: assets/models/raw/deltrol_p2s_explorer_v36.glb
---

# TASK-068 — real 3D rail geometry insert

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Geometry requirements

1. Start from `assets/models/raw/deltrol_p2s_explorer_v33.glb` (or v35 only
   after proving the binary is identical). Restore normal v33 materials; do
   not inherit v34's shared-material unlit change.
2. Use the TASK-067 raycast and the fixed fixture to derive and record the
   world-space placement for the missing upper horizontal rail under
   `top_roof_glass`. It must be a genuine connected mechanical mesh with
   thickness, end structure and correct perspective, not a flat camera-facing
   plane or screenshot.
3. The rail may be a new named mesh/node with an isolated warm dark-steel PBR
   material. It must be geometrically aligned to the existing gantry/printhead
   assembly and remain coherent in front, left20, right20 and elevated views.
4. Do not change camera, exposure, global lights, shell, glass, turbine,
   chamber or console materials. No `KHR_materials_unlit` for the interior,
   no emission compensation, no texture projection, no billboard and no
   2.5D overlay.
5. If the rail must appear behind glass, keep the glass physically intact and
   prove the rail is visible through it without turning the glass opaque or
   recoloring unrelated regions.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v36.glb`
- `reports/task068-explorer-front.png`
- `reports/task068-explorer-left20.png`
- `reports/task068-explorer-right20.png`
- `reports/task068-explorer-elevated.png`
- `reports/task068-explorer-4view-sheet.png`
- `reports/task068-reference-candidate-contact-sheet.png`
- `reports/task068-rail-geometry-diagnostic.png`
- `reports/task068-before-after.png`
- `reports/task068-silhouette-overlay.png`
- `reports/TASK-068-antigravity-real-rail-geometry-insert.md`
- `bridge/outbox/TASK-068-REAL-RAIL-GEOMETRY-INSERT-antigravity-response.md`

Every image must be rendered from v36. The contact sheet must say
`CANDIDATE v36` and include the v36 SHA-256; do not reuse a v31/v33/v35
caption. The report must include node/mesh/material details for the inserted
rail, world-space placement, old/new hashes, all 15 ROIs, 12 landmarks and
GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15`;
- ROIs 01–12, 14 and 15 remain `PASS` and no worse than v33;
- centered IoU `>= 0.90`, silhouette unchanged, no floating/detached parts;
- upper rail/printhead landmark visibly approaches the reference;
- all four views show one coherent real 3D asset;
- no mislabeled evidence or analytic visual trick.

If the rail cannot be placed without changing unrelated regions, report the
measured obstruction and a concrete next geometry pivot; do not claim PASS.
