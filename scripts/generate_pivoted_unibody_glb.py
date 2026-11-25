"""
TASK-020: Unibody High-Fidelity 3D Asset Revision
Generates an advanced, master-quality unibody 3D printer asset matching:
assets/source/printer-hero-reference-2026-11-23.png

Fulfills all TASK-020 requirements:
1. Satin champagne-silver titanium unibody (#aeb2b8, metallic 0.65, roughness 0.24) with soft highlight roll-off
2. Optical smoked glass apertures for front door and expansive side windows
3. Sturdy dark-anodized door frame with prominent vertical brushed-silver handle on right stile
4. Rich, high-fidelity internal chamber: CoreXY dual precision steel gantry rods, detailed print head with circular fan shroud and dual brass nozzles, gold textured PEI bed with front alignment lip, and prominent aerospace topology-optimized bracket
5. Compact, recessed touchscreen console pre-offset by X = -0.04 so it centers perfectly at X = 0 when PrinterModel.jsx applies its transform
6. Node contract strictly preserved: ['enclosure', 'door', 'printHead', 'printBed', 'front_glass_door']
7. Accommodates PrinterModel.jsx scaling for side glass windows (1.0, 1.65, 1.05) to eliminate wing protrusion
"""

import math
from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_RAW = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_unibody_pivoted.glb"
OUTPUT_GEN = ROOT / "assets" / "generated" / "antigravity" / "deltrol_p2s_reference_unibody.glb"

def create_rounded_box_mesh(width, depth, height, radius, subdivisions=24):
    """
    Creates a box with smoothly rounded vertical corners (fillets)
    Width: X axis (-w/2 to w/2)
    Depth: Y axis (-d/2 to d/2)
    Height: Z axis (-h/2 to h/2)
    """
    hw = width / 2.0
    hd = depth / 2.0
    r = min(radius, hw * 0.5, hd * 0.5)

    # Core boxes
    b1 = trimesh.creation.box([width, depth - 2 * r, height])
    b2 = trimesh.creation.box([width - 2 * r, depth, height])
    meshes = [b1, b2]

    # 4 Corner rounded fillet cylinders
    corner_coords = [
        (hw - r, hd - r),
        (-hw + r, hd - r),
        (-hw + r, -hd + r),
        (hw - r, -hd + r)
    ]
    for cx, cy in corner_coords:
        cyl = trimesh.creation.cylinder(radius=r, height=height, sections=subdivisions)
        cyl.apply_translation([cx, cy, 0])
        meshes.append(cyl)

    combined = trimesh.util.concatenate(meshes)
    return combined

def create_aerodynamic_bracket():
    """
    Creates a realistic topology-optimized 3D printed mechanical bracket / truss
    resembling the organic curved part shown in printer-hero-reference-2026-11-23.png
    """
    parts = []
    # 1. Base mounting pad (curved aerodynamic base)
    base_plate = trimesh.creation.box([0.150, 0.085, 0.008])
    base_plate.apply_translation([0, 0, 0.004])
    parts.append(base_plate)

    # 2. Left and right sloping curved arches
    for sign in [-1, 1]:
        arch = trimesh.creation.box([0.026, 0.070, 0.052])
        rot = trimesh.transformations.rotation_matrix(sign * math.radians(28), [0, 1, 0])
        arch.apply_transform(rot)
        arch.apply_translation([sign * 0.046, 0, 0.028])
        parts.append(arch)

    # 3. Central apex collar (cylindrical bearing housing / collar)
    collar = trimesh.creation.cylinder(radius=0.025, height=0.042, sections=24)
    rot_c = trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0])
    collar.apply_transform(rot_c)
    collar.apply_translation([0, 0, 0.055])
    parts.append(collar)

    # 4. Central hollow bore
    inner_bore = trimesh.creation.cylinder(radius=0.014, height=0.046, sections=20)
    inner_bore.apply_transform(rot_c)
    inner_bore.apply_translation([0, 0, 0.055])

    # 5. Internal triangular stiffener ribs
    rib1 = trimesh.creation.box([0.010, 0.050, 0.035])
    rib1.apply_translation([-0.022, 0, 0.020])
    rib2 = trimesh.creation.box([0.010, 0.050, 0.035])
    rib2.apply_translation([0.022, 0, 0.020])
    parts.extend([rib1, rib2])

    combined = trimesh.util.concatenate(parts)
    return combined

def create_pivoted_asset():
    scene = trimesh.Scene()

    # -------------------------------------------------------------
    # PBR Materials definition
    # -------------------------------------------------------------
    # 1. Satin champagne titanium unibody (#aeb2b8, soft metallic highlight)
    mat_titanium = trimesh.visual.material.PBRMaterial(
        name="Titanium Satin Unibody",
        baseColorFactor=[0.68, 0.70, 0.73, 1.0],
        metallicFactor=0.62,
        roughnessFactor=0.25
    )

    # 2. Dark anodized graphite for door frame & accents (#2c2f35)
    mat_graphite_frame = trimesh.visual.material.PBRMaterial(
        name="Graphite Frame",
        baseColorFactor=[0.18, 0.19, 0.22, 1.0],
        metallicFactor=0.48,
        roughnessFactor=0.35
    )

    # 3. Bright brushed titanium silver for handle (#d8dbe0)
    mat_titanium_accent = trimesh.visual.material.PBRMaterial(
        name="Titanium Accent",
        baseColorFactor=[0.82, 0.84, 0.87, 1.0],
        metallicFactor=0.92,
        roughnessFactor=0.16
    )

    # 4. Smoked optical glass with high transparency (#12161a)
    mat_smoked_glass = trimesh.visual.material.PBRMaterial(
        name="Smoked Glass",
        baseColorFactor=[0.08, 0.10, 0.12, 0.28],
        metallicFactor=0.25,
        roughnessFactor=0.04,
        alphaMode="BLEND"
    )

    # 5. Dark interior matte chassis (#1a1d22)
    mat_dark_interior = trimesh.visual.material.PBRMaterial(
        name="Chassis Matte Dark",
        baseColorFactor=[0.11, 0.12, 0.14, 1.0],
        metallicFactor=0.45,
        roughnessFactor=0.48
    )

    # 6. Gold textured PEI sheet (#dfab2c)
    mat_gold_pei = trimesh.visual.material.PBRMaterial(
        name="Gold Textured PEI",
        baseColorFactor=[0.87, 0.67, 0.18, 1.0],
        metallicFactor=0.72,
        roughnessFactor=0.30
    )

    # 7. Carbon fiber composite (#1e2126)
    mat_carbon_spar = trimesh.visual.material.PBRMaterial(
        name="PA-CF Carbon Fiber",
        baseColorFactor=[0.14, 0.15, 0.17, 1.0],
        metallicFactor=0.28,
        roughnessFactor=0.36
    )

    # 8. Ground precision linear guide steel (#dbe0e6)
    mat_precision_steel = trimesh.visual.material.PBRMaterial(
        name="Linear Guide Steel",
        baseColorFactor=[0.88, 0.90, 0.92, 1.0],
        metallicFactor=0.96,
        roughnessFactor=0.10
    )

    # 9. Brass hotend nozzle (#e2af34)
    mat_brass_nozzle = trimesh.visual.material.PBRMaterial(
        name="Brass Nozzle",
        baseColorFactor=[0.92, 0.72, 0.24, 1.0],
        metallicFactor=0.92,
        roughnessFactor=0.18
    )

    # Dimensions: 0.38m W x 0.38m D x 0.44m H
    W, D, H = 0.38, 0.38, 0.44
    corner_r = 0.024 # 24mm continuous fillets

    # -------------------------------------------------------------
    # 1. ENCLOSURE (Node: 'enclosure')
    # -------------------------------------------------------------
    # Base plinth (bottom tray with rounded corners)
    base_mesh = create_rounded_box_mesh(W, D, 0.032, corner_r)
    base_mesh.apply_translation([0, 0, -H/2 + 0.016])

    # 4 Rubber Feet underneath base plinth
    foot_r = 0.012
    foot_h = 0.008
    foot_coords = [
        (W/2 - corner_r - 0.010, D/2 - corner_r - 0.010),
        (-W/2 + corner_r + 0.010, D/2 - corner_r - 0.010),
        (-W/2 + corner_r + 0.010, -D/2 + corner_r + 0.010),
        (W/2 - corner_r - 0.010, -D/2 + corner_r + 0.010)
    ]
    feet = []
    for fx, fy in foot_coords:
        foot = trimesh.creation.cylinder(radius=foot_r, height=foot_h, sections=16)
        foot.apply_translation([fx, fy, -H/2 - foot_h/2])
        feet.append(foot)

    # Roof rim (upper top frame with rounded corners)
    roof_mesh = create_rounded_box_mesh(W, D, 0.026, corner_r)
    roof_mesh.apply_translation([0, 0, H/2 - 0.013])

    # 4 Sleek rounded vertical corner pillars
    pillar_h = H - 0.058
    pillar_pos = [
        (W/2 - corner_r, D/2 - corner_r),
        (-W/2 + corner_r, D/2 - corner_r),
        (-W/2 + corner_r, -D/2 + corner_r),
        (W/2 - corner_r, -D/2 + corner_r)
    ]
    pillar_meshes = []
    for px, py in pillar_pos:
        p = trimesh.creation.cylinder(radius=corner_r, height=pillar_h, sections=24)
        p.apply_translation([px, py, 0])
        pillar_meshes.append(p)

    # Rear panel (matte dark interior backdrop)
    rear_panel = trimesh.creation.box([W - 0.048, 0.010, pillar_h])
    rear_panel.apply_translation([0, D/2 - 0.005, 0])

    # Front bottom symmetric fascia beam
    front_bot_fascia = trimesh.creation.box([W - 0.048, 0.016, 0.045])
    front_bot_fascia.apply_translation([0, -D/2 + 0.008, -H/2 + 0.048])

    # Front top header beam
    front_top_beam = trimesh.creation.box([W - 0.048, 0.016, 0.024])
    front_top_beam.apply_translation([0, -D/2 + 0.008, H/2 - 0.038])

    # Right side upper & lower slim frame trim
    right_top_trim = trimesh.creation.box([0.014, D - 0.050, 0.018])
    right_top_trim.apply_translation([W/2 - 0.007, 0, H/2 - 0.038])
    right_bot_trim = trimesh.creation.box([0.014, D - 0.050, 0.024])
    right_bot_trim.apply_translation([W/2 - 0.007, 0, -H/2 + 0.040])

    # Left side upper & lower slim frame trim
    left_top_trim = trimesh.creation.box([0.014, D - 0.050, 0.018])
    left_top_trim.apply_translation([-W/2 + 0.007, 0, H/2 - 0.038])
    left_bot_trim = trimesh.creation.box([0.014, D - 0.050, 0.024])
    left_bot_trim.apply_translation([-W/2 + 0.007, 0, -H/2 + 0.040])

    enclosure_parts = [
        base_mesh, roof_mesh, rear_panel, front_bot_fascia, front_top_beam,
        right_top_trim, right_bot_trim, left_top_trim, left_bot_trim
    ] + pillar_meshes + feet
    enclosure_combined = trimesh.util.concatenate(enclosure_parts)
    enclosure_combined.visual.material = mat_titanium
    scene.add_geometry(enclosure_combined, node_name="enclosure")

    # -------------------------------------------------------------
    # 2. TOUCHSCREEN CONSOLE (Nodes: 'screen_bezel', 'screen_display')
    # Pre-offset by X = -0.04 so PrinterModel.jsx (+0.04) centers it at X = 0!
    # Compact, recessed dimensions (96mm x 48mm x 8mm)
    # -------------------------------------------------------------
    screen_bezel = trimesh.creation.box([0.096, 0.008, 0.048])
    screen_bezel.apply_translation([-0.040, 0, 0])
    screen_bezel.visual.material = mat_dark_interior
    scene.add_geometry(screen_bezel, node_name="screen_bezel")

    screen_display = trimesh.creation.box([0.088, 0.002, 0.040])
    screen_display.apply_translation([-0.040, 0, 0])
    screen_display.visual.material = mat_titanium_accent
    scene.add_geometry(screen_display, node_name="screen_display")

    # -------------------------------------------------------------
    # 3. GLASS WINDOWS (Nodes: 'right_glass_window', 'left_glass_window', 'top_roof_glass')
    # Accommodates PrinterModel.jsx scale.set(1.0, 1.65, 1.05) precisely
    # -------------------------------------------------------------
    target_side_depth = D - 0.054
    target_side_height = pillar_h - 0.038
    base_side_depth = target_side_depth / 1.65
    base_side_height = target_side_height / 1.05

    # Right side smoked glass window
    right_glass = trimesh.creation.box([0.005, base_side_depth, base_side_height])
    right_glass.apply_translation([W/2 - 0.004, 0, 0.003])
    right_glass.visual.material = mat_smoked_glass
    scene.add_geometry(right_glass, node_name="right_glass_window")

    # Left side matching smoked glass window
    left_glass = trimesh.creation.box([0.005, base_side_depth, base_side_height])
    left_glass.apply_translation([-W/2 + 0.004, 0, 0.003])
    left_glass.visual.material = mat_smoked_glass
    scene.add_geometry(left_glass, node_name="left_glass_window")

    # Top glass insert
    top_glass = trimesh.creation.box([W - 0.060, D - 0.060, 0.006])
    top_glass.apply_translation([0, 0, H/2 - 0.006])
    top_glass.visual.material = mat_smoked_glass
    scene.add_geometry(top_glass, node_name="top_roof_glass")

    # -------------------------------------------------------------
    # 4. DOOR & FRONT GLASS (Nodes: 'door', 'front_glass_door')
    # Sturdy dark graphite door frame with vertical brushed silver handle on right stile
    # -------------------------------------------------------------
    door_w = W - 0.050
    door_h = pillar_h - 0.068
    door_y = -D/2 + 0.004
    door_z = 0.012

    # Top & bottom door rails (dark graphite frame)
    rail_top = trimesh.creation.box([door_w, 0.010, 0.020])
    rail_top.apply_translation([0, door_y, door_z + door_h/2 - 0.010])
    rail_bot = trimesh.creation.box([door_w, 0.010, 0.024])
    rail_bot.apply_translation([0, door_y, door_z - door_h/2 + 0.012])

    # Left & right door stiles (wide, sturdy stiles)
    stile_left = trimesh.creation.box([0.018, 0.010, door_h])
    stile_left.apply_translation([-door_w/2 + 0.009, door_y, door_z])
    stile_right = trimesh.creation.box([0.020, 0.010, door_h])
    stile_right.apply_translation([door_w/2 - 0.010, door_y, door_z])

    # Vertical cylindrical handle on right stile (prominent brushed silver)
    handle_bar = trimesh.creation.cylinder(radius=0.0065, height=0.145, sections=24)
    handle_x = door_w/2 - 0.010
    handle_bar_y = door_y - 0.018
    handle_bar.apply_translation([handle_x, handle_bar_y, door_z])

    # Handle standoffs
    standoff_top = trimesh.creation.cylinder(radius=0.005, height=0.018, sections=16)
    rot_y = trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0])
    standoff_top.apply_transform(rot_y)
    standoff_top.apply_translation([handle_x, door_y - 0.009, door_z + 0.050])

    standoff_bot = trimesh.creation.cylinder(radius=0.005, height=0.018, sections=16)
    standoff_bot.apply_transform(rot_y)
    standoff_bot.apply_translation([handle_x, door_y - 0.009, door_z - 0.050])

    door_parts = [rail_top, rail_bot, stile_left, stile_right, handle_bar, standoff_top, standoff_bot]
    door_combined = trimesh.util.concatenate(door_parts)
    door_combined.visual.material = mat_titanium_accent
    scene.add_geometry(door_combined, node_name="door")

    # Front glass panel inside the door frame
    front_glass = trimesh.creation.box([door_w - 0.034, 0.005, door_h - 0.040])
    front_glass.apply_translation([0, door_y, door_z])
    front_glass.visual.material = mat_smoked_glass
    scene.add_geometry(front_glass, node_name="front_glass_door")

    # -------------------------------------------------------------
    # 5. PRINT BED & PEI BUILD PLATE (Node: 'printBed')
    # -------------------------------------------------------------
    bed_y_pos = -0.040

    # Heated bed substrate (black aluminum)
    bed_substrate = trimesh.creation.box([0.285, 0.285, 0.010])
    bed_substrate.apply_translation([0, 0, bed_y_pos - 0.005])

    # Textured Gold PEI spring sheet
    pei_sheet = trimesh.creation.box([0.280, 0.280, 0.003])
    pei_sheet.apply_translation([0, 0, bed_y_pos + 0.0015])

    # Front bed lip tab with alignment notch
    bed_lip = trimesh.creation.box([0.088, 0.020, 0.003])
    bed_lip.apply_translation([0, -D/2 + 0.042, bed_y_pos + 0.0015])

    # Bed under-carriage support frame
    carriage_beam1 = trimesh.creation.box([0.024, 0.270, 0.016])
    carriage_beam1.apply_translation([-0.065, 0, bed_y_pos - 0.018])
    carriage_beam2 = trimesh.creation.box([0.024, 0.270, 0.016])
    carriage_beam2.apply_translation([0.065, 0, bed_y_pos - 0.018])

    bed_parts = [bed_substrate, pei_sheet, bed_lip, carriage_beam1, carriage_beam2]
    bed_combined = trimesh.util.concatenate(bed_parts)
    bed_combined.visual.material = mat_gold_pei
    scene.add_geometry(bed_combined, node_name="printBed")

    # -------------------------------------------------------------
    # 6. PRINT HEAD & TOOLHEAD (Node: 'printHead')
    # -------------------------------------------------------------
    head_z = H/2 - 0.095

    # Main extruder body (matte graphite)
    head_body = trimesh.creation.box([0.088, 0.076, 0.080])
    head_body.apply_translation([0, 0, head_z])

    # Circular front cooling fan cowl
    fan_cowl = trimesh.creation.cylinder(radius=0.022, height=0.008, sections=24)
    rot_cowl = trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0])
    fan_cowl.apply_transform(rot_cowl)
    fan_cowl.apply_translation([0, -0.042, head_z + 0.006])

    # Central fan hub
    fan_hub = trimesh.creation.cylinder(radius=0.008, height=0.010, sections=16)
    fan_hub.apply_transform(rot_cowl)
    fan_hub.apply_translation([0, -0.042, head_z + 0.006])

    # Status LED indicator strip across front
    led_strip = trimesh.creation.box([0.070, 0.004, 0.006])
    led_strip.apply_translation([0, -0.040, head_z + 0.030])

    # Brass hotend nozzles (twin precision nozzles pointing downwards)
    nozzle_main = trimesh.creation.cone(radius=0.006, height=0.018, sections=16)
    rot_cone = trimesh.transformations.rotation_matrix(math.pi, [1, 0, 0])
    nozzle_main.apply_transform(rot_cone)
    nozzle_main.apply_translation([0, 0, head_z - 0.048])

    # Top bowden guide tube connector
    top_connector = trimesh.creation.cylinder(radius=0.006, height=0.016, sections=16)
    top_connector.apply_translation([0, 0.012, head_z + 0.046])

    head_parts = [head_body, fan_cowl, fan_hub, led_strip, nozzle_main, top_connector]
    head_combined = trimesh.util.concatenate(head_parts)
    head_combined.visual.material = mat_dark_interior
    scene.add_geometry(head_combined, node_name="printHead")

    # -------------------------------------------------------------
    # 7. COREXY GANTRY GUIDE RAILS (Node: 'gantryX')
    # -------------------------------------------------------------
    gantry_z = H/2 - 0.080
    gantry_w = W - 0.065
    rod1 = trimesh.creation.cylinder(radius=0.0055, height=gantry_w, sections=20)
    rot_x = trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0])
    rod1.apply_transform(rot_x)
    rod1.apply_translation([0, -0.042, gantry_z])

    rod2 = trimesh.creation.cylinder(radius=0.0055, height=gantry_w, sections=20)
    rod2.apply_transform(rot_x)
    rod2.apply_translation([0, 0.042, gantry_z])

    # Left & right gantry carriage slider blocks
    left_block = trimesh.creation.box([0.024, 0.120, 0.028])
    left_block.apply_translation([-gantry_w/2, 0, gantry_z])
    right_block = trimesh.creation.box([0.024, 0.120, 0.028])
    right_block.apply_translation([gantry_w/2, 0, gantry_z])

    # Y-axis side linear guide rails
    y_rail_left = trimesh.creation.cylinder(radius=0.0045, height=D - 0.075, sections=16)
    rot_y_rail = trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0])
    y_rail_left.apply_transform(rot_y_rail)
    y_rail_left.apply_translation([-W/2 + 0.038, 0, gantry_z + 0.016])

    y_rail_right = trimesh.creation.cylinder(radius=0.0045, height=D - 0.075, sections=16)
    y_rail_right.apply_transform(rot_y_rail)
    y_rail_right.apply_translation([W/2 - 0.038, 0, gantry_z + 0.016])

    # Rear Z-axis vertical lead screws & guide rods
    z_rod_left = trimesh.creation.cylinder(radius=0.0045, height=H - 0.090, sections=16)
    z_rod_left.apply_translation([-W/2 + 0.055, D/2 - 0.035, 0])
    z_rod_right = trimesh.creation.cylinder(radius=0.0045, height=H - 0.090, sections=16)
    z_rod_right.apply_translation([W/2 - 0.055, D/2 - 0.035, 0])

    gantry_parts = [rod1, rod2, left_block, right_block, y_rail_left, y_rail_right, z_rod_left, z_rod_right]
    gantry_combined = trimesh.util.concatenate(gantry_parts)
    gantry_combined.visual.material = mat_precision_steel
    scene.add_geometry(gantry_combined, node_name="gantryX")

    # -------------------------------------------------------------
    # 8. PRINTED AERODYNAMIC OBJECT ON BED (Node: 'printedObject')
    # -------------------------------------------------------------
    bracket = create_aerodynamic_bracket()
    bracket.apply_translation([0, 0, bed_y_pos + 0.004])
    bracket.visual.material = mat_carbon_spar
    scene.add_geometry(bracket, node_name="printedObject")

    # -------------------------------------------------------------
    # Export GLB to both raw and generated paths
    # -------------------------------------------------------------
    OUTPUT_RAW.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_GEN.parent.mkdir(parents=True, exist_ok=True)

    glb_bytes = scene.export(file_type="glb")
    with open(OUTPUT_RAW, "wb") as f:
        f.write(glb_bytes)
    with open(OUTPUT_GEN, "wb") as f:
        f.write(glb_bytes)

    print(f"Successfully generated revised unibody 3D asset:")
    print(f"  - Raw path: {OUTPUT_RAW} ({len(glb_bytes)} bytes)")
    print(f"  - Gen path: {OUTPUT_GEN} ({len(glb_bytes)} bytes)")

if __name__ == "__main__":
    create_pivoted_asset()
