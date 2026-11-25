"""
TASK-031: Reference-Locked Photoreal True-3D Fidelity Builder (v3)
Generates assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb

Visual Fidelity Upgrades over TASK-030:
1. Calibrated P2S 3/4 silhouette proportions (W=0.415, D=0.358, H=0.398 raw -> matches
   reference front-vs-side aspect ~72%:28% and vertical ratio W/H ~ 1.05).
2. Silky liquid-metal anodized champagne finish (eliminated coarse horizontal grain lines!):
   - Continuous smooth cylindrical highlight ribbon across the rounded front-right pillar.
   - Crisp bright champagne highlight bevel along the slim front-left corner pillar.
   - Soft studio softbox tonal falloff across the top forehead, front chin, and darker
     gunmetal-champagne shaded right side wall.
3. Warm amber-illuminated CoreXY chamber inside the smoked glass door:
   - Enclosed interior backplane & left-inner liner radiating calibrated warm studio amber
     through the 52%-opacity Smoked Glass without crushing interior hardware into black.
   - Prominent 3-rail steel CoreXY gantry, brushed champagne toolhead front cover,
     curved white PTFE Bowden tube, rear drag chain, gold-bronze PEI plate, and 15-fin
     aerospace arch bracket.
4. Reference-exact architectural console notch & sturdy integrated corner legs on flat
   rubber corner pads (eliminated floating black bottom plate and right-side bright seam).
5. 100% genuine connected 3D geometry across all viewing angles (zero billboards/planes).
"""

import io
import json
import math
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_true3d_candidate_v3.glb"


def make_silky_champagne_front_texture(size=512):
    """Smooth silky champagne anodized metal with soft studio top-left highlight (NO coarse stripes!)."""
    u = np.linspace(0.0, 1.0, size).reshape(1, size, 1)
    v = np.linspace(0.0, 1.0, size).reshape(size, 1, 1)
    # Soft diagonal studio softbox gradient (brighter left/top-center -> deeper right/bottom)
    sheen = 1.06 - 0.14 * u + 0.08 * (1.0 - v)
    rng = np.random.default_rng(202)
    micro = rng.normal(0.0, 0.45, (size, size, 1))
    base = np.array([154.0, 144.0, 132.0], dtype=np.float32).reshape(1, 1, 3)
    arr = np.clip(base * sheen + micro, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_pillar_specular_ribbon_texture(size=512):
    """
    Smooth cylindrical anodized metal wrap for the front-right rounded post:
    Reproduces the crisp vertical silver-champagne specular ribbon on the curved nose
    flanked by rich bronze-titanium midtones and dark gunmetal edge roll-off.
    u in [0..1] wraps smoothly around the 90-deg pillar arc!
    """
    u = np.linspace(0.0, 1.0, size).reshape(1, size, 1)
    v = np.linspace(0.0, 1.0, size).reshape(size, 1, 1)
    # Specular highlight ribbon peaking around u = 0.34 (facing front-right camera edge)
    highlight = np.exp(-((u - 0.34) / 0.16) ** 2) * 0.48
    rim_shadow = np.exp(-((u - 0.78) / 0.20) ** 2) * 0.30
    left_edge_dark = np.exp(-((u - 0.04) / 0.08) ** 2) * 0.18
    v_grad = 1.04 - 0.06 * v
    base = np.array([142.0, 130.0, 116.0], dtype=np.float32).reshape(1, 1, 3)
    hl_col = np.array([224.0, 214.0, 200.0], dtype=np.float32).reshape(1, 1, 3)
    sh_col = np.array([76.0, 66.0, 56.0], dtype=np.float32).reshape(1, 1, 3)

    col = base * (1.0 - highlight - rim_shadow - left_edge_dark) + hl_col * highlight + sh_col * (rim_shadow + left_edge_dark)
    col = col * v_grad
    rng = np.random.default_rng(303)
    col += rng.normal(0.0, 0.35, (size, size, 1))
    arr = np.clip(col, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_left_pillar_texture(size=256):
    """Crisp left edge brushed silver-champagne pillar highlight matching reference left border."""
    u = np.linspace(0.0, 1.0, size).reshape(1, size, 1)
    hl = np.exp(-((u - 0.48) / 0.25) ** 2) * 0.55
    base = np.array([156.0, 148.0, 138.0], dtype=np.float32).reshape(1, 1, 3)
    hl_col = np.array([234.0, 228.0, 216.0], dtype=np.float32).reshape(1, 1, 3)
    col = base * (1.0 - hl) + hl_col * hl
    arr = np.repeat(np.clip(col, 0, 255).astype(np.uint8), size, axis=0)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_side_shaded_metal_texture(size=256):
    """Rich shaded anodized titanium-bronze for side walls (natural lighting contrast vs front)."""
    u = np.linspace(0.0, 1.0, size).reshape(1, size, 1)
    v = np.linspace(0.0, 1.0, size).reshape(size, 1, 1)
    grad = 0.96 - 0.14 * u + 0.08 * (1.0 - v)
    base = np.array([112.0, 100.0, 86.0], dtype=np.float32).reshape(1, 1, 3)
    arr = np.clip(base * grad, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_pei_plate_texture(size=512):
    rng = np.random.default_rng(77)
    speckle = rng.normal(0.0, 6.0, (size, size, 1))
    base = np.array([164.0, 134.0, 88.0], dtype=np.float32).reshape(1, 1, 3)
    arr = np.clip(base + speckle, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_sleek_screen_texture(width=512, height=256):
    img = Image.new("RGBA", (width, height), (20, 22, 24, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, width - 4, height - 4], radius=12, fill=(24, 26, 29, 255), outline=(48, 48, 52, 255), width=2)
    d.polygon([(0, 0), (int(width * 0.52), 0), (int(width * 0.30), height), (0, height)], fill=(34, 35, 38, 255))
    return img


class True3DV3Builder:
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

    def add_material(self, name, rgba, metallic, roughness, alpha_mode="OPAQUE", texture_img=None, emissive=None, double_sided=False):
        if name in self.material_cache:
            return self.material_cache[name]

        pbr = {
            "baseColorFactor": [rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0, rgba[3] / 255.0],
            "metallicFactor": metallic,
            "roughnessFactor": roughness,
        }

        if texture_img is not None:
            stream = io.BytesIO()
            texture_img.save(stream, format="PNG", optimize=True)
            img_bytes = stream.getvalue()
            image_view = self.add_blob(img_bytes)
            image_index = len(self.images)
            self.images.append({"bufferView": image_view, "mimeType": "image/png", "name": f"{name} Texture"})
            texture_index = len(self.textures)
            self.textures.append({"sampler": 0, "source": image_index, "name": f"{name} Texture"})
            pbr["baseColorTexture"] = {"index": texture_index}

        material = {
            "name": name,
            "pbrMetallicRoughness": pbr,
            "alphaMode": alpha_mode,
            "doubleSided": double_sided,
        }
        if emissive:
            material["emissiveFactor"] = emissive

        self.materials.append(material)
        idx = len(self.materials) - 1
        self.material_cache[name] = idx
        return idx

    def add_parent(self, name):
        idx = len(self.nodes)
        self.nodes.append({"name": name, "children": [], "extras": {"logicalPart": name}})
        self.parents[name] = idx
        return idx

    def _fix_winding(self, positions, normals, indices):
        fixed = list(indices)
        for t in range(0, len(fixed), 3):
            i0, i1, i2 = fixed[t], fixed[t + 1], fixed[t + 2]
            p0 = np.array(positions[i0 * 3:i0 * 3 + 3])
            p1 = np.array(positions[i1 * 3:i1 * 3 + 3])
            p2 = np.array(positions[i2 * 3:i2 * 3 + 3])
            gn = np.cross(p1 - p0, p2 - p0)
            vn = (
                np.array(normals[i0 * 3:i0 * 3 + 3])
                + np.array(normals[i1 * 3:i1 * 3 + 3])
                + np.array(normals[i2 * 3:i2 * 3 + 3])
            )
            if np.dot(gn, vn) < 0.0:
                fixed[t + 1], fixed[t + 2] = fixed[t + 2], fixed[t + 1]
        return fixed

    def add_mesh_node(self, parent_name, mesh_name, positions, normals, uvs, indices, material_index):
        indices = self._fix_winding(positions, normals, indices)

        pos_bytes = struct.pack(f"<{len(positions)}f", *positions)
        norm_bytes = struct.pack(f"<{len(normals)}f", *normals)
        uv_bytes = struct.pack(f"<{len(uvs)}f", *uvs)
        use_u32 = len(positions) // 3 > 65535
        if use_u32:
            idx_bytes = struct.pack(f"<{len(indices)}I", *indices)
            idx_ctype = 5125
        else:
            idx_bytes = struct.pack(f"<{len(indices)}H", *indices)
            idx_ctype = 5123

        mins = [min(positions[i::3]) for i in range(3)]
        maxs = [max(positions[i::3]) for i in range(3)]

        pos_acc = self.add_accessor(pos_bytes, 5126, len(positions) // 3, "VEC3", mins, maxs, 34962)
        norm_acc = self.add_accessor(norm_bytes, 5126, len(normals) // 3, "VEC3", target=34962)
        uv_acc = self.add_accessor(uv_bytes, 5126, len(uvs) // 2, "VEC2", target=34962)
        idx_acc = self.add_accessor(idx_bytes, idx_ctype, len(indices), "SCALAR", target=34963)

        mesh_idx = len(self.meshes)
        self.meshes.append({
            "name": mesh_name,
            "primitives": [{
                "attributes": {"POSITION": pos_acc, "NORMAL": norm_acc, "TEXCOORD_0": uv_acc},
                "indices": idx_acc,
                "material": material_index,
                "mode": 4,
            }],
        })

        node_idx = len(self.nodes)
        self.nodes.append({"name": mesh_name, "mesh": mesh_idx})
        self.nodes[self.parents[parent_name]]["children"].append(node_idx)
        return node_idx

    # -----------------------------------------------------------------
    # Geometry Generators
    # -----------------------------------------------------------------
    def _asym_rounded_rect_ring(self, w, d, r_left, r_right, seg=16):
        hw, hd = w / 2.0, d / 2.0
        pts, norms = [], []
        corners = [
            ( hw - r_right,  hd - r_right, r_right, 0.0, math.pi / 2.0),
            (-hw + r_left,   hd - r_left,  r_left,  math.pi / 2.0, math.pi),
            (-hw + r_left,  -hd + r_left,  r_left,  math.pi, 1.5 * math.pi),
            ( hw - r_right, -hd + r_right, r_right, 1.5 * math.pi, 2.0 * math.pi),
        ]
        for cx, cy, r, a0, a1 in corners:
            for i in range(seg + 1):
                a = a0 + (a1 - a0) * (i / seg)
                ca, sa = math.cos(a), math.sin(a)
                pts.append((cx + r * ca, cy + r * sa))
                norms.append((ca, sa))
        return pts, norms

    def add_extruded_asym_frame(self, parent_name, mesh_name, w, d, inner_w, inner_d, z_bot, z_top, r_left, r_right, inner_r, top_bevel, material_index, seg=16):
        b = top_bevel
        out_bot, out_n = self._asym_rounded_rect_ring(w, d, r_left, r_right, seg)
        out_top, _ = self._asym_rounded_rect_ring(w - 2 * b, d - 2 * b, max(0.002, r_left - b), max(0.002, r_right - b), seg)
        in_ring, in_n = self._asym_rounded_rect_ring(inner_w, inner_d, inner_r, inner_r, seg)
        n_pts = len(out_bot)
        positions, normals, uvs, indices = [], [], [], []

        def emit_strip(ringA, zA, ringB, zB, nrm_fn):
            base_v = len(positions) // 3
            for i in range(n_pts + 1):
                k = i % n_pts
                xa, ya = ringA[k]
                xb, yb = ringB[k]
                na = nrm_fn(k)
                u_val = (xa + w / 2.0) / w
                positions.extend([xa, ya, zA, xb, yb, zB])
                normals.extend([na[0], na[1], na[2], na[0], na[1], na[2]])
                uvs.extend([u_val, (z_top - zA) * 2.0, u_val, (z_top - zB) * 2.0])
            for i in range(n_pts):
                v0 = base_v + i * 2
                indices.extend([v0, v0 + 2, v0 + 3, v0, v0 + 3, v0 + 1])

        emit_strip(out_bot, z_bot, out_bot, z_top - b, lambda k: (out_n[k][0], out_n[k][1], 0.0))
        emit_strip(out_bot, z_top - b, out_top, z_top, lambda k: (out_n[k][0] * 0.707, out_n[k][1] * 0.707, 0.707))
        emit_strip(out_top, z_top, in_ring, z_top, lambda k: (0.0, 0.0, 1.0))
        emit_strip(in_ring, z_top, in_ring, z_bot, lambda k: (-in_n[k][0], -in_n[k][1], 0.0))
        emit_strip(in_ring, z_bot, out_bot, z_bot, lambda k: (0.0, 0.0, -1.0))

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_corner_pillar(self, parent_name, mesh_name, corner_x, corner_y, radius, z_bot, z_top, quad_idx, material_index, seg=16):
        """
        Extrudes a vertical quarter-round pillar with smooth cylindrical UV wrapping u in [0..1]
        across the 90-degree arc so anisotropic specular ribbon wraps seamlessly across angles!
        """
        a0 = quad_idx * (math.pi / 2.0)
        a1 = a0 + math.pi / 2.0
        arc_pts, arc_norms = [], []
        for i in range(seg + 1):
            a = a0 + (a1 - a0) * (i / seg)
            ca, sa = math.cos(a), math.sin(a)
            arc_pts.append((corner_x + radius * ca, corner_y + radius * sa))
            arc_norms.append((ca, sa))

        poly = arc_pts + [(corner_x, corner_y)]
        n_p = len(poly)
        positions, normals, uvs, indices = [], [], [], []

        for i in range(n_p):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n_p]
            if i < seg:
                n0, n1 = arc_norms[i], arc_norms[i + 1]
                # u runs smoothly 0 -> 1 along outer 90-deg curve
                u0, u1 = i / seg, (i + 1) / seg
            else:
                dx, dy = x1 - x0, y1 - y0
                ln = math.hypot(dx, dy) or 1.0
                n0 = n1 = (dy / ln, -dx / ln)
                u0 = u1 = 0.05

            base_v = len(positions) // 3
            positions.extend([x0, y0, z_bot, x1, y1, z_bot, x1, y1, z_top, x0, y0, z_top])
            normals.extend([n0[0], n0[1], 0.0, n1[0], n1[1], 0.0, n1[0], n1[1], 0.0, n0[0], n0[1], 0.0])
            uvs.extend([u0, 1.0, u1, 1.0, u1, 0.0, u0, 0.0])
            indices.extend([base_v, base_v + 1, base_v + 2, base_v, base_v + 2, base_v + 3])

        cx = sum(p[0] for p in poly) / n_p
        cy = sum(p[1] for p in poly) / n_p
        for z_c, nz in ((z_bot, -1.0), (z_top, 1.0)):
            c_idx = len(positions) // 3
            positions.extend([cx, cy, z_c])
            normals.extend([0.0, 0.0, nz])
            uvs.extend([0.5, 0.5])
            for x, y in poly:
                positions.extend([x, y, z_c])
                normals.extend([0.0, 0.0, nz])
                uvs.extend([0.5, 0.5])
            for i in range(n_p):
                nxt = (i + 1) % n_p
                indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_extruded_polygon_y(self, parent_name, mesh_name, poly_xz, y0, y1, material_index):
        n_p = len(poly_xz)
        positions, normals, uvs, indices = [], [], [], []
        cx = sum(p[0] for p in poly_xz) / n_p
        cz = sum(p[1] for p in poly_xz) / n_p

        area2 = sum(poly_xz[i][0] * poly_xz[(i + 1) % n_p][1] - poly_xz[(i + 1) % n_p][0] * poly_xz[i][1] for i in range(n_p))
        pts = list(poly_xz) if area2 > 0 else list(reversed(poly_xz))

        for i in range(n_p):
            x0, z0 = pts[i]
            x1, z1 = pts[(i + 1) % n_p]
            dx, dz = x1 - x0, z1 - z0
            ln = math.hypot(dx, dz) or 1.0
            nx, nz = dz / ln, -dx / ln
            base_v = len(positions) // 3
            positions.extend([x0, y0, z0, x1, y0, z1, x1, y1, z1, x0, y1, z0])
            normals.extend([nx, 0.0, nz] * 4)
            uvs.extend([x0 + 0.5, 0.5 - z0, x1 + 0.5, 0.5 - z1, x1 + 0.5, 0.5 - z1, x0 + 0.5, 0.5 - z0])
            indices.extend([base_v, base_v + 1, base_v + 2, base_v, base_v + 2, base_v + 3])

        for y_c, ny in ((y0, -1.0), (y1, 1.0)):
            c_idx = len(positions) // 3
            positions.extend([cx, y_c, cz])
            normals.extend([0.0, ny, 0.0])
            uvs.extend([cx + 0.5, 0.5 - cz])
            for x, z in pts:
                positions.extend([x, y_c, z])
                normals.extend([0.0, ny, 0.0])
                uvs.extend([x + 0.5, 0.5 - z])
            for i in range(n_p):
                nxt = (i + 1) % n_p
                indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_extruded_polygon_x(self, parent_name, mesh_name, poly_yz, x0, x1, material_index):
        n_p = len(poly_yz)
        positions, normals, uvs, indices = [], [], [], []
        cy = sum(p[0] for p in poly_yz) / n_p
        cz = sum(p[1] for p in poly_yz) / n_p
        area2 = sum(poly_yz[i][0] * poly_yz[(i + 1) % n_p][1] - poly_yz[(i + 1) % n_p][0] * poly_yz[i][1] for i in range(n_p))
        pts = list(poly_yz) if area2 > 0 else list(reversed(poly_yz))

        for i in range(n_p):
            y0, z0 = pts[i]
            y1, z1 = pts[(i + 1) % n_p]
            dy, dz = y1 - y0, z1 - z0
            ln = math.hypot(dy, dz) or 1.0
            ny, nz = dz / ln, -dy / ln
            base_v = len(positions) // 3
            positions.extend([x0, y0, z0, x0, y1, z1, x1, y1, z1, x1, y0, z0])
            normals.extend([0.0, ny, nz] * 4)
            uvs.extend([y0 + 0.5, 0.5 - z0, y1 + 0.5, 0.5 - z1, y1 + 0.5, 0.5 - z1, y0 + 0.5, 0.5 - z0])
            indices.extend([base_v, base_v + 1, base_v + 2, base_v, base_v + 2, base_v + 3])

        for x_c, nx in ((x0, -1.0), (x1, 1.0)):
            c_idx = len(positions) // 3
            positions.extend([x_c, cy, cz])
            normals.extend([nx, 0.0, 0.0])
            uvs.extend([cy + 0.5, 0.5 - cz])
            for y, z in pts:
                positions.extend([x_c, y, z])
                normals.extend([nx, 0.0, 0.0])
                uvs.extend([y + 0.5, 0.5 - z])
            for i in range(n_p):
                nxt = (i + 1) % n_p
                indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_box(self, parent_name, mesh_name, center, size, material_index, rot_x=0.0, rot_y=0.0):
        cx, cy, cz = center
        sx, sy, sz = [s / 2.0 for s in size]
        cax, sax = math.cos(rot_x), math.sin(rot_x)
        cay, say = math.cos(rot_y), math.sin(rot_y)

        def xform(x, y, z):
            x1 = x * cay + z * say
            z1 = -x * say + z * cay
            y2 = y * cax - z1 * sax
            z2 = y * sax + z1 * cax
            return (cx + x1, cy + y2, cz + z2)

        def xnorm(nx, ny, nz):
            x1 = nx * cay + nz * say
            z1 = -nx * say + nz * cay
            y2 = ny * cax - z1 * sax
            z2 = ny * sax + z1 * cax
            return (x1, y2, z2)

        faces = [
            ((0,  1,  0), [( sx,  sy, -sz), (-sx,  sy, -sz), (-sx,  sy,  sz), ( sx,  sy,  sz)]),
            ((0, -1,  0), [(-sx, -sy, -sz), ( sx, -sy, -sz), ( sx, -sy,  sz), (-sx, -sy,  sz)]),
            ((-1, 0,  0), [(-sx,  sy, -sz), (-sx, -sy, -sz), (-sx, -sy,  sz), (-sx,  sy,  sz)]),
            (( 1, 0,  0), [( sx, -sy, -sz), ( sx,  sy, -sz), ( sx,  sy,  sz), ( sx, -sy,  sz)]),
            ((0,  0,  1), [(-sx, -sy,  sz), ( sx, -sy,  sz), ( sx,  sy,  sz), (-sx,  sy,  sz)]),
            ((0,  0, -1), [(-sx,  sy, -sz), ( sx,  sy, -sz), ( sx, -sy, -sz), (-sx, -sy, -sz)]),
        ]
        positions, normals, uvs, indices = [], [], [], []
        idx = 0
        for norm, quad in faces:
            nx, ny, nz = xnorm(*norm)
            for vx, vy, vz in quad:
                px, py, pz = xform(vx, vy, vz)
                positions.extend([px, py, pz])
                normals.extend([nx, ny, nz])
            uvs.extend([0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
            indices.extend([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
            idx += 4

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_cylinder(self, parent_name, mesh_name, center, radius, length, axis, material_index, seg=24):
        cx, cy, cz = center
        half = length / 2.0
        positions, normals, uvs, indices = [], [], [], []

        for i in range(seg + 1):
            t = 2.0 * math.pi * (i / seg)
            ct, st = math.cos(t), math.sin(t)
            u = i / seg
            if axis == "z":
                nx, ny, nz = ct, st, 0.0
                v0 = (cx + radius * ct, cy + radius * st, cz - half)
                v1 = (cx + radius * ct, cy + radius * st, cz + half)
            elif axis == "y":
                nx, ny, nz = ct, 0.0, st
                v0 = (cx + radius * ct, cy - half, cz + radius * st)
                v1 = (cx + radius * ct, cy + half, cz + radius * st)
            else:
                nx, ny, nz = 0.0, ct, st
                v0 = (cx - half, cy + radius * ct, cz + radius * st)
                v1 = (cx + half, cy + radius * ct, cz + radius * st)

            positions.extend([*v0, *v1])
            normals.extend([nx, ny, nz, nx, ny, nz])
            uvs.extend([u, 0.0, u, 1.0])

        for i in range(seg):
            v0 = i * 2
            indices.extend([v0, v0 + 1, v0 + 3, v0, v0 + 3, v0 + 2])

        for cap_dir in (-1, 1):
            c_idx = len(positions) // 3
            cn = [0.0, 0.0, 0.0]
            if axis == "z":
                cn[2] = float(cap_dir)
                positions.extend([cx, cy, cz + cap_dir * half])
            elif axis == "y":
                cn[1] = float(cap_dir)
                positions.extend([cx, cy + cap_dir * half, cz])
            else:
                cn[0] = float(cap_dir)
                positions.extend([cx + cap_dir * half, cy, cz])
            normals.extend(cn)
            uvs.extend([0.5, 0.5])
            for i in range(seg):
                t = 2.0 * math.pi * (i / seg)
                ct, st = math.cos(t), math.sin(t)
                if axis == "z":
                    positions.extend([cx + radius * ct, cy + radius * st, cz + cap_dir * half])
                elif axis == "y":
                    positions.extend([cx + radius * ct, cy + cap_dir * half, cz + radius * st])
                else:
                    positions.extend([cx + cap_dir * half, cy + radius * ct, cz + radius * st])
                normals.extend(cn)
                uvs.extend([0.5 + 0.5 * ct, 0.5 + 0.5 * st])
            for i in range(seg):
                nxt = (i + 1) % seg
                indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_curved_tube(self, parent_name, mesh_name, points, radius, material_index, seg=12):
        positions, normals, uvs, indices = [], [], [], []
        rings = []
        for idx_p, p in enumerate(points):
            if idx_p == 0:
                tangent = np.array(points[1]) - np.array(points[0])
            elif idx_p == len(points) - 1:
                tangent = np.array(points[-1]) - np.array(points[-2])
            else:
                tangent = np.array(points[idx_p + 1]) - np.array(points[idx_p - 1])
            tangent = tangent / (np.linalg.norm(tangent) or 1.0)
            up = np.array([1.0, 0.0, 0.0]) if abs(tangent[0]) < 0.8 else np.array([0.0, 1.0, 0.0])
            b1 = np.cross(tangent, up)
            b1 = b1 / (np.linalg.norm(b1) or 1.0)
            b2 = np.cross(tangent, b1)
            ring = []
            for s in range(seg + 1):
                a = 2.0 * math.pi * (s / seg)
                n_vec = math.cos(a) * b1 + math.sin(a) * b2
                pos = np.array(p) + radius * n_vec
                ring.append((pos, n_vec))
            rings.append(ring)

        for r_i in range(len(rings) - 1):
            base_v = len(positions) // 3
            for s in range(seg + 1):
                p0, n0 = rings[r_i][s]
                p1, n1 = rings[r_i + 1][s]
                u = s / seg
                v0_uv = r_i / (len(rings) - 1)
                v1_uv = (r_i + 1) / (len(rings) - 1)
                positions.extend([*p0.tolist(), *p1.tolist()])
                normals.extend([*n0.tolist(), *n1.tolist()])
                uvs.extend([u, v0_uv, u, v1_uv])
            for s in range(seg):
                v0 = base_v + s * 2
                indices.extend([v0, v0 + 1, v0 + 3, v0, v0 + 3, v0 + 2])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def build_scene(self):
        tex_front = make_silky_champagne_front_texture(512)
        tex_pillar_r = make_pillar_specular_ribbon_texture(512)
        tex_pillar_l = make_left_pillar_texture(256)
        tex_side = make_side_shaded_metal_texture(256)
        tex_pei = make_pei_plate_texture(512)
        tex_ui = make_sleek_screen_texture()

        # Silky Multi-Zone Metallic Champagne Materials (eliminated flat/striped beige CAD look!)
        mat_front_metal = self.add_material("Champagne Metal Front", (255, 255, 255, 255), 0.34, 0.24, texture_img=tex_front)
        mat_pillar_r = self.add_material("Champagne Pillar Highlight", (255, 255, 255, 255), 0.32, 0.22, texture_img=tex_pillar_r)
        mat_pillar_l = self.add_material("Champagne Pillar Left", (255, 255, 255, 255), 0.30, 0.22, texture_img=tex_pillar_l)
        mat_side_metal = self.add_material("Champagne Side Shaded", (255, 255, 255, 255), 0.38, 0.28, texture_img=tex_side)

        mat_graphite = self.add_material("Graphite Door Frame", (22, 24, 28, 255), 0.52, 0.24)
        mat_smoked_glass = self.add_material("Smoked Glass", (18, 22, 26, 135), 0.35, 0.08, alpha_mode="BLEND", double_sided=True)
        mat_gunmetal_handle = self.add_material("Anodized Gunmetal Handle", (66, 62, 58, 255), 0.65, 0.25)
        mat_console_rim = self.add_material("Console Metallic Trim", (142, 134, 122, 255), 0.48, 0.26)
        mat_hinge_metal = self.add_material("Satin Hinge Metal", (128, 120, 110, 255), 0.42, 0.26)
        mat_rubber_foot = self.add_material("Matte Rubber Foot", (34, 32, 30, 255), 0.06, 0.80)

        # Warm glowing amber chamber backplane/liner so chamber glows warmly behind 52% smoked glass!
        mat_chamber_glow = self.add_material("Interior Chamber Amber", (238, 200, 162, 255), 0.18, 0.40, emissive=[0.56, 0.39, 0.25])
        mat_chamber_ceiling = self.add_material("Interior Ceiling Glow", (250, 222, 186, 255), 0.10, 0.35, emissive=[0.85, 0.64, 0.42])
        mat_interior_dark = self.add_material("Chassis Matte Dark", (72, 60, 50, 255), 0.35, 0.45, emissive=[0.12, 0.09, 0.06])
        mat_led_glow = self.add_material("Interior LED Glow", (255, 240, 212, 255), 0.05, 0.20, emissive=[1.0, 0.86, 0.68])

        mat_pei = self.add_material("Gold Textured PEI", (255, 255, 255, 255), 0.68, 0.32, texture_img=tex_pei, emissive=[0.18, 0.13, 0.06])
        mat_carbon = self.add_material("PA-CF Carbon Fiber", (112, 98, 86, 255), 0.35, 0.34, emissive=[0.10, 0.08, 0.05])
        mat_toolhead_face = self.add_material("Toolhead Titanium Face", (234, 206, 176, 255), 0.42, 0.24, emissive=[0.32, 0.23, 0.15])
        mat_part_metal = self.add_material("Printed Aerospace Alloy", (216, 192, 168, 255), 0.48, 0.28, emissive=[0.24, 0.17, 0.12])
        mat_steel = self.add_material("Linear Guide Steel", (245, 240, 232, 255), 0.90, 0.14, emissive=[0.28, 0.23, 0.18])
        mat_brass = self.add_material("Brass Nozzle", (228, 178, 54, 255), 0.92, 0.18, emissive=[0.15, 0.10, 0.02])
        mat_ptfe = self.add_material("PTFE Bowden Tube", (250, 246, 240, 255), 0.05, 0.28, emissive=[0.32, 0.26, 0.20])
        mat_screen = self.add_material("Touchscreen UI", (255, 255, 255, 255), 0.18, 0.10, texture_img=tex_ui)

        for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]:
            self.add_parent(p)

        # Calibrated P2S 3/4 Dimensions: wider front face (W=0.415) vs shallower right side (D=0.356),
        # taller vertical presence (Z in [-0.204, +0.194]) -> matches reference front:side ~ 72%:28%
        W, D = 0.415, 0.356
        R_left = 0.015    # Sleek bright silver-champagne left vertical edge
        R_right = 0.028   # Bold rounded front-right post with liquid metal ribbon!
        Z_leg_bot = -0.202
        Z_side_arch = -0.186
        Z_chin_top = -0.142
        Z_door_top = 0.138
        Z_roof_top = 0.192

        # -------------------------------------------------------------
        # 1. FLUSH MONOLITHIC UNIBODY ENCLOSURE (`enclosure`)
        # -------------------------------------------------------------
        # Floor tray & rear casing strictly inside wall envelopes
        self.add_box("enclosure", "interior_floor_tray", (0.0, 0.0, Z_chin_top - 0.008), (W - 0.050, D - 0.050, 0.014), mat_interior_dark)
        self.add_box("enclosure", "chassis_underpan", (0.0, 0.0, Z_side_arch + 0.012), (W - 0.054, D - 0.054, 0.024), mat_graphite)

        # Corner Pillars: Left pillars use crisp bright-edge highlight; Right front/rear use specular ribbon!
        self.add_corner_pillar("enclosure", "unibody_corner_0",  W / 2.0 - R_right,  D / 2.0 - R_right, R_right, Z_leg_bot, Z_door_top, 0, mat_side_metal)
        self.add_corner_pillar("enclosure", "unibody_corner_1", -W / 2.0 + R_left,   D / 2.0 - R_left,  R_left,  Z_leg_bot, Z_door_top, 1, mat_side_metal)
        self.add_corner_pillar("enclosure", "unibody_corner_2", -W / 2.0 + R_left,  -D / 2.0 + R_left,  R_left,  Z_leg_bot, Z_door_top, 2, mat_pillar_l)
        self.add_corner_pillar("enclosure", "unibody_corner_3",  W / 2.0 - R_right, -D / 2.0 + R_right, R_right, Z_leg_bot, Z_door_top, 3, mat_pillar_r)

        # Low-profile Rubber Feet strictly tucked under corner pads (matching reference height!)
        foot_coords = [
            (-W / 2.0 + 0.020, -D / 2.0 + 0.020, 0.022),
            ( W / 2.0 - 0.032, -D / 2.0 + 0.032, 0.030),
            ( W / 2.0 - 0.032,  D / 2.0 - 0.032, 0.030),
            (-W / 2.0 + 0.020,  D / 2.0 - 0.020, 0.022),
        ]
        for i, (fx, fy, fw) in enumerate(foot_coords):
            self.add_box("enclosure", f"chassis_foot_{i}", (fx, fy, Z_leg_bot - 0.002), (fw, fw, 0.006), mat_rubber_foot)

        # Flush Top Crown Rim + Solid Dark Roof Inset (keeps 3/4 silhouette clean like reference!)
        self.add_extruded_asym_frame("enclosure", "unibody_top_frame", W, D, 0.340, 0.285,
                                     Z_door_top, Z_roof_top, R_left, R_right, 0.012, 0.0025, mat_front_metal)
        self.add_extruded_asym_frame("enclosure", "top_rim_outer", 0.344, 0.289, 0.330, 0.275,
                                     Z_roof_top - 0.009, Z_roof_top - 0.001, 0.012, 0.012, 0.010, 0.001, mat_graphite)
        self.add_box("enclosure", "top_roof_glass", (0.0, 0.0, Z_roof_top - 0.006), (0.334, 0.279, 0.004), mat_smoked_glass)

        # Front Header & Clean Level Chin (with subtle recessed center notch for console)
        x_f_min = -W / 2.0 + R_left
        x_f_max =  W / 2.0 - R_right
        f_mid_w = x_f_max - x_f_min
        f_mid_x = 0.5 * (x_f_min + x_f_max)

        self.add_box("enclosure", "unibody_front_header", (f_mid_x, -D / 2.0 + 0.012, Z_door_top - 0.005), (f_mid_w, 0.024, 0.010), mat_front_metal)
        front_skirt_poly = [
            (x_f_min,          Z_leg_bot),
            (x_f_min + 0.048,  Z_leg_bot),
            (x_f_min + 0.056,  Z_leg_bot + 0.003),
            (x_f_max - 0.056,  Z_leg_bot + 0.003),
            (x_f_max - 0.048,  Z_leg_bot),
            (x_f_max,          Z_leg_bot),
            (x_f_max,          Z_chin_top),
            (x_f_min,          Z_chin_top),
        ]
        self.add_extruded_polygon_y("enclosure", "unibody_front_chin_skirt", front_skirt_poly, -D / 2.0, -D / 2.0 + 0.024, mat_front_metal)

        # Shaded Side Wall Frames + Clean Rectangular Side Arch Skirt + Sealed Window
        y_l_min, y_l_max = -D / 2.0 + R_left,  D / 2.0 - R_left
        y_r_min, y_r_max = -D / 2.0 + R_right, D / 2.0 - R_right

        for side_name, sx_sign, y_min, y_max in [
            ("left",  -1.0, y_l_min, y_l_max),
            ("right",  1.0, y_r_min, y_r_max),
        ]:
            s_span = y_max - y_min
            s_yc = 0.5 * (y_min + y_max)
            wx = sx_sign * (W / 2.0 - 0.012)
            self.add_box("enclosure", f"unibody_{side_name}_top_beam", (wx, s_yc, Z_door_top - 0.005), (0.024, s_span, 0.010), mat_side_metal)

            side_skirt_poly = [
                (y_min,         Z_leg_bot),
                (y_min + 0.022, Z_leg_bot),
                (y_min + 0.034, Z_side_arch),
                (y_max - 0.034, Z_side_arch),
                (y_max - 0.022, Z_leg_bot),
                (y_max,         Z_leg_bot),
                (y_max,         Z_chin_top),
                (y_min,         Z_chin_top),
            ]
            x0_s = sx_sign * (W / 2.0 - 0.024) if sx_sign > 0 else -W / 2.0
            x1_s = sx_sign * (W / 2.0)         if sx_sign > 0 else -W / 2.0 + 0.024
            self.add_extruded_polygon_x("enclosure", f"unibody_{side_name}_skirt", side_skirt_poly, min(x0_s, x1_s), max(x0_s, x1_s), mat_side_metal)

            # Dark perimeter gasket reaches flush to outer side plane (W/2 - 0.001) to cover any bright interior skirt shelf!
            gx = sx_sign * (W / 2.0 - 0.012)
            win_z_ctr = 0.5 * ((Z_door_top - 0.010) + Z_chin_top)
            win_h = (Z_door_top - 0.010) - Z_chin_top
            self.add_box("enclosure", f"{side_name}_gasket_top", (gx, s_yc, Z_door_top - 0.014), (0.022, s_span + 0.004, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_bot", (gx, s_yc, Z_chin_top + 0.004),  (0.023, s_span + 0.004, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_f",   (gx, y_min + 0.003, win_z_ctr),  (0.022, 0.014, win_h), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_r",   (gx, y_max - 0.003, win_z_ctr),  (0.023, 0.016, win_h), mat_graphite)
            self.add_box("enclosure", f"{side_name}_glass_window", (sx_sign * (W / 2.0 - 0.012), s_yc, win_z_ctr), (0.005, s_span - 0.008, win_h - 0.008), mat_smoked_glass)

        # Rear Wall + Warm Glowing Interior Chamber (rear & left chamber surfaces glow warm amber!)
        rear_w = (W / 2.0 - R_right) - (-W / 2.0 + R_left)
        rear_xc = 0.5 * ((W / 2.0 - R_right) + (-W / 2.0 + R_left))
        rear_h = Z_door_top - Z_chin_top
        rear_zc = 0.5 * (Z_door_top + Z_chin_top)
        self.add_box("enclosure", "unibody_rear_wall", (rear_xc, D / 2.0 - 0.012, 0.5 * (Z_door_top + Z_leg_bot)),
                     (rear_w, 0.024, Z_door_top - Z_leg_bot), mat_side_metal)

        # Warm glowing interior backplane + left chamber liner (keep ceiling open in center for chamberSpot light!)
        self.add_box("enclosure", "interior_rear_panel", (0.0, D / 2.0 - 0.028, rear_zc), (W - 0.056, 0.006, rear_h), mat_chamber_glow)
        self.add_box("enclosure", "interior_left_back_baffle", (-W / 2.0 + 0.032, 0.020, rear_zc), (0.006, 0.240, rear_h - 0.012), mat_chamber_glow)
        self.add_box("enclosure", "interior_rear_electronics_box", (0.062, D / 2.0 - 0.036, -0.020), (0.140, 0.014, 0.165), mat_interior_dark)

        # Rear architectural louvers
        self.add_box("enclosure", "rear_exhaust_housing", (-0.070, D / 2.0 + 0.003, 0.045), (0.092, 0.006, 0.092), mat_graphite)
        for sl in range(5):
            self.add_box("enclosure", f"rear_vent_louver_{sl}", (-0.070, D / 2.0 + 0.006, 0.015 + sl * 0.015), (0.074, 0.003, 0.006), mat_interior_dark)

        # Warm Interior Ceiling LED Strip Bars (mounted around perimeter so top chamberSpot reaches gantry!)
        self.add_box("enclosure", "led_bar_front", (0.0, -0.125, Z_door_top - 0.008), (0.290, 0.014, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_left",  (-0.155, 0.0, Z_door_top - 0.008), (0.014, 0.220, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_right", ( 0.155, 0.0, Z_door_top - 0.008), (0.014, 0.220, 0.005), mat_led_glow)

        # Console mounted cleanly into bottom chin (dock tucked strictly inside rim width -> zero black ears!)
        console_angle = math.radians(-26.0)
        n_y = -math.cos(console_angle)
        n_z = -math.sin(console_angle)
        bz_y = -D / 2.0 - 0.006
        bz_z = Z_chin_top - 0.022
        self.add_box("enclosure", "screen_dock_wedge", (f_mid_x - 0.006, -D / 2.0 + 0.004, bz_z - 0.002), (0.106, 0.020, 0.026), mat_graphite)
        self.add_box("enclosure", "screen_metal_rim",  (f_mid_x - 0.006, bz_y, bz_z), (0.118, 0.008, 0.042), mat_console_rim, rot_x=console_angle)
        self.add_box("enclosure", "screen_bezel",      (f_mid_x - 0.006, bz_y + n_y * 0.002, bz_z + n_z * 0.002),
                     (0.112, 0.006, 0.036), mat_graphite, rot_x=console_angle)
        self.add_box("enclosure", "screen_display",    (f_mid_x - 0.006, bz_y + n_y * 0.0055, bz_z + n_z * 0.0055),
                     (0.104, 0.002, 0.030), mat_screen, rot_x=console_angle)

        # -------------------------------------------------------------
        # 2. FRONT DOOR ASSEMBLY (`door` + `front_glass_door`)
        # -------------------------------------------------------------
        door_y = -D / 2.0 + 0.007
        door_h = (Z_door_top - 0.010) - Z_chin_top
        door_zc = 0.5 * ((Z_door_top - 0.010) + Z_chin_top)
        door_w = f_mid_w - 0.002
        door_xc = f_mid_x

        self.add_box("enclosure", "front_jamb_seal_l", (x_f_min + 0.006, door_y + 0.008, door_zc), (0.012, 0.008, door_h + 0.004), mat_graphite)
        self.add_box("enclosure", "front_jamb_seal_r", (x_f_max - 0.006, door_y + 0.008, door_zc), (0.012, 0.008, door_h + 0.004), mat_graphite)

        # Flush satin champagne hinges on left edge (matching reference!)
        for h_name, hz in [("door_hinge_top", door_zc + door_h / 2.0 - 0.022), ("door_hinge_bot", door_zc - door_h / 2.0 + 0.022)]:
            self.add_box("enclosure", h_name, (x_f_min + 0.006, door_y - 0.0025, hz), (0.013, 0.009, 0.022), mat_hinge_metal)

        stile_w = 0.015
        rail_h = 0.015
        self.add_box("door", "door_left_stile",  (door_xc - door_w / 2.0 + stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), mat_graphite)
        self.add_box("door", "door_right_stile", (door_xc + door_w / 2.0 - stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), mat_graphite)
        self.add_box("door", "door_top_rail",    (door_xc, door_y, door_zc + door_h / 2.0 - rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), mat_graphite)
        self.add_box("door", "door_bottom_rail", (door_xc, door_y, door_zc - door_h / 2.0 + rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), mat_graphite)

        self.add_box("door", "front_glass_door", (door_xc, door_y, door_zc), (door_w - 2 * stile_w, 0.004, door_h - 2 * rail_h), mat_smoked_glass)

        # Compact rounded dark anodized handle on right edge (matches ref thickness & proportions!)
        hx = door_xc + door_w / 2.0 - 0.004
        hz = door_zc - 0.006
        self.add_box("door", "door_ergo_handle",      (hx, door_y - 0.011, hz), (0.014, 0.011, 0.056), mat_gunmetal_handle)
        self.add_box("door", "door_handle_mount_top", (hx, door_y - 0.006, hz + 0.016), (0.010, 0.008, 0.008), mat_gunmetal_handle)
        self.add_box("door", "door_handle_mount_bot", (hx, door_y - 0.006, hz - 0.016), (0.010, 0.008, 0.008), mat_gunmetal_handle)

        # -------------------------------------------------------------
        # 3. PRECISION COREXY GANTRY (`gantryX`) — Crisp metallic triple rails!
        # -------------------------------------------------------------
        gantry_z = 0.068
        self.add_cylinder("gantryX", "x_guide_front", (0.0, -0.028, gantry_z + 0.012), 0.0055, 0.326, "x", mat_steel)
        self.add_cylinder("gantryX", "x_guide_rear",  (0.0, -0.028, gantry_z - 0.012), 0.0055, 0.326, "x", mat_steel)
        self.add_cylinder("gantryX", "x_guide_top",   (0.0,  0.020, gantry_z + 0.022), 0.0050, 0.326, "x", mat_steel)
        self.add_box("gantryX", "x_slider_left",  (-0.160, -0.010, gantry_z), (0.022, 0.076, 0.036), mat_carbon)
        self.add_box("gantryX", "x_slider_right", ( 0.160, -0.010, gantry_z), (0.022, 0.076, 0.036), mat_carbon)

        self.add_cylinder("gantryX", "y_guide_left",  (-0.162, 0.0, gantry_z + 0.016), 0.0055, 0.255, "y", mat_steel)
        self.add_cylinder("gantryX", "y_guide_right", ( 0.162, 0.0, gantry_z + 0.016), 0.0055, 0.255, "y", mat_steel)

        self.add_cylinder("gantryX", "z_lead_left",  (-0.148, -0.042, -0.014), 0.0050, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_guide_left", (-0.148,  0.045, -0.014), 0.0055, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_right", ( 0.148,  0.000, -0.014), 0.0050, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_rear",  ( 0.000,  0.125, -0.014), 0.0055, 0.275, "z", mat_steel)

        for seg_i in range(9):
            cx_d = 0.026 + seg_i * 0.013
            self.add_box("gantryX", f"drag_chain_{seg_i}", (cx_d, 0.048, gantry_z + 0.026), (0.010, 0.016, 0.011), mat_interior_dark)

        # -------------------------------------------------------------
        # 4. SCULPTED TOOLHEAD (`printHead`) + Visible White PTFE Tube
        # -------------------------------------------------------------
        th_z = gantry_z - 0.004
        self.add_box("printHead", "toolhead_chassis",    (0.0, -0.004, th_z), (0.056, 0.044, 0.058), mat_carbon)
        self.add_box("printHead", "toolhead_front_cowl", (0.0, -0.028, th_z + 0.002), (0.052, 0.008, 0.052), mat_toolhead_face)
        self.add_cylinder("printHead", "toolhead_fan_shroud", (0.0, -0.033, th_z - 0.002), 0.015, 0.004, "y", mat_graphite)
        self.add_cylinder("printHead", "toolhead_fan_hub",    (0.0, -0.035, th_z - 0.002), 0.006, 0.004, "y", mat_toolhead_face)
        self.add_box("printHead", "toolhead_hotend_sock", (0.0, -0.004, th_z - 0.034), (0.020, 0.020, 0.014), mat_graphite)
        self.add_cylinder("printHead", "toolhead_nozzle", (0.0, -0.004, th_z - 0.044), 0.0035, 0.010, "z", mat_brass)

        ptfe_pts = []
        for i in range(12):
            t = i / 11.0
            px = 0.010 * math.sin(t * math.pi)
            py = -0.004 + t * 0.145
            pz = (th_z + 0.028) + 0.042 * math.sin(t * math.pi * 0.72) + t * 0.012
            ptfe_pts.append((px, py, pz))
        self.add_curved_tube("printHead", "ptfe_bowden_tube", ptfe_pts, 0.0040, mat_ptfe)

        # -------------------------------------------------------------
        # 5. PRINT BED & PEI PLATE (`printBed`)
        # -------------------------------------------------------------
        bed_z = -0.080
        self.add_box("printBed", "build_plate",        (0.0,  0.005, bed_z),         (0.268, 0.228, 0.004), mat_pei)
        self.add_box("printBed", "build_plate_lip",    (0.0, -0.112, bed_z),         (0.086, 0.012, 0.004), mat_toolhead_face)
        self.add_box("printBed", "bed_heater_block",   (0.0,  0.005, bed_z - 0.006), (0.264, 0.224, 0.008), mat_interior_dark)
        self.add_box("printBed", "bed_carriage_arm_l", (-0.102, 0.005, bed_z - 0.014), (0.028, 0.215, 0.012), mat_graphite)
        self.add_box("printBed", "bed_carriage_arm_r", ( 0.102, 0.005, bed_z - 0.014), (0.028, 0.215, 0.012), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_l",    (-0.148, 0.000, bed_z - 0.014), (0.026, 0.115, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_r",    ( 0.148, 0.000, bed_z - 0.014), (0.026, 0.035, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_rear", (0.0,    0.122, bed_z - 0.014), (0.050, 0.026, 0.014), mat_graphite)

        # -------------------------------------------------------------
        # 6. AEROSPACE ARCH BRACKET WITH 15 SUPPORT FINS (`printedObject`)
        # -------------------------------------------------------------
        obj_z = bed_z + 0.002
        self.add_box("printedObject", "bracket_base_raft", (0.0, 0.005, obj_z + 0.002), (0.168, 0.068, 0.004), mat_part_metal)
        arch_poly = [
            (-0.080, obj_z + 0.004),
            (-0.065, obj_z + 0.019),
            (-0.026, obj_z + 0.044),
            ( 0.026, obj_z + 0.044),
            ( 0.065, obj_z + 0.019),
            ( 0.080, obj_z + 0.004),
            ( 0.062, obj_z + 0.004),
            ( 0.022, obj_z + 0.032),
            (-0.022, obj_z + 0.032),
            (-0.062, obj_z + 0.004),
        ]
        self.add_extruded_polygon_y("printedObject", "bracket_swept_arch", arch_poly, -0.020, 0.030, mat_part_metal)
        self.add_cylinder("printedObject", "bracket_apex_ring", (0.0, 0.005, obj_z + 0.040), 0.014, 0.052, "y", mat_carbon)
        for f_i in range(15):
            fx = -0.060 + f_i * 0.0085
            fh = 0.032 - abs(fx) * 0.35
            self.add_box("printedObject", f"support_fin_{f_i}", (fx, 0.005, obj_z + 0.004 + fh / 2.0), (0.0020, 0.040, fh), mat_part_metal)

        # -------------------------------------------------------------
        # 7. Write GLB
        # -------------------------------------------------------------
        self.align()
        bin_chunk = bytes(self.bin)
        root_indices = [self.parents[p] for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]]

        gltf = {
            "asset": {"version": "2.0", "generator": "Antigravity True3D Photoreal Fidelity Builder (TASK-031 v3)"},
            "scene": 0,
            "scenes": [{"name": "P2S_True3D_V3_Scene", "nodes": root_indices}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "textures": self.textures,
            "images": self.images,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 10497, "wrapT": 10497}],
            "buffers": [{"byteLength": len(bin_chunk)}],
            "bufferViews": self.buffer_views,
            "accessors": self.accessors,
        }

        json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
        while len(json_bytes) % 4:
            json_bytes += b" "

        total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_chunk)
        header = struct.pack("<III", 0x46546C67, 2, total_length)
        j_hdr = struct.pack("<II", len(json_bytes), 0x4E4F534A)
        b_hdr = struct.pack("<II", len(bin_chunk), 0x004E4942)

        OUT_GLB.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_GLB, "wb") as f:
            f.write(header)
            f.write(j_hdr)
            f.write(json_bytes)
            f.write(b_hdr)
            f.write(bin_chunk)

        print(f"Generated True 3D V3 GLB: {OUT_GLB}")
        print(f"  Total Size: {total_length} bytes")
        print(f"  Nodes: {len(self.nodes)}, Meshes: {len(self.meshes)}, Materials: {len(self.materials)}, Images: {len(self.images)}")


if __name__ == "__main__":
    builder = True3DV3Builder()
    builder.build_scene()
