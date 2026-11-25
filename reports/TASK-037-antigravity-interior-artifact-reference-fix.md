# TASK-037 Antigravity Interior Artifact & Reference Fidelity Report

- **Task ID**: `TASK-037-INTERIOR-ARTIFACT-REFERENCE-FIX`
- **Owner**: `antigravity`
- **Generator Script**: [build_p2s_blender_pivot_v5_rev2.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_blender_pivot_v5_rev2.py)
- **Candidate GLB**: [deltrol_p2s_source_geometry_pivot_v5_rev2.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev2.glb) (`1,810,644` bytes)
- **Reference Image**: [printer-hero-reference-2026-11-23.png](file:///c:/Users/PC/Downloads/3DPrinter/assets/source/printer-hero-reference-2026-11-23.png)
- **Scope Check**: `git status --short website/src` returned empty (`website/src/**` untouched).

---

## 1. Zero Image Planes / Zero 2.5D Confirmation

- **No image planes, billboards, or 2.5D depth rigs are used.**
- All enclosure, door frame, smoked glass, CoreXY gantry, toolhead, PEI build plate, and turbine arch bracket meshes are connected Blender `5.3.0` 3D hard-surface geometry with Cycles `OPTIX` baked textures.
- **glTF Contract Validation** (`scripts/verify_glb.py`):
  - `Magic: glTF, Version: 2, Length: 1810644`
  - `Total nodes (62)` (`56` meshes)
  - `Missing required nodes: []` (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` all present)
  - `NONE MAT NODES: []` (every mesh primitive has a valid glTF material assigned)

---

## 2. Root Cause Found & Source-Level Fix for Black Triangle Artifact

1. **Root Cause Traced via Three.js Raycast (`pixel 470, 440` in `task036-front.png`)**:
   - In `v5_rev1`, `cut_win_l` spanned `y in [-0.138, +0.138]` and poked inward to `x = -0.198`, crossing beyond `cut_cavity` (`x = -0.210`, `y in [-0.134, +0.134]`) while remaining coplanar with `cut_cavity` at `z = Z_chin_top (-0.138)`.
   - Blender's `EXACT` Boolean left a zero-thickness double-walled stray sheet on `unibody_shell` at `x = -0.198` (both `normal = [+1, 0, 0]` and `[-1, 0, 0]` at `pt = [-0.198, -0.13, 0.014]`), which baked pitch-black (`RGB [4, 3, 2]`) and projected diagonally across the lower-left interior behind `front_glass_door` in `front`, `right20`, and `elevated`.
2. **Source Fix Applied in `v5_rev2`**:
   - Constrained left/right side window cutouts (`y_l_min..max = -0.122..+0.122`, `y_r_min..max = -0.118..+0.118`) strictly inside the flat side span of `cut_cavity`, reduced Boolean penetration depth cleanly to `x = ±0.206..±0.250`, offset front/side cutout floors `+2mm` above `Z_chin_top` (covered cleanly by the door/window bottom gasket) to eliminate all coplanar Boolean intersections, and added an explicit `bmesh` interior-cavity stray-face purge on `unibody_shell`.
   - **Verification**: Sampling the identical coordinate `(470, 440)` in `task037-front.png` shifted cleanly from pitch-black `[4, 3, 2]` to smoked-glass/left-window interior `[98, 93, 90]`. Zero black triangular artifact appears in `front`, `left20`, `right20`, or `elevated`.
3. **Additional Calibration Improvements**:
   - Added `Chamber_Right_Fill` warm bounce lighting (`energy=3.2W` at `(0.215, -0.045, 0.020)`) and warmed `mat_chamber_shroud` (`(0.14, 0.105, 0.078)`) so `interior_right_lower_shroud` reads cleanly as brushed warm-bronze chassis detail in `right20` instead of a flat black slab.
   - Adjusted `create_glass_sheen_export_mat()` (`diag_val = (v - 0.40) - 0.68 * (u - 0.08)`) so the diagonal studio reflection concentrates cleanly in the upper-left glass corner without hazing the lower-left smoked glass.

---

## 3. Audit Screenshots (`1226x708`, Chrome Headless via `tools/true3d_audit_viewer.html`)

- [task037-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task037-front.png) — `non-white px = 194,319`, cropped printer bbox `W=465, H=406, W/H=1.145` (reference crop `W=425, H=408, W/H=1.042`)
- [task037-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task037-left20.png) — `non-white px = 184,340`
- [task037-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task037-right20.png) — `non-white px = 187,308`
- [task037-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task037-elevated.png) — `non-white px = 218,851`
- [task037-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task037-4view-sheet.png) — 4-angle overview sheet

---

## 4. Honest Remaining Deltas vs Hero Reference

- The black triangular artifact is fully eliminated across all 4 views, door handle/hinges/smoked glass/seals are coherent, and interior geometry (`gantryX`, `printHead`, `printBed`, `printedObject`) is clearly readable.
- Remaining minor visual deltas left for Codex evaluation:
  - Cropped front 3/4 aspect ratio (`W/H = 1.145` vs reference `1.042` at ~30° azimuth in `true3d_audit_viewer.html`).
  - X-gantry horizontal steel rods and gold PEI surface share the unified baked interior material (`Cycles Baked Interior Warm`), giving softer specular contrast than discrete metallic steel chrome highlights in the hero photo.
  - Under-chassis corner feet arch relief sits slightly shallower than the reference's deeper front-to-back corner arch shadow.

Closed at `status: completed` with `verdict: REVISION_REQUIRED` pending Codex visual audit.
