#!/usr/bin/env python3
"""
build_p2s_photoreal_2p5d_depth_glb.py
Generates a clean, photoreal 2.5D Single-View Depth glTF 2.0 binary (.glb) asset
for the Deltrol P2S 3D Printer.

Features:
- True alpha blend photoreal facade (zero white rectangular borders).
- Distinct front glass door window only (no full-plane overlay).
- 3D physical door handle, volumetric chassis casing, and rubber feet.
- 5/5 required contract nodes: enclosure, door, front_glass_door, printHead, printBed.
- Fully compatible with glb-repair-harness.ps1 and glTF 2.0 specification.
"""

import io
import json
import math
import struct
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_RAW = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_photoreal_2p5d_depth.glb"
HERO_PNG = ROOT / "website" / "public" / "hero_architectural_printer.png"

class GlbBuilder:
    def __init__(self):
        self.bin = bytearray()
        self.buffer_views = []
        self.accessors = []
        self.meshes = []
        self.nodes = []
        self.materials = []
        self.images = []
        self.textures = []
        self.parents = {}
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

    def add_material(self, name, rgba, metallic=0.1, roughness=0.5, alpha_mode="OPAQUE", texture_img=None):
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
        self.images.append({"bufferView": image_view, "mimeType": "image/png", "name": f"{name} Image"})

        texture_index = len(self.textures)
        self.textures.append({"sampler": 0, "source": image_index, "name": f"{name} Texture"})

        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [1.0, 1.0, 1.0, rgba[3] / 255.0],
                "baseColorTexture": {"index": texture_index},
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "alphaMode": alpha_mode,
            "doubleSided": True,
        }
        if alpha_mode == "MASK":
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

    def add_parent(self, name, translation=(0, 0, 0)):
        idx = len(self.nodes)
        self.nodes.append({"name": name, "children": [], "translation": list(translation)})
        self.parents[name] = idx
        return idx

    def add_child_node(self, parent_name, name, mesh_index, translation=(0, 0, 0)):
        idx = len(self.nodes)
        node = {"name": name, "mesh": mesh_index}
        if any(translation):
            node["translation"] = list(translation)
        self.nodes.append(node)
        self.nodes[self.parents[parent_name]]["children"].append(idx)
        return idx

    def add_quad(self, parent_name, mesh_name, p0, p1, p2, p3, material_index, normal=(0, 0, 1)):
        positions = [*p0, *p1, *p2, *p0, *p2, *p3]
        normals = [*normal, *normal, *normal, *normal, *normal, *normal]
        uvs = [0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
        indices = [0, 1, 2, 3, 4, 5]
        mesh_index = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        self.add_child_node(parent_name, mesh_name, mesh_index)

    def add_box(self, parent_name, mesh_name, center, size, material_index):
        cx, cy, cz = center
        sx, sy, sz = [s / 2.0 for s in size]
        faces = [
            # Front (+y in GLB space is front)
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

    def add_cylinder(self, parent_name, mesh_name, center, radius, height, axis, material_index, segments=16):
        cx, cy, cz = center
        h_half = height / 2.0
        positions, normals, uvs, indices = [], [], [], []
        for i in range(segments + 1):
            theta = (2.0 * math.pi * i) / segments
            c = math.cos(theta)
            s = math.sin(theta)
            u = i / float(segments)
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

        for i in range(segments):
            v0 = i * 2
            v1 = v0 + 1
            v2 = (i + 1) * 2
            v3 = v2 + 1
            indices.extend([v0, v2, v1, v1, v2, v3])

        mesh_index = self.add_mesh_primitive(mesh_name, positions, normals, uvs, indices, material_index)
        self.add_child_node(parent_name, mesh_name, mesh_index)

    def build(self):
        # 1. Load Photoreal Hero Texture
        hero_img = Image.open(HERO_PNG).convert("RGBA")
        print(f"Loaded hero texture: {hero_img.size}")

        # 2. Materials
        # Facade: Photoreal Alpha Blend Texture (ZERO white background)
        mat_photoreal_facade = self.add_material(
            "Photoreal_Facade_PBR",
            (255, 255, 255, 255),
            metallic=0.15,
            roughness=0.35,
            alpha_mode="BLEND",
            texture_img=hero_img
        )

        # Titanium Unibody Backing
        mat_titanium = self.add_material("Titanium Depth Casing", (174, 180, 186, 255), metallic=0.82, roughness=0.28)
        # Dark Interior Cavity
        mat_cavity = self.add_material("Chassis Dark Depth", (28, 32, 38, 255), metallic=0.45, roughness=0.48)
        # Silver Handle
        mat_handle = self.add_material("Silver Handle Bar", (220, 224, 230, 255), metallic=0.92, roughness=0.15)
        # Smoked Door Window Glass (ONLY for door window)
        mat_glass = self.add_material("Smoked Door Glass", (18, 22, 26, 75), metallic=0.45, roughness=0.06, alpha_mode="BLEND")
        # Gold PEI Bed
        mat_pei = self.add_material("Gold PEI Bed", (216, 165, 54, 255), metallic=0.65, roughness=0.35)
        # Carbon Fiber Toolhead
        mat_toolhead = self.add_material("PA-CF Toolhead", (35, 38, 44, 255), metallic=0.25, roughness=0.40)

        # 3. Create Root Contract Parents
        self.add_parent("enclosure")
        self.add_parent("door")
        self.add_parent("front_glass_door")
        self.add_parent("printBed")
        self.add_parent("printHead")

        # 4. Primary Photoreal Facade
        # In GLB coordinates (where X=right, Y=front, Z=up):
        # Center of printer in GLB space:
        center_glb = np.array([-0.064, -0.038, -0.011])
        w_m = 0.596
        h_m = 0.553

        # Basis vectors aligned with camera view angle:
        u_glb = np.array([0.8675, 0.4974, 0.0])
        v_glb = np.array([-0.0628, 0.1095, 0.8857])
        forward_glb = np.array([-0.4934, 0.8606, -0.1127])
        billboard_norm = (-forward_glb / np.linalg.norm(forward_glb)).tolist()

        p_bl = center_glb - 0.5 * w_m * u_glb - 0.5 * h_m * v_glb
        p_br = center_glb + 0.5 * w_m * u_glb - 0.5 * h_m * v_glb
        p_tr = center_glb + 0.5 * w_m * u_glb + 0.5 * h_m * v_glb
        p_tl = center_glb - 0.5 * w_m * u_glb + 0.5 * h_m * v_glb

        # Add Photoreal Facade to 'enclosure'
        self.add_quad(
            "enclosure",
            "photoreal_facade_layer",
            p_bl.tolist(),
            p_br.tolist(),
            p_tr.tolist(),
            p_tl.tolist(),
            mat_photoreal_facade,
            normal=billboard_norm
        )

        # 5. Volumetric Depth Shell (Behind facade)
        depth_offset = forward_glb * 0.04
        c_depth = center_glb + depth_offset

        # Chassis volumetric backing: dark titanium box placed behind
        self.add_box("enclosure", "chassis_depth_backing", (c_depth[0], c_depth[1] + 0.04, c_depth[2]), (0.28, 0.24, 0.30), mat_titanium)
        self.add_box("enclosure", "chassis_cavity_interior", (c_depth[0], c_depth[1] + 0.02, c_depth[2]), (0.26, 0.22, 0.28), mat_cavity)

        # Base Plinth & Rubber Feet for Ground Contact
        base_z = -0.27 / 1.12
        self.add_box("enclosure", "base_plinth_ground", (center_glb[0], center_glb[1] + 0.03, base_z + 0.012), (0.28, 0.26, 0.018), mat_titanium)
        for fx in (-0.14, 0.14):
            for fy in (-0.14, 0.14):
                self.add_cylinder("enclosure", f"rubber_foot_{fx}_{fy}", (center_glb[0] + fx, center_glb[1] + fy, base_z), 0.015, 0.012, "z", mat_cavity)

        # 6. Door & Front Glass Window (ONLY inside door frame area, NOT entire bounding box)
        # Door Window: positioned slightly in front of facade, specifically in the front opening aperture
        door_center = center_glb - forward_glb * 0.008 + 0.02 * v_glb - 0.02 * u_glb
        w_glass = 0.24
        h_glass = 0.30
        g_bl = door_center - 0.5 * w_glass * u_glb - 0.5 * h_glass * v_glb
        g_br = door_center + 0.5 * w_glass * u_glb - 0.5 * h_glass * v_glb
        g_tr = door_center + 0.5 * w_glass * u_glb + 0.5 * h_glass * v_glb
        g_tl = door_center - 0.5 * w_glass * u_glb + 0.5 * h_glass * v_glb

        self.add_quad(
            "front_glass_door",
            "front_glass_window",
            g_bl.tolist(),
            g_br.tolist(),
            g_tr.tolist(),
            g_tl.tolist(),
            mat_glass,
            normal=billboard_norm
        )

        # 3D Physical Silver Door Handle on Right Stile
        handle_pos = door_center + 0.5 * w_glass * u_glb + 0.015 * u_glb - forward_glb * 0.010
        self.add_cylinder("door", "door_handle_bar", handle_pos.tolist(), 0.0045, 0.140, "z", mat_handle)
        self.add_cylinder("door", "door_handle_top_post", (handle_pos + [0, 0, 0.060]).tolist(), 0.0035, 0.016, "y", mat_handle)
        self.add_cylinder("door", "door_handle_bot_post", (handle_pos - [0, 0, 0.060]).tolist(), 0.0035, 0.016, "y", mat_handle)

        # 7. Print Bed (Contract Node) - inside chamber
        bed_pos = (center_glb[0] + depth_offset[0], center_glb[1] + depth_offset[1] + 0.01, -0.058)
        self.add_box("printBed", "gold_pei_build_plate", bed_pos, (0.21, 0.21, 0.008), mat_pei)

        # 8. Print Head (Contract Node) - CoreXY gantry position
        head_pos = (center_glb[0] + depth_offset[0], center_glb[1] + depth_offset[1] + 0.01, 0.040)
        self.add_box("printHead", "corexy_toolhead_body", head_pos, (0.052, 0.048, 0.044), mat_toolhead)

        # 9. Assembly & GLB Export
        root_children = [self.parents[name] for name in ["enclosure", "door", "front_glass_door", "printBed", "printHead"]]
        scene_node = len(self.nodes)
        self.nodes.append({"name": "Scene_Root", "children": root_children})

        gltf = {
            "asset": {"version": "2.0", "generator": "Deltrol Photoreal 2.5D GLB Builder"},
            "scene": 0,
            "scenes": [{"name": "Scene", "nodes": [scene_node]}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "textures": self.textures,
            "images": self.images,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
            "accessors": self.accessors,
            "bufferViews": self.buffer_views,
            "buffers": [{"byteLength": len(self.bin)}],
        }

        json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
        while len(json_bytes) % 4:
            json_bytes += b" "

        while len(self.bin) % 4:
            self.bin.append(0)

        total_length = 12 + 8 + len(json_bytes) + 8 + len(self.bin)
        header = struct.pack("<4sII", b"glTF", 2, total_length)
        json_chunk_header = struct.pack("<II", len(json_bytes), 0x4E4F534A)
        bin_chunk_header = struct.pack("<II", len(self.bin), 0x004E4942)

        glb_data = header + json_chunk_header + json_bytes + bin_chunk_header + bytes(self.bin)

        OUT_RAW.parent.mkdir(parents=True, exist_ok=True)
        OUT_RAW.write_bytes(glb_data)
        print(f"Exported photoreal 2.5D GLB: {OUT_RAW} ({len(glb_data):,} bytes)")

if __name__ == "__main__":
    builder = GlbBuilder()
    builder.build()
