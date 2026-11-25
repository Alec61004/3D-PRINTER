import io
import json
import math
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OPT_PATH = ROOT / "assets" / "models" / "optimized" / "deltrol_p2s_optimized.glb"
PUB_PATH = ROOT / "website" / "public" / "models" / "deltrol_p2s_optimized.glb"

class DetailedGLBBuilder:
    def __init__(self, cylinder_segments=24):
        self.bin = bytearray()
        self.buffer_views = []
        self.accessors = []
        self.meshes = []
        self.nodes = []
        self.materials = []
        self.images = []
        self.textures = []
        self.parents = {}
        self.cylinder_segments = cylinder_segments
        self.material_cache = {}

    def align(self, multiple=4):
        while len(self.bin) % multiple:
            self.bin.append(0)

    def add_blob(self, data: bytes, target=None):
        self.align()
        offset = len(self.bin)
        self.bin.extend(data)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
        if target is not None:
            view["target"] = target
        self.buffer_views.append(view)
        return len(self.buffer_views) - 1

    def add_accessor(self, data: bytes, component_type: int, count: int, accessor_type: str, minimum=None, maximum=None, target=None):
        view = self.add_blob(data, target=target)
        accessor = {
            "bufferView": view,
            "componentType": component_type,
            "count": count,
            "type": accessor_type,
        }
        if minimum is not None:
            accessor["min"] = minimum
        if maximum is not None:
            accessor["max"] = maximum
        self.accessors.append(accessor)
        return len(self.accessors) - 1

    def add_material(self, name, rgba, metallic, roughness, alpha_mode="OPAQUE", texture_img=None, emissive=None):
        key = name
        if key in self.material_cache:
            return self.material_cache[key]

        if texture_img is None:
            texture_img = Image.new("RGBA", (4, 4), tuple(rgba))

        stream = io.BytesIO()
        texture_img.save(stream, format="PNG", optimize=True)
        img_bytes = stream.getvalue()

        image_view = self.add_blob(img_bytes)
        image_index = len(self.images)
        self.images.append({"bufferView": image_view, "mimeType": "image/png", "name": f"{name} Texture"})

        texture_index = len(self.textures)
        self.textures.append({"sampler": 0, "source": image_index, "name": f"{name} Texture"})

        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [1, 1, 1, rgba[3] / 255.0],
                "baseColorTexture": {"index": texture_index},
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "alphaMode": alpha_mode,
            "doubleSided": True,
        }
        if emissive:
            material["emissiveFactor"] = emissive
        if alpha_mode == "BLEND":
            material["extras"] = {"note": "Smoked transparent glass"}
        self.materials.append(material)
        index = len(self.materials) - 1
        self.material_cache[key] = index
        return index

    def add_mesh_primitive(self, name, positions, normals, uvs, indices, material_index):
        pos_bytes = struct.pack(f"<{len(positions)}f", *positions)
        norm_bytes = struct.pack(f"<{len(normals)}f", *normals)
        uv_bytes = struct.pack(f"<{len(uvs)}f", *uvs)
        index_bytes = struct.pack(f"<{len(indices)}H", *indices)
        mins = [min(positions[i::3]) for i in range(3)]
        maxs = [max(positions[i::3]) for i in range(3)]
        pos_accessor = self.add_accessor(pos_bytes, 5126, len(positions) // 3, "VEC3", mins, maxs, 34962)
        norm_accessor = self.add_accessor(norm_bytes, 5126, len(normals) // 3, "VEC3", target=34962)
        uv_accessor = self.add_accessor(uv_bytes, 5126, len(uvs) // 2, "VEC2", target=34962)
        idx_accessor = self.add_accessor(index_bytes, 5123, len(indices), "SCALAR", target=34963)
        mesh = {
            "name": name,
            "primitives": [{
                "attributes": {"POSITION": pos_accessor, "NORMAL": norm_accessor, "TEXCOORD_0": uv_accessor},
                "indices": idx_accessor,
                "material": material_index,
                "mode": 4,
            }],
        }
        self.meshes.append(mesh)
        return len(self.meshes) - 1

    def add_parent(self, name):
        node_index = len(self.nodes)
        self.nodes.append({"name": name, "children": [], "extras": {"logicalPart": name}})
        self.parents[name] = node_index
        return node_index

    def add_box(self, parent_name, mesh_name, center, size, material_index):
        cx, cy, cz = center
        sx, sy, sz = [s / 2.0 for s in size]
        faces = [
            # Front (+y)
            {"norm": (0, 1, 0), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            # Back (-y)
            {"norm": (0, -1, 0), "quad": [(cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz)]},
            # Right (+x)
            {"norm": (1, 0, 0), "quad": [(cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz)]},
            # Left (-x)
            {"norm": (-1, 0, 0), "quad": [(cx - sx, cy - sy, cz - sz), (cx - sx, cy + sy, cz - sz), (cx - sx, cy + sy, cz + sz), (cx - sx, cy - sy, cz + sz)]},
            # Top (+z)
            {"norm": (0, 0, 1), "quad": [(cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            # Bottom (-z)
            {"norm": (0, 0, -1), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz)]},
        ]
        positions, normals, uvs, indices = [], [], [], []
        idx = 0
        for f in faces:
            nx, ny, nz = f["norm"]
            for i, p in enumerate(f["quad"]):
                positions.extend(p)
                normals.extend([nx, ny, nz])
                u = 0.0 if i in (0, 3) else 1.0
                v = 0.0 if i in (0, 1) else 1.0
                uvs.extend([u, v])
            indices.extend([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
            idx += 4

        mesh_idx = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        node_idx = len(self.nodes)
        self.nodes.append({"name": mesh_name, "mesh": mesh_idx})
        self.nodes[self.parents[parent_name]]["children"].append(node_idx)
        return node_idx

    def add_cylinder(self, parent_name, mesh_name, center, radius, height, axis="z", material_index=0):
        cx, cy, cz = center
        seg = self.cylinder_segments
        positions, normals, uvs, indices = [], [], [], []
        hh = height / 2.0

        for i in range(seg):
            th1 = 2 * math.pi * i / seg
            th2 = 2 * math.pi * (i + 1) / seg
            c1, s1 = math.cos(th1), math.sin(th1)
            c2, s2 = math.cos(th2), math.sin(th2)

            if axis == "z":
                p1_bot = (cx + radius * c1, cy + radius * s1, cz - hh)
                p2_bot = (cx + radius * c2, cy + radius * s2, cz - hh)
                p2_top = (cx + radius * c2, cy + radius * s2, cz + hh)
                p1_top = (cx + radius * c1, cy + radius * s1, cz + hh)
                n1 = (c1, s1, 0)
                n2 = (c2, s2, 0)
            elif axis == "y":
                p1_bot = (cx + radius * c1, cy - hh, cz + radius * s1)
                p2_bot = (cx + radius * c2, cy - hh, cz + radius * s2)
                p2_top = (cx + radius * c2, cy + hh, cz + radius * s2)
                p1_top = (cx + radius * c1, cy + hh, cz + radius * s1)
                n1 = (c1, 0, s1)
                n2 = (c2, 0, s2)
            else: # x
                p1_bot = (cx - hh, cy + radius * c1, cz + radius * s1)
                p2_bot = (cx - hh, cy + radius * c2, cz + radius * s2)
                p2_top = (cx + hh, cy + radius * c2, cz + radius * s2)
                p1_top = (cx + hh, cy + radius * c1, cz + radius * s1)
                n1 = (0, c1, s1)
                n2 = (0, c2, s2)

            base_idx = len(positions) // 3
            positions.extend([*p1_bot, *p2_bot, *p2_top, *p1_top])
            normals.extend([*n1, *n2, *n2, *n1])
            uvs.extend([i / seg, 0.0, (i + 1) / seg, 0.0, (i + 1) / seg, 1.0, i / seg, 1.0])
            indices.extend([base_idx, base_idx + 1, base_idx + 2, base_idx, base_idx + 2, base_idx + 3])

        # End caps
        for cap_dir in (-1, 1):
            cap_center = list(center)
            if axis == "z":
                cap_center[2] += cap_dir * hh
                norm = (0, 0, cap_dir)
            elif axis == "y":
                cap_center[1] += cap_dir * hh
                norm = (0, cap_dir, 0)
            else:
                cap_center[0] += cap_dir * hh
                norm = (cap_dir, 0, 0)

            c_idx = len(positions) // 3
            positions.extend(cap_center)
            normals.extend(norm)
            uvs.extend([0.5, 0.5])

            for i in range(seg):
                th = 2 * math.pi * i / seg
                c, s = math.cos(th), math.sin(th)
                if axis == "z":
                    p = (cap_center[0] + radius * c, cap_center[1] + radius * s, cap_center[2])
                elif axis == "y":
                    p = (cap_center[0] + radius * c, cap_center[1], cap_center[2] + radius * s)
                else:
                    p = (cap_center[0], cap_center[1] + radius * c, cap_center[2] + radius * s)

                positions.extend(p)
                normals.extend(norm)
                uvs.extend([0.5 + 0.5 * c, 0.5 + 0.5 * s])

            for i in range(seg):
                nxt = (i + 1) % seg
                if cap_dir == 1:
                    indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])
                else:
                    indices.extend([c_idx, c_idx + 1 + nxt, c_idx + 1 + i])

        mesh_idx = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        node_idx = len(self.nodes)
        self.nodes.append({"name": mesh_name, "mesh": mesh_idx})
        self.nodes[self.parents[parent_name]]["children"].append(node_idx)
        return node_idx

    def add_spool(self, parent_name, spool_name, center, outer_r, width, inner_r, axis, rim_mat, filament_mat, mount_mat):
        cx, cy, cz = center
        # Spool mount bracket attached to chassis wall
        flange_thick = width * 0.10
        if axis == "x":
            # Spool holder axle
            self.add_cylinder(parent_name, f"{spool_name}_axle", (cx, cy, cz), inner_r * 0.45, width * 1.35, "x", mount_mat)
            # Spool flanges
            self.add_cylinder(parent_name, f"{spool_name}_flange_L", (cx - width/2 + flange_thick/2, cy, cz), outer_r, flange_thick, "x", rim_mat)
            self.add_cylinder(parent_name, f"{spool_name}_flange_R", (cx + width/2 - flange_thick/2, cy, cz), outer_r, flange_thick, "x", rim_mat)
            # Wound filament coil
            self.add_cylinder(parent_name, f"{spool_name}_filament", (cx, cy, cz), outer_r * 0.88, width * 0.80, "x", filament_mat)

    def create_screen_texture(self):
        w, h = 256, 128
        img = Image.new("RGBA", (w, h), (14, 18, 24, 255))
        draw = ImageDraw.Draw(img)
        # Gradient border
        draw.rectangle([2, 2, w - 3, h - 3], outline=(36, 54, 72, 255), width=2)
        # Status header
        draw.text((12, 8), "DELTROL P2S PRO", fill=(215, 235, 250, 255))
        draw.text((172, 8), "PRINTING", fill=(56, 189, 248, 255))
        draw.line([12, 25, w - 12, 25], fill=(42, 60, 78, 255), width=1)
        # Telemetry
        draw.text((14, 34), "NOZZLE: 245°C", fill=(245, 155, 35, 255))
        draw.text((14, 52), "BED:    65°C", fill=(56, 189, 248, 255))
        draw.text((14, 70), "CHAMBER: 52°C", fill=(175, 195, 215, 255))
        draw.text((14, 88), "SPEED: 250 mm/s", fill=(130, 165, 185, 255))
        draw.text((14, 106), "MATERIAL: PA-CF", fill=(95, 135, 155, 255))
        # 45% circular gauge on right side
        cx, cy, r = 195, 75, 34
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 45, 60, 255), width=5)
        # Arc for 45%
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=-90, end=72, fill=(56, 189, 248, 255), width=5)
        draw.text((cx - 15, cy - 8), "45%", fill=(255, 255, 255, 255))
        return img

    def build_scene(self):
        # -------------------------------------------------------------
        # High-Fidelity Materials matching Doop Canvas Hero Render
        # -------------------------------------------------------------
        dark_chassis   = self.add_material("Chassis Matte Dark", (28, 32, 36, 255), 0.40, 0.45)
        chassis_accent = self.add_material("Chassis Dark Gray", (40, 45, 52, 255), 0.45, 0.38)
        silver_frame   = self.add_material("Silver Aluminum Frame", (205, 212, 220, 255), 0.88, 0.20)
        silver_caps    = self.add_material("Chamfered Corner Caps", (225, 232, 238, 255), 0.92, 0.16)
        smoked_glass   = self.add_material("Smoked Glass", (18, 26, 34, 85), 0.15, 0.08, alpha_mode="BLEND")
        ceiling_light  = self.add_material("Ceiling LED Bar", (255, 248, 220, 255), 0.10, 0.20, emissive=[1.0, 0.94, 0.80])
        gold_pei       = self.add_material("Gold Textured PEI", (215, 172, 48, 255), 0.70, 0.32)
        carbon_fiber   = self.add_material("PA-CF Carbon Fiber", (34, 38, 42, 255), 0.28, 0.42)
        tree_support   = self.add_material("White Tree Support", (238, 235, 228, 255), 0.08, 0.58)
        brass_nozzle   = self.add_material("Brass Nozzle", (238, 178, 42, 255), 0.92, 0.22)
        ptfe_white     = self.add_material("PTFE Guide Tube", (245, 245, 250, 255), 0.05, 0.30)
        steel_rails    = self.add_material("Linear Guide Steel", (220, 225, 230, 255), 0.95, 0.12)
        rubber_belt    = self.add_material("GT2 Timing Belt", (15, 18, 22, 255), 0.05, 0.85)
        spool_rim      = self.add_material("Spool Rim Poly", (85, 95, 105, 255), 0.25, 0.35)
        carbon_filament= self.add_material("Black Filament PA-CF", (24, 26, 30, 255), 0.25, 0.48)
        white_filament = self.add_material("White Filament PLA", (242, 244, 246, 255), 0.10, 0.40)

        # Screen with 45% gauge
        screen_tex = self.create_screen_texture()
        screen_mat = self.add_material("Screen UI 45%", (255, 255, 255, 255), 0.0, 0.2, texture_img=screen_tex)

        # Logical parts
        for part in ["enclosure", "door", "printHead", "printBed", "gantryX", "gantryY", "printedObject", "treeSupport", "spools"]:
            self.add_parent(part)

        # -------------------------------------------------------------
        # 1. ENCLOSURE (Unibody Casing, thick pillars, chamfered corner caps)
        # Dimensions: Width: 0.40m, Depth: 0.40m, Height: 0.46m
        # Bed surface at Z = -0.128. Chamber ceiling at Z = +0.200.
        # -------------------------------------------------------------
        # Base plinth and bottom tray
        self.add_box("enclosure", "base_plinth", (0, 0, -0.238), (0.40, 0.40, 0.024), dark_chassis)
        self.add_box("enclosure", "bottom_panel", (0, 0, -0.224), (0.39, 0.39, 0.012), silver_frame)
        self.add_box("enclosure", "top_rim_outer", (0, 0, 0.222), (0.40, 0.40, 0.018), silver_frame)
        self.add_box("enclosure", "top_roof_glass", (0, 0, 0.222), (0.32, 0.32, 0.012), smoked_glass)

        # Overhead warm LED lighting bars inside ceiling
        self.add_box("enclosure", "led_bar_front", (0, -0.145, 0.205), (0.32, 0.014, 0.008), ceiling_light)
        self.add_box("enclosure", "led_bar_rear",  (0, 0.145, 0.205),  (0.32, 0.014, 0.008), ceiling_light)
        self.add_box("enclosure", "led_bar_left",  (-0.155, 0, 0.205), (0.014, 0.28, 0.008), ceiling_light)
        self.add_box("enclosure", "led_bar_right", (0.155, 0, 0.205),  (0.014, 0.28, 0.008), ceiling_light)

        # Vertical corner columns (substantial structural corner posts)
        for x in (-0.185, 0.185):
            for y in (-0.185, 0.185):
                # Cylindrical posts give the enclosure the rounded vertical
                # silhouette visible in the reference instead of sharp boxes.
                self.add_cylinder("enclosure", f"corner_post_{x}_{y}", (x, y, -0.005), 0.022, 0.442, "z", dark_chassis)

        # Chamfered corner bumper caps (4 top, 4 bottom - iconic Doop Canvas design)
        for x in (-0.186, 0.186):
            for y in (-0.186, 0.186):
                self.add_box("enclosure", f"corner_cap_top_{x}_{y}", (x, y, 0.218), (0.040, 0.040, 0.026), silver_caps)
                self.add_box("enclosure", f"corner_cap_bot_{x}_{y}", (x, y, -0.228), (0.040, 0.040, 0.026), silver_caps)

        # Front top header beam
        self.add_box("enclosure", "front_top_beam", (0, -0.186, 0.205), (0.34, 0.026, 0.026), dark_chassis)
        # Front bottom fascia, symmetric around the recessed center console.
        self.add_box("enclosure", "front_bot_fascia_left", (-0.085, -0.186, -0.198), (0.170, 0.024, 0.048), dark_chassis)
        self.add_box("enclosure", "front_bot_fascia_right", (0.085, -0.186, -0.198), (0.170, 0.024, 0.048), dark_chassis)

        # Side walls with window cutouts for filament spools
        # Left side wall: Solid dark charcoal panel with central tinted window & vent louvers
        self.add_box("enclosure", "left_wall_top", (-0.188, 0, 0.185), (0.014, 0.34, 0.032), dark_chassis)
        self.add_box("enclosure", "left_wall_bot", (-0.188, 0, -0.185), (0.014, 0.34, 0.032), dark_chassis)
        self.add_box("enclosure", "left_wall_front", (-0.188, -0.154, 0), (0.014, 0.032, 0.34), dark_chassis)
        self.add_box("enclosure", "left_wall_rear", (-0.188, 0.154, 0), (0.014, 0.032, 0.34), dark_chassis)
        self.add_box("enclosure", "left_glass_window", (-0.188, 0, 0), (0.008, 0.30, 0.34), smoked_glass)
        # Recessed handle on left
        self.add_box("enclosure", "left_handle", (-0.194, 0, 0.160), (0.012, 0.080, 0.032), chassis_accent)
        # Vent louvers on lower left
        self.add_box("enclosure", "left_vent", (-0.194, 0, -0.165), (0.010, 0.160, 0.035), rubber_belt)

        # Right side wall: Solid dark charcoal panel with central tinted window & vent louvers
        self.add_box("enclosure", "right_wall_top", (0.188, 0, 0.185), (0.014, 0.34, 0.032), dark_chassis)
        self.add_box("enclosure", "right_wall_bot", (0.188, 0, -0.185), (0.014, 0.34, 0.032), dark_chassis)
        self.add_box("enclosure", "right_wall_front", (0.188, -0.154, 0), (0.014, 0.032, 0.34), dark_chassis)
        self.add_box("enclosure", "right_wall_rear", (0.188, 0.154, 0), (0.014, 0.032, 0.34), dark_chassis)
        self.add_box("enclosure", "right_glass_window", (0.188, 0, 0), (0.008, 0.30, 0.34), smoked_glass)
        # Recessed handle on right
        self.add_box("enclosure", "right_handle", (0.194, 0, 0.160), (0.012, 0.080, 0.032), chassis_accent)
        # Vent louvers on lower right
        self.add_box("enclosure", "right_vent", (0.194, 0, -0.165), (0.010, 0.160, 0.035), rubber_belt)

        # Rear metal panel
        self.add_box("enclosure", "rear_panel", (0, 0.188, -0.005), (0.34, 0.014, 0.442), dark_chassis)

        # Door (front glass with dark frame & silver handle)
        self.add_box("door", "front_glass_door", (0, -0.188, 0.010), (0.33, 0.008, 0.365), smoked_glass)
        self.add_box("door", "door_left_stile", (-0.165, -0.194, 0.010), (0.015, 0.010, 0.365), dark_chassis)
        self.add_box("door", "door_right_stile", (0.165, -0.194, 0.010), (0.015, 0.010, 0.365), dark_chassis)
        self.add_box("door", "door_top_rail", (0, -0.194, 0.186), (0.33, 0.010, 0.015), dark_chassis)
        self.add_box("door", "door_bottom_rail", (0, -0.194, -0.166), (0.33, 0.010, 0.015), dark_chassis)
        self.add_box("door", "door_handle", (0.155, -0.204, 0), (0.010, 0.014, 0.14), silver_frame)

        # Bottom-right angled touchscreen console (Canvas exact placement)
        self.add_box("enclosure", "screen_bezel", (0.105, -0.196, -0.185), (0.118, 0.024, 0.068), dark_chassis)
        self.add_box("enclosure", "screen_display", (0.105, -0.208, -0.185), (0.105, 0.004, 0.054), screen_mat)

        # -------------------------------------------------------------
        # 2. DUAL FILAMENT SPOOLS (Left: Carbon PA-CF, Right: White PLA)
        # Mounted inside the side windows
        # -------------------------------------------------------------
        self.add_spool("spools", "left_carbon_spool", (-0.142, 0.015, 0.005), 0.068, 0.030, 0.040, "x", spool_rim, carbon_filament, dark_chassis)
        self.add_spool("spools", "right_white_spool", (0.142, 0.015, 0.005), 0.068, 0.030, 0.040, "x", spool_rim, white_filament, dark_chassis)

        # -------------------------------------------------------------
        # 3. PRINT BED (Gold Textured PEI plate on carriage)
        # Bed surface is at exact Z = -0.128
        # -------------------------------------------------------------
        self.add_box("printBed", "build_plate", (0, -0.015, -0.135), (0.30, 0.28, 0.014), gold_pei)
        self.add_box("printBed", "bed_lip", (0, -0.158, -0.126), (0.26, 0.012, 0.014), silver_caps)
        self.add_box("printBed", "bed_carriage", (0, 0.015, -0.158), (0.25, 0.22, 0.018), dark_chassis)
        for x in (-0.11, 0.11):
            for y in (-0.10, 0.10):
                self.add_cylinder("printBed", f"bed_mount_{x}_{y}", (x, y, -0.122), 0.006, 0.008, "z", steel_rails)

        # -------------------------------------------------------------
        # 4. GANTRY & COREXY MOTION
        # -------------------------------------------------------------
        self.add_cylinder("gantryX", "x_guide_front", (0, -0.065, 0.145), 0.006, 0.29, "x", steel_rails)
        self.add_cylinder("gantryX", "x_guide_rear", (0, 0.065, 0.145), 0.006, 0.29, "x", steel_rails)
        self.add_box("gantryX", "x_belt_front", (0, -0.076, 0.125), (0.30, 0.004, 0.004), rubber_belt)
        self.add_box("gantryX", "x_belt_rear", (0, 0.076, 0.125), (0.30, 0.004, 0.004), rubber_belt)

        self.add_cylinder("gantryY", "y_guide_left", (-0.138, 0, 0.145), 0.006, 0.26, "y", steel_rails)
        self.add_cylinder("gantryY", "y_guide_right", (0.138, 0, 0.145), 0.006, 0.26, "y", steel_rails)
        self.add_cylinder("gantryY", "z_lead_left", (-0.138, 0.09, 0.0), 0.005, 0.32, "z", steel_rails)
        self.add_cylinder("gantryY", "z_lead_right", (0.138, 0.09, 0.0), 0.005, 0.32, "z", steel_rails)
        self.add_box("gantryY", "left_carriage", (-0.138, 0, 0.145), (0.022, 0.035, 0.038), dark_chassis)
        self.add_box("gantryY", "right_carriage", (0.138, 0, 0.145), (0.022, 0.035, 0.038), dark_chassis)

        # -------------------------------------------------------------
        # 5. DUAL-EXTRUDER TOOLHEAD (`printHead`)
        # Standardized so that at printHead Z-offset = 0, the active nozzle
        # tip is EXACTLY at Z = -0.128 (touching the PEI bed surface)!
        # Active nozzle is at (X = 0.016, Y = -0.015).
        # -------------------------------------------------------------
        # Dual brass nozzles (bottom tips at Z = -0.128)
        self.add_cylinder("printHead", "nozzle_left",   (-0.016, -0.015, -0.115), 0.0045, 0.026, "z", brass_nozzle)
        self.add_cylinder("printHead", "nozzle_active", (0.016,  -0.015, -0.115), 0.0045, 0.026, "z", brass_nozzle)

        # Extruder heatblock
        self.add_box("printHead", "heatblock_left",  (-0.016, -0.015, -0.094), (0.022, 0.022, 0.016), silver_frame)
        self.add_box("printHead", "heatblock_right", (0.016,  -0.015, -0.094), (0.022, 0.022, 0.016), silver_frame)

        # Toolhead main chassis housing
        self.add_box("printHead", "toolhead_body", (0, -0.015, -0.046), (0.086, 0.054, 0.076), dark_chassis)
        self.add_box("printHead", "toolhead_face", (0, -0.043, -0.046), (0.082, 0.006, 0.068), silver_frame)

        # Dual circular cooling fan intakes on front face (iconic P2S look)
        for fx in (-0.022, 0.022):
            # Outer dark bezel
            self.add_cylinder("printHead", f"fan_bezel_{fx}", (fx, -0.046, -0.042), 0.016, 0.004, "y", dark_chassis)
            # Silver center spinner hub
            self.add_cylinder("printHead", f"fan_hub_{fx}", (fx, -0.048, -0.042), 0.007, 0.004, "y", silver_caps)
            # Circular intake ring
            self.add_cylinder("printHead", f"fan_ring_{fx}", (fx, -0.047, -0.042), 0.014, 0.002, "y", rubber_belt)

        # Dual curved white PTFE tubes arching gracefully into the ceiling
        for tube_x in (-0.018, 0.018):
            for seg in range(7):
                t_frac = seg / 6.0
                pz = -0.006 + t_frac * 0.165
                py = -0.015 + t_frac * 0.055
                px = tube_x * (1.0 - t_frac * 0.35)
                self.add_cylinder("printHead", f"ptfe_tube_{tube_x}_{seg}", (px, py, pz), 0.003, 0.025, "z", ptfe_white)

        # -------------------------------------------------------------
        # 6. PRINTED CARBON FIBER MECHANICAL ARM (`printedObject`)
        # Spans exactly from Z = -0.128 (PEI bed) to Z = +0.038 (top layer).
        # Total height: 0.166m (166mm), occupying ~60% build height.
        # Matches Doop Canvas: lower right pivot, diagonal spar, hollow pocket,
        # upper cantilever boss and ear.
        # -------------------------------------------------------------
        # 1. Base mounting foot bolted to PEI bed (Z: -0.128 to -0.108)
        self.add_box("printedObject", "arm_base_foot", (0.045, -0.020, -0.118), (0.095, 0.065, 0.020), carbon_fiber)
        # 2. Lower cylindrical pivot boss (Z: -0.120 to -0.065)
        self.add_cylinder("printedObject", "arm_base_pivot", (0.068, -0.020, -0.092), 0.028, 0.055, "y", carbon_fiber)
        self.add_cylinder("printedObject", "arm_base_bore",  (0.068, -0.020, -0.092), 0.014, 0.058, "y", dark_chassis)
        # 3. Main angled structural spar ascending diagonally to upper left (Z: -0.095 to +0.020)
        self.add_box("printedObject", "arm_main_spar", (0.012, -0.020, -0.038), (0.135, 0.042, 0.115), carbon_fiber)
        # 4. Internal weight-reduction pocket cutout (hollow truss)
        self.add_box("printedObject", "arm_pocket_cutout", (0.015, -0.020, -0.038), (0.068, 0.045, 0.058), dark_chassis)
        # 5. Upper cantilever arm flange (Z: -0.010 to +0.025)
        self.add_box("printedObject", "arm_upper_flange", (-0.035, -0.020, 0.008), (0.075, 0.038, 0.035), carbon_fiber)
        # 6. Upper pivot mounting boss (Z: -0.002 to +0.046)
        self.add_cylinder("printedObject", "arm_top_pivot", (-0.052, -0.020, 0.022), 0.024, 0.048, "y", carbon_fiber)
        self.add_cylinder("printedObject", "arm_top_bore",  (-0.052, -0.020, 0.022), 0.012, 0.052, "y", dark_chassis)
        # 7. Top mounting ear (Z: +0.028 to +0.040) - finish layer
        self.add_box("printedObject", "arm_top_ear", (-0.015, -0.020, 0.034), (0.055, 0.032, 0.012), carbon_fiber)

        # -------------------------------------------------------------
        # 7. TREE SUPPORT STRUCTURE (`treeSupport`)
        # Organic tree support columns branching up to support cantilever overhang
        # Spans Z = -0.128 to Z = +0.020
        # -------------------------------------------------------------
        # Base brim raft on PEI sheet
        self.add_box("treeSupport", "tree_base_raft", (-0.045, -0.020, -0.126), (0.110, 0.075, 0.004), tree_support)
        # Main vertical tree trunks
        self.add_cylinder("treeSupport", "tree_trunk_A",   (-0.065, -0.020, -0.065), 0.010, 0.120, "z", tree_support)
        self.add_cylinder("treeSupport", "tree_branch_A1", (-0.055, -0.030, 0.002),  0.007, 0.038, "z", tree_support)
        self.add_cylinder("treeSupport", "tree_branch_A2", (-0.072, -0.010, 0.002),  0.007, 0.038, "z", tree_support)
        # Secondary tree trunks
        self.add_cylinder("treeSupport", "tree_trunk_B",   (-0.025, -0.038, -0.078), 0.009, 0.095, "z", tree_support)
        self.add_cylinder("treeSupport", "tree_branch_B1", (-0.025, -0.032, -0.018), 0.006, 0.035, "z", tree_support)
        self.add_cylinder("treeSupport", "tree_trunk_C",   (-0.025, -0.002, -0.078), 0.009, 0.095, "z", tree_support)
        self.add_cylinder("treeSupport", "tree_branch_C1", (-0.025, -0.008, -0.018), 0.006, 0.035, "z", tree_support)
        # Tree interface contact tips
        self.add_box("treeSupport", "tree_pad_1", (-0.055, -0.030, 0.018),  (0.016, 0.016, 0.004), tree_support)
        self.add_box("treeSupport", "tree_pad_2", (-0.072, -0.010, 0.018),  (0.016, 0.016, 0.004), tree_support)
        self.add_box("treeSupport", "tree_pad_3", (-0.025, -0.020, -0.002), (0.022, 0.035, 0.004), tree_support)

    def export(self, out_path: Path):
        self.build_scene()
        for node in self.nodes:
            if "children" in node and not node["children"]:
                del node["children"]

        root_indices = [i for i, n in enumerate(self.nodes) if n.get("name") in [
            "enclosure", "door", "printHead", "printBed", "gantryX", "gantryY", "printedObject", "treeSupport", "spools"
        ]]

        gltf = {
            "asset": {"generator": "Detailed Industrial CoreXY GLB Builder", "version": "2.1"},
            "scene": 0,
            "scenes": [{"name": "Deltrol Industrial P2S Scene", "nodes": root_indices}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "textures": self.textures,
            "images": self.images,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
            "accessors": self.accessors,
            "bufferViews": self.buffer_views,
            "buffers": [{"byteLength": len(self.bin)}],
        }

        json_bytes = json.dumps(gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        while len(json_bytes) % 4 != 0:
            json_bytes += b" "

        self.align()
        total_len = 12 + 8 + len(json_bytes) + 8 + len(self.bin)
        glb = bytearray()
        glb.extend(struct.pack("<4sII", b"glTF", 2, total_len))
        glb.extend(struct.pack("<II", len(json_bytes), 0x4E4F534A)) # JSON
        glb.extend(json_bytes)
        glb.extend(struct.pack("<II", len(self.bin), 0x004E4942))   # BIN
        glb.extend(self.bin)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(glb)
        print(f"Exported detailed industrial GLB to {out_path} ({len(glb)} bytes)")

if __name__ == "__main__":
    builder = DetailedGLBBuilder(cylinder_segments=24)
    builder.export(OPT_PATH)
    # Also copy to website public
    builder2 = DetailedGLBBuilder(cylinder_segments=24)
    builder2.export(PUB_PATH)
