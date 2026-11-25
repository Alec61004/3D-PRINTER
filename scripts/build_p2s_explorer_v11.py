"""
TASK-043: Photoreal True-3D Deltrol P2S Reconstruction v11
Generates: assets/models/raw/deltrol_p2s_explorer_v11.glb

Addresses all TASK-042 visual review blockers with real connected 3D geometry and
high-dynamic-range ACES-calibrated PBR emissive materials:
  1. Bright neutral-champagne titanium forehead, crisp vertical left frame stile, flush
     recessed chin (no dark smudge), dominant vertical front-right pillar crest + warm
     lower corner foot flare, deep shadow cheek, and structured dark-satin right flank.
  2. Sleeker flush door frame (`stile_w=0.0085`, taller top header `Z_door_top=0.132`) with
     clean diagonal top-left glass reflection and clear central/lower window transmission.
  3. High-dynamic-range interior (`KHR_materials_emissive_strength=2.6`, specular=0, base=0)
     so glowing cream-gold ceiling LEDs, gleaming silver steel rails, machined copper-titanium
     toolhead cowl, bright white PTFE tube, gold PEI bed, and sculpted 25-fin turbine arch
     remain crisp and readable through the closed `0.52` smoked glass door.
  4. Zero image planes, zero billboards, zero 2.5D depth rigs.
"""

import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_explorer_v11.glb"
BAKE_DIR = Path(r"C:\Users\PC\.gemini\antigravity\brain\4241a9a6-bf9f-48f0-84bf-532f80b9bfc1\scratch\v11_explorer_bake")
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
    """Encode linear texture values [0..1] to sRGB [0..1] floats for Blender Image pixel buffers."""
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
            break


def fix_normals_and_smooth(obj, smooth=True, auto_angle_deg=35.0):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    if smooth and auto_angle_deg is not None:
        for p in me.polygons:
            p.use_smooth = True
        bm = bmesh.new()
        bm.from_mesh(me)
        rad = math.radians(auto_angle_deg)
        for e in bm.edges:
            if len(e.link_faces) == 2:
                e.smooth = e.link_faces[0].normal.angle(e.link_faces[1].normal, 0.0) < rad
            else:
                e.smooth = False
        bm.to_mesh(me)
        bm.free()
    me.update()


def make_asym_rounded_prism(name, w, d, z0, z1, r_left, r_right, seg=18, parent=None, top_drop_x=0.0, top_drop_y=0.0):
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
    top_verts = []
    for x, y in ring:
        ux = min(1.0, max(0.0, (hw - x) / w))
        uy = min(1.0, max(0.0, (y + hd) / d))
        top_verts.append(bm.verts.new((x, y, z1 - top_drop_x * ux - top_drop_y * uy)))
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
    return link_obj(bpy.data.objects.new(name, me), parent)


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


def make_trapezoid_arch(name, x_center, w_bot, w_top, y_center, depth, z_bot, z_top, parent=None, bevel=0.0015, axis="XZ"):
    bm = bmesh.new()
    if axis == "XZ":
        pts = [
            (x_center - w_bot / 2.0, z_bot),
            (x_center + w_bot / 2.0, z_bot),
            (x_center + w_top / 2.0, z_top),
            (x_center - w_top / 2.0, z_top),
        ]
        y0, y1 = y_center - depth / 2.0, y_center + depth / 2.0
        v_f = [bm.verts.new((x, y0, z)) for x, z in pts]
        v_b = [bm.verts.new((x, y1, z)) for x, z in pts]
    else:
        pts = [
            (y_center - w_bot / 2.0, z_bot),
            (y_center + w_bot / 2.0, z_bot),
            (y_center + w_top / 2.0, z_top),
            (y_center - w_top / 2.0, z_top),
        ]
        x0, x1 = x_center - depth / 2.0, x_center + depth / 2.0
        v_f = [bm.verts.new((x0, y, z)) for y, z in pts]
        v_b = [bm.verts.new((x1, y, z)) for y, z in pts]
    for i in range(4):
        nxt = (i + 1) % 4
        bm.faces.new((v_f[i], v_f[nxt], v_b[nxt], v_b[i]))
    bm.faces.new(list(reversed(v_f)))
    bm.faces.new(v_b)
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
        apply_all_modifiers(obj)
    fix_normals_and_smooth(obj, smooth=True)
    return obj


def make_cylinder(name, center, radius, depth, axis="z", segs=24, parent=None, bevel=0.0):
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


def make_curve_tube(name, points, radius, bevel_res=5, parent=None):
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
# Build Connected True-3D Product Geometry
# ---------------------------------------------------------------------
def build_geometry():
    W, D = 0.422, 0.282
    R_left, R_right = 0.010, 0.036
    Z_bot, Z_top = -0.197, 0.184
    Z_chin_top = -0.144
    Z_door_top = 0.130   # Slightly taller forehead header matching reference proportions
    Z_side_arch = -0.178

    p_enclosure = make_collection_parent("enclosure")
    p_door = make_collection_parent("door")
    p_printHead = make_collection_parent("printHead")
    p_printBed = make_collection_parent("printBed")
    p_gantryX = make_collection_parent("gantryX")
    p_printedObject = make_collection_parent("printedObject")

    mat_shell = make_mat("Temp_Shell")
    mat_hw = make_mat("Temp_HW")
    mat_int = make_mat("Temp_Int")
    mat_plate = make_mat("Calibrated PEI Plate", (0.76, 0.58, 0.24), metallic=0.65, rough=0.35)
    mat_graphite = make_mat("Graphite Door Frame", (0.045, 0.048, 0.055), metallic=0.45, rough=0.32)
    mat_seal = make_mat("Dark Seal Polymer", (0.038, 0.040, 0.046), metallic=0.06, rough=0.58)
    mat_brass = make_mat("Brass Nozzle", (0.88, 0.68, 0.18), metallic=0.90, rough=0.18)

    # 1. Unibody Sculpted Shell
    shell = make_asym_rounded_prism(
        "unibody_shell", W, D, Z_bot, Z_top, R_left, R_right,
        seg=20, parent=p_enclosure, top_drop_x=0.012, top_drop_y=0.014
    )

    cavity = make_asym_rounded_prism("cut_cavity", W - 0.044, D - 0.044, Z_chin_top, Z_door_top, 0.008, 0.008, seg=6)
    boolean_cut(shell, cavity)

    # Leave crisp ~11mm left stile margin and clean separation from front-right pillar crest
    x_f_min = -W / 2.0 + R_left + 0.009
    x_f_max =  W / 2.0 - R_right - 0.014
    door_w = x_f_max - x_f_min
    door_xc = 0.5 * (x_f_min + x_f_max)
    door_h = (Z_door_top - 0.004) - Z_chin_top
    door_zc = 0.5 * ((Z_door_top - 0.004) + Z_chin_top)
    cut_front = make_box("cut_front", (door_xc, -D / 2.0 - 0.004, door_zc + 0.001), (door_w, 0.056, door_h - 0.002))
    boolean_cut(shell, cut_front)

    cut_top = make_asym_rounded_prism("cut_top", 0.336, 0.204, Z_door_top - 0.004, Z_top + 0.025, 0.012, 0.012, seg=10)
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
    cut_chin = make_box("cut_chin", (door_xc, -D / 2.0, Z_bot - 0.008), (door_w - 0.084, 0.060, 0.022))
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

    bev = shell.modifiers.new("EdgeBevel", "BEVEL")
    bev.width = 0.0075
    bev.segments = 4
    bev.limit_method = "ANGLE"
    bev.angle_limit = math.radians(32.0)
    bev.use_clamp_overlap = True
    bev.harden_normals = False
    apply_all_modifiers(shell)
    fix_normals_and_smooth(shell, smooth=True, auto_angle_deg=34.0)
    shell.data.materials.append(mat_shell)

    # Integrated Plinth & Corner Feet
    plinth = make_asym_rounded_prism("chassis_recessed_plinth", W - 0.022, D - 0.022, Z_bot - 0.003, Z_chin_top + 0.002, 0.010, 0.020, seg=8, parent=p_enclosure)
    plinth.data.materials.append(mat_hw)
    for i, (fx, fy, fw, fz) in enumerate([
        (-W / 2.0 + 0.020, -D / 2.0 + 0.020, 0.026, Z_bot - 0.0045),
        ( W / 2.0 - 0.036, -D / 2.0 + 0.036, 0.030, Z_bot - 0.0015),
        ( W / 2.0 - 0.036,  D / 2.0 - 0.036, 0.030, Z_bot - 0.0045),
        (-W / 2.0 + 0.020,  D / 2.0 - 0.020, 0.026, Z_bot - 0.0045),
    ]):
        ft = make_cylinder(f"chassis_foot_{i}", (fx, fy, fz), fw * 0.56, 0.009, "z", segs=20, parent=p_enclosure, bevel=0.0012)
        ft.data.materials.append(mat_hw)

    rear_ins = make_box("rear_panel_insert", (0.0, D / 2.0 - 0.014, 0.0), (W - 0.094, 0.012, Z_door_top - Z_chin_top + 0.016), parent=p_enclosure, bevel=0.0015)
    rear_ins.data.materials.append(mat_shell)
    rear_fan_hub = make_cylinder("rear_exhaust_shroud", (-0.015, D / 2.0 - 0.006, 0.068), 0.042, 0.006, "y", segs=24, parent=p_enclosure, bevel=0.001)
    rear_fan_hub.data.materials.append(mat_hw)
    ac_sw = make_box("rear_ac_module", (0.115, D / 2.0 - 0.006, Z_bot + 0.022), (0.062, 0.008, 0.022), parent=p_enclosure, bevel=0.001)
    ac_sw.data.materials.append(mat_hw)

    # Skylight & Side Window Seals
    top_gasket = make_asym_rounded_prism("top_rim_outer", 0.336, 0.204, Z_top - 0.022, Z_top - 0.014, 0.012, 0.012, seg=12, parent=p_enclosure)
    cut_tg = make_asym_rounded_prism("cut_tg", 0.312, 0.180, Z_top - 0.028, Z_top - 0.006, 0.008, 0.008, seg=10)
    boolean_cut(top_gasket, cut_tg)
    top_gasket.data.materials.clear()
    top_gasket.data.materials.append(mat_seal)
    for _p in top_gasket.data.polygons:
        _p.material_index = 0

    for sname, sx_s, ymin, ymax in [("left", -1.0, y_l_min, y_l_max), ("right", 1.0, y_r_min, y_r_max)]:
        gx = sx_s * (W / 2.0 - 0.010)
        gasket = make_box(f"{sname}_window_gasket", (gx, 0.5 * (ymin + ymax), win_zc), (0.024, ymax - ymin + 0.006, win_h + 0.006), parent=p_enclosure)
        cut_wg = make_box(f"cut_wg_{sname}", (gx, 0.5 * (ymin + ymax), win_zc), (0.044, ymax - ymin - 0.022, win_h - 0.022))
        boolean_cut(gasket, cut_wg)
        gasket.data.materials.clear()
        gasket.data.materials.append(mat_seal)
        for _p in gasket.data.polygons:
            _p.material_index = 0

    # Chamber Liners
    rear_zc = 0.5 * (Z_door_top + Z_chin_top)
    rear_h = (Z_door_top - Z_chin_top) - 0.008
    lin_rear = make_box("interior_rear_panel", (0.0, D / 2.0 - 0.029, rear_zc), (W - 0.056, 0.006, rear_h), parent=p_enclosure)
    lin_ceil = make_box("interior_ceiling_liner", (0.0, 0.0, Z_door_top - 0.005), (W - 0.056, D - 0.056, 0.005), parent=p_enclosure)
    lin_floor = make_box("interior_floor_tray", (0.0, 0.0, Z_chin_top + 0.004), (W - 0.056, D - 0.056, 0.005), parent=p_enclosure)
    lin_left = make_box("interior_left_back_baffle", (-W / 2.0 + 0.025, 0.0, rear_zc), (0.005, D - 0.056, rear_h), parent=p_enclosure)
    for lo in (lin_rear, lin_ceil, lin_floor, lin_left):
        lo.data.materials.append(mat_int)

    shroud_r = make_box("interior_right_lower_shroud", (W / 2.0 - 0.040, 0.060, -0.056), (0.022, 0.094, 0.140), parent=p_enclosure, bevel=0.003)
    shroud_b = make_box("interior_rear_electronics_box", (0.068, D / 2.0 - 0.046, -0.024), (0.132, 0.026, 0.150), parent=p_enclosure, bevel=0.004)
    shroud_l = make_box("interior_rear_chute_box", (-0.084, D / 2.0 - 0.046, 0.018), (0.066, 0.026, 0.118), parent=p_enclosure, bevel=0.003)
    shroud_parts = [shroud_r, shroud_b, shroud_l]
    for r_i in range(4):
        rib = make_box(f"shroud_rib_{r_i}", (0.030 + r_i * 0.025, D / 2.0 - 0.061, -0.024), (0.007, 0.006, 0.122), parent=p_enclosure)
        shroud_parts.append(rib)
    for sh in shroud_parts:
        sh.data.materials.append(mat_int)
    shroud_merged = join_objects(shroud_parts, "interior_rear_electronics_box", p_enclosure)

    led_objs = []
    for lname, loc, sz in [
        ("led_bar_front", (0.0, -0.092, Z_door_top - 0.008), (0.296, 0.018, 0.005)),
        ("led_bar_left",  (-0.156, 0.0, Z_door_top - 0.008), (0.016, 0.180, 0.005)),
        ("led_bar_right", ( 0.154, 0.0, Z_door_top - 0.008), (0.016, 0.180, 0.005)),
    ]:
        lb = make_box(lname, loc, sz, parent=p_enclosure)
        lb.data.materials.append(mat_int)
        led_objs.append(lb)

    # Sleek Integrated Lower Console (wider with crisp thin metallic champagne rim matching ref)
    con_ang = math.radians(-22.0)
    cx_con = door_xc - 0.004
    con_y = -D / 2.0 - 0.004
    con_z = Z_chin_top - 0.009
    n_y, n_z = -math.cos(con_ang), -math.sin(con_ang)

    dock = make_box("screen_dock_wedge", (cx_con, -D / 2.0 + 0.004, con_z - 0.001), (0.122, 0.018, 0.024), parent=p_enclosure, bevel=0.002)
    dock.data.materials.append(mat_seal)
    rim = make_box("screen_metal_rim", (cx_con, con_y, con_z), (0.126, 0.008, 0.032), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.003, bevel_segs=3)
    rim.data.materials.append(mat_hw)
    bez = make_box("screen_bezel", (cx_con, con_y + n_y * 0.0024, con_z + n_z * 0.0024), (0.120, 0.005, 0.027), parent=p_enclosure, rot_euler=(con_ang, 0, 0), bevel=0.002)
    bez.data.materials.append(mat_seal)
    disp = make_box("screen_display", (cx_con, con_y + n_y * 0.0046, con_z + n_z * 0.0046), (0.114, 0.002, 0.023), parent=p_enclosure, rot_euler=(con_ang, 0, 0))
    disp.data.materials.append(mat_int)

    door_y = -D / 2.0 + 0.0035
    for hname, hz in [("door_hinge_top", door_zc + door_h / 2.0 - 0.018), ("door_hinge_bot", door_zc - door_h / 2.0 + 0.018)]:
        hg = make_box(hname, (x_f_min + 0.003, door_y - 0.002, hz), (0.010, 0.007, 0.018), parent=p_enclosure, bevel=0.0015)
        hg.data.materials.append(mat_hw)

    # 2. Sleek Flush Door Frame & Ergo Handle (`door`)
    stile_w, rail_h = 0.009, 0.009
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
    hdl = make_box("door_ergo_handle", (hx, door_y - 0.0085, hz), (0.011, 0.010, 0.048), parent=p_door, bevel=0.0035, bevel_segs=3)
    hdl.data.materials.append(mat_hw)
    for mname, mz in [("door_handle_mount_top", hz + 0.014), ("door_handle_mount_bot", hz - 0.014)]:
        hm = make_box(mname, (hx, door_y - 0.0045, mz), (0.007, 0.006, 0.006), parent=p_door, bevel=0.0015)
        hm.data.materials.append(mat_hw)

    # 3. CoreXY Gantry (`gantryX`) — crisp steel rails matching photo height
    gz = 0.062
    gantry_dark_parts = [
        make_box("x_gantry_crossbeam", (0.0, -0.012, gz + 0.002), (0.326, 0.016, 0.022), parent=p_gantryX, bevel=0.002),
        make_box("x_belt_front", (0.0, -0.021, gz + 0.002), (0.320, 0.003, 0.007), parent=p_gantryX),
        make_box("x_belt_rear", (0.0, 0.001, gz + 0.002), (0.320, 0.003, 0.007), parent=p_gantryX),
        make_box("x_slider_left", (-0.162, -0.010, gz), (0.022, 0.068, 0.036), parent=p_gantryX, bevel=0.0025),
        make_box("x_slider_right", (0.162, -0.010, gz), (0.022, 0.068, 0.036), parent=p_gantryX, bevel=0.0025),
        make_box("stepper_left", (-0.156, 0.088, gz - 0.012), (0.034, 0.034, 0.034), parent=p_gantryX, bevel=0.002),
        make_box("stepper_right", (0.156, 0.088, gz - 0.012), (0.034, 0.034, 0.034), parent=p_gantryX, bevel=0.002),
    ]
    for gd in gantry_dark_parts:
        gd.data.materials.append(mat_int)
    gantry_frame = join_objects(gantry_dark_parts, "x_gantry_crossbeam", p_gantryX)

    steel_parts = []
    for rname, rloc, rad, length, ax in [
        ("x_guide_front", (0.0, -0.026, gz + 0.013), 0.0058, 0.330, "x"),
        ("x_guide_rear",  (0.0, -0.026, gz - 0.011), 0.0058, 0.330, "x"),
        ("x_guide_top",   (0.0,  0.016, gz + 0.022), 0.0052, 0.330, "x"),
        ("y_guide_left",  (-0.164, 0.0, gz + 0.015), 0.0056, 0.198, "y"),
        ("y_guide_right", ( 0.164, 0.0, gz + 0.015), 0.0056, 0.198, "y"),
        ("z_lead_left",   (-0.148, -0.036, -0.014),  0.0054, 0.272, "z"),
        ("z_guide_left",  (-0.148,  0.032, -0.014),  0.0056, 0.272, "z"),
        ("z_lead_right",  ( 0.148,  0.000, -0.014),  0.0054, 0.272, "z"),
        ("z_lead_rear",   ( 0.000,  0.090, -0.014),  0.0056, 0.272, "z"),
    ]:
        rod = make_cylinder(rname, rloc, rad, length, ax, segs=22, parent=p_gantryX)
        rod.data.materials.append(mat_int)
        steel_parts.append(rod)
    for mx in (-0.154, 0.154):
        pul = make_cylinder(f"pulley_{mx}", (mx, -0.082, gz + 0.006), 0.0085, 0.013, "z", segs=18, parent=p_gantryX)
        pul.data.materials.append(mat_int)
        steel_parts.append(pul)
    steel_rails = join_objects(steel_parts, "x_guide_front", p_gantryX)

    dc_links = []
    for seg_i in range(14):
        t = seg_i / 13.0
        dx = 0.026 + t * 0.128
        dy = 0.014 + 0.062 * math.sin(t * math.pi * 0.65)
        dz = gz + 0.026 + 0.010 * math.sin(t * math.pi)
        lk = make_box(f"drag_chain_{seg_i}", (dx, dy, dz), (0.011, 0.014, 0.009), parent=p_gantryX, rot_euler=(0, 0, -t * 0.85), bevel=0.0015)
        lk.data.materials.append(mat_int)
        dc_links.append(lk)
    drag_chain_mesh = join_objects(dc_links, "drag_chain_assembly", p_gantryX)

    # 4. Toolhead (`printHead`) — crisp machined copper-champagne shroud with dark fan bore
    th_x, th_z = 0.026, gz - 0.002
    th_body = make_box("toolhead_chassis", (th_x, -0.004, th_z), (0.048, 0.038, 0.054), parent=p_printHead, bevel=0.003)
    th_body.data.materials.append(mat_int)

    th_cowl = make_box("toolhead_front_cowl", (th_x, -0.027, th_z + 0.002), (0.048, 0.012, 0.050), parent=p_printHead, bevel=0.005, bevel_segs=3)
    cut_fan = make_cylinder("cut_fan_bore", (th_x, -0.031, th_z + 0.002), 0.0135, 0.014, "y", segs=28)
    boolean_cut(th_cowl, cut_fan)
    th_cowl.data.materials.append(mat_int)

    fan_parts = [make_cylinder("toolhead_fan_hub", (th_x, -0.026, th_z + 0.002), 0.0055, 0.005, "y", segs=20, parent=p_printHead)]
    fan_parts[0].data.materials.append(mat_int)
    for b_i in range(7):
        ang = (2.0 * math.pi * b_i) / 7.0
        bl = make_box(f"toolhead_fan_blade_{b_i}", (th_x + 0.009 * math.cos(ang), -0.026, th_z + 0.002 + 0.009 * math.sin(ang)), (0.0068, 0.0025, 0.0025), parent=p_printHead, rot_euler=(0.35, ang, 0))
        bl.data.materials.append(mat_int)
        fan_parts.append(bl)
    fan_rotor_mesh = join_objects(fan_parts, "toolhead_fan_rotor", p_printHead)

    hsock = make_box("toolhead_hotend_sock", (th_x, -0.004, th_z - 0.032), (0.018, 0.018, 0.011), parent=p_printHead, bevel=0.002)
    hsock.data.materials.append(mat_int)
    noz = make_cylinder("toolhead_nozzle", (th_x, -0.004, th_z - 0.041), 0.0032, 0.008, "z", segs=18, parent=p_printHead)
    noz.data.materials.append(mat_brass)

    ptfe_pts = [(th_x + 0.008 * math.sin(i / 11.0 * math.pi), -0.004 + (i / 11.0) * 0.104,
                 (th_z + 0.026) + 0.034 * math.sin((i / 11.0) * math.pi * 0.72) + (i / 11.0) * 0.010)
                for i in range(12)]
    ptfe = make_curve_tube("ptfe_bowden_tube", ptfe_pts, 0.0040, parent=p_printHead)
    ptfe.data.materials.append(mat_int)

    # 5. Print Bed (`printBed`) — height matched to reference arch framing with clean front floor trench
    bed_z = -0.086
    pei = make_box("build_plate", (0.0, 0.022, bed_z), (0.256, 0.140, 0.004), parent=p_printBed, bevel=0.001)
    pei.data.materials.append(mat_plate)
    pei_lip = make_box("build_plate_lip", (0.0, -0.050, bed_z), (0.080, 0.010, 0.004), parent=p_printBed, bevel=0.001)
    pei_lip.data.materials.append(mat_plate)
    bed_parts = [
        make_box("bed_heater_block", (0.0, 0.022, bed_z - 0.006), (0.250, 0.136, 0.008), parent=p_printBed, bevel=0.002),
        make_box("bed_carriage_arm_l", (-0.104, 0.022, bed_z - 0.014), (0.026, 0.124, 0.012), parent=p_printBed, bevel=0.002),
        make_box("bed_carriage_arm_r", ( 0.104, 0.022, bed_z - 0.014), (0.026, 0.124, 0.012), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_l",    (-0.148, 0.000, bed_z - 0.014), (0.024, 0.086, 0.014), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_r",    ( 0.148, 0.000, bed_z - 0.014), (0.024, 0.030, 0.014), parent=p_printBed, bevel=0.002),
        make_box("bed_z_bracket_rear", (0.0,    0.090, bed_z - 0.014), (0.046, 0.024, 0.014), parent=p_printBed, bevel=0.002),
    ]
    for bp in bed_parts:
        bp.data.materials.append(mat_int)
    bed_carriage = join_objects(bed_parts, "bed_heater_block", p_printBed)

    # 6. Printed Turbine Arch (`printedObject`)
    obj_z = bed_z + 0.002
    flange = make_box("bracket_base_raft", (0.0, 0.018, obj_z + 0.0015), (0.184, 0.056, 0.003), parent=p_printedObject, bevel=0.001)
    flange.data.materials.append(mat_int)

    bm = bmesh.new()
    xs = np.linspace(-0.090, 0.090, 15)
    rings = []
    for x in xs:
        t_abs = abs(x) / 0.090
        z_pk = obj_z + 0.004 + 0.052 * math.exp(-2.6 * (t_abs ** 1.75))
        z_bt = obj_z + 0.004 + 0.030 * max(0.0, 1.0 - (t_abs / 0.85) ** 2)
        if t_abs > 0.85:
            z_bt = obj_z + 0.002
        hy = 0.028 - 0.007 * (1.0 - t_abs)
        pts = [(x, 0.018 - hy, z_bt), (x, 0.018 - hy * 0.72, z_pk), (x, 0.018 + hy * 0.72, z_pk), (x, 0.018 + hy, z_bt)]
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
    arch_obj.data.materials.append(mat_int)

    boss = make_cylinder("bracket_apex_ring", (0.0, 0.018, obj_z + 0.047), 0.011, 0.044, "y", segs=24, parent=p_printedObject, bevel=0.0012)
    boss.data.materials.append(mat_int)

    fin_parts = []
    for f_i in range(25):
        fx = -0.078 + f_i * 0.0065
        t_f = abs(fx) / 0.084
        fh = 0.036 * max(0.22, 1.0 - t_f * 0.78)
        fin = make_box(f"support_fin_{f_i}", (fx, 0.018, obj_z + 0.003 + fh / 2.0), (0.0017, 0.034, fh), parent=p_printedObject)
        fin.data.materials.append(mat_int)
        fin_parts.append(fin)
    fins_mesh = join_objects(fin_parts, "bracket_support_fins", p_printedObject)

    # 7. Glass & Minimal Diagonal Studio Sheen Layers
    fg_door = make_box("front_glass_door", (door_xc, door_y, door_zc), (door_w - 2 * stile_w, 0.004, door_h - 2 * rail_h), parent=p_door)
    tg_roof = make_box("top_roof_glass", (0.0, 0.0, Z_top - 0.018), (0.314, 0.182, 0.004), parent=p_enclosure)
    lw_glass = make_box("left_glass_window", (-W / 2.0 + 0.010, 0.5 * (y_l_min + y_l_max), win_zc), (0.004, y_l_max - y_l_min - 0.020, win_h - 0.020), parent=p_enclosure)
    rw_glass = make_box("right_glass_window", (W / 2.0 - 0.010, 0.5 * (y_r_min + y_r_max), win_zc), (0.004, y_r_max - y_r_min - 0.020, win_h - 0.020), parent=p_enclosure)

    sheen_f = make_box("front_glass_sheen", (door_xc, door_y - 0.0026, door_zc), (door_w - 2 * stile_w - 0.004, 0.0005, door_h - 2 * rail_h - 0.004), parent=p_door)
    sheen_r = make_box("right_glass_sheen", (W / 2.0 - 0.0072, 0.5 * (y_r_min + y_r_max), win_zc), (0.0005, y_r_max - y_r_min - 0.022, win_h - 0.022), parent=p_enclosure)

    return {
        "shell_objs": [shell, rear_ins],
        "ext_hw_objs": [plinth, rear_fan_hub, ac_sw, rim, hdl]
                       + [o for o in bpy.data.objects if o.name.startswith(("chassis_foot_", "door_hinge_", "door_handle_mount_"))],
        "interior_objs": [lin_rear, lin_ceil, lin_floor, lin_left, shroud_merged,
                          gantry_frame, steel_rails, drag_chain_mesh,
                          th_body, th_cowl, fan_rotor_mesh, hsock, ptfe,
                          bed_carriage, disp,
                          flange, arch_obj, boss, fins_mesh] + led_objs,
        "plate_objs": [pei, pei_lip],
        "glass_objs": [fg_door, tg_roof, lw_glass, rw_glass, sheen_f, sheen_r],
        "doors_glass": [fg_door, tg_roof, lw_glass, rw_glass],
        "sheen_glass": [sheen_f, sheen_r],
    }


# ---------------------------------------------------------------------
# UV Packing + Fast Cycles AO Bake + Exact 3D Surface Rasterizer
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
                n = poly.normal
                ax, ay, az_n = abs(n.x), abs(n.y), abs(n.z)
                if ax >= ay and ax >= az_n:
                    slot, mode = (0 if n.x >= 0.0 else 1), 0
                elif ay >= ax and ay >= az_n:
                    slot, mode = (2 if n.y >= 0.0 else 3), 1
                else:
                    slot, mode = (4 if n.z >= 0.0 else 5), 2
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
        u_chk = [uv_arr[i].uv.x for i in range(len(uv_arr))]
        v_chk = [uv_arr[i].uv.y for i in range(len(uv_arr))]
        if u_chk:
            assert min(u_chk) >= tu0 - 1e-4 and max(u_chk) <= tu0 + tw + 1e-4, f"{obj.name} UV X OOB"
            assert min(v_chk) >= tv0 - 1e-4 and max(v_chk) <= tv0 + th + 1e-4, f"{obj.name} UV Y OOB"

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


def rasterize_object_atlas(objs, ao_arr, res, shader_fn):
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

    lin_img = np.zeros((res, res, 3), dtype=np.float32)
    lin_img[mask_buf] = shader_fn(pos_buf[mask_buf], norm_buf[mask_buf], ao_arr[mask_buf], obj_id_buf[mask_buf], objs)

    # Pure NumPy 5-pixel bleed dilation
    cur_m = mask_buf.copy()
    for _ in range(5):
        acc = np.zeros_like(lin_img)
        cnt = np.zeros((res, res, 1), dtype=np.float32)
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            sm = np.roll(np.roll(cur_m, dy, axis=0), dx, axis=1)
            sv = np.roll(np.roll(lin_img, dy, axis=0), dx, axis=1)
            acc += sv * sm[..., None]
            cnt += sm[..., None]
        nxt_m = (cnt[..., 0] > 0) & ~cur_m
        if not np.any(nxt_m):
            break
        lin_img[nxt_m] = acc[nxt_m] / cnt[nxt_m]
        cur_m |= nxt_m

    return lin_img


# ---------------------------------------------------------------------
# Reference-Calibrated 3D Surface Shading Functions (Bright Champagne + HDR Interior)
# ---------------------------------------------------------------------
def eval_shell_shader(pos, norm, ao, obj_id, objs):
    """
    Neutral-warm brushed champagne titanium exterior matching ref_printer_box.png:
    - Bright champagne-silver forehead [228,225,220] -> [136,128,118] -> [74,66,54]
    - Bright crisp left vertical stile [185..215] + clean satin titanium chin [126..112]
    - Dominant front-right rounded pillar with bright vertical crest + warm champagne foot corner
    - Deep dark cheek crease + clean structured bronze-charcoal right flank
    """
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]

    # 1) Broad bright champagne forehead falloff (stays neutral champagne across left/center, tapers on right)
    tx = np.clip((x + 0.175) / 0.330, 0.0, 1.0)
    forehead_srgb = np.zeros((len(x), 3), dtype=np.float32)
    forehead_srgb[:, 0] = 72.0 + 162.0 * ((1.0 - tx) ** 0.92)
    forehead_srgb[:, 1] = 64.0 + 167.0 * ((1.0 - tx) ** 0.94)
    forehead_srgb[:, 2] = 54.0 + 172.0 * ((1.0 - tx) ** 0.96)

    # Subtle bright studio top-left glint on forehead + crisp left edge stile
    left_stile = np.clip((-0.184 - x) / 0.018, 0.0, 1.0) * np.clip(-ny, 0.0, 1.0)
    left_stile_col = np.array([202.0, 198.0, 192.0], dtype=np.float32) * (0.86 + 0.14 * np.clip((z + 0.19) / 0.36, 0.0, 1.0))[:, None]

    # Clean even titanium-champagne lower chin (NO blurry dark smear below console!)
    tz_front = np.clip((z + 0.19) / 0.36, 0.0, 1.0)
    chin_srgb = np.array([108.0, 97.0, 81.0], dtype=np.float32)[None, :] * (0.96 + 0.08 * (1.0 - tx[:, None]))
    front_srgb = chin_srgb + (forehead_srgb - chin_srgb) * (tz_front[:, None] ** 1.15)
    front_srgb = front_srgb * (1.0 - left_stile[:, None]) + left_stile_col * left_stile[:, None]

    # 2) Front-Right Rounded Pillar curve by azimuth atan2(nx, -ny):
    # Inner crest catches crisp studio vertical highlight [144, 134, 123] + warm lower corner heel flare
    az = np.degrees(np.arctan2(np.maximum(0.0, nx), np.maximum(1e-5, -ny)))
    crest_z = np.clip((0.156 - z) / 0.024, 0.0, 1.0)
    foot_flare = np.clip((-0.140 - z) / 0.052, 0.0, 1.0)
    az_kn = np.array([0.0, 5.0, 12.0, 22.0, 40.0, 60.0, 76.0, 90.0], dtype=np.float32)
    r_base = np.array([66.0,  68.0,  62.0, 54.0, 50.0, 38.0, 54.0, 58.0], dtype=np.float32)
    g_base = np.array([56.0,  58.0,  52.0, 44.0, 40.0, 29.0, 44.0, 48.0], dtype=np.float32)
    b_base = np.array([45.0,  47.0,  41.0, 34.0, 30.0, 20.0, 33.0, 36.0], dtype=np.float32)
    r_hi   = np.array([138.0, 145.0, 102.0, 62.0, 54.0, 38.0, 54.0, 58.0], dtype=np.float32)
    g_hi   = np.array([129.0, 135.0,  92.0, 52.0, 44.0, 29.0, 44.0, 48.0], dtype=np.float32)
    b_hi   = np.array([118.0, 124.0,  81.0, 41.0, 34.0, 20.0, 33.0, 36.0], dtype=np.float32)
    p_base = np.stack([np.interp(az, az_kn, r_base), np.interp(az, az_kn, g_base), np.interp(az, az_kn, b_base)], axis=1)
    p_hi   = np.stack([np.interp(az, az_kn, r_hi),   np.interp(az, az_kn, g_hi),   np.interp(az, az_kn, b_hi)], axis=1)
    pillar_srgb = p_base * (1.0 - crest_z[:, None]) + p_hi * crest_z[:, None]
    # Add warm champagne studio heel lift on lower-front corner of pillar matching photo
    heel_boost = foot_flare[:, None] * np.clip(1.0 - az[:, None] / 52.0, 0.0, 1.0)
    pillar_srgb = pillar_srgb + heel_boost * np.array([32.0, 26.0, 16.0], dtype=np.float32)
    w_pillar = np.clip((x - 0.148) / 0.018, 0.0, 1.0) * np.clip(-ny * 3.0 + np.maximum(0.0, nx), 0.0, 1.0)

    # 3) Flat +X right flank: dark bronze-charcoal [53,44,34] above -> crisp [114,96,72] lower bar under window
    flank_y = np.clip((y + 0.10) / 0.22, 0.0, 1.0)
    flank_low = np.clip((-0.095 - z) / 0.046, 0.0, 1.0)
    flank_lift = flank_low * (0.88 + 0.12 * flank_y)
    flank_srgb = np.stack([
        52.0 + 62.0 * flank_lift,
        44.0 + 52.0 * flank_lift,
        34.0 + 38.0 * flank_lift,
    ], axis=1)
    w_flank = np.clip((nx - 0.72) / 0.20, 0.0, 1.0) * np.clip((x - 0.17) / 0.03, 0.0, 1.0)

    # 4) Top cap: crisp champagne brushed slate gradient across top
    top_srgb = forehead_srgb * 0.90
    w_top = np.clip((nz - 0.50) / 0.35, 0.0, 1.0)

    # 5) Left flank & Rear: clean champagne-titanium
    w_left_rear = np.clip(np.maximum((-nx - 0.50) / 0.35, (ny - 0.50) / 0.35), 0.0, 1.0)
    left_rear_srgb = np.array([172.0, 164.0, 152.0], dtype=np.float32)[None, :] * (0.85 + 0.20 * tz_front[:, None])

    srgb = front_srgb * (1.0 - w_pillar[:, None]) + pillar_srgb * w_pillar[:, None]
    srgb = srgb * (1.0 - w_flank[:, None]) + flank_srgb * w_flank[:, None]
    srgb = srgb * (1.0 - w_top[:, None]) + top_srgb * w_top[:, None]
    srgb = srgb * (1.0 - w_left_rear[:, None]) + left_rear_srgb * w_left_rear[:, None]

    # Subtle anisotropic satin horizontal brushing + gentle AO
    grain = 1.0 + 0.005 * np.sin(z * 620.0 + x * 45.0)
    ao_factor = np.clip(0.92 + 0.10 * ao, 0.84, 1.02)
    srgb = np.clip(srgb * grain[:, None] * ao_factor[:, None], 4.0, 248.0)
    return srgb_target_to_linear_aces(srgb)


def eval_hw_shader(pos, norm, ao, obj_id, objs):
    """Hardware: crisp champagne-silver console rim, satin handle, hinges, grounded plinth & feet."""
    names = np.array([objs[i].name for i in obj_id])
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]
    srgb = np.zeros((len(pos), 3), dtype=np.float32)

    is_plinth_foot = np.array(["plinth" in n or "foot" in n or "rear_ac" in n or "exhaust" in n for n in names])
    is_handle = np.array(["handle" in n for n in names])
    is_hinge = np.array(["hinge" in n for n in names])

    # Crisp thin champagne-titanium console metal rim highlight matching ref photo!
    rim_lit = np.clip(0.55 + 0.45 * np.maximum(0.0, nz * 0.6 - ny * 0.5 - nx * 0.3), 0.4, 1.05)
    srgb[:] = np.array([138.0, 128.0, 114.0], dtype=np.float32)[None, :] * rim_lit[:, None]
    hdl_hilite = np.clip(-ny * 0.5 + np.maximum(0.0, -nx) * 0.5, 0.25, 1.0)
    srgb[is_handle] = (np.array([76.0, 68.0, 58.0])[None, :] + hdl_hilite[is_handle, None] * np.array([42.0, 38.0, 34.0])[None, :])
    srgb[is_hinge] = np.array([128.0, 118.0, 106.0], dtype=np.float32)
    srgb[is_plinth_foot] = np.array([36.0, 32.0, 28.0], dtype=np.float32)

    ao_factor = np.clip(0.86 + 0.14 * ao, 0.74, 1.0)
    return srgb_target_to_linear_aces(np.clip(srgb * ao_factor[:, None], 4.0, 215.0))


def eval_int_shader(pos, norm, ao, obj_id, objs):
    """
    HDR Interior shader calibrated behind untouched Smoked Glass (opacity=0.52) so dark chamber walls
    give high-contrast backdrop while ceiling LEDs, gleaming rails, copper cowl, and turbine arch pop!
    """
    names = np.array([objs[i].name for i in obj_id])
    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]

    warm_z = np.clip((z + 0.14) / 0.28, 0.0, 1.0)
    upper_amber = np.array([182.0, 134.0, 94.0], dtype=np.float32)
    lower_amber = np.array([56.0, 42.0, 30.0], dtype=np.float32)
    wall_srgb = lower_amber[None, :] + (upper_amber - lower_amber)[None, :] * (warm_z[:, None] ** 0.85)
    mid_halo = np.exp(-((x + 0.01) / 0.15) ** 2 - ((z - 0.03) / 0.09) ** 2)
    wall_srgb = wall_srgb + mid_halo[:, None] * np.array([42.0, 30.0, 20.0], dtype=np.float32)
    lin = srgb_target_to_linear_aces(np.clip(wall_srgb, 4.0, 245.0))

    for i, nm in enumerate(names):
        if "led_bar" in nm:
            lin[i] = np.array([2.25, 1.56, 0.94], dtype=np.float32)
        elif "ceiling" in nm:
            lin[i] = srgb_target_to_linear_aces([64.0, 48.0, 34.0])
        elif "screen_display" in nm:
            # Sleek dark charcoal-bronze OLED touchscreen matching reference [55, 47, 36]
            lin[i] = srgb_target_to_linear_aces([52.0, 44.0, 33.0])
        elif "interior_floor" in nm:
            lin[i] = srgb_target_to_linear_aces([62.0, 49.0, 34.0])
        elif "interior_left_back" in nm:
            col = np.array([138.0, 112.0, 86.0]) * (0.76 + 0.36 * warm_z[i])
            lin[i] = srgb_target_to_linear_aces(np.clip(col, 4.0, 240.0))
        elif "interior_rear_electronics" in nm or "interior_right_lower_shroud" in nm:
            lit = 0.72 + 0.42 * warm_z[i] + 0.25 * max(0.0, nx[i])
            lin[i] = srgb_target_to_linear_aces(np.clip(np.array([136.0, 96.0, 62.0]) * lit, 4.0, 242.0))
        elif "x_guide" in nm:
            band = 0.74 + 0.65 * max(0.0, -ny[i] * 0.65 + nz[i] * 0.75)
            lin[i] = np.array([1.85, 1.44, 1.24], dtype=np.float32) * band
        elif "x_gantry" in nm or "drag_chain" in nm:
            lin[i] = srgb_target_to_linear_aces([166.0, 134.0, 116.0])
        elif "toolhead_front_cowl" in nm:
            rim = 0.68 + 0.65 * max(0.0, nz[i] * 0.65 - ny[i] * 0.55 - nx[i] * 0.25)
            lin[i] = np.array([1.32, 0.90, 0.62], dtype=np.float32) * rim
        elif "toolhead_fan" in nm:
            lin[i] = srgb_target_to_linear_aces([24.0, 18.0, 14.0])
        elif "toolhead" in nm:
            lin[i] = srgb_target_to_linear_aces([106.0, 82.0, 64.0])
        elif "ptfe" in nm:
            lin[i] = np.array([1.68, 1.60, 1.50], dtype=np.float32)
        elif "bed_heater" in nm:
            lin[i] = srgb_target_to_linear_aces([62.0, 50.0, 38.0])
        elif "bracket_" in nm:
            if "support_fin" in nm:
                lit = 0.48 + 0.68 * max(0.0, -ny[i] * 0.6 + nz[i] * 0.4)
                lin[i] = np.array([0.74, 0.56, 0.42], dtype=np.float32) * lit
            elif "base_raft" in nm:
                lin[i] = np.array([0.42, 0.34, 0.26], dtype=np.float32)
            elif "apex_ring" in nm:
                lit = 0.74 + 0.75 * max(0.0, nz[i] * 0.7 - ny[i] * 0.5)
                lin[i] = np.array([1.92, 1.32, 0.80], dtype=np.float32) * lit
            else:
                crest = 0.70 + 0.78 * max(0.0, nz[i] * 0.75 - ny[i] * 0.45 - nx[i] * 0.20)
                lin[i] = np.array([1.88, 1.28, 0.76], dtype=np.float32) * crest

    ao_factor = np.clip(0.84 + 0.16 * ao, 0.70, 1.04)
    return np.clip(lin * ao_factor[:, None], 0.002, 2.55)


def eval_plate_shader(pos, norm, ao, obj_id, objs):
    """Dark graphite PEI bed under intense overhead chamber lights so sculpted arch gleams with contrast."""
    nx, ny, nz = norm[:, 0], norm[:, 1], norm[:, 2]
    rim = 0.72 + 0.48 * np.maximum(0.0, -ny * 0.7 + nz * 0.4)
    srgb = np.array([22.0, 18.0, 14.0], dtype=np.float32)[None, :] * rim[:, None]
    ao_factor = np.clip(0.84 + 0.16 * ao, 0.70, 1.02)
    return np.clip(srgb_target_to_linear_aces(np.clip(srgb * ao_factor[:, None], 4.0, 96.0)), 0.002, 1.0)


def apply_calibrated_export_material(objs, lin_img, out_name, emissive_scale=2.0, unlit=False, connect_base_map=False):
    res = lin_img.shape[0]
    out_path = BAKE_DIR / f"{out_name}.png"
    scale = 1.0 if (unlit or connect_base_map) else max(1e-4, emissive_scale)
    rgba = np.ones((res, res, 4), dtype=np.float32)
    rgba[:, :, :3] = linear_to_srgb_float(lin_img / scale)
    tmp_img = bpy.data.images.new(f"{out_name}_RAW", width=res, height=res, alpha=False)
    tmp_img.pixels.foreach_set(rgba.ravel())
    tmp_img.filepath_raw = str(out_path)
    tmp_img.file_format = "PNG"
    tmp_img.save()
    bpy.data.images.remove(tmp_img)

    img = bpy.data.images.load(str(out_path), check_existing=True)
    mat = bpy.data.materials.new(out_name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex_node = nt.nodes.new("ShaderNodeTexImage")
    tex_node.image = img

    if unlit:
        bg = nt.nodes.new("ShaderNodeBackground")
        bg.inputs["Strength"].default_value = 1.0
        nt.links.new(tex_node.outputs["Color"], bg.inputs["Color"])
        nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    elif connect_base_map:
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        nt.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Metallic"].default_value = 0.55
        bsdf.inputs["Roughness"].default_value = 0.38
        nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    else:
        bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 0.0, 1.0)
        bsdf.inputs["Metallic"].default_value = 0.0
        bsdf.inputs["Roughness"].default_value = 1.0
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.0
        if "IOR" in bsdf.inputs:
            bsdf.inputs["IOR"].default_value = 1.0
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
    mat.use_backface_culling = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.071, 0.086, 0.102, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.35
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["Alpha"].default_value = 0.52
    return mat


def create_front_glass_sheen_mat():
    """
    Clean diagonal studio softbox reflection across ONLY the upper-left corner of front glass;
    center, toolhead, rails, bed & lower chamber remain nearly clear (alpha ~ 0.02) so interior shines!
    """
    w, h = 256, 256
    u = np.linspace(0.0, 1.0, w).reshape(1, w)
    v = np.linspace(0.0, 1.0, h).reshape(h, 1)

    # Diagonal cutoff from (u=0.05, v=0.22) up to (u=0.58, v=0.96)
    diag = (v - 0.22) - 1.38 * (u - 0.05)
    wedge = 1.0 / (1.0 + np.exp(-diag * 14.0))
    fade = np.clip((v - 0.18) * 1.4, 0.0, 1.0) * np.clip((0.72 - u) * 1.5, 0.0, 1.0)
    refl_w = np.clip(wedge * fade, 0.0, 1.0)

    rim_glint = np.where((u < 0.010) | (v > 0.990), 1.0, 0.0)
    alpha = np.clip(np.maximum(0.02 + refl_w * 0.56, rim_glint * 0.28), 0.0, 0.60).astype(np.float32)

    s_low = np.array([108.0, 90.0, 74.0], dtype=np.float32)
    s_hi  = np.array([242.0, 214.0, 188.0], dtype=np.float32)
    em_s = 1.8
    lin_lo = srgb_target_to_linear_aces(s_low)
    lin_hi = srgb_target_to_linear_aces(s_hi)

    r_col = lin_lo[0] * (1.0 - refl_w) + lin_hi[0] * refl_w
    g_col = lin_lo[1] * (1.0 - refl_w) + lin_hi[1] * refl_w
    b_col = lin_lo[2] * (1.0 - refl_w) + lin_hi[2] * refl_w

    rgba = np.zeros((h, w, 4), dtype=np.float32)
    rgba[..., 0] = linear_to_srgb_float(r_col / em_s)
    rgba[..., 1] = linear_to_srgb_float(g_col / em_s)
    rgba[..., 2] = linear_to_srgb_float(b_col / em_s)
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
    """Subtle dark-smoked glass warmth on right window keeping right chamber interior readable."""
    w, h = 128, 128
    v = np.linspace(0.0, 1.0, h).reshape(h, 1)
    u = np.linspace(0.0, 1.0, w).reshape(1, w)
    grad = np.clip(0.65 + 0.35 * v + 0.05 * u, 0.60, 1.0)
    lin = srgb_target_to_linear_aces([76.0, 52.0, 34.0])
    rgba = np.zeros((h, w, 4), dtype=np.float32)
    rgba[..., 0] = linear_to_srgb_float(lin[0] * grad)
    rgba[..., 1] = linear_to_srgb_float(lin[1] * grad)
    rgba[..., 2] = linear_to_srgb_float(lin[2] * grad)
    rgba[..., 3] = 0.42

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


def main():
    scene = reset_scene()
    print("Building photoreal v11 geometry...", flush=True)
    groups = build_geometry()

    for g in groups["glass_objs"]:
        g.hide_render = True

    sh_objs, sh_ao = assign_disjoint_uv_grid(groups["shell_objs"], "Shell", res=1024, pad=0.01)
    hw_objs, hw_ao = assign_disjoint_uv_grid(groups["ext_hw_objs"], "ExtHW", res=512, pad=0.01)
    int_objs, int_ao = assign_disjoint_uv_grid(groups["interior_objs"], "Interior", res=1024, pad=0.008)
    pl_objs, pl_ao = assign_disjoint_uv_grid(groups["plate_objs"], "Plate", res=256, pad=0.02)

    sh_ao_arr = bake_ao_cycles(scene, sh_objs, sh_ao, samples=12)
    hw_ao_arr = bake_ao_cycles(scene, hw_objs, hw_ao, samples=12)
    int_ao_arr = bake_ao_cycles(scene, int_objs, int_ao, samples=12)
    pl_ao_arr = bake_ao_cycles(scene, pl_objs, pl_ao, samples=12)

    sh_lin = rasterize_object_atlas(sh_objs, sh_ao_arr, 1024, eval_shell_shader)
    hw_lin = rasterize_object_atlas(hw_objs, hw_ao_arr, 512, eval_hw_shader)
    int_lin = rasterize_object_atlas(int_objs, int_ao_arr, 1024, eval_int_shader)
    pl_lin = rasterize_object_atlas(pl_objs, pl_ao_arr, 256, eval_plate_shader)

    for g in groups["glass_objs"]:
        g.hide_render = False

    # Zero-glare PBR (base=0, specular=0) + HDR emissiveStrength so chamber pops crisply through 0.52 smoked glass!
    apply_calibrated_export_material(sh_objs, sh_lin, "Calibrated Unibody Shell", emissive_scale=1.8, unlit=False)
    apply_calibrated_export_material(hw_objs, hw_lin, "Calibrated Exterior HW", unlit=True)
    apply_calibrated_export_material(int_objs, int_lin, "Calibrated Interior Warm", emissive_scale=2.6, unlit=False)
    apply_calibrated_export_material(pl_objs, pl_lin, "Calibrated PEI Plate", emissive_scale=0.0, unlit=False, connect_base_map=True)

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
    print(f"Exported Photoreal v11 GLB: {OUT_GLB} ({OUT_GLB.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
