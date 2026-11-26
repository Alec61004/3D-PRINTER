---
task_id: TASK-046-RAIL-TURBINE-CONTRAST-FINAL
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-26T08:40:45+07:00
created_at: 2026-11-26T09:00:00+07:00
request: Final focused correction of the rail/toolhead/turbine material contrast in v13. Keep the accepted shell/framing unchanged and make only the failing interior metal regions match the reference.
result_path: assets/models/raw/deltrol_p2s_explorer_v14.glb
---

# Read first

- `AGENTS.md`
- `bridge/coordinator/visual-acceptance-policy.md`
- `reports/reference-fidelity-criteria.md`
- `reports/TASK-045-codex-review.md`
- `reports/task045-reference-candidate-contact-sheet.png`
- `reports/ref_printer_box.png`
- `assets/models/raw/deltrol_p2s_explorer_v13.glb`

# Exact remaining failure

V13's exterior and framing are acceptable, but its front interior is still visibly too pale/flat. The failed regions are explicit:

- `13_Steel_Rail`: reference `(114.3,93.3,80.4)`, candidate `(80.3,65.7,55.4)`, `dMax=34.0`.
- `14_Turbine_Arch`: reference `(109.0,88.1,72.7)`, candidate `(90.1,77.7,64.9)`, `dMax=18.8`.

# Required correction

Create `assets/models/raw/deltrol_p2s_explorer_v14.glb` from v13 with the exterior geometry/framing preserved:

1. Tune steel rails and crossbeam to a warm medium bronze/chrome response matching the reference values above: not white, not black, with visible cylindrical specular bands and darker undersides.
2. Tune the turbine/printed arch to a warm metallic highlight matching `(109,88,73)` while retaining dark fin pockets and the readable lower-middle silhouette.
3. Tune the toolhead cowl/rotor consistently with the rail and arch materials; it must read as compact copper/dark alloy, not a pale block.
4. Do not change camera, shell silhouette, glass framing, console, or right-side values except where strictly necessary to keep the interior visible.
5. No global tint, unlit flattening, image plane, billboard, 2.5D rig, or detached facade.

# Fixed acceptance

Use unchanged `tools/true3d_audit_viewer.html`: `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES, exposure `1.05`; render front/left20/right20/elevated and an equal-scale reference/candidate contact sheet.

Must pass:

- centered IoU ≥ `0.90`, bbox tolerance;
- rail and turbine ROI `dMax ≤ 15`, plus every other key ROI `≤15`;
- all 12 landmarks explicit `PASS`;
- direct contact sheet visibly shows warm metallic rails/toolhead/turbine like the reference;
- no artifact or hidden 2.5D construction.

# Deliverables

- `assets/models/raw/deltrol_p2s_explorer_v14.glb`
- `reports/TASK-046-antigravity-rail-turbine-contrast-final.md`
- `reports/task046-explorer-front.png`
- `reports/task046-explorer-left20.png`
- `reports/task046-explorer-right20.png`
- `reports/task046-explorer-elevated.png`
- `reports/task046-explorer-4view-sheet.png`
- `reports/task046-silhouette-overlay.png`
- `reports/task046-reference-candidate-contact-sheet.png`
- `bridge/outbox/TASK-046-RAIL-TURBINE-CONTRAST-FINAL-antigravity-response.md`

Do not edit `website/src`; Codex audits first.
