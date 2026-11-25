# TASK-038 Antigravity Hybrid Reference-Locked Hero + True-3D Explorer Report

- **Task ID**: `TASK-038-HYBRID-REFERENCE-3D-EXPLORER-PIVOT`
- **Owner**: `antigravity`
- **Status**: `completed` (`verdict: REVISION_REQUIRED` — pipeline pivot pending Codex audit before integration; not claimed as `PASS`)
- **Scope Check**: `git status --short website/src assets/source/printer-hero-reference-2026-11-23.png` returned empty (`website/src/**` and reference hero asset untouched).

---

## 1. Two-Asset Hybrid Handoff Declaration

1. **Default Reference-Locked Hero (`assets/source/printer-hero-reference-2026-11-23.png`)**:
   - **Exact reference image, not a 3D reconstruction**: Kept bit-for-bit unchanged (`212,909` bytes, `1226x708`, SHA-256 `2D8B25482C66E54FDA31073A6C5EA2382BE0F1AD709636FEC63064EF42E8D7E0`). Not repainted, warped, or wrapped on any billboard/plane.
   - Recommended role: Default landing hero presentation visual before the user enters interactive 3D exploration/rotation mode (Codex implements mode switch in `website/src/**`).
2. **True-3D Explorer Candidate (`assets/models/raw/deltrol_p2s_explorer_v6.glb`)**:
   - **Real connected 3D hard-surface geometry**: Built from [build_p2s_explorer_v6.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_explorer_v6.py) in Blender `5.3.0` (`Cycles OPTIX` baked atlases), containing **zero billboards, image planes, or 2.5D facades**.
   - **Contract Validation** (`scripts/verify_glb.py`):
     - File: [deltrol_p2s_explorer_v6.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_explorer_v6.glb) (`1,812,916` bytes)
     - `Total nodes (62)` (`56` meshes, `NONE MAT NODES: []`)
     - `Missing required nodes: []` — required nodes `enclosure`, `door`, `front_glass_door`, `printHead`, and `printBed` are all present and parented cleanly.
   - **Structural Cleanliness Across Rotations**:
     - Zero wedges, detached panels, floating feet (`chassis_foot_0..3` embed cleanly into corner legs at `Z = -0.190` / `chassis_recessed_plinth`), or black bake triangle artifacts in any angle (`front`, `left20`, `right20`, `elevated`).

---

## 2. Explorer Visual Verification (`1226x708`, Chrome Headless via `tools/true3d_audit_viewer.html`)

- [task038-explorer-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task038-explorer-front.png) — Front 3/4 (`non-white px = 194,319`, cropped printer `W=465, H=406, W/H=1.145`)
- [task038-explorer-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task038-explorer-left20.png) — Rotated ~20° Left (`non-white px = 184,340`)
- [task038-explorer-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task038-explorer-right20.png) — Rotated ~20° Right (`non-white px = 187,308`)
- [task038-explorer-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task038-explorer-elevated.png) — Elevated +18° (`non-white px = 218,851`)
- [task038-explorer-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task038-explorer-4view-sheet.png) — 4-view sheet

---

## 3. Honest Remaining Visual Differences in Explorer Mode (vs Reference Photo)

1. **Not pixel-identical to the studio hero photo**: Derived from a single front-3/4 source view, so hidden flanks, under-arch curvature, and micro-chamfers differ slightly from studio photography.
2. **Proportion & silhouette framing**: Cropped front 3/4 bounding box in `tools/true3d_audit_viewer.html` (`W/H = 1.145`) sits slightly wider horizontally than the cropped hero reference (`W/H = 1.042`).
3. **Interior specular & material separation**: CoreXY X-guide rails, belt gantry, gold PEI build plate, and turbine arch share `Cycles Baked Interior Warm` (`metallic=0.10, roughness=0.32`), producing softer matte-metallic sheen than the crisp polished chrome rail reflections and high-contrast CNC anodized textures in the hero photo.
4. **Under-chassis corner feet arch**: Corner arch cutoffs (`cut_arch_l`, `cut_arch_r`) are subtly shallower than the deeper contoured foot taper visible along the reference bottom edge.
5. **Chamber reflection contrast**: `front_glass_sheen` provides a controlled upper-left softbox studio diagonal veil, leaving the lower chamber cleanly legible across rotation angles rather than matching the exact environment bounce of the photographed room.

Handoff submitted as pipeline pivot (`verdict: REVISION_REQUIRED`) for Codex audit and hybrid UI integration.
