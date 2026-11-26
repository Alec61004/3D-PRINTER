---
task_id: TASK-072-REFERENCE-DERIVED-UPPER-ROOF-REBUILD
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:19:45+07:00
created_at: 2026-11-26T10:42:00+07:00
request: >-
  Replace the conflicting upper-roof/ceiling source relationship exposed by
  TASK-071 with a reference-derived real mesh rebuild. Lock the exterior shell
  contour to the reference, create a recessed upper chamber opening, and mount
  the real upper gantry rail inside that opening so it is visible through the
  glass without protruding or being occluded. Preserve the v33 material/light
  baseline and all passing regions.
result_path: assets/models/raw/deltrol_p2s_explorer_v40.glb
---

# TASK-072 — reference-derived upper roof/chamber rebuild

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Required reconstruction pivot

1. Use the fixed reference crop `reports/ref_printer_box.png` and the mandated
   fixture as the source for the upper roof/chamber proportions. Start from
   the best numeric baseline (v33) but replace the conflicting upper-roof,
   ceiling liner and rail mounting relationship as real 3D geometry.
2. Lock the outer silhouette before placing the interior rail: target bbox
   `W=425`, `H=408`, W/H `1.042`, aligned edges within ±3px, centered IoU
   `>=0.90`. No geometry may protrude above the shell.
3. Build a recessed chamber opening behind the intact front/top glass. Place a
   real horizontal upper rail plus plausible mounts and gantry connection in
   the opening. The rail must occupy the visible reference layer, not the
   roof-glass occluded layer. Record exact screen-space and world-space
   measurements.
4. Keep the glass as real glass; do not remove, opaque, globally recolor,
   unlit, emit, or bypass it. No billboard, image plane, screenshot texture,
   projected reference, camera change or exposure trick.
5. Preserve shell/pillar, right-window, turbine, console and chamber material
   hierarchy from v33. Any changed material must be named and justified.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v40.glb`
- `reports/task072-explorer-front.png`
- `reports/task072-explorer-left20.png`
- `reports/task072-explorer-right20.png`
- `reports/task072-explorer-elevated.png`
- `reports/task072-explorer-4view-sheet.png`
- `reports/task072-reference-candidate-contact-sheet.png`
- `reports/task072-upper-roof-rebuild-diagnostic.png`
- `reports/task072-before-after.png`
- `reports/task072-silhouette-overlay.png`
- `reports/TASK-072-antigravity-reference-derived-upper-roof-rebuild.md`
- `bridge/outbox/TASK-072-REFERENCE-DERIVED-UPPER-ROOF-REBUILD-antigravity-response.md`

Every image must be rendered from v40. The contact sheet must say
`CANDIDATE v40` and include the v40 SHA-256. The report must include old/new
hashes, a mesh/node/material manifest for the rebuilt roof/chamber/rail,
screen/world-space placement, all 15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15` with the rail visibly matching the reference landmark;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing return within reference tolerance;
- roof/rail/chamber are connected real 3D geometry in all four views;
- direct contact sheet visibly approaches the reference;
- no mislabeled evidence or analytic visual trick.

If the current asset cannot support this rebuild, use a new source mesh or
reference-derived reconstruction and document the pivot; do not claim PASS.
