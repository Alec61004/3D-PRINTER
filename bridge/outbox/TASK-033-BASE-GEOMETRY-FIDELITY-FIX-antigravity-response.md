---
task_id: TASK-033-BASE-GEOMETRY-FIDELITY-FIX
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-25T12:54:00+07:00
result_path: assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb
report_path: reports/TASK-033-antigravity-base-geometry-fidelity-fix.md
---

Completed `TASK-033-BASE-GEOMETRY-FIDELITY-FIX` (`scripts/build_p2s_asset_pivot_v4_rev1.py`) keeping the reference-derived connected true-3D pipeline with zero image planes, zero billboards, and zero 2.5D depth-rigs.

- **Root causes resolved**:
  - Removed studio white background bleed (`11.2%` in `side_bot`, `9.2%` in `pillar_l`, `33.7%` in `hinge`) from reference QUAD-unwarped surface textures with runtime `0.000` bleed assertions.
  - Closed lower-base hollow gaps with a solid full-footprint dark recessed chassis plinth (`chassis_recessed_plinth`) and watertight convex single-span chin/side skirts + inset corner rubber feet.
  - Extended `unibody_corner_0..3` seamlessly to the roof crown bevel (`Z_crown_split`), refined console placement/bezel into the compact door arch notch, and boosted linear-compensated warm amber chamber radiance through 52% smoked glass.
- **GLB artifact**: `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb` (`1,254,448` bytes, `121` nodes, `115` meshes, `28` materials, `17` images, `5/5` required nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`).
- **4-angle screenshots (`1226x708`)**: `reports/task033-front.png`, `reports/task033-left20.png`, `reports/task033-right20.png`, `reports/task033-elevated.png`, `reports/task033-4view-sheet.png`.
- **Report**: `reports/TASK-033-antigravity-base-geometry-fidelity-fix.md`.
- **`website/src/**`**: untouched.
