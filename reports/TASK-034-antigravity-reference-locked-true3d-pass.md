# TASK-034-REFERENCE-LOCKED-TRUE3D-PASS — Antigravity Report

- **Task ID**: `TASK-034-REFERENCE-LOCKED-TRUE3D-PASS`
- **Owner**: `antigravity`
- **Result Path**: `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev2.glb`
- **Script**: `scripts/build_p2s_asset_pivot_v4_rev2.py`
- **Verdict**: `REVISION_REQUIRED` (handoff ready for Codex visual audit and integration decision)

## 1. Zero-Billboard Confirmation

**Zero image planes, zero front-facing photo billboards, and zero 2.5D depth-rigs are used.** Every structural component in `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev2.glb` is watertight, connected true-3D geometry. The subtle `front_glass_sheen` / `right_glass_sheen` meshes are single-sided (`doubleSided: false`) thin transparent optical specular layers (`alpha = 0.0` everywhere except a soft diagonal top-left studio highlight wedge fading smoothly out), preserving unobstructed real-time 3D view-through to the chamber, CoreXY gantry, toolhead, PEI plate, and turbine bracket from all angles.

## 2. Key Fidelity & Optical Fixes Implemented

1. **Restored True Single-Pass Smoked Glass Transmission (`2.1x` interior readability)**:
   - Diagnosed why `TASK-033` (`v4_rev1`) rendered the chamber interior as flat dark gray (`[59, 59, 58]`): `mat_smoked_glass` had `doubleSided: true` on closed 6-face glass boxes (`front_glass_door`, `left_glass_window`, `right_glass_window`), causing WebGL to blend BOTH front and back faces (`0.48 * 0.48 ≈ 23%` effective transmission) and stripping amber warmth.
   - Setting `double_sided=False` on `mat_smoked_glass` restored true single-pass `48%` glass transmission, lifting `Upper Chamber L` from `[52, 51, 49]` to `[120.5, 116.9, 112.9]` and `Mid Chamber L` from `[59, 59, 57]` to `[119.7, 100.9, 73.2]` while keeping crisp warm amber-to-espresso depth contrast (`ref`: `[155.1, 138.5, 123.3]` / `[141.9, 120.9, 96.4]`).
2. **Titanium-Champagne Material Calibration (eliminating dark murky CAD brown)**:
   - Because `Scene.jsx` has no `<Environment>` HDR map, `metallic = 0.20..0.25` attenuated directional diffuse reflection into darkness. Calibrating exterior baked metals to `metallic = 0.06..0.08`, `base_scale = 0.80..0.86`, and `emissive_scale = 0.54..0.60` matched `Forehead L` (`[224.6, 222.6, 219.9]` vs reference `[228.1, 224.5, 220.0]`), diagonal forehead shadow (`Forehead R = [128.4, 114.8, 102.5]` vs ref `[111.3, 101.7, 93.5]`), and shaded right beam (`Right Side Top = [99.2, 80.9, 59.8]` vs ref `[84.5, 72.0, 56.9]`).
3. **Reference-Locked Proportions & Hero Details**:
   - Widened footprint to `W = 0.444, D = 0.304, Z in [-0.194, +0.184]` (with `R_right = 0.032` fuller front-right pillar) to compensate for `PrinterModel.jsx`'s `1.12` Z-scale (`W/H` improved from `1.023` to `1.044` toward reference `1.082`).
   - Sealed 5-wall warm chamber liner (`interior_rear_panel`, `interior_ceiling_liner`, `interior_left_back_baffle`, `interior_right_lower_shroud`, `interior_rear_electronics_box`), added `x_gantry_crossbeam`, `Ref Steel Guide Rod` specular rails, refined `toolhead_front_cowl` + `toolhead_fan_bezel`, `21` dense support fins under the lofted turbine arch, sleeker door stiles/rails/handle, and compact flush console bezel.
4. **Preserved TASK-033 Base Integrity**:
   - Runtime zero-white-bleed assertion passed (`0.000` bleed across all 8 exterior metal textures), convex single-span skirts + `chassis_recessed_plinth` + centered corner feet keep all 4 angles free of wedges, gaps, or detached geometry.

## 3. GLB & Render Verification Metrics

- **GLB**: `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev2.glb` (`1,332,084` bytes, `128` nodes, `122` meshes, `30` materials, `19` embedded PNG images).
- **Required contract nodes (`5/5` present)**: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` (`Missing required nodes: []` verified by `scripts/verify_glb.py`).
- **Audit screenshots (`1226x708`, rendered with `tools/true3d_audit_viewer.html`)**:
  - `reports/task034-front.png` (`1226x708`, non-white px: `192,777`)
  - `reports/task034-left20.png` (`1226x708`, non-white px: `182,503`)
  - `reports/task034-right20.png` (`1226x708`, non-white px: `186,560`)
  - `reports/task034-elevated.png` (`1226x708`, non-white px: `219,554`)
  - `reports/task034-4view-sheet.png` (`1226x708`)

## 4. Honest Remaining Gaps vs Reference

1. `W/H` bbox (`1.044`) remains slightly taller than the hero reference (`1.082`) due in part to `Scene.jsx`'s camera elevation (`~7.25°`) vs the lower eye-level reference shot (`~3.5°`) and `PrinterModel.jsx`'s hardcoded `[1, 1, 1.12]` Z-scale.
2. `interior_right_lower_shroud` behind `right_glass_window` is clean matte dark-bronze geometry rather than stepped internal PCB/motor detail, and `Upper Chamber L` (`[120.5, 116.9, 112.9]`) remains slightly softer than the reference's `[155.1, 138.5, 123.3]`.
