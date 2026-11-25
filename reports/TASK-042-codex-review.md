# Codex audit — TASK-042 fresh reference-derived mesh pivot

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v10.glb`
- **Evidence read:** task/report/outbox, GLB hash/payload, front/left20/right20/elevated renders, four-view sheet and silhouette overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v10 is not promoted to the website explorer.

## What is valid

- The GLB is a real mesh asset with the required logical nodes and no reported billboard/image-plane/2.5D construction.
- Framing is close: `423×407`, ratio `1.0393`; centered IoU `0.9187` passes the geometry-framing threshold.
- The submitted artifact has no obvious detached-foot/white-wedge/black-triangle failure in the four views.

## Why the visual result still fails

The direct `task042-explorer-front.png` and four-view sheet do not look like `reports/ref_printer_box.png`:

1. The candidate's whole exterior is dark brown/gray and flat, while the reference has a bright champagne forehead and controlled darker right side. The global value hierarchy is wrong even though the report claims `15/15` sampled ROI passes.
2. The smoked door is too opaque/dim: rails, toolhead, bed and printed object are barely readable. The reference keeps these interior landmarks legible through the dark glass.
3. The top cap, front-right pillar and right-side transition still read as a simple rectangular box rather than the reference's photoreal product shell.
4. The report's photometric table is not sufficient evidence because its values contradict the direct screenshot. V10 uses an analytic/unlit/baked color pipeline; until a same-pipeline contact sheet and luminance hierarchy prove the samples are aligned, the screenshot wins under the evidence-consistency rule.
5. Therefore the visual acceptance gate is not met despite the good bbox/IoU numbers. The 12/12 and 15/15 claims are not accepted as final Codex verdicts.

## Required next direction

Keep the true-3D requirement, but correct the render/material pipeline so the actual fixed-fixture screenshot visibly matches the reference: bright champagne exterior, darker but not black smoked glass, readable warm interior, correct right-side contrast and natural photographic gradients. Include a direct reference/candidate contact sheet and luminance/value-hierarchy evidence; do not rely on isolated ROI samples.
