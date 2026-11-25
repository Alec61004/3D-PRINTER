# TASK-033-BASE-GEOMETRY-FIDELITY-FIX — Antigravity Report

- **Task ID**: `TASK-033-BASE-GEOMETRY-FIDELITY-FIX`
- **Owner**: `antigravity`
- **Result Path**: `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb`
- **Script**: `scripts/build_p2s_asset_pivot_v4_rev1.py`
- **Verdict**: `REVISION_REQUIRED` (handoff ready for Codex visual audit and integration decision)

## 1. Zero-Billboard Confirmation

**Zero image planes, zero front-facing photo billboards, and zero 2.5D depth-rigs are used.** Every mesh in `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb` is watertight, connected 3D hard-surface geometry (extruded asymmetric bevel frames, quarter-round corner pillars, convex mapped prisms, cylinders, curved Bowden tube, and a 9-station lofted turbine arch) textured with perspective-unwarped reference surface maps (`PIL.Image.Transform.QUAD`).

## 2. Root-Cause Geometry & Texture Fixes Completed

1. **Removed white studio background bleed from reference surface textures**:
   - In `TASK-032` (`v4`), `tex_side_bot` sampled `y = 502..534` across `x = 942..1038`, capturing `11.2%` studio white/gray floor beneath the side-skirt arch cutout and painting a white wedge onto both the right and left lower skirts (`mat_side_bot`), while `tex_pillar_l` (`9.2%`) and `tex_hinge` (`33.7%`) also picked up studio canvas edge pixels.
   - `build_p2s_asset_pivot_v4_rev1.py` restricts every quad crop strictly inside solid metallic regions (`tex_side_bot` sampled cleanly above the arch line and graded smoothly front-to-rear so the rear leg has no bright-tan tonal jump; `tex_left_bot` derived cleanly from front-left champagne tones), enforces edge luminance clamping, and asserts `0.000` white bleed (`>236` RGB) across all exterior metallic textures.
2. **Closed lower-base hollow gaps and replaced concave skirts**:
   - Added a full-footprint dark recessed chassis underbody plinth (`chassis_recessed_plinth`, spanning `Z_leg_bot + 0.002` to `Z_chin_top`, size `(W - 0.016, D - 0.016)`) tucked cleanly behind the side/front arches so no white background shows through the lower base from any angle (`front`, `left20`, `right20`, `elevated`).
   - Replaced concave polygon fan-triangulation skirts with watertight single-piece convex prisms (`unibody_front_chin_main`, `unibody_left_skirt_band`, `unibody_right_skirt_band`) plus flush lower leg tabs (`unibody_*_leg`), and centered all 4 `chassis_foot_0..3` pads strictly underneath the corner footprints.
3. **Continuous roof-to-foot corner pillars & front 3/4 fidelity upgrades**:
   - Extended `unibody_corner_0..3` seamlessly from `Z_leg_bot` up to `Z_crown_split` (`Z_roof_top - 0.0025`) with a non-overlapping `unibody_top_frame` crown bevel above `Z_crown_split`, eliminating the upper-right dark seam seen in `v4`.
   - Seated the angled dark-obsidian touchscreen console flush against the compact `door_console_arch_hood` notch with a sleeker dark-champagne metallic rim (`3.4:1` ratio).
   - Added `interior_ceiling_liner` and linear-compensated warm studio-amber radiance across `Ref Baked Chamber Glow`, `Ref Baked Chamber Bronze`, `Toolhead Baked Metal`, `Bracket Baked Alloy`, and `Gold Textured PEI` to maintain interior warmth behind `PrinterModel.jsx`'s forced `52%` `#12161a` `Smoked Glass` override.

## 3. GLB & Render Verification Metrics

- **GLB**: `assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb` (`1,254,448` bytes, `121` nodes, `115` meshes, `28` materials, `17` embedded PNG images).
- **Required contract nodes (`5/5` present)**: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` (`Missing required nodes: []` verified by `scripts/verify_glb.py`).
- **Audit screenshots (`1226x708`, rendered with `tools/true3d_audit_viewer.html`)**:
  - `reports/task033-front.png` (`1226x708`, non-white px: `187,344`)
  - `reports/task033-left20.png` (`1226x708`, non-white px: `176,866`)
  - `reports/task033-right20.png` (`1226x708`, non-white px: `181,823`)
  - `reports/task033-elevated.png` (`1226x708`, non-white px: `214,054`)
  - `reports/task033-4view-sheet.png` (`1226x708`)

## 4. Visual Audit Notes & Remaining Gaps vs Reference

- **Verified fixes**: Lower-right and lower-left base wedges, open side-arch white gaps, upper-right post seam, and front chin seam are eliminated across all 4 inspected angles (`front`, `left20`, `right20`, `elevated`).
- **Honest remaining differences vs `assets/source/printer-hero-reference-2026-11-23.png`**:
  1. `PrinterModel.jsx` (untouched per `Do not edit website/src/**`) still overrides `Smoked Glass` to `map: null, opacity: 0.52, #12161a`, which omits the diagonal glass reflection streak present on the hero reference photo and slightly cools internal contrast.
  2. In `Scene.jsx` (`~7.25°` camera elevation), the top bevel edge shows slightly more top-rim depth than the flatter eye-level angle (`~3.5°`) of the reference image.
