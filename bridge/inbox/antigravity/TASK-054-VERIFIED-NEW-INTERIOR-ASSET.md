---
task_id: TASK-054-VERIFIED-NEW-INTERIOR-ASSET
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T09:14:25+07:00
created_at: 2026-11-26T09:50:00+07:00
request: >-
  TASK-053 was a no-op: deltrol_p2s_explorer_v21.glb has the exact same SHA-256 as
  v20 and the render is unchanged. Produce a genuinely different interior asset
  using a new source mesh or separately authored Blender/CAD geometry, then match
  the Deltrol reference's upper rails/toolhead and lower bed/turbine proportions.
  Preserve the accepted exterior shell and right-window glass where possible.
result_path: assets/models/raw/deltrol_p2s_explorer_v22.glb
---

# TASK-054 — Verified new interior asset

## Owner boundary

Antigravity owns the new source asset and visual implementation. Do not edit
Codex-owned website source.

## Mandatory preflight before rendering

1. Do not copy or rename v20/v21. The output must have a SHA-256 different from
   both `v20` (`84641D7DA27FE993186002694F868F9190528902257C544BAB66394C57B9E4F8`)
   and `v19` (`2144C1586105D66BAD9E00F6DC09FE70960A98DAFE09200D105A2665B5E232AC`).
2. The report must show changed GLB node/mesh inventory and identify the new
   source method. A different filename or changed texture bytes alone is not a
   source-mesh pivot.
3. Use a fresh manually authored Blender/CAD interior or a verifiable new source
   asset. Do not invoke the existing v12-v21 procedural generator unchanged.

## Geometry target

Create real 3D geometry for the reference-visible interior:

- three dark warm horizontal rails and compact upper gantry;
- smaller central carriage/toolhead with the dark intake face;
- correctly spaced vertical lead screws;
- low dark bed with a warm metallic turbine/arch print in the reference position;
- rear chamber panel and floor with the same visibility hierarchy.

No billboard, image plane, projected screenshot, camera-facing card or 2.5D
replacement is allowed.

## Material/glass constraints

- rail/turbine materials must have no emissive factor or emissive texture;
- use viewer-driven warm steel/bronze materials with visible contrast;
- preserve the v19 right-window glass appearance if possible; do not repeat the
  v20 regression;
- preserve outer shell, pillar, door/handle, console and accepted framing.

## Required evidence

Create:

- `assets/models/raw/deltrol_p2s_explorer_v22.glb`
- `reports/task054-explorer-front.png`
- `reports/task054-explorer-left20.png`
- `reports/task054-explorer-right20.png`
- `reports/task054-explorer-elevated.png`
- `reports/task054-explorer-4view-sheet.png`
- `reports/task054-reference-candidate-contact-sheet.png`
- `reports/task054-interior-before-after.png`
- `reports/task054-silhouette-overlay.png`
- `reports/TASK-054-antigravity-verified-new-interior-asset.md`
- `bridge/outbox/TASK-054-VERIFIED-NEW-INTERIOR-ASSET-antigravity-response.md`

The report must include both old/new hashes, old/new node and mesh counts,
material JSON proof of no emissive rail/turbine, exact node/primitive mapping,
fixed-fixture bbox/IoU, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- artifact hash and mesh inventory demonstrably differ from v20/v21;
- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90` and exterior silhouette retained;
- direct contact sheet visibly resembles the reference rather than the pale v20
  gantry.

If the new source asset cannot improve the direct image, report `PIVOT_REQUIRED`
with the actual blocker; do not submit another byte-identical artifact.
