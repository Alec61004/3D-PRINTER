---
task_id: TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION
owner: antigravity
status: pending
created_at: 2026-11-26T10:36:00+07:00
request: >-
  Integrate the successful v38 depth-calibrated rail into the printer shell.
  The rail now passes ROI 13 at dMax=10.2 but protrudes above the exterior and
  breaks five other ROIs. Rebuild/reshape the upper roof, chamber ceiling and
  rail mounts, or perform a measured rail-fit adjustment, so the real rail
  remains visible in the chamber while staying inside the reference shell
  envelope and restoring the v33 ROI baseline.
result_path: assets/models/raw/deltrol_p2s_explorer_v39.glb
---

# TASK-071 — rail/shell envelope integration

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Required integration

1. Start from v38's successful depth relationship, but use the v33 material and
   light baseline. Do not restore the hidden v36/v37 placement.
2. Keep the real upper rail assembly in the visible chamber layer (the depth
   that made ROI 13 pass), then fit its length, mounts and roof/ceiling
   geometry inside the exterior shell envelope. No detached parts above the
   roof, no floating boxes, no billboard/image plane, no projected texture,
   no emission, no global unlit material, and no camera/exposure change.
3. Preserve the reference exterior bbox: target `W=425`, `H=408`, W/H `1.042`,
   aligned edges within ±3px, and centered IoU `>=0.90`. The rail must remain a
   plausible connected mechanical assembly in front/left20/right20/elevated.
4. Preserve `top_roof_glass` and front glass as intact real glass; do not make
   the shell transparent or globally recolor it. If the roof needs a recess,
   model a real recess and keep the visible outer contour unchanged.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v39.glb`
- `reports/task071-explorer-front.png`
- `reports/task071-explorer-left20.png`
- `reports/task071-explorer-right20.png`
- `reports/task071-explorer-elevated.png`
- `reports/task071-explorer-4view-sheet.png`
- `reports/task071-reference-candidate-contact-sheet.png`
- `reports/task071-rail-shell-fit-diagnostic.png`
- `reports/task071-before-after.png`
- `reports/task071-silhouette-overlay.png`
- `reports/TASK-071-antigravity-rail-shell-envelope-integration.md`
- `bridge/outbox/TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION-antigravity-response.md`

Every image must be rendered from v39. The contact sheet must say
`CANDIDATE v39` and include the v39 SHA-256. The report must include old/new
hashes, rail depth/AABB, shell-envelope measurements, all 15 ROIs, 12
landmarks and GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15` and visible rail landmark retained;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing return within reference tolerance;
- no protruding/detached/floating geometry in any required view;
- direct contact sheet visibly approaches the reference;
- no mislabeled evidence or analytic visual trick.

If the successful depth cannot fit inside the current shell without changing
the outer contour, report the measured conflict and propose a new source mesh
or reference-derived reconstruction; do not claim PASS.
