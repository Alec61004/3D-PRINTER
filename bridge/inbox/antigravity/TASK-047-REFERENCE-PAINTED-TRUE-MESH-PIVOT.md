---
task_id: TASK-047-REFERENCE-PAINTED-TRUE-MESH-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T08:45:35+07:00
created_at: 2026-11-26T09:15:00+07:00
request: Pivot away from the stalled v12-v14 PBR/material family. Build a real connected mesh whose actual front render matches the reference using per-surface reference-derived texture/material projection, while forbidding a whole-image plane, billboard, or 2.5D rig.
result_path: assets/models/raw/deltrol_p2s_explorer_v15.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-046-codex-review.md`
- `reports/ref_printer_box.png`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `assets/models/raw/deltrol_p2s_explorer_v14.glb`

# Why the current pipeline is retired

V12, v13 and v14 kept the same visible interior failure. The fixed renders remain pale/flat inside the glass; `13_Steel_Rail` stays at `dMax=34.0` and `14_Turbine_Arch` at `18.8`. Changing PBR values inside this viewer has not converged.

# New construction method

Create `assets/models/raw/deltrol_p2s_explorer_v15.glb` as a genuine connected 3D mesh with product-specific geometry. To achieve front-reference fidelity, use a materially different approach such as camera-projected/reference-derived textures or painted per-surface atlases on the actual shell, glass, rails, toolhead, bed and printed object. This is allowed only when:

- every visible element is still attached to real mesh geometry with physical depth and can be inspected/rotated;
- textures are assigned to the corresponding surfaces, not one full reference image on a plane;
- there is no billboard, image plane, stacked 2.5D depth rig, detached facade, or camera-facing cheat;
- rotated views remain coherent enough to pass artifact/continuity checks.

The goal is that the front contact sheet visually reads as the supplied photoreal printer, including the warm metallic rails/toolhead/turbine detail that the PBR family failed to reproduce.

# Fixed acceptance

Use unchanged `tools/true3d_audit_viewer.html`: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`; render `front`, `left20`, `right20`, `elevated (+18°)` and an equal-scale contact sheet.

Must pass:

- centered zero-shift IoU ≥ `0.90`, bbox tolerance;
- all 12 landmarks explicit `PASS`;
- every key ROI ≤15 RGB/channel;
- direct contact sheet visibly matches the reference's shell, glass, warm interior, rails, toolhead, bed and turbine;
- GLB inspection proves real mesh surfaces and no whole-image plane/billboard/2.5D construction;
- rotated views show no texture-sheet collapse, floating parts or broken depth.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v15.glb`
- `reports/TASK-047-antigravity-reference-painted-true-mesh-pivot.md`
- `reports/task047-explorer-front.png`
- `reports/task047-explorer-left20.png`
- `reports/task047-explorer-right20.png`
- `reports/task047-explorer-elevated.png`
- `reports/task047-explorer-4view-sheet.png`
- `reports/task047-silhouette-overlay.png`
- `reports/task047-reference-candidate-contact-sheet.png`
- `bridge/outbox/TASK-047-REFERENCE-PAINTED-TRUE-MESH-PIVOT-antigravity-response.md`

Do not edit `website/src`; Codex audits before integration.
