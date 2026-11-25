import io
import json
import math
import struct
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OPT_PATH = ROOT / "assets" / "models" / "optimized" / "deltrol_p2s_optimized.glb"
PUB_PATH = ROOT / "website" / "public" / "models" / "deltrol_p2s_optimized.glb"
RAW_PATH = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_photoreal_pivot.glb"
TEX_DIR = ROOT / "assets" / "generated" / "antigravity" / "textures"

class PhotorealPivotBuilder:
    def __init__(self, cylinder_segments=32):
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
            material["extras"] = {"note": "Photoreal Optical Smoked Glass"}
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

    def add_box(self, parent_name, mesh_name, center, size, material_index, custom_uvs=None):
        cx, cy, cz = center
        sx, sy, sz = [s / 2.0 for s in size]
        faces = [
            # Front (+y)
            {"norm": (0, 1, 0), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            # Back (-y)
            {"norm": (0, -1, 0), "quad": [(cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz)]},
            # Left (-x)
            {"norm": (-1, 0, 0), "quad": [(cx - sx, cy - sy, cz - sz), (cx - sx, cy + sy, cz - sz), (cx - sx, cy + sy, cz + sz), (cx - sx, cy - sy, cz + sz)]},
            # Right (+x)
            {"norm": (1, 0, 0), "quad": [(cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz)]},
            # Top (+z)
            {"norm": (0, 0, 1), "quad": [(cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            # Bottom (-z)
            {"norm": (0, 0, -1), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz)]},
        ]
        positions, normals, uvs, indices = [], [], [], []
        idx = 0
        for f in faces:
            nx, ny, nz = f["norm"]
            for vx, vy, vz in f["quad"]:
                positions.extend([vx, vy, vz])
                normals.extend([nx, ny, nz])
            if custom_uvs:
                uvs.extend(custom_uvs)
            else:
                uvs.extend([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0])
            indices.extend([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
            idx += 4

        mesh_idx = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        node_idx = len(self.nodes)
        self.nodes.append({"name": mesh_name, "mesh": mesh_idx})
        self.nodes[self.parents[parent_name]]["children"].append(node_idx)
        return node_idx

    def add_cylinder(self, parent_name, mesh_name, center, radius, length, axis, material_index):
        cx, cy, cz = center
        seg = self.cylinder_segments
        half = length / 2.0
        positions, normals, uvs, indices = [], [], [], []

        for i in range(seg + 1):
            theta = 2.0 * math.pi * (i / seg)
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            u = i / seg

            if axis == "z":
                nx, ny, nz = cos_t, sin_t, 0.0
                vx0, vy0, vz0 = cx + radius * cos_t, cy + radius * sin_t, cz - half
                vx1, vy1, vz1 = cx + radius * cos_t, cy + radius * sin_t, cz + half
            elif axis == "y":
                nx, ny, nz = cos_t, 0.0, sin_t
                vx0, vy0, vz0 = cx + radius * cos_t, cy - half, cz + radius * sin_t
                vx1, vy1, vz1 = cx + radius * cos_t, cy + half, cz + radius * sin_t
            else:
                nx, ny, nz = 0.0, cos_t, sin_t
                vx0, vy0, vz0 = cx - half, cy + radius * cos_t, cz + radius * sin_t
                vx1, vy1, vz1 = cx + half, cy + radius * cos_t, cz + radius * sin_t

            positions.extend([vx0, vy0, vz0, vx1, vy1, vz1])
            normals.extend([nx, ny, nz, nx, ny, nz])
            uvs.extend([u, 0.0, u, 1.0])

        for i in range(seg):
            idx0 = i * 2
            idx1 = idx0 + 1
            idx2 = idx0 + 2
            idx3 = idx0 + 3
            indices.extend([idx0, idx1, idx3, idx0, idx3, idx2])

        # Caps
        for cap_dir in (-1, 1):
            c_idx = len(positions) // 3
            cap_norm = [0.0, 0.0, 0.0]
            if axis == "z":
                cap_norm[2] = float(cap_dir)
                positions.extend([cx, cy, cz + cap_dir * half])
            elif axis == "y":
                cap_norm[1] = float(cap_dir)
                positions.extend([cx, cy + cap_dir * half, cz])
            else:
                cap_norm[0] = float(cap_dir)
                positions.extend([cx + cap_dir * half, cy, cz])

            normals.extend(cap_norm)
            uvs.extend([0.5, 0.5])

            for i in range(seg):
                theta = 2.0 * math.pi * (i / seg)
                cos_t = math.cos(theta)
                sin_t = math.sin(theta)
                if axis == "z":
                    positions.extend([cx + radius * cos_t, cy + radius * sin_t, cz + cap_dir * half])
                elif axis == "y":
                    positions.extend([cx + radius * cos_t, cy + cap_dir * half, cz + radius * sin_t])
                else:
                    positions.extend([cx + cap_dir * half, cy + radius * cos_t, cz + radius * sin_t])
                normals.extend(cap_norm)
                uvs.extend([0.5 + 0.5 * cos_t, 0.5 + 0.5 * sin_t])

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

    def build_scene(self):
        # 1. Load Photographic Rectified Textures
        t_albedo_p = TEX_DIR / "titanium_satin_v2_albedo.png"
        g_pei_p = TEX_DIR / "gold_pei_albedo.png"
        c_fib_p = TEX_DIR / "carbon_fiber_diffuse.png"
        u_p = TEX_DIR / "console_v2_ui.png"
        door_photo_p = TEX_DIR / "hero_door_photoreal.png"
        side_photo_p = TEX_DIR / "hero_side_photoreal.png"

        t_img = Image.open(t_albedo_p).convert("RGBA") if t_albedo_p.exists() else None
        g_img = Image.open(g_pei_p).convert("RGBA") if g_pei_p.exists() else None
        c_img = Image.open(c_fib_p).convert("RGBA") if c_fib_p.exists() else None
        u_img = Image.open(u_p).convert("RGBA") if u_p.exists() else None
        door_img = Image.open(door_photo_p).convert("RGBA") if door_photo_p.exists() else None
        side_img = Image.open(side_photo_p).convert("RGBA") if side_photo_p.exists() else None

        # 2. Materials
        # Photoreal unibody titan satin
        titanium_satin = self.add_material("Titanium Satin Unibody", (174, 180, 188, 255), 0.60, 0.25, texture_img=t_img)
        # Polished aerospace aluminum for bevels and handle
        polished_alu   = self.add_material("Polished Aluminum", (220, 224, 230, 255), 0.88, 0.16)
        # Inner dark graphite chamber chassis
        dark_chassis   = self.add_material("Chassis Matte Dark", (28, 32, 36, 255), 0.35, 0.45)
        # Graphite door perimeter bezel
        graphite_frame = self.add_material("Graphite Door Frame", (38, 42, 48, 255), 0.50, 0.30)
        # Photoreal front glass door with authentic reflection
        photoreal_door_glass = self.add_material("Photoreal Door Glass", (255, 255, 255, 255), 0.20, 0.08, texture_img=door_img, alpha_mode="BLEND")
        # Photoreal right side window
        photoreal_side_glass = self.add_material("Photoreal Side Glass", (255, 255, 255, 255), 0.18, 0.08, texture_img=side_img, alpha_mode="BLEND")
        # Top roof glass
        top_roof_glass = self.add_material("Smoked Optical Glass", (20, 26, 32, 60), 0.15, 0.06, alpha_mode="BLEND")
        # Warm internal LED light
        interior_led   = self.add_material("Interior LED Glow", (255, 250, 238, 255), 0.10, 0.20, emissive=[1.0, 0.96, 0.90])
        # Golden textured PEI sheet
        gold_pei       = self.add_material("Gold Textured PEI", (226, 178, 48, 255), 0.72, 0.25, texture_img=g_img)
        # Carbon fiber composite
        carbon_fiber   = self.add_material("PA-CF Carbon Fiber", (32, 34, 38, 255), 0.28, 0.40, texture_img=c_img)
        # Brass nozzle
        brass_nozzle   = self.add_material("Brass Nozzle", (232, 180, 42, 255), 0.92, 0.18)
        # Precision steel rails
        steel_rails    = self.add_material("Linear Guide Steel", (228, 232, 236, 255), 0.96, 0.10)
        # Rubber belts
        rubber_belt    = self.add_material("GT2 Timing Belt", (18, 20, 24, 255), 0.05, 0.85)
        # Touchscreen UI Decal
        screen_mat     = self.add_material("Touchscreen UI", (255, 255, 255, 255), 0.0, 0.15, texture_img=u_img)

        # Node hierarchy parents
        for part in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]:
            self.add_parent(part)

        # -------------------------------------------------------------
        # 1. ENCLOSURE (Unibody Casing, Pivot Dimensions)
        # Target: W: 0.365m, D: 0.365m, H: 0.408m
        # -------------------------------------------------------------
        # Bottom tray and base plinth
        self.add_box("enclosure", "base_plinth", (0, 0, -0.200), (0.365, 0.365, 0.020), titanium_satin)
        self.add_box("enclosure", "bottom_panel", (0, 0, -0.188), (0.355, 0.355, 0.008), dark_chassis)
        # Top outer rim and roof glass
        self.add_box("enclosure", "top_rim_outer", (0, 0, 0.200), (0.365, 0.365, 0.016), titanium_satin)
        self.add_box("enclosure", "top_roof_glass", (0, 0, 0.200), (0.295, 0.295, 0.008), top_roof_glass)

        # Interior warm LED ceiling bars
        self.add_box("enclosure", "led_bar_front", (0, -0.135, 0.188), (0.290, 0.010, 0.006), interior_led)
        self.add_box("enclosure", "led_bar_left",  (-0.145, 0, 0.188), (0.010, 0.260, 0.006), interior_led)
        self.add_box("enclosure", "led_bar_right", ( 0.145, 0, 0.188), (0.010, 0.260, 0.006), interior_led)

        # 4 Vertical rounded unibody corner pillars (R = 22mm cylinders)
        for x in (-0.160, 0.160):
            for y in (-0.160, 0.160):
                self.add_cylinder("enclosure", f"corner_post_{x}_{y}", (x, y, 0), 0.022, 0.384, "z", titanium_satin)
                self.add_box("enclosure", f"corner_cap_top_{x}_{y}", (x, y, 0.198), (0.044, 0.044, 0.014), polished_alu)
                self.add_box("enclosure", f"corner_cap_bot_{x}_{y}", (x, y, -0.198), (0.044, 0.044, 0.014), polished_alu)

        # Front top header beam
        self.add_box("enclosure", "front_top_beam", (0, -0.168, 0.186), (0.320, 0.022, 0.034), titanium_satin)
        # Front bottom fascia & chin
        self.add_box("enclosure", "front_bot_fascia_left",  (-0.090, -0.168, -0.186), (0.130, 0.022, 0.034), titanium_satin)
        self.add_box("enclosure", "front_bot_fascia_right", ( 0.090, -0.168, -0.186), (0.130, 0.022, 0.034), titanium_satin)

        # Touchscreen Console embedded flush in front bottom fascia
        self.add_box("enclosure", "screen_bezel",   (0.060, -0.176, -0.186), (0.105, 0.008, 0.032), graphite_frame)
        self.add_box("enclosure", "screen_display", (0.060, -0.182, -0.186), (0.098, 0.004, 0.026), screen_mat)

        # Left side panel
        self.add_box("enclosure", "left_wall_top",  (-0.170, 0, 0.172), (0.012, 0.320, 0.040), titanium_satin)
        self.add_box("enclosure", "left_wall_bot",  (-0.170, 0, -0.172), (0.012, 0.320, 0.048), titanium_satin)
        self.add_box("enclosure", "left_wall_front",(-0.170, -0.135, 0.005), (0.012, 0.045, 0.295), titanium_satin)
        self.add_box("enclosure", "left_wall_rear", (-0.170,  0.135, 0.005), (0.012, 0.045, 0.295), titanium_satin)
        self.add_box("enclosure", "left_glass_window", (-0.170, 0, 0.005), (0.005, 0.225, 0.295), top_roof_glass)

        # Right side panel (with Photoreal Side Window)
        self.add_box("enclosure", "right_wall_top",  (0.170, 0, 0.172), (0.012, 0.320, 0.040), titanium_satin)
        self.add_box("enclosure", "right_wall_bot",  (0.170, 0, -0.172), (0.012, 0.320, 0.048), titanium_satin)
        self.add_box("enclosure", "right_wall_front",(0.170, -0.142, 0.005), (0.012, 0.030, 0.295), titanium_satin)
        self.add_box("enclosure", "right_wall_rear", (0.170,  0.142, 0.005), (0.012, 0.030, 0.295), titanium_satin)
        self.add_box("enclosure", "right_glass_window", (0.170, 0, 0.005), (0.005, 0.255, 0.295), photoreal_side_glass)

        # Rear enclosure panel
        self.add_box("enclosure", "rear_panel", (0, 0.170, 0), (0.320, 0.012, 0.384), dark_chassis)

        # -------------------------------------------------------------
        # 2. FRONT DOOR ASSEMBLY (`door`)
        # -------------------------------------------------------------
        # Front Photoreal Glass Door
        self.add_box("door", "front_glass_door", (0.005, -0.174, 0.005), (0.298, 0.005, 0.335), photoreal_door_glass)
        self.add_box("door", "door_left_stile",  (-0.140, -0.176, 0.005), (0.016, 0.008, 0.338), graphite_frame)
        self.add_box("door", "door_right_stile", ( 0.145, -0.176, 0.005), (0.018, 0.008, 0.338), graphite_frame)
        self.add_box("door", "door_top_rail",    ( 0.005, -0.176, 0.170), (0.298, 0.008, 0.015), graphite_frame)
        self.add_box("door", "door_bottom_rail", ( 0.005, -0.176,-0.160), (0.298, 0.008, 0.015), graphite_frame)

        # Vertical cylindrical door handle on right stile
        self.add_cylinder("door", "door_handle", (0.145, -0.188, 0.010), 0.005, 0.150, "z", polished_alu)
        self.add_box("door", "handle_standoff_top", (0.145, -0.182,  0.065), (0.008, 0.012, 0.008), polished_alu)
        self.add_box("door", "handle_standoff_bot", (0.145, -0.182, -0.045), (0.008, 0.012, 0.008), polished_alu)

        # -------------------------------------------------------------
        # 3. PRINT BED (`printBed`)
        # -------------------------------------------------------------
        self.add_box("printBed", "build_plate", (0, 0.005, -0.115), (0.236, 0.236, 0.006), gold_pei)
        self.add_box("printBed", "bed_lip",     (0, -0.116, -0.115), (0.070, 0.010, 0.002), gold_pei)
        self.add_box("printBed", "bed_heater",  (0, 0.005, -0.122), (0.234, 0.234, 0.008), dark_chassis)
        self.add_box("printBed", "bed_carriage",(0, 0.005, -0.130), (0.210, 0.190, 0.010), dark_chassis)
        for x in (-0.105, 0.105):
            self.add_cylinder("printBed", f"bed_mount_{x}", (x, 0.075, -0.122), 0.006, 0.022, "z", steel_rails)

        # -------------------------------------------------------------
        # 4. GANTRY & COREXY MOTION (`gantryX`)
        # -------------------------------------------------------------
        self.add_cylinder("gantryX", "x_guide_front", (0, -0.040, 0.138), 0.0055, 0.265, "x", steel_rails)
        self.add_cylinder("gantryX", "x_guide_rear",  (0,  0.040, 0.138), 0.0055, 0.265, "x", steel_rails)
        self.add_box("gantryX", "x_belt_front", (0, -0.048, 0.125), (0.275, 0.003, 0.003), rubber_belt)
        self.add_box("gantryX", "x_belt_rear",  (0,  0.048, 0.125), (0.275, 0.003, 0.003), rubber_belt)

        # -------------------------------------------------------------
        # 5. COREXY TOOLHEAD (`printHead`)
        # -------------------------------------------------------------
        self.add_box("printHead", "toolhead_body", (0, -0.010, -0.040), (0.076, 0.050, 0.070), dark_chassis)
        self.add_box("printHead", "toolhead_face", (0, -0.036, -0.040), (0.072, 0.005, 0.064), carbon_fiber)

        for fx in (-0.018, 0.018):
            self.add_cylinder("printHead", f"fan_bezel_{fx}", (fx, -0.040, -0.038), 0.014, 0.003, "y", graphite_frame)
            self.add_cylinder("printHead", f"fan_hub_{fx}",   (fx, -0.042, -0.038), 0.005, 0.003, "y", polished_alu)

        self.add_cylinder("printHead", "nozzle", (0, -0.010, -0.105), 0.004, 0.016, "z", brass_nozzle)

        for seg in range(6):
            t_frac = seg / 5.0
            pz = -0.002 + t_frac * 0.150
            py = -0.010 + t_frac * 0.045
            px = 0.008 * (1.0 - t_frac * 0.40)
            self.add_cylinder("printHead", f"ptfe_tube_{seg}", (px, py, pz), 0.0025, 0.022, "z", polished_alu)

        # -------------------------------------------------------------
        # 6. PRINTED MECHANICAL BRACKET (`printedObject`)
        # -------------------------------------------------------------
        self.add_box("printedObject", "bracket_base",   (0.030, -0.012, -0.108), (0.078, 0.058, 0.014), carbon_fiber)
        self.add_cylinder("printedObject", "pivot_boss", (0.048, -0.012, -0.082), 0.022, 0.044, "y", carbon_fiber)
        self.add_cylinder("printedObject", "pivot_bore", (0.048, -0.012, -0.082), 0.011, 0.048, "y", dark_chassis)
        self.add_box("printedObject", "structural_spar", (0.008, -0.012, -0.035), (0.105, 0.034, 0.090), carbon_fiber)
        self.add_box("printedObject", "weight_pocket",   (0.010, -0.012, -0.035), (0.048, 0.038, 0.045), dark_chassis)
        self.add_box("printedObject", "upper_cantilever",(-0.022, -0.012, 0.005), (0.058, 0.030, 0.026), carbon_fiber)
        self.add_cylinder("printedObject", "upper_boss", (-0.036, -0.012, 0.016), 0.018, 0.035, "y", carbon_fiber)

    def export(self, out_paths):
        self.build_scene()
        for node in self.nodes:
            if "children" in node and not node["children"]:
                del node["children"]

        root_indices = [i for i, n in enumerate(self.nodes) if n.get("name") in [
            "enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"
        ]]

        gltf = {
            "asset": {"generator": "Antigravity P2S Photoreal Pivot GLB Builder", "version": "2.0"},
            "scene": 0,
            "scenes": [{"name": "Deltrol P2S Photoreal Pivot Scene", "nodes": root_indices}],
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
        glb.extend(struct.pack("<II", len(json_bytes), 0x4E4F534A))
        glb.extend(json_bytes)
        glb.extend(struct.pack("<II", len(self.bin), 0x004E4942))
        glb.extend(self.bin)

        for p in out_paths:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "wb") as f:
                f.write(glb)
            print(f"Exported Photoreal Pivot GLB to {p} ({len(glb)} bytes)")

if __name__ == "__main__":
    builder = PhotorealPivotBuilder(cylinder_segments=32)
    builder.export([RAW_PATH, OPT_PATH, PUB_PATH])
