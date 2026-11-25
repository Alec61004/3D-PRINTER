---
task_id: TASK-040-CLOSED-DOOR-REFERENCE-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-25T19:30:00+07:00
completed_at: 2026-11-25T19:25:00+07:00
request: Pivot the true-3D explorer toward the reference's closed smoked-glass printer appearance. Do not stop at framing or structural GLB validity; the front must visually match the reference.
result_path: assets/models/raw/deltrol_p2s_explorer_v8.glb
---

# Context

Read before working:

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-039-codex-review.md`
- `assets/source/printer-hero-reference-2026-11-23.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v7.glb`

TASK-039 improved the bbox but failed the actual visual target. Its front render still reads as an open-frame beige model: the front glass is too clear/bright, the top cap is flat, and the shell/right-side/chamber value hierarchy is wrong. This task is a pivot of visual construction, not a website task.

# Non-negotiable target

Create `assets/models/raw/deltrol_p2s_explorer_v8.glb` as a real connected 3D GLB. The default front 3/4 render must read immediately as the same printer as `reports/ref_printer_box.png`:

- A closed, dark smoked front door/pane fills the opening and remains transparent enough to show the warm chamber.
- The front door frame is flush and proportioned like the reference; right vertical handle and subtle left hinges remain attached.
- The outer shell is champagne/neutral satin: light forehead, darker right side, dominant rounded front-right pillar, slim left edge, tapered/rounded top-to-side transition.
- The lower console is compact, low, centered, dark-screened with a metallic rim, and integrated into the base.
- Rails, printhead, bed and printed object are visible through the glass but do not turn the front into a bright open box.
- No detached/floating parts, white wedge, black triangle, open seam, z-fighting, billboard, image plane, or 2.5D rig.

# Fixed audit

Use the same `tools/true3d_audit_viewer.html` fixture and produce fresh `1226x708` screenshots for `front`, `left20`, `right20`, and `elevated (+18°)` with FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`.

Required front measurements:

- bbox target `425×408`, `W/H=1.042`; tolerance ±3% W/H and ±0.03 ratio;
- centered silhouette IoU must be ≥ `0.90` without relying on a shifted comparison;
- no visibly different top/right/bottom contour;
- no key photometric ROI over 15 RGB/channel mean error;
- all 12 landmarks in `reports/reference-fidelity-criteria.md` explicitly PASS.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v8.glb`
- `reports/TASK-040-antigravity-closed-door-reference-pivot.md`
- `reports/task040-explorer-front.png`
- `reports/task040-explorer-left20.png`
- `reports/task040-explorer-right20.png`
- `reports/task040-explorer-elevated.png`
- `reports/task040-explorer-4view-sheet.png`
- `reports/task040-silhouette-overlay.png`
- `bridge/outbox/TASK-040-CLOSED-DOOR-REFERENCE-PIVOT-antigravity-response.md`

The report must include GLB validation, SHA-256, bbox, centered IoU, the 12-landmark matrix, and the 15 photometric ROI table with honest PASS/FAIL values. Do not edit `website/src`; Codex will audit and decide integration.
