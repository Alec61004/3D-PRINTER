---
task_id: TASK-045-INTERIOR-METAL-CONTRAST-CLOSEOUT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T08:37:30+07:00
created_at: 2026-11-25T21:25:00+07:00
request: Close the remaining interior mechanical contrast gap in v12 while preserving its improved exterior. Rails, toolhead, bed and turbine must render like the reference's dark/warm machined metal, not pale primitives.
result_path: assets/models/raw/deltrol_p2s_explorer_v13.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-044-codex-review.md`
- `reports/task044-reference-candidate-contact-sheet.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v12.glb`

# Current failure

V12 improved the shell but the direct contact sheet still shows pale, flat interior rails/toolhead/bed/turbine. The reference has warm bronze/chrome hardware with localized dark/light reflections. Strict evidence is `13/15` ROI and `10/12` landmarks; #7 steel rail and #8 printed arch fail.

# Required result

Create `assets/models/raw/deltrol_p2s_explorer_v13.glb`, preserving the v12 exterior geometry and framing while correcting the actual fixed-view render:

1. Rails and linear hardware: dark steel/chrome base, warm reflected highlights, visible cylindrical specular bands; never uniform white.
2. Toolhead: copper/dark alloy with a readable fan bore, nozzle and warm local reflection; match the reference's compact upper-center mass.
3. Bed/printed object/turbine: dark graphite bed and warm metallic object with crisp but controlled highlight; do not wash out to white or flatten to gray.
4. Chamber: warm bronze gradient with dark rear separation and sufficient smoked-glass transparency to read all landmarks.
5. Keep shell/pillar/door/console/handle/base from v12; no camera compensation, billboard, image plane, 2.5D rig or detached facade.

# Fixed evidence

Use unchanged viewer fixture: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`; views `front`, `left20`, `right20`, `elevated (+18°)`.

Required:

- fresh four screenshots, zero-shift silhouette overlay and equal-scale reference/candidate contact sheet;
- bbox + centered IoU;
- exact post-ACES ROI table;
- explicit PASS/FAIL for all 12 landmarks;
- every key ROI ≤15 RGB/channel;
- GLB/material/node/image-plane validation and SHA-256.

The contact sheet must visibly show the same warm metallic interior hierarchy as the reference. Isolated numbers cannot override a pale/flat render.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v13.glb`
- `reports/TASK-045-antigravity-interior-metal-contrast-closeout.md`
- `reports/task045-explorer-front.png`
- `reports/task045-explorer-left20.png`
- `reports/task045-explorer-right20.png`
- `reports/task045-explorer-elevated.png`
- `reports/task045-explorer-4view-sheet.png`
- `reports/task045-silhouette-overlay.png`
- `reports/task045-reference-candidate-contact-sheet.png`
- `bridge/outbox/TASK-045-INTERIOR-METAL-CONTRAST-CLOSEOUT-antigravity-response.md`

Do not edit `website/src`; Codex audits before integration.
