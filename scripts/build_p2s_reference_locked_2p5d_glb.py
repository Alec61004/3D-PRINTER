import io
import json
import math
import struct
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_reference_locked_2p5d.glb"
OPT_PATH = ROOT / "assets" / "models" / "optimized" / "deltrol_p2s_optimized.glb"
PUB_PATH = ROOT / "website" / "public" / "models" / "deltrol_p2s_optimized.glb"
HERO_PNG = ROOT / "website" / "public" / "hero_architectural_printer.png"

class ReferenceLockedGlbBuilder:
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
            material["extras"] = {"note": "Reference-Locked Alpha Blend Texture"}
        elif alpha_mode == "MASK":
            material["alphaCutoff"] = 0.05
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

    def add_child_node(self, parent_name, mesh_name, mesh_index, translation=(0, 0, 0)):
        node_index = len(self.nodes)
        node = {"name": mesh_name, "mesh": mesh_index}
        if translation != (0, 0, 0):
            node["translation"] = list(translation)
        self.nodes.append(node)
        if parent_name in self.parents:
            self.nodes[self.parents[parent_name]]["children"].append(node_index)
        return node_index

    def add_quad(self, parent_name, mesh_name, p_bl, p_br, p_tr, p_tl, material_index, normal=None):
        # Coordinates in GLB
        v0 = p_bl
        v1 = p_br
        v2 = p_tr
        v3 = p_tl
        positions = [
            v0[0], v0[1], v0[2],
            v1[0], v1[1], v1[2],
            v2[0], v2[1], v2[2],
            v3[0], v3[1], v3[2],
        ]
        if normal is None:
            e1 = np.array(v1) - np.array(v0)
            e2 = np.array(v3) - np.array(v0)
            n = np.cross(e1, e2)
            n_len = np.linalg.norm(n)
            normal = (n / n_len).tolist() if n_len > 1e-6 else [0, 0, 1]

        normals = normal * 4
        # Standard UV: (0,1) for BL, (1,1) for BR, (1,0) for TR, (0,0) for TL
        # In glTF, (0,0) is top-left, (1,1) is bottom-right!
        uvs = [
            0.0, 1.0,  # BL
            1.0, 1.0,  # BR
            1.0, 0.0,  # TR
            0.0, 0.0,  # TL
        ]
        indices = [0, 1, 2, 0, 2, 3]
        mesh_index = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        self.add_child_node(parent_name, mesh_name, mesh_index)

    def add_box(self, parent_name, mesh_name, center, size, material_index):
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
            uvs.extend([0, 1, 1, 1, 1, 0, 0, 0])
            indices.extend([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
            idx += 4

        mesh_index = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        self.add_child_node(parent_name, mesh_name, mesh_index)

    def add_cylinder(self, parent_name, mesh_name, center, radius, height, axis, material_index):
        cx, cy, cz = center
        h_half = height / 2.0
        n_seg = self.cylinder_segments
        positions, normals, uvs, indices = [], [], [], []

        for i in range(n_seg + 1):
            theta = (2.0 * math.pi * i) / n_seg
            c = math.cos(theta)
            s = math.sin(theta)
            u = i / float(n_seg)
            if axis == "z":
                positions.extend([cx + radius * c, cy + radius * s, cz - h_half])
                positions.extend([cx + radius * c, cy + radius * s, cz + h_half])
                normals.extend([c, s, 0])
                normals.extend([c, s, 0])
            elif axis == "y":
                positions.extend([cx + radius * c, cy - h_half, cz + radius * s])
                positions.extend([cx + radius * c, cy + h_half, cz + radius * s])
                normals.extend([c, 0, s])
                normals.extend([c, 0, s])
            else: # x
                positions.extend([cx - h_half, cy + radius * c, cz + radius * s])
                positions.extend([cx + h_half, cy + radius * c, cz + radius * s])
                normals.extend([0, c, s])
                normals.extend([0, c, s])
            uvs.extend([u, 1.0, u, 0.0])

        for i in range(n_seg):
            v0 = i * 2
            v1 = v0 + 1
            v2 = (i + 1) * 2
            v3 = v2 + 1
            indices.extend([v0, v2, v1, v1, v2, v3])

        mesh_index = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        self.add_child_node(parent_name, mesh_name, mesh_index)

    def build_scene(self):
        # 1. Load Photoreal Reference Texture
        hero_img = Image.open(HERO_PNG).convert("RGBA")
        print(f"Loaded reference hero texture: {hero_img.size}")

        # 2. Materials
        # RefLocked Photoreal Texture Material (Calibrated to cancel Three.js ambient+studio light gain)
        mat_reflocked = self.add_material(
            "RefLocked_Photoreal_Chassis",
            (172, 168, 162, 255),
            metallic=0.08,
            roughness=0.45,
            alpha_mode="MASK",
            texture_img=hero_img
        )

        # Titanium Frame Depth Material
        mat_titanium = self.add_material("Titanium Depth Casing", (174, 180, 186, 255), metallic=0.82, roughness=0.28)
        # Dark Chassis Interior
        mat_dark_chassis = self.add_material("Chassis Dark Depth", (26, 29, 34, 255), metallic=0.45, roughness=0.48)
        # Smoked Optical Glass
        mat_smoked_glass = self.add_material("Smoked Optical Glass", (18, 22, 26, 90), metallic=0.42, roughness=0.08, alpha_mode="BLEND")
        # Gold Textured PEI
        mat_gold_pei = self.add_material("Gold Textured PEI", (216, 165, 54, 255), metallic=0.65, roughness=0.35)
        # Polished Aluminum / Titanium Handle
        mat_handle = self.add_material("Polished Aluminum", (219, 224, 230, 255), metallic=0.90, roughness=0.16)
        # Carbon Fiber PA-CF
        mat_carbon = self.add_material("PA-CF Carbon Fiber", (38, 41, 47, 255), metallic=0.25, roughness=0.38)
        # Brass Nozzle
        mat_brass = self.add_material("Brass Nozzle", (226, 175, 52, 255), metallic=0.92, roughness=0.18)

        # 3. Create Root Contract Parents
        self.add_parent("enclosure")
        self.add_parent("door")
        self.add_parent("front_glass_door")
        self.add_parent("printBed")
        self.add_parent("printHead")

        # -------------------------------------------------------------
        # 4. PRIMARY REFERENCE-LOCKED BILLBOARD
        # -------------------------------------------------------------
        # Exactly derived camera basis & projection math:
        # Camera in Three.js: [0.86, 0.22, 1.50], fov 27 deg
        # Target pixel bbox on 1226x708 viewport: (618, 152, 1074, 575)
        center_glb = np.array([-0.06445052, -0.03875908, -0.01100312])
        w_m = 0.596297
        h_m = 0.553144

        u_glb = np.array([0.86753043, 0.49738411, 0.0])
        v_glb = np.array([-0.06277991, 0.10949985, 0.88571629])

        # Direction vector from camera towards model in GLB space
        # Three.js camera to target forward is [-0.4934, -0.1262, -0.8606]
        # In GLB: [forward[0], -forward[2], forward[1] / 1.12]
        forward_glb = np.array([-0.49340616, 0.86059214, -0.11269659])

        # Normal of billboard points towards camera (opposite of forward)
        billboard_norm = (-forward_glb / np.linalg.norm(forward_glb)).tolist()

        p_bl = center_glb - 0.5 * w_m * u_glb - 0.5 * h_m * v_glb
        p_br = center_glb + 0.5 * w_m * u_glb - 0.5 * h_m * v_glb
        p_tr = center_glb + 0.5 * w_m * u_glb + 0.5 * h_m * v_glb
        p_tl = center_glb - 0.5 * w_m * u_glb + 0.5 * h_m * v_glb

        self.add_quad(
            "enclosure",
            "reflocked_hero_billboard",
            p_bl.tolist(),
            p_br.tolist(),
            p_tr.tolist(),
            p_tl.tolist(),
            mat_reflocked,
            normal=billboard_norm
        )

        # -------------------------------------------------------------
        # 5. VOLUMETRIC DEPTH SHELL & CHASSIS (behind billboard)
        # -------------------------------------------------------------
        # Depth offset: displace slightly deeper along forward_glb
        # Provides solid 3D backing when orbiting camera
        depth_offset = forward_glb * 0.05
        depth_center = center_glb + depth_offset

        # Bounding box of physical chassis (completely contained behind billboard at hero angle)
        self.add_box("enclosure", "chassis_depth_backing", (depth_center[0], depth_center[1] + 0.05, depth_center[2]), (0.28, 0.26, 0.32), mat_titanium)
        self.add_box("enclosure", "interior_cavity_dark", (depth_center[0], depth_center[1] + 0.02, depth_center[2]), (0.26, 0.24, 0.30), mat_dark_chassis)

        # Base plinth resting at bottom to cast contact shadow
        base_z = -0.27 / 1.12  # in GLB local Z
        self.add_box("enclosure", "base_plinth_ground", (center_glb[0], center_glb[1] + 0.04, base_z + 0.015), (0.28, 0.28, 0.02), mat_titanium)
        for fx in (-0.16, 0.16):
            for fy in (-0.16, 0.16):
                self.add_cylinder("enclosure", f"rubber_foot_{fx}_{fy}", (center_glb[0] + fx, center_glb[1] + fy, base_z), 0.016, 0.014, "z", mat_dark_chassis)

        # -------------------------------------------------------------
        # 6. DOOR & FRONT GLASS (Contract Nodes)
        # -------------------------------------------------------------
        # Door handle located at right stile
        handle_pos = center_glb + 0.20 * u_glb - 0.02 * v_glb - forward_glb * 0.01
        self.add_cylinder("door", "door_handle", handle_pos.tolist(), 0.005, 0.150, "z", mat_handle)
        self.add_cylinder("door", "door_handle_top_post", (handle_pos + [0, 0, 0.065]).tolist(), 0.004, 0.018, "y", mat_handle)
        self.add_cylinder("door", "door_handle_bot_post", (handle_pos - [0, 0, 0.065]).tolist(), 0.004, 0.018, "y", mat_handle)

        # Front glass door: subtle optical transmission quad in front of cavity
        glass_p_bl = p_bl + forward_glb * 0.01
        glass_p_br = p_br + forward_glb * 0.01
        glass_p_tr = p_tr + forward_glb * 0.01
        glass_p_tl = p_tl + forward_glb * 0.01
        self.add_quad(
            "front_glass_door",
            "front_glass_panel",
            glass_p_bl.tolist(),
            glass_p_br.tolist(),
            glass_p_tr.tolist(),
            glass_p_tl.tolist(),
            mat_smoked_glass,
            normal=billboard_norm
        )

        # -------------------------------------------------------------
        # 7. PRINT BED (`printBed`)
        # -------------------------------------------------------------
        bed_center = center_glb + forward_glb * 0.04 - [0, 0, 0.08]
        self.add_box("printBed", "build_plate", (bed_center[0], bed_center[1], bed_center[2]), (0.24, 0.24, 0.012), mat_gold_pei)
        self.add_box("printBed", "bed_heater_block", (bed_center[0], bed_center[1], bed_center[2] - 0.015), (0.25, 0.25, 0.018), mat_dark_chassis)
        # Bracket printed object on bed
        self.add_box("printBed", "printed_bracket", (bed_center[0], bed_center[1], bed_center[2] + 0.035), (0.08, 0.08, 0.06), mat_carbon)

        # -------------------------------------------------------------
        # 8. PRINT HEAD & GANTRY (`printHead`)
        # -------------------------------------------------------------
        head_center = center_glb + forward_glb * 0.03 + [0, 0, 0.08]
        self.add_box("printHead", "toolhead_housing", (head_center[0], head_center[1], head_center[2]), (0.075, 0.075, 0.085), mat_carbon)
        self.add_cylinder("printHead", "fan_left", (head_center[0] - 0.018, head_center[1] - 0.038, head_center[2]), 0.014, 0.004, "y", mat_dark_chassis)
        self.add_cylinder("printHead", "fan_right", (head_center[0] + 0.018, head_center[1] - 0.038, head_center[2]), 0.014, 0.004, "y", mat_dark_chassis)
        self.add_cylinder("printHead", "nozzle_brass", (head_center[0], head_center[1], head_center[2] - 0.048), 0.004, 0.014, "z", mat_brass)

    def export(self, out_path):
        self.build_scene()
        for node in self.nodes:
            if "children" in node and not node["children"]:
                del node["children"]

        root_indices = [i for i, n in enumerate(self.nodes) if n.get("name") in [
            "enclosure", "door", "front_glass_door", "printHead", "printBed"
        ]]

        gltf = {
            "asset": {"generator": "Antigravity Reference-Locked 2.5D GLB Builder", "version": "2.0"},
            "scene": 0,
            "scenes": [{"name": "Reference Locked Scene", "nodes": root_indices}],
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

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(glb)
        print(f"Exported Reference-Locked 2.5D GLB to {out_path} ({len(glb)} bytes)")

if __name__ == "__main__":
    builder = ReferenceLockedGlbBuilder(cylinder_segments=24)
    builder.export(RAW_PATH)
