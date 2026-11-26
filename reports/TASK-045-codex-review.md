# Codex audit — TASK-045 interior metal contrast closeout

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v13.glb`
- **Evidence read:** task/report/outbox, GLB hash/payload, direct contact sheet, front render, four-view sheet and silhouette overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v13 is not promoted to the website explorer.

## Accepted progress

- Exterior/framing remains stable: bbox `423×404`, ratio `1.047`, centered IoU `0.9073`.
- Shell, console, right-side glass and chamber floor remain close to the previous pass.
- No detached geometry, billboard, image plane or major artifact is visible.

## Remaining blockers

1. The direct contact sheet still shows rails and toolhead as pale/low-contrast pieces instead of warm dark machined metal with crisp highlights.
2. The report records `13/15` ROI and `10/12` landmark pass. `13_Steel_Rail` is `dMax=34.0`; `14_Turbine_Arch` is `dMax=18.8`. Landmarks #9 and #12 fail.
3. The printed arch/bed and rails do not carry the reference's bronze/chrome local reflections. This is still a visible material hierarchy problem, not a framing problem.

The candidate is close enough to keep the exterior, but not close enough for final acceptance.
