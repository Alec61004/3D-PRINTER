# Deltrol P2S — Reference Fidelity Criteria

Status: `ACTIVE / NOT YET PASSED`

This is the measurement sheet for the Codex review loop. It is intentionally stricter than an Antigravity completion report. A build, a valid GLB, or a working orbit control never counts as visual acceptance by itself.

## Reference and test fixture

| Item | Fixed value |
|---|---|
| Full reference | `assets/source/printer-hero-reference-2026-11-23.png` |
| Object-only reference | `reports/ref_printer_box.png` |
| Audit viewport | `1226x708` |
| Camera | Perspective, FOV `27°`, position `[0.86, 0.22, 1.50]`, target `[0, -0.01, 0]` |
| Lighting | Audit viewer rig, white background, ACES, exposure `1.05`, pixel ratio `1` |
| Required views | `front`, `left20`, `right20`, `elevated (+18°)` |
| Reference crop bbox | `W=425px`, `H=408px`, `W/H=1.042` |

The reference bbox is the object crop measured with the same foreground segmentation used by the existing audit reports. The old `457x424` values came from a different full-hero/non-white measurement and must not be mixed into this gate.

## Acceptance matrix

| Gate | Required evidence | Pass threshold | Current v6 status |
|---|---|---|---|
| Framing | Front screenshot + bbox report | Width/height ±3%, ratio ±0.03, edge alignment ±3px | FAIL: `W=465`, `H=406`, ratio `1.145` |
| Silhouette | Reference/render overlay or IoU report | IoU ≥ `0.90`; no top/right/bottom contour mismatch | FAIL: top and side contours differ visibly |
| Camera | Viewer URL/config + screenshot | Exact fixed camera; no per-candidate compensation | PASS for audit fixture |
| Enclosure | Front + ±20° + elevated | Closed, continuous shell; no floating/detached parts | PASS for v6 artifact check; visual form still differs |
| Door/glass | Front close comparison | Smoked framed glass fills opening; right handle and left hinges present | FAIL: framing/material/detail are not reference-close |
| Top/right shell | Front close comparison | Rounded front-right pillar and sloped top-to-side transition | FAIL: generic/open rectangular reading remains |
| Console/base | Front close comparison | Low centered dark console with metallic rim; integrated base/feet | FAIL if detached, oversized, or misplaced |
| Interior landmarks | Front close comparison | Rails, upper print head, bed, warm printed object in matching relative positions | FAIL until placements and density match reference |
| Materials/value | Region samples | Champagne satin shell; darker smoked glass/right side; warm chamber; white ground | FAIL if pale/flat/uniform or hue-inverted |
| Photometric regions | RGB/Delta-E report | No key region >15 RGB/channel mean error; no strong inversion | PENDING measurement per candidate |
| Artifact/mesh | GLB verify + 4 screenshots | Real connected mesh; no billboard/image plane/wedge/black bake/z-fight | PASS for v6 structural check |
| Interaction | Browser audit | Reference hero stays exact; 3D loads lazily and rotates without breaking | PASS as contract; not a fidelity pass |

## Landmark checklist

The reviewer must explicitly mark each item `PASS`/`FAIL`, not infer it from the overall impression:

1. The printer occupies the same compact right-facing 3/4 pose and low eye level.
2. The top shell is a single continuous cap with the same left-to-right taper.
3. The front-right pillar is the dominant rounded vertical highlight; the left edge is slimmer/sharper.
4. The front door is closed, dark, framed, and flush with the shell.
5. The right handle is attached to the door at the reference height; left hinges remain subtle.
6. The chamber is warm amber and readable through the smoked glass.
7. The upper rails and print head sit near the same vertical band and horizontal span.
8. The bed and printed object occupy the same lower-middle region.
9. The lower console is compact, centered, dark-screened, and angled like the reference.
10. The bottom feet/base are integrated and touch the same soft shadow; nothing floats.
11. The right side panel is dark and deep, with a controlled metallic reflection—not a flat beige wall.
12. No white wedge, black triangular bake, detached panel, detached foot, open seam, or accidental image plane exists in any view.

## Required audit output for every future handoff

- Candidate GLB path and SHA-256.
- Four fresh screenshots at the fixed fixture.
- Measured bbox `(xmin, ymin, xmax, ymax, W, H, W/H)` for front.
- Silhouette IoU/overlay evidence.
- Landmark matrix above with 12 explicit verdicts.
- Material/photometric region samples and method.
- GLB node/mesh/image-plane validation.
- Codex verdict: `PASS`, `REVISION_REQUIRED`, or `PIVOT_REQUIRED`.

Current decision: the exact reference image may remain the fidelity hero, while the true-3D explorer remains `REVISION_REQUIRED` until the front gate and landmark matrix pass.
