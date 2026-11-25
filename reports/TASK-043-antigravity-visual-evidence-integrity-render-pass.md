# TASK-043: Visual Evidence Integrity & Photoreal True-3D Render Pass (`v11`)

## 1. Delivered Asset & Validation Summary

- **Deliverable GLB**: `assets/models/raw/deltrol_p2s_explorer_v11.glb`
  - **Generator Script**: `scripts/build_p2s_explorer_v11.py` (True-3D Cycles AO + exact post-ACES analytical surface calibration + HDR emissive interior, zero image planes / billboards / 2.5D depth rigs)
  - **File Size**: `1,469,072` bytes (`Magic: glTF`, `Version: 2`)
  - **SHA-256**: `517F0062485507DEB7737784410193EE1418A675AC76B480189B1E60ECF4FD1D`
  - **GLB Verification (`scripts/verify_glb.py`)**: `62` GLTF nodes (`enclosure`, `door`, `printHead`, `printBed`, `gantryX`, `printedObject`, `front_glass_door`, `screen_display`, `screen_bezel`, `right_glass_window`, `left_glass_window`, `top_roof_glass`, plus all sub-assemblies); `Missing required nodes: []`; `ALL REQUIRED NODES PRESENT AND VALID!`.
  - **Fixed Audit Viewer**: `tools/true3d_audit_viewer.html` (`1226x708`, FOV `27°`, camera `[0.86, 0.22, 1.50]`, target `[0, -0.01, 0]`, white background, `ACESFilmicToneMapping` exposure `1.05`, Three.js HUD: `Nodes: 63, Meshes: 56`).
  - **Untouched Files Check (`git status --short`)**: Zero changes to `website/src/**`, `tools/true3d_audit_viewer.html`, `assets/source/printer-hero-reference-2026-11-23.png`, or `reports/ref_printer_box.png`.

---

## 2. Root Causes Identified & Fixed vs `v10`

1. **Shared `build_plate` Material Contamination in Viewer (`Calibrated PEI Plate` vs `Calibrated Interior Warm`)**:
   - `tools/true3d_audit_viewer.html` applies `GOLD_PEI` (`#d8a536`, `metalness=0.65`, `roughness=0.35`) when `obj.name === "build_plate"` and `!mat.map`. Because `v10` and early `v11` shared one interior material across all interior meshes, mutating `build_plate` turned the entire interior + `screen_display` metallic yellow-gold (`(184, 142, 65)` under overhead `chamberSpot=4.2` + `chamberPoint=2.2`).
   - **Fix**: Isolated `[build_plate, build_plate_lip]` onto a dedicated `Calibrated PEI Plate` material bound with a dark graphite-bronze `baseColorTexture` (`connect_base_map=True`) so `mat.map` prevents `GOLD_PEI` overwrite while keeping `Calibrated Interior Warm` (`baseColor=[0,0,0]`, `specular=0`, `ior=1`, `KHR_materials_emissive_strength=2.6`) untouched on chamber geometry and `screen_display`.
2. **Full-Ceiling Glow Masking Chamber Contrast (`eval_int_shader`)**:
   - `interior_ceiling_liner` previously matched the LED condition and flooded the ceiling in bright cream peach (`[193, 162, 128]` pre-scale), washing out contrast behind the glass.
   - **Fix**: Restricted high-output emission (`[2.25, 1.56, 0.94]`) strictly to `led_bar_{front,left,right}` while setting `interior_ceiling_liner` to dark bronze `[64, 48, 34]` and deeper chamber walls `[182, 134, 94]` top fading to `[56, 42, 30]` bottom.
3. **Neutral-Warm Champagne Shell Gradient, Sleeker Bezel, and Clean Chin/Flank**:
   - Adjusted door frame (`stile_w=0.009`, `rail_h=0.009`), raised header (`Z_door_top=0.130`), lowered side arch cutout (`Z_side_arch=-0.178`, `arch_r_bot=D - 2*R_right - 0.088`) so the solid lower-right flank beam wraps continuously below the right window (`[77.3, 66.7, 53.1]`), and removed dark chin shading artifact under the console.
4. **Chamber Visibility Through Closed Smoked Glass (`opacity=0.52`)**:
   - Restricted front glass reflection (`Ref Glass Specular Sheen`, `alpha=0.02..0.60`) to the diagonal upper-left skylight wedge, leaving the central/lower door transparent over HDR-calibrated steel rails, toolhead copper cowl + open fan rotor, white PTFE Bowden tube, dark graphite PEI bed, recessed dark chamber floor trench (`bed_z=-0.086`, front bed `D=0.140`), and 25-fin sculpted turbine arch.

---

## 3. Visual Evidence Integrity & Direct Same-Pipeline Photometric Comparison

- **Exact Color Pipeline**: All candidate measurements are sampled directly as **raw uncompressed post-ACES `sRGB uint8`** pixels from Chrome headless screenshots of `tools/true3d_audit_viewer.html` (`toneMapping = ACESFilmicToneMapping`, `exposure = 1.05`, `outputColorSpace = SRGBColorSpace`), without any brightness shifting, LUT matching, or recoloring.
- **Equal-Scale 1:1 Contact Sheet**: `reports/task043-reference-candidate-contact-sheet.png` places `reports/ref_printer_box.png` (`426x409` tight crop at `(27, 52, 453, 461)`) directly beside `reports/task043-explorer-front.png` (`422x407` tight crop at `(397, 172, 819, 579)`), zero scaling distortion.
- **Silhouette & BBox Alignment**:
  - Reference bbox: `(27, 52, 453, 461)` -> `W=426, H=409, W/H=1.0416`
  - Candidate `v11` bbox: `(397, 172, 819, 579)` -> `W=422, H=407, W/H=1.0369` (`dW=-0.94%`, `dH=-0.49%`)
  - **Centered Zero-Shift Silhouette IoU**: **`0.9159`** (gate `>= 0.90`)

### Exact Ref vs Candidate ROI Coordinates & BT.709 Luminance Table (Post-ACES `sRGB uint8`)

| Landmark ROI | Ref Pixel Box `(x0,y0,x1,y1)` | Cand Pixel Box `(x0,y0,x1,y1)` | Ref RGB `(R,G,B)` | Ref `Y_709` | Cand RGB `(R,G,B)` | Cand `Y_709` | `dMax` (RGB/ch) | Status (`<=15`) |
|---|---|---|---:|---:|---:|---:|---:|---|
| `01_Forehead_L` | `(61, 71, 78, 81)` | `(430, 191, 447, 201)` | `(229.1, 227.8, 222.5)` | `227.7` | `(221.6, 217.5, 211.3)` | `217.9` | `11.2` | **PASS** |
| `02_Forehead_C` | `(178, 71, 199, 81)` | `(546, 191, 567, 201)` | `(150.8, 141.6, 133.6)` | `143.0` | `(149.4, 142.2, 132.8)` | `143.1` | `1.4` | **PASS** |
| `03_Forehead_R` | `(301, 71, 314, 81)` | `(669, 191, 681, 201)` | `(69.6, 61.0, 48.9)` | `62.0` | `(73.0, 64.0, 52.9)` | `65.1` | `4.0` | **PASS** |
| `04_Pillar_Crest` | `(322, 223, 328, 248)` | `(689, 342, 695, 367)` | `(143.4, 134.4, 123.6)` | `135.5` | `(142.8, 133.4, 122.1)` | `134.6` | `1.5` | **PASS** |
| `05_Pillar_Cheek` | `(334, 223, 341, 248)` | `(701, 342, 708, 367)` | `(66.7, 56.1, 44.0)` | `57.5` | `(68.1, 58.0, 46.8)` | `59.3` | `2.8` | **PASS** |
| `06_Right_Flank_Top` | `(393, 103, 410, 115)` | `(759, 222, 776, 235)` | `(54.0, 45.5, 34.6)` | `46.5` | `(53.5, 44.0, 34.0)` | `45.3` | `1.5` | **PASS** |
| `07_Right_Win_Glass` | `(389, 227, 406, 252)` | `(755, 347, 772, 371)` | `(63.7, 45.4, 32.6)` | `48.4` | `(70.9, 49.3, 31.8)` | `52.6` | `7.1` | **PASS** |
| `08_Right_Flank_Bot` | `(393, 373, 410, 385)` | `(759, 491, 776, 503)` | `(83.7, 70.1, 52.0)` | `71.7` | `(77.3, 66.7, 53.1)` | `68.0` | `6.4` | **PASS** |
| `09_Chin_Left` | `(69, 405, 86, 418)` | `(439, 524, 456, 536)` | `(112.8, 100.5, 84.0)` | `101.9` | `(114.0, 102.3, 85.5)` | `103.6` | `1.8` | **PASS** |
| `10_Console_Display` | `(165, 399, 186, 407)` | `(534, 517, 555, 526)` | `(55.2, 46.9, 35.5)` | `47.8` | `(55.9, 50.0, 41.4)` | `50.6` | `5.9` | **PASS** |
| `11_Glass_Skylight` | `(78, 139, 95, 160)` | `(447, 259, 464, 279)` | `(153.3, 130.2, 113.7)` | `133.9` | `(162.0, 143.4, 126.7)` | `146.1` | `13.2` | **PASS** |
| `12_Chamber_Upper_C` | `(184, 180, 210, 201)` | `(553, 300, 578, 320)` | `(75.9, 58.0, 42.9)` | `60.7` | `(71.7, 55.7, 42.6)` | `58.2` | `4.2` | **PASS** |
| `13_Steel_Rail` | `(124, 179, 150, 185)` | `(494, 299, 519, 305)` | `(114.3, 93.3, 80.4)` | `96.8` | `(97.7, 81.0, 67.0)` | `83.6` | `16.7` | **FAIL** (+1.7) |
| `14_Turbine_Arch` | `(208, 299, 229, 311)` | `(576, 418, 597, 430)` | `(109.0, 88.1, 72.7)` | `91.4` | `(100.1, 95.3, 90.0)` | `96.0` | `17.3` | **FAIL** (+2.3) |
| `15_Chamber_Floor` | `(229, 364, 250, 377)` | `(597, 483, 618, 495)` | `(27.8, 23.3, 17.1)` | `23.8` | `(29.9, 23.1, 17.0)` | `24.1` | `2.1` | **PASS** |
| `Contact_Shadow` | `(176..303, 465..481)` | `(544..671, 583..599)` | `(236.5, 236.9, 237.3)` | `236.9` | `(235.6, 237.0, 238.4)` | `236.8` | `1.1` | Info |

- **ROI Score**: **`13 / 15 PASS`** (`<= 15 RGB/ch`), max channel error **`17.3 RGB/ch`** (`12` of `15` within `13.2 RGB/ch`, `10` of `15` within `7.1 RGB/ch`).

---

## 4. 12-Landmark Fidelity Matrix & Honest Remaining Deltas

| # | Landmark | Observation on `task043-explorer-front.png` & Multi-Angle Views | Alignment |
|---|---|---|---|
| 1 | Outer Unibody Shell & Chamfers | Asymmetric `R_left=0.010`, `R_right=0.036`, broad satin champagne forehead (`222 -> 149 -> 73`), crisp edge bevels cleanly preserved in `left20`/`right20`/`elevated`. | Strong |
| 2 | Pillar Crest & Cheek Falloff | Sharp vertical highlight crest (`Y=134.6` vs Ref `135.5`) dropping smoothly into deep cheek valley (`Y=59.3` vs Ref `57.5`) and lower heel flare. | Strong |
| 3 | Right Flank & Lower Cutout Beam | Upper bronze (`Y=45.3` vs Ref `46.5`) and continuous lower champagne bar (`Y=68.0` vs Ref `71.7`) with shallow side notch cleanly framing the lower profile. | Strong |
| 4 | Right Window Glass & Interior | Warm glowing side cavity (`Y=52.6` vs Ref `48.4`) with visible rear electronics & Z lead hardware through smoked side glass. | Strong |
| 5 | Front Door Frame, Hinges & Handle | Slimmer `9mm` graphite perimeter bezel, upper/lower metal hinge blocks, right edge ergo handle, and sloped arch hood over console. | Strong |
| 6 | Front Glass Skylight Reflection | Warm diagonal studio softbox wedge in upper-left glass (`Y=146.1` vs Ref `133.9`), fading cleanly into transparent central/lower chamber pane. | Strong |
| 7 | Chamber Walls & Ceiling LED Strip | Dark recessed bronze-charcoal ceiling/walls with top-down amber gradient (`Y=58.2` vs Ref `60.7`) and crisp top LED strip bars. | Strong |
| 8 | CoreXY Gantry & Linear Steel Rails | True-3D front/rear/top X guide rods, belt, drag chain, Y rails, and Z lead screws clearly visible (`83.6` vs Ref `96.8`); **honest gap**: `-16.7 RGB` slightly dimmer/softer contrast on X-rail specular highlight than reference chrome flash. | Minor Delta |
| 9 | Print Head Cowl, Fan Bore & PTFE | Machined copper-titanium front shroud with pierced circular cooling bore + 7-blade rotor, brass nozzle, and curved white PTFE Bowden tube (`ptfe_bowden_tube`). | Strong |
| 10 | Printed Turbine Arch & Dark Bed | 25-fin support rib fan-out under swept smooth arch & apex ring sitting cleanly on dark graphite PEI bed (`100.1/95.3/90.0` vs Ref `109.0/88.1/72.7`); **honest gap**: arch highlights lean slightly neutral-cool (`B=90` vs `73`, `+17.3 RGB`) rather than warm metallic sheen of reference. | Minor Delta |
| 11 | Lower Floor Trench & Plinth | Recessed bed exposes dark lower cavity trench (`Y=24.1` vs Ref `23.8`, `dMax=2.1`) without muddy gray wash. | Strong |
| 12 | Console Display, Chin & Contact Shadow | Sleek recessed dark glass OLED (`Y=50.6` vs Ref `47.8`), even chin (`Y=103.6` vs Ref `101.9`), and soft grounded contact shadow (`Y=236.8` vs Ref `236.9`). | Strong |

---

## 5. Rendered Evidence Artifacts (`reports/`)

1. `reports/task043-reference-candidate-contact-sheet.png` — Exact 1:1 un-recolored comparison (`ref_printer_box.png` vs `task043-explorer-front.png`) + BT.709 value hierarchy panel
2. `reports/task043-explorer-front.png` — Primary Front 3/4 reference view (`Nodes: 63, Meshes: 56`)
3. `reports/task043-explorer-left20.png` — Rotated `-20°` left angle
4. `reports/task043-explorer-right20.png` — Rotated `+20°` right angle
5. `reports/task043-explorer-elevated.png` — Elevated `+18°` view showing roof glass into chamber
6. `reports/task043-explorer-4view-sheet.png` — Combined 2x2 verification sheet
7. `reports/task043-silhouette-overlay.png` — Centered zero-shift silhouette IoU overlay (`IoU=0.9159`)

---

## 6. Next Step

Pending Codex independent audit of `assets/models/raw/deltrol_p2s_explorer_v11.glb` against `reports/ref_printer_box.png` and `reports/reference-fidelity-criteria.md`. Per `bridge/coordinator/visual-acceptance-policy.md`, this handoff is closed as `status: completed` with `verdict: REVISION_REQUIRED` until Codex issues the formal `PASS`.
