# TASK-006 — GLB Build and Optimization Report

## Result

Status: `COMPLETED`

Built two self-contained glTF 2.0 binary assets from the approved multiview
preparation set. The raw/source output is preserved separately from the browser
optimized output. No Antigravity asset was modified and no website code was created.

## Build provenance

- Task: `TASK-006`
- Input metadata: `assets/generated/antigravity/multiview/p2s_multiview_metadata.json`
- Input reference set: `assets/generated/antigravity/multiview/`
- Reproducible local builder: `reports/task-006-build-glb.py`
- Coordinate convention: front `-Y`, right `+X`, up `+Z`
- Units: meters
- Nominal envelope: 0.40 m wide × 0.40 m deep × 0.50 m high

## Outputs

| Variant | Path | Bytes | SHA-256 | Meshes | Nodes | Materials | Embedded textures |
|---|---|---:|---|---:|---:|---:|---:|
| Source/raw | `assets/models/raw/deltrol_p2s_source.glb` | 67232 | `d244e8928db076d938137f29cdf57ae9e9f28f59877cb342843371fcdce44f0b` | 36 | 43 | 8 | 8 |
| Browser optimized | `assets/models/optimized/deltrol_p2s_optimized.glb` | 62672 | `284dedc8d5d97bad6f3221b8e55aa30ceafbbbcffcd984b7f1393b087c5c64a3` | 36 | 43 | 8 | 8 |

The optimized file is approximately 6.8% smaller than the raw file by using fewer
cylinder segments while preserving the same dimensions and logical scene structure.
All textures are embedded PNGs; there are no external URI dependencies.

## Logical parts

The scene contains named root nodes for:

`enclosure`, `door`, `printHead`, `printBed`, `gantryX`, `gantryY`, `printedObject`.

The model includes the enclosure, smoked front door, handle, screen, bed/carriage,
CoreXY guide rods and belts, toolhead/nozzle, power details, and a simple printed
calibration object.

## Validation

- GLB magic/version: valid glTF 2.0 for both files.
- Declared total length equals actual file length for both files.
- JSON and BIN chunks are present and structurally readable.
- All buffer views and accessors remain within the embedded BIN chunk.
- All images use embedded `bufferView` data; no external image URI exists.
- Overall bounds for both variants: min `[-0.204, -0.225, -0.235]`, max `[0.204, 0.204, 0.235]` meters.
- Overall bounds are centered around the origin and preserve the intended front/right/up convention.
- Materials include metallic enclosure/steel, dark polymer, smoked glass, PEI bed, screen, rubber, and printed-object finishes.

## Limitations

This is a browser-safe technical proxy assembled from AI visual references, not a
manufacturing CAD reconstruction. Internal screw threads, wire gauges, exact belt
routing, motor housings, and hidden enclosure geometry remain inferred. The smoked
glass uses an approximation suitable for viewer presentation. These limitations must
remain visible in later viewer and final QA reviews.
