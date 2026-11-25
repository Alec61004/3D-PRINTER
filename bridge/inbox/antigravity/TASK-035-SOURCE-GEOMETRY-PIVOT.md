---
task_id: TASK-035-SOURCE-GEOMETRY-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T13:45:00+07:00
completed_at: 2026-11-25T13:55:00+07:00
request: Pivot away from the exhausted v4 reference-derived quad/loft pipeline. Inspect the existing source geometry in assets/models/optimized/deltrol_p2s_optimized.glb and use it or a new Blender hard-surface reconstruction as the geometric base, then apply reference-derived materials/details to real surfaces. Produce a stable, connected true-3D printer that matches the supplied reference front 3/4 much more closely. Do not use image planes, billboards, or 2.5D depth-rigs, and do not edit website/src/**.
result_path: assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb
---

# Task 035 — Source-geometry pipeline pivot

Codex audit has rejected three successive v4 pipeline attempts (TASK-032/033/034): they remain simplified box reconstructions and their material/light tuning has not reached the reference. This task must use a different geometry foundation.

## Required approach

1. Inspect `assets/models/optimized/deltrol_p2s_optimized.glb` first. If its topology/proportions are closer to the real printer, use it as the geometric base and improve it; otherwise rebuild with Blender hard-surface modeling from the reference and any local/free multi-view evidence.
2. Use reference-derived PBR/material maps only on actual curved/volumetric surfaces. No front-facing photo plane, billboard, facade quad, or 2.5D depth-rig may form the body or silhouette.
3. Keep all parts physically attached and genuinely rotatable; preserve door, glass, base and feet integrity.

Reference:

`assets/source/printer-hero-reference-2026-11-23.png`

## Deliverable

`assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb`

Required contract nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

## Acceptance evidence

- `reports/task035-front.png`
- `reports/task035-left20.png`
- `reports/task035-right20.png`
- `reports/task035-elevated.png`
- `reports/task035-4view-sheet.png`
- `reports/TASK-035-antigravity-source-geometry-pivot.md`
- `bridge/outbox/TASK-035-SOURCE-GEOMETRY-PIVOT-antigravity-response.md`

All screenshots must be 1226×708. The front view must be materially closer to the reference in silhouette, material, glass/door, console, warm chamber and interior detail than TASK-034. State explicitly whether image planes are used. If it is still a generic box or any geometry disconnects, report `REVISION_REQUIRED` or `BLOCKED`; do not claim PASS from GLB loadability.
