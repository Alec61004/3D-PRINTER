---
task_id: TASK-075-CLEAN-SOURCE-UPPER-ASSET-PIVOT
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:26:30+07:00
created_at: 2026-11-26T11:02:00+07:00
request: >-
  Abandon the current GLB upper-node editing workflow. Build a clean physical
  source asset for the Deltrol upper shell/chamber/gantry rail in a fresh
  Blender scene, then combine it with the proven v33 lower-body baseline. The
  clean upper asset must remove the old exterior-shadow path and make the
  reference rail visible while preserving the reference exterior silhouette.
result_path: assets/models/raw/deltrol_p2s_clean_upper_asset_v1.glb
---

# TASK-075 — clean-source upper asset pivot

## Owner boundary

Antigravity owns the visual/source asset and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Clean-source requirements

1. Create the upper shell/chamber/rail in a fresh Blender scene or from a
   demonstrably different physical source asset. Do not open and patch the
   existing upper nodes from v33–v42. Keep the v33 lower-body assembly only
   where it is needed for the final combined asset.
2. Model a closed champagne-metal upper enclosure matching the reference
   contour, a recessed dark chamber opening, real front/top glass, a horizontal
   gantry rail with mounts, and the printhead connection. The rail must be
   visible in the reference layer without protruding above the shell.
3. Match the fixed reference first: bbox `W=425`, `H=408`, W/H `1.042`,
   aligned edges within ±3px, centered IoU `>=0.90`. Keep the lower body,
   right flank, turbine, bed and console from v33 unless a documented interface
   is required.
4. The clean source must be real connected 3D geometry in all views. No
   billboard, image plane, screenshot texture, projected reference, emission,
   global unlit, camera change or exposure trick.
5. Prove the old shadow path is gone with an object/depth diagnostic: the
   fixed ROI 13 ray must hit the new rail/chamber geometry in the visible layer,
   not a reused roof/ceiling node or an exterior shell shadow.

## Required proof

- Source-scene or source-mesh manifest showing a new upper asset namespace and
  no reuse of old upper roof/ceiling nodes.
- A render-visible before/after demonstrating the upper chamber is not the v33
  shadowed result.
- Exact ROI 13 depth hits and world-space AABB for the new rail.

## Required evidence

- `assets/models/raw/deltrol_p2s_clean_upper_asset_v1.glb`
- `reports/task075-explorer-front.png`
- `reports/task075-explorer-left20.png`
- `reports/task075-explorer-right20.png`
- `reports/task075-explorer-elevated.png`
- `reports/task075-explorer-4view-sheet.png`
- `reports/task075-reference-candidate-contact-sheet.png`
- `reports/task075-clean-source-diagnostic.png`
- `reports/task075-source-manifest.md`
- `reports/task075-before-after.png`
- `reports/task075-silhouette-overlay.png`
- `reports/TASK-075-antigravity-clean-source-upper-asset-pivot.md`
- `bridge/outbox/TASK-075-CLEAN-SOURCE-UPPER-ASSET-PIVOT-antigravity-response.md`

Every image must be rendered from the new clean-source asset. The contact
sheet must say `CANDIDATE CLEAN-UPPER-v1` and include the artifact SHA-256.

## Acceptance gates

- ROI 13 `dMax <= 15` with a real visible rail;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing within reference tolerance;
- clean-source upper assembly is connected and coherent in all four views;
- object/depth proof shows the old shadow path is absent;
- no mislabeled evidence or analytic visual trick.

If no clean physical source can meet the constraints, report that concrete
blocker and identify a different source asset/reconstruction method; do not
claim PASS.
