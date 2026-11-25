# TASK-044: PBR & Mechanical Detail Fidelity Pass (`v12`)

## 1. Delivered Asset, Materials & Structural Validation

- **Deliverable GLB**: `assets/models/raw/deltrol_p2s_explorer_v12.glb`
  - **Generator Script**: `scripts/build_p2s_explorer_v12.py` (Connected True-3D geometry, 18 distinct PBR materials with dedicated `baseColor` / `roughness` / `emissive` textures + Cycles AO, zero image planes / billboards / 2.5D rigs)
  - **File Size**: `3,266,096` bytes (`Magic: glTF`, `Version: 2`)
  - **SHA-256**: `24412A38281A7337DC09A6C9332605A78147B788135E9C8F477D87543BCFB35A`
  - **GLB Node Check (`scripts/verify_glb.py`)**: `63` GLTF nodes (`enclosure`, `door`, `printHead`, `printBed`, `gantryX`, `printedObject`, `front_glass_door`, `screen_display`, `screen_bezel`, `right_glass_window`, `left_glass_window`, `top_roof_glass`, `chamber_rear_exhaust_ring`, `bracket_apex_ring`, etc.); `Missing required nodes: []`; `ALL REQUIRED NODES PRESENT AND VALID!`.
  - **Viewer Render Setup (`tools/true3d_audit_viewer.html` unchanged)**: `1226x708`, FOV `27°`, camera `[0.86, 0.22, 1.50]`, target `[0, -0.01, 0]`, white background, `ACESFilmicToneMapping` exposure `1.05`, Three.js HUD: `Nodes: 64, Meshes: 56`.
  - **Untouched Scope (`git status --short`)**: Zero edits to `website/src/**`, `tools/true3d_audit_viewer.html`, `assets/source/printer-hero-reference-2026-11-23.png`, or `reports/ref_printer_box.png`.

### Distinct PBR Material Breakdown (`18` materials in GLB)

| Material Name | Assigned Parts | `metallicFactor` | `emissiveStrength` | Purpose / Physical Response |
|---|---|---:|---:|---|
| `Champagne Satin Shell` | `unibody_shell`, `rear_panel_insert` | `0.34` | `1.6` | Brushed satin anodized champagne aluminum (`baseColorTexture` + horizontal grain `roughnessMap` `[0.18..0.42]`) |
| `Machined Steel Rails` | `x_guide_*`, `y_guide_*`, `z_lead_*`, pulleys, Z collars | `0.88` | `1.9` | High-metalness turned chrome/steel (`roughness [0.09..0.18]`, lathe texture, dark undersides, top specular streak) |
| `Anodized Copper Toolhead` | `toolhead_front_cowl`, fan bezel, top hood, pneumatic collet | `0.76` | `1.4` | Machined warm copper CNC shroud (`roughness [0.10..0.24]`) |
| `Machined Dark Alloy` | `x_gantry_crossbeam`, `drag_chain_assembly`, `toolhead_chassis`, `toolhead_fan_rotor`, `toolhead_hotend_sock`, `bed_heater_block`, rear electronics/shroud/louver ring, `chassis_recessed_plinth` | `0.55` | `0.0` (`map` + AO / edge bevels) | Dark espresso anodized extrusions, ribbed rear bulkhead, heatsink fins, 7-blade rotor & drag chain |
| `Sculpted Metallic Turbine Arch` | `bracket_swept_arch`, `bracket_apex_ring` (+ `bracket_turbine_hub`/`shaft`), `bracket_support_fins`, `bracket_base_raft` | `0.60` | `2.6` | Titanium metallic sculpted aerospace arch (`roughness 0.14`) contrasting dark 27-fin pockets (`roughness 0.26`) |
| `Dark Graphite PEI Bed` | `build_plate`, `build_plate_lip` | `0.58` | `0.0` | Stippled charcoal-bronze PEI build plate (`baseColorTexture` prevents viewer `GOLD_PEI` override) |
| `Brass Nozzle` | `toolhead_nozzle` | `0.92` | `0.0` | Bright machined brass extruder nozzle (`roughness 0.18`) |
| `Warm Chamber Anodized Interior` | `interior_rear_panel`, `interior_ceiling_liner`, `interior_left_back_baffle` | `0.22` | `0.0` | Low-reflectance warm bronze inner liner panels framing rear CNC hardware |
| `Dark Matte Floor Tray` | `interior_floor_tray` | `0.00` | `0.0` | Non-specular matte tray eliminating 82-deg grazing `rearFill` Fresnel glare |
| `Chamber LED Emitter Strip` | `led_bar_front`, `led_bar_left`, `led_bar_right` | `0.05` | `2.4` | Warm amber-cream perimeter chamber ceiling LEDs |
| `PTFE Bowden Tube` | `ptfe_bowden_tube` | `0.05` | `0.0` | Curved translucent milky Bowden tube |
| `Exterior Metallic Hardware` | `screen_metal_rim`, `door_hinge_*`, `door_ergo_handle`, `chassis_foot_0..3`, rear exhaust/AC | `0.65` | `0.0` | Brushed dark champagne bezel rim, hinges, handle, corner feet w/ rubber bases |
| `Console OLED Glass` | `screen_display` | `0.20` | `0.0` | Dark glossy glass touchscreen (`roughness 0.14`) with subtle understated status UI bar |
| `Smoked Glass`, `Ref Glass Specular Sheen`, `Right Glass Warm Sheen`, `Graphite Door Frame`, `Dark Seal Polymer` | Door & roof glass, diagonal softbox reflection wedge, right window warm tint, 8.5mm door frame & window gaskets | `0.0..0.45` | `0.0..1.8` | Multi-layer smoked glass enclosure & diagonal studio skylight highlight |

---

## 2. Geometry & Mechanical Upgrades in `v12` vs `v11`

- **Sculpted Top-Cap Shoulder & Sloped Gasket Alignment**: Rounded/beveled perimeter (`EdgeBevel 0.0095m`, `4` segments), left-to-right/front-to-rear roof taper (`top_drop_x=0.017, top_drop_y=0.017, left_shoulder_drop=0.004`), and identically tapered/recessed `top_rim_outer` & `top_roof_glass` eliminating top-rear protrusion in all 4 views.
- **Mechanical Chamber Density**: Added rear fluted CNC ribs (`6` vertical flutes), `chamber_rear_exhaust_ring`, left/right corner posts, left aux blower housing, turned Z-leadscrew collars (`z_collar_*`), dual X linear steel rods (`x_guide_front/rear`) + top rail + timing pulleys, CNC toolhead intake bezel ring, top hood, pneumatic collet, `4` stepped heatsink fins, `7`-blade rotor, and recessed turbine hub/shaft inside the hollowed `bracket_apex_ring` with `27` tapered support fins.

---

## 3. Framing, Silhouette & Same-Pipeline Photometric Evidence

- **Segmentation Rule Consistency**: Both reference (`ref_printer_box.png`) and candidate (`task044-explorer-front.png`) use identical `min(RGB) < 220` foreground extraction so the Three.js `contactPlane` radial shadow (`RGB 232..243`) is excluded identically on both crops.
- **Framing & Silhouette BBox**:
  - **Reference (`reports/ref_printer_box.png`)**: `(27, 52, 453, 461)` -> `W=426`, `H=409`, `W/H=1.0416`
  - **Candidate (`reports/task044-explorer-front.png`)**: `(396, 174, 819, 578)` -> `W=423`, `H=404`, `W/H=1.0470` (`dW=-0.70%`, `dH=-1.22%`, `dRatio=+0.0054`)
  - **Centered Zero-Shift Silhouette IoU**: **`0.9073`** (threshold `>= 0.90`)

### Exact Same-Pipeline ROI Table (`Post-ACES sRGB uint8`, exposure `1.05`, zero recoloring)

| Landmark ROI | Ref Box `(x0,y0,x1,y1)` | Cand Box `(x0,y0,x1,y1)` | Ref RGB `(R,G,B)` | Ref `Y_709` | Cand RGB `(R,G,B)` | Cand `Y_709` | `dMax` (RGB/ch) | Status (`<=15`) |
|---|---|---|---:|---:|---:|---:|---:|---|
| `01_Forehead_L` | `(61, 70, 78, 81)` | `(429, 192, 446, 203)` | `(229.8, 228.2, 222.6)` | `228.1` | `(226.3, 222.8, 215.4)` | `223.0` | `7.1` | **PASS** |
| `02_Forehead_C` | `(178, 70, 199, 81)` | `(546, 192, 567, 203)` | `(149.8, 140.9, 132.7)` | `142.2` | `(150.4, 143.0, 132.4)` | `143.8` | `2.1` | **PASS** |
| `03_Forehead_R` | `(301, 70, 314, 81)` | `(668, 192, 681, 203)` | `(69.5, 61.0, 48.8)` | `61.9` | `(70.0, 60.7, 50.0)` | `61.9` | `1.2` | **PASS** |
| `04_Pillar_Crest` | `(321, 222, 328, 248)` | `(688, 342, 695, 367)` | `(142.9, 134.2, 123.4)` | `135.3` | `(140.8, 130.5, 118.4)` | `131.8` | `5.0` | **PASS** |
| `05_Pillar_Cheek` | `(333, 222, 341, 248)` | `(700, 342, 708, 367)` | `(67.4, 56.9, 44.4)` | `58.2` | `(61.4, 51.2, 40.7)` | `52.6` | `6.0` | **PASS** |
| `06_Right_Flank_Top` | `(393, 103, 410, 115)` | `(759, 224, 776, 236)` | `(54.0, 45.5, 34.6)` | `46.5` | `(51.5, 43.0, 32.0)` | `44.0` | `2.6` | **PASS** |
| `07_Right_Win_Glass` | `(389, 227, 406, 252)` | `(755, 346, 772, 371)` | `(63.7, 45.4, 32.6)` | `48.4` | `(63.4, 45.4, 30.6)` | `48.2` | `1.9` | **PASS** |
| `08_Right_Flank_Bot` | `(393, 373, 410, 385)` | `(759, 491, 776, 503)` | `(83.7, 70.1, 52.0)` | `71.7` | `(80.2, 68.6, 53.8)` | `70.0` | `3.5` | **PASS** |
| `09_Chin_Left` | `(69, 405, 86, 418)` | `(438, 523, 455, 535)` | `(112.8, 100.5, 84.0)` | `101.9` | `(110.5, 98.3, 82.4)` | `99.7` | `2.4` | **PASS** |
| `10_Console_Display` | `(165, 398, 186, 407)` | `(533, 516, 554, 525)` | `(54.9, 46.3, 35.3)` | `47.3` | `(51.7, 43.9, 35.6)` | `45.0` | `3.2` | **PASS** |
| `11_Glass_Skylight` | `(78, 138, 95, 159)` | `(446, 259, 463, 280)` | `(153.2, 130.6, 114.3)` | `134.2` | `(159.0, 138.5, 119.8)` | `141.5` | `7.9` | **PASS** |
| `12_Chamber_Upper_C` | `(184, 180, 210, 201)` | `(552, 301, 577, 321)` | `(75.9, 58.0, 42.9)` | `60.7` | `(89.0, 69.8, 51.8)` | `72.6` | `13.1` | **PASS** |
| `13_Steel_Rail` | `(124, 179, 150, 185)` | `(493, 300, 518, 305)` | `(114.3, 93.3, 80.4)` | `96.8` | `(98.1, 78.4, 63.4)` | `81.5` | `17.0` | **FAIL** (+2.0) |
| `14_Turbine_Arch` | `(208, 299, 229, 311)` | `(575, 418, 596, 430)` | `(109.0, 88.1, 72.7)` | `91.4` | `(92.7, 80.0, 66.7)` | `81.8` | `16.2` | **FAIL** (+1.2) |
| `15_Chamber_Floor` | `(229, 364, 250, 376)` | `(596, 482, 618, 494)` | `(27.7, 23.2, 16.9)` | `23.7` | `(20.5, 16.3, 12.0)` | `16.9` | `7.2` | **PASS** |
| `Contact_Shadow` | `(176..303, 465..481)` | `(544..671, 582..598)` | `(236.5, 236.9, 237.3)` | `236.9` | `(234.8, 236.2, 237.7)` | `236.0` | `1.7` | Info |

- **Aggregate ROI Score**: `13 / 15 PASS`, `max dMax = 17.0 RGB/ch` (`13` of `15` within `0.8–13.1 RGB/ch`; `13_Steel_Rail` `17.0` and `14_Turbine_Arch` `16.2` fail the strict every-ROI `<= 15` gate by `1.2–2.0 RGB/ch`).

---

## 4. Explicit 12-Landmark Checklist (`reports/reference-fidelity-criteria.md`)

| # | Landmark Criterion | Verdict | Measured / Visual Evidence & Honest Reason |
|---|---|---|---|
| 1 | Compact right-facing 3/4 pose & low eye level | **PASS** | Fixed viewer `[0.86, 0.22, 1.50]`, `FOV 27°`, crop `423x404` (`W/H=1.047` vs Ref `426x409`, `1.042`), `IoU=0.9073`. |
| 2 | Single continuous top shell with left-to-right taper | **PASS** | Asymmetric continuous cap (`top_drop_x=0.017, top_drop_y=0.017, left_shoulder_drop=0.004`), recessed sloped gasket, flush in all 4 views. |
| 3 | Dominant rounded front-right pillar; slim/sharp left edge | **PASS** | Asymmetric `R_right=0.036` vs `R_left=0.008`, Pillar Crest `Y=131.8` vs Ref `135.3` (`dMax=5.0`), Cheek `Y=52.6` vs Ref `58.2` (`dMax=6.0`). |
| 4 | Front door closed, dark, framed, and flush with shell | **PASS** | Slim `8.5mm` `Graphite Door Frame` + `Smoked Glass (opacity=0.52)` flush inside enclosure cutout. |
| 5 | Right handle at reference height; left hinges subtle | **PASS** | Attached contoured `door_ergo_handle` at `z=-0.016` and dual subtle `door_hinge_top/bot` on left stile. |
| 6 | Chamber warm amber and readable through smoked glass | **PASS** | Warm interior wall gradient (`12_Chamber_Upper_C Y=72.6` vs Ref `60.7`, `dMax=11.8`), perimeter LED strips, dark matte floor (`15_Chamber_Floor dMax=7.2`), diagonal glass reflection wedge (`11_Glass_Skylight dMax=7.9`). |
| 7 | Upper rails and print head at matching band/span | **FAIL** | Rails, X gantry, copper toolhead shroud, fan rotor & PTFE sit in matching positions, **but** `13_Steel_Rail` ROI misses `<= 15` (`dMax=17.0` over X-gantry gap) and visually lacks razor-sharp chrome mirror reflections compared to the reference photo. |
| 8 | Bed and printed object in lower-middle region | **FAIL** | Dark graphite PEI bed + 27-fin sculpted turbine arch & hub sit in matching lower-middle region, **but** `14_Turbine_Arch` ROI misses `<= 15` (`dMax=16.2`) and metallic arch highlights look noticeably more uniform/muted than the reference's crisp brushed chrome contrast. |
| 9 | Lower console compact, centered, dark-screened, angled | **PASS** | Compact `-23°` recessed OLED screen `10_Console_Display` (`Y=45.0` vs Ref `47.3`, `dMax=3.2`) with brushed metal trim rim. |
| 10 | Bottom feet/base integrated, touching soft shadow | **PASS** | Connected corner foot housings + `chassis_recessed_plinth` meeting radial contact shadow (`Y=236.0` vs Ref `236.9`), nothing floating. |
| 11 | Right side panel dark/deep with warm reflection | **PASS** | `06_Right_Flank_Top` (`dMax=2.6`), `07_Right_Win_Glass` (`dMax=1.9`, deep warm internal glow), `08_Right_Flank_Bot` (`dMax=3.5`), shallow side arch. |
| 12 | No white wedge, black bake triangle, detached part, or image plane across all views | **PASS** | Verified visually across `front`, `left20`, `right20`, and `elevated (+18°)`; `63` GLB nodes with real PBR geometry only. |

**Checklist Result**: **`10 / 12 PASS`**, **`2 / 12 FAIL`** (#7 Upper Rails / Toolhead metallic contrast & `13_Steel_Rail` `dMax=17.0`, #8 Printed Arch metallic contrast & `14_Turbine_Arch` `dMax=16.2`).

---

## 5. Honest Contact-Sheet Judgment & Next Required Action

Comparing `reports/task044-reference-candidate-contact-sheet.png` at 1:1 scale against `reports/ref_printer_box.png`:
- `v12` substantially improves interior depth, material separation (`18` distinct PBR materials instead of one flattened unlit interior material), top roof bezel flushness, right flank continuity (`dMax 1.9–3.5`), lower dark floor matte control (`15_Chamber_Floor dMax=7.2`), and exterior Forehead/Pillar/Chin fidelity (`dMax 1.2–7.1`).
- **Remaining gap**: Inside the smoked glass, the copper toolhead cowl, dual steel X rails, and turbine arch still render somewhat flatter/softer in specular contrast than the high-contrast brushed chrome/anodized reflections in `ref_printer_box.png` (and `13_Steel_Rail` `17.0`, `14_Turbine_Arch` `16.2` exceed `15.0`). Under `TASK-044` and `bridge/coordinator/visual-acceptance-policy.md`, this handoff is closed as `status: completed` with **`verdict: REVISION_REQUIRED`** for Codex review and decision on the next pass (or viewer PMREM envMap vs specular metal calibration).

---

## 6. Evidence Files (`reports/`)

- [task044-reference-candidate-contact-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-reference-candidate-contact-sheet.png)
- [task044-explorer-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-explorer-front.png)
- [task044-explorer-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-explorer-left20.png)
- [task044-explorer-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-explorer-right20.png)
- [task044-explorer-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-explorer-elevated.png)
- [task044-explorer-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-explorer-4view-sheet.png)
- [task044-silhouette-overlay.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task044-silhouette-overlay.png)
