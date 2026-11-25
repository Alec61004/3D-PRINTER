import io
import json
import math
import struct
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OPT_PATH = ROOT / "assets" / "models" / "optimized" / "deltrol_p2s_optimized.glb"
PUB_PATH = ROOT / "website" / "public" / "models" / "deltrol_p2s_optimized.glb"
RAW_PATH = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_photoreal_v1.glb"
TEX_DIR = ROOT / "assets" / "generated" / "antigravity" / "textures"

class PhotorealGLBBuilder:
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
            material["extras"] = {"note": "Smoked optical glass"}
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
            {"norm": (0, 1, 0), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            {"norm": (0, -1, 0), "quad": [(cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz)]},
            {"norm": (-1, 0, 0), "quad": [(cx - sx, cy - sy, cz - sz), (cx - sx, cy + sy, cz - sz), (cx - sx, cy + sy, cz + sz), (cx - sx, cy - sy, cz + sz)]},
            {"norm": (1, 0, 0), "quad": [(cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz)]},
            {"norm": (0, 0, 1), "quad": [(cx - sx, cy - sy, cz + sz), (cx + sx, cy - sy, cz + sz), (cx + sx, cy + sy, cz + sz), (cx - sx, cy + sy, cz + sz)]},
            {"norm": (0, 0, -1), "quad": [(cx - sx, cy + sy, cz - sz), (cx + sx, cy + sy, cz - sz), (cx + sx, cy - sy, cz - sz), (cx - sx, cy - sy, cz - sz)]},
        ]
        positions, normals, uvs, indices = [], [], [], []
        idx = 0
        for f in faces:
            nx, ny, nz = f["norm"]
            for vx, vy, vz in f["quad"]:
                positions.extend([vx, vy, vz])
                normals.extend([nx, ny, nz])
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
            else: # "x"
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
        base_cap = len(positions) // 3
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
        # Load external generated textures if available
        titanium_img = None
        gold_img = None
        carbon_img = None
        ui_img = None
        
        t_norm_p = TEX_DIR / "titanium_satin_albedo.png"
        g_pei_p = TEX_DIR / "gold_pei_albedo.png"
        c_fib_p = TEX_DIR / "carbon_fiber_diffuse.png"
        ui_p = TEX_DIR / "touchscreen_ui_decal.png"

        if t_norm_p.exists():
            titanium_img = Image.open(t_norm_p).convert("RGBA")
        if g_pei_p.exists():
            gold_img = Image.open(g_pei_p).convert("RGBA")
        if c_fib_p.exists():
            carbon_img = Image.open(c_fib_p).convert("RGBA")
        if ui_p.exists():
            ui_img = Image.open(ui_p).convert("RGBA")

        # -------------------------------------------------------------
        # PBR Materials matching Reference assets/source/printer-hero-reference-2026-11-23.png
        # -------------------------------------------------------------
        # Titanium Champagne Satin Unibody (#c2c6cc)
        titanium_satin = self.add_material("Titanium Satin Unibody", (198, 202, 208, 255), 0.55, 0.28, texture_img=titanium_img)
        # Inner dark chamber chassis (#202428)
        dark_chassis   = self.add_material("Chassis Matte Dark", (36, 40, 46, 255), 0.35, 0.45)
        # Structural graphite door frame (#32363e)
        graphite_frame = self.add_material("Graphite Door Frame", (50, 54, 62, 255), 0.45, 0.35)
        # Polished aluminum corner caps & handle (#e4e8ee)
        polished_alu   = self.add_material("Polished Aluminum", (228, 232, 238, 255), 0.88, 0.15)
        # Smoked optical glass (#18222a, opacity 0.32)
        smoked_glass   = self.add_material("Smoked Optical Glass", (24, 30, 38, 80), 0.15, 0.08, alpha_mode="BLEND")
        # Warm internal LED light
        interior_led   = self.add_material("Interior LED Glow", (255, 250, 235, 255), 0.10, 0.20, emissive=[1.0, 0.96, 0.88])
        # Gold PEI spring sheet
        gold_pei       = self.add_material("Gold Textured PEI", (223, 171, 44, 255), 0.75, 0.26, texture_img=gold_img)
        # PA-CF Carbon composite
        carbon_fiber   = self.add_material("PA-CF Carbon Fiber", (32, 34, 38, 255), 0.25, 0.40, texture_img=carbon_img)
        # Brass nozzle
        brass_nozzle   = self.add_material("Brass Nozzle", (230, 180, 40, 255), 0.92, 0.20)
        # Linear steel guide rails
        steel_rails    = self.add_material("Linear Guide Steel", (226, 230, 234, 255), 0.95, 0.12)
        # Rubber belts
        rubber_belt    = self.add_material("GT2 Timing Belt", (16, 18, 22, 255), 0.05, 0.85)

        # Touchscreen UI Decal
        screen_mat = self.add_material("Touchscreen UI", (255, 255, 255, 255), 0.0, 0.20, texture_img=ui_img)

        # Required parent nodes per contract
        for part in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]:
            self.add_parent(part)

        # -------------------------------------------------------------
        # 1. ENCLOSURE (Unibody Casing, thick rounded pillars, titanium satin)
        # Outer dimensions: W: 0.389m, D: 0.389m, H: 0.457m
        # -------------------------------------------------------------
        # Bottom plinth & tray
        self.add_box("enclosure", "base_plinth", (0, 0, -0.228), (0.389, 0.389, 0.024), titanium_satin)
        self.add_box("enclosure", "bottom_panel", (0, 0, -0.214), (0.380, 0.380, 0.008), dark_chassis)
        # Top rim & roof glass
        self.add_box("enclosure", "top_rim_outer", (0, 0, 0.222), (0.389, 0.389, 0.016), titanium_satin)
        self.add_box("enclosure", "top_roof_glass", (0, 0, 0.222), (0.320, 0.320, 0.008), smoked_glass)

        # Warm LED lighting bars along ceiling perimeter
        self.add_box("enclosure", "led_bar_front", (0, -0.145, 0.208), (0.310, 0.012, 0.006), interior_led)
        self.add_box("enclosure", "led_bar_left",  (-0.155, 0, 0.208), (0.012, 0.280, 0.006), interior_led)
        self.add_box("enclosure", "led_bar_right", (0.155, 0, 0.208),  (0.012, 0.280, 0.006), interior_led)

        # Vertical rounded unibody corner pillars (R = 24mm cylinders)
        # At (±0.170, ±0.170) to create seamless G2-like corner transitions
        for x in (-0.170, 0.170):
            for y in (-0.170, 0.170):
                self.add_cylinder("enclosure", f"corner_post_{x}_{y}", (x, y, 0), 0.024, 0.435, "z", titanium_satin)
                self.add_box("enclosure", f"corner_cap_top_{x}_{y}", (x, y, 0.220), (0.048, 0.048, 0.014), polished_alu)
                self.add_box("enclosure", f"corner_cap_bot_{x}_{y}", (x, y, -0.226), (0.048, 0.048, 0.014), polished_alu)

        # Front top header beam
        self.add_box("enclosure", "front_top_beam", (0, -0.180, 0.208), (0.340, 0.026, 0.038), titanium_satin)
        # Front bottom fascia & chin
        self.add_box("enclosure", "front_bot_fascia_left",  (-0.100, -0.180, -0.210), (0.140, 0.026, 0.040), titanium_satin)
        self.add_box("enclosure", "front_bot_fascia_right", ( 0.100, -0.180, -0.210), (0.140, 0.026, 0.040), titanium_satin)

        # Touchscreen Console embedded flush in front bottom fascia
        self.add_box("enclosure", "screen_bezel",   (0.070, -0.190, -0.210), (0.115, 0.010, 0.038), graphite_frame)
        self.add_box("enclosure", "screen_display", (0.070, -0.196, -0.210), (0.105, 0.004, 0.030), screen_mat)

        # Left side panel (solid titanium unibody with glass window cutout)
        self.add_box("enclosure", "left_wall_top",  (-0.182, 0, 0.190), (0.014, 0.340, 0.045), titanium_satin)
        self.add_box("enclosure", "left_wall_bot",  (-0.182, 0, -0.190), (0.014, 0.340, 0.055), titanium_satin)
        self.add_box("enclosure", "left_wall_front",(-0.182, -0.145, 0.005), (0.014, 0.050, 0.335), titanium_satin)
        self.add_box("enclosure", "left_wall_rear", (-0.182,  0.145, 0.005), (0.014, 0.050, 0.335), titanium_satin)
        self.add_box("enclosure", "left_glass_window", (-0.182, 0, 0.005), (0.006, 0.240, 0.335), smoked_glass)

        # Right side panel (wide optical smoked glass window viewing chamber)
        self.add_box("enclosure", "right_wall_top",  (0.182, 0, 0.190), (0.014, 0.340, 0.045), titanium_satin)
        self.add_box("enclosure", "right_wall_bot",  (0.182, 0, -0.190), (0.014, 0.340, 0.055), titanium_satin)
        self.add_box("enclosure", "right_wall_front",(0.182, -0.155, 0.005), (0.014, 0.030, 0.335), titanium_satin)
        self.add_box("enclosure", "right_wall_rear", (0.182,  0.155, 0.005), (0.014, 0.030, 0.335), titanium_satin)
        self.add_box("enclosure", "right_glass_window", (0.182, 0, 0.005), (0.006, 0.280, 0.335), smoked_glass)

        # Rear enclosure panel with ventilation slots
        self.add_box("enclosure", "rear_panel", (0, 0.182, 0), (0.340, 0.014, 0.435), dark_chassis)

        # -------------------------------------------------------------
        # 2. FRONT DOOR ASSEMBLY (`door`)
        # Contains smoked glass pane, graphite perimeter bezel, and vertical handle
        # -------------------------------------------------------------
        # Front smoked glass door (required contract: `front_glass_door`)
        self.add_box("door", "front_glass_door", (0.005, -0.186, 0.005), (0.318, 0.006, 0.370), smoked_glass)
        # Door frame stiles (graphite bezel)
        self.add_box("door", "door_left_stile",  (-0.150, -0.188, 0.005), (0.018, 0.008, 0.375), graphite_frame)
        self.add_box("door", "door_right_stile", ( 0.156, -0.188, 0.005), (0.022, 0.008, 0.375), graphite_frame)
        self.add_box("door", "door_top_rail",    ( 0.005, -0.188, 0.188), (0.318, 0.008, 0.016), graphite_frame)
        self.add_box("door", "door_bottom_rail", ( 0.005, -0.188,-0.178), (0.318, 0.008, 0.018), graphite_frame)
        # Vertical cylindrical door handle on right edge
        self.add_cylinder("door", "door_handle", (0.156, -0.200, 0.005), 0.006, 0.145, "z", polished_alu)
        self.add_box("door", "handle_standoff_top", (0.156, -0.194,  0.060), (0.010, 0.014, 0.010), polished_alu)
        self.add_box("door", "handle_standoff_bot", (0.156, -0.194, -0.050), (0.010, 0.014, 0.010), polished_alu)

        # -------------------------------------------------------------
        # 3. PRINT BED (`printBed`)
        # Heated aluminum plate with golden textured PEI flex sheet
        # -------------------------------------------------------------
        self.add_box("printBed", "build_plate", (0, 0.005, -0.126), (0.256, 0.256, 0.006), gold_pei)
        self.add_box("printBed", "bed_lip",     (0, -0.126, -0.126), (0.075, 0.012, 0.002), gold_pei)
        self.add_box("printBed", "bed_heater",  (0, 0.005, -0.134), (0.254, 0.254, 0.010), dark_chassis)
        self.add_box("printBed", "bed_carriage",(0, 0.005, -0.144), (0.230, 0.210, 0.012), dark_chassis)
        # Z-axis leadscrew brackets
        for x in (-0.115, 0.115):
            self.add_cylinder("printBed", f"bed_mount_{x}", (x, 0.080, -0.134), 0.007, 0.024, "z", steel_rails)

        # -------------------------------------------------------------
        # 4. GANTRY & COREXY MOTION (`gantryX`)
        # Parallel carbon/steel rods across X axis
        # -------------------------------------------------------------
        self.add_cylinder("gantryX", "x_guide_front", (0, -0.045, 0.145), 0.006, 0.285, "x", steel_rails)
        self.add_cylinder("gantryX", "x_guide_rear",  (0,  0.045, 0.145), 0.006, 0.285, "x", steel_rails)
        self.add_box("gantryX", "x_belt_front", (0, -0.055, 0.130), (0.295, 0.003, 0.003), rubber_belt)
        self.add_box("gantryX", "x_belt_rear",  (0,  0.055, 0.130), (0.295, 0.003, 0.003), rubber_belt)

        # -------------------------------------------------------------
        # 5. COREXY TOOLHEAD (`printHead`)
        # Aerodynamic dual-cooling fan toolhead housing in PA-CF carbon composite
        # Active brass nozzle tip at Z = -0.123 (touching PEI plate)
        # -------------------------------------------------------------
        self.add_box("printHead", "toolhead_body", (0, -0.010, -0.046), (0.082, 0.054, 0.075), dark_chassis)
        self.add_box("printHead", "toolhead_face", (0, -0.038, -0.046), (0.078, 0.006, 0.068), carbon_fiber)

        # Dual circular fan intake rings on toolhead front face
        for fx in (-0.020, 0.020):
            self.add_cylinder("printHead", f"fan_bezel_{fx}", (fx, -0.042, -0.042), 0.015, 0.003, "y", graphite_frame)
            self.add_cylinder("printHead", f"fan_hub_{fx}",   (fx, -0.044, -0.042), 0.006, 0.003, "y", polished_alu)

        # Active brass nozzle (Z: -0.110 to -0.123)
        self.add_cylinder("printHead", "nozzle", (0, -0.010, -0.115), 0.004, 0.018, "z", brass_nozzle)

        # Arched PTFE filament guide tube rising to ceiling
        for seg in range(6):
            t_frac = seg / 5.0
            pz = -0.005 + t_frac * 0.160
            py = -0.010 + t_frac * 0.050
            px = 0.010 * (1.0 - t_frac * 0.40)
            self.add_cylinder("printHead", f"ptfe_tube_{seg}", (px, py, pz), 0.0025, 0.025, "z", polished_alu)

        # -------------------------------------------------------------
        # 6. PRINTED PA-CF MECHANICAL BRACKET (`printedObject`)
        # Topology-optimized cantilever bracket on PEI sheet
        # -------------------------------------------------------------
        self.add_box("printedObject", "bracket_base",   (0.035, -0.015, -0.118), (0.085, 0.065, 0.016), carbon_fiber)
        self.add_cylinder("printedObject", "pivot_boss", (0.055, -0.015, -0.090), 0.024, 0.050, "y", carbon_fiber)
        self.add_cylinder("printedObject", "pivot_bore", (0.055, -0.015, -0.090), 0.012, 0.054, "y", dark_chassis)
        self.add_box("printedObject", "structural_spar", (0.010, -0.015, -0.040), (0.115, 0.038, 0.100), carbon_fiber)
        self.add_box("printedObject", "weight_pocket",   (0.012, -0.015, -0.040), (0.055, 0.042, 0.050), dark_chassis)
        self.add_box("printedObject", "upper_cantilever",(-0.025, -0.015, 0.005), (0.065, 0.034, 0.030), carbon_fiber)
        self.add_cylinder("printedObject", "upper_boss", (-0.040, -0.015, 0.018), 0.020, 0.040, "y", carbon_fiber)

    def export(self, out_paths):
        self.build_scene()
        for node in self.nodes:
            if "children" in node and not node["children"]:
                del node["children"]

        root_indices = [i for i, n in enumerate(self.nodes) if n.get("name") in [
            "enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"
        ]]

        gltf = {
            "asset": {"generator": "Antigravity P2S Photoreal GLB Builder v1", "version": "2.0"},
            "scene": 0,
            "scenes": [{"name": "Deltrol P2S Photoreal Scene", "nodes": root_indices}],
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
            print(f"Exported Photoreal GLB to {p} ({len(glb)} bytes)")

if __name__ == "__main__":
    builder = PhotorealGLBBuilder(cylinder_segments=32)
    builder.export([RAW_PATH, OPT_PATH, PUB_PATH])
