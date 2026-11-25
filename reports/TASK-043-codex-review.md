# Codex audit — TASK-043 visual evidence integrity render pass

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v11.glb`
- **Evidence read:** task/report/outbox, GLB hash/payload, direct contact sheet, front render, four-view sheet and overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v11 is not promoted to the website explorer.

## What improved

- The contact sheet now compares equal-scale crops and exposes the real mismatch instead of hiding it behind a metric-only report.
- Framing and silhouette remain close (`422×407`, centered IoU `0.9159`).
- Exterior brightness is closer than v10, and there are no obvious detached or image-plane artifacts.

## Blocking differences visible in the contact sheet

1. The reference has photoreal metal rails, toolhead, bed, rear panels and printed object. V11 renders many of these as flat pale/white primitives with weak metallic response, so the interior does not read like the same machine.
2. The reference has a rich warm studio gradient through the smoked glass; v11 has a much flatter brown/black interior and loses the reference's controlled reflections and local depth cues.
3. The shell silhouette is close in bbox but still visibly more rectangular and generic around the top cap, right side and lower base.
4. The strict ROI gate is not complete: `13/15` pass, with the steel rail and turbine arch still over threshold. The task requires every key ROI, not “most”.
5. The report's landmark table uses qualitative labels such as `Strong`/`Minor Delta` instead of the required explicit PASS/FAIL matrix, so it cannot be accepted as final evidence.

The direct contact sheet is the decisive evidence: v11 is a valid 3D model but not yet a visual match to the supplied reference.

## Required next direction

Continue with a real PBR/geometry detail pass: distinct metal/glass/interior materials, physically readable rails/toolhead/bed/rear hardware, and reference-matched warm reflections. Do not solve this by more global tint, unlit flattening, or isolated ROI tuning.
