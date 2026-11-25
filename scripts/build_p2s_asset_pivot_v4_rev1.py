"""
TASK-033: Base Geometry Integrity & Reference Fidelity Revision (v4_rev1)
Reference-Derived Multi-View Surface Unwarping + Connected Hard-Surface 3D Reconstruction
Generates: assets/models/raw/deltrol_p2s_asset_pivot_v4_rev1.glb

Key Fixes over TASK-032 (v4):
1. Zero white background bleed in reference-unwarped surface textures (`side_bot`,
   `side_top`, `pillar_l`, `chin`, `hinge`), verified via strict pixel checks.
2. Eliminated lower-base white wedge / open skirt seams:
   - Replaced concave polygon fan-triangulation skirts with watertight convex segments.
   - Added full-depth dark recessed chassis underbody plinth (`chassis_recessed_plinth`)
     spanning Z_leg_bot + 0.004 .. Z_chin_top so no background shows through side arches.
   - Centered corner rubber feet strictly beneath leg footprints (zero side overhang).
3. Extended rounded front-right & left corner pillars continuously from foot to top roof
   chamfer (`Z_leg_bot .. Z_roof_top - 0.0025`) with non-overlapping top crown cap.
4. Upgraded front 3/4 fidelity: sleeker dark-bronze console housing + obsidian screen glass,
   compact door arch hood, and warm studio-amber chamber radiosity calibrated for 52%
   Smoked Glass transmittance (`PrinterModel.jsx`).
"""

import io
import json
import math
import struct
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
REF_PATH = ROOT / "assets" / "source" / "printer-hero-reference-2026-11-23.png"
MV_DIR = ROOT / "assets" / "generated" / "antigravity" / "multiview"
OUT_GLB = ROOT / "assets" / "models" / "raw" / "deltrol_p2s_asset_pivot_v4_rev1.glb"


def unwarp_quad(img: Image.Image, quad_pts, out_size=(256, 256), shrink_px=1):
    """
    Perspective-unwarps a 4-point quad (tl, bl, br, tr) in reference pixel coords
    into a rectangular surface map, inset slightly to prevent background bleed.
    """
    tl, bl, br, tr = [np.array(p, dtype=np.float32) for p in quad_pts]
    ctr = 0.25 * (tl + bl + br + tr)
    if shrink_px != 0:
        def move_in(p):
            v = ctr - p
            ln = np.linalg.norm(v) or 1.0
            return p + (v / ln) * shrink_px
        tl, bl, br, tr = move_in(tl), move_in(bl), move_in(br), move_in(tr)
    data = (tl[0], tl[1], bl[0], bl[1], br[0], br[1], tr[0], tr[1])
    return img.transform(out_size, Image.Transform.QUAD, data=data, resample=Image.Resampling.BICUBIC)


def _clamp_bright(im: Image.Image, max_val=232) -> Image.Image:
    """Clamps accidental white studio edge highlights so unwarped metal never reads white."""
    arr = np.array(im, dtype=np.float32)
    lum = arr.mean(axis=2, keepdims=True)
    scale = np.where(lum > max_val, max_val / np.maximum(lum, 1.0), 1.0)
    return Image.fromarray(np.clip(arr * scale, 0, 255).astype(np.uint8), "RGB")


def build_baked_surface_textures():
    ref = Image.open(REF_PATH).convert("RGB")
    arr_ref = np.array(ref, dtype=np.float32)

    # 1. Forehead beam (pure champagne brushed metal with top-right diagonal soft shadow)
    tex_forehead = unwarp_quad(ref, [(647, 172), (647, 204), (892, 197), (892, 161)], (512, 128), shrink_px=1)

    # 2. Front-Right Rounded Pillar (continuous liquid-metal ribbon from roof chamfer to foot)
    tex_pillar_r = unwarp_quad(ref, [(894, 162), (894, 533), (934, 533), (934, 162)], (256, 512), shrink_px=1)

    # 3. Front-Left Corner Pillar (strictly inside metallic edge, clamped against studio bleed)
    tex_pillar_l = _clamp_bright(
        unwarp_quad(ref, [(633, 178), (633, 518), (640, 518), (640, 178)], (128, 512), shrink_px=1),
        max_val=226,
    )

    # 4. Front Chin Skirt (sampled strictly inside champagne metal y<=528, zero floor shadow bleed)
    chin_l = np.array(unwarp_quad(ref, [(648, 492), (648, 526), (707, 528), (707, 493)], (160, 128), shrink_px=1))
    chin_r = np.array(unwarp_quad(ref, [(846, 494), (846, 529), (892, 528), (892, 493)], (160, 128), shrink_px=1))
    mid_col_l = chin_l[:, -4:].mean(axis=1, keepdims=True)
    mid_col_r = chin_r[:, :4].mean(axis=1, keepdims=True)
    t_mix = np.linspace(0.0, 1.0, 192).reshape(1, 192, 1)
    chin_mid = np.clip(mid_col_l * (1.0 - t_mix) + mid_col_r * t_mix, 0, 255).astype(np.uint8)
    tex_chin = _clamp_bright(Image.fromarray(np.concatenate([chin_l, chin_mid, chin_r], axis=1), "RGB"), max_val=224)

    # 5. Shaded Right Side Upper Beam, Smooth Gradient Right Lower Skirt (zero rear-tab bright jump!), Left Skirt & Rear Post
    tex_side_top = _clamp_bright(
        unwarp_quad(ref, [(944, 164), (944, 194), (1034, 197), (1034, 176)], (256, 128), shrink_px=1),
        max_val=215,
    )
    # Sample uniform dark shaded right-side champagne band x=944..992 so rear leg matches arch smoothly
    raw_sb = np.array(
        unwarp_quad(ref, [(944, 500), (944, 514), (988, 510), (988, 497)], (256, 128), shrink_px=1),
        dtype=np.float32,
    )
    # Smooth gentle front-to-rear tonal falloff across the side skirt (zero sudden rear tan block!)
    u_sb = np.linspace(1.0, 0.82, 256).reshape(1, 256, 1)
    tex_side_bot = _clamp_bright(Image.fromarray(np.clip(raw_sb * u_sb, 0, 255).astype(np.uint8), "RGB"), max_val=175)

    # Left lower skirt derived cleanly from front-left champagne metal
    left_arr = np.array(tex_chin.resize((256, 128), Image.Resampling.BICUBIC), dtype=np.float32)
    tex_left_bot = Image.fromarray(np.clip(left_arr * np.array([1.02, 1.01, 0.99]), 0, 220).astype(np.uint8), "RGB")

    # Rear corner post graded smoothly toward rear-right tone so no bright foot spot appears
    raw_srp = np.array(
        unwarp_quad(ref, [(1020, 176), (1020, 512), (1034, 510), (1034, 177)], (128, 512), shrink_px=1),
        dtype=np.float32,
    )
    v_srp = np.linspace(1.0, 0.72, 512).reshape(512, 1, 1)
    tex_side_rear_post = _clamp_bright(Image.fromarray(np.clip(raw_srp * v_srp, 0, 255).astype(np.uint8), "RGB"), max_val=175)

    # 6. Door Hinges & Door Handle (hinge inset inside metallic block so zero white canvas)
    tex_hinge = _clamp_bright(
        unwarp_quad(ref, [(636, 215), (636, 238), (645, 238), (645, 215)], (64, 128), shrink_px=1),
        max_val=224,
    )
    tex_handle = unwarp_quad(ref, [(885, 338), (885, 394), (900, 394), (900, 338)], (64, 192), shrink_px=0)

    # 7. Sleek Smoked-Obsidian Console Screen (clean glass gradient + subtle diagonal upper sheen)
    u_g = np.linspace(0.0, 1.0, 512).reshape(1, 512, 1)
    v_g = np.linspace(0.0, 1.0, 192).reshape(192, 1, 1)
    sheen = np.clip(1.0 - np.abs((0.62 * u_g + 0.58 * v_g) - 0.34) * 3.8, 0.0, 1.0)
    con_base = np.array([22.0, 21.0, 20.0], dtype=np.float32).reshape(1, 1, 3)
    con_sheen = np.array([58.0, 50.0, 42.0], dtype=np.float32).reshape(1, 1, 3)
    tex_console = Image.fromarray(np.clip(con_base + con_sheen * (sheen ** 1.6), 0, 255).astype(np.uint8), "RGB")

    # 8. Toolhead Front Cover (champagne cowl & fan shroud)
    tex_toolhead = unwarp_quad(ref, [(811, 248), (811, 288), (839, 288), (839, 248)], (256, 256), shrink_px=1)

    # 9. Printed Turbine Bracket Surface (swept warm alloy arch + lattice texture)
    tex_bracket = unwarp_quad(ref, [(742, 386), (726, 419), (854, 421), (836, 388)], (512, 192), shrink_px=0)

    # 10. Warm Amber Chamber Backplane & Side Liners (linear-compensated for 52% #12161a Smoked Glass!)
    left_glow_raw = unwarp_quad(ref, [(690, 286), (690, 405), (764, 405), (764, 286)], (256, 256), shrink_px=2)
    top_glow_rgb = arr_ref[224:240, 828:860].mean(axis=(0, 1))
    lg_arr = np.array(left_glow_raw.filter(ImageFilter.GaussianBlur(12)), dtype=np.float32)
    v_lin = np.linspace(1.0, 0.0, 256).reshape(256, 1, 1)
    amber_top = np.clip(top_glow_rgb * np.array([2.15, 1.85, 1.50]), 0, 255).reshape(1, 1, 3)
    chamber_arr = np.clip(lg_arr * np.array([2.10, 1.78, 1.42]) * (1.0 - 0.45 * v_lin) + amber_top * 0.45 * v_lin, 0, 255).astype(np.uint8)
    tex_chamber = Image.fromarray(chamber_arr, "RGB")

    # Warm lit lower chamber/electronics bronze-amber glow panel (visible through right glass & rear-right)
    el_arr = np.clip(chamber_arr * 0.78, 0, 255).astype(np.uint8)
    tex_chamber_bronze = Image.fromarray(el_arr, "RGB")

    # 11. Multi-view Rear Wall Texture (color-graded to warm titanium-champagne)
    rear_path = MV_DIR / "p2s_multiview_rear.jpg"
    if rear_path.exists():
        mv_rear = Image.open(rear_path).convert("RGB").crop((260, 130, 940, 790)).resize((512, 512), Image.Resampling.LANCZOS)
        r_arr = np.array(mv_rear, dtype=np.float32)
        r_arr[..., 0] = np.clip(r_arr[..., 0] * 0.62, 0, 255)
        r_arr[..., 1] = np.clip(r_arr[..., 1] * 0.56, 0, 255)
        r_arr[..., 2] = np.clip(r_arr[..., 2] * 0.49, 0, 255)
        tex_rear = Image.fromarray(r_arr.astype(np.uint8), "RGB")
    else:
        tex_rear = tex_side_rear_post.resize((512, 512))

    # 12. Gold-Bronze PEI Bed Texture
    rng = np.random.default_rng(77)
    pei_base = np.array([188.0, 152.0, 102.0], dtype=np.float32).reshape(1, 1, 3)
    pei_arr = np.clip(pei_base + rng.normal(0.0, 5.5, (512, 512, 1)), 0, 255).astype(np.uint8)
    tex_pei = Image.fromarray(pei_arr, "RGB")

    textures = {
        "forehead": tex_forehead,
        "pillar_r": tex_pillar_r,
        "pillar_l": tex_pillar_l,
        "chin": tex_chin,
        "side_top": tex_side_top,
        "side_bot": tex_side_bot,
        "left_bot": tex_left_bot,
        "side_rear_post": tex_side_rear_post,
        "hinge": tex_hinge,
        "handle": tex_handle,
        "console": tex_console,
        "toolhead": tex_toolhead,
        "bracket": tex_bracket,
        "chamber": tex_chamber,
        "chamber_bronze": tex_chamber_bronze,
        "rear": tex_rear,
        "pei": tex_pei,
    }
    # Assert zero bright studio white bleed (>240 RGB across all 3 channels) in exterior metal maps
    for k in ("forehead", "chin", "side_top", "side_bot", "left_bot", "pillar_l", "side_rear_post", "hinge"):
        a = np.array(textures[k])
        bleed = float(((a[..., 0] > 236) & (a[..., 1] > 236) & (a[..., 2] > 236)).mean())
        assert bleed == 0.0, f"Background white bleed detected in texture '{k}': {bleed:.4f}"

    return {k: v.convert("RGBA") for k, v in textures.items()}


class PivotV4Rev1GlbBuilder:
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
        self.tex_cache = {}

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

    def _embed_texture(self, name, texture_img):
        if name in self.tex_cache:
            return self.tex_cache[name]
        stream = io.BytesIO()
        texture_img.save(stream, format="PNG", optimize=True)
        img_bytes = stream.getvalue()
        image_view = self.add_blob(img_bytes)
        image_index = len(self.images)
        self.images.append({"bufferView": image_view, "mimeType": "image/png", "name": f"{name} Image"})
        texture_index = len(self.textures)
        self.textures.append({"sampler": 0, "source": image_index, "name": f"{name} Texture"})
        self.tex_cache[name] = texture_index
        return texture_index

    def add_baked_material(self, name, texture_img, metallic=0.22, roughness=0.34,
                           base_scale=0.62, emissive_scale=0.38, double_sided=False):
        if name in self.material_cache:
            return self.material_cache[name]
        tex_idx = self._embed_texture(name, texture_img)
        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [base_scale, base_scale, base_scale, 1.0],
                "baseColorTexture": {"index": tex_idx},
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
            "emissiveFactor": [emissive_scale, emissive_scale, emissive_scale],
            "emissiveTexture": {"index": tex_idx},
            "alphaMode": "OPAQUE",
            "doubleSided": double_sided,
        }
        self.materials.append(material)
        idx = len(self.materials) - 1
        self.material_cache[name] = idx
        return idx

    def add_solid_material(self, name, rgba, metallic, roughness, alpha_mode="OPAQUE", emissive=None, double_sided=False):
        if name in self.material_cache:
            return self.material_cache[name]
        material = {
            "name": name,
            "pbrMetallicRoughness": {
                "baseColorFactor": [rgba[0] / 255.0, rgba[1] / 255.0, rgba[2] / 255.0, rgba[3] / 255.0],
                "metallicFactor": metallic,
                "roughnessFactor": roughness,
            },
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
        idx_bytes = struct.pack(f"<{len(indices)}{'I' if use_u32 else 'H'}", *indices)
        idx_ctype = 5125 if use_u32 else 5123

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
    # Watertight Hard-Surface Primitives (Strictly Convex / Quad-Stripped)
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
                u_val = np.clip((xa + w / 2.0 - r_left) / max(0.01, w - r_left - r_right), 0.0, 1.0)
                vA = np.clip((z_top - zA) / max(0.005, z_top - z_bot), 0.0, 1.0)
                vB = np.clip((z_top - zB) / max(0.005, z_top - z_bot), 0.0, 1.0)
                positions.extend([xa, ya, zA, xb, yb, zB])
                normals.extend([na[0], na[1], na[2], na[0], na[1], na[2]])
                uvs.extend([float(u_val), float(vA), float(u_val), float(vB)])
            for i in range(n_pts):
                v0 = base_v + i * 2
                indices.extend([v0, v0 + 2, v0 + 3, v0, v0 + 3, v0 + 1])

        emit_strip(out_bot, z_bot, out_bot, z_top - b, lambda k: (out_n[k][0], out_n[k][1], 0.0))
        emit_strip(out_bot, z_top - b, out_top, z_top, lambda k: (out_n[k][0] * 0.707, out_n[k][1] * 0.707, 0.707))
        emit_strip(out_top, z_top, in_ring, z_top, lambda k: (0.0, 0.0, 1.0))
        emit_strip(in_ring, z_top, in_ring, z_bot, lambda k: (-in_n[k][0], -in_n[k][1], 0.0))
        emit_strip(in_ring, z_bot, out_bot, z_bot, lambda k: (0.0, 0.0, -1.0))

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_corner_pillar(self, parent_name, mesh_name, corner_x, corner_y, radius, z_bot, z_top, quad_idx, material_index, seg=16, u_flip=False):
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
                u0, u1 = i / seg, (i + 1) / seg
                if u_flip:
                    u0, u1 = 1.0 - u0, 1.0 - u1
            else:
                dx, dy = x1 - x0, y1 - y0
                ln = math.hypot(dx, dy) or 1.0
                n0 = n1 = (dy / ln, -dx / ln)
                u0 = u1 = 0.95 if not u_flip else 0.05

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

    def add_mapped_box(self, parent_name, mesh_name, bounds_xyz, material_index, uv_face="y", uv_bounds=None):
        """
        Strictly convex rectangular prism whose UVs are continuously mapped across uv_bounds
        so segmented beams/skirts join with zero UV seams or concave polygon artifacts.
        """
        x0, x1, y0, y1, z0, z1 = bounds_xyz
        faces = [
            ((0,  1,  0), [(x1, y1, z0), (x0, y1, z0), (x0, y1, z1), (x1, y1, z1)]),
            ((0, -1,  0), [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)]),
            ((-1, 0,  0), [(x0, y1, z0), (x0, y0, z0), (x0, y0, z1), (x0, y1, z1)]),
            (( 1, 0,  0), [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)]),
            ((0,  0,  1), [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]),
            ((0,  0, -1), [(x0, y1, z0), (x1, y1, z0), (x1, y0, z0), (x0, y0, z0)]),
        ]
        if uv_bounds is None:
            uv_bounds = (x0, x1, z0, z1) if uv_face == "y" else (y0, y1, z0, z1)
        a_min, a_max, z_min, z_max = uv_bounds

        def to_uv(px, py, pz):
            coord = px if uv_face == "y" else py
            u = float(np.clip((coord - a_min) / max(1e-5, a_max - a_min), 0.0, 1.0))
            v = float(np.clip((z_max - pz) / max(1e-5, z_max - z_min), 0.0, 1.0))
            return (u, v)

        positions, normals, uvs, indices = [], [], [], []
        idx = 0
        for (nx, ny, nz), quad in faces:
            for vx, vy, vz in quad:
                positions.extend([vx, vy, vz])
                normals.extend([nx, ny, nz])
                uv = to_uv(vx, vy, vz)
                uvs.extend([uv[0], uv[1]])
            indices.extend([idx, idx + 1, idx + 2, idx, idx + 2, idx + 3])
            idx += 4

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def add_extruded_polygon_y(self, parent_name, mesh_name, poly_xz, y0, y1, material_index, uv_bounds=None):
        """Extrudes strictly CONVEX 2D XZ polygon along Y."""
        n_p = len(poly_xz)
        positions, normals, uvs, indices = [], [], [], []
        cx = sum(p[0] for p in poly_xz) / n_p
        cz = sum(p[1] for p in poly_xz) / n_p

        if uv_bounds is None:
            xs = [p[0] for p in poly_xz]
            zs = [p[1] for p in poly_xz]
            x_min, x_max, z_min, z_max = min(xs), max(xs), min(zs), max(zs)
        else:
            x_min, x_max, z_min, z_max = uv_bounds

        def to_uv(x, z):
            u = np.clip((x - x_min) / max(1e-5, x_max - x_min), 0.0, 1.0)
            v = np.clip((z_max - z) / max(1e-5, z_max - z_min), 0.0, 1.0)
            return (float(u), float(v))

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
            uv0, uv1 = to_uv(x0, z0), to_uv(x1, z1)
            uvs.extend([uv0[0], uv0[1], uv1[0], uv1[1], uv1[0], uv1[1], uv0[0], uv0[1]])
            indices.extend([base_v, base_v + 1, base_v + 2, base_v, base_v + 2, base_v + 3])

        for y_c, ny in ((y0, -1.0), (y1, 1.0)):
            c_idx = len(positions) // 3
            positions.extend([cx, y_c, cz])
            normals.extend([0.0, ny, 0.0])
            c_uv = to_uv(cx, cz)
            uvs.extend([c_uv[0], c_uv[1]])
            for x, z in pts:
                positions.extend([x, y_c, z])
                normals.extend([0.0, ny, 0.0])
                p_uv = to_uv(x, z)
                uvs.extend([p_uv[0], p_uv[1]])
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

    def add_sculpted_turbine_arch(self, parent_name, mesh_name, bed_top_z, material_index):
        n_stat = 9
        xs = np.linspace(-0.078, 0.078, n_stat)
        positions, normals, uvs, indices = [], [], [], []
        rings = []

        for ix, x in enumerate(xs):
            t_abs = abs(x) / 0.078
            z_peak = bed_top_z + 0.004 + 0.039 * math.exp(-3.2 * (t_abs ** 1.85))
            z_bot_arch = bed_top_z + 0.004 + 0.025 * max(0.0, 1.0 - (t_abs / 0.85) ** 2)
            if t_abs > 0.85:
                z_bot_arch = bed_top_z + 0.002
            half_y = 0.026 - 0.007 * (1.0 - t_abs)
            ring = [
                (x, -half_y, z_bot_arch),
                (x, -half_y * 0.78, z_peak),
                (x,  half_y * 0.78, z_peak),
                (x,  half_y, z_bot_arch),
            ]
            rings.append(ring)

        for i in range(n_stat - 1):
            r0, r1 = rings[i], rings[i + 1]
            u0, u1 = i / (n_stat - 1), (i + 1) / (n_stat - 1)
            for side_idx in range(4):
                nxt = (side_idx + 1) % 4
                p00 = np.array(r0[side_idx])
                p01 = np.array(r0[nxt])
                p11 = np.array(r1[nxt])
                p10 = np.array(r1[side_idx])
                n = np.cross(p10 - p00, p01 - p00)
                ln = np.linalg.norm(n) or 1.0
                n = n / ln
                bv = len(positions) // 3
                for p in (p00, p10, p11, p01):
                    positions.extend(p.tolist())
                    normals.extend(n.tolist())
                v_a = 0.15 + 0.7 * (side_idx / 3.0)
                v_b = 0.15 + 0.7 * (nxt / 3.0)
                uvs.extend([u0, v_a, u1, v_a, u1, v_b, u0, v_b])
                indices.extend([bv, bv + 1, bv + 2, bv, bv + 2, bv + 3])

        for r_end, nx in [(rings[0], -1.0), (rings[-1], 1.0)]:
            bv = len(positions) // 3
            for p in r_end:
                positions.extend(p)
                normals.extend([nx, 0.0, 0.0])
            uvs.extend([0.1, 0.5, 0.2, 0.1, 0.8, 0.1, 0.9, 0.5])
            indices.extend([bv, bv + 1, bv + 2, bv, bv + 2, bv + 3])

        return self.add_mesh_node(parent_name, mesh_name, positions, normals, uvs, indices, material_index)

    def build_scene(self):
        tex = build_baked_surface_textures()

        # Reference-Derived Baked PBR Materials
        mat_forehead = self.add_baked_material("Ref Baked Forehead", tex["forehead"], metallic=0.20, roughness=0.32, base_scale=0.60, emissive_scale=0.40)
        mat_pillar_r = self.add_baked_material("Ref Baked Right Post", tex["pillar_r"], metallic=0.22, roughness=0.28, base_scale=0.56, emissive_scale=0.44)
        mat_pillar_l = self.add_baked_material("Ref Baked Left Post", tex["pillar_l"], metallic=0.20, roughness=0.28, base_scale=0.56, emissive_scale=0.40)
        mat_chin = self.add_baked_material("Ref Baked Chin", tex["chin"], metallic=0.20, roughness=0.34, base_scale=0.58, emissive_scale=0.42)
        mat_side_top = self.add_baked_material("Ref Baked Side Top", tex["side_top"], metallic=0.24, roughness=0.34, base_scale=0.56, emissive_scale=0.44)
        mat_side_bot = self.add_baked_material("Ref Baked Side Bot", tex["side_bot"], metallic=0.24, roughness=0.36, base_scale=0.54, emissive_scale=0.42)
        mat_left_bot = self.add_baked_material("Ref Baked Left Bot", tex["left_bot"], metallic=0.20, roughness=0.34, base_scale=0.56, emissive_scale=0.42)
        mat_rear_post = self.add_baked_material("Ref Baked Rear Post", tex["side_rear_post"], metallic=0.24, roughness=0.34, base_scale=0.55, emissive_scale=0.45)
        mat_rear_wall = self.add_baked_material("Ref Baked Rear Wall", tex["rear"], metallic=0.25, roughness=0.38, base_scale=0.60, emissive_scale=0.35)

        mat_hinge = self.add_baked_material("Ref Baked Hinge", tex["hinge"], metallic=0.32, roughness=0.28, base_scale=0.58, emissive_scale=0.40)
        mat_handle = self.add_baked_material("Ref Baked Handle", tex["handle"], metallic=0.38, roughness=0.26, base_scale=0.52, emissive_scale=0.48)
        mat_console_screen = self.add_baked_material("Ref Baked Console", tex["console"], metallic=0.22, roughness=0.14, base_scale=0.38, emissive_scale=0.55)

        mat_graphite = self.add_solid_material("Graphite Door Frame", (20, 22, 26, 255), 0.50, 0.24)
        mat_smoked_glass = self.add_solid_material("Smoked Glass", (18, 22, 26, 135), 0.35, 0.08, alpha_mode="BLEND", double_sided=True)
        # Sleeker dark champagne-bronze console chamfer housing (replacing thick pale rectangle)
        mat_console_rim = self.add_solid_material("Console Metallic Trim", (72, 62, 52, 255), 0.45, 0.28, emissive=[0.05, 0.04, 0.03])
        mat_rubber_foot = self.add_solid_material("Matte Rubber Foot", (26, 24, 22, 255), 0.06, 0.85)
        mat_chassis_shadow = self.add_solid_material("Underbody Shadow Plinth", (34, 28, 24, 255), 0.28, 0.62, emissive=[0.04, 0.03, 0.025])

        # Warm glowing amber interior calibrated to shine warmly through 52% Smoked Glass
        mat_chamber = self.add_baked_material("Ref Baked Chamber Glow", tex["chamber"], metallic=0.08, roughness=0.46, base_scale=0.55, emissive_scale=1.0)
        mat_chamber_bronze = self.add_baked_material("Ref Baked Chamber Bronze", tex["chamber_bronze"], metallic=0.22, roughness=0.42, base_scale=0.55, emissive_scale=0.88)
        mat_interior_dark = self.add_solid_material("Chassis Matte Dark", (84, 66, 52, 255), 0.32, 0.44, emissive=[0.22, 0.16, 0.11])
        mat_led_glow = self.add_solid_material("Interior LED Glow", (255, 232, 198, 255), 0.05, 0.20, emissive=[1.0, 0.82, 0.60])

        mat_toolhead = self.add_baked_material("Toolhead Baked Metal", tex["toolhead"], metallic=0.28, roughness=0.26, base_scale=0.62, emissive_scale=0.88)
        mat_bracket = self.add_baked_material("Bracket Baked Alloy", tex["bracket"], metallic=0.36, roughness=0.26, base_scale=0.66, emissive_scale=0.86)
        mat_pei = self.add_baked_material("Gold Textured PEI", tex["pei"], metallic=0.55, roughness=0.30, base_scale=0.72, emissive_scale=0.68)

        mat_carbon = self.add_solid_material("PA-CF Carbon Fiber", (102, 86, 72, 255), 0.30, 0.36, emissive=[0.22, 0.16, 0.11])
        mat_steel = self.add_solid_material("Linear Guide Steel", (250, 240, 226, 255), 0.88, 0.15, emissive=[0.52, 0.44, 0.34])
        mat_brass = self.add_solid_material("Brass Nozzle", (236, 184, 58, 255), 0.90, 0.20, emissive=[0.28, 0.18, 0.05])
        mat_ptfe = self.add_solid_material("PTFE Bowden Tube", (252, 246, 236, 255), 0.05, 0.26, emissive=[0.54, 0.44, 0.34])

        for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]:
            self.add_parent(p)

        # Calibrated P2S 3/4 Dimensions
        W, D = 0.418, 0.292
        R_left = 0.014
        R_right = 0.028
        Z_leg_bot = -0.200
        Z_side_arch = -0.190  # Clean subtle 10mm arch backed by solid recessed plinth
        Z_chin_top = -0.142
        Z_door_top = 0.142
        Z_roof_top = 0.190
        Z_crown_split = Z_roof_top - 0.0025

        # -------------------------------------------------------------
        # 1. WATERTIGHT UNIBODY ENCLOSURE (`enclosure`)
        # -------------------------------------------------------------
        # Solid full-depth dark recessed chassis underbody plinth (prevents any background bleed under arches!)
        self.add_box("enclosure", "chassis_recessed_plinth", (0.0, 0.0, 0.5 * ((Z_leg_bot + 0.002) + Z_chin_top)),
                     (W - 0.016, D - 0.016, Z_chin_top - (Z_leg_bot + 0.002)), mat_chassis_shadow)
        self.add_box("enclosure", "interior_floor_tray", (0.0, 0.0, Z_chin_top - 0.004),
                     (W - 0.048, D - 0.048, 0.010), mat_chamber_bronze)

        # 4 Continuous Corner Pillars (from foot bottom Z_leg_bot uninterrupted to top bevel Z_crown_split!)
        self.add_corner_pillar("enclosure", "unibody_corner_0",  W / 2.0 - R_right,  D / 2.0 - R_right, R_right, Z_leg_bot, Z_crown_split, 0, mat_rear_post)
        self.add_corner_pillar("enclosure", "unibody_corner_1", -W / 2.0 + R_left,   D / 2.0 - R_left,  R_left,  Z_leg_bot, Z_crown_split, 1, mat_rear_post)
        self.add_corner_pillar("enclosure", "unibody_corner_2", -W / 2.0 + R_left,  -D / 2.0 + R_left,  R_left,  Z_leg_bot, Z_crown_split, 2, mat_pillar_l, u_flip=False)
        self.add_corner_pillar("enclosure", "unibody_corner_3",  W / 2.0 - R_right, -D / 2.0 + R_right, R_right, Z_leg_bot, Z_crown_split, 3, mat_pillar_r, u_flip=False)

        # 4 Embedded Corner Rubber Feet centered strictly beneath leg footprints (zero side overhang!)
        foot_coords = [
            (-W / 2.0 + 0.017, -D / 2.0 + 0.017, 0.020),
            ( W / 2.0 - 0.032, -D / 2.0 + 0.032, 0.028),
            ( W / 2.0 - 0.032,  D / 2.0 - 0.032, 0.028),
            (-W / 2.0 + 0.017,  D / 2.0 - 0.017, 0.020),
        ]
        for i, (fx, fy, fw) in enumerate(foot_coords):
            self.add_box("enclosure", f"chassis_foot_{i}", (fx, fy, Z_leg_bot - 0.002), (fw, fw, 0.004), mat_rubber_foot)

        # Top Crown Bevel Ring (`Z_crown_split .. Z_roof_top`) + Inner Roof Deck (`Z_roof_top - 0.008 .. Z_roof_top`)
        self.add_extruded_asym_frame("enclosure", "unibody_top_frame", W, D, 0.344, 0.220,
                                     Z_crown_split, Z_roof_top, R_left, R_right, 0.012, 0.0025, mat_side_top)
        self.add_extruded_asym_frame("enclosure", "top_rim_outer", 0.348, 0.224, 0.334, 0.210,
                                     Z_roof_top - 0.009, Z_roof_top - 0.001, 0.012, 0.012, 0.010, 0.001, mat_graphite)
        self.add_box("enclosure", "top_roof_glass", (0.0, 0.0, Z_roof_top - 0.006), (0.338, 0.214, 0.004), mat_smoked_glass)

        x_f_min = -W / 2.0 + R_left
        x_f_max =  W / 2.0 - R_right
        f_mid_w = x_f_max - x_f_min
        f_mid_x = 0.5 * (x_f_min + x_f_max)

        # Front Top Forehead Panel (strictly flush between pillar_l and pillar_r up to Z_crown_split)
        self.add_mapped_box("enclosure", "unibody_front_header",
                            (x_f_min, x_f_max, -D / 2.0, -D / 2.0 + 0.024, Z_door_top - 0.008, Z_crown_split),
                            mat_forehead, uv_face="y")

        # Seamless Front Chin Skirt (one continuous slab + small flush leg pads at Z_leg_bot)
        y_f0, y_f1 = -D / 2.0, -D / 2.0 + 0.024
        front_uv = (x_f_min, x_f_max, Z_leg_bot, Z_chin_top)
        self.add_mapped_box("enclosure", "unibody_front_chin_main",
                            (x_f_min, x_f_max, y_f0, y_f1, Z_leg_bot + 0.002, Z_chin_top),
                            mat_chin, uv_face="y", uv_bounds=front_uv)
        self.add_mapped_box("enclosure", "unibody_front_chin_leg_l",
                            (x_f_min, x_f_min + 0.044, y_f0, y_f1, Z_leg_bot, Z_leg_bot + 0.002),
                            mat_chin, uv_face="y", uv_bounds=front_uv)
        self.add_mapped_box("enclosure", "unibody_front_chin_leg_r",
                            (x_f_max - 0.044, x_f_max, y_f0, y_f1, Z_leg_bot, Z_leg_bot + 0.002),
                            mat_chin, uv_face="y", uv_bounds=front_uv)

        # Right & Left Side Wall Frames + Watertight Continuous Skirts + Sealed Smoked Windows
        y_l_min, y_l_max = -D / 2.0 + R_left,  D / 2.0 - R_left
        y_r_min, y_r_max = -D / 2.0 + R_right, D / 2.0 - R_right

        for side_name, sx_sign, y_min, y_max, mat_s_bot in [
            ("left",  -1.0, y_l_min, y_l_max, mat_left_bot),
            ("right",  1.0, y_r_min, y_r_max, mat_side_bot),
        ]:
            s_span = y_max - y_min
            s_yc = 0.5 * (y_min + y_max)
            x0_s = sx_sign * (W / 2.0 - 0.024) if sx_sign > 0 else -W / 2.0
            x1_s = sx_sign * (W / 2.0)         if sx_sign > 0 else -W / 2.0 + 0.024
            sx0, sx1 = min(x0_s, x1_s), max(x0_s, x1_s)

            # Side Upper Beam extends cleanly up to Z_crown_split connecting directly into unibody_top_frame!
            self.add_mapped_box("enclosure", f"unibody_{side_name}_top_beam",
                                (sx0, sx1, y_min, y_max, Z_door_top - 0.012, Z_crown_split),
                                mat_side_top, uv_face="x", uv_bounds=(y_min, y_max, Z_door_top - 0.012, Z_crown_split))

            # Seamless Side Skirt Band (continuous full-span beam Z_side_arch..Z_chin_top + lower leg tabs Z_leg_bot..Z_side_arch)
            side_uv = (y_min, y_max, Z_leg_bot, Z_chin_top)
            self.add_mapped_box("enclosure", f"unibody_{side_name}_skirt_band",
                                (sx0, sx1, y_min, y_max, Z_side_arch, Z_chin_top),
                                mat_s_bot, uv_face="x", uv_bounds=side_uv)
            self.add_mapped_box("enclosure", f"unibody_{side_name}_skirt_front_leg",
                                (sx0, sx1, y_min, y_min + 0.042, Z_leg_bot, Z_side_arch),
                                mat_s_bot, uv_face="x", uv_bounds=side_uv)
            self.add_mapped_box("enclosure", f"unibody_{side_name}_skirt_rear_leg",
                                (sx0, sx1, y_max - 0.032, y_max, Z_leg_bot, Z_side_arch),
                                mat_s_bot, uv_face="x", uv_bounds=side_uv)

            # Dark Flush Side Window Gasket + Smoked Window
            gx = sx_sign * (W / 2.0 - 0.012)
            win_z_ctr = 0.5 * ((Z_door_top - 0.012) + Z_chin_top)
            win_h = (Z_door_top - 0.012) - Z_chin_top
            self.add_box("enclosure", f"{side_name}_gasket_top", (gx, s_yc, Z_door_top - 0.016), (0.022, s_span + 0.004, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_bot", (gx, s_yc, Z_chin_top + 0.004),  (0.023, s_span + 0.004, 0.012), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_f",   (gx, y_min + 0.003, win_z_ctr),  (0.022, 0.014, win_h), mat_graphite)
            self.add_box("enclosure", f"{side_name}_gasket_r",   (gx, y_max - 0.003, win_z_ctr),  (0.023, 0.016, win_h), mat_graphite)
            self.add_box("enclosure", f"{side_name}_glass_window", (gx, s_yc, win_z_ctr), (0.005, s_span - 0.008, win_h - 0.008), mat_smoked_glass)

        # Rear Wall (flush up to Z_crown_split)
        rear_h = Z_door_top - Z_chin_top
        rear_zc = 0.5 * (Z_door_top + Z_chin_top)
        self.add_mapped_box("enclosure", "unibody_rear_wall",
                            (-W / 2.0 + R_left, W / 2.0 - R_right, D / 2.0 - 0.024, D / 2.0, Z_leg_bot, Z_crown_split),
                            mat_rear_wall, uv_face="y")

        # Warm Backlit Studio Amber Interior Chamber Liners (ceiling + rear + left + right-rear electronics hump)
        self.add_box("enclosure", "interior_rear_panel", (0.0, D / 2.0 - 0.028, rear_zc), (W - 0.056, 0.006, rear_h + 0.006), mat_chamber)
        self.add_box("enclosure", "interior_ceiling_liner", (0.0, 0.010, Z_door_top - 0.006), (W - 0.068, D - 0.068, 0.005), mat_chamber)
        self.add_box("enclosure", "interior_left_back_baffle", (-W / 2.0 + 0.032, 0.010, rear_zc), (0.006, 0.210, rear_h - 0.012), mat_chamber)
        self.add_box("enclosure", "interior_rear_electronics_box", (0.068, D / 2.0 - 0.042, -0.022), (0.142, 0.024, 0.160), mat_chamber_bronze)

        self.add_box("enclosure", "led_bar_front", (0.0, -0.105, Z_door_top - 0.010), (0.290, 0.014, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_left",  (-0.155, 0.0, Z_door_top - 0.010), (0.014, 0.180, 0.005), mat_led_glow)
        self.add_box("enclosure", "led_bar_right", ( 0.155, 0.0, Z_door_top - 0.010), (0.014, 0.180, 0.005), mat_led_glow)

        # Sleek Dark-Bronze Angled Touchscreen Console seated flush against door rail notch
        console_angle = math.radians(-24.0)
        n_y = -math.cos(console_angle)
        n_z = -math.sin(console_angle)
        bz_y = -D / 2.0 - 0.006
        bz_z = Z_chin_top - 0.013
        cx_con = f_mid_x - 0.008
        self.add_box("enclosure", "screen_dock_wedge", (cx_con, -D / 2.0 + 0.004, bz_z - 0.001), (0.112, 0.018, 0.022), mat_graphite)
        self.add_box("enclosure", "screen_metal_rim",  (cx_con, bz_y, bz_z), (0.118, 0.007, 0.036), mat_console_rim, rot_x=console_angle)
        self.add_box("enclosure", "screen_bezel",      (cx_con, bz_y + n_y * 0.002, bz_z + n_z * 0.002),
                     (0.113, 0.005, 0.031), mat_graphite, rot_x=console_angle)
        self.add_box("enclosure", "screen_display",    (cx_con, bz_y + n_y * 0.005, bz_z + n_z * 0.005),
                     (0.107, 0.002, 0.026), mat_console_screen, rot_x=console_angle)

        # -------------------------------------------------------------
        # 2. FRONT DOOR ASSEMBLY (`door` + `front_glass_door`)
        # -------------------------------------------------------------
        door_y = -D / 2.0 + 0.006
        door_h = (Z_door_top - 0.008) - Z_chin_top
        door_zc = 0.5 * ((Z_door_top - 0.008) + Z_chin_top)
        door_w = f_mid_w - 0.002
        door_xc = f_mid_x

        self.add_box("enclosure", "front_jamb_seal_l", (x_f_min + 0.006, door_y + 0.008, door_zc), (0.012, 0.008, door_h + 0.004), mat_graphite)
        self.add_box("enclosure", "front_jamb_seal_r", (x_f_max - 0.006, door_y + 0.008, door_zc), (0.012, 0.008, door_h + 0.004), mat_graphite)

        for h_name, hz in [("door_hinge_top", door_zc + door_h / 2.0 - 0.022), ("door_hinge_bot", door_zc - door_h / 2.0 + 0.022)]:
            self.add_box("enclosure", h_name, (x_f_min + 0.006, door_y - 0.0025, hz), (0.013, 0.009, 0.022), mat_hinge)

        stile_w = 0.014
        rail_h = 0.014
        self.add_box("door", "door_left_stile",  (door_xc - door_w / 2.0 + stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), mat_graphite)
        self.add_box("door", "door_right_stile", (door_xc + door_w / 2.0 - stile_w / 2.0, door_y, door_zc), (stile_w, 0.007, door_h), mat_graphite)
        self.add_box("door", "door_top_rail",    (door_xc, door_y, door_zc + door_h / 2.0 - rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), mat_graphite)

        b_rail_bot = door_zc - door_h / 2.0
        self.add_box("door", "door_bottom_rail", (door_xc, door_y, b_rail_bot + rail_h / 2.0), (door_w - 2 * stile_w, 0.007, rail_h), mat_graphite)
        hood_poly = [
            (cx_con - 0.064, b_rail_bot),
            (cx_con + 0.064, b_rail_bot),
            (cx_con + 0.052, b_rail_bot + rail_h + 0.005),
            (cx_con - 0.052, b_rail_bot + rail_h + 0.005),
        ]
        self.add_extruded_polygon_y("door", "door_console_arch_hood", hood_poly, door_y - 0.004, door_y + 0.004, mat_graphite)

        self.add_box("door", "front_glass_door", (door_xc, door_y, door_zc), (door_w - 2 * stile_w, 0.004, door_h - 2 * rail_h), mat_smoked_glass)

        # Reference-Baked Beveled Vertical Door Handle
        hx = door_xc + door_w / 2.0 - 0.004
        hz = door_zc - 0.004
        self.add_box("door", "door_ergo_handle",      (hx, door_y - 0.011, hz), (0.014, 0.011, 0.056), mat_handle)
        self.add_box("door", "door_handle_mount_top", (hx, door_y - 0.006, hz + 0.016), (0.010, 0.008, 0.008), mat_handle)
        self.add_box("door", "door_handle_mount_bot", (hx, door_y - 0.006, hz - 0.016), (0.010, 0.008, 0.008), mat_handle)

        # -------------------------------------------------------------
        # 3. COREXY GANTRY (`gantryX`)
        # -------------------------------------------------------------
        gantry_z = 0.072
        self.add_cylinder("gantryX", "x_guide_front", (0.0, -0.024, gantry_z + 0.012), 0.0058, 0.328, "x", mat_steel)
        self.add_cylinder("gantryX", "x_guide_rear",  (0.0, -0.024, gantry_z - 0.012), 0.0058, 0.328, "x", mat_steel)
        self.add_cylinder("gantryX", "x_guide_top",   (0.0,  0.016, gantry_z + 0.022), 0.0052, 0.328, "x", mat_steel)
        self.add_box("gantryX", "x_slider_left",  (-0.160, -0.010, gantry_z), (0.022, 0.068, 0.036), mat_carbon)
        self.add_box("gantryX", "x_slider_right", ( 0.160, -0.010, gantry_z), (0.022, 0.068, 0.036), mat_carbon)

        self.add_cylinder("gantryX", "y_guide_left",  (-0.162, 0.0, gantry_z + 0.016), 0.0055, 0.210, "y", mat_steel)
        self.add_cylinder("gantryX", "y_guide_right", ( 0.162, 0.0, gantry_z + 0.016), 0.0055, 0.210, "y", mat_steel)

        self.add_cylinder("gantryX", "z_lead_left",  (-0.148, -0.036, -0.014), 0.0050, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_guide_left", (-0.148,  0.035, -0.014), 0.0055, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_right", ( 0.148,  0.000, -0.014), 0.0050, 0.275, "z", mat_steel)
        self.add_cylinder("gantryX", "z_lead_rear",  ( 0.000,  0.095, -0.014), 0.0055, 0.275, "z", mat_steel)

        for seg_i in range(9):
            cx_d = 0.026 + seg_i * 0.013
            self.add_box("gantryX", f"drag_chain_{seg_i}", (cx_d, 0.038, gantry_z + 0.026), (0.010, 0.016, 0.011), mat_interior_dark)

        # -------------------------------------------------------------
        # 4. REFERENCE-BAKED SCULPTED TOOLHEAD (`printHead`)
        # -------------------------------------------------------------
        th_z = gantry_z - 0.004
        self.add_box("printHead", "toolhead_chassis",    (0.0, -0.002, th_z), (0.056, 0.042, 0.058), mat_carbon)
        self.add_box("printHead", "toolhead_front_cowl", (0.0, -0.026, th_z + 0.002), (0.052, 0.008, 0.052), mat_toolhead)
        self.add_box("printHead", "toolhead_hotend_sock",(0.0, -0.002, th_z - 0.034), (0.020, 0.020, 0.014), mat_graphite)
        self.add_cylinder("printHead", "toolhead_nozzle",(0.0, -0.002, th_z - 0.044), 0.0035, 0.010, "z", mat_brass)

        ptfe_pts = []
        for i in range(12):
            t = i / 11.0
            px = 0.010 * math.sin(t * math.pi)
            py = -0.002 + t * 0.115
            pz = (th_z + 0.028) + 0.042 * math.sin(t * math.pi * 0.72) + t * 0.010
            ptfe_pts.append((px, py, pz))
        self.add_curved_tube("printHead", "ptfe_bowden_tube", ptfe_pts, 0.0040, mat_ptfe)

        # -------------------------------------------------------------
        # 5. PRINT BED & PEI PLATE (`printBed`)
        # -------------------------------------------------------------
        bed_z = -0.078
        self.add_box("printBed", "build_plate",        (0.0,  0.002, bed_z),         (0.268, 0.188, 0.004), mat_pei)
        self.add_box("printBed", "build_plate_lip",    (0.0, -0.092, bed_z),         (0.086, 0.012, 0.004), mat_toolhead)
        self.add_box("printBed", "bed_heater_block",   (0.0,  0.002, bed_z - 0.006), (0.264, 0.184, 0.008), mat_interior_dark)
        self.add_box("printBed", "bed_carriage_arm_l", (-0.102, 0.002, bed_z - 0.014), (0.028, 0.175, 0.012), mat_graphite)
        self.add_box("printBed", "bed_carriage_arm_r", ( 0.102, 0.002, bed_z - 0.014), (0.028, 0.175, 0.012), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_l",    (-0.148, 0.000, bed_z - 0.014), (0.026, 0.095, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_r",    ( 0.148, 0.000, bed_z - 0.014), (0.026, 0.032, 0.014), mat_graphite)
        self.add_box("printBed", "bed_z_bracket_rear", (0.0,    0.095, bed_z - 0.014), (0.050, 0.026, 0.014), mat_graphite)

        # -------------------------------------------------------------
        # 6. LOFTED SMOOTH TURBINE ARCH BRACKET + 19 SUPPORT FINS (`printedObject`)
        # -------------------------------------------------------------
        obj_z = bed_z + 0.002
        self.add_box("printedObject", "bracket_base_raft", (0.0, 0.002, obj_z + 0.002), (0.166, 0.058, 0.004), mat_bracket)
        self.add_sculpted_turbine_arch("printedObject", "bracket_swept_arch", obj_z, mat_bracket)
        self.add_cylinder("printedObject", "bracket_apex_ring", (0.0, 0.002, obj_z + 0.038), 0.012, 0.044, "y", mat_carbon)
        for f_i in range(19):
            fx = -0.063 + f_i * 0.007
            t_f = abs(fx) / 0.072
            fh = 0.028 * max(0.25, 1.0 - t_f * 0.78)
            self.add_box("printedObject", f"support_fin_{f_i}", (fx, 0.002, obj_z + 0.004 + fh / 2.0), (0.0018, 0.034, fh), mat_bracket)

        # -------------------------------------------------------------
        # 7. Write GLB
        # -------------------------------------------------------------
        self.align()
        bin_chunk = bytes(self.bin)
        root_indices = [self.parents[p] for p in ["enclosure", "door", "printHead", "printBed", "gantryX", "printedObject"]]

        gltf = {
            "asset": {"version": "2.0", "generator": "Antigravity Reference-Projected Multi-View Pipeline (TASK-033 v4_rev1)"},
            "scene": 0,
            "scenes": [{"name": "P2S_Asset_Pivot_V4_Rev1_Scene", "nodes": root_indices}],
            "nodes": self.nodes,
            "meshes": self.meshes,
            "materials": self.materials,
            "textures": self.textures,
            "images": self.images,
            "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}],
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

        print(f"Generated Pivot V4 Rev1 GLB: {OUT_GLB}")
        print(f"  Total Size: {total_length} bytes")
        print(f"  Nodes: {len(self.nodes)}, Meshes: {len(self.meshes)}, Materials: {len(self.materials)}, Images: {len(self.images)}")


if __name__ == "__main__":
    builder = PivotV4Rev1GlbBuilder()
    builder.build_scene()
