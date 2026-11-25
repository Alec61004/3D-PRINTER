---
task_id: TASK-035-SOURCE-GEOMETRY-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-25T13:55:00+07:00
result_path: assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb
report_path: reports/TASK-035-antigravity-source-geometry-pivot.md
---

Completed `TASK-035-SOURCE-GEOMETRY-PIVOT` (`scripts/build_p2s_blender_pivot_v5.py`), pivoting away from the exhausted `v4` builder and rejecting `deltrol_p2s_optimized.glb` (`288`-tri `Photoreal_Facade_PBR` box) in favor of a fresh **Blender 5.3.0 Hard-Surface Reconstruction + Cycles RTX 3050 OPTIX Studio Baking** pipeline with zero image planes, zero billboards, and zero 2.5D depth-rigs.

- **Geometry & optical upgrades**:
  - Seamless beveled `unibody_shell` carved with Boolean door/window/skylight/arch/rear-bay cutouts + weighted normals; `chassis_recessed_plinth` & 4 beveled feet keep all views sealed with zero gaps or white wedges.
  - Added `rear_exhaust_shroud`, `rear_ac_module`, CoreXY belts/pulleys/steppers, 14-link `drag_chain_assembly`, recessed 7-blade `toolhead_fan_rotor`, Sub-D lofted `bracket_swept_arch` + 23 `bracket_support_fins`, single-pass `Smoked Glass` (`doubleSided: false`), and corner `front_glass_sheen` / `right_glass_sheen` optical highlights.
  - Baked 3 disjoint Cycles OPTIX atlases (`Atlas_Unibody_Shell` 1024px, `Atlas_Exterior_Hardware` 512px, `Atlas_Interior_Studio` 1024px).
- **GLB artifact**: `assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb` (`1,602,824` bytes, `85` nodes, `79` meshes, `5/5` contract nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`).
- **4-angle screenshots (`1226x708`)**: `reports/task035-front.png`, `reports/task035-left20.png`, `reports/task035-right20.png`, `reports/task035-elevated.png`, `reports/task035-4view-sheet.png`.
- **Report**: `reports/TASK-035-antigravity-source-geometry-pivot.md`.
- **`website/src/**`**: untouched.
