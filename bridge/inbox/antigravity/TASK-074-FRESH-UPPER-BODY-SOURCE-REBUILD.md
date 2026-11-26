---
task_id: TASK-074-FRESH-UPPER-BODY-SOURCE-REBUILD
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:24:05+07:00
created_at: 2026-11-26T10:55:00+07:00
request: >-
  Perform a genuinely fresh source-mesh rebuild of the Deltrol upper body and
  chamber/gantry region. Do not clone, rename or incrementally patch the old
  roof/ceiling nodes. Reconstruct the reference-derived upper enclosure,
  chamber opening, front glass boundary, gantry rail and printhead mounting
  surfaces as a new coherent mesh group, while locking the exterior silhouette
  and preserving the v33 lower-body material/light baseline.
result_path: assets/models/raw/deltrol_p2s_explorer_v42.glb
---

# TASK-074 — fresh upper-body source rebuild

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Non-negotiable source pivot

1. Build a new upper-body/chamber mesh group in Blender or an equivalent
   source-geometry pipeline. Do not reuse the old nodes that have caused the
   shadow conflict: `top_roof_glass`, `interior_ceiling_liner`, old upper
   chamber liners, or the copied rail assembly. Use a new node/mesh inventory
   and include it in the report.
2. Use `reports/ref_printer_box.png` as a modeling guide only; no reference
   image may ship inside the GLB or appear as a plane/texture. Model the
   closed exterior shell, recessed chamber opening, real front glass boundary,
   upper rail, mounts and printhead connection from geometry.
3. Lock the outer contour before the interior solve: bbox `W=425`, `H=408`,
   W/H `1.042`, aligned edges within ±3px, centered IoU `>=0.90`. The rail
   must not protrude outside this envelope.
4. Place the rail in the visible chamber layer using the measured v38 depth
   constraint, but solve the new roof/chamber occlusion physically. Keep glass
   real and intact; no billboard, image plane, projected texture, emission,
   global unlit, camera change or exposure trick.
5. Keep the lower body, right-side window, turbine, bed and console from the
   v33 baseline unless a documented new upper-body interface requires a small
   connection change. Preserve the warm metal/glass value hierarchy.

## Required proof of a real rebuild

- A node/mesh diff showing the old upper nodes are absent from scene 0 and a
  new upper-body group exists with new mesh primitives.
- A front before/after where the upper chamber visibly differs, not a caption
  or metadata-only change.
- A depth/occlusion diagnostic proving the rail is not behind the old roof
  shadow path.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v42.glb`
- `reports/task074-explorer-front.png`
- `reports/task074-explorer-left20.png`
- `reports/task074-explorer-right20.png`
- `reports/task074-explorer-elevated.png`
- `reports/task074-explorer-4view-sheet.png`
- `reports/task074-reference-candidate-contact-sheet.png`
- `reports/task074-fresh-upper-body-diagnostic.png`
- `reports/task074-node-mesh-diff.md`
- `reports/task074-before-after.png`
- `reports/task074-silhouette-overlay.png`
- `reports/TASK-074-antigravity-fresh-upper-body-source-rebuild.md`
- `bridge/outbox/TASK-074-FRESH-UPPER-BODY-SOURCE-REBUILD-antigravity-response.md`

Every image must be rendered from v42. The contact sheet must say
`CANDIDATE v42` and include the v42 SHA-256. The report must include all 15
ROIs, 12 landmarks, exact shell/rail measurements and GLB validation.

## Acceptance gates

- ROI 13 `dMax <= 15` and rail/printhead visibly approaches the reference;
- ROIs 01–12, 14 and 15 all `PASS` and no worse than v33;
- bbox/silhouette/framing within reference tolerance;
- new upper-body geometry is connected and coherent in all four views;
- node/mesh proof and evidence labels are correct;
- no analytic visual trick.

If a genuinely fresh upper-body source mesh still cannot satisfy these gates,
report the measured limitation and recommend a different physical asset/source;
do not claim PASS.
