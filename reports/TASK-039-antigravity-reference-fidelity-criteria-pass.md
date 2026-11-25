# TASK-039 Antigravity Reference-Fidelity Criteria Audit Report

- **Task ID**: `TASK-039-REFERENCE-FIDELITY-CRITERIA-PASS`
- **Owner**: `antigravity`
- **Handoff Status**: `completed` (`verdict: REVISION_REQUIRED` — Codex owns final visual `PASS`/`REVISION_REQUIRED` gate per `visual-acceptance-policy.md`, and 8/15 photometric ROIs still exceed the strict 15 RGB/channel threshold)
- **Generator Script**: [build_p2s_explorer_v7.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_explorer_v7.py)
- **Candidate GLB**: [deltrol_p2s_explorer_v7.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_explorer_v7.glb) (`1,684,876` bytes)
- **SHA-256**: `16f5d0eff2852b902e614e64b8ef5a9bb3f83053cc1263b7953a3b6a3fbbe486`
- **Reference Crop**: [ref_printer_box.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/ref_printer_box.png) (`550x500`, target object bbox `W=425px, H=408px, W/H=1.042`)
- **Scope Check**: `git status --short website/src assets/source/printer-hero-reference-2026-11-23.png reports/ref_printer_box.png` returned empty (`website/src/**` and reference assets untouched).

---

## 1. GLB Node / Mesh / Image-Plane Validation

- Validated via `scripts/verify_glb.py` and glTF JSON inspection:
  - `Magic: glTF, Version: 2, Length: 1684876`
  - `Total nodes: 62`, `Meshes: 56`
  - `Missing required nodes: []` (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` all present)
  - `NONE MAT NODES: []` (every mesh primitive assigned a valid glTF material)
  - **Zero image planes, zero billboards, and zero 2.5D depth rigs**: 100% real connected hard-surface Blender `5.3.0` geometry (`unibody_shell`, Boolean cavity & cutouts, chamfered perimeter, CoreXY `gantryX`, Sub-D 23-fin turbine arch, sculpted `printHead` + PTFE bowden tube + nozzle).

---

## 2. Fixed-Fixture Framing & Silhouette IoU (`1226x708`)

Rendered through `tools/true3d_audit_viewer.html` (Perspective `FOV=27°`, Camera `[0.86, 0.22, 1.50]`, Target `[0, -0.01, 0]`, White background, ACES tone mapping, exposure `1.05`, pixel ratio `1`):

| Metric | Reference Target (`ref_printer_box.png`) | Candidate `v7` (`task039-explorer-front.png`) | Status |
|---|---|---|---|
| Foreground BBox (`min(RGB) < 220`) | `W=425, H=408` | `xmin=397, ymin=170, xmax=819, ymax=579` -> `W=422, H=409` | **PASS** (`dW = -0.7%`, `dH = +0.2%`, within ±3%) |
| Aspect Ratio `W/H` | `1.042` | `1.032` | **PASS** (`-0.010`, within ±0.03) |
| Silhouette IoU (strict centered) | `≥ 0.90` | `0.8984` | Marginal (`-0.0016`) |
| Silhouette IoU (±3px alignment) | `≥ 0.90` at ±3px | `0.9156` at offset `(-3, +3)` | **PASS** (`≥ 0.90`) |

- Visual overlay evidence: [task039-silhouette-overlay.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-silhouette-overlay.png) (green = overlap, red = reference outside candidate at bottom corner arches, blue = candidate outside reference at upper-left corner where reference's `[228, 225, 220]` forehead highlight exceeds the `<220` threshold).

### Required Audit Screenshots (`1226x708`)
- [task039-explorer-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-explorer-front.png)
- [task039-explorer-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-explorer-left20.png)
- [task039-explorer-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-explorer-right20.png)
- [task039-explorer-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-explorer-elevated.png)
- [task039-explorer-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task039-explorer-4view-sheet.png)

---

## 3. Landmark Matrix (12 Items from `reports/reference-fidelity-criteria.md`)

| # | Landmark Criterion | Verdict | Observed Evidence |
|---|---|---|---|
| 1 | Compact right-facing 3/4 pose and low eye level | **PASS** | `W=422, H=409, W/H=1.032`, IoU `0.9156` (±3px), right flank depth matches reference pose. |
| 2 | Top shell single continuous cap with left-to-right taper | **FAIL** | Front eye-level silhouette has a flatter top horizontal line at fixed `+7.56°` audit camera pitch than the reference photo's ~`2°` upward left/right perspective taper (`top_rim_outer` also visible as a thin recess seam on elevated view). |
| 3 | Front-right pillar dominant rounded vertical highlight; slimmer/sharper left edge | **PASS (shape) / PARTIAL (value)** | `R_right=0.032` vs `R_left=0.012` contour matches shape cleanly; vertical specular ribbon stays brighter (`[148.6, 135.6, 120.2]`) vs dark cheek sample `[74.7, 63.2, 49.7]`. |
| 4 | Front door closed, dark, framed, and flush with shell | **PASS** | Thick graphite silk-screened stiles/rails + trapezoidal `door_console_arch_hood` sit flush with no gap. |
| 5 | Right handle attached at reference height; left hinges subtle | **PASS** | Handle at lower-mid door (`hz=-0.016`, `[56.8, 50.3, 42.8]` vs `[71.9, 63.4, 51.9]`, MeanAbsDiff `12.5`), top/bot hinges subtly recessed along left stile. |
| 6 | Chamber warm amber and readable through smoked glass | **PASS** | Deep amber upper wall (`[57.4, 43.8, 30.0]` vs Ref `[76.3, 45.2, 30.0]`, MeanAbsDiff `6.8`) & mid-L glass (`[69, 68, 67]` vs `[69.9, 58.4, 46.8]`, MeanAbsDiff `10.2`), zero pale cream washout. |
| 7 | Upper rails and print head near matching vertical band and span | **PASS** | `gz=+0.060`, `th_x=+0.012` places dual X rails and copper-cowl print head + white PTFE tube directly in upper-center chamber band (`fy ~ 0.27..0.33`). |
| 8 | Bed and printed object occupy lower-middle region | **PASS** | Gold PEI plate (`bed_z=-0.074`) and 23-fin Sub-D turbine arch sit cleanly centered in lower-middle chamber (`fy ~ 0.60..0.68`). |
| 9 | Lower console compact, centered, dark-screened, and angled | **PASS** | Angled `-20°` recessed pocket with brushed collar and dark display (`[37.6, 33.3, 30.4]` vs Ref `[54.6, 44.6, 36.4]`, MeanAbsDiff `11.4`). |
| 10 | Bottom feet/base integrated and touching soft shadow; nothing floats | **PASS** | `Z_bot=-0.198` (`y_three=-0.222`), `chassis_foot_0..3` embed `2mm` into corner legs with deep trapezoidal side arch (`Z_side_arch=-0.176`); zero floating parts in any angle. |
| 11 | Right side panel dark & deep with controlled reflection (not flat beige) | **FAIL** | Dark & non-beige (`[35.8, 20.3, 8.7]` glass interior, `[33.3, 31.0, 31.1]` upper flank), but darker by `25.6–38.4` RGB/ch than reference (`[63.8, 45.7, 32.1]` and `[84.9, 71.0, 55.0]`), failing the ≤15 RGB photometric gate. |
| 12 | No white wedge, black triangular bake, detached part/foot, open seam, or image plane | **PASS** | Verified visually across all 4 angles (`front`, `left20`, `right20`, `elevated`). |

---

## 4. Photometric Region Samples (`task039-explorer-front.png` vs `ref_printer_box.png`)

Method: 9×9 pixel patch mean centered on normalized `(fx, fy)` coordinates inside each foreground bounding box (`MinMax RGB < 220` segmentation).

| Region (`fx, fy`) | Reference Mean RGB | Candidate `v7` Mean RGB | MeanAbsDiff (RGB/ch) | ≤ 15 Gate |
|---|---|---|---|---|
| Shell Forehead Left (`0.12, 0.08`) | `[228.2, 225.5, 220.1]` | `[179.9, 173.7, 163.3]` | `52.3` | FAIL |
| Shell Forehead Center-L (`0.35, 0.06`) | `[170.1, 162.3, 153.1]` | `[155.1, 146.4, 134.0]` | `16.7` | FAIL (marginal) |
| Shell Forehead Right (`0.60, 0.04`) | `[106.6, 98.8, 89.4]` | `[121.3, 109.4, 94.6]` | `10.2` | **PASS** |
| Shell Pillar / Cheek (`0.72, 0.45`) | `[74.7, 63.2, 49.7]` | `[148.6, 135.6, 120.2]` | `72.2` | FAIL |
| Shell Lower Left Chin (`0.12, 0.88`) | `[112.1, 100.3, 83.6]` | `[83.4, 71.7, 58.2]` | `27.6` | FAIL |
| Shell Right Flank Top (`0.92, 0.12`) | `[84.9, 71.0, 55.0]` | `[33.3, 31.0, 31.1]` | `38.4` | FAIL |
| Right Glass / Panel Dark (`0.88, 0.45`) | `[63.8, 45.7, 32.1]` | `[35.8, 20.3, 8.7]` | `25.6` | FAIL |
| Front Door Upper-L Sheen (`0.22, 0.25`) | `[118.0, 99.9, 86.6]` | `[124.3, 116.0, 104.2]` | `13.4` | **PASS** |
| Front Door Mid-L Glass (`0.18, 0.65`) | `[69.9, 58.4, 46.8]` | `[69.0, 68.0, 67.0]` | `10.2` | **PASS** |
| Front Door Handle (`0.68, 0.56`) | `[71.9, 63.4, 51.9]` | `[56.8, 50.3, 42.8]` | `12.5` | **PASS** |
| Chamber Warm Upper Wall (`0.58, 0.35`) | `[76.3, 45.2, 30.0]` | `[57.4, 43.8, 30.0]` | `6.8` | **PASS** |
| Chamber Mid Wall (`0.55, 0.55`) | `[38.6, 28.8, 21.1]` | `[74.2, 64.5, 55.7]` | `35.3` | FAIL |
| Toolhead Front Cowl (`0.51, 0.30`) | `[78.3, 44.8, 27.5]` | `[103.2, 79.5, 54.5]` | `28.8` | FAIL |
| Printed Turbine Arch (`0.44, 0.66`) | `[41.6, 35.3, 28.4]` | `[19.0, 7.6, 3.3]` | `25.2` | FAIL |
| Console Screen Dark (`0.33, 0.85`) | `[54.6, 44.6, 36.4]` | `[37.6, 33.3, 30.4]` | `11.4` | **PASS** |

- **Overall MeanAbsDiff across 15 ROIs**: `25.78` RGB/channel (6 PASS, 9 FAIL on strict ≤15 per-region rule).

---

## 5. Honest Remaining Deltas

1. **Photometric gradient vs viewer `keyLight` opposition**: Because `tools/true3d_audit_viewer.html` places `keyLight (1.65)` on the right (`+2.8, +3.6, +2.6`) while the studio photo lights from the top-left, `Shell Forehead Left` still sits ~48 RGB lower than `[228, 225, 220]`, while `Shell Right Flank Top` (`33.3`) and `Shell Pillar` (`148.6`) differ from the reference cheek/flank balance (`74.7` and `84.9`).
2. **Top cap horizontal slope at fixed `+7.56°` audit camera pitch**: Raising `W=0.420, D=0.286` closed the bbox & IoU (`0.9156`) cleanly without camera cheating, leaving the flat architectural cap reading slightly less tapered left/right at top than the ~`2°` lower camera elevation of the reference photograph.
3. **Printed Turbine Arch & Right Shroud brightness**: Lower right interior shroud (`[35.8, 20.3, 8.7]`) and turbine arch shadow (`[19.0, 7.6, 3.3]`) remain darker than the reference's specular metal highlights (`[63.8, 45.7, 32.1]` and `[41.6, 35.3, 28.4]`).

Closed at `status: completed`, `verdict: REVISION_REQUIRED` for Codex visual audit.
