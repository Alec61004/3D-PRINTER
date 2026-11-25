# Codex audit — TASK-040 closed-door reference pivot

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v8.glb`
- **Evidence:** task/report/outbox, GLB hash and payload, front/left20/right20/elevated renders, four-view sheet and silhouette overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v8 is not promoted to the website explorer.

## Improvements confirmed

- The front pane now reads darker and more closed than v7.
- The candidate remains a real connected GLB with required nodes and no reported billboard/image-plane/2.5D rig.
- Framing remains close: `422×407`, `W/H=1.037` against target `425×408`, `1.042`.
- No detached feet, white wedge or black diagonal bake artifact is visible in the submitted views.

## Blocking differences

1. **Silhouette is still not accepted:** centered IoU is `0.8986`, below the unshifted `0.90` gate. The top contour and lower arch still disagree with the reference; the near-pass cannot be rescued by shifted alignment.
2. **The mesh still reads as a generic rectangular procedural enclosure:** the reference has a more photographic, tapered/rounded cap and a specific front-right pillar/side transition. V8's top remains flat and its outer shading makes the pillar too bright.
3. **Photometric mismatch remains broad:** the report records only 6/15 strict ROI passes and an overall mean absolute difference of `23.18` RGB/channel. Forehead-left, forehead-right, pillar/cheek, right flank, right glass, mid glass, handle, chamber and printed object still fail in the submitted table.
4. **Door improvement is incomplete:** darkening the pane fixes open-box glare but over-darkens the lower-left glass and printed object. The reference needs a smoked pane plus readable warm interior, not a uniformly brown/black overlay.
5. **The visual target is still not the supplied product image:** the 3D asset loads and rotates, but that is an interaction/structure result, not fidelity acceptance.

## Next action

Create the next task as a geometry-and-lighting correction/pivot. Do not spend another revision solely changing alpha/tint or compensating with camera values. The next evidence must show the reference beside the candidate and must report centered IoU, 12 landmarks, and all 15 ROI samples.
