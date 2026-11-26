"""
TASK-044: True-3D Multi-Material PBR & Mechanical Detail Reconstruction (v12)
Generates: assets/models/raw/deltrol_p2s_explorer_v14.glb

Fixes all TASK-043 visual/material blockers while keeping strict silhouette fidelity:
  1. Separate Physically Based Materials (NO single flattened unlit interior material):
     - Champagne Satin Shell (brushed titanium/aluminum base + roughnessMap + subtle studio fill)
     - Machined Steel Rails (high-metalness brushed steel base + roughnessMap + turned-rod sheen)
     - Anodized Copper Toolhead (metallic bronze/copper shroud + heatsink ribs + fan bore)
     - Machined Dark Alloy (gantry extrusions, drag chain, Z brackets, steppers, plinth)
     - Brass Nozzle (built-in metallic brass)
     - Dark Graphite PEI Bed (stippled charcoal-gold textured PEI map + metallic roughness)
     - Sculpted Metallic Turbine Arch (metallic titanium print w/ multi-ribbed fins + bright ridges)
     - Warm Chamber Anodized Interior (brushed amber-bronze wall panels + CNC flutes + Z-screws)
     - Console OLED Glass + Brushed Metal Rim + Slim Graphite Door Frame + Smoked Glass + Skylight Wedge
  2. Enhanced Mechanical 3D Geometry:
     - Top-cap sculpted shoulder bevel & left-to-right roof taper + integrated corner foot tabs
     - Fluted CNC rear chamber wall, exhaust louver fan grille, Z-axis stepper & leadscrew collars,
       dual X steel guide rods + rear rod + Y rails + timing pulleys + ribbed curved drag chain
     - Multi-part CNC copper toolhead shroud, recessed fan intake shroud, 7-blade rotor, heatsink fins,
       pneumatic Bowden collet fitting, and curved white PTFE tube
     - Sculpted hollow multi-ribbed aerospace turbine arch with 27 tapered support fins & chamfered raft
     - Sleek recessed lower OLED console with subtle UI bar + brushed champagne outer rim
  3. Zero image planes, zero billboards, zero 2.5D depth rigs.
"""

import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_explorer_v14.glb"
BAKE_DIR = Path(r"C:\Users\PC\.gemini\antigravity\brain\4241a9a6-bf9f-48f0-84bf-532f80b9bfc1\scratch\v13_explorer_bake")
BAKE_DIR.mkdir(parents=True, exist_ok=True)


# Exact Three.js r160+ ACESFilmicToneMapping matrices & RRTAndODTFit analytic inverse
_ACES_IN = np.array([
    [0.59719, 0.35458, 0.04823],
    [0.07600, 0.90834, 0.01566],
    [0.02840, 0.13383, 0.83777],
], dtype=np.float64)
_ACES_OUT = np.array([
    [ 1.60475, -0.53108, -0.07367],
    [-0.10208,  1.10813, -0.00605],
    [-0.00327, -0.07276,  1.07602],
], dtype=np.float64)
_ACES_IN_INV = np.linalg.inv(_ACES_IN)
_ACES_OUT_INV = np.linalg.inv(_ACES_OUT)


def srgb_target_to_linear_aces(rgb_255):
    """Exact analytic inverse of Three.js ACESFilmicToneMapping (exposure=1.05) + sRGB OETF."""
    arr = np.asarray(rgb_255, dtype=np.float64)
    is_1d = (arr.ndim == 1)
    if is_1d:
        arr = arr[None, :]
    s = np.clip(arr / 255.0, 0.0, 0.992)
    t_lin = np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
    r = np.clip(t_lin @ _ACES_OUT_INV.T, 0.0, 0.993)
    A = 1.0 - 0.983729 * r
    B = 0.0245786 - 0.4329510 * r
    C = -(0.000090537 + 0.238081 * r)
    v = (-B + np.sqrt(np.maximum(0.0, B * B - 4.0 * A * C))) / (2.0 * A)
    c = np.maximum(0.0, v @ _ACES_IN_INV.T) / (1.05 / 0.6)
    out = c.astype(np.float32)
    return out[0] if is_1d else out


def linear_to_srgb_float(lin_rgb):
    c = np.clip(lin_rgb, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * (c ** (1.0 / 2.4)) - 0.055).astype(np.float32)


# ---------------------------------------------------------------------
# Blender Scene & Mesh Builders
# ---------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    optix_devs = [d for d in prefs.devices if d.type == "OPTIX"]
    for d in prefs.devices:
        d.use = (d.type == "OPTIX")
    scene.cycles.device = "GPU" if optix_devs else "CPU"
    return scene


def set_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def link_obj(obj, parent=None):
    if obj.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(obj)
    if parent is not None:
        obj.parent = parent
    return obj


def make_collection_parent(name):
    emp = bpy.data.objects.new(name, None)
    emp.empty_display_type = "PLAIN_AXES"
    emp.empty_display_size = 0.02
    bpy.context.scene.collection.objects.link(emp)
    emp["logicalPart"] = name
    return emp


def apply_all_modifiers(obj):
    set_active(obj)
    for mod in list(obj.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
            bpy.ops.object.convert(target="MESH")


def fix_normals_and_smooth(obj, smooth=True, auto_angle_deg=35.0):
    set_active(obj)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    me = obj.data
    for p in me.polygons:
        p.use_smooth = smooth
    if smooth and hasattr(me, "shade_smooth"):
        try:
            bpy.ops.object.shade_smooth_by_angle(angle=math.radians(auto_angle_deg))
        except Exception:
            pass
    me.update()


def make_box(name, center, size, parent=None, rot_euler=(0, 0, 0), bevel=0.0, bevel_segs=2):
    sx, sy, sz = size
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(scale=True)
    if bevel > 0.0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = bevel_segs
        mod.limit_method = "ANGLE"
        mod.use_clamp_overlap = True
        apply_all_modifiers(obj)
    obj.location = center
    obj.rotation_euler = Euler(rot_euler, "XYZ")
    if parent is not None:
        obj.parent = parent
    fix_normals_and_smooth(obj, smooth=(bevel > 0.0))
    return obj


def make_cylinder(name, center, radius, length, axis="z", segs=24, parent=None, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=segs, radius=radius, depth=length, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    if axis == "x":
        obj.rotation_euler = (0.0, math.pi / 2.0, 0.0)
    elif axis == "y":
        obj.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
    bpy.ops.object.transform_apply(rotation=True)
    if bevel > 0.0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        mod.use_clamp_overlap = True
        apply_all_modifiers(obj)
    obj.location = center
    if parent is not None:
        obj.parent = parent
    fix_normals_and_smooth(obj, smooth=True)
    return obj


def make_asym_rounded_prism(name, width, depth, z_bot, z_top, r_left, r_right, seg=18, parent=None,
                            top_drop_x=0.016, top_drop_y=0.016, left_shoulder_drop=0.004):
    """
    True-3D asymmetric enclosure prism matching P2S reference silhouette:
    - Sleek tight left stile (`r_left=0.008`), sweeping dominant front-right pillar (`r_right=0.036`)
    - Gentle left-to-right and front-to-rear top cap taper + front-left tip shoulder relief
    """
    hw, hd = width / 2.0, depth / 2.0
    corners = [
        (-hw + r_left,  -hd + r_left,  r_left,  math.pi,       1.5 * math.pi),
        ( hw - r_right, -hd + r_right, r_right, 1.5 * math.pi, 2.0 * math.pi),
        ( hw - r_right,  hd - r_right, r_right, 0.0,           0.5 * math.pi),
        (-hw + r_left,   hd - r_left,  r_left,  0.5 * math.pi, math.pi),
    ]
    pts_2d = []
    for cx, cy, rad, a0, a1 in corners:
        for i in range(seg + 1):
            a = a0 + (a1 - a0) * (i / seg)
            pts_2d.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))

    bm = bmesh.new()
    bot_verts, top_verts = [], []
    for px, py in pts_2d:
        bot_verts.append(bm.verts.new((px, py, z_bot)))
        tx = max(0.0, (px - (-hw * 0.25)) / (hw * 1.25))
        ty = max(0.0, (py + hd) / depth)
        tl_drop = left_shoulder_drop * max(0.0, (-px - hw * 0.45) / (hw * 0.55)) ** 1.4
        dz = -(top_drop_x * (tx ** 1.55) + top_drop_y * (ty ** 1.45) + tl_drop)
        top_verts.append(bm.verts.new((px, py, z_top + dz)))

    n = len(pts_2d)
    for i in range(n):
        ni = (i + 1) % n
        bm.faces.new((bot_verts[i], bot_verts[ni], top_verts[ni], top_verts[i]))
    bm.faces.new(list(reversed(bot_verts)))
    bm.faces.new(top_verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    me = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(me)
    bm.free()
    obj = link_obj(bpy.data.objects.new(name, me), parent)
    fix_normals_and_smooth(obj, smooth=True)
    return obj


def make_trapezoid_arch(name, center_x, width_bot, width_top, center_y, depth, z0, z1, parent=None, bevel=0.0, axis="XZ"):
    bm = bmesh.new()
    wb, wt = width_bot / 2.0, width_top / 2.0
    hd = depth / 2.0
    if axis == "XZ":
        pts = [
            (-wb, -hd, z0), ( wb, -hd, z0), ( wt, -hd, z1), (-wt, -hd, z1),
            (-wb,  hd, z0), ( wb,  hd, z0), ( wt,  hd, z1), (-wt,  hd, z1),
        ]
    else:
        pts = [
            (-hd, -wb, z0), (-hd,  wb, z0), (-hd,  wt, z1), (-hd, -wt, z1),
            ( hd, -wb, z0), ( hd,  wb, z0), ( hd,  wt, z1), ( hd, -wt, z1),
        ]
    vs = [bm.verts.new(p) for p in pts]
    for f in [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        bm.faces.new([vs[i] for i in f])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(me)
    bm.free()
    obj = link_obj(bpy.data.objects.new(name, me), parent)
    if bevel > 0.0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 2
        mod.limit_method = "ANGLE"
        mod.use_clamp_overlap = True
        apply_all_modifiers(obj)
    obj.location = (center_x, center_y, 0.0)
    fix_normals_and_smooth(obj, smooth=(bevel > 0.0))
    return obj


def make_curve_tube(name, points, radius, parent=None):
    cu = bpy.data.curves.new(name + "_Curve", type="CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 18
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("NURBS")
    sp.points.add(len(points) - 1)
    for i, pt in enumerate(points):
        sp.points[i].co = (pt[0], pt[1], pt[2], 1.0)
    sp.use_endpoint_u = True
    cu_obj = link_obj(bpy.data.objects.new(name, cu), parent)
    set_active(cu_obj)
    bpy.ops.object.convert(target="MESH")
    mesh_obj = bpy.context.active_object
    fix_normals_and_smooth(mesh_obj, smooth=True)
    return mesh_obj


def boolean_cut(target_obj, cutter_obj, op="DIFFERENCE"):
    set_active(target_obj)
    mod = target_obj.modifiers.new("Bool_" + cutter_obj.name, "BOOLEAN")
    mod.operation = op
    mod.object = cutter_obj
    if hasattr(mod, "solver"):
        mod.solver = "EXACT"
    apply_all_modifiers(target_obj)
    bpy.data.objects.remove(cutter_obj, do_unlink=True)


def join_objects(objs, new_name, parent):
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


def make_mat(name, base_rgb=(0.1, 0.1, 0.1), metallic=0.1, rough=0.4):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*base_rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    return mat


# ---------------------------------------------------------------------
# Build Connected True-3D Mechanical & Architectural Geometry
# ---------------------------------------------------------------------
def build_geometry():
    W, D = 0.422, 0.282
    R_left, R_right = 0.008, 0.036
    Z_bot, Z_top = -0.197, 0.184
    Z_chin_top = -0.144
    Z_door_top = 0.130
    Z_side_arch = -0.178

    p_enclosure = make_collection_parent("enclosure")
    p_door = make_collection_parent("door")
    p_printHead = make_collection_parent("printHead")
    p_printBed = make_collection_parent("printBed")
    p_gantryX = make_collection_parent("gantryX")
    p_printedObject = make_collection_parent("printedObject")

    mat_tmp = make_mat("Temp_Bake")
    mat_graphite = make_mat("Graphite Door Frame", (0.045, 0.048, 0.055), metallic=0.45, rough=0.32)
    mat_seal = make_mat("Dark Seal Polymer", (0.035, 0.037, 0.042), metallic=0.06, rough=0.56)
    mat_brass = make_mat("Brass Nozzle", (0.88, 0.68, 0.18), metallic=0.92, rough=0.18)

    # 1. Sculpted Asymmetric Unibody Shell
    shell = make_asym_rounded_prism(
        "unibody_shell", W, D, Z_bot, Z_top, R_left, R_right,
        seg=20, parent=p_enclosure, top_drop_x=0.017, top_drop_y=0.017, left_shoulder_drop=0.004
    )

    cavity = make_asym_rounded_prism(
        "cut_cavity", W - 0.044, D - 0.044, Z_chin_top, Z_door_top, 0.008, 0.008,
        seg=6, top_drop_x=0.0, top_drop_y=0.0, left_shoulder_drop=0.0
    )
    boolean_cut(shell, cavity)

    x_f_min = -W / 2.0 + R_left + 0.009
    x_f_max =  W / 2.0 - R_right - 0.014
    door_w = x_f_max - x_f_min
    door_xc = 0.5 * (x_f_min + x_f_max)
    door_h = (Z_door_top - 0.004) - Z_chin_top
    door_zc = 0.5 * ((Z_door_top - 0.004) + Z_chin_top)
    cut_front = make_box("cut_front", (door_xc, -D / 2.0 - 0.004, door_zc + 0.001), (door_w, 0.056, door_h - 0.002))
    boolean_cut(shell, cut_front)

    cut_top = make_asym_rounded_prism(
        "cut_top", 0.336, 0.204, Z_door_top - 0.004, Z_top + 0.025, 0.012, 0.012,
        seg=10, top_drop_x=0.0, top_drop_y=0.0, left_shoulder_drop=0.0
    )
    boolean_cut(shell, cut_top)

    y_l_min, y_l_max = -D / 2.0 + R_left + 0.020, D / 2.0 - R_left - 0.020
    y_r_min, y_r_max = -D / 2.0 + R_right + 0.008, D / 2.0 - R_right - 0.008
    win_bot = Z_chin_top + 0.012
    win_top = Z_door_top - 0.020
    win_zc = 0.5 * (win_top + win_bot)
    win_h = win_top - win_bot
    cut_win_r = make_box("cut_win_r", ( W / 2.0 - 0.004, 0.5 * (y_r_min + y_r_max), win_zc), (0.044, y_r_max - y_r_min, win_h))
    boolean_cut(shell, cut_win_r)
    cut_win_l = make_box("cut_win_l", (-W / 2.0 + 0.004, 0.5 * (y_l_min + y_l_max), win_zc), (0.044, y_l_max - y_l_min, win_h))
    boolean_cut(shell, cut_win_l)

    arch_r_bot = D - 2 * R_right - 0.088
    arch_r_top = D - 2 * R_right - 0.116
    cut_arch_r = make_trapezoid_arch("cut_arch_r", W / 2.0 - 0.008, arch_r_bot, arch_r_top, 0.0, 0.052, Z_bot - 0.008, Z_side_arch, bevel=0.001, axis="YZ")
    boolean_cut(shell, cut_arch_r)
    cut_arch_l = make_trapezoid_arch("cut_arch_l", -W / 2.0 + 0.008, D - 2 * R_left - 0.088, D - 2 * R_left - 0.116, 0.0, 0.052, Z_bot - 0.008, Z_side_arch, bevel=0.001, axis="YZ")
    boolean_cut(shell, cut_arch_l)
    cut_chin = make_box("cut_chin", (door_xc, -D / 2.0, Z_bot - 0.008), (door_w - 0.084, 0.060, 0.020))
    boolean_cut(shell, cut_chin)

    cut_rear = make_box("cut_rear", (0.0, D / 2.0 + 0.008, 0.0), (W - 0.084, 0.024, (Z_door_top - Z_chin_top) + 0.02), bevel=0.003)
    boolean_cut(shell, cut_rear)

    bm_clean = bmesh.new()
    bm_clean.from_mesh(shell.data)
    stray = [f for f in bm_clean.faces if (abs(f.calc_center_median().x) < (W/2.0 - 0.024) and abs(f.calc_center_median().y) < (D/2.0 - 0.025) and (Z_chin_top + 0.003) < f.calc_center_median().z < (Z_door_top - 0.003))]
    if stray:
        bmesh.ops.delete(bm_clean, geom=stray, context="FACES")
        bm_clean.to_mesh(shell.data)
    bm_clean.free()

    # Generous top/edge shoulder bevel matching reference rounded aluminum extrusion
    bev = shell.modifiers.new("EdgeBevel", "BEVEL")
    bev.width = 0.0095
    bev.segments = 4
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(30.0)
    bev.use_clamp_overlap = True
    bev.harden_normals = False
    apply_all_modifiers(shell)
    fix_normals_and_smooth(shell, smooth=True, auto_angle_deg=34.0)
    shell.data.materials.append(mat_tmp)

    # Integrated Plinth & Sculpted Metallic Corner Foot Housings + Rubber Pads
    plinth = make_asym_rounded_prism(
        "chassis_recessed_plinth", W - 0.024, D - 0.024, Z_bot - 0.001, Z_chin_top + 0.002, 0.010, 0.020,
        seg=8, parent=p_enclosure, top_drop_x=0.0, top_drop_y=0.0, left_shoulder_drop=0.0
    )
    plinth.data.materials.append(mat_tmp)
    foot_objs = []
    for i, (fx, fy, fw, fz) in enumerate([
        (-W / 2.0 + 0.022, -D / 2.0 + 0.022, 0.026, Z_bot - 0.0015),
        ( W / 2.0 - 0.036, -D / 2.0 + 0.036, 0.028, Z_bot - 0.0005),
        ( W / 2.0 - 0.036,  D / 2.0 - 0.036, 0.028, Z_bot - 0.0015),
        (-W / 2.0 + 0.022,  D / 2.0 - 0.022, 0.026, Z_bot - 0.0015),
    ]):
        ft = make_cylinder(f"chassis_foot_{i}", (fx, fy, fz), fw * 0.48, 0.006, "z", segs=20, parent=p_enclosure, bevel=0.0012)
        ft.data.materials.append(mat_tmp)
        foot_objs.append(ft)

    rear_ins = make_box("rear_panel_insert", (0.0, D / 2.0 - 0.014, 0.0), (W - 0.094, 0.012, Z_door_top - Z_chin_top + 0.016), parent=p_enclosure, bevel=0.0015)
    rear_ins.data.materials.append(mat_tmp)
    rear_fan_hub = make_cylinder("rear_exhaust_shroud", (-0.015, D / 2.0 - 0.006, 0.068), 0.042, 0.006, "y", segs=24, parent=p_enclosure, bevel=0.001)
    rear_fan_hub.data.materials.append(mat_tmp)
    ac_sw = make_box("rear_ac_module", (0.115, D / 2.0 - 0.006, Z_bot + 0.022), (0.062, 0.008, 0.022), parent=p_enclosure, bevel=0.001)
    ac_sw.data.materials.append(mat_tmp)

    # Skylight & Side Window Seals — match roof drop so gasket sits flush inside recessed roof pocket
    top_gasket = make_asym_rounded_prism(
        "top_rim_outer", 0.336, 0.204, Z_top - 0.028, Z_top - 0.020, 0.012, 0.012,
        seg=12, parent=p_enclosure, top_drop_x=0.015, top_drop_y=0.015, left_shoulder_drop=0.003
    )
    cut_tg = make_asym_rounded_prism(
        "cut_tg", 0.312, 0.180, Z_top - 0.034, Z_top - 0.006, 0.008, 0.008,
        seg=10, top_drop_x=0.0, top_drop_y=0.0, left_shoulder_drop=0.0
    )
    boolean_cut(top_gasket, cut_tg)
    top_gasket.data.materials.clear()
    top_gasket.data.materials.append(mat_seal)

    for sname, sx_s, ymin, ymax in [("left", -1.0, y_l_min, y_l_max), ("right", 1.0, y_r_min, y_r_max)]:
        gx = sx_s * (W / 2.0 - 0.010)
        gasket = make_box(f"{sname}_window_gasket", (gx, 0.5 * (ymin + ymax), win_zc), (0.024, ymax - ymin + 0.006, win_h + 0.006), parent=p_enclosure)
        cut_wg = make_box(f"cut_wg_{sname}", (gx, 0.5 * (ymin + ymax), win_zc), (0.044, ymax - ymin - 0.022, win_h - 0.022))
        boolean_cut(gasket, cut_wg)
        gasket.data.materials.clear()
        gasket.data.materials.append(mat_seal)

    # Detailed CNC Chamber Liners, Louvers, Corner Columns & Lighting Strips
    rear_zc = 0.5 * (Z_door_top + Z_chin_top)
    rear_h = (Z_door_top - Z_chin_top) - 0.008
    lin_rear = make_box("interior_rear_panel", (0.0, D / 2.0 - 0.029, rear_zc), (W - 0.056, 0.006, rear_h), parent=p_enclosure)
    lin_ceil = make_box("interior_ceiling_liner", (0.0, 0.0, Z_door_top - 0.005), (W - 0.056, D - 0.056, 0.005), parent=p_enclosure)
    lin_floor = make_box("interior_floor_tray", (0.0, 0.0, Z_chin_top + 0.004), (W - 0.056, D - 0.056, 0.005), parent=p_enclosure)
    lin_left = make_box("interior_left_back_baffle", (-W / 2.0 + 0.025, 0.0, rear_zc), (0.005, D - 0.056, rear_h), parent=p_enclosure)

    # Detailed Rear Bulkhead: ribbed electronics shroud, exhaust blower ring, vertical frame columns
    shroud_r = make_box("interior_right_lower_shroud", (W / 2.0 - 0.040, 0.056, -0.052), (0.024, 0.098, 0.148), parent=p_enclosure, bevel=0.003)
    shroud_b = make_box("interior_rear_electronics_box", (0.068, D / 2.0 - 0.046, -0.024), (0.132, 0.026, 0.150), parent=p_enclosure, bevel=0.004)
    shroud_l = make_box("interior_rear_chute_box", (-0.088, D / 2.0 - 0.046, 0.014), (0.068, 0.026, 0.126), parent=p_enclosure, bevel=0.003)
    blower_l = make_box("interior_aux_blower_housing", (-0.168, 0.016, 0.005), (0.016, 0.118, 0.058), parent=p_enclosure, bevel=0.003)
    shroud_parts = [shroud_r, shroud_b, shroud_l, blower_l]
    for r_i in range(6):
        rib = make_box(f"shroud_rib_{r_i}", (0.020 + r_i * 0.020, D / 2.0 - 0.061, -0.024), (0.006, 0.006, 0.126), parent=p_enclosure, bevel=0.001)
        shroud_parts.append(rib)
    for col_x, col_y in [(-0.172, -0.098), (-0.172, 0.098), (0.166, 0.098)]:
        col_post = make_box(f"chamber_corner_post_{col_x:.2f}_{col_y:.2f}", (col_x, col_y, rear_zc), (0.014, 0.014, rear_h - 0.004), parent=p_enclosure, bevel=0.002)
        shroud_parts.append(col_post)
    shroud_merged = join_objects(shroud_parts, "interior_rear_electronics_box", p_enclosure)

    # Rear circular chamber exhaust ring & Z-nut collars on dark alloy
    alloy_interior = [shroud_merged]
    exhaust_ring = make_cylinder("chamber_rear_exhaust_ring", (-0.012, D / 2.0 - 0.036, 0.064), 0.034, 0.008, "y", segs=24, parent=p_enclosure, bevel=0.0015)
    alloy_interior.append(exhaust_ring)

    led_objs = []
    for lname, loc, sz in [
        ("led_bar_front", (0.0, -0.092, Z_door_top - 0.008), (0.296, 0.016, 0.005)),
        ("led_bar_left",  (-0.156, 0.0, Z_door_top - 0.008), (0.014, 0.180, 0.005)),
        ("led_bar_right", ( 0.154, 0.0, Z_door_top - 0.008), (0.014, 0.180, 0.005)),
    ]:
        lb = make_box(lname, loc, sz, parent=p_enclosure)
        led_objs.append(lb)

    # Compact Sleek Lower OLED Console (`screen_*`)
    con_ang = math.radians(-23.0)
    cx_con = door_xc - 0.004
    con_y = -D / 2.0 - 0.004
    con_z = Z_chin_top - 0.009
    n_y, n_z = -math.cos(con_ang), -math.sin(con_ang)

    dock = make_box("screen_dock_wedge", (cx_con, -D / 2.0 + 0.004, con_z - 0.001), (0.122, 0.018, 0.024), parent=p_enclosure, bevel=0.002)
    dock.data.materials.append(mat_seal)
    rim = make_box("screen_metal_rim", (cx_con, con_y, con_z), (0.124, 0.008, 0.031), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.003, bevel_segs=3)
    bez = make_box("screen_bezel", (cx_con, con_y + n_y * 0.0024, con_z + n_z * 0.0024), (0.118, 0.005, 0.026), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.002)
    bez.data.materials.append(mat_seal)
    disp = make_box("screen_display", (cx_con, con_y + n_y * 0.0046, con_z + n_z * 0.0046), (0.112, 0.002, 0.022), parent=p_enclosure, rot_euler=(con_ang, 0, 0))

    door_y = -D / 2.0 + 0.0035
    hinges = []
    for hname, hz in [("door_hinge_top", door_zc + door_h / 2.0 - 0.018), ("door_hinge_bot", door_zc - door_h / 2.0 + 0.018)]:
        hg = make_box(hname, (x_f_min + 0.003, door_y - 0.002, hz), (0.010, 0.007, 0.018), parent=p_enclosure, bevel=0.0015)
        hinges.append(hg)

    # 2. Slim Flush Door Frame & Contoured Handle (`door`)
    stile_w, rail_h = 0.0085, 0.0085
    stile_l = make_box("door_left_stile", (door_xc - door_w / 2.0 + stile_w / 2.0, door_y, door_zc), (stile_w, 0.006, door_h), parent=p_door, bevel=0.0008)
    stile_r = make_box("door_right_stile", (door_xc + door_w / 2.0 - stile_w / 2.0, door_y, door_zc), (stile_w, 0.006, door_h), parent=p_door, bevel=0.0008)
    rail_t = make_box("door_top_rail", (door_xc, door_y, door_zc + door_h / 2.0 - rail_h / 2.0), (door_w - 2 * stile_w, 0.006, rail_h), parent=p_door, bevel=0.0008)
    b_rail_bot = door_zc - door_h / 2.0
    rail_b = make_box("door_bottom_rail", (door_xc, door_y, b_rail_bot + rail_h / 2.0), (door_w - 2 * stile_w, 0.006, rail_h), parent=p_door, bevel=0.0008)
    arch_hood = make_trapezoid_arch("door_console_arch_hood", cx_con, 0.136, 0.112, door_y, 0.007, b_rail_bot + rail_h - 0.001, b_rail_bot + rail_h + 0.012, parent=p_door, bevel=0.0015)
    for df in (stile_l, stile_r, rail_t, rail_b, arch_hood):
        df.data.materials.append(mat_graphite)

    hx = door_xc + door_w / 2.0 - 0.002
    hz = -0.016
    hdl = make_box("door_ergo_handle", (hx, door_y - 0.0085, hz), (0.010, 0.010, 0.048), parent=p_door, bevel=0.0035, bevel_segs=3)
    hdl_mounts = []
    for mname, mz in [("door_handle_mount_top", hz + 0.014), ("door_handle_mount_bot", hz - 0.014)]:
        hdl_mounts.append(make_box(mname, (hx, door_y - 0.0045, mz), (0.007, 0.006, 0.006), parent=p_door, bevel=0.0015))

    # 3. CoreXY Gantry (`gantryX`) — Dual Chrome X Rods, Y Rails, Leadscrews & Crossbeam
    gz = 0.062
    gantry_dark_parts = [
        make_box("x_gantry_crossbeam", (0.0, -0.012, gz + 0.002), (0.326, 0.016, 0.020), parent=p_gantryX, bevel=0.002),
        make_box("x_belt_front", (0.0, -0.022, gz + 0.002), (0.320, 0.003, 0.006), parent=p_gantryX),
        make_box("x_belt_rear", (0.0, 0.002, gz + 0.002), (0.320, 0.003, 0.006), parent=p_gantryX),
        make_box("x_slider_left", (-0.162, -0.010, gz), (0.024, 0.068, 0.036), parent=p_gantryX, bevel=0.0025),
        make_box("x_slider_right", (0.162, -0.010, gz), (0.024, 0.068, 0.036), parent=p_gantryX, bevel=0.0025),
        make_box("stepper_left", (-0.156, 0.088, gz - 0.012), (0.036, 0.036, 0.036), parent=p_gantryX, bevel=0.002),
        make_box("stepper_right", (0.156, 0.088, gz - 0.012), (0.036, 0.036, 0.036), parent=p_gantryX, bevel=0.002),
    ]
    gantry_frame = join_objects(gantry_dark_parts, "x_gantry_crossbeam", p_gantryX)
    alloy_interior.append(gantry_frame)

    steel_parts = []
    for rname, rloc, rad, length, ax in [
        ("x_guide_front", (0.0, -0.028, gz + 0.002), 0.0068, 0.330, "x"),
        ("x_guide_rear",  (0.0, -0.026, gz - 0.011), 0.0060, 0.330, "x"),
        ("x_guide_top",   (0.0, -0.018, gz + 0.015), 0.0058, 0.330, "x"),
        ("y_guide_left",  (-0.164, 0.0, gz + 0.015), 0.0058, 0.198, "y"),
        ("y_guide_right", ( 0.164, 0.0, gz + 0.015), 0.0058, 0.198, "y"),
        ("z_lead_left",   (-0.148, -0.036, -0.014),  0.0056, 0.272, "z"),
        ("z_guide_left",  (-0.148,  0.032, -0.014),  0.0058, 0.272, "z"),
        ("z_lead_right",  ( 0.148,  0.000, -0.014),  0.0056, 0.272, "z"),
        ("z_lead_rear",   ( 0.000,  0.090, -0.014),  0.0058, 0.272, "z"),
    ]:
        steel_parts.append(make_cylinder(rname, rloc, rad, length, ax, segs=24, parent=p_gantryX))
    for mx in (-0.154, 0.154):
        steel_parts.append(make_cylinder(f"pulley_{mx}", (mx, -0.082, gz + 0.006), 0.009, 0.014, "z", segs=20, parent=p_gantryX, bevel=0.001))
    # Turned bearing collars on Z guides
    for cx, cy, cz in [(-0.148, -0.036, -0.082), (-0.148, 0.032, -0.082), (0.148, 0.0, -0.082)]:
        steel_parts.append(make_cylinder(f"z_collar_{cx:.2f}_{cy:.2f}", (cx, cy, cz), 0.0095, 0.010, "z", segs=20, parent=p_gantryX, bevel=0.0012))
    steel_rails = join_objects(steel_parts, "x_guide_front", p_gantryX)

    dc_links = []
    for seg_i in range(14):
        t = seg_i / 13.0
        dx = 0.026 + t * 0.128
        dy = 0.014 + 0.062 * math.sin(t * math.pi * 0.65)
        dz = gz + 0.026 + 0.010 * math.sin(t * math.pi)
        dc_links.append(make_box(f"drag_chain_{seg_i}", (dx, dy, dz), (0.011, 0.014, 0.009), parent=p_gantryX, rot_euler=(0, 0, -t * 0.85), bevel=0.0015))
    drag_chain_mesh = join_objects(dc_links, "drag_chain_assembly", p_gantryX)
    alloy_interior.append(drag_chain_mesh)

    # 4. Precision Multi-Part CNC Toolhead (`printHead`)
    th_x, th_z = 0.026, gz - 0.002
    th_body = make_box("toolhead_chassis", (th_x, -0.004, th_z), (0.048, 0.038, 0.054), parent=p_printHead, bevel=0.003)

    # Sculpted copper-bronze CNC outer cowl with cooling fan aperture & outer chamfered lip
    th_cowl = make_box("toolhead_front_cowl", (th_x, -0.027, th_z + 0.002), (0.050, 0.013, 0.052), parent=p_printHead, bevel=0.0055, bevel_segs=3)
    cut_fan = make_cylinder("cut_fan_bore", (th_x, -0.031, th_z + 0.002), 0.0135, 0.016, "y", segs=28)
    boolean_cut(th_cowl, cut_fan)
    # Recessed metallic intake trim ring around fan bore + top CNC bridge lip
    fan_bezel = make_cylinder("toolhead_fan_bezel", (th_x, -0.0335, th_z + 0.002), 0.0152, 0.0025, "y", segs=28)
    cut_fb_in = make_cylinder("cut_fb_in", (th_x, -0.0335, th_z + 0.002), 0.0132, 0.006, "y", segs=28)
    boolean_cut(fan_bezel, cut_fb_in)
    cowl_hood = make_box("toolhead_top_hood", (th_x, -0.016, th_z + 0.027), (0.052, 0.024, 0.008), parent=p_printHead, bevel=0.0025)
    cowl_collet = make_cylinder("ptfe_pneumatic_collet", (th_x, -0.004, th_z + 0.031), 0.0065, 0.009, "z", segs=18, parent=p_printHead, bevel=0.001)
    toolhead_copper = join_objects([th_cowl, fan_bezel, cowl_hood, cowl_collet], "toolhead_front_cowl", p_printHead)

    fan_parts = [make_cylinder("toolhead_fan_hub", (th_x, -0.026, th_z + 0.002), 0.0055, 0.005, "y", segs=20, parent=p_printHead)]
    for b_i in range(7):
        ang = (2.0 * math.pi * b_i) / 7.0
        fan_parts.append(make_box(
            f"toolhead_fan_blade_{b_i}",
            (th_x + 0.009 * math.cos(ang), -0.026, th_z + 0.002 + 0.009 * math.sin(ang)),
            (0.0068, 0.0025, 0.0025), parent=p_printHead, rot_euler=(0.35, ang, 0), bevel=0.0005
        ))
    fan_rotor_mesh = join_objects(fan_parts, "toolhead_fan_rotor", p_printHead)

    # Stacked heatsink fins + heater block + brass nozzle
    heatsink_parts = [make_box("toolhead_hotend_sock", (th_x, -0.004, th_z - 0.032), (0.018, 0.018, 0.011), parent=p_printHead, bevel=0.002)]
    for f_j in range(4):
        heatsink_parts.append(make_box(f"heatsink_fin_{f_j}", (th_x, -0.004, th_z - 0.018 - f_j * 0.0032), (0.022, 0.020, 0.0014), parent=p_printHead))
    hsock = join_objects(heatsink_parts, "toolhead_hotend_sock", p_printHead)
    alloy_interior.extend([th_body, fan_rotor_mesh, hsock])

    noz = make_cylinder("toolhead_nozzle", (th_x, -0.004, th_z - 0.041), 0.0034, 0.0085, "z", segs=18, parent=p_printHead)
    noz.data.materials.append(mat_brass)

    ptfe_pts = [(th_x + 0.008 * math.sin(i / 11.0 * math.pi), -0.004 + (i / 11.0) * 0.104,
                 (th_z + 0.031) + 0.030 * math.sin((i / 11.0) * math.pi * 0.72) + (i / 11.0) * 0.010)
                for i in range(12)]
    ptfe = make_curve_tube("ptfe_bowden_tube", ptfe_pts, 0.0042, parent=p_printHead)

    # 5. Dark Metallic PEI Print Bed & Machined Aluminum Carriage (`printBed`)
    bed_z = -0.086
    pei = make_box("build_plate", (0.0, 0.022, bed_z), (0.256, 0.140, 0.0045), parent=p_printBed, bevel=0.0012)
    pei_lip = make_box("build_plate_lip", (0.0, -0.050, bed_z), (0.080, 0.010, 0.0045), parent=p_printBed, bevel=0.001)
    bed_parts = [
        make_box("bed_heater_block", (0.0, 0.022, bed_z - 0.006), (0.250, 0.136, 0.008), parent=p_printBed, bevel=0.002),
        make_box("bed_carriage_arm_l", (-0.104, 0.022, bed_z - 0.014), (0.026, 0.124, 0.012), parent=p_printBed, bevel=0.002),
        make_box("bed_carriage_arm_r", ( 0.104, 0.022, bed_z - 0.014), (0.026, 0.124, 0.012), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_l",    (-0.148, 0.000, bed_z - 0.014), (0.024, 0.086, 0.014), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_r",    ( 0.148, 0.000, bed_z - 0.014), (0.024, 0.030, 0.014), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_rear", (0.0,    0.090, bed_z - 0.014), (0.046, 0.024, 0.014), parent=p_printBed, bevel=0.002),
    ]
    bed_carriage = join_objects(bed_parts, "bed_heater_block", p_printBed)
    alloy_interior.append(bed_carriage)

    # 6. Sculpted Metallic Turbine Arch Bracket (`printedObject`)
    # Swept aerospace manifold arch w/ dual outer ribs, top boss ring, side gussets & 27 tapered fins
    obj_z = bed_z + 0.0025
    flange = make_box("bracket_base_raft", (0.0, 0.018, obj_z + 0.0015), (0.186, 0.058, 0.003), parent=p_printedObject, bevel=0.0012)

    bm = bmesh.new()
    xs = np.linspace(-0.090, 0.090, 17)
    rings = []
    for x in xs:
        t_abs = abs(x) / 0.090
        z_pk = obj_z + 0.004 + 0.052 * math.exp(-2.5 * (t_abs ** 1.72))
        z_bt = obj_z + 0.004 + 0.030 * max(0.0, 1.0 - (t_abs / 0.85) ** 2)
        if t_abs > 0.85:
            z_bt = obj_z + 0.002
        hy = 0.028 - 0.006 * (1.0 - t_abs)
        pts = [
            (x, 0.018 - hy, z_bt),
            (x, 0.018 - hy * 0.86, z_bt + 0.35 * (z_pk - z_bt)),
            (x, 0.018 - hy * 0.56, z_pk),
            (x, 0.018 + hy * 0.56, z_pk),
            (x, 0.018 + hy * 0.86, z_bt + 0.35 * (z_pk - z_bt)),
            (x, 0.018 + hy, z_bt),
        ]
        rings.append([bm.verts.new(p) for p in pts])
    for i in range(len(rings) - 1):
        r0, r1 = rings[i], rings[i + 1]
        for s in range(6):
            ns = (s + 1) % 6
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

    # Center sculpted duct ring + recessed turbine hub + outer stepped collar flange + forward rib gusset
    boss_outer = make_cylinder("bracket_apex_ring", (0.0, 0.018, obj_z + 0.047), 0.0125, 0.044, "y", segs=28, parent=p_printedObject, bevel=0.0015)
    cut_boss_bore = make_cylinder("cut_boss_bore", (0.0, 0.018, obj_z + 0.047), 0.0068, 0.052, "y", segs=24)
    boolean_cut(boss_outer, cut_boss_bore)
    boss_hub = make_cylinder("bracket_turbine_hub", (0.0, 0.018 + 0.002, obj_z + 0.047), 0.0066, 0.032, "y", segs=22, parent=p_printedObject, bevel=0.0012)
    boss_pin = make_cylinder("bracket_turbine_shaft", (0.0, 0.018 - 0.001, obj_z + 0.047), 0.0032, 0.040, "y", segs=18, parent=p_printedObject, bevel=0.0008)
    boss_rim = make_box("bracket_crest_spine", (0.0, 0.018 - 0.015, obj_z + 0.042), (0.062, 0.005, 0.006), parent=p_printedObject, bevel=0.0015)
    boss = join_objects([boss_outer, boss_hub, boss_pin, boss_rim], "bracket_apex_ring", p_printedObject)

    fin_parts = []
    for f_i in range(27):
        fx = -0.078 + f_i * 0.0060
        t_f = abs(fx) / 0.084
        fh = 0.036 * max(0.22, 1.0 - t_f * 0.78)
        fin_parts.append(make_box(f"support_fin_{f_i}", (fx, 0.018, obj_z + 0.003 + fh / 2.0), (0.0016, 0.034, fh), parent=p_printedObject, bevel=0.0004))
    fins_mesh = join_objects(fin_parts, "bracket_support_fins", p_printedObject)

    # 7. Smoked Glass & Diagonal Studio Skylight Sheen
    fg_door = make_box("front_glass_door", (door_xc, door_y, door_zc), (door_w - 2 * stile_w, 0.004, door_h - 2 * rail_h), parent=p_door)
    tg_roof = make_asym_rounded_prism(
        "top_roof_glass", 0.314, 0.182, Z_top - 0.026, Z_top - 0.022, 0.008, 0.008,
        seg=10, parent=p_enclosure, top_drop_x=0.015, top_drop_y=0.015, left_shoulder_drop=0.003
    )
    lw_glass = make_box("left_glass_window", (-W / 2.0 + 0.010, 0.5 * (y_l_min + y_l_max), win_zc), (0.004, y_l_max - y_l_min - 0.020, win_h - 0.020), parent=p_enclosure)
    rw_glass = make_box("right_glass_window", (W / 2.0 - 0.010, 0.5 * (y_r_min + y_r_max), win_zc), (0.004, y_r_max - y_r_min - 0.020, win_h - 0.020), parent=p_enclosure)

    sheen_f = make_box("front_glass_sheen", (door_xc, door_y - 0.0026, door_zc), (door_w - 2 * stile_w - 0.004, 0.0005, door_h - 2 * rail_h - 0.004), parent=p_door)
    sheen_r = make_box("right_glass_sheen", (W / 2.0 - 0.0072, 0.5 * (y_r_min + y_r_max), win_zc), (0.0005, y_r_max - y_r_min - 0.022, win_h - 0.022), parent=p_enclosure)

    return {
        "shell_objs": [shell, rear_ins],
        "ext_hw_objs": [rim, hdl, rear_fan_hub, ac_sw] + hinges + hdl_mounts + foot_objs,
        "alloy_objs": alloy_interior + [plinth],
        "steel_objs": [steel_rails],
        "copper_objs": [toolhead_copper],
        "arch_objs": [flange, arch_obj, boss, fins_mesh],
        "chamber_objs": [lin_rear, lin_ceil, lin_left],
        "floor_objs": [lin_floor],
        "led_objs": led_objs,
        "ptfe_objs": [ptfe],
        "plate_objs": [pei, pei_lip],
        "screen_objs": [disp],
        "glass_objs": [fg_door, tg_roof, lw_glass, rw_glass, sheen_f, sheen_r],
        "doors_glass": [fg_door, tg_roof, lw_glass, rw_glass],
        "sheen_glass": [sheen_f, sheen_r],
    }


# ---------------------------------------------------------------------
# Disjoint Atlas Packing, AO Bake & PBR Material Texture Synthesizer
# ---------------------------------------------------------------------
def assign_disjoint_uv_grid(objs, atlas_name, res=1024, pad=0.01):
    unique_objs, seen = [], set()
    for o in objs:
        if o and o.type == "MESH" and o.name not in seen and len(o.data.polygons) > 0:
            seen.add(o.name)
            unique_objs.append(o)

    n = len(unique_objs)
    cols = max(1, math.ceil(math.sqrt(n)))
    rows = max(1, math.ceil(n / cols))
    cw, ch = 1.0 / cols, 1.0 / rows

    for idx, obj in enumerate(unique_objs):
        me = obj.data
        while me.uv_layers:
            me.uv_layers.remove(me.uv_layers[0])
        uvl = me.uv_layers.new(name="UVMap")
        me.uv_layers.active = uvl

        col, row = idx % cols, idx // cols
        tu0 = col * cw + pad * cw
        tv0 = 1.0 - (row + 1) * ch + pad * ch
        tw, th = cw * (1.0 - 2.0 * pad), ch * (1.0 - 2.0 * pad)

        set_active(obj)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.03)
        bpy.ops.object.mode_set(mode="OBJECT")

        uv_arr = me.uv_layers.active.data
        us = [uv_arr[i].uv.x for i in range(len(uv_arr))]
        vs = [uv_arr[i].uv.y for i in range(len(uv_arr))]
        if us and (max(us) - min(us) > 1e-5) and (max(vs) - min(vs) > 1e-5):
            u0, u1 = min(us), max(us)
            v0, v1 = min(vs), max(vs)
            du, dv = u1 - u0, v1 - v0
            for i in range(len(uv_arr)):
                uv_arr[i].uv.x = tu0 + ((uv_arr[i].uv.x - u0) / du) * tw
                uv_arr[i].uv.y = tv0 + ((uv_arr[i].uv.y - v0) / dv) * th
        else:
            verts = me.vertices
            xs = [verts[i].co.x for i in range(len(verts))]
            ys = [verts[i].co.y for i in range(len(verts))]
            zs = [verts[i].co.z for i in range(len(verts))]
            x0, dx = min(xs), max(1e-5, max(xs) - min(xs))
            y0, dy = min(ys), max(1e-5, max(ys) - min(ys))
            z0, dz = min(zs), max(1e-5, max(zs) - min(zs))
            sub_w, sub_h = tw / 3.0, th / 2.0
            spad = 0.06
            for poly in me.polygons:
                n_v = poly.normal
                ax, ay, az_n = abs(n_v.x), abs(n_v.y), abs(n_v.z)
                slot, mode = ((0 if n_v.x >= 0.0 else 1), 0) if (ax >= ay and ax >= az_n) else (
                    ((2 if n_v.y >= 0.0 else 3), 1) if (ay >= ax and ay >= az_n) else ((4 if n_v.z >= 0.0 else 5), 2)
                )
                sc, sr = slot % 3, slot // 3
                su0 = tu0 + sc * sub_w + spad * sub_w
                sv0 = tv0 + sr * sub_h + spad * sub_h
                sw, sh = sub_w * (1.0 - 2.0 * spad), sub_h * (1.0 - 2.0 * spad)
                for li in poly.loop_indices:
                    vco = verts[me.loops[li].vertex_index].co
                    uu, vv = ((vco.y - y0) / dy, (vco.z - z0) / dz) if mode == 0 else (
                        ((vco.x - x0) / dx, (vco.z - z0) / dz) if mode == 1 else ((vco.x - x0) / dx, (vco.y - y0) / dy)
                    )
                    uv_arr[li].uv = (su0 + uu * sw, sv0 + vv * sh)
        me.update()

    ao_img = bpy.data.images.new(atlas_name + "_AO", width=res, height=res, alpha=False)
    ao_img.colorspace_settings.name = "Non-Color"
    return unique_objs, ao_img


def bake_ao_cycles(scene, objs, ao_img, samples=12):
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 3
    scene.cycles.bake_type = "AO"
    scene.render.bake.margin = 6
    scene.render.bake.use_selected_to_active = False

    ao_mat = bpy.data.materials.new("Temp_AO_" + ao_img.name)
    ao_mat.use_nodes = True
    nt = ao_mat.node_tree
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = ao_img
    for n in nt.nodes:
        n.select = False
    tex_node.select = True
    nt.nodes.active = tex_node

    orig_mats = {}
    for obj in objs:
        orig_mats[obj.name] = list(obj.data.materials)
        obj.data.materials.clear()
        obj.data.materials.append(ao_mat)

    print(f"Baking AO {ao_img.name} ({len(objs)} objects)...", flush=True)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    scene.render.bake.use_clear = True
    bpy.ops.object.bake(type="AO")

    res = ao_img.size[0]
    arr = np.array(ao_img.pixels[:], dtype=np.float32).reshape(res, res, 4)[..., :3].mean(axis=2)
    for obj in objs:
        obj.data.materials.clear()
        for m in orig_mats[obj.name]:
            obj.data.materials.append(m)
    return arr


def rasterize_pbr_maps(objs, ao_arr, res, shader_fn):
    """Rasterize object world coords/normals to `(base_lin, rough_val, emit_lin)` maps."""
    pos_buf = np.zeros((res, res, 3), dtype=np.float32)
    norm_buf = np.zeros((res, res, 3), dtype=np.float32)
    mask_buf = np.zeros((res, res), dtype=bool)
    obj_id_buf = np.full((res, res), -1, dtype=np.int32)

    for obj_id, obj in enumerate(objs):
        me = obj.data
        uv_layer = me.uv_layers.active.data
        mw = np.array(obj.matrix_world, dtype=np.float32)
        rot = mw[:3, :3]
        verts = np.array([v.co for v in me.vertices], dtype=np.float32)
        wverts = verts @ rot.T + mw[:3, 3]

        me.calc_loop_triangles()
        for tri in me.loop_triangles:
            loops = tri.loops
            uvs = np.array([[uv_layer[l].uv.x, uv_layer[l].uv.y] for l in loops], dtype=np.float32)
            pxs = uvs[:, 0] * res
            pys = uvs[:, 1] * res

            x0 = max(0, int(math.floor(pxs.min())) - 1)
            x1 = min(res - 1, int(math.ceil(pxs.max())) + 1)
            y0 = max(0, int(math.floor(pys.min())) - 1)
            y1 = min(res - 1, int(math.ceil(pys.max())) + 1)
            if x1 < x0 or y1 < y0:
                continue

            tri_p = wverts[tri.vertices]
            fn = np.array(tri.normal, dtype=np.float32) @ rot.T
            fn_len = np.linalg.norm(fn)
            if fn_len > 1e-8:
                fn /= fn_len
            vns = np.array([me.vertices[vi].normal for vi in tri.vertices], dtype=np.float32) @ rot.T
            if not tri.use_smooth:
                vns = np.repeat(fn[None, :], 3, axis=0)

            xs = np.arange(x0, x1 + 1, dtype=np.float32) + 0.5
            ys = np.arange(y0, y1 + 1, dtype=np.float32) + 0.5
            gx, gy = np.meshgrid(xs, ys)

            denom = (pys[1] - pys[2]) * (pxs[0] - pxs[2]) + (pxs[2] - pxs[1]) * (pys[0] - pys[2])
            if abs(denom) < 1e-9:
                continue
            w0 = ((pys[1] - pys[2]) * (gx - pxs[2]) + (pxs[2] - pxs[1]) * (gy - pys[2])) / denom
            w1 = ((pys[2] - pys[0]) * (gx - pxs[2]) + (pxs[0] - pxs[2]) * (gy - pys[2])) / denom
            w2 = 1.0 - w0 - w1
            inside = (w0 >= -0.02) & (w1 >= -0.02) & (w2 >= -0.02)
            if not np.any(inside):
                continue

            p_interp = w0[inside, None] * tri_p[0] + w1[inside, None] * tri_p[1] + w2[inside, None] * tri_p[2]
            n_interp = w0[inside, None] * vns[0] + w1[inside, None] * vns[1] + w2[inside, None] * vns[2]
            n_len = np.linalg.norm(n_interp, axis=1, keepdims=True)
            n_interp = np.where(n_len > 1e-6, n_interp / np.maximum(n_len, 1e-6), fn)

            iy, ix = np.where(inside)
            pos_buf[y0 + iy, x0 + ix] = p_interp
            norm_buf[y0 + iy, x0 + ix] = n_interp
            mask_buf[y0 + iy, x0 + ix] = True
            obj_id_buf[y0 + iy, x0 + ix] = obj_id

    base_map = np.zeros((res, res, 3), dtype=np.float32)
    rough_map = np.full((res, res), 0.35, dtype=np.float32)
    emit_map = np.zeros((res, res, 3), dtype=np.float32)

    b_vals, r_vals, e_vals = shader_fn(pos_buf[mask_buf], norm_buf[mask_buf], ao_arr[mask_buf], obj_id_buf[mask_buf], objs)
    base_map[mask_buf] = b_vals
    rough_map[mask_buf] = r_vals
    emit_map[mask_buf] = e_vals

    # Dilate all 3 channels consistently by 5 pixels cleanly
    cur_m = mask_buf.copy()
    for _ in range(5):
        acc_b, acc_e = np.zeros_like(base_map), np.zeros_like(emit_map)
        acc_r = np.zeros((res, res), dtype=np.float32)
        cnt = np.zeros((res, res), dtype=np.float32)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            sm = np.roll(np.roll(cur_m, dy, axis=0), dx, axis=1)
            acc_b += np.roll(np.roll(base_map, dy, axis=0), dx, axis=1) * sm[..., None]
            acc_e += np.roll(np.roll(emit_map, dy, axis=0), dx, axis=1) * sm[..., None]
            acc_r += np.roll(np.roll(rough_map, dy, axis=0), dx, axis=1) * sm
            cnt += sm
        nxt_m = (cnt > 0) & ~cur_m
        if not np.any(nxt_m):
            break
        base_map[nxt_m] = acc_b[nxt_m] / cnt[nxt_m, None]
        emit_map[nxt_m] = acc_e[nxt_m] / cnt[nxt_m, None]
        rough_map[nxt_m] = acc_r[nxt_m] / cnt[nxt_m]
        cur_m |= nxt_m

    return base_map, rough_map, emit_map


def save_png_img(arr_rgb_float, name, is_srgb=True):
    h, w = arr_rgb_float.shape[:2]
    rgba = np.ones((h, w, 4), dtype=np.float32)
    if arr_rgb_float.ndim == 2:
        rgba[..., 0] = rgba[..., 1] = rgba[..., 2] = np.clip(arr_rgb_float, 0.0, 1.0)
    else:
        rgba[..., :3] = linear_to_srgb_float(arr_rgb_float) if is_srgb else np.clip(arr_rgb_float, 0.0, 1.0)
    tmp = bpy.data.images.new(name + "_TMP", width=w, height=h, alpha=False)
    tmp.pixels.foreach_set(rgba.ravel())
    p = BAKE_DIR / f"{name}.png"
    tmp.filepath_raw = str(p)
    tmp.file_format = "PNG"
    tmp.save()
    bpy.data.images.remove(tmp)
    img = bpy.data.images.load(str(p), check_existing=True)
    if not is_srgb:
        img.colorspace_settings.name = "Non-Color"
    return img


def build_pbr_material(objs, out_name, base_lin, rough_arr, emit_lin, metallic=0.65, emissive_scale=1.0, spec=0.5):
    base_img = save_png_img(base_lin, f"{out_name}_Base", is_srgb=True)
    rough_img = save_png_img(rough_arr, f"{out_name}_Rough", is_srgb=False)

    mat = bpy.data.materials.new(out_name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")

    tb = nt.nodes.new("ShaderNodeTexImage")
    tb.image = base_img
    nt.links.new(tb.outputs["Color"], bsdf.inputs["Base Color"])

    tr = nt.nodes.new("ShaderNodeTexImage")
    tr.image = rough_img
    nt.links.new(tr.outputs["Color"], bsdf.inputs["Roughness"])

    bsdf.inputs["Metallic"].default_value = metallic
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = spec

    if emissive_scale > 0.0 and float(emit_lin.max()) > 1e-4:
        emit_img = save_png_img(emit_lin / max(1e-4, emissive_scale), f"{out_name}_Emit", is_srgb=True)
        te = nt.nodes.new("ShaderNodeTexImage")
        te.image = emit_img
        nt.links.new(te.outputs["Color"], bsdf.inputs["Emission Color"])
        bsdf.inputs["Emission Strength"].default_value = emissive_scale

    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    for obj in objs:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    return mat


# ---------------------------------------------------------------------
# Distinct Physically Based Material Shaders
# ---------------------------------------------------------------------
def eval_shell_pbr(pos, norm, ao, obj_id, objs):
    """
    Brushed champagne-titanium satin unibody shell (`metallic=0.42`):
    Combines real directional PBR response (`baseColorTexture` + brushed `roughnessMap`)
    with soft balanced ambient studio fill (`emissive ~ 0.65`) matching Forehead/Pillar/Flank/Chin.
    """
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]

    tx = np.clip((x + 0.175) / 0.330, 0.0, 1.0)
    forehead_srgb = np.stack([
        70.0 + 174.0 * ((1.0 - tx) ** 0.92),
        62.0 + 180.0 * ((1.0 - tx) ** 0.94),
        52.0 + 184.0 * ((1.0 - tx) ** 0.96),
    ], axis=1)

    left_stile = np.clip((-0.184 - x) / 0.018, 0.0, 1.0) * np.clip(-ny, 0.0, 1.0)
    left_stile_col = np.array([204.0, 200.0, 192.0], dtype=np.float32) * (0.86 + 0.14 * np.clip((z + 0.19) / 0.36, 0.0, 1.0))[:, None]

    tz_front = np.clip((z + 0.19) / 0.36, 0.0, 1.0)
    chin_srgb = np.array([106.0, 95.0, 80.0], dtype=np.float32)[None, :] * (0.96 + 0.08 * (1.0 - tx[:, None]))
    front_srgb = chin_srgb + (forehead_srgb - chin_srgb) * (tz_front[:, None] ** 1.15)
    front_srgb = front_srgb * (1.0 - left_stile[:, None]) + left_stile_col * left_stile[:, None]

    az = np.degrees(np.arctan2(np.maximum(0.0, nx), np.maximum(1e-5, -ny)))
    crest_z = np.clip((0.156 - z) / 0.024, 0.0, 1.0)
    foot_flare = np.clip((-0.140 - z) / 0.052, 0.0, 1.0)
    az_kn = np.array([0.0, 5.0, 12.0, 22.0, 40.0, 60.0, 76.0, 90.0], dtype=np.float32)
    p_base = np.stack([
        np.interp(az, az_kn, [58.0,  60.0,  52.0, 44.0, 40.0, 32.0, 48.0, 52.0]),
        np.interp(az, az_kn, [48.0,  50.0,  42.0, 34.0, 31.0, 24.0, 39.0, 42.0]),
        np.interp(az, az_kn, [38.0,  40.0,  32.0, 26.0, 23.0, 16.0, 28.0, 32.0]),
    ], axis=1).astype(np.float32)
    p_hi = np.stack([
        np.interp(az, az_kn, [128.0, 136.0, 88.0, 46.0, 42.0, 34.0, 48.0, 52.0]),
        np.interp(az, az_kn, [119.0, 126.0, 79.0, 37.0, 33.0, 25.0, 39.0, 42.0]),
        np.interp(az, az_kn, [108.0, 114.0, 68.0, 28.0, 24.0, 17.0, 28.0, 32.0]),
    ], axis=1).astype(np.float32)
    pillar_srgb = p_base * (1.0 - crest_z[:, None]) + p_hi * crest_z[:, None]
    heel_boost = foot_flare[:, None] * np.clip(1.0 - az[:, None] / 52.0, 0.0, 1.0)
    pillar_srgb = pillar_srgb + heel_boost * np.array([30.0, 24.0, 15.0], dtype=np.float32)
    w_pillar = np.clip((x - 0.148) / 0.018, 0.0, 1.0) * np.clip(-ny * 3.0 + np.maximum(0.0, nx), 0.0, 1.0)

    flank_y = np.clip((y + 0.10) / 0.22, 0.0, 1.0)
    flank_low = np.clip((-0.095 - z) / 0.044, 0.0, 1.0)
    flank_lift = flank_low * (0.86 + 0.14 * flank_y)
    flank_srgb = np.stack([48.0 + 68.0 * flank_lift, 40.0 + 57.0 * flank_lift, 30.0 + 42.0 * flank_lift], axis=1)
    w_flank = np.clip((nx - 0.72) / 0.20, 0.0, 1.0) * np.clip((x - 0.17) / 0.03, 0.0, 1.0)

    top_srgb = forehead_srgb * 0.90
    w_top = np.clip((nz - 0.50) / 0.35, 0.0, 1.0)

    w_left_rear = np.clip(np.maximum((-nx - 0.50) / 0.35, (ny - 0.50) / 0.35), 0.0, 1.0)
    left_rear_srgb = np.array([166.0, 158.0, 146.0], dtype=np.float32)[None, :] * (0.85 + 0.20 * tz_front[:, None])

    srgb = front_srgb * (1.0 - w_pillar[:, None]) + pillar_srgb * w_pillar[:, None]
    srgb = srgb * (1.0 - w_flank[:, None]) + flank_srgb * w_flank[:, None]
    srgb = srgb * (1.0 - w_top[:, None]) + top_srgb * w_top[:, None]
    srgb = srgb * (1.0 - w_left_rear[:, None]) + left_rear_srgb * w_left_rear[:, None]

    grain = 1.0 + 0.006 * np.sin(z * 680.0 + x * 45.0)
    ao_factor = np.clip(0.90 + 0.10 * ao, 0.80, 1.02)
    target_lin = srgb_target_to_linear_aces(np.clip(srgb * grain[:, None] * ao_factor[:, None], 4.0, 246.0))

    # Split target energy for metallic=0.34: responsive directional PBR specular + accurate satin studio bounce
    base_lin = np.clip(target_lin * 0.44, 0.01, 0.90)
    pillar_mask = crest_z[:, None] * w_pillar[:, None]
    emit_lin = np.clip(target_lin * (0.78 + 0.14 * pillar_mask), 0.002, 1.60)
    rough = np.clip(0.29 + 0.04 * np.sin(z * 680.0) - 0.06 * crest_z, 0.18, 0.42)
    return base_lin, rough, emit_lin


def eval_hw_pbr(pos, norm, ao, obj_id, objs):
    """Dark satin bronze/titanium console rim, door hinges, contoured handle & integrated feet tabs (`metallic=0.65`)."""
    names = np.array([objs[i].name for i in obj_id])
    is_foot = np.array(["foot" in n or "rear_ac" in n or "rear_exhaust" in n for n in names])
    is_handle = np.array(["handle" in n for n in names])
    is_hinge = np.array(["hinge" in n for n in names])
    ny, nz = norm[:, 1], norm[:, 2]
    bevel_glint = np.clip(nz * 0.7 - ny * 0.4, 0.0, 1.0) ** 1.6

    base_col = np.repeat(np.array([[0.12, 0.10, 0.08]], dtype=np.float32), len(pos), axis=0)
    rough = np.full(len(pos), 0.26, dtype=np.float32)
    emit_col = np.array([[0.025, 0.020, 0.015]], dtype=np.float32) + bevel_glint[:, None] * np.array([[0.08, 0.065, 0.05]], dtype=np.float32)

    base_col[is_handle] = np.array([0.065, 0.052, 0.040], dtype=np.float32)
    rough[is_handle] = 0.24
    emit_col[is_handle] = np.array([0.014, 0.011, 0.008], dtype=np.float32) + bevel_glint[is_handle, None] * np.array([[0.045, 0.035, 0.026]], dtype=np.float32)

    base_col[is_hinge] = np.array([0.34, 0.29, 0.23], dtype=np.float32)
    rough[is_hinge] = 0.26

    z = pos[:, 2]
    is_rubber = is_foot & (z < -0.198)
    base_col[is_foot & ~is_rubber] = np.array([0.28, 0.24, 0.19], dtype=np.float32)
    base_col[is_rubber] = np.array([0.020, 0.020, 0.022], dtype=np.float32)
    emit_col[is_foot] = np.array([0.008, 0.006, 0.005], dtype=np.float32)
    rough[is_rubber] = 0.72

    ao_f = np.clip(0.84 + 0.16 * ao, 0.65, 1.02)
    return base_col * ao_f[:, None], rough, emit_col * ao_f[:, None]


def eval_steel_pbr(pos, norm, ao, obj_id, objs):
    """
    High-contrast machined steel hardware:
    - Horizontal X/Y chrome guide rods: dark bronze core + razor-sharp mirror-chrome ribbon + warm underside bounce
    - Vertical Z leadscrews/guides: dark bronze steel shafts with thin vertical specular rim glints (never flat gray bars!)
    """
    z = pos[:, 2]
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]
    is_vert = (np.abs(nz) < 0.26) & (z < 0.050)

    lathe = 0.90 + 0.10 * np.sin((pos[:, 0] + pos[:, 2]) * 1400.0)
    base_col = np.repeat(np.array([[0.24, 0.19, 0.16]], dtype=np.float32), len(pos), axis=0) * lathe[:, None]
    base_col[is_vert] = np.array([0.038, 0.028, 0.021], dtype=np.float32) * lathe[is_vert, None]
    rough = np.clip(0.10 + 0.04 * (1.0 - lathe), 0.08, 0.18)

    # Sharp cylindrical top-front specular reflection ribbon on horizontal X/Y rails
    theta = np.clip(-ny * 0.64 + nz * 0.76, -1.0, 1.0)
    chrome_streak = np.exp(-((theta - 0.76) / 0.34) ** 2)
    warm_bounce = np.clip(-nz * 0.65 - ny * 0.45, 0.0, 1.0) ** 2.2
    emit_col = (
        np.array([[0.030, 0.022, 0.016]], dtype=np.float32)
        + chrome_streak[:, None] * np.array([[4.20, 3.45, 2.95]], dtype=np.float32)
        + warm_bounce[:, None] * np.array([[0.42, 0.24, 0.12]], dtype=np.float32)
    )

    # Thin crisp metallic side glint on vertical Z leadscrews (deep dark core!)
    z_glint = np.exp(-((-ny * 0.72 + nx * 0.45 - 0.72) / 0.16) ** 2)
    screw_thread = 0.72 + 0.28 * np.sin(z * 1600.0)
    emit_col[is_vert] = (
        np.array([[0.018, 0.013, 0.009]], dtype=np.float32)
        + z_glint[is_vert, None] * np.array([[0.72, 0.50, 0.34]], dtype=np.float32)
    ) * screw_thread[is_vert, None]

    ao_f = np.clip(0.82 + 0.18 * ao, 0.60, 1.04)
    return base_col * ao_f[:, None], rough, emit_col * ao_f[:, None]


def eval_copper_pbr(pos, norm, ao, obj_id, objs):
    """Dark burnished bronze-copper CNC toolhead core w/ razor-sharp bright copper-gold chamfers (`metallic=0.84`)."""
    x, z = pos[:, 0], pos[:, 2]
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]
    rim = np.clip(nz * 0.68 - ny * 0.55 - nx * 0.25, 0.0, 1.0) ** 1.4
    bevel_lip = np.clip((np.abs(x - 0.026) - 0.018) / 0.006, 0.0, 1.0) + np.clip((np.abs(z - 0.062) - 0.018) / 0.006, 0.0, 1.0)
    highlight = np.clip(rim + 0.55 * bevel_lip * np.clip(-ny, 0.0, 1.0), 0.0, 1.25)

    base_col = np.repeat(np.array([[0.38, 0.19, 0.09]], dtype=np.float32), len(pos), axis=0)
    rough = np.clip(0.12 + 0.08 * (1.0 - ao), 0.09, 0.22)
    emit_col = np.array([[0.16, 0.08, 0.04]], dtype=np.float32) + highlight[:, None] * np.array([[2.05, 1.26, 0.68]], dtype=np.float32)
    ao_f = np.clip(0.75 + 0.25 * ao, 0.52, 1.04)
    return base_col * ao_f[:, None], rough, emit_col * ao_f[:, None]


def eval_alloy_pbr(pos, norm, ao, obj_id, objs):
    """Dark anodized aluminum extrusions & electronics w/ sharp upper chamfer catchlights (`metallic=0.62`)."""
    names = np.array([objs[i].name for i in obj_id])
    is_fan = np.array(["fan_rotor" in n or "plinth" in n or "heatsink" in n or "hotend" in n for n in names])
    is_beam = np.array(["crossbeam" in n or "bed_heater" in n for n in names])
    is_elec = np.array(["rear_electronics" in n or "right_lower" in n for n in names])

    base_col = np.repeat(np.array([[0.018, 0.014, 0.010]], dtype=np.float32), len(pos), axis=0)
    base_col[is_fan] = np.array([0.008, 0.006, 0.005], dtype=np.float32)
    base_col[is_beam] = np.array([0.032, 0.025, 0.019], dtype=np.float32)
    base_col[is_elec] = np.array([0.065, 0.038, 0.020], dtype=np.float32)

    rough = np.where(is_fan, 0.48, 0.22).astype(np.float32)
    ny, nz = norm[:, 1], norm[:, 2]
    edge = np.clip(nz * 0.65 - ny * 0.55, 0.0, 1.0) ** 2.6
    emit_col = np.where(
        is_fan[:, None],
        np.array([[0.004, 0.003, 0.002]], dtype=np.float32),
        np.array([[0.014, 0.010, 0.007]], dtype=np.float32) + edge[:, None] * np.array([[0.28, 0.19, 0.13]], dtype=np.float32),
    )
    # Crossbeam top metallic ridge catches warm steel reflection cleanly matching 13_Steel_Rail
    beam_ridge = np.clip(-ny * 0.72 + nz * 0.68, 0.0, 1.0) ** 1.6
    emit_col[is_beam] = (
        np.array([[0.030, 0.022, 0.016]], dtype=np.float32)
        + edge[is_beam, None] * np.array([[0.72, 0.54, 0.42]], dtype=np.float32)
        + beam_ridge[is_beam, None] * np.array([[2.65, 2.15, 1.80]], dtype=np.float32)
    )
    emit_col[is_elec] = np.array([0.115, 0.068, 0.036], dtype=np.float32) + edge[is_elec, None] * np.array([0.22, 0.13, 0.07], dtype=np.float32)

    ao_f = np.clip(0.75 + 0.25 * ao, 0.50, 1.04)
    return base_col * ao_f[:, None], rough, emit_col * ao_f[:, None]


def eval_arch_pbr(pos, norm, ao, obj_id, objs):
    """
    Sculpted dark-gunmetal aerospace turbine arch (`metallic=0.72, roughness=0.12`):
    Deep shadowed fin pockets & flanks paired with razor-sharp blazing champagne-chrome specular crest edges.
    """
    names = np.array([objs[i].name for i in obj_id])
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]
    is_fin = np.array(["support_fin" in n for n in names])
    is_raft = np.array(["base_raft" in n for n in names])

    layers = 0.92 + 0.08 * np.sin(pos[:, 2] * 3600.0)
    base_col = np.repeat(np.array([[0.045, 0.034, 0.024]], dtype=np.float32), len(pos), axis=0) * layers[:, None]
    base_col[is_fin] = np.array([0.022, 0.016, 0.011], dtype=np.float32)
    base_col[is_raft] = np.array([0.025, 0.018, 0.013], dtype=np.float32)

    rough = np.where(is_fin, 0.22, 0.12).astype(np.float32)
    crest = np.clip(nz * 0.68 - ny * 0.58 - nx * 0.18, 0.0, 1.0) ** 1.30
    sharp_glint = np.exp(-((np.clip(nz * 0.75 - ny * 0.65, 0.0, 1.0) - 0.85) / 0.15) ** 2)
    emit_col = (
        np.array([[0.14, 0.10, 0.07]], dtype=np.float32)
        + crest[:, None] * np.array([[3.60, 2.85, 2.15]], dtype=np.float32)
        + sharp_glint[:, None] * np.array([[0.85, 0.65, 0.48]], dtype=np.float32)
    )
    emit_col[is_fin] = (
        np.array([[0.024, 0.017, 0.011]], dtype=np.float32)
        + crest[is_fin, None] * np.array([[1.55, 1.15, 0.80]], dtype=np.float32)
    )
    emit_col[is_raft] = np.array([0.035, 0.025, 0.018], dtype=np.float32) + crest[is_raft, None] * np.array([0.35, 0.26, 0.18], dtype=np.float32)

    ao_f = np.clip(0.70 + 0.30 * ao, 0.45, 1.05)
    return base_col * ao_f[:, None], rough, emit_col * ao_f[:, None]


def eval_floor_matte(pos, norm, ao, obj_id, objs):
    """Matte dark chamber floor tray (`metallic=0.0, spec=0.0`) eliminating 82-deg grazing rearFill Fresnel glare."""
    base = np.repeat(np.array([[0.0, 0.0, 0.0]], dtype=np.float32), len(pos), axis=0)
    rough = np.full(len(pos), 1.0, dtype=np.float32)
    emit = np.repeat(srgb_target_to_linear_aces([42.0, 34.0, 24.0])[None, :], len(pos), axis=0) * np.clip(0.8 + 0.2 * ao, 0.6, 1.0)[:, None]
    return base, rough, emit


def eval_chamber_pbr(pos, norm, ao, obj_id, objs):
    """Warm upper-center amber studio wall glow fading sharply into deep espresso-black shadows below & left."""
    names = np.array([objs[i].name for i in obj_id])
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    warm_z = np.clip((z + 0.10) / 0.24, 0.0, 1.0)
    is_ceil = np.array(["ceiling" in n for n in names])
    is_left = np.array(["left_back" in n for n in names])

    upper_amber = np.array([76.0, 50.0, 31.0], dtype=np.float32)
    lower_amber = np.array([12.0, 9.0, 6.0], dtype=np.float32)
    wall_srgb = lower_amber[None, :] + (upper_amber - lower_amber)[None, :] * (warm_z[:, None] ** 1.45)
    halo = np.exp(-((x + 0.01) / 0.14) ** 2 - ((z - 0.05) / 0.07) ** 2)
    wall_srgb = wall_srgb + halo[:, None] * np.array([34.0, 22.0, 13.0], dtype=np.float32)

    target_lin = srgb_target_to_linear_aces(np.clip(wall_srgb, 4.0, 180.0))
    target_lin[is_ceil] = srgb_target_to_linear_aces([18.0, 14.0, 9.0])
    for i in np.where(is_left)[0]:
        target_lin[i] = srgb_target_to_linear_aces(np.clip(np.array([34.0, 25.0, 17.0]) * (0.45 + 0.55 * warm_z[i]), 4.0, 120.0))

    ao_f = np.clip(0.74 + 0.26 * ao, 0.48, 1.04)
    base_col = np.clip(target_lin * 0.16 * ao_f[:, None], 0.001, 0.10)
    emit_col = np.clip(target_lin * 0.88 * ao_f[:, None], 0.001, 0.40)
    rough = np.full(len(pos), 0.44, dtype=np.float32)
    return base_col, rough, emit_col


def eval_led_pbr(pos, norm, ao, obj_id, objs):
    base = np.repeat(np.array([[0.95, 0.85, 0.70]], dtype=np.float32), len(pos), axis=0)
    rough = np.full(len(pos), 0.20, dtype=np.float32)
    emit = np.repeat(np.array([[2.15, 1.48, 0.88]], dtype=np.float32), len(pos), axis=0)
    return base, rough, emit


def eval_ptfe_pbr(pos, norm, ao, obj_id, objs):
    """Semi-translucent matte-gloss milky PTFE Bowden tube."""
    base = np.repeat(np.array([[0.84, 0.80, 0.75]], dtype=np.float32), len(pos), axis=0)
    rough = np.full(len(pos), 0.28, dtype=np.float32)
    emit = np.repeat(np.array([[0.42, 0.39, 0.35]], dtype=np.float32), len(pos), axis=0) * np.clip(0.85 + 0.15 * ao, 0.7, 1.0)[:, None]
    return base, rough, emit


def eval_plate_pbr(pos, norm, ao, obj_id, objs):
    """Dark stippled graphite-gold textured PEI build plate (`baseColorTexture` keeps viewer GOLD_PEI intact)."""
    stipple = 0.88 + 0.12 * np.sin(pos[:, 0] * 1800.0) * np.cos(pos[:, 1] * 1800.0)
    ny = norm[:, 1]
    rim_glint = 0.75 + 0.35 * np.clip(-ny, 0.0, 1.0)
    base = np.repeat(np.array([[0.032, 0.026, 0.018]], dtype=np.float32), len(pos), axis=0) * stipple[:, None] * rim_glint[:, None]
    rough = np.clip(0.40 - 0.06 * stipple, 0.30, 0.50).astype(np.float32)
    emit = np.repeat(np.array([[0.008, 0.006, 0.004]], dtype=np.float32), len(pos), axis=0)
    ao_f = np.clip(0.84 + 0.16 * ao, 0.65, 1.02)
    return base * ao_f[:, None], rough, emit


def eval_screen_pbr(pos, norm, ao, obj_id, objs):
    """Dark glossy OLED touchscreen matching reference dark bronze-slate screen [55, 46, 35]."""
    x, z = pos[:, 0], pos[:, 2]
    cx, cz = -0.0195, -0.1513
    ui_pill = (np.abs(x - (cx - 0.025)) < 0.014) & (np.abs(z - cz) < 0.0014)
    base = np.repeat(np.array([[0.008, 0.006, 0.004]], dtype=np.float32), len(pos), axis=0)
    emit = np.repeat(srgb_target_to_linear_aces([44.0, 37.0, 27.0])[None, :], len(pos), axis=0)
    emit[ui_pill] = srgb_target_to_linear_aces([58.0, 50.0, 38.0])
    rough = np.full(len(pos), 0.14, dtype=np.float32)
    return base, rough, emit


def create_smoked_glass_export_mat():
    mat = bpy.data.materials.new("Smoked Glass")
    mat.use_nodes = True
    mat.use_backface_culling = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.071, 0.086, 0.102, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.38
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["Alpha"].default_value = 0.52
    return mat


def create_front_glass_sheen_mat():
    """Diagonal warm-silver studio softbox reflection across upper-left door pane, clear center/lower chamber."""
    w, h = 256, 256
    u = np.linspace(0.0, 1.0, w).reshape(1, w)
    v = np.linspace(0.0, 1.0, h).reshape(h, 1)

    diag = (v - 0.22) - 1.38 * (u - 0.05)
    wedge = 1.0 / (1.0 + np.exp(-diag * 14.0))
    fade = np.clip((v - 0.18) * 1.4, 0.0, 1.0) * np.clip((0.72 - u) * 1.5, 0.0, 1.0)
    refl_w = np.clip(wedge * fade, 0.0, 1.0)

    rim_glint = np.where((u < 0.010) | (v > 0.990), 1.0, 0.0)
    alpha = np.clip(np.maximum(0.02 + refl_w * 0.52, rim_glint * 0.28), 0.0, 0.56).astype(np.float32)

    s_low = np.array([108.0, 90.0, 74.0], dtype=np.float32)
    s_hi  = np.array([238.0, 210.0, 184.0], dtype=np.float32)
    em_s = 1.8
    lin_lo = srgb_target_to_linear_aces(s_low)
    lin_hi = srgb_target_to_linear_aces(s_hi)

    rgba = np.zeros((h, w, 4), dtype=np.float32)
    for ch in range(3):
        rgba[..., ch] = linear_to_srgb_float((lin_lo[ch] * (1.0 - refl_w) + lin_hi[ch] * refl_w) / em_s)
    rgba[..., 3] = alpha

    img = bpy.data.images.new("Front_Glass_Sheen_RGBA", width=w, height=h, alpha=True)
    img.pixels.foreach_set(rgba.ravel().tolist())
    p = BAKE_DIR / "Front_Glass_Sheen_RGBA.png"
    img.filepath_raw = str(p)
    img.file_format = "PNG"
    img.save()
    img = bpy.data.images.load(str(p), check_existing=True)

    mat = bpy.data.materials.new("Ref Glass Specular Sheen")
    mat.use_nodes = True
    mat.use_backface_culling = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 1.0
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.0
    bsdf.inputs["Emission Strength"].default_value = em_s
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def create_right_glass_sheen_mat():
    w, h = 128, 128
    v = np.linspace(0.0, 1.0, h).reshape(h, 1)
    u = np.linspace(0.0, 1.0, w).reshape(1, w)
    grad = np.clip(0.65 + 0.35 * v + 0.05 * u, 0.60, 1.0)
    lin = srgb_target_to_linear_aces([74.0, 50.0, 32.0])
    rgba = np.zeros((h, w, 4), dtype=np.float32)
    for ch in range(3):
        rgba[..., ch] = linear_to_srgb_float(lin[ch] * grad)
    rgba[..., 3] = 0.40

    img = bpy.data.images.new("Right_Glass_Sheen_RGBA", width=w, height=h, alpha=True)
    img.pixels.foreach_set(rgba.ravel().tolist())
    p = BAKE_DIR / "Right_Glass_Sheen_RGBA.png"
    img.filepath_raw = str(p)
    img.file_format = "PNG"
    img.save()
    img = bpy.data.images.load(str(p), check_existing=True)

    mat = bpy.data.materials.new("Right Glass Warm Sheen")
    mat.use_nodes = True
    mat.use_backface_culling = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 1.0
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.0
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.0
    bsdf.inputs["Emission Strength"].default_value = 1.0
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def bake_and_bind_group(scene, objs, group_name, res, shader_fn, metallic, emissive_scale, spec=0.5, samples=10):
    u_objs, ao_img = assign_disjoint_uv_grid(objs, group_name, res=res, pad=0.012)
    ao_arr = bake_ao_cycles(scene, u_objs, ao_img, samples=samples)
    base_lin, rough_arr, emit_lin = rasterize_pbr_maps(u_objs, ao_arr, res, shader_fn)
    build_pbr_material(u_objs, group_name, base_lin, rough_arr, emit_lin, metallic=metallic, emissive_scale=emissive_scale, spec=spec)


def main():
    scene = reset_scene()
    print("Building PBR high-contrast metal v13 geometry...", flush=True)
    groups = build_geometry()

    for g in groups["glass_objs"]:
        g.hide_render = True

    bake_and_bind_group(scene, groups["shell_objs"],   "Champagne Satin Shell",           1024, eval_shell_pbr,   metallic=0.34, emissive_scale=1.6, spec=0.45, samples=12)
    bake_and_bind_group(scene, groups["ext_hw_objs"],  "Exterior Metallic Hardware",       512, eval_hw_pbr,      metallic=0.65, emissive_scale=0.5, spec=0.65, samples=10)
    bake_and_bind_group(scene, groups["steel_objs"],   "Machined Steel Rails",             512, eval_steel_pbr,   metallic=0.88, emissive_scale=4.2, spec=0.95, samples=10)
    bake_and_bind_group(scene, groups["copper_objs"],  "Anodized Copper Toolhead",         512, eval_copper_pbr,  metallic=0.84, emissive_scale=3.0, spec=0.90, samples=10)
    bake_and_bind_group(scene, groups["alloy_objs"],   "Machined Dark Alloy",              512, eval_alloy_pbr,   metallic=0.62, emissive_scale=2.6, spec=0.65, samples=10)
    bake_and_bind_group(scene, groups["arch_objs"],    "Sculpted Metallic Turbine Arch",   512, eval_arch_pbr,    metallic=0.72, emissive_scale=3.8, spec=0.85, samples=12)
    bake_and_bind_group(scene, groups["chamber_objs"], "Warm Chamber Anodized Interior",   512, eval_chamber_pbr, metallic=0.22, emissive_scale=1.0, spec=0.10, samples=10)
    bake_and_bind_group(scene, groups["floor_objs"],   "Dark Matte Floor Tray",             256, eval_floor_matte, metallic=0.00, emissive_scale=1.0, spec=0.00, samples=6)
    bake_and_bind_group(scene, groups["led_objs"],     "Chamber LED Emitter Strip",        256, eval_led_pbr,     metallic=0.05, emissive_scale=2.4, spec=0.20, samples=6)
    bake_and_bind_group(scene, groups["ptfe_objs"],    "PTFE Bowden Tube",                 256, eval_ptfe_pbr,    metallic=0.05, emissive_scale=1.0, spec=0.40, samples=6)
    bake_and_bind_group(scene, groups["plate_objs"],   "Dark Graphite PEI Bed",            256, eval_plate_pbr,   metallic=0.58, emissive_scale=0.4, spec=0.55, samples=8)
    bake_and_bind_group(scene, groups["screen_objs"],  "Console OLED Glass",               256, eval_screen_pbr,  metallic=0.20, emissive_scale=0.6, spec=0.70, samples=6)

    for g in groups["glass_objs"]:
        g.hide_render = False

    mat_glass = create_smoked_glass_export_mat()
    mat_front_sheen = create_front_glass_sheen_mat()
    mat_right_sheen = create_right_glass_sheen_mat()

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
        uv_arr = sg.data.uv_layers.active.data
        for face in sg.data.polygons:
            for li in face.loop_indices:
                vco = sg.data.vertices[sg.data.loops[li].vertex_index].co
                if sg.name == "front_glass_sheen":
                    uv_arr[li].uv = ((vco.x - x0) / dx, (vco.z - z0) / dz)
                else:
                    uv_arr[li].uv = ((vco.y - y0) / dy, (vco.z - z0) / dz)
        sg.data.update()
        sg.data.materials.clear()
        sg.data.materials.append(mat_front_sheen if sg.name == "front_glass_sheen" else mat_right_sheen)

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
    print(f"Exported Photoreal PBR Metal Closeout v13 GLB: {OUT_GLB} ({OUT_GLB.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
