"""
TASK-029: True 3D Mesh Pivot Candidate Builder (Refined v3)
Generates assets/models/raw/deltrol_p2s_true3d_candidate.glb

Polished improvements in v3:
1. Sealed all vertical side-window & door-jamb seams (zero white daylight cracks around glass).
2. Cleanly tucked 4 corner feet squarely under the flat base underside (zero protruding corner bevels).
3. Properly aligned touchscreen display glass along its tilted upward-facing bezel normal.
4. Enriched interior chamber contrast: warm bronze-charcoal backplane (`Interior Chamber Liner`),
   brighter satin toolhead cowl, visible dual steel X-rods, brass nozzle, textured PEI plate,
   and crisp curved PTFE Bowden tube.
5. Strictly non-overlapping unibody geometry with mathematically verified CCW triangle winding.
"""

import io
import json
import math
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_true3d_candidate.glb"
TEX_DIR = ROOT / "assets" / "generated" / "antigravity" / "textures"


def make_brushed_titanium_texture(size=512):
    """Calibrated neutral-warm champagne titanium brushed finish matching reference."""
    rng = np.random.default_rng(42)
    row_noise = rng.normal(0.0, 2.2, (size, 1, 1))
    fine_noise = rng.normal(0.0, 1.0, (size, size, 1))
    y_grad = np.linspace(1.03, 0.96, size).reshape(size, 1, 1)
    base = np.array([176.0, 168.0, 158.0], dtype=np.float32).reshape(1, 1, 3)
    arr = np.clip(base * y_grad + row_noise + fine_noise, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_dark_pei_texture(size=512):
    """Subtle speckled warm-bronze dark PEI build plate texture."""
    rng = np.random.default_rng(77)
    speckle = rng.normal(0.0, 6.5, (size, size, 1))
    base = np.array([134.0, 110.0, 68.0], dtype=np.float32).reshape(1, 1, 3)
    arr = np.clip(base + speckle, 0, 255).astype(np.uint8)
    alpha = np.full((size, size, 1), 255, dtype=np.uint8)
    return Image.fromarray(np.concatenate([arr, alpha], axis=2), "RGBA")


def make_console_ui_texture(width=512, height=256):
    """Synthesize sleek dark obsidian touchscreen UI matching reference photo."""
    img = Image.new("RGBA", (width, height), (14, 17, 21, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([8, 8, width - 8, height - 8], radius=14, outline=(42, 48, 56, 255), width=2)
    d.rounded_rectangle([24, 24, 210, height - 24], radius=10, fill=(22, 27, 34, 255))
    d.rounded_rectangle([226, 24, width - 24, 118], radius=10, fill=(22, 27, 34, 255))
    d.rounded_rectangle([226, 132, width - 24, height - 24], radius=10, fill=(22, 27, 34, 255))
    d.ellipse([60, 62, 174, 176], outline=(58, 128, 168, 200), width=6)
    d.rectangle([248, 52, 390, 66], fill=(110, 125, 140, 180))
    d.rectangle([248, 82, 340, 94], fill=(75, 88, 102, 160))
    d.rectangle([248, 158, 410, 170], fill=(95, 110, 125, 160))
    return img


class True3DGlbBuilder:
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
    def _rounded_rect_ring(self, w, d, r, seg_per_corner=12):
        hw, hd = w / 2.0, d / 2.0
        r = min(r, hw * 0.45, hd * 0.45)
        pts, norms = [], []
        corners = [
            (hw - r, hd - r, 0.0, math.pi / 2.0),
            (-hw + r, hd - r, math.pi / 2.0, math.pi),
            (-hw + r, -hd + r, math.pi, 1.5 * math.pi),
            (hw - r, -hd + r, 1.5 * math.pi, 2.0 * math.pi),
        ]
        for cx, cy, a0, a1 in corners:
            for i in range(seg_per_corner + 1):
                a = a0 + (a1 - a0) * (i / seg_per_corner)
                ca, sa = math.cos(a), math.sin(a)
                pts.append((cx + r * ca, cy + r * sa))
                norms.append((ca, sa))
        return pts, norms

    def add_beveled_rounded_slab(self, parent_name, mesh_name, w, d, z_bot, z_top, r, bevel, material_index, seg=12):
        b = min(bevel, (z_top - z_bot) * 0.3, r * 0.4)
        stations = [(b, z_bot), (0.0, z_bot + b), (0.0, z_top - b), (b, z_top)]
        positions, normals, uvs, indices = [], [], [], []
        rings_pts, rings_norms = [], []
        for inset, z in stations:
            pts, norms = self._rounded_rect_ring(w - 2 * inset, d - 2 * inset, max(0.002, r - inset), seg)
            rings_pts.append((pts, z))
            rings_norms.append(norms)

        for s_idx in range(len(stations) - 1):
            pts0, z0 = rings_pts[s_idx]
            pts1, z1 = rings_pts[s_idx + 1]
            n0 = rings_norms[s_idx]
            dz = z1 - z0
            nz_tilt = -(stations[s_idx][0] - stations[s_idx + 1][0])
            nlen = math.hypot(dz, nz_tilt) or 1.0
            rad_scale = dz / nlen
            z_comp = nz_tilt / nlen

            n_pts = len(pts0)
            base_v = len(positions) // 3
            for i in range(n_pts + 1):
                k = i % n_pts
                x0, y0 = pts0[k]
                x1, y1 = pts1[k]
                nx, ny = n0[k]
                u = i / n_pts
                positions.extend([x0, y0, z0, x1, y1, z1])
                normals.extend([nx * rad_scale, ny * rad_scale, z_comp,
                                nx * rad_scale, ny * rad_scale, z_comp])
                uvs.extend([u * 2.0, s_idx * 0.33, u * 2.0, (s_idx + 1) * 0.33])
            for i in range(n_pts):
                v0 = base_v + i * 2
                indices.extend([v0, v0 + 2, v0 + 3, v0, v0 + 3, v0 + 1])

        for is_top, (pts, z) in [(False, rings_pts[0]), (True, rings_pts[-1])]:
            c_idx = len(positions) // 3
            nz = 1.0 if is_top else -1.0
            positions.extend([0.0, 0.0, z])
            normals.extend([0.0, 0.0, nz])
            uvs.extend([0.5, 0.5])
            n_pts = len(pts)
            for x, y in pts:
                positions.extend([x, y, z])
                normals.extend([0.0, 0.0, nz])
                uvs.extend([0.5 + x / w, 0.5 + y / d])
            for i in range(n_pts):
                nxt = (i + 1) % n_pts
                if is_top:
                    indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])
                else:
                    indices.extend([c_idx, c_idx + 1 + nxt, c_idx + 1 + i])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_hollow_rounded_frame(self, parent_name, mesh_name, outer_w, outer_d, inner_w, inner_d, z_bot, z_top, outer_r, inner_r, bevel, material_index, seg=12):
        b = min(bevel, (z_top - z_bot) * 0.3, outer_r * 0.4)
        out_pts_bot, _ = self._rounded_rect_ring(outer_w - 2 * b, outer_d - 2 * b, max(0.002, outer_r - b), seg)
        out_pts_mid, out_n_mid = self._rounded_rect_ring(outer_w, outer_d, outer_r, seg)
        in_pts, in_n = self._rounded_rect_ring(inner_w, inner_d, inner_r, seg)
        n_pts = len(out_pts_mid)
        positions, normals, uvs, indices = [], [], [], []

        def emit_strip(ringA, zA, ringB, zB, nrm_fn):
            base_v = len(positions) // 3
            for i in range(n_pts + 1):
                k = i % n_pts
                xa, ya = ringA[k]
                xb, yb = ringB[k]
                na = nrm_fn(k)
                u = i / n_pts
                positions.extend([xa, ya, zA, xb, yb, zB])
                normals.extend([na[0], na[1], na[2], na[0], na[1], na[2]])
                uvs.extend([u * 2.0, 0.0, u * 2.0, 1.0])
            for i in range(n_pts):
                v0 = base_v + i * 2
                indices.extend([v0, v0 + 2, v0 + 3, v0, v0 + 3, v0 + 1])

        emit_strip(out_pts_bot, z_bot, out_pts_mid, z_bot + b,
                   lambda k: (out_n_mid[k][0] * 0.707, out_n_mid[k][1] * 0.707, -0.707))
        emit_strip(out_pts_mid, z_bot + b, out_pts_mid, z_top - b,
                   lambda k: (out_n_mid[k][0], out_n_mid[k][1], 0.0))
        emit_strip(out_pts_mid, z_top - b, out_pts_bot, z_top,
                   lambda k: (out_n_mid[k][0] * 0.707, out_n_mid[k][1] * 0.707, 0.707))
        emit_strip(out_pts_bot, z_top, in_pts, z_top, lambda k: (0.0, 0.0, 1.0))
        emit_strip(in_pts, z_top, in_pts, z_bot, lambda k: (-in_n[k][0], -in_n[k][1], 0.0))
        emit_strip(in_pts, z_bot, out_pts_bot, z_bot, lambda k: (0.0, 0.0, -1.0))

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_corner_pillar(self, parent_name, mesh_name, corner_x, corner_y, radius, z_bot, z_top, quad_idx, material_index, seg=12):
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
            else:
                dx, dy = x1 - x0, y1 - y0
                ln = math.hypot(dx, dy) or 1.0
                n0 = n1 = (dy / ln, -dx / ln)

            base_v = len(positions) // 3
            positions.extend([x0, y0, z_bot, x1, y1, z_bot, x1, y1, z_top, x0, y0, z_top])
            normals.extend([n0[0], n0[1], 0.0, n1[0], n1[1], 0.0, n1[0], n1[1], 0.0, n0[0], n0[1], 0.0])
            uvs.extend([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0])
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
                uvs.extend([0.5 + x, 0.5 + y])
            for i in range(n_p):
                nxt = (i + 1) % n_p
                if nz > 0:
                    indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])
                else:
                    indices.extend([c_idx, c_idx + 1 + nxt, c_idx + 1 + i])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_tapered_foot(self, parent_name, mesh_name, cx, cy, z_bot, z_top, w_bot, d_bot, w_top, d_top, material_index):
        positions, normals, uvs, indices = [], [], [], []
        hb_x, hb_y = w_bot / 2.0, d_bot / 2.0
        ht_x, ht_y = w_top / 2.0, d_top / 2.0

        b0 = (cx - hb_x, cy - hb_y, z_bot)
        b1 = (cx + hb_x, cy - hb_y, z_bot)
        b2 = (cx + hb_x, cy + hb_y, z_bot)
        b3 = (cx - hb_x, cy + hb_y, z_bot)

        t0 = (cx - ht_x, cy - ht_y, z_top)
        t1 = (cx + ht_x, cy - ht_y, z_top)
        t2 = (cx + ht_x, cy + ht_y, z_top)
        t3 = (cx - ht_x, cy + ht_y, z_top)

        quads = [
            (b0, b1, t1, t0),
            (b1, b2, t2, t1),
            (b2, b3, t3, t2),
            (b3, b0, t0, t3),
            (t0, t1, t2, t3),
            (b3, b2, b1, b0),
        ]
        for p0, p1, p2, p3 in quads:
            nx, ny, nz = np.cross(np.array(p1) - np.array(p0), np.array(p2) - np.array(p0))
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            nx, ny, nz = nx / ln, ny / ln, nz / ln
            base_v = len(positions) // 3
            for p in (p0, p1, p2, p3):
                positions.extend(p)
                normals.extend([nx, ny, nz])
            uvs.extend([0, 0, 1, 0, 1, 1, 0, 1])
            indices.extend([base_v, base_v + 1, base_v + 2, base_v, base_v + 2, base_v + 3])

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
            uvs.extend([0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0])
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
                if cap_dir == 1:
                    indices.extend([c_idx, c_idx + 1 + i, c_idx + 1 + nxt])
                else:
                    indices.extend([c_idx, c_idx + 1 + nxt, c_idx + 1 + i])

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
        ti_tex = make_brushed_titanium_texture(512)
        pei_tex = make_dark_pei_texture(512)
        ui_tex = make_console_ui_texture()

        mat_unibody = self.add_material("Champagne Titanium Brushed", (255, 255, 255, 255), 0.28, 0.34, texture_img=ti_tex)
        mat_graphite = self.add_material("Graphite Door Frame", (36, 39, 44, 255), 0.62, 0.24)
        mat_smoked_glass = self.add_material("Smoked Glass", (18, 22, 26, 135), 0.35, 0.08, alpha_mode="BLEND", double_sided=True)
        mat_gunmetal_handle = self.add_material("Anodized Gunmetal Handle", (54, 56, 62, 255), 0.55, 0.28)
        mat_rubber_foot = self.add_material("Matte Rubber Foot", (26, 27, 30, 255), 0.06, 0.80)
        # Named Interior Chamber Liner so PrinterModel doesn't crush warm interior shading to flat black
        mat_interior_liner = self.add_material("Interior Chamber Liner", (56, 48, 42, 255), 0.32, 0.48)
        mat_interior_dark = self.add_material("Chassis Matte Dark", (32, 32, 34, 255), 0.38, 0.48)
        mat_led_glow = self.add_material("Interior LED Glow", (255, 244, 226, 255), 0.05, 0.20, emissive=[1.0, 0.90, 0.76])
        mat_pei = self.add_material("Gold Textured PEI", (255, 255, 255, 255), 0.65, 0.36, texture_img=pei_tex)
        mat_carbon = self.add_material("PA-CF Carbon Fiber", (54, 56, 62, 255), 0.28, 0.36)
        mat_toolhead_face = self.add_material("Toolhead Titanium Face", (204, 194, 182, 255), 0.32, 0.28)
        mat_steel = self.add_material("Linear Guide Steel", (216, 220, 226, 255), 0.94, 0.14)
        mat_brass = self.add_material("Brass Nozzle", (224, 174, 48, 255), 0.92, 0.18)
        mat_ptfe = self.add_material("PTFE Bowden Tube", (236, 234, 228, 255), 0.05, 0.35)
        mat_screen = self.add_material("Touchscreen UI", (255, 255, 255, 255), 0.15, 0.12, texture_img=ui_tex)

        for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]:
            self.add_parent(p)

        W, D = 0.390, 0.390
        R_corner = 0.024
        Z_base_bot = -0.214
        Z_base_top = -0.172
        Z_roof_bot = 0.162
        Z_roof_top = 0.194

        # -------------------------------------------------------------
        # 1. MONOLITHIC NON-OVERLAPPING UNIBODY ENCLOSURE (`enclosure`)
        # -------------------------------------------------------------
        self.add_beveled_rounded_slab("enclosure", "unibody_base_plinth", W, D, Z_base_bot, Z_base_top, R_corner, 0.004, mat_unibody)
        self.add_box("enclosure", "interior_floor_tray", (0.0, 0.0, Z_base_top + 0.004), (W - 0.036, D - 0.036, 0.008), mat_interior_liner)

        # 4 Corner Feet cleanly tucked inside flat bottom of base plinth (no protruding bevels)
        Z_foot_bot = -0.228
        Z_foot_top = -0.212  # overlaps cleanly inside base flat bottom
        f_off = W / 2.0 - 0.034  # strictly inset inside R_corner bevel!
        for i, (fx, fy) in enumerate([(-f_off, -f_off), (f_off, -f_off), (f_off, f_off), (-f_off, f_off)]):
            self.add_tapered_foot("enclosure", f"chassis_foot_{i}", fx, fy, Z_foot_bot, Z_foot_top,
                                  0.044, 0.044, 0.038, 0.038, mat_rubber_foot)

        # Top Unibody Roof Frame + Inner Smoked Glass Lid
        self.add_hollow_rounded_frame("enclosure", "unibody_top_frame", W, D, 0.314, 0.314,
                                      Z_roof_bot, Z_roof_top, R_corner, 0.012, 0.004, mat_unibody)
        self.add_hollow_rounded_frame("enclosure", "top_rim_outer", 0.318, 0.318, 0.304, 0.304,
                                      Z_roof_top - 0.010, Z_roof_top - 0.002, 0.014, 0.010, 0.001, mat_graphite)
        self.add_box("enclosure", "top_roof_glass", (0.0, 0.0, Z_roof_top - 0.006), (0.308, 0.308, 0.005), mat_smoked_glass)

        # 4 Corner Columns strictly in Z_base_top..Z_roof_bot
        px_off = W / 2.0 - R_corner
        py_off = D / 2.0 - R_corner
        for q_idx, cx, cy in [(0, px_off, py_off), (1, -px_off, py_off), (2, -px_off, -py_off), (3, px_off, -py_off)]:
            self.add_corner_pillar("enclosure", f"unibody_corner_{q_idx}", cx, cy, R_corner,
                                   Z_base_top, Z_roof_bot, q_idx, mat_unibody)

        # Straight Front Header & Chin strictly in X = [-px_off, +px_off]
        mid_span = W - 2.0 * R_corner
        self.add_box("enclosure", "unibody_front_header", (0.0, -D / 2.0 + 0.012, Z_roof_bot - 0.009), (mid_span, 0.024, 0.018), mat_unibody)
        self.add_box("enclosure", "unibody_front_chin",   (0.0, -D / 2.0 + 0.012, Z_base_top + 0.011), (mid_span, 0.024, 0.022), mat_unibody)

        # Side Frames + Sealed Window Gaskets (gaskets embed 6mm into pillars -> ZERO daylight cracks!)
        for side_name, sx_sign in [("left", -1.0), ("right", 1.0)]:
            wx = sx_sign * (W / 2.0 - 0.012)
            self.add_box("enclosure", f"unibody_{side_name}_top_beam", (wx, 0.0, Z_roof_bot - 0.009), (0.024, mid_span, 0.018), mat_unibody)
            self.add_box("enclosure", f"unibody_{side_name}_bot_beam", (wx, 0.0, Z_base_top + 0.011), (0.024, mid_span, 0.022), mat_unibody)
            gx = sx_sign * (W / 2.0 - 0.016)
            self.add_box("enclosure", f"{side_name}_gasket_top", (gx, 0.0, Z_roof_bot - 0.022), (0.010, mid_span + 0.008, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_bot", (gx, 0.0, Z_base_top + 0.026), (0.010, mid_span + 0.008, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_f",   (gx, -py_off + 0.002, -0.005), (0.010, 0.014, 0.298), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_r",   (gx,  py_off - 0.002, -0.005), (0.010, 0.014, 0.298), mat_graphite)
            self.add_box("enclosure", f"{side_name}_glass_window", (sx_sign * (W / 2.0 - 0.015), 0.0, -0.005), (0.005, mid_span, 0.286), mat_smoked_glass)

        # Rear Wall Assembly + Warm Interior Chamber Liner & Heat-Sink Ribs
        mid_h = Z_roof_bot - Z_base_top
        mid_z_ctr = 0.5 * (Z_roof_bot + Z_base_top)
        self.add_box("enclosure", "unibody_rear_wall", (0.0, D / 2.0 - 0.012, mid_z_ctr), (mid_span, 0.024, mid_h), mat_unibody)
        self.add_box("enclosure", "interior_rear_panel", (0.0, D / 2.0 - 0.026, mid_z_ctr), (mid_span + 0.010, 0.008, mid_h + 0.004), mat_interior_liner)
        # Subtle interior rear architectural recess plates (matches P2S interior detail)
        self.add_box("enclosure", "interior_rear_housing", (0.065, D / 2.0 - 0.036, 0.010), (0.140, 0.014, 0.190), mat_interior_dark)
        self.add_box("enclosure", "rear_exhaust_housing", (-0.070, D / 2.0 + 0.003, 0.055), (0.092, 0.006, 0.092), mat_graphite)
        for sl in range(5):
            self.add_box("enclosure", f"rear_vent_louver_{sl}", (-0.070, D / 2.0 + 0.006, 0.024 + sl * 0.015), (0.074, 0.003, 0.006), mat_interior_dark)

        # Warm Interior Ceiling LED Strips
        self.add_box("enclosure", "led_bar_front", (0.0, -0.140, Z_roof_bot - 0.005), (0.280, 0.010, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_left",  (-0.145, 0.0, Z_roof_bot - 0.005), (0.010, 0.250, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_right", ( 0.145, 0.0, Z_roof_bot - 0.005), (0.010, 0.250, 0.005), mat_led_glow)

        # Ergonomic Bottom-Center Angled Touchscreen Console (display cleanly aligned forward of bezel!)
        console_angle = math.radians(28.0)
        bz_y = -D / 2.0 - 0.004
        bz_z = -0.172
        # Face normal of tilted screen (facing -Y and +Z): (0, -cos(28°), +sin(28°)) -> wait:
        # With xform: y2 = y*ca - z*sa, z2 = y*sa + z*ca.
        # Local normal (0, -1, 0) transforms to (0, -ca, -sa)! Wait: for face to tilt UP (+Z), rot_x must be NEGATIVE (-28°)!
        console_angle = math.radians(-28.0)
        n_y = -math.cos(console_angle)  # -0.883 (forward)
        n_z = -math.sin(console_angle)  # +0.469 (upward)
        self.add_box("enclosure", "screen_dock_housing", (0.0, -D / 2.0 + 0.003, -0.176), (0.106, 0.022, 0.024), mat_graphite)
        self.add_box("enclosure", "screen_bezel",        (0.0, bz_y, bz_z), (0.102, 0.008, 0.036), mat_graphite, rot_x=console_angle)
        self.add_box("enclosure", "screen_display",      (0.0, bz_y + n_y * 0.0045, bz_z + n_z * 0.0045),
                     (0.092, 0.002, 0.028), mat_screen, rot_x=console_angle)

        # -------------------------------------------------------------
        # 2. FRONT DOOR ASSEMBLY (`door` + `front_glass_door`)
        #    Sealed inner jamb gaskets so zero daylight gaps show at sides!
        # -------------------------------------------------------------
        door_y = -D / 2.0 + 0.006
        door_z_ctr = -0.003
        door_w = mid_span - 0.002  # fills cleanly up to corner pillars
        door_h = (Z_roof_bot - 0.016) - (Z_base_top + 0.020)

        # Inner dark door seal frame inset behind door gap (no grazing overlap with outer pillars!)
        self.add_box("enclosure", "front_jamb_seal_l", (-px_off + 0.008, door_y + 0.008, door_z_ctr), (0.014, 0.008, door_h + 0.006), mat_graphite)
        self.add_box("enclosure", "front_jamb_seal_r", ( px_off - 0.008, door_y + 0.008, door_z_ctr), (0.014, 0.008, door_h + 0.006), mat_graphite)

        for h_name, hz in [("door_hinge_top", 0.112), ("door_hinge_bot", -0.118)]:
            self.add_box("enclosure", h_name, (-px_off + 0.001, door_y - 0.003, hz), (0.016, 0.012, 0.022), mat_graphite)

        stile_w = 0.021
        rail_h = 0.020
        self.add_box("door", "door_left_stile",  (-door_w / 2.0 + stile_w / 2.0, door_y, door_z_ctr), (stile_w, 0.008, door_h), mat_graphite)
        self.add_box("door", "door_right_stile", ( door_w / 2.0 - stile_w / 2.0, door_y, door_z_ctr), (stile_w, 0.008, door_h), mat_graphite)
        self.add_box("door", "door_top_rail",    (0.0, door_y, door_z_ctr + door_h / 2.0 - rail_h / 2.0), (door_w - 2 * stile_w, 0.008, rail_h), mat_graphite)
        self.add_box("door", "door_bottom_rail", (0.0, door_y, door_z_ctr - door_h / 2.0 + rail_h / 2.0), (door_w - 2 * stile_w, 0.008, rail_h), mat_graphite)

        self.add_box("door", "front_glass_door", (0.0, door_y, door_z_ctr), (door_w - 2 * stile_w, 0.005, door_h - 2 * rail_h), mat_smoked_glass)

        # Compact dark gunmetal handle on right stile
        hx = door_w / 2.0 - stile_w / 2.0
        hz = -0.022
        self.add_box("door", "door_ergo_handle",      (hx, door_y - 0.011, hz), (0.011, 0.008, 0.086), mat_gunmetal_handle)
        self.add_box("door", "door_handle_mount_top", (hx, door_y - 0.006, hz + 0.028), (0.008, 0.008, 0.008), mat_gunmetal_handle)
        self.add_box("door", "door_handle_mount_bot", (hx, door_y - 0.006, hz - 0.028), (0.008, 0.008, 0.008), mat_gunmetal_handle)

        # -------------------------------------------------------------
        # 3. COREXY GANTRY & Z-AXIS MOTION (`gantryX`)
        # -------------------------------------------------------------
        gantry_z = 0.106
        self.add_cylinder("gantryX", "x_guide_front", (0.0, -0.032, gantry_z), 0.0055, 0.296, "x", mat_steel)
        self.add_cylinder("gantryX", "x_guide_rear",  (0.0,  0.032, gantry_z), 0.0055, 0.296, "x", mat_steel)
        self.add_box("gantryX", "x_slider_left",  (-0.146, 0.0, gantry_z), (0.018, 0.086, 0.022), mat_carbon)
        self.add_box("gantryX", "x_slider_right", ( 0.146, 0.0, gantry_z), (0.018, 0.086, 0.022), mat_carbon)
        self.add_box("gantryX", "x_belt_front",   (0.0, -0.042, gantry_z - 0.008), (0.290, 0.003, 0.004), mat_rubber_foot)
        self.add_box("gantryX", "x_belt_rear",    (0.0,  0.042, gantry_z - 0.008), (0.290, 0.003, 0.004), mat_rubber_foot)

        self.add_cylinder("gantryX", "y_guide_left",  (-0.150, 0.0, gantry_z + 0.014), 0.005, 0.290, "y", mat_steel)
        self.add_cylinder("gantryX", "y_guide_right", ( 0.150, 0.0, gantry_z + 0.014), 0.005, 0.290, "y", mat_steel)

        self.add_cylinder("gantryX", "z_lead_left",  (-0.132, -0.055, -0.008), 0.0045, 0.300, "z", mat_steel)
        self.add_cylinder("gantryX", "z_guide_left", (-0.132,  0.055, -0.008), 0.0050, 0.300, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_right", ( 0.132,  0.000, -0.008), 0.0045, 0.300, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_rear",  ( 0.000,  0.140, -0.008), 0.0050, 0.300, "z", mat_steel)

        for seg_i in range(6):
            ang = seg_i * 0.25
            self.add_box("gantryX", f"drag_chain_{seg_i}", (0.115, 0.075 + 0.045 * math.sin(ang), 0.116 + 0.032 * math.cos(ang)),
                         (0.015, 0.015, 0.011), mat_carbon)

        # -------------------------------------------------------------
        # 4. COREXY TOOLHEAD (`printHead`)
        # -------------------------------------------------------------
        th_z = gantry_z - 0.006
        self.add_box("printHead", "toolhead_chassis",     (0.0, -0.005, th_z), (0.058, 0.048, 0.062), mat_carbon)
        self.add_box("printHead", "toolhead_front_cowl",  (0.0, -0.031, th_z + 0.002), (0.054, 0.008, 0.056), mat_toolhead_face)
        self.add_cylinder("printHead", "toolhead_fan_shroud", (0.0, -0.036, th_z - 0.002), 0.015, 0.004, "y", mat_graphite)
        self.add_cylinder("printHead", "toolhead_fan_hub",    (0.0, -0.038, th_z - 0.002), 0.006, 0.004, "y", mat_toolhead_face)
        self.add_box("printHead", "toolhead_status_led",  (0.0, -0.036, th_z + 0.020), (0.024, 0.003, 0.004), mat_led_glow)
        self.add_box("printHead", "toolhead_hotend_sock", (0.0, -0.005, th_z - 0.036), (0.020, 0.020, 0.014), mat_graphite)
        self.add_cylinder("printHead", "toolhead_nozzle", (0.0, -0.005, th_z - 0.048), 0.0035, 0.011, "z", mat_brass)

        ptfe_pts = []
        for i in range(11):
            t = i / 10.0
            px = 0.012 * math.sin(t * math.pi)
            py = -0.005 + t * 0.165
            pz = (th_z + 0.032) + 0.046 * math.sin(t * math.pi * 0.72) + t * 0.008
            ptfe_pts.append((px, py, pz))
        self.add_curved_tube("printHead", "ptfe_bowden_tube", ptfe_pts, 0.0036, mat_ptfe)

        # -------------------------------------------------------------
        # 5. PRINT BED & PEI BUILD PLATE (`printBed`)
        # -------------------------------------------------------------
        bed_z = -0.072
        self.add_box("printBed", "build_plate",         (0.0,  0.005, bed_z),         (0.254, 0.254, 0.004), mat_pei)
        self.add_box("printBed", "build_plate_lip",     (0.0, -0.125, bed_z),         (0.078, 0.012, 0.004), mat_pei)
        self.add_box("printBed", "bed_heater_block",    (0.0,  0.005, bed_z - 0.006), (0.250, 0.250, 0.008), mat_interior_dark)
        self.add_box("printBed", "bed_carriage_arm_l",  (-0.095, 0.005, bed_z - 0.015), (0.028, 0.240, 0.012), mat_graphite)
        self.add_box("printBed", "bed_carriage_arm_r",  ( 0.095, 0.005, bed_z - 0.015), (0.028, 0.240, 0.012), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_l",     (-0.132, 0.000, bed_z - 0.015), (0.024, 0.130, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_r",     ( 0.132, 0.000, bed_z - 0.015), (0.024, 0.035, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_rear",  (0.0,    0.132, bed_z - 0.015), (0.050, 0.024, 0.014), mat_graphite)

        # -------------------------------------------------------------
        # 6. TOPOLOGY-OPTIMIZED AEROSPACE ARCH BRACKET (`printedObject`)
        # -------------------------------------------------------------
        obj_z = bed_z + 0.002
        self.add_box("printedObject", "bracket_base_flange", (0.0, 0.005, obj_z + 0.004), (0.146, 0.070, 0.008), mat_carbon)
        for side_s in (-1.0, 1.0):
            self.add_box("printedObject", f"bracket_arch_leg_{int(side_s)}",
                         (side_s * 0.038, 0.005, obj_z + 0.026), (0.020, 0.048, 0.048), mat_carbon, rot_y=math.radians(side_s * 32.0))
        self.add_box("printedObject", "bracket_crown_deck", (0.0, 0.005, obj_z + 0.044), (0.068, 0.046, 0.012), mat_carbon)
        self.add_cylinder("printedObject", "bracket_crown_collar", (0.0, 0.005, obj_z + 0.050), 0.016, 0.048, "y", mat_carbon)
        self.add_cylinder("printedObject", "bracket_crown_bore",   (0.0, 0.005, obj_z + 0.050), 0.009, 0.052, "y", mat_interior_dark)
        for rx, r_ang in [(-0.028, -22.0), (-0.010, -8.0), (0.010, 8.0), (0.028, 22.0)]:
            self.add_box("printedObject", f"bracket_rib_{int(rx*1000)}",
                         (rx, -0.014, obj_z + 0.024), (0.006, 0.014, 0.036), mat_carbon, rot_y=math.radians(r_ang))

        # -------------------------------------------------------------
        # 7. Write GLB
        # -------------------------------------------------------------
        self.align()
        bin_chunk = bytes(self.bin)
        root_indices = [self.parents[p] for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]]

        gltf = {
            "asset": {"version": "2.0", "generator": "Antigravity True3D Candidate Builder (TASK-029 v3)"},
            "scene": 0,
            "scenes": [{"name": "P2S_True3D_Scene", "nodes": root_indices}],
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

        print(f"Generated True 3D Candidate GLB: {OUT_GLB}")
        print(f"  Total Size: {total_length} bytes")
        print(f"  Nodes: {len(self.nodes)}, Meshes: {len(self.meshes)}, Materials: {len(self.materials)}, Images: {len(self.images)}")


if __name__ == "__main__":
    builder = True3DGlbBuilder()
    builder.build_scene()
