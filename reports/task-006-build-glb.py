import io
import json
import math
import struct
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_source.glb"
OPT_PATH = ROOT / "assets" / "models" / "optimized" / "deltrol_p2s_optimized.glb"


class GLBBuilder:
    def __init__(self, cylinder_segments: int, variant: str):
        self.bin = bytearray()
        self.buffer_views = []
        self.accessors = []
        self.meshes = []
        self.nodes = []
        self.materials = []
        self.images = []
        self.textures = []
        self.parents = {}
        self.variant = variant
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

    def add_texture_material(self, name, rgba, metallic, roughness, alpha_mode="OPAQUE"):
        key = (name, tuple(rgba), metallic, roughness, alpha_mode)
        if key in self.material_cache:
            return self.material_cache[key]
        image = Image.new("RGBA", (4, 4), tuple(rgba))
        stream = io.BytesIO()
        image.save(stream, format="PNG", optimize=True)
        image_view = self.add_blob(stream.getvalue())
        image_index = len(self.images)
        self.images.append({"bufferView": image_view, "mimeType": "image/png", "name": f"{name} Texture"})
        texture_index = len(self.textures)
        self.textures.append({"sampler": 0, "source": image_index, "name": f"{name} Texture"})
        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [1, 1, 1, rgba[3] / 255],
                "baseColorTexture": {"index": texture_index},
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "alphaMode": alpha_mode,
            "doubleSided": True,
        }
        if alpha_mode == "BLEND":
            material["extras"] = {"note": "Smoked glass approximation; not a manufacturing material specification."}
        self.materials.append(material)
        index = len(self.materials) - 1
        self.material_cache[key] = index
        return index

    def add_box_mesh(self, name, center, size, material_index):
        cx, cy, cz = center
        sx, sy, sz = (v / 2 for v in size)
        faces = [
            ((0, 0, 1), [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]),
            ((0, 0, -1), [(-1, 1, -1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)]),
            ((0, 1, 0), [(-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1)]),
            ((0, -1, 0), [(1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1)]),
            ((1, 0, 0), [(1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1)]),
            ((-1, 0, 0), [(-1, -1, 1), (-1, 1, 1), (-1, 1, -1), (-1, -1, -1)]),
        ]
        positions, normals, uvs, indices = [], [], [], []
        for normal, corners in faces:
            start = len(positions) // 3
            for u, v, w in corners:
                positions.extend([cx + u * sx, cy + v * sy, cz + w * sz])
                normals.extend(normal)
                uvs.extend([(u + 1) / 2, (v + 1) / 2])
            indices.extend([start, start + 1, start + 2, start, start + 2, start + 3])
        return self.add_mesh(name, positions, normals, uvs, indices, material_index)

    def add_cylinder_mesh(self, name, center, radius, depth, axis, material_index):
        segments = self.cylinder_segments
        positions, normals, uvs, indices = [], [], [], []
        cx, cy, cz = center
        for ring in range(2):
            along = -depth / 2 + ring * depth
            for i in range(segments):
                a = 2 * math.pi * i / segments
                ca, sa = math.cos(a), math.sin(a)
                if axis == "x":
                    pos = (cx + along, cy + radius * ca, cz + radius * sa)
                    normal = (0, ca, sa)
                elif axis == "y":
                    pos = (cx + radius * ca, cy + along, cz + radius * sa)
                    normal = (ca, 0, sa)
                else:
                    pos = (cx + radius * ca, cy + radius * sa, cz + along)
                    normal = (ca, sa, 0)
                positions.extend(pos)
                normals.extend(normal)
                uvs.extend([i / segments, ring])
        for i in range(segments):
            j = (i + 1) % segments
            indices.extend([i, j, segments + j, i, segments + j, segments + i])
        return self.add_mesh(name, positions, normals, uvs, indices, material_index)

    def add_mesh(self, name, positions, normals, uvs, indices, material_index):
        pos_bytes = struct.pack(f"<{len(positions)}f", *positions)
        normal_bytes = struct.pack(f"<{len(normals)}f", *normals)
        uv_bytes = struct.pack(f"<{len(uvs)}f", *uvs)
        index_bytes = struct.pack(f"<{len(indices)}H", *indices)
        mins = [min(positions[i::3]) for i in range(3)]
        maxs = [max(positions[i::3]) for i in range(3)]
        pos_accessor = self.add_accessor(pos_bytes, 5126, len(positions) // 3, "VEC3", mins, maxs, 34962)
        norm_accessor = self.add_accessor(normal_bytes, 5126, len(normals) // 3, "VEC3", target=34962)
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

    def add_part(self, parent_name, name, mesh_index):
        node_index = len(self.nodes)
        self.nodes.append({"name": name, "mesh": mesh_index})
        self.nodes[self.parents[parent_name]]["children"].append(node_index)

    def add_box(self, parent, name, center, size, material):
        mesh = self.add_box_mesh(name, center, size, material)
        self.add_part(parent, name, mesh)

    def add_cylinder(self, parent, name, center, radius, depth, axis, material):
        mesh = self.add_cylinder_mesh(name, center, radius, depth, axis, material)
        self.add_part(parent, name, mesh)

    def build_scene(self):
        silver = self.add_texture_material("Silver Enclosure", (158, 166, 172, 255), 0.72, 0.25)
        dark = self.add_texture_material("Dark Polymer", (18, 23, 28, 255), 0.18, 0.34)
        glass = self.add_texture_material("Smoked Glass", (22, 34, 44, 218), 0.08, 0.14, "BLEND")
        steel = self.add_texture_material("Brushed Steel", (132, 140, 148, 255), 0.92, 0.22)
        bed = self.add_texture_material("PEI Build Plate", (20, 23, 25, 255), 0.1, 0.5)
        screen = self.add_texture_material("Screen Blue", (40, 145, 206, 255), 0.18, 0.18)
        orange = self.add_texture_material("Printed Object", (226, 104, 28, 255), 0.25, 0.38)
        rubber = self.add_texture_material("Belt Rubber", (10, 12, 14, 255), 0.05, 0.58)

        for part in ["enclosure", "door", "printHead", "printBed", "gantryX", "gantryY", "printedObject"]:
            self.add_parent(part)

        # Overall envelope: 0.40 m wide x 0.40 m deep x 0.50 m high; front is -Y.
        self.add_box("enclosure", "bottom_panel", (0, 0, -0.225), (0.40, 0.40, 0.02), silver)
        self.add_box("enclosure", "base_plinth", (0, -0.004, -0.242), (0.42, 0.42, 0.025), dark)
        self.add_box("enclosure", "base_front_fascia", (0, -0.211, -0.205), (0.39, 0.024, 0.052), dark)
        self.add_box("enclosure", "top_panel", (0, 0, 0.225), (0.40, 0.40, 0.02), silver)
        self.add_box("enclosure", "top_front_lip", (0, -0.207, 0.205), (0.39, 0.028, 0.038), dark)
        for x in (-0.19, 0.19):
            for y in (-0.19, 0.19):
                self.add_box("enclosure", f"corner_post_{x}_{y}", (x, y, 0), (0.024, 0.024, 0.43), silver)
        self.add_box("enclosure", "left_side_panel", (-0.198, 0, 0), (0.012, 0.35, 0.40), glass)
        self.add_box("enclosure", "right_side_panel", (0.198, 0, 0), (0.012, 0.35, 0.40), glass)
        self.add_box("enclosure", "rear_panel", (0, 0.198, 0), (0.36, 0.012, 0.40), silver)
        self.add_box("enclosure", "rear_fan_grille", (0, 0.191, 0.02), (0.15, 0.008, 0.15), dark)
        self.add_cylinder("enclosure", "rear_fan_hub", (0, 0.196, 0.02), 0.037, 0.008, "y", steel)
        for index, z in enumerate((-0.035, -0.012, 0.011, 0.034, 0.057)):
            self.add_box("enclosure", f"rear_fan_slot_{index}", (0, 0.198, z), (0.12, 0.006, 0.006), rubber)

        self.add_box("door", "front_glass_door", (0, -0.198, 0), (0.35, 0.012, 0.39), glass)
        self.add_box("door", "door_handle", (0.16, -0.214, 0), (0.012, 0.018, 0.17), dark)
        self.add_box("door", "door_left_stile", (-0.176, -0.216, 0), (0.018, 0.014, 0.39), dark)
        self.add_box("door", "door_right_stile", (0.176, -0.216, 0), (0.018, 0.014, 0.39), dark)
        self.add_box("door", "door_top_rail", (0, -0.216, 0.205), (0.35, 0.014, 0.018), dark)
        self.add_box("door", "door_bottom_rail", (0, -0.216, -0.205), (0.35, 0.014, 0.018), dark)
        self.add_box("door", "handle_mount_top", (0.16, -0.229, 0.073), (0.026, 0.018, 0.025), steel)
        self.add_box("door", "handle_mount_bottom", (0.16, -0.229, -0.073), (0.026, 0.018, 0.025), steel)

        self.add_box("printBed", "build_plate", (0, -0.015, -0.135), (0.31, 0.29, 0.016), bed)
        self.add_box("printBed", "bed_lip", (0, -0.164, -0.125), (0.30, 0.012, 0.018), steel)
        self.add_box("printBed", "bed_carriage", (0, 0.015, -0.165), (0.27, 0.24, 0.018), dark)
        for x in (-0.125, 0.125):
            for y in (-0.115, 0.115):
                self.add_cylinder("printBed", f"bed_mount_{x}_{y}", (x, y, -0.121), 0.006, 0.006, "z", steel)

        self.add_cylinder("gantryX", "x_guide_front", (0, -0.10, 0.145), 0.008, 0.29, "x", steel)
        self.add_cylinder("gantryX", "x_guide_rear", (0, 0.10, 0.145), 0.008, 0.29, "x", steel)
        self.add_box("gantryX", "x_belt_front", (0, -0.112, 0.125), (0.30, 0.006, 0.006), rubber)
        self.add_box("gantryX", "x_belt_rear", (0, 0.112, 0.125), (0.30, 0.006, 0.006), rubber)

        self.add_cylinder("gantryY", "y_guide_left", (-0.14, 0, 0.145), 0.007, 0.25, "y", steel)
        self.add_cylinder("gantryY", "y_guide_right", (0.14, 0, 0.145), 0.007, 0.25, "y", steel)
        self.add_cylinder("gantryY", "z_guide_left", (-0.14, 0.11, 0.0), 0.006, 0.31, "z", steel)
        self.add_cylinder("gantryY", "z_guide_right", (0.14, 0.11, 0.0), 0.006, 0.31, "z", steel)
        self.add_box("gantryY", "y_belt_left", (-0.152, 0, 0.125), (0.006, 0.26, 0.006), rubber)
        self.add_box("gantryY", "y_belt_right", (0.152, 0, 0.125), (0.006, 0.26, 0.006), rubber)
        self.add_box("gantryY", "left_carriage", (-0.14, 0, 0.145), (0.025, 0.035, 0.042), dark)
        self.add_box("gantryY", "right_carriage", (0.14, 0, 0.145), (0.025, 0.035, 0.042), dark)

        self.add_box("printHead", "toolhead_body", (0, -0.015, 0.105), (0.055, 0.045, 0.060), dark)
        self.add_box("printHead", "toolhead_face", (0, -0.041, 0.105), (0.040, 0.006, 0.038), steel)
        self.add_box("printHead", "toolhead_top", (0, -0.015, 0.139), (0.038, 0.036, 0.012), steel)
        self.add_box("printHead", "cooling_fan", (0, -0.046, 0.116), (0.026, 0.004, 0.026), rubber)
        self.add_cylinder("printHead", "nozzle", (0, -0.015, 0.060), 0.006, 0.035, "z", orange)
        self.add_box("printHead", "cable_chain_anchor", (0.035, 0.035, 0.105), (0.010, 0.035, 0.018), rubber)

        self.add_box("enclosure", "screen_bezel", (-0.145, -0.215, 0.155), (0.085, 0.012, 0.058), dark)
        self.add_box("enclosure", "screen_surface", (-0.145, -0.222, 0.155), (0.068, 0.006, 0.040), screen)
        self.add_box("enclosure", "screen_chin", (-0.145, -0.224, 0.119), (0.068, 0.006, 0.008), steel)
        self.add_box("enclosure", "interior_light", (0, -0.11, 0.19), (0.23, 0.012, 0.008), screen)
        self.add_box("enclosure", "power_switch", (0.155, 0.192, -0.155), (0.028, 0.010, 0.035), dark)
        self.add_box("enclosure", "power_socket", (0.112, 0.192, -0.155), (0.045, 0.010, 0.035), dark)

        # A simple orange calibration object makes the scene useful for viewer tests.
        self.add_box("printedObject", "object_base", (0.02, -0.02, -0.082), (0.075, 0.065, 0.042), orange)
        self.add_box("printedObject", "object_upper", (0.02, -0.02, -0.043), (0.050, 0.042, 0.035), orange)
        self.add_box("printedObject", "object_tip", (0.02, -0.02, -0.014), (0.025, 0.022, 0.025), orange)

    def make_glb(self, path: Path):
        self.build_scene()
        for node in self.nodes:
            if "children" in node and not node["children"]:
                node.pop("children")
        gltf = {
            "asset": {"version": "2.0", "generator": "Deltrol TASK-006 procedural GLB builder"},
            "scene": 0,
            "scenes": [{"name": "Deltrol P2S Reference", "nodes": list(self.parents.values())}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "textures": self.textures,
            "images": self.images,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
            "accessors": self.accessors,
            "bufferViews": self.buffer_views,
            "buffers": [{"byteLength": len(self.bin)}],
            "extras": {
                "deltrol": {
                    "frontAxis": "-Y",
                    "upAxis": "+Z",
                    "units": "meters",
                    "dimensionsMeters": {"width": 0.4, "depth": 0.4, "height": 0.5},
                    "variant": self.variant,
                    "logicalParts": ["enclosure", "door", "printHead", "printBed", "gantryX", "gantryY", "printedObject"],
                    "sourceReference": "assets/generated/antigravity/multiview/",
                }
            },
        }
        json_bytes = json.dumps(gltf, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        json_bytes += b" " * ((4 - len(json_bytes) % 4) % 4)
        bin_bytes = bytes(self.bin)
        bin_bytes += b"\x00" * ((4 - len(bin_bytes) % 4) % 4)
        total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
        with path.open("wb") as handle:
            handle.write(struct.pack("<IHHI", 0x46546C67, 2, 0, total_length))
            handle.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
            handle.write(json_bytes)
            handle.write(struct.pack("<II", len(bin_bytes), 0x004E4942))
            handle.write(bin_bytes)
        return {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": path.stat().st_size,
            "mesh_count": len(self.meshes),
            "node_count": len(self.nodes),
            "material_count": len(self.materials),
            "texture_count": len(self.textures),
            "buffer_bytes": len(self.bin),
            "sha256": __import__("hashlib").sha256(path.read_bytes()).hexdigest(),
        }


def main():
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    OPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw = GLBBuilder(cylinder_segments=24, variant="source_raw")
    optimized = GLBBuilder(cylinder_segments=12, variant="browser_optimized")
    print(json.dumps({"raw": raw.make_glb(RAW_PATH), "optimized": optimized.make_glb(OPT_PATH)}, indent=2))


if __name__ == "__main__":
    main()
