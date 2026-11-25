# TASK-041 Antigravity Product Silhouette & Lighting Pivot Report

- **Task ID**: `TASK-041-PRODUCT-SILHOUETTE-LIGHTING-PIVOT`
- **Owner**: `antigravity`
- **Handoff Status**: `completed` (`verdict: REVISION_REQUIRED` — centered IoU `0.9154` & framing bbox `420x406` PASS strict gates, while 9/15 photometric ROIs and Landmark #3/#11 still sit outside ≤15 RGB/ch pending Codex audit)
- **Generator Script**: [build_p2s_explorer_v9.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_explorer_v9.py)
- **Candidate GLB**: [deltrol_p2s_explorer_v9.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_explorer_v9.glb) (`1,776,436` bytes)
- **SHA-256**: `16bf9c70072ab315e6431d6b5710f1229627dd34e58eb961d9cb43db487a608b`
- **Reference Crop**: [ref_printer_box.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/ref_printer_box.png) (`W=425px, H=408px, W/H=1.042`)
- **Scope Check**: `git status --short website/src assets/source/printer-hero-reference-2026-11-23.png reports/ref_printer_box.png` returned empty (`website/src/**` and reference files untouched).

---

## 1. Geometry & Lighting Pivot Summary (`v8` -> `v9`)

1. **Sculpted Architectural Cap Taper & Corner-Foot Grounding**:
   - Rebuilt `make_asym_rounded_prism()` with smooth architectural top-cap perimeter taper (`top_drop_x=0.012, top_drop_y=0.014` peaking at the front-right pillar shoulder) over `W=0.422, D=0.282, Z_bot=-0.197, Z_top=+0.184` and lowered recessed `top_rim_outer` / `top_roof_glass` (`Z_top - 0.022 .. -0.014`) cleanly inside the chamfered cap.
   - Grounded `chassis_foot_0..3` solidly on the contact plane shadow, lifting **zero-shift centered IoU** cleanly from `0.8986` (`v8`) to **`0.9154`** (`≥ 0.90` PASS).
2. **Spatially Varying Front & Right Glass Treatments**:
   - Replaced `v8`'s dark brown/charcoal base overlay with warm taupe smoked sheen (`88, 74, 60` at `alpha=0.22`) blending into a crisp upper-left skylight reflection wedge (`Glass_Sheen_RGBA.png`), plus a dedicated warm-amber smoked sheen (`Right_Glass_Sheen_RGBA.png`, `alpha=0.28`) on `right_glass_sheen`.
   - Improved handle (`MeanAbsDiff = 0.5`), turbine arch (`9.6`), and right smoked glass (`9.7`), reducing aggregate 15-ROI error (`23.18 -> 21.52`).

---

## 2. GLB Node / Mesh / Image-Plane Validation

- `Magic: glTF, Version: 2, Length: 1776436` (`File size: 1776436`)
- `Total nodes: 62`, `Meshes: 56`
- `Missing required nodes: []` (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` all present)
- `NONE MAT NODES: []` (all mesh primitives have valid glTF materials)
- **Zero image planes, zero billboards, and zero 2.5D depth rigs.**

---

## 3. Fixed-Fixture Framing & Centered IoU (`1226x708`)

Rendered via `tools/true3d_audit_viewer.html` unchanged (Perspective `FOV=27°`, Camera `[0.86, 0.22, 1.50]`, Target `[0, -0.01, 0]`, White background, ACES tone mapping, exposure `1.05`, pixel ratio `1`):

| Metric | Reference Target (`ref_printer_box.png`) | Candidate `v9` (`task041-explorer-front.png`) | Verdict |
|---|---|---|---|
| Foreground BBox (`min(RGB) < 220`) | `W=425, H=408` | `xmin=399, ymin=172, xmax=819, ymax=578` -> `W=420, H=406` | **PASS** (`-1.2%` W, `-0.5%` H, within ±3%) |
| Aspect Ratio `W/H` | `1.042` | `1.034` | **PASS** (`-0.008`, within ±0.03) |
| **Centered IoU (zero shift)** | `≥ 0.90` | **`0.9154`** | **PASS** |

- Silhouette Overlay: [task041-silhouette-overlay.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-silhouette-overlay.png)
- Audit Screenshots (`1226x708`):
  - [task041-explorer-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-explorer-front.png)
  - [task041-explorer-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-explorer-left20.png)
  - [task041-explorer-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-explorer-right20.png)
  - [task041-explorer-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-explorer-elevated.png)
  - [task041-explorer-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task041-explorer-4view-sheet.png)

---

## 4. Landmark Matrix (12 Items from `reports/reference-fidelity-criteria.md`)

| # | Landmark Criterion | Verdict | Observed Evidence |
|---|---|---|---|
| 1 | Compact right-facing 3/4 pose and low eye level | **PASS** | `W=420, H=406, W/H=1.034`, centered IoU **`0.9154`**; exact pose match. |
| 2 | Top shell single continuous cap with left-to-right taper | **PASS (silhouette) / PARTIAL (detail)** | Sculpted cap taper brings centered IoU to `0.9154` with no open seam, though left-to-right drop is smoother/gentler than the photo's slight right-shoulder bevel. |
| 3 | Front-right pillar dominant rounded vertical highlight; slimmer left edge | **FAIL (value)** | Contour matches shape (`R_right=0.032` vs `R_left=0.012`), but cheek sample `[141.1, 125.9, 107.0]` remains brighter than right flank `[102.4, 91.1, 79.1]` (vs Ref cheek `74.7` < flank `84.9`). |
| 4 | Front door closed, dark, framed, and flush with shell | **PASS** | Closed smoked glass + flush graphite stiles/rails + arch hood immediately read as closed. |
| 5 | Right handle attached at reference height; left hinges subtle | **PASS** | Handle (`[73.0, 63.6, 52.1]` vs Ref `[71.9, 63.4, 51.9]`, `MeanAbsDiff = 0.5`) and left hinges match position & value across all 4 angles. |
| 6 | Chamber warm amber and readable through smoked glass | **FAIL (value)** | Reads clearly as warm amber chamber behind glass without pale blowout, though mid rear wall (`[92.3, 75.8, 61.3]` vs `[38.6, 28.8, 21.1]`) is brighter than reference (`47.0` diff). |
| 7 | Upper rails and print head near matching vertical band and span | **PASS (shape) / FAIL (cowl value)** | Rails and print head align accurately in upper-center chamber; toolhead cowl (`[105.6, 85.3, 64.2]`) runs brighter than reference (`[78.3, 44.8, 27.5]`). |
| 8 | Bed and printed object occupy lower-middle region | **PASS** | Gold PEI plate (`bed_z=-0.074`) and 23-fin turbine arch (`[37.5, 23.9, 15.2]` vs Ref `[41.6, 35.3, 28.4]`, `MeanAbsDiff = 9.6`) match position and readability. |
| 9 | Lower console compact, centered, dark-screened, and angled | **PASS** | Low centered `-20°` dark console (`[40.4, 36.0, 32.5]`, `MeanAbsDiff = 8.9`) cleanly nestled into arch pocket. |
| 10 | Bottom feet/base integrated and touching soft shadow; nothing floats | **PASS** | Integrated plinth and corner feet sit solidly grounded across all 4 views. |
| 11 | Right side panel dark & deep with controlled reflection | **PASS (glass) / FAIL (flank)** | Right glass sample matches closely (`[60.6, 35.6, 16.2]` vs `[63.8, 45.7, 32.1]`, `MeanAbsDiff = 9.7`), while top right flank (`[102.4, 91.1, 79.1]`) runs `+20.6` bright. |
| 12 | No white wedge, black triangular bake, detached part/foot, open seam, or image plane | **PASS** | Clean across `front`, `left20`, `right20`, and `elevated`. |

---

## 5. Photometric Region Samples (`task041-explorer-front.png` vs `ref_printer_box.png`)

Method: 9×9 pixel patch mean centered on normalized `(fx, fy)` inside foreground bbox (`min(RGB) < 220`).

| Region (`fx, fy`) | Reference Mean RGB | Candidate `v9` Mean RGB | MeanAbsDiff (RGB/ch) | ≤ 15 Gate |
|---|---|---|---|---|
| Shell Forehead Left (`0.12, 0.08`) | `[228.2, 225.5, 220.1]` | `[210.9, 206.8, 200.7]` | `18.5` | FAIL (marginal) |
| Shell Forehead Center-L (`0.35, 0.06`) | `[170.1, 162.3, 153.1]` | `[175.3, 166.1, 153.3]` | `3.1` | **PASS** |
| Shell Forehead Right (`0.60, 0.04`) | `[106.6, 98.8, 89.4]` | `[142.1, 127.6, 108.1]` | `27.7` | FAIL |
| Shell Pillar / Cheek (`0.72, 0.45`) | `[74.7, 63.2, 49.7]` | `[141.1, 125.9, 107.0]` | `62.1` | FAIL |
| Shell Lower Left Chin (`0.12, 0.88`) | `[112.1, 100.3, 83.6]` | `[126.4, 112.0, 93.3]` | `11.9` | **PASS** |
| Shell Right Flank Top (`0.92, 0.12`) | `[84.9, 71.0, 55.0]` | `[102.4, 91.1, 79.1]` | `20.6` | FAIL |
| Right Glass / Panel Dark (`0.88, 0.45`) | `[63.8, 45.7, 32.1]` | `[60.6, 35.6, 16.2]` | `9.7` | **PASS** |
| Front Door Upper-L Sheen (`0.22, 0.25`) | `[118.0, 99.9, 86.6]` | `[141.1, 130.9, 115.8]` | `27.8` | FAIL |
| Front Door Mid-L Glass (`0.18, 0.65`) | `[69.9, 58.4, 46.8]` | `[58.1, 32.2, 18.0]` | `22.3` | FAIL |
| Front Door Handle (`0.68, 0.56`) | `[71.9, 63.4, 51.9]` | `[73.0, 63.6, 52.1]` | `0.5` | **PASS** |
| Chamber Warm Upper Wall (`0.58, 0.35`) | `[76.3, 45.2, 30.0]` | `[84.9, 69.7, 52.3]` | `18.5` | FAIL (marginal) |
| Chamber Mid Wall (`0.55, 0.55`) | `[38.6, 28.8, 21.1]` | `[92.3, 75.8, 61.3]` | `47.0` | FAIL |
| Toolhead Front Cowl (`0.51, 0.30`) | `[78.3, 44.8, 27.5]` | `[105.6, 85.3, 64.2]` | `34.8` | FAIL |
| Printed Turbine Arch (`0.44, 0.66`) | `[41.6, 35.3, 28.4]` | `[37.5, 23.9, 15.2]` | `9.6` | **PASS** |
| Console Screen Dark (`0.33, 0.85`) | `[54.6, 44.6, 36.4]` | `[40.4, 36.0, 32.5]` | `8.9` | **PASS** |

- **Overall MeanAbsDiff across 15 ROIs**: `21.52` RGB/channel (6/15 strict PASS, improved from `25.78` in `v7` and `23.18` in `v8`).

---

## 6. Honest Remaining Deltas

- **Pillar Cheek vs Right Flank inversion & Chamber Mid brightness**: Raising `Fill_Right` (`34W`) during Cycles bake also lifted the rounded cheek (`141.1`) above the right flank (`102.4`) instead of darkening the cheek below flank (`74.7` vs `84.9`), and `Chamber_Warm_Bounce = 8.5W` over-brightened `Chamber Mid Wall` (`92.3` vs `38.6`) and `Toolhead Cowl` (`105.6` vs `78.3`).
- **Mid-L Glass Tint Hue**: Warm taupe smoke (`88, 74, 60`) over brown wall reads warmer/redder (`[58.1, 32.2, 18.0]`) than reference's neutral smoked shadow (`[69.9, 58.4, 46.8]`).

Closed at `status: completed`, `verdict: REVISION_REQUIRED` for Codex audit.
