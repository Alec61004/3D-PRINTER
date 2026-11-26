---
task_id: TASK-048-DEBUG-REFERENCE-PROJECTION
owner: antigravity
status: pending
created_at: 2026-11-26T09:30:00+07:00
request: Debug and prove the reference-painted texture projection on the real mesh. The rail/turbine render must visibly change to match reference; do not report a projection based only on a helper function existing in the script.
result_path: assets/models/raw/deltrol_p2s_explorer_v16.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-047-codex-review.md`
- `reports/task047-reference-candidate-contact-sheet.png`
- `assets/models/raw/deltrol_p2s_explorer_v15.glb`
- `scripts/build_p2s_explorer_v15.py`

# Failure to correct

V15 claims a reference projection onto rail/turbine mesh surfaces, but the actual fixed render and metrics are unchanged from v14: `13_Steel_Rail dMax=34.0`, `14_Turbine_Arch dMax=18.8`. The projection is not proven to reach the displayed surfaces.

# Required debugged result

Create `assets/models/raw/deltrol_p2s_explorer_v16.glb` with the same true-3D/no-billboard constraints, but instrument the projection pipeline:

1. Identify exact GLB node/material/primitive assignments for every rail and turbine mesh that appears in the ROI.
2. Produce the actual texture atlas images used by those primitives and show the source reference pixel coordinates mapped into them.
3. Include a before/after render or diagnostic texture pass proving the rail and turbine colors change toward the reference. The final render must not leave those parts pale white.
4. Use reference target samples approximately `(114,93,80)` for the steel rail and `(109,88,73)` for the turbine arch while retaining dark undersides/fin pockets and 3D depth.
5. Keep all existing shell/framing/door/console geometry; no whole-image plane, billboard, 2.5D rig, detached facade or camera cheat.

# Fixed acceptance

Use unchanged viewer fixture: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`; views `front`, `left20`, `right20`, `elevated (+18°)`.

Must include:

- final four views and equal-scale reference/candidate contact sheet;
- centered IoU/bbox;
- exact post-ACES ROI table;
- explicit 12-landmark PASS/FAIL matrix;
- rail and turbine ROI ≤15 RGB/channel and visible warm metal in contact sheet;
- texture atlas files/paths, material-to-node mapping, source pixel mapping and before/after diagnostic evidence;
- GLB validation proving real mesh surfaces and no image-plane/billboard/2.5D construction.

Do not edit `website/src`; Codex audits before integration.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v16.glb`
- `reports/TASK-048-antigravity-debug-reference-projection.md`
- `reports/task048-explorer-front.png`
- `reports/task048-explorer-left20.png`
- `reports/task048-explorer-right20.png`
- `reports/task048-explorer-elevated.png`
- `reports/task048-explorer-4view-sheet.png`
- `reports/task048-silhouette-overlay.png`
- `reports/task048-reference-candidate-contact-sheet.png`
- `reports/task048-projection-diagnostic.png`
- `bridge/outbox/TASK-048-DEBUG-REFERENCE-PROJECTION-antigravity-response.md`
