---
task_id: TASK-069-ROOF-CEILING-CLEARANCE-BLENDER-PIVOT
owner: antigravity
status: pending
created_at: 2026-11-26T10:24:00+07:00
request: >-
  Pivot from the occluded rail insertion in v36. Rebuild the upper roof/ceiling
  clearance relationship with a real source-geometry/Blender pass so the
  reference's dark horizontal upper rail is physically visible through the
  intact top/front glass at fixed ROI 13. Preserve v33's 14 passing ROI values
  and the exterior silhouette.
result_path: assets/models/raw/deltrol_p2s_explorer_v37.glb
---

# TASK-069 — roof/ceiling clearance geometry pivot

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Required source-geometry pivot

1. Start from v33 as the numeric/material baseline; do not carry v34's unlit
   materials or v36's hidden rail placement without proving the correction.
2. Use Blender or an equivalent real-mesh pipeline to remodel the upper
   roof/ceiling/rail mounting relationship. The rail must occupy a physically
   plausible unobstructed chamber position below the glass, with enough
   clearance to be visible in the mandated front render and still connected to
   the gantry/printhead assembly.
3. Preserve the top roof glass as real glass. Do not make it opaque, remove it,
   recolor it globally, or use an emission/material trick to fake visibility.
4. Preserve camera, exposure, global light rig, shell, right glass, turbine,
   chamber and console materials. No billboard, image plane, projected
   reference, screenshot texture, or 2.5D overlay.
5. The rail should be a real mechanical assembly (bar plus plausible mounts or
   end blocks), not an isolated floating box. Record the new node/mesh/material
   names, world-space AABB and the clearance from the glass and ceiling liner.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v37.glb`
- `reports/task069-explorer-front.png`
- `reports/task069-explorer-left20.png`
- `reports/task069-explorer-right20.png`
- `reports/task069-explorer-elevated.png`
- `reports/task069-explorer-4view-sheet.png`
- `reports/task069-reference-candidate-contact-sheet.png`
- `reports/task069-roof-rail-clearance-diagnostic.png`
- `reports/task069-before-after.png`
- `reports/task069-silhouette-overlay.png`
- `reports/TASK-069-antigravity-roof-ceiling-clearance-blender-pivot.md`
- `bridge/outbox/TASK-069-ROOF-CEILING-CLEARANCE-BLENDER-PIVOT-antigravity-response.md`

Every image must be rendered from v37. The contact sheet must say
`CANDIDATE v37` and include the v37 SHA-256. The report must include old/new
hashes, clearance measurements, all 15 ROIs, 12 landmarks, and GLB
validation.

## Acceptance gates

- ROI 13 `dMax <= 15` and visible rail pixels move toward reference;
- ROIs 01–12, 14 and 15 remain `PASS` and no worse than v33;
- centered IoU `>= 0.90`, exterior silhouette and framing preserved;
- rail/printhead landmark visibly approaches reference in front view;
- all four views show one coherent real 3D asset with no floating/detached
  geometry;
- no mislabeled evidence and no shader/camera/exposure trick.

If the source geometry cannot be remade without collateral damage, report the
measured obstruction and a concrete alternate mesh/source pivot; do not claim
PASS.
