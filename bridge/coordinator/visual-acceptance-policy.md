# Persistent Visual Acceptance Policy

## Owner of the loop

Codex owns the review loop and the final visual verdict. Antigravity is the execution partner: it creates or revises visual assets, GLB files, textures, and screenshots according to a task. An Antigravity completion message is a handoff signal, not proof of acceptance.

## Required loop

For every handoff, Codex must:

1. Read the task file, report, outbox response, artifact manifest, and newest screenshot.
2. Compare the rendered result against the reference at the same viewport and camera angle.
3. Audit silhouette, proportions, primary geometry, materials, lighting, camera, and required interaction/asset contracts.
4. Mark the result accepted only when the visual evidence supports it.
5. If it is not close enough, issue the next revision task in the same stable Antigravity session and keep the loop active.

## Handoff state machine

`in_progress` means the executor is still working. Once the report, outbox response,
artifact and screenshot are written, the executor must close that handoff with a
terminal task state and `completed_at`: use `completed` plus
`verdict: REVISION_REQUIRED` or `verdict: BLOCKED` when Codex still has to audit or
continue, and reserve `PASS` for Codex's own audit. Keeping a ready handoff at
`in_progress` prevents the completion watcher from waking Codex.

## Three-strike meaning

Three consecutive revisions without meaningful improvement only retires the current approach. It does **not** stop the project or the acceptance loop. Codex must pivot to another asset, reconstruction method, pipeline, or reference set and continue until the target is accepted or a concrete external blocker is documented.

## Stop condition

Never stop merely because a build passes, a model loads, a model rotates, or an agent reports `completed`. Stop only after Codex's own audit records an evidence-backed `APPROVED`/`PASS`. If the result is not accepted, the next action must be a revision or pivot task.

## Persistence

This policy is part of the workspace source of truth. Read it together with `AGENTS.md` before continuing or closing a visual task, including after a long idle period or when resuming from a new conversation.

## Reference-specific acceptance gate — Deltrol P2S

This section is the persistent visual contract for the current Deltrol P2S printer. It replaces subjective decisions such as “trông khá giống” or “model load được”. The complete audit sheet is `reports/reference-fidelity-criteria.md`.

### Fixed audit setup

- Reference source: `assets/source/printer-hero-reference-2026-11-23.png`.
- Object-only target crop: `reports/ref_printer_box.png`. Do not compare against the whole webpage screenshot when judging the mesh.
- Every candidate must provide a fresh front screenshot at exactly `1226x708` using the audit viewer camera: perspective FOV `27°`, camera position `[0.86, 0.22, 1.50]`, target `[0, -0.01, 0]`, white background, pixel ratio `1`, ACES tone mapping, exposure `1.05`.
- Required secondary screenshots: front, `left20`, `right20`, and `elevated (+18°)`. A rotated view is for artifact/continuity checks; it does not waive the front-reference gate.

### Hard visual gates

All gates below must pass. A candidate is `REVISION_REQUIRED` if any one fails.

1. **Framing and silhouette:** in the front render, the printer bounding box must be measured against the same segmentation rule as the reference. Target reference crop is `W=425px`, `H=408px`, `W/H=1.042`; acceptable tolerance is ±3% for W and H, ±0.03 for W/H, and ±3px for the aligned top/bottom/left/right edges. Silhouette overlap (IoU) must be at least `0.90`; a visibly different top contour, side contour, or lower cutout is an automatic fail even if the bbox passes.
2. **Camera and pose:** the front view must use the fixed camera above; no per-candidate camera or scale cheating. The visible right-side depth, top plane, and low eye-level pitch must read like the reference. If camera changes are proposed, the task must include old/new camera values and a fresh side-by-side comparison.
3. **Primary geometry:** closed enclosure; slim left front edge; rounded, dominant front-right vertical pillar; sloped/rounded top transition into the right side; dark framed front glass; right-side dark panel/glass; compact centered lower console; integrated lower feet/base. No floating panel, detached floor, detached feet, white wedge, open seam, black diagonal bake triangle, or generic rectangular facade.
4. **Reference landmarks:** front door is closed and fills the front opening; right vertical handle is visible at the same relative height; left hinges remain visible; print head is near the upper central rail; horizontal rails span the chamber; print bed is in the lower middle; the warm printed object is visible on the bed; console sits low and centered with a dark screen and metallic rim. Missing or materially misplaced landmarks fail the front gate.
5. **Material and value hierarchy:** outer shell is champagne/neutral satin metal, not pale white or flat beige; front glass is smoked/dark but still reveals the warm chamber; right side is visibly darker than the front pillar; chamber has warm amber light; console is dark with a readable rim; background is white with a soft contact shadow. No uniform material across shell, glass, interior, and console.
6. **Photometric similarity:** on the fixed front render, compare corresponding shell, right-side, chamber, glass, and console regions using mean RGB/Delta-E or an equivalent documented metric. No key region may differ by more than `15` RGB units per channel on average; a region with a strong hue/value inversion is an automatic fail regardless of the aggregate score.
7. **Geometry integrity across views:** all four required views must show one connected, stable printer. No new artifacts, disappearing parts, z-fighting, texture projection, billboard, image plane, or 2.5D depth rig. The GLB must contain real mesh nodes for enclosure, door, front glass, print head, and bed.
8. **Interaction contract:** the default hero must remain reference-fidelity; 3D exploration may rotate only after lazy load and must preserve the same connected asset. “Can rotate” is not a visual pass.

### Decision rule and loop behavior

- Report every gate as `PASS` or `FAIL` with measured values, screenshot paths, and the reason for any failure. Do not use an aggregate “looks better” verdict.
- **Evidence-consistency rule:** numerical ROI/bbox results never override the actual fixed-fixture screenshot. If the screenshot visibly disagrees with the reference's global brightness, material hierarchy, silhouette, or landmark readability, the gate is `FAIL` and the metric is treated as invalid/misaligned until a side-by-side overlay explains it. A claimed `15/15` ROI result cannot pass a visibly dark/flat render.
- Every future handoff must include a direct reference-vs-candidate contact sheet using the same crop, plus a luminance/value-hierarchy note for forehead, pillar/cheek, right flank, glass, chamber, console and shadow. The reviewer must inspect the contact sheet before trusting sampled points.
- Analytic/unlit materials may not be used to game the ROI sampler while the fixed viewer produces a materially different visual hierarchy. If `KHR_materials_unlit` or baked color inversion is used, the report must prove the same color pipeline and the contact sheet must still pass visual inspection.
- `PASS` is reserved for Codex's audit after reading the artifact and screenshots. Antigravity's `completed` is only a handoff.
- Three consecutive revisions without meaningful improvement retire the current approach, but do not stop the project. Create a pivot task (different mesh source, reconstruction method, asset, or reference set) and reapply this same gate.
- For a single-view reference, pixel-exact hidden-side geometry is not inferable. Therefore the front view is the fidelity gate; rotated views are continuity and artifact gates unless additional multi-angle references are supplied.
