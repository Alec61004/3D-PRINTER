# TASK-040 Antigravity Closed Smoked-Glass Reference Pivot Report

- **Task ID**: `TASK-040-CLOSED-DOOR-REFERENCE-PIVOT`
- **Owner**: `antigravity`
- **Handoff Status**: `completed` (`verdict: REVISION_REQUIRED` — centered IoU `0.8986` sits `-0.0014` under strict unshifted `0.90` and 9/15 photometric ROIs exceed strict `15` RGB/ch limit; Codex owns final `PASS` integration verdict)
- **Generator Script**: [build_p2s_explorer_v8.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_explorer_v8.py)
- **Candidate GLB**: [deltrol_p2s_explorer_v8.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_explorer_v8.glb) (`1,675,800` bytes)
- **SHA-256**: `1a80b2c40fba8c9aba7769c57bef5803165af24ae1f6201d667ba12bf26b94ca`
- **Reference Crop**: [ref_printer_box.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/ref_printer_box.png) (`W=425px, H=408px, W/H=1.042`)
- **Scope Check**: `git status --short website/src assets/source/printer-hero-reference-2026-11-23.png reports/ref_printer_box.png` returned empty (`website/src/**` and reference files untouched).

---

## 1. Visual Pivot Summary (`v7` -> `v8`)

1. **Closed Smoked-Glass Door Optical Density & Reflection**:
   - Eliminated white background bleed through the left enclosure side (`interior_left_back_baffle` now spans the full cavity depth inside the enclosure) so the front door no longer reads as a transparent open-frame box.
   - Upgraded `Ref Glass Specular Sheen` (`front_glass_sheen`) with a full-pane dark warm smoked base (`alpha = 0.34`, RGB `22, 18, 15`) combined with an upper-left diagonal skylight reflection (`[116.9, 103.8, 89.2]` vs ref `[118.0, 99.9, 86.6]`, `MeanAbsDiff = 2.5`) and perimeter rim glint while keeping CoreXY rails, copper toolhead, PEI plate, and turbine arch readable behind the glass.
2. **Champagne-Titanium Studio Hierarchy & Top/Bottom Contour Refinement**:
   - Adjusted Cycles softbox gradient (`base_scale=0.18, emissive_scale=1.02`, reduced `l_rib` cheek glare from `6.5W` to `3.0W`, warmed right-flank base tone) bringing `Forehead Center-L` (`MeanAbsDiff = 2.7`) and `Lower Left Chin` (`MeanAbsDiff = 9.3`) within strict tolerance.
   - Applied an `8mm` 4-segment `EdgeBevel` shoulder chamfer across `unibody_shell` and embedded 4 solid corner feet (`chassis_foot_0..3`) plus darker lower plinth (`chassis_recessed_plinth`).

---

## 2. GLB Node / Mesh / Image-Plane Validation

- `Magic: glTF, Version: 2, Length: 1675800` (`File size: 1675800`)
- `Total nodes: 62`, `Meshes: 56`
- `Missing required nodes: []` (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` all present)
- `NONE MAT NODES: []` (every mesh primitive assigned a valid glTF material)
- **Zero image planes, zero billboards, zero 2.5D depth rigs.**

---

## 3. Fixed-Fixture Framing & Centered IoU (`1226x708`)

Rendered through `tools/true3d_audit_viewer.html` (Perspective `FOV=27°`, Camera `[0.86, 0.22, 1.50]`, Target `[0, -0.01, 0]`, White background, ACES, exposure `1.05`, pixel ratio `1`):

| Metric | Reference Target (`ref_printer_box.png`) | Candidate `v8` (`task040-explorer-front.png`) | Verdict |
|---|---|---|---|
| Foreground BBox (`min(RGB) < 220`) | `W=425, H=408` | `xmin=397, ymin=172, xmax=819, ymax=579` -> `W=422, H=407` | **PASS** (`-0.7%` W, `-0.2%` H) |
| Aspect Ratio `W/H` | `1.042` | `1.037` | **PASS** (`-0.005`, within ±0.03) |
| Strict Centered IoU (zero shift) | `≥ 0.90` | `0.8986` | **FAIL** (`-0.0014` short of strict `0.90`) |

- Visual overlay evidence: [task040-silhouette-overlay.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-silhouette-overlay.png)
- Audit Screenshots (`1226x708`):
  - [task040-explorer-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-explorer-front.png)
  - [task040-explorer-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-explorer-left20.png)
  - [task040-explorer-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-explorer-right20.png)
  - [task040-explorer-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-explorer-elevated.png)
  - [task040-explorer-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task040-explorer-4view-sheet.png)

---

## 4. Landmark Matrix (12 Items from `reports/reference-fidelity-criteria.md`)

| # | Landmark Criterion | Verdict | Observed Evidence |
|---|---|---|---|
| 1 | Compact right-facing 3/4 pose and low eye level | **PASS** | `W=422, H=407, W/H=1.037`, centered IoU `0.8986`; matches right flank depth and low stance. |
| 2 | Top shell single continuous cap with left-to-right taper | **FAIL** | Top cap bevel (`8mm`) rounds shoulders cleanly in `front`, but top edge remains flatter horizontally at fixed `+7.56°` audit camera than the reference's ~`2°` upward left/right perspective crown. |
| 3 | Front-right pillar dominant rounded vertical highlight; slimmer left edge | **FAIL (value)** | `R_right=0.032` vs `R_left=0.012` contour matches shape cleanly, but `fx=0.72` sample measures `[137.9, 123.1, 104.8]` vs `[74.7, 63.2, 49.7]` cheek value. |
| 4 | Front door closed, dark, framed, and flush with shell | **PASS** | Dark smoked glass overlay + flush graphite stiles/rails + arch hood immediately reads as a closed door. |
| 5 | Right handle attached at reference height; left hinges subtle | **FAIL (value)** | Handle position & attachment match cleanly across all 4 angles, though darker (`[46.5, 37.4, 28.7]` vs `[71.9, 63.4, 51.9]`, MeanAbsDiff `24.9`). |
| 6 | Chamber warm amber and readable through smoked glass | **PASS** | Upper wall `[45.9, 33.4, 22.3]` / Mid wall `[46.9, 38.3, 31.3]` (`9.3` diff) read as warm dark amber behind smoked glass without open-box glare. |
| 7 | Upper rails and print head near matching vertical band and span | **PASS** | Dual X-rails and copper cowl toolhead (`[70.6, 56.5, 43.7]`, `11.9` diff) align cleanly in upper-center chamber band. |
| 8 | Bed and printed object occupy lower-middle region | **PASS** | Gold PEI plate and 23-fin turbine arch sit in matching lower-middle band (turbine arch silhouette legible; surface value darker at `[9.8, 4.2, 2.2]`). |
| 9 | Lower console compact, centered, dark-screened, and angled | **PASS** | Centered low `-20°` dark screen (`[37.0, 32.9, 29.9]`, `11.9` diff) with metallic rim flush in arch notch. |
| 10 | Bottom feet/base integrated and touching soft shadow; nothing floats | **PASS** | Integrated plinth and 4 corner feet grounded cleanly on shadow plane across all 4 views. |
| 11 | Right side panel dark & deep with controlled reflection | **FAIL (value)** | Visual value reads dark smoked bronze-amber (`[29.3, 16.4, 6.9]` vs `[63.8, 45.7, 32.1]`), MeanAbsDiff `29.7` still exceeds `15` RGB/ch threshold. |
| 12 | No white wedge, black triangular bake, detached part/foot, open seam, or image plane | **PASS** | Verified cleanly across `front`, `left20`, `right20`, and `elevated`. |

---

## 5. Photometric Region Samples (`task040-explorer-front.png` vs `ref_printer_box.png`)

Method: 9×9 pixel patch mean centered on normalized `(fx, fy)` coordinates inside foreground bbox (`min(RGB) < 220`).

| Region (`fx, fy`) | Reference Mean RGB | Candidate `v8` Mean RGB | MeanAbsDiff (RGB/ch) | ≤ 15 Gate |
|---|---|---|---|---|
| Shell Forehead Left (`0.12, 0.08`) | `[228.2, 225.5, 220.1]` | `[197.3, 192.6, 185.2]` | `32.9` | FAIL |
| Shell Forehead Center-L (`0.35, 0.06`) | `[170.1, 162.3, 153.1]` | `[173.5, 165.7, 154.4]` | `2.7` | **PASS** |
| Shell Forehead Right (`0.60, 0.04`) | `[106.6, 98.8, 89.4]` | `[137.8, 124.7, 107.5]` | `25.1` | FAIL |
| Shell Pillar / Cheek (`0.72, 0.45`) | `[74.7, 63.2, 49.7]` | `[137.9, 123.1, 104.8]` | `59.4` | FAIL |
| Shell Lower Left Chin (`0.12, 0.88`) | `[112.1, 100.3, 83.6]` | `[105.2, 90.5, 72.4]` | `9.3` | **PASS** |
| Shell Right Flank Top (`0.92, 0.12`) | `[84.9, 71.0, 55.0]` | `[38.9, 35.9, 34.8]` | `33.7` | FAIL |
| Right Glass / Panel Dark (`0.88, 0.45`) | `[63.8, 45.7, 32.1]` | `[29.3, 16.4, 6.9]` | `29.7` | FAIL |
| Front Door Upper-L Sheen (`0.22, 0.25`) | `[118.0, 99.9, 86.6]` | `[116.9, 103.8, 89.2]` | `2.5` | **PASS** |
| Front Door Mid-L Glass (`0.18, 0.65`) | `[69.9, 58.4, 46.8]` | `[20.0, 8.0, 3.4]` | `47.9` | FAIL |
| Front Door Handle (`0.68, 0.56`) | `[71.9, 63.4, 51.9]` | `[46.5, 37.4, 28.7]` | `24.9` | FAIL |
| Chamber Warm Upper Wall (`0.58, 0.35`) | `[76.3, 45.2, 30.0]` | `[45.9, 33.4, 22.3]` | `16.7` | FAIL (marginal) |
| Chamber Mid Wall (`0.55, 0.55`) | `[38.6, 28.8, 21.1]` | `[46.9, 38.3, 31.3]` | `9.3` | **PASS** |
| Toolhead Front Cowl (`0.51, 0.30`) | `[78.3, 44.8, 27.5]` | `[70.6, 56.5, 43.7]` | `11.9` | **PASS** |
| Printed Turbine Arch (`0.44, 0.66`) | `[41.6, 35.3, 28.4]` | `[9.8, 4.2, 2.2]` | `29.7` | FAIL |
| Console Screen Dark (`0.33, 0.85`) | `[54.6, 44.6, 36.4]` | `[37.0, 32.9, 29.9]` | `11.9` | **PASS** |

- **Overall MeanAbsDiff across 15 ROIs**: `23.18` RGB/channel (6/15 strict PASS, improved from `25.78` in `v7`).

---

## 6. Honest Remaining Deltas

- Strict centered IoU (`0.8986`) remains `0.0014` shy of `0.90` due to top/bottom perspective edge mismatch between fixed `+7.56°` audit camera pitch and ~`2°` reference photo elevation.
- Lower-left smoked glass reflection (`[20.0, 8.0, 3.4]`) became darker than reference (`[69.9, 58.4, 46.8]`) after sealing `interior_left_back_baffle` + adding `0.34` smoke tint, and `Right Flank Top` (`[38.9, 35.9, 34.8]`) / `Pillar Cheek` (`[137.9, 123.1, 104.8]`) still show opposite directional lighting bias from `true3d_audit_viewer.html`'s `+X` `keyLight`.

Closed as `status: completed`, `verdict: REVISION_REQUIRED` for Codex review.
