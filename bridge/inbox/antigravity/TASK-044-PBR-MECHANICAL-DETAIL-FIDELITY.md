---
task_id: TASK-044-PBR-MECHANICAL-DETAIL-FIDELITY
owner: antigravity
status: pending
created_at: 2026-11-25T21:00:00+07:00
request: Improve v11's photoreal mechanical detail and PBR material fidelity against the reference contact sheet. The model must read as the same printer, not a box with pale interior primitives.
result_path: assets/models/raw/deltrol_p2s_explorer_v12.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-043-codex-review.md`
- `reports/task043-reference-candidate-contact-sheet.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v11.glb`

# Failure to correct

V11 is framed well, but the contact sheet shows a major material/detail mismatch: reference rails, toolhead, bed, rear panel and printed object are photoreal metallic/warm parts, while v11 renders many as flat pale primitives behind a flat brown/black pane. Strict ROI is only `13/15`, and the required landmark matrix is not explicit PASS/FAIL.

# Required result

Create `assets/models/raw/deltrol_p2s_explorer_v12.glb` as real connected 3D geometry. Keep the good framing and shell proportions, but replace the flat interior reading with a true mechanical/PBR pass:

1. Use separate physically based materials for champagne shell, smoked glass, graphite frame, steel rails, copper/brass toolhead, dark bed, warm rear chamber and printed object. Do not use one unlit material to flatten all interior parts.
2. Give rails, toolhead, bed and rear hardware distinct metallic roughness/specular behavior and geometry that reads at the reference crop scale; they must not render as pale white bars/blocks.
3. Preserve the reference's warm studio gradient and glass reflection while keeping interior landmarks readable.
4. Keep the close outer silhouette, compact console, attached handle/hinges and grounded base. Do not add image planes, billboards, 2.5D rigs, detached facades, or camera compensation.

# Fixed audit

Use the unchanged viewer: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`; views `front`, `left20`, `right20`, `elevated (+18°)`.

Required evidence:

- fresh four screenshots and zero-shift silhouette overlay;
- equal-scale, unmodified reference/candidate contact sheet;
- exact post-ACES sRGB ROI coordinate table with color/alpha handling;
- all 12 landmarks explicitly `PASS` or `FAIL`;
- every key ROI ≤15 RGB/channel;
- GLB nodes/materials/image-plane validation and SHA-256.

The contact sheet is decisive. If its global metal/detail/value hierarchy visibly differs, mark `REVISION_REQUIRED` even if isolated ROI numbers pass.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v12.glb`
- `reports/TASK-044-antigravity-pbr-mechanical-detail-fidelity.md`
- `reports/task044-explorer-front.png`
- `reports/task044-explorer-left20.png`
- `reports/task044-explorer-right20.png`
- `reports/task044-explorer-elevated.png`
- `reports/task044-explorer-4view-sheet.png`
- `reports/task044-silhouette-overlay.png`
- `reports/task044-reference-candidate-contact-sheet.png`
- `bridge/outbox/TASK-044-PBR-MECHANICAL-DETAIL-FIDELITY-antigravity-response.md`

Do not edit `website/src`; Codex audits first.
