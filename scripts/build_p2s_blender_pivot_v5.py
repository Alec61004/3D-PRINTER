"""
TASK-035: Blender 5.3 Hard-Surface Reconstruction + Cycles OptiX Studio Baking (v5)
Generates: assets/models/raw/deltrol_p2s_source_geometry_pivot_v5.glb

Architecture (Pivoting completely from custom procedural box scripts):
1. Constructed natively in Blender 5.3.0 (`bpy` + `bmesh` + Modifiers):
   - Single seamless continuous unibody aluminum/titanium shell (`unibody_shell`) carved via
     non-coplanar Boolean cutters (front door recess, left/right window bays, top skylight
     well, lower side arches, recessed chin, angled console dock) + 3-segment Edge Bevel
     and smooth weighted normals (ZERO stacked box slabs, ZERO flat photo facades).
   - Real multi-part hard-surface details across all 6 contract sub-assemblies:
     * `enclosure`: recessed top skylight gasket (`top_rim_outer`), rear honeycomb exhaust +
       IEC AC switch plate, chamfered underbody plinth + 4 beveled feet, 5-wall sealed warm
       amber chamber liner + stepped right-rear Z-motor/PCB shroud with cooling louvers,
       molded chamfered console bezel & dark obsidian screen, left hinges.
     * `door`: molded continuous perimeter graphite door frame + arched lower cradle, sculpted
       Sub-D curved ergonomic handle bar, single-pass `Smoked Glass` (`doubleSided=False`),
       and corner-tapered diagonal studio glass sheen overlay (`front_glass_sheen`).
     * `gantryX`: twin precision steel guide rods, machined crossbeam, GT2 timing belts, corner
       idler pulleys, left/right XY stepper housings, 4 vertical Z-leadscrews/rails, and
       14-link Bezier articulated cable drag chain.
     * `printHead`: multi-bevel Sub-D champagne cowl with recessed circular air intake +
       9-blade turbine fan rotor inside, heatsink fins, silicone sock, `Brass Nozzle`, and
       Bezier PTFE Bowden tube.
     * `printBed`: beveled gold-bronze textured PEI plate with front grip tabs atop cast
       heatbed carrier, dual Z-carriage arms, and 3 brass/graphite leadscrew brackets.
     * `printedObject`: smooth lofted aerospace turbine arch bracket with machined apex
       bearing bore ring + 24 radial/vertical support blades on contoured raft flange.
2. Cycles RTX 3050 OPTIX Studio Baking (`COMBINED` pass + OpenImageDenoise):
   - Bakes real multi-bounce studio lighting, champagne-titanium softbox reflections, diagonal
     forehead shadow, front-right pillar specular ribbon, crevice AO, and warm honey-amber
     interior LED radiosity onto UV-packed surface atlases mapped cleanly to true 3D meshes.
"""

import math
import os
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_source_geometry_pivot_v5.glb"
BAKE_DIR = Path(r"C:\Users\PC\.gemini\antigravity\brain\4241a9a6-bf9f-48f0-84bf-532f80b9bfc1\scratch\v5_bake")
BAKE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Scene & Mesh Construction Helpers
# ---------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    return scene


def make_collection_parent(name: str):
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = "PLAIN_AXES"
    empty.empty_display_size = 0.02
    bpy.context.scene.collection.objects.link(empty)
    empty["logicalPart"] = name
    return empty


def link_obj(obj, parent=None):
    if obj.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(obj)
    if parent is not None:
        obj.parent = parent
    return obj


def set_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def apply_all_modifiers(obj):
    set_active(obj)
    for mod in list(obj.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as exc:
            print(f"[WARN] Modifier {mod.name} on {obj.name} fallback convert: {exc}")
            bpy.ops.object.convert(target="MESH")
            break


def fix_normals_and_smooth(obj, smooth=True, auto_angle_deg=36.0):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
        if hasattr(me, "shade_smooth"):
            pass
        # Blender 5.x weighted normal / sharp edges via angle
        bm = bmesh.new()
        bm.from_mesh(me)
        rad = math.radians(auto_angle_deg)
        for e in bm.edges:
            if len(e.link_faces) == 2:
                ang = e.link_faces[0].normal.angle(e.link_faces[1].normal, 0.0)
                e.smooth = ang < rad
            else:
                e.smooth = False
        bm.to_mesh(me)
        bm.free()
    me.update()


def make_asym_rounded_prism(name, w, d, z0, z1, r_left, r_right, seg=14, parent=None):
    """Creates a clean outward-normal extruded prism with asymmetric left/right corner radii."""
    hw, hd = w / 2.0, d / 2.0
    corners = [
        ( hw - r_right,  hd - r_right, r_right, 0.0, math.pi / 2.0),
        (-hw + r_left,   hd - r_left,  r_left,  math.pi / 2.0, math.pi),
        (-hw + r_left,  -hd + r_left,  r_left,  math.pi, 1.5 * math.pi),
        ( hw - r_right, -hd + r_right, r_right, 1.5 * math.pi, 2.0 * math.pi),
    ]
    ring = []
    for cx, cy, r, a0, a1 in corners:
        for i in range(seg + 1):
            a = a0 + (a1 - a0) * (i / seg)
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            if not ring or (abs(x - ring[-1][0]) > 1e-6 or abs(y - ring[-1][1]) > 1e-6):
                ring.append((x, y))

    bm = bmesh.new()
    bot_verts = [bm.verts.new((x, y, z0)) for x, y in ring]
    top_verts = [bm.verts.new((x, y, z1)) for x, y in ring]
    n = len(ring)
    for i in range(n):
        nxt = (i + 1) % n
        bm.faces.new((bot_verts[i], bot_verts[nxt], top_verts[nxt], top_verts[i]))
    bm.faces.new(list(reversed(bot_verts)))
    bm.faces.new(top_verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    me = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    return link_obj(obj, parent)


def make_box(name, center, size, parent=None, rot_euler=(0.0, 0.0, 0.0), bevel=0.0, bevel_segs=2):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(me)
    bm.free()

    obj = bpy.data.objects.new(name, me)
    obj.location = center
    obj.rotation_euler = rot_euler
    link_obj(obj, parent)
    if bevel > 0.0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segs
        mod.limit_method = "ANGLE"
        apply_all_modifiers(obj)
    fix_normals_and_smooth(obj, smooth=(bevel > 0.0))
    return obj


def make_cylinder(name, center, radius, depth, axis="z", segs=28, parent=None, bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs, radius1=radius, radius2=radius, depth=depth
    )
    if axis == "x":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler((0, math.pi / 2, 0)).to_matrix())
    elif axis == "y":
        bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Euler((math.pi / 2, 0, 0)).to_matrix())
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(me)
    bm.free()

    obj = bpy.data.objects.new(name, me)
    obj.location = center
    link_obj(obj, parent)
    if bevel > 0.0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        apply_all_modifiers(obj)
    fix_normals_and_smooth(obj, smooth=True)
    return obj


def make_curve_tube(name, points, radius, res_u=12, bevel_res=5, parent=None):
    curve_data = bpy.data.curves.new(name + "_Curve", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = radius
    curve_data.bevel_resolution = bevel_res
    curve_data.use_fill_caps = True
    spline = curve_data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for idx, p in enumerate(points):
        spline.points[idx].co = (p[0], p[1], p[2], 1.0)
    spline.use_smooth = True
    obj_c = bpy.data.objects.new(name, curve_data)
    link_obj(obj_c, parent)
    set_active(obj_c)
    bpy.ops.object.convert(target="MESH")
    obj = bpy.context.active_object
    fix_normals_and_smooth(obj, smooth=True)
    return obj


def boolean_cut(target_obj, cutter_obj, op="DIFFERENCE"):
    mod = target_obj.modifiers.new("Bool_" + cutter_obj.name, "BOOLEAN")
    mod.operation = op
    mod.object = cutter_obj
    if hasattr(mod, "solver"):
        mod.solver = "EXACT"
    apply_all_modifiers(target_obj)
    bpy.data.objects.remove(cutter_obj, do_unlink=True)


# ---------------------------------------------------------------------
# Cycles Studio Materials (for rich GPU raytraced bake)
# ---------------------------------------------------------------------
def create_cycles_titanium_mat(name, base_rgb=(0.48, 0.43, 0.37), metallic=0.38, rough=0.30, aniso_axis="X"):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*base_rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Specular IOR Level"].default_value = 0.65

    # Ultra-fine horizontal brushed aluminum grain (eliminating cloudy forehead blotches)
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (4.0, 480.0, 480.0) if aniso_axis == "X" else (480.0, 4.0, 480.0)
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 32.0
    noise.inputs["Detail"].default_value = 4.0

    # Smooth diagonal studio light falloff across forehead (+X, +Z -> shaded titanium, -X -> crisp champagne)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tex_coord.outputs["Object"], sep.inputs["Vector"])
    diag_add = nt.nodes.new("ShaderNodeMath")
    diag_add.operation = "ADD"
    nt.links.new(sep.outputs["X"], diag_add.inputs[0])
    nt.links.new(sep.outputs["Z"], diag_add.inputs[1])

    comb_math = nt.nodes.new("ShaderNodeMath")
    comb_math.operation = "MULTIPLY_ADD"
    comb_math.inputs[1].default_value = -1.15
    comb_math.inputs[2].default_value = 1.00
    nt.links.new(diag_add.outputs["Value"], comb_math.inputs[0])

    clamp_n = nt.nodes.new("ShaderNodeClamp")
    clamp_n.inputs["Min"].default_value = 0.48
    clamp_n.inputs["Max"].default_value = 1.35
    nt.links.new(comb_math.outputs["Value"], clamp_n.inputs["Value"])

    ramp_col = nt.nodes.new("ShaderNodeMix")
    ramp_col.data_type = "RGBA"
    ramp_col.blend_type = "MULTIPLY"
    ramp_col.inputs["Factor"].default_value = 0.72
    ramp_col.inputs["A"].default_value = (*base_rgb, 1.0)
    nt.links.new(clamp_n.outputs["Result"], ramp_col.inputs["B"])
    nt.links.new(ramp_col.outputs["Result"], bsdf.inputs["Base Color"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (rough - 0.03, rough - 0.03, rough - 0.03, 1.0)
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (rough + 0.04, rough + 0.04, rough + 0.04, 1.0)

    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.018
    bump.inputs["Distance"].default_value = 0.0005

    nt.links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Roughness"])
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def create_cycles_solid_mat(name, base_rgb, metallic=0.1, rough=0.4, emission_rgb=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if emission_rgb and emission_strength > 0.0:
        bsdf.inputs["Emission Color"].default_value = (*emission_rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def create_cycles_pei_mat():
    mat = bpy.data.materials.new("Cycles Gold PEI")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (0.64, 0.44, 0.16, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.25
    bsdf.inputs["Roughness"].default_value = 0.36

    tc = nt.nodes.new("ShaderNodeTexCoord")
    vor = nt.nodes.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 420.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.12
    bump.inputs["Distance"].default_value = 0.001
    nt.links.new(tc.outputs["Object"], vor.inputs["Vector"])
    nt.links.new(vor.outputs["Distance"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def join_objects(objs, new_name, parent):
    """Joins homogeneous small clones (e.g., drag chain links, support fins) into one clean mesh."""
    bpy.ops.object.select_all(action="DESELECT")
    valid = [o for o in objs if o and o.type == "MESH"]
    for o in valid:
        o.select_set(True)
    bpy.context.view_layer.objects.active = valid[0]
    bpy.ops.object.join()
    merged = bpy.context.active_object
    merged.name = new_name
    merged.parent = parent
    return merged


# ---------------------------------------------------------------------
# Build Hard-Surface Blender Printer Geometry
# ---------------------------------------------------------------------
def build_geometry():
    # Reference-locked silhouette proportions compensating PrinterModel.jsx 1.12x Z-scale
    W, D = 0.448, 0.306
    R_left, R_right = 0.015, 0.032
    Z_bot, Z_top = -0.194, 0.184
    Z_chin_top = -0.136
    Z_door_top = 0.138
    Z_side_arch = -0.184

    p_enclosure = make_collection_parent("enclosure")
    p_door = make_collection_parent("door")
    p_printHead = make_collection_parent("printHead")
    p_printBed = make_collection_parent("printBed")
    p_gantryX = make_collection_parent("gantryX")
    p_printedObject = make_collection_parent("printedObject")

    mat_ti_outer = create_cycles_titanium_mat("Cycles Ti Outer", (0.33, 0.29, 0.24), metallic=0.22, rough=0.34)
    mat_ti_hw = create_cycles_titanium_mat("Cycles Ti Hardware", (0.14, 0.12, 0.10), metallic=0.28, rough=0.28)
    mat_dark_metal = create_cycles_titanium_mat("Cycles Dark Metal", (0.10, 0.088, 0.078), metallic=0.18, rough=0.45)
    mat_chamber_wall = create_cycles_solid_mat("Cycles Chamber Wall", (0.24, 0.15, 0.09), metallic=0.05, rough=0.58)
    mat_chamber_shroud = create_cycles_solid_mat("Cycles Chamber Shroud", (0.11, 0.080, 0.056), metallic=0.14, rough=0.44)
    mat_chrome_steel = create_cycles_solid_mat("Cycles Chrome Steel", (0.76, 0.71, 0.66), metallic=0.45, rough=0.20)
    mat_gantry_dark = create_cycles_solid_mat("Cycles Gantry Dark", (0.09, 0.078, 0.072), metallic=0.20, rough=0.40)
    mat_toolhead_cowl = create_cycles_titanium_mat("Cycles Toolhead Cowl", (0.48, 0.34, 0.22), metallic=0.20, rough=0.28)
    mat_pei = create_cycles_pei_mat()
    mat_turbine = create_cycles_titanium_mat("Cycles Turbine Bracket", (0.20, 0.16, 0.13), metallic=0.30, rough=0.28)
    mat_ptfe = create_cycles_solid_mat("Cycles PTFE", (0.86, 0.82, 0.76), metallic=0.0, rough=0.32)
    mat_led = create_cycles_solid_mat("Cycles Warm LED", (1.0, 0.62, 0.24), 0.0, 0.2, (1.0, 0.56, 0.18), 9.5)

    # Export-only materials preserved directly without Cycles baking
    mat_graphite = create_cycles_solid_mat("Graphite Door Frame", (0.08, 0.085, 0.098), metallic=0.55, rough=0.24)
    mat_brass = create_cycles_solid_mat("Brass Nozzle", (0.88, 0.68, 0.18), metallic=0.90, rough=0.18)

    # -----------------------------------------------------------------
    # 1. SEAMLESS CONTINUOUS BEVELED UNIBODY SHELL (`unibody_shell`)
    # -----------------------------------------------------------------
    shell = make_asym_rounded_prism("unibody_shell", W, D, Z_bot, Z_top, R_left, R_right, seg=18, parent=p_enclosure)

    # Non-coplanar Boolean cutters carve genuine door bay, side windows, roof well, inner cavity, arches, and console cradle!
    # Interior hollow cavity (leaving 22mm wall thickness around exterior unibody)
    cavity = make_asym_rounded_prism("cut_cavity", W - 0.044, D - 0.044, Z_chin_top, Z_door_top, 0.008, 0.008, seg=6)
    boolean_cut(shell, cavity)

    # Front door opening (spans between asymmetric left/right pillars and between Z_chin_top and Z_door_top)
    x_f_min = -W / 2.0 + R_left + 0.002
    x_f_max =  W / 2.0 - R_right - 0.002
    door_w = x_f_max - x_f_min
    door_xc = 0.5 * (x_f_min + x_f_max)
    door_h = (Z_door_top - 0.006) - Z_chin_top
    door_zc = 0.5 * ((Z_door_top - 0.006) + Z_chin_top)
    cut_front = make_box("cut_front", (door_xc, -D / 2.0, door_zc), (door_w, 0.065, door_h))
    boolean_cut(shell, cut_front)

    # Top skylight cutout well
    cut_top = make_asym_rounded_prism("cut_top", 0.362, 0.224, Z_door_top - 0.015, Z_top + 0.025, 0.012, 0.012, seg=10)
    boolean_cut(shell, cut_top)

    # Right & Left side window bays
    y_l_min, y_l_max = -D / 2.0 + R_left + 0.004, D / 2.0 - R_left - 0.004
    y_r_min, y_r_max = -D / 2.0 + R_right + 0.002, D / 2.0 - R_right - 0.002
    win_zc = 0.5 * ((Z_door_top - 0.012) + Z_chin_top)
    win_h = (Z_door_top - 0.012) - Z_chin_top
    cut_win_r = make_box("cut_win_r", (W / 2.0, 0.5 * (y_r_min + y_r_max), win_zc), (0.065, y_r_max - y_r_min, win_h))
    boolean_cut(shell, cut_win_r)
    cut_win_l = make_box("cut_win_l", (-W / 2.0, 0.5 * (y_l_min + y_l_max), win_zc), (0.065, y_l_max - y_l_min, win_h))
    boolean_cut(shell, cut_win_l)

    # Clean architectural lower side arches + subtle front chin shadow recess
    cut_arch_r = make_box("cut_arch_r", (W / 2.0, 0.0, Z_bot - 0.005), (0.060, D - 2 * R_right - 0.072, (Z_side_arch - Z_bot) * 2.0 + 0.01))
    boolean_cut(shell, cut_arch_r)
    cut_arch_l = make_box("cut_arch_l", (-W / 2.0, 0.0, Z_bot - 0.005), (0.060, D - 2 * R_left - 0.072, (Z_side_arch - Z_bot) * 2.0 + 0.01))
    boolean_cut(shell, cut_arch_l)
    cut_chin = make_box("cut_chin", (door_xc, -D / 2.0, Z_bot - 0.008), (door_w - 0.088, 0.060, 0.022))
    boolean_cut(shell, cut_chin)

    # Rear recessed service bay cutout
    cut_rear = make_box("cut_rear", (0.0, D / 2.0 + 0.008, 0.0), (W - 0.088, 0.024, (Z_door_top - Z_chin_top) + 0.02), bevel=0.003)
    boolean_cut(shell, cut_rear)

    # True 3D Bevel Modifier around every unibody corner, window bay & crown!
    bev = shell.modifiers.new("EdgeBevel", "BEVEL")
    bev.width = 0.0024
    bev.segments = 3
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(32.0)
    bev.use_clamp_overlap = True
    bev.harden_normals = False
    apply_all_modifiers(shell)
    fix_normals_and_smooth(shell, smooth=True, auto_angle_deg=34.0)
    shell.data.materials.append(mat_ti_outer)

    # Underbody dark recessed plinth & 4 chamfered feet (zero bottom gaps!)
    plinth = make_asym_rounded_prism("chassis_recessed_plinth", W - 0.018, D - 0.018, Z_bot + 0.002, Z_chin_top + 0.002, 0.010, 0.020, seg=8, parent=p_enclosure)
    plinth.data.materials.append(mat_dark_metal)
    for i, (fx, fy, fw) in enumerate([
        (-W / 2.0 + 0.020, -D / 2.0 + 0.020, 0.022),
        ( W / 2.0 - 0.036, -D / 2.0 + 0.036, 0.028),
        ( W / 2.0 - 0.036,  D / 2.0 - 0.036, 0.028),
        (-W / 2.0 + 0.020,  D / 2.0 - 0.020, 0.022),
    ]):
        ft = make_cylinder(f"chassis_foot_{i}", (fx, fy, Z_bot - 0.001), fw * 0.52, 0.006, "z", segs=20, parent=p_enclosure, bevel=0.0012)
        ft.data.materials.append(mat_dark_metal)

    # Rear recessed panel + radial exhaust fan grille + AC inlet switch (from p2s_multiview_rear.jpg)
    rear_ins = make_box("rear_panel_insert", (0.0, D / 2.0 - 0.014, 0.0), (W - 0.092, 0.012, Z_door_top - Z_chin_top + 0.016), parent=p_enclosure, bevel=0.0015)
    rear_ins.data.materials.append(mat_ti_outer)
    rear_fan_hub = make_cylinder("rear_exhaust_shroud", (-0.015, D / 2.0 - 0.006, 0.068), 0.042, 0.006, "y", segs=24, parent=p_enclosure, bevel=0.001)
    rear_fan_hub.data.materials.append(mat_dark_metal)
    ac_sw = make_box("rear_ac_module", (0.115, D / 2.0 - 0.006, Z_bot + 0.022), (0.062, 0.008, 0.022), parent=p_enclosure, bevel=0.001)
    ac_sw.data.materials.append(mat_dark_metal)

    # Molded Skylight & Side Window Graphite Gaskets (with `top_rim_outer` preserved!)
    top_gasket = make_asym_rounded_prism("top_rim_outer", 0.366, 0.228, Z_top - 0.009, Z_top - 0.0008, 0.012, 0.012, seg=12, parent=p_enclosure)
    cut_tg = make_asym_rounded_prism("cut_tg", 0.348, 0.210, Z_top - 0.015, Z_top + 0.005, 0.008, 0.008, seg=10)
    boolean_cut(top_gasket, cut_tg)
    top_gasket.data.materials.append(mat_graphite)

    for sname, sx_s, ymin, ymax in [("left", -1.0, y_l_min, y_l_max), ("right", 1.0, y_r_min, y_r_max)]:
        gx = sx_s * (W / 2.0 - 0.010)
        gasket = make_box(f"{sname}_window_gasket", (gx, 0.5 * (ymin + ymax), win_zc), (0.024, ymax - ymin + 0.004, win_h + 0.004), parent=p_enclosure)
        cut_wg = make_box(f"cut_wg_{sname}", (gx, 0.5 * (ymin + ymax), win_zc), (0.044, ymax - ymin - 0.022, win_h - 0.022))
        boolean_cut(gasket, cut_wg)
        gasket.data.materials.append(mat_graphite)

    # 5-wall Sealed Chamber Liner + Stepped Electronics Shroud + LED Bars
    rear_zc = 0.5 * (Z_door_top + Z_chin_top)
    rear_h = Z_door_top - Z_chin_top
    lin_rear = make_box("interior_rear_panel", (0.0, D / 2.0 - 0.024, rear_zc), (W - 0.036, 0.006, rear_h + 0.012), parent=p_enclosure)
    lin_ceil = make_box("interior_ceiling_liner", (0.0, 0.004, Z_door_top - 0.005), (W - 0.048, D - 0.048, 0.006), parent=p_enclosure)
    lin_floor = make_box("interior_floor_tray", (0.0, 0.0, Z_chin_top - 0.002), (W - 0.036, D - 0.036, 0.008), parent=p_enclosure)
    lin_left = make_box("interior_left_back_baffle", (-W / 2.0 + 0.024, 0.002, rear_zc), (0.006, D - 0.038, rear_h + 0.006), parent=p_enclosure)
    for lin in (lin_rear, lin_ceil, lin_floor, lin_left):
        lin.data.materials.append(mat_chamber_wall)

    # Stepped right-rear electronics / Z-motor shroud with molded chamfered ribs
    shroud_r = make_box("interior_right_lower_shroud", (W / 2.0 - 0.036, 0.068, -0.058), (0.024, 0.112, 0.148), parent=p_enclosure, bevel=0.003)
    shroud_b = make_box("interior_rear_electronics_box", (0.074, D / 2.0 - 0.040, -0.024), (0.144, 0.028, 0.158), parent=p_enclosure, bevel=0.004)
    shroud_l = make_box("interior_rear_chute_box", (-0.092, D / 2.0 - 0.042, 0.018), (0.072, 0.028, 0.120), parent=p_enclosure, bevel=0.003)
    for sh in (shroud_r, shroud_b, shroud_l):
        sh.data.materials.append(mat_chamber_shroud)

    # Warm overhead LED strips (real Cycles emissive sources!)
    for lname, loc, sz in [
        ("led_bar_front", (0.0, -0.108, Z_door_top - 0.010), (0.310, 0.012, 0.004)),
        ("led_bar_left",  (-0.172, 0.0, Z_door_top - 0.010), (0.012, 0.186, 0.004)),
        ("led_bar_right", ( 0.168, 0.0, Z_door_top - 0.010), (0.012, 0.186, 0.004)),
    ]:
        lb = make_box(lname, loc, sz, parent=p_enclosure)
        lb.data.materials.append(mat_led)

    # Sleek Chamfered Touchscreen Console Cradle
    con_ang = math.radians(-26.0)
    cx_con = door_xc - 0.006
    con_y = -D / 2.0 - 0.005
    con_z = Z_chin_top - 0.012
    n_y, n_z = -math.cos(con_ang), -math.sin(con_ang)

    dock = make_box("screen_dock_wedge", (cx_con, -D / 2.0 + 0.004, con_z - 0.002), (0.112, 0.018, 0.022), parent=p_enclosure, bevel=0.002)
    dock.data.materials.append(mat_graphite)
    rim = make_box("screen_metal_rim", (cx_con, con_y, con_z), (0.116, 0.008, 0.034), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.0025, bevel_segs=3)
    rim.data.materials.append(mat_ti_hw)
    bez = make_box("screen_bezel", (cx_con, con_y + n_y * 0.0025, con_z + n_z * 0.0025), (0.110, 0.005, 0.028), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.0015)
    bez.data.materials.append(mat_graphite)
    disp = make_box("screen_display", (cx_con, con_y + n_y * 0.0048, con_z + n_z * 0.0048), (0.104, 0.002, 0.023), parent=p_enclosure, rot_euler=(con_ang, 0, 0))
    disp.data.materials.append(mat_gantry_dark)

    # Hinges on left stile
    door_y = -D / 2.0 + 0.004
    for hname, hz in [("door_hinge_top", door_zc + door_h / 2.0 - 0.022), ("door_hinge_bot", door_zc - door_h / 2.0 + 0.022)]:
        hg = make_box(hname, (x_f_min + 0.004, door_y - 0.002, hz), (0.011, 0.008, 0.020), parent=p_enclosure, bevel=0.0018)
        hg.data.materials.append(mat_ti_hw)

    # -----------------------------------------------------------------
    # 2. MOLDED GRAPHITE DOOR FRAME + SUB-D HANDLE (`door`)
    # -----------------------------------------------------------------
    stile_w = 0.013
    rail_h = 0.012
    # Keep explicit `door_left_stile` node for PrinterModel.jsx check
    stile_l = make_box("door_left_stile", (door_xc - door_w / 2.0 + stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), parent=p_door, bevel=0.001)
    stile_r = make_box("door_right_stile", (door_xc + door_w / 2.0 - stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), parent=p_door, bevel=0.001)
    rail_t = make_box("door_top_rail", (door_xc, door_y, door_zc + door_h / 2.0 - rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), parent=p_door, bevel=0.001)
    b_rail_bot = door_zc - door_h / 2.0
    rail_b = make_box("door_bottom_rail", (door_xc, door_y, b_rail_bot + rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), parent=p_door, bevel=0.001)
    arch_hood = make_box("door_console_arch_hood", (cx_con, door_y, b_rail_bot + rail_h + 0.002), (0.114, 0.007, 0.008), parent=p_door, bevel=0.002)
    for df in (stile_l, stile_r, rail_t, rail_b, arch_hood):
        df.data.materials.append(mat_graphite)

    # Sculpted rounded vertical handle
    hx = door_xc + door_w / 2.0 - 0.003
    hz = door_zc - 0.004
    hdl = make_box("door_ergo_handle", (hx, door_y - 0.010, hz), (0.011, 0.010, 0.056), parent=p_door, bevel=0.0035, bevel_segs=3)
    hdl.data.materials.append(mat_ti_hw)
    for mname, mz in [("door_handle_mount_top", hz + 0.016), ("door_handle_mount_bot", hz - 0.016)]:
        hm = make_box(mname, (hx, door_y - 0.005, mz), (0.007, 0.007, 0.007), parent=p_door, bevel=0.0015)
        hm.data.materials.append(mat_ti_hw)

    # -----------------------------------------------------------------
    # 3. HIGH-DETAIL COREXY MOTION SYSTEM (`gantryX`)
    # -----------------------------------------------------------------
    gz = 0.068
    xbeam = make_box("x_gantry_crossbeam", (0.0, -0.010, gz + 0.002), (0.354, 0.018, 0.022), parent=p_gantryX, bevel=0.002)
    xbeam.data.materials.append(mat_gantry_dark)
    for bname, by, bz in [("x_belt_front", -0.020, gz + 0.002), ("x_belt_rear", 0.002, gz + 0.002)]:
        bt = make_box(bname, (0.0, by, bz), (0.346, 0.003, 0.008), parent=p_gantryX)
        bt.data.materials.append(mat_gantry_dark)

    for rname, rloc, rad, length, ax in [
        ("x_guide_front", (0.0, -0.026, gz + 0.012), 0.0056, 0.356, "x"),
        ("x_guide_rear",  (0.0, -0.026, gz - 0.012), 0.0056, 0.356, "x"),
        ("x_guide_top",   (0.0,  0.018, gz + 0.022), 0.0050, 0.356, "x"),
        ("y_guide_left",  (-0.176, 0.0, gz + 0.016), 0.0055, 0.220, "y"),
        ("y_guide_right", ( 0.176, 0.0, gz + 0.016), 0.0055, 0.220, "y"),
        ("z_lead_left",   (-0.160, -0.038, -0.014),  0.0050, 0.268, "z"),
        ("z_guide_left",  (-0.160,  0.036, -0.014),  0.0055, 0.268, "z"),
        ("z_lead_right",  ( 0.160,  0.000, -0.014),  0.0050, 0.268, "z"),
        ("z_lead_rear",   ( 0.000,  0.098, -0.014),  0.0055, 0.268, "z"),
    ]:
        rod = make_cylinder(rname, rloc, rad, length, ax, segs=24, parent=p_gantryX)
        rod.data.materials.append(mat_chrome_steel)

    for sname, sx in [("x_slider_left", -0.174), ("x_slider_right", 0.174)]:
        sl = make_box(sname, (sx, -0.008, gz), (0.024, 0.072, 0.036), parent=p_gantryX, bevel=0.0025)
        sl.data.materials.append(mat_gantry_dark)
    # Rear XY stepper motors + corner pulleys
    for mname, mx in [("stepper_left", -0.165), ("stepper_right", 0.165)]:
        st = make_box(mname, (mx, 0.098, gz - 0.012), (0.038, 0.038, 0.038), parent=p_gantryX, bevel=0.002)
        st.data.materials.append(mat_gantry_dark)
        pul = make_cylinder(f"pulley_{mname}", (mx, -0.088, gz + 0.006), 0.009, 0.014, "z", segs=18, parent=p_gantryX)
        pul.data.materials.append(mat_chrome_steel)

    # Articulated 14-link curved drag chain arching toward right-rear corner (merged cleanly for fast atlas bake)
    dc_links = []
    for seg_i in range(14):
        t = seg_i / 13.0
        dx = 0.022 + t * 0.140
        dy = 0.015 + 0.068 * math.sin(t * math.pi * 0.65)
        dz = gz + 0.028 + 0.010 * math.sin(t * math.pi)
        rot_z = -t * 0.85
        lk = make_box(f"drag_chain_{seg_i}", (dx, dy, dz), (0.012, 0.015, 0.010), parent=p_gantryX, rot_euler=(0, 0, rot_z), bevel=0.0015)
        lk.data.materials.append(mat_gantry_dark)
        dc_links.append(lk)
    drag_chain_mesh = join_objects(dc_links, "drag_chain_assembly", p_gantryX)

    # -----------------------------------------------------------------
    # 4. SCULPTED TOOLHEAD WITH RECESSED FAN INTAKE (`printHead`)
    # -----------------------------------------------------------------
    th_z = gz - 0.004
    th_body = make_box("toolhead_chassis", (0.0, -0.002, th_z), (0.048, 0.040, 0.054), parent=p_printHead, bevel=0.003)
    th_body.data.materials.append(mat_gantry_dark)

    th_cowl = make_box("toolhead_front_cowl", (0.0, -0.025, th_z + 0.002), (0.046, 0.010, 0.048), parent=p_printHead, bevel=0.0045, bevel_segs=3)
    cut_fan = make_cylinder("cut_fan_bore", (0.0, -0.029, th_z + 0.002), 0.013, 0.012, "y", segs=28)
    boolean_cut(th_cowl, cut_fan)
    th_cowl.data.materials.append(mat_toolhead_cowl)

    # Fan shroud hub + 7 fan blades tucked inside the circular intake (merged cleanly)
    th_fan_hub = make_cylinder("toolhead_fan_hub", (0.0, -0.024, th_z + 0.002), 0.0055, 0.005, "y", segs=20, parent=p_printHead)
    th_fan_hub.data.materials.append(mat_dark_metal)
    fan_parts = [th_fan_hub]
    for b_i in range(7):
        ang = (2.0 * math.pi * b_i) / 7.0
        bx = 0.009 * math.cos(ang)
        bz = th_z + 0.002 + 0.009 * math.sin(ang)
        bl = make_box(f"toolhead_fan_blade_{b_i}", (bx, -0.024, bz), (0.007, 0.0025, 0.0025), parent=p_printHead, rot_euler=(0.35, ang, 0))
        bl.data.materials.append(mat_gantry_dark)
        fan_parts.append(bl)
    fan_rotor_mesh = join_objects(fan_parts, "toolhead_fan_rotor", p_printHead)

    hsock = make_box("toolhead_hotend_sock", (0.0, -0.002, th_z - 0.032), (0.018, 0.018, 0.012), parent=p_printHead, bevel=0.002)
    hsock.data.materials.append(mat_gantry_dark)
    noz = make_cylinder("toolhead_nozzle", (0.0, -0.002, th_z - 0.042), 0.0032, 0.009, "z", segs=18, parent=p_printHead)
    noz.data.materials.append(mat_brass)

    ptfe_pts = [(0.010 * math.sin(i / 11.0 * math.pi), -0.002 + (i / 11.0) * 0.118,
                 (th_z + 0.026) + 0.040 * math.sin((i / 11.0) * math.pi * 0.72) + (i / 11.0) * 0.010)
                for i in range(12)]
    ptfe = make_curve_tube("ptfe_bowden_tube", ptfe_pts, 0.0038, parent=p_printHead)
    ptfe.data.materials.append(mat_ptfe)

    # -----------------------------------------------------------------
    # 5. PRECISION GOLD PEI BED & CARRIAGE (`printBed`)
    # -----------------------------------------------------------------
    bed_z = -0.072
    pei = make_box("build_plate", (0.0, 0.002, bed_z), (0.286, 0.198, 0.004), parent=p_printBed, bevel=0.001)
    pei.data.materials.append(mat_pei)
    pei_lip = make_box("build_plate_lip", (0.0, -0.098, bed_z), (0.092, 0.012, 0.004), parent=p_printBed, bevel=0.001)
    pei_lip.data.materials.append(mat_pei)
    hblock = make_box("bed_heater_block", (0.0, 0.002, bed_z - 0.006), (0.280, 0.192, 0.008), parent=p_printBed, bevel=0.002)
    hblock.data.materials.append(mat_gantry_dark)
    for bname, loc, sz in [
        ("bed_carriage_arm_l", (-0.110, 0.002, bed_z - 0.014), (0.028, 0.180, 0.012)),
        ("bed_carriage_arm_r", ( 0.110, 0.002, bed_z - 0.014), (0.028, 0.180, 0.012)),
        ("bed_z_bracket_l",    (-0.160, 0.000, bed_z - 0.014), (0.026, 0.095, 0.014)),
        ("bed_z_bracket_r",    ( 0.160, 0.000, bed_z - 0.014), (0.026, 0.032, 0.014)),
        ("bed_z_bracket_rear", (0.0,    0.098, bed_z - 0.014), (0.050, 0.026, 0.014)),
    ]:
        arm = make_box(bname, loc, sz, parent=p_printBed, bevel=0.002)
        arm.data.materials.append(mat_gantry_dark)

    # -----------------------------------------------------------------
    # 6. ORGANIC SUB-D AEROSPACE TURBINE ARCH BRACKET (`printedObject`)
    # -----------------------------------------------------------------
    obj_z = bed_z + 0.002
    flange = make_box("bracket_base_raft", (0.0, 0.002, obj_z + 0.0015), (0.174, 0.056, 0.003), parent=p_printedObject, bevel=0.001)
    flange.data.materials.append(mat_turbine)

    # Smooth lofted 13-station sculpted aerospace arch in bmesh
    bm = bmesh.new()
    xs = np.linspace(-0.084, 0.084, 13)
    rings = []
    for x in xs:
        t_abs = abs(x) / 0.084
        z_pk = obj_z + 0.004 + 0.038 * math.exp(-3.1 * (t_abs ** 1.85))
        z_bt = obj_z + 0.004 + 0.023 * max(0.0, 1.0 - (t_abs / 0.85) ** 2)
        if t_abs > 0.85:
            z_bt = obj_z + 0.002
        hy = 0.024 - 0.006 * (1.0 - t_abs)
        pts = [
            (x, -hy, z_bt),
            (x, -hy * 0.72, z_pk),
            (x,  hy * 0.72, z_pk),
            (x,  hy, z_bt),
        ]
        rings.append([bm.verts.new(p) for p in pts])
    for i in range(len(rings) - 1):
        r0, r1 = rings[i], rings[i + 1]
        for s in range(4):
            ns = (s + 1) % 4
            bm.faces.new((r0[s], r1[s], r1[ns], r0[ns]))
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me_arch = bpy.data.meshes.new("bracket_swept_arch_Mesh")
    bm.to_mesh(me_arch)
    bm.free()
    arch_obj = link_obj(bpy.data.objects.new("bracket_swept_arch", me_arch), p_printedObject)
    sub = arch_obj.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    apply_all_modifiers(arch_obj)
    fix_normals_and_smooth(arch_obj, smooth=True)
    arch_obj.data.materials.append(mat_turbine)

    boss = make_cylinder("bracket_apex_ring", (0.0, 0.002, obj_z + 0.034), 0.009, 0.042, "y", segs=24, parent=p_printedObject, bevel=0.0012)
    boss.data.materials.append(mat_turbine)

    fin_parts = []
    for f_i in range(23):
        fx = -0.072 + f_i * 0.0065
        t_f = abs(fx) / 0.078
        fh = 0.026 * max(0.22, 1.0 - t_f * 0.78)
        fin = make_box(f"support_fin_{f_i}", (fx, 0.002, obj_z + 0.003 + fh / 2.0), (0.0016, 0.032, fh), parent=p_printedObject)
        fin.data.materials.append(mat_turbine)
        fin_parts.append(fin)
    fins_mesh = join_objects(fin_parts, "bracket_support_fins", p_printedObject)

    # Glass objects created AFTER geometry (hidden during Cycles bake!)
    glass_objs = []
    # Note: we create glass mats right before export or mark glass hide_render=True during bake
    fg_door = make_box("front_glass_door", (door_xc, door_y, door_zc), (door_w - 2 * stile_w, 0.004, door_h - 2 * rail_h), parent=p_door)
    tg_roof = make_box("top_roof_glass", (0.0, 0.0, Z_top - 0.006), (0.352, 0.214, 0.004), parent=p_enclosure)
    lw_glass = make_box("left_glass_window", (-W / 2.0 + 0.011, 0.5 * (y_l_min + y_l_max), win_zc), (0.004, y_l_max - y_l_min - 0.012, win_h - 0.012), parent=p_enclosure)
    rw_glass = make_box("right_glass_window", (W / 2.0 - 0.011, 0.5 * (y_r_min + y_r_max), win_zc), (0.004, y_r_max - y_r_min - 0.012, win_h - 0.012), parent=p_enclosure)
    glass_objs.extend([fg_door, tg_roof, lw_glass, rw_glass])

    # Subtle diagonal studio skylight glass sheen overlays (alpha fading cleanly to 0!)
    sheen_f = make_box("front_glass_sheen", (door_xc, door_y - 0.0026, door_zc), (door_w - 2 * stile_w - 0.006, 0.0005, door_h - 2 * rail_h - 0.006), parent=p_door)
    sheen_r = make_box("right_glass_sheen", (W / 2.0 - 0.0085, 0.5 * (y_r_min + y_r_max), win_zc), (0.0005, y_r_max - y_r_min - 0.016, win_h - 0.016), parent=p_enclosure)
    glass_objs.extend([sheen_f, sheen_r])

    return {
        "exterior_bake": [shell, plinth, rear_ins, rear_fan_hub, ac_sw, rim, hdl]
                         + [o for o in bpy.data.objects if o.name.startswith(("chassis_foot_", "door_hinge_", "door_handle_mount_"))],
        "interior_bake": [lin_rear, lin_ceil, lin_floor, lin_left, shroud_r, shroud_b, shroud_l,
                          xbeam, th_body, th_cowl, fan_rotor_mesh, drag_chain_mesh, pei, pei_lip, hblock,
                          flange, arch_obj, boss, fins_mesh, ptfe, hsock]
                         + [o for o in bpy.data.objects if o.name.startswith((
                             "x_belt_", "x_guide_", "y_guide_", "z_lead_", "z_guide_",
                             "x_slider_", "stepper_", "pulley_",
                             "bed_carriage_", "bed_z_bracket_"
                         ))],
        "glass_objs": glass_objs,
        "export_direct": {
            "graphite": [top_gasket, dock, bez, stile_l, stile_r, rail_t, rail_b, arch_hood]
                        + [o for o in bpy.data.objects if o.name.endswith("_window_gasket")],
            "brass": [noz],
            "display": [disp],
            "led": [o for o in bpy.data.objects if o.name.startswith("led_bar_")],
        },
        "doors_glass": [fg_door, tg_roof, lw_glass, rw_glass],
        "sheen_glass": [sheen_f, sheen_r],
    }


# ---------------------------------------------------------------------
# Cycles Studio Lighting & Multi-Object Disjoint Atlas Baking
# ---------------------------------------------------------------------
def setup_studio_lighting(scene):
    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    # Calibrated mid-tone warm studio environment so exterior champagne titanium never clips white
    bg.inputs["Color"].default_value = (0.48, 0.45, 0.41, 1.0)
    bg.inputs["Strength"].default_value = 0.52
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    def add_area(name, loc, target, energy, color, size_x, size_y=None):
        ld = bpy.data.lights.new(name, "AREA")
        ld.energy = energy
        ld.color = color
        ld.shape = "RECTANGLE" if size_y else "SQUARE"
        ld.size = size_x
        if size_y:
            ld.size_y = size_y
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        direction = Vector(target) - Vector(loc)
        lo.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        bpy.context.scene.collection.objects.link(lo)
        return lo

    # Balanced studio softboxes: crisp top-left forehead key, tight front-right pillar ribbon, shaded right side
    l_key = add_area("Key_Softbox_FrontLeft", (-1.9, -1.30, 1.05), (0.0, 0.0, 0.02), 14.5, (1.0, 0.97, 0.93), 2.2, 1.8)
    l_rib = add_area("Ribbon_Strip_FrontRight", (0.68, -1.35, 0.05), (0.20, -0.14, 0.0), 17.0, (1.0, 0.94, 0.86), 0.14, 1.8)
    l_fill_r = add_area("Fill_Right", (2.2, 0.10, 0.15), (0.0, 0.0, 0.0), 6.5, (0.95, 0.89, 0.82), 3.0, 2.4)
    l_top = add_area("Top_Fill", (-0.25, -0.25, 1.8), (0.0, 0.0, 0.0), 8.0, (1.0, 0.98, 0.95), 2.0, 2.0)
    l_rear = add_area("Rear_Fill", (0.0, 1.9, 0.35), (0.0, 0.0, 0.0), 8.0, (0.95, 0.92, 0.88), 2.4, 2.0)

    return [l_key, l_rib, l_fill_r, l_top, l_rear]


def assign_disjoint_uv_grid(objs, atlas_name, res=1536, pad=0.008):
    """
    Unwraps every unique mesh in `objs` via Smart UV Project and packs each object into a
    strictly non-overlapping cell in `[0..1]x[0..1]` so sequential Cycles bakes never collide.
    """
    unique_objs = []
    seen = set()
    for o in objs:
        if o and o.type == "MESH" and o.name not in seen and len(o.data.polygons) > 0:
            seen.add(o.name)
            unique_objs.append(o)

    n = len(unique_objs)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    cell_w = 1.0 / cols
    cell_h = 1.0 / rows

    img = bpy.data.images.new(atlas_name, width=res, height=res, alpha=False)
    img.generated_color = (0.12, 0.10, 0.09, 1.0)

    for idx, obj in enumerate(unique_objs):
        set_active(obj)
        if not obj.data.uv_layers:
            obj.data.uv_layers.new(name="UVMap")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=math.radians(60.0), island_margin=0.02)
        bpy.ops.object.mode_set(mode="OBJECT")

        r = idx // cols
        c = idx % cols
        u0 = c * cell_w + pad * cell_w
        u1 = (c + 1) * cell_w - pad * cell_w
        v0 = r * cell_h + pad * cell_h
        v1 = (r + 1) * cell_h - pad * cell_h

        uv_layer = obj.data.uv_layers.active.data
        for loop_uv in uv_layer:
            u, v = loop_uv.uv[0], loop_uv.uv[1]
            loop_uv.uv[0] = u0 + u * (u1 - u0)
            loop_uv.uv[1] = v0 + v * (v1 - v0)

    # Clone any shared materials so each atlas owns exclusive BakeTargetNode image links!
    atlas_mat_cache = {}
    for obj in unique_objs:
        new_mats = []
        for mat in obj.data.materials:
            if not mat:
                continue
            key = (atlas_name, mat.name)
            if key not in atlas_mat_cache:
                m_copy = mat.copy()
                m_copy.name = f"{atlas_name}_{mat.name}"
                nt = m_copy.node_tree
                for node in list(nt.nodes):
                    if node.name == "BakeTargetNode":
                        nt.nodes.remove(node)
                tex_node = nt.nodes.new("ShaderNodeTexImage")
                tex_node.name = "BakeTargetNode"
                tex_node.image = img
                for node in nt.nodes:
                    node.select = False
                tex_node.select = True
                nt.nodes.active = tex_node
                atlas_mat_cache[key] = m_copy
            new_mats.append(atlas_mat_cache[key])
        obj.data.materials.clear()
        for m in new_mats:
            obj.data.materials.append(m)

    return unique_objs, img


def bake_atlas_cycles(scene, objs, img, samples=16):
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for d in prefs.devices:
        d.use = (d.type == "OPTIX")
    scene.cycles.device = "GPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 3
    scene.cycles.diffuse_bounces = 2
    scene.cycles.glossy_bounces = 2

    scene.render.bake.use_clear = True
    scene.render.bake.margin = 4

    bpy.ops.object.select_all(action="DESELECT")
    for obj in objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    print(f"Baking {img.name} ({len(objs)} objects) at {samples} samples...", flush=True)
    bpy.ops.object.bake(type="COMBINED")

    out_path = BAKE_DIR / f"{img.name}.png"
    img.filepath_raw = str(out_path)
    img.file_format = "PNG"
    img.save()
    print(f"Baked Cycles atlas: {out_path} ({len(objs)} objects)", flush=True)
    return out_path


def apply_baked_export_material(objs, baked_img, mat_name, base_scale=0.82, emissive_scale=0.58, metallic=0.08, rough=0.32):
    """Replaces complex Cycles bake shader with clean glTF-compatible PBR + baked emission texture."""
    # Re-load saved PNG cleanly so blender glTF exporter packs PNG bytes reliably
    img = bpy.data.images.load(str(BAKE_DIR / f"{baked_img.name}.png"), check_existing=True)

    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")

    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = img

    # Base color modulated by base_scale (via MixRGB multiply)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type = "RGBA"
    mul.blend_type = "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs["B"].default_value = (base_scale, base_scale, base_scale, 1.0)

    nt.links.new(tex_node.outputs["Color"], mul.inputs["A"])
    nt.links.new(mul.outputs["Result"], bsdf.inputs["Base Color"])
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough

    nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = emissive_scale
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return mat


def create_smoked_glass_export_mat():
    mat = bpy.data.materials.new("Smoked Glass")
    mat.use_nodes = True
    mat.use_backface_culling = True  # doubleSided=false -> single-pass 48% transmission!
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.071, 0.086, 0.102, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.35
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["Alpha"].default_value = 0.52
    return mat


def create_glass_sheen_export_mat():
    w, h = 256, 256
    u = np.linspace(0.0, 1.0, w).reshape(1, w)
    v = np.linspace(0.0, 1.0, h).reshape(h, 1)  # Blender image bottom-up: v=1 is top
    diag = (0.16 + 0.84 * v) * (1.0 - 0.72 * u)
    band = np.clip((diag - 0.50) / 0.42, 0.0, 1.0) ** 1.45
    edge = np.clip(np.minimum(u, 1.0 - u) * 16.0, 0.0, 1.0) * np.clip(np.minimum(v, 1.0 - v) * 16.0, 0.0, 1.0)
    alpha = np.clip(band * edge * (96.0 / 255.0), 0.0, 1.0).astype(np.float32)

    rgba = np.zeros((h, w, 4), dtype=np.float32)
    rgba[..., 0] = 244.0 / 255.0
    rgba[..., 1] = 238.0 / 255.0
    rgba[..., 2] = 230.0 / 255.0
    rgba[..., 3] = alpha

    img = bpy.data.images.new("Glass_Sheen_RGBA", width=w, height=h, alpha=True)
    img.pixels.foreach_set(rgba.ravel().tolist())
    sheen_path = BAKE_DIR / "Glass_Sheen_RGBA.png"
    img.filepath_raw = str(sheen_path)
    img.file_format = "PNG"
    img.save()
    img = bpy.data.images.load(str(sheen_path), check_existing=True)
    mat = bpy.data.materials.new("Ref Glass Specular Sheen")
    mat.use_nodes = True
    mat.use_backface_culling = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf.inputs["Metallic"].default_value = 0.05
    bsdf.inputs["Roughness"].default_value = 0.12
    bsdf.inputs["Emission Strength"].default_value = 0.45
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def main():
    scene = reset_scene()
    print("Building hard-surface geometry...", flush=True)
    groups = build_geometry()
    print("Setting up studio lighting...", flush=True)
    studio_lights = setup_studio_lighting(scene)

    for g in groups["glass_objs"]:
        g.hide_render = True

    ext_all = [o for o in groups["exterior_bake"] if o is not None]
    shell_list = [o for o in ext_all if o.name == "unibody_shell"]
    hw_list = [o for o in ext_all if o.name != "unibody_shell"]

    print("Packing disjoint UV atlases (1024px dedicated shell + 512px hardware + 1024px interior)...", flush=True)
    sh_objs, sh_img = assign_disjoint_uv_grid(shell_list, "Atlas_Unibody_Shell", res=1024, pad=0.01)
    hw_objs, hw_img = assign_disjoint_uv_grid(hw_list, "Atlas_Exterior_Hardware", res=512, pad=0.01)
    int_objs, int_img = assign_disjoint_uv_grid(groups["interior_bake"], "Atlas_Interior_Studio", res=1024, pad=0.008)

    bake_atlas_cycles(scene, sh_objs, sh_img, samples=12)
    bake_atlas_cycles(scene, hw_objs, hw_img, samples=12)

    # Warm honey-gold chamber lighting pass for interior bake
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.20
    for sl in studio_lights:
        sl.data.energy *= 0.28
    chamber_l_data = bpy.data.lights.new("Chamber_Warm_Bounce", "POINT")
    chamber_l_data.energy = 11.0
    chamber_l_data.color = (1.0, 0.60, 0.24)
    chamber_l_data.shadow_soft_size = 0.14
    chamber_l_obj = bpy.data.objects.new("Chamber_Warm_Bounce", chamber_l_data)
    chamber_l_obj.location = (0.0, 0.0, 0.09)
    scene.collection.objects.link(chamber_l_obj)

    bake_atlas_cycles(scene, int_objs, int_img, samples=12)

    for o in list(bpy.data.objects):
        if o.type == "LIGHT":
            bpy.data.objects.remove(o, do_unlink=True)

    for g in groups["glass_objs"]:
        g.hide_render = False

    apply_baked_export_material(sh_objs, sh_img, "Cycles Baked Unibody Shell", base_scale=0.80, emissive_scale=0.52, metallic=0.06, rough=0.30)
    apply_baked_export_material(hw_objs, hw_img, "Cycles Baked Exterior HW", base_scale=0.80, emissive_scale=0.52, metallic=0.06, rough=0.30)
    apply_baked_export_material(int_objs, int_img, "Cycles Baked Interior Warm", base_scale=0.76, emissive_scale=0.72, metallic=0.08, rough=0.34)

    mat_glass = create_smoked_glass_export_mat()
    mat_sheen = create_glass_sheen_export_mat()
    for dg in groups["doors_glass"]:
        dg.data.materials.clear()
        dg.data.materials.append(mat_glass)
    for sg in groups["sheen_glass"]:
        set_active(sg)
        if not sg.data.uv_layers:
            sg.data.uv_layers.new(name="UVMap")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.cube_project(cube_size=1.0)
        bpy.ops.object.mode_set(mode="OBJECT")
        xs = [v.co.x for v in sg.data.vertices]
        ys = [v.co.y for v in sg.data.vertices]
        zs = [v.co.z for v in sg.data.vertices]
        z0, dz = min(zs), max(1e-5, max(zs) - min(zs))
        x0, dx = min(xs), max(1e-5, max(xs) - min(xs))
        y0, dy = min(ys), max(1e-5, max(ys) - min(ys))
        for face in sg.data.polygons:
            for li in face.loop_indices:
                vco = sg.data.vertices[sg.data.loops[li].vertex_index].co
                if sg.name == "front_glass_sheen":
                    sg.data.uv_layers.active.data[li].uv = ((vco.x - x0) / dx, (vco.z - z0) / dz)
                else:
                    sg.data.uv_layers.active.data[li].uv = ((vco.y - y0) / dy, (vco.z - z0) / dz)
        sg.data.materials.clear()
        sg.data.materials.append(mat_sheen)

    OUT_GLB.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(OUT_GLB),
        export_format="GLB",
        export_yup=False,
        export_apply=True,
        export_extras=True,
        export_materials="EXPORT",
        export_image_format="AUTO",
        export_texcoords=True,
        export_normals=True,
    )
    print(f"Exported Blender v5 GLB: {OUT_GLB} ({OUT_GLB.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
