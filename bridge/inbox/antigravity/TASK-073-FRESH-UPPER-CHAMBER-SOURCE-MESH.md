---
task_id: TASK-073-FRESH-UPPER-CHAMBER-SOURCE-MESH
owner: antigravity
status: pending
created_at: 2026-11-26T10:48:00+07:00
request: >-
  Pivot to a fresh reference-derived source mesh for the upper chamber and
  gantry rail. Do not patch the current roof/ceiling nodes. Lock the exterior
  shell envelope to the reference first, then build a coherent recessed upper
  chamber with a visible real rail at the measured v38 depth relationship,
  preserving the v33 material/light baseline and all other passing regions.
result_path: assets/models/raw/deltrol_p2s_explorer_v41.glb
---

# TASK-073 — fresh upper-chamber source mesh

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Full source-mesh pivot

1. Build a new upper-chamber assembly from real meshes in Blender or an
   equivalent source-geometry pipeline. Do not modify the existing
   `top_roof_glass`, `interior_ceiling_liner` and rail nodes incrementally;
   replace the conflicting upper assembly as a coherent mesh group.
2. Lock the outer shell first against `reports/ref_printer_box.png`: bbox
   `W=425`, `H=408`, W/H `1.042`, aligned edges within ±3px, centered IoU
   `>=0.90`. No rail or interior piece may protrude beyond that envelope.
3. Inside the locked shell, create a recessed chamber opening, intact glass
   boundary, horizontal gantry rail, end mounts and printhead connection. Use
   v38's measured visible depth (`t≈1.600`) as a constraint, but solve the
   actual world-space geometry from the new chamber mesh rather than reusing
   the old roof intersection.
4. Preserve the exterior shell, right-side glass, turbine, bed, console and
   v33 material/light hierarchy unless the report documents a necessary
   source-mesh change. No billboard, image plane, reference projection,
   screenshot texture, emission, global unlit material, camera change or
   exposure trick.
5. Validate continuity in front, left20, right20 and elevated views. The new
   upper assembly must be one connected real 3D asset, not a front-only patch.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v41.glb`
- `reports/task073-explorer-front.png`
- `reports/task073-explorer-left20.png`
- `reports/task073-explorer-right20.png`
- `reports/task073-explorer-elevated.png`
- `reports/task073-explorer-4view-sheet.png`
- `reports/task073-reference-candidate-contact-sheet.png`
- `reports/task073-fresh-upper-chamber-diagnostic.png`
- `reports/task073-before-after.png`
- `reports/task073-silhouette-overlay.png`
- `reports/TASK-073-antigravity-fresh-upper-chamber-source-mesh.md`
- `bridge/outbox/TASK-073-FRESH-UPPER-CHAMBER-SOURCE-MESH-antigravity-response.md`

Every image must be rendered from v41. The contact sheet must say
`CANDIDATE v41` and include the v41 SHA-256. The report must include a fresh
node/mesh/material manifest, locked shell measurements, rail depth/AABB, all
15 ROIs, 12 landmarks and GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15` with visibly correct upper rail/printhead landmark;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing within reference tolerance;
- fresh upper assembly remains connected and coherent in all four views;
- direct contact sheet visibly approaches the reference;
- no stale candidate label and no analytic visual trick.

If a fresh upper assembly still cannot satisfy the reference, document the
measured geometric limitation and propose a different source asset/rebuild;
do not claim PASS.
