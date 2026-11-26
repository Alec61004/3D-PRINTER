# Codex audit — TASK-047 reference-painted true-mesh pivot

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v15.glb`
- **Evidence read:** task/report/outbox, GLB hash/payload, direct contact sheet, front render, four-view sheet and overlay.
- **Codex verdict:** `REVISION_REQUIRED / PROJECTION_DEBUG_REQUIRED`
- **Integration:** v15 is not promoted to the website explorer.

## Audit result

The artifact remains a real mesh and the framing gate remains `423×404`, centered IoU `0.9073`, but the new projection method did not produce a measurable or visible change in the failing regions:

- Steel rail ROI remains exactly `dMax=34.0`.
- Turbine arch ROI remains exactly `dMax=18.8`.
- The contact sheet still shows pale/low-contrast rails and turbine instead of the reference's warm machined metal.
- The report does not provide texture-map images, per-material assignments, source-to-atlas pixel coordinates, or a before/after sample proving the projection reached those surfaces.

The presence of a `project_ref_rgb` function is not evidence that the projection affected the rendered mesh. This handoff fails visual acceptance and requires a debugged, instrumented projection/material pass.
