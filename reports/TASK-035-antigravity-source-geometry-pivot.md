# TASK-035-SOURCE-GEOMETRY-PIVOT — Antigravity Report

- **Task ID**: `TASK-035-SOURCE-GEOMETRY-PIVOT`
- **Owner**: `antigravity`
- **Result Path**: `assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb`
- **Script**: `scripts/build_p2s_blender_pivot_v5.py`
- **Verdict**: `REVISION_REQUIRED` (handoff ready for Codex visual audit and integration decision)

## 1. Inspection of Existing Candidate & Pipeline Pivot Decision

1. **Inspected `assets/models/optimized/deltrol_p2s_optimized.glb`**:
   - Confirmed `227,140` bytes, `20` nodes, `14` meshes, `288` triangles using `Photoreal_Facade_PBR` + `photoreal_facade_layer` + `chassis_depth_backing` (a 2.5D facade/billboard slab box).
   - Rejected as geometric base because it does not meet the true-3D hard-surface silhouette requirement.
2. **Pivoted to Blender 5.3.0 Hard-Surface Reconstruction + Cycles GPU (`RTX 3050 OPTIX`) Studio Baking**:
   - Authored `scripts/build_p2s_blender_pivot_v5.py` using Blender `bpy`, `bmesh`, non-coplanar `Boolean` cutouts, `Bevel` (`3` segments), and `Subsurf` modifiers (`2` levels).
   - **Zero image planes / zero billboards / zero 2.5D depth-rigs**: Every body panel, corner radius, window bay, skylight bezel, hinge, handle, CoreXY gantry rail/belt/pulley/drag-chain, toolhead intake fan rotor, PEI bed, and turbine arch bracket is genuine rotatable 3D geometry. (`front_glass_sheen` and `right_glass_sheen` are thin single-sided transparent RGBA specular glint layers fading smoothly to `alpha = 0.0` outside the top-left diagonal highlight, preserving full 3D view-through.)

## 2. Hard-Surface Geometry & Cycles Baking Highlights

- **Single seamless beveled unibody (`unibody_shell`)**: Asymmetric rounded prism (`W = 0.448`, `D = 0.306`, `Z in [-0.194, +0.184]`, `R_left = 0.015`, `R_right = 0.032`) with Boolean cutouts for front door bay, side windows, top skylight well (`top_rim_outer`), lower side arches, recessed front chin, and rear service bay (`rear_panel_insert`, `rear_exhaust_shroud`, `rear_ac_module`), beveled (`2.4mm`, `3` segments) + weighted smooth normals.
- **Sealed lower base & contract hierarchy**: `chassis_recessed_plinth` + 4 beveled `chassis_foot_0..3` pads eliminate bottom wedges/gaps; all 5 required contract nodes (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`) plus `gantryX` and `printedObject` (`bracket_swept_arch` Sub-D + `bracket_apex_ring` + 23 `bracket_support_fins`) are intact.
- **Single-pass `Smoked Glass` (`doubleSided: false`)**: Prevents WebGL double-blending across closed panes so the Cycles-baked warm honey-amber interior glow (`Cycles Warm LED` bars + chamber radiosity) reads clearly behind `52%` `#12161a` glass (`Upper Chamber L = [127.4, 118.5, 100.4]`, `Mid Chamber L = [120.5, 98.7, 63.6]`).
- **3 Disjoint Cycles OPTIX Atlases**:
  - `Atlas_Unibody_Shell` (`1024x1024`, dedicated to `unibody_shell`, `12` samples + OpenImageDenoise)
  - `Atlas_Exterior_Hardware` (`512x512`, `14` exterior hardware objects)
  - `Atlas_Interior_Studio` (`1024x1024`, `43` interior chamber, CoreXY, toolhead, bed & turbine objects)

## 3. Verification Metrics

- **GLB**: `assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb` (`1,602,824` bytes, `85` nodes, `79` meshes).
- **Required nodes (`5/5` present)**: `['enclosure', 'door', 'front_glass_door', 'printHead', 'printBed']` (`Missing required nodes: []` verified by `scripts/verify_glb.py`).
- **Audit screenshots (`1226x708`, captured from `tools/true3d_audit_viewer.html` via Chrome CDP)**:
  - `reports/task035-front.png`: `1226x708`, non-white px = `190,275` (`W/H = 1.049` vs reference `1.082`)
  - `reports/task035-left20.png`: `1226x708`, non-white px = `181,907`
  - `reports/task035-right20.png`: `1226x708`, non-white px = `187,825`
  - `reports/task035-elevated.png`: `1226x708`, non-white px = `221,381`
  - `reports/task035-4view-sheet.png`: `1226x708` composite

## 4. Honest Comparison & Remaining Gaps vs Reference

- **Major structural & material gains**: Eliminated the segmented box slabs of `v4` with true Boolean/bevel Blender hard-surface topology, added real rear exhaust/AC hardware, CoreXY belts/steppers/pulleys, articulated 14-link drag chain, recessed 7-blade toolhead turbine fan, and Cycles radiosity baking with zero lower-base wedges or white bleed.
- **Remaining gaps vs `assets/source/printer-hero-reference-2026-11-23.png`**:
  1. **Lighting gradient on chin & forehead**: `Forehead L` (`[192.4, 180.7, 164.8]`) and `Forehead R` (`[176.4, 163.3, 145.2]`) have softer diagonal contrast than the reference (`[228, 225, 220]` -> `[111, 102, 94]`), while the lower front chin reflects slightly warmer/brighter ivory than the mid-tone champagne reference chin, and the bottom-right side skirt bevel reflects brighter studio light than the darker side panel above it.
  2. **Right window border thickness**: `right_window_gasket` appears slightly thin/gray at the outer bevel edge compared with the thicker dark smoked-glass frame in the reference.
  3. **Aspect ratio (`W/H = 1.049` vs `1.082`)**: Slightly constrained by `PrinterModel.jsx`'s untouched `scale = [1, 1, 1.12]` and `Scene.jsx`'s camera pitch (`~7.25°`).
