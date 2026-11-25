# TASK-036 Antigravity Source-Mesh Reference Calibration Report

- **Task ID**: `TASK-036-SOURCE-MESH-REFERENCE-CALIBRATION`
- **Owner**: `antigravity`
- **Generator Script**: [build_p2s_blender_pivot_v5_rev1.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_blender_pivot_v5_rev1.py)
- **Output GLB**: [deltrol_p2s_source_geometry_pivot_v5_rev1.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev1.glb) (`1,782,420` bytes)
- **Reference Image**: [printer-hero-reference-2026-11-23.png](file:///c:/Users/PC/Downloads/3DPrinter/assets/source/printer-hero-reference-2026-11-23.png)
- **Viewer Constraints Check**: `git status --short website/src` returned empty (`website/src/**` untouched).

---

## 1. Zero Image Planes / Zero 2.5D Confirmation

- Built purely in Blender `5.3.0` from beveled hard-surface meshes (`unibody_shell` Boolean cavity + side/top/front cutouts + EdgeBevel, door frame + `door_console_arch_hood`, CoreXY gantry, Sub-D `bracket_swept_arch` + 23 fins, toolhead fan rotor & PTFE bowden tube) with Cycles GPU (`OPTIX`) baked atlases (`Atlas_Unibody_Shell.png`, `Atlas_Exterior_Hardware.png`, `Atlas_Interior_Studio.png`).
- **glTF Verification** (`scripts/verify_glb.py`):
  - `Magic: glTF, Version: 2, Length: 1782420`
  - `Total nodes (62)` (`56` meshes, `NONE MAT NODES: []`)
  - `Missing required nodes: []` (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` all present)
  - Zero image planes, billboards, or 2.5D parallax rigs.

---

## 2. Calibration Changes Implemented (`v5_rev1`)

1. **Fixed White/Unassigned Gasket Material Slots (`top_rim_outer`, `left_window_gasket`, `right_window_gasket`)**:
   - Assigned a dedicated matte charcoal material (`Dark Seal Polymer`, `metallic=0.08, roughness=0.54`) and explicitly cleared blank Boolean material slots (`data.materials.clear()`) with polygon `material_index = 0` so skylights, side window seals, and console dock/bezel render crisp dark seals instead of triggering `PrinterModel.jsx`'s metallic `Graphite Door Frame` override or exporting with `None` material.
2. **Eliminated Diagonal Black Bake Artifacts Inside Chamber (`interior_rear_panel`, `interior_left_back_baffle`, `interior_floor_tray`, `interior_ceiling_liner`)**:
   - Disabled external directional studio lights during `Atlas_Interior_Studio` Cycles baking so the door frame no longer casts a hard diagonal shadow across the rear wall.
   - Inset chamber liners (`interior_rear_panel`, `interior_left_back_baffle`, `interior_floor_tray`, `interior_ceiling_liner`, and electronics shrouds) strictly inside the `cut_cavity` bounds to eliminate coplanar shell interpenetration (`RGB 0,0,0` black triangle artifacts).
   - Used centered soft dual warm point lights (`Chamber_Warm_Bounce` and `Chamber_Front_Fill`) for balanced honey-amber chamber illumination.
3. **Exterior Champagne-Titanium Tone Calibration**:
   - Adjusted `Cycles Ti Outer` (`(0.29, 0.26, 0.22)`), studio backdrop (`Strength=0.34`), front-left key (`15.5W`), front-right vertical specular ribbon (`22.0W`), and baked export scale (`base_scale=0.72, emissive_scale=0.44`) to maintain a darker champagne/titanium finish with clear forehead-to-right-side shading separation instead of washed-out pale white.

---

## 3. Audit Screenshots (`1226x708`, Chrome Headless via `tools/true3d_audit_viewer.html`)

- [task036-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-front.png) — Front 3/4 (~30°), `non-white px = 194,448`
- [task036-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-left20.png) — Rotated ~20° Left, `non-white px = 184,694`
- [task036-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-right20.png) — Rotated ~20° Right, `non-white px = 187,308`
- [task036-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-elevated.png) — Elevated (+18°), `non-white px = 218,996`
- [task036-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-4view-sheet.png) — 4-view comparison sheet

---

## 4. Honest Visual Comparison vs Hero Reference (for Codex Audit)

- **Aligned well**:
  - Clean chamfered unibody champagne-titanium finish with asymmetric front-right pillar (`R_right=0.032`) vs sharper left edge (`R_left=0.014`) and vertical highlight ribbon.
  - Dark matte skylight/side window seals (`Dark Seal Polymer`), closed smoked glass (`Smoked Glass` `opacity=0.52`), diagonal reflection band (`front_glass_sheen`), attached right handle + left hinges, and recessed trapezoid-notch console coherent across all 4 angles.
  - Warm honey-amber interior reading with gantry, steel rods, ribbed rear panel, PEI bed, and sub-D multi-fin turbine arch clear of previous black coplanar cutout artifacts.
- **Remaining differences observed honestly**:
  - **Front crop `W/H`**: Cropped printer bounding box in `task036-front.png` (`W=465, H=406, W/H=1.145`) vs cropped `printer-hero-reference-2026-11-23.png` (`W=425, H=408, W/H=1.042`) reads slightly wider at the viewer's ~30° azimuth (`(0.86, 0.22, 1.50)`).
  - **Lower-left interior corner / right shroud depth**: `task036-front.png` still shows a darker wedge near the bottom-left interior corner behind the glass reflection edge, and `interior_right_lower_shroud` remains dark on its front-facing side in `right20`.
  - **Metallic rail / PEI contrast**: Interior rails and PEI plate share the unified `Cycles Baked Interior Warm` material (`roughness=0.32, metallic=0.10`), so specular chrome contrast on X/Z rails is softer than the reference's crisp metallic sheen (can optionally preserve discrete `"Linear Guide Steel"` / `"Gold Textured PEI"` slots if Codex wants `PrinterModel.jsx` material overrides to drive them directly).

Handoff closed as `completed` with `verdict: REVISION_REQUIRED` pending Codex visual audit.
