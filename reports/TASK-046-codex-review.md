# Codex audit — TASK-046 rail/turbine contrast final

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v14.glb`
- **Evidence read:** task/report/outbox, GLB hash/payload, direct contact sheet, front render, four-view sheet and overlay.
- **Codex verdict:** `REVISION_REQUIRED / PIVOT_REQUIRED`
- **Integration:** v14 is not promoted to the website explorer.

## Audit result

The handoff is structurally valid and framing remains close (`423×404`, centered IoU `0.9073`), but v14 is effectively a no-op relative to v13 for the failing regions:

- `13_Steel_Rail` remains `dMax=34.0`.
- `14_Turbine_Arch` remains `dMax=18.8`.
- The contact sheet still shows pale/flat interior hardware instead of the reference's dark warm machined metal.
- The same 13/15 ROI and 10/12 landmark result remains.

This is the third consecutive pass in the v12–v14 PBR/material-tuning family without resolving the same interior mismatch. The family is retired under the persistent three-strike rule. The project does not stop; the next task must use a different rendering/material construction method.
