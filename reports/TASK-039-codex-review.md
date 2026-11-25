# Codex audit — TASK-039 reference-fidelity criteria pass

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v7.glb`
- **Evidence read:** task file, Antigravity report, outbox response, GLB payload, fixed-fixture front/left20/right20/elevated screenshots, silhouette overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration decision:** do not replace the current website asset with v7.

## What passed

- The handoff is complete and the artifact is a valid glTF 2.0 payload with 62 nodes / 56 meshes in the report, required logical nodes present, and no reported image plane/billboard/2.5D rig.
- The fixed fixture was used.
- Framing is materially improved: candidate bbox `422×409`, `W/H=1.032` versus target `425×408`, `1.042`, within the framing tolerance.
- The four views show a connected object without the previous detached feet, white wedge, or black diagonal bake artifact.

## Why it is not accepted

The reference is a closed, smoked-glass, photoreal printer. The v7 front screenshot still reads as a light open-frame enclosure:

1. **Front closure failure:** the door/glass does not visually read as a dark closed pane; the chamber is too exposed and bright. This is the largest semantic mismatch.
2. **Top shell failure:** the top cap is too flat and rectangular; the reference has a more controlled low-angle taper/rounded transition into the right side.
3. **Value/material failure:** the shell/pillar/right flank contrast is inverted in key regions. The report records 9/15 photometric ROIs over the strict 15 RGB/channel limit, including forehead left, pillar/cheek, lower left, right flank, right glass, chamber mid, toolhead, and printed object.
4. **Silhouette is only marginal:** centered IoU is `0.8984` (< `0.90`); the `0.9156` result depends on a `(-3,+3)` alignment. The overlay still shows top-corner and lower-arch disagreement.
5. **Reference landmarks are not enough by presence:** rails, bed, printhead and console exist, but their visual density and contrast do not match the reference because the front glass/value hierarchy is wrong.

## Required next direction

This is not a website/build problem and should not be “fixed” with camera compensation or an image plane. The next task must prioritize a visually closed smoked door and reference-like material/light hierarchy, then re-measure silhouette and landmarks. If the current v7 construction cannot produce that without facade overlays, pivot the mesh/material construction method.

`PASS` remains reserved for Codex after a new artifact and evidence pass all hard gates in `reports/reference-fidelity-criteria.md`.
