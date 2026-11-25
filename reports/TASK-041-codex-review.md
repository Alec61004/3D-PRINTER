# Codex audit — TASK-041 product silhouette and lighting pivot

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v9.glb`
- **Evidence read:** task/report/outbox, GLB payload/hash, fixed-fixture front/left20/right20/elevated images, four-view sheet and silhouette overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v9 is not promoted to the website explorer.

## Positive change

- Centered zero-shift silhouette IoU improved to `0.9154`; bbox `420×406`, ratio `1.034` is within the framing gate.
- The object remains a real connected GLB with required nodes and no reported image-plane/billboard/2.5D construction.
- Handle, console, right glass and printed-object samples improved relative to v8.

## Blocking visual differences

1. The supplied reference is a photoreal product image; v9 still visibly reads as a simplified rectangular CAD enclosure. The cap, front-right pillar, side transition and lower shell do not carry the same product-specific contour/detail.
2. The photometric gate is still far from complete: only 6/15 ROI samples pass, with overall mean error `21.52`. The pillar/cheek is `62.1` RGB/channel off, chamber mid is `47.0`, toolhead is `34.8`, front glass is `22.3`, and multiple shell regions are over-bright.
3. The front glass is now closed enough to pass the structural landmark, but the warm chamber is still too evenly bright and the model lacks the reference's natural photographic value gradient.
4. The report admits landmark #3 and #6 failures and landmark #11 partial failure. Therefore this is not a Codex `PASS` even though the bbox/IoU gate passes.

## Loop decision

V7, v8 and v9 are three consecutive iterations of the same procedural/reference-baked family. They improved framing and local samples but did not converge to the reference product appearance. Retire this construction approach and pivot to a fresh reference-derived mesh/material reconstruction. The project loop continues; only this method is retired.
