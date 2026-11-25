---
task_id: TASK-043-VISUAL-EVIDENCE-INTEGRITY-RENDER-PASS
owner: antigravity
status: pending
created_at: 2026-11-25T20:35:00+07:00
request: Correct v10's actual rendered appearance so it visibly matches the reference, and provide evidence that the photometric metrics and screenshot use the same color pipeline. Preserve true 3D; do not optimize isolated ROI numbers while the whole image remains dark/flat.
result_path: assets/models/raw/deltrol_p2s_explorer_v11.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-042-codex-review.md`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v10.glb`

# Failure to correct

V10 passes bbox/IoU on paper but the direct fixed-fixture screenshot is visibly wrong: the shell is dark brown/gray instead of champagne, the smoked front glass hides the rails/bed/toolhead/object, and the exterior still reads as a generic rectangular box. Its claimed `15/15` ROI table conflicts with the screenshot because the analytic/unlit/baked color pipeline is not yet proven equivalent to the reference comparison.

# Required result

Create `assets/models/raw/deltrol_p2s_explorer_v11.glb` as real connected 3D geometry and make the actual render visually match the reference crop:

1. Bright champagne/neutral satin forehead and lower shell with natural gradients.
2. Darker right side and cheek, but not a crushed-black exterior.
3. Smoked front glass that is visibly closed while keeping rails, printhead, bed and printed object readable at reference contrast.
4. Correct product-specific top cap/pillar/side transition, compact console, handle, hinges and grounded base.
5. No billboard, image plane, 2.5D rig, detached facade, floating parts, white wedge, black bake artifact or z-fighting.

# Fixed render and evidence

Use the unchanged audit viewer: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`, and views `front`, `left20`, `right20`, `elevated (+18°)`.

In addition to the four views and silhouette overlay, the handoff MUST include a direct contact sheet showing the same-crop reference beside the candidate at equal scale, with no recoloring or post-processing. It must annotate the luminance/value hierarchy for: forehead, pillar/cheek, right flank, front glass, chamber, console and contact shadow.

The ROI table must show the exact source crop coordinates, candidate coordinates, color space, alpha handling and whether values are sampled before or after tone mapping. If unlit/baked materials are used, prove the viewer and reference are in the same color pipeline. Any visible global mismatch overrides the table and remains `REVISION_REQUIRED`.

# Acceptance gates

- bbox and centered IoU thresholds from `reports/reference-fidelity-criteria.md`;
- 12 landmarks pass;
- every key ROI ≤15 RGB/channel;
- direct contact sheet visibly matches the reference's brightness, material hierarchy and readable interior;
- no artifact or hidden image-plane construction.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v11.glb`
- `reports/TASK-043-antigravity-visual-evidence-integrity-render-pass.md`
- `reports/task043-explorer-front.png`
- `reports/task043-explorer-left20.png`
- `reports/task043-explorer-right20.png`
- `reports/task043-explorer-elevated.png`
- `reports/task043-explorer-4view-sheet.png`
- `reports/task043-silhouette-overlay.png`
- `reports/task043-reference-candidate-contact-sheet.png`
- `bridge/outbox/TASK-043-VISUAL-EVIDENCE-INTEGRITY-RENDER-PASS-antigravity-response.md`

Do not edit `website/src`; Codex will audit independently before integration.
