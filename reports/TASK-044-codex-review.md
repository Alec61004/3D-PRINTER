# Codex audit — TASK-044 PBR mechanical detail fidelity

- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v12.glb`
- **Evidence read:** task/report/outbox, GLB payload/hash, direct contact sheet, front render, four-view sheet and overlay.
- **Codex verdict:** `REVISION_REQUIRED`
- **Integration:** v12 is not promoted to the website explorer.

## Improvements confirmed

- The outer shell value hierarchy and framing are closer than v11.
- v12 contains more named mechanical parts and separate material assignments.
- Bbox `423×404`, ratio `1.047`, and centered IoU `0.9073` pass the framing gate.
- No obvious image plane, billboard, detached foot or black bake artifact is visible.

## Blocking differences

1. The contact sheet still shows rails, toolhead, vertical hardware and the turbine/bed assembly as pale, low-contrast primitives. The reference shows dark/warm machined metal with crisp localized reflections. This is a global interior-material mismatch, not only a two-pixel ROI issue.
2. The report itself records `13/15` ROI pass and `10/12` landmark pass. Steel rail and turbine arch fail the strict threshold; landmarks #7 and #8 fail.
3. The candidate's chamber depth/readability remains materially different: the reference has strong warm bronze/black separation and a detailed printed object, while v12's interior is flatter and more uniformly beige/white.
4. A valid GLB with many PBR materials is not proof that the materials render correctly in the fixed viewer. The direct contact sheet remains the deciding evidence.

## Next action

Keep the exterior v12 geometry, but perform a focused interior contrast/material closeout: dark warm steel rails, copper/dark toolhead, warm metallic turbine/printed object, readable but smoked glass, and matching local reflections. Re-submit the same fixed-fixture evidence with explicit PASS/FAIL.
