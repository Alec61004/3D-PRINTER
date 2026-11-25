---
task_id: TASK-039-REFERENCE-FIDELITY-CRITERIA-PASS
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T16:00:00+07:00
completed_at: 2026-11-25T19:16:00+07:00
request: Improve the true-3D Deltrol P2S explorer against the persistent reference-fidelity acceptance sheet. Do not stop at build/load/rotation success. Produce a fresh real connected GLB candidate and fixed-fixture audit evidence.
result_path: assets/models/raw/deltrol_p2s_explorer_v7.glb
---

# Objective

The current v6 explorer is structurally valid but visibly unlike the supplied printer reference. This task is not accepted by a generic “looks better” statement. Read these files before working:

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v6.glb`
- `reports/TASK-038-codex-review.md`

# Required outcome

Create `assets/models/raw/deltrol_p2s_explorer_v7.glb` as a real connected 3D mesh. The default front 3/4 view must be rebuilt/calibrated to the reference, not merely repainted or wrapped in a photo plane. If the current construction method cannot meet the thresholds, pivot the reconstruction method or source asset instead of adding facade boxes or a 2.5D rig.

## Fixed audit fixture

Render fresh screenshots at exactly `1226x708` with the existing audit viewer fixture:

- Perspective FOV `27°`
- Camera position `[0.86, 0.22, 1.50]`
- Target `[0, -0.01, 0]`
- White background, pixel ratio `1`, ACES tone mapping, exposure `1.05`
- Views: `front`, `left20`, `right20`, `elevated (+18°)`

Reference front crop target is `W=425px`, `H=408px`, `W/H=1.042` using the same segmentation rule. Candidate tolerance is ±3% for W/H, ±0.03 for ratio, and ±3px for aligned edges. The front silhouette must achieve IoU ≥ `0.90`; a visibly different top/right/bottom contour fails even if the bbox passes.

## Geometry/appearance priorities

Match these in order and document measurements:

1. Closed continuous enclosure; no open-frame generic box reading.
2. Slim left edge, dominant rounded front-right pillar, and the reference top-to-right-side taper.
3. Closed smoked front door, attached right handle at the reference height, subtle left hinges.
4. Warm visible chamber with matching upper rails, central print head, lower bed, and printed object.
5. Compact low centered dark console with metallic rim and integrated lower base/feet.
6. Champagne/neutral satin shell, darker smoked glass/right panel, warm amber interior, white ground and soft contact shadow.
7. No floating parts, detached feet, white wedges, black diagonal artifacts, seams, z-fighting, image planes, billboards, or 2.5D depth rigs.

## Mandatory handoff files

Write all of the following before closing the task:

- `assets/models/raw/deltrol_p2s_explorer_v7.glb`
- `reports/TASK-039-antigravity-reference-fidelity-criteria-pass.md`
- `reports/task039-explorer-front.png`
- `reports/task039-explorer-left20.png`
- `reports/task039-explorer-right20.png`
- `reports/task039-explorer-elevated.png`
- `reports/task039-explorer-4view-sheet.png`
- `bridge/outbox/TASK-039-REFERENCE-FIDELITY-CRITERIA-PASS-antigravity-response.md`

The report must include:

- GLB node/mesh/image-plane validation and SHA-256.
- Front bbox `(xmin, ymin, xmax, ymax, W, H, W/H)`.
- Silhouette overlay/IoU evidence.
- A PASS/FAIL result for each of the 12 landmarks in `reports/reference-fidelity-criteria.md`.
- Material/photometric samples for shell, right side, chamber, glass, and console.
- Honest remaining deltas. Do not claim PASS unless every hard visual gate is evidenced.

Do not edit `website/src` in this task. Codex will audit the artifact first and decide whether to integrate it.
