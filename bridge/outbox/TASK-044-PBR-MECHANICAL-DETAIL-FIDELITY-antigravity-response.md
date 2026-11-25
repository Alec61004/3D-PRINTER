---
task_id: TASK-044-PBR-MECHANICAL-DETAIL-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-25T21:10:00+07:00
artifact_path: assets/models/raw/deltrol_p2s_explorer_v12.glb
report_path: reports/TASK-044-antigravity-pbr-mechanical-detail-fidelity.md
---

# TASK-044 Antigravity Response — `v12` PBR & Mechanical Detail Pass

Completed `assets/models/raw/deltrol_p2s_explorer_v12.glb` (`scripts/build_p2s_explorer_v12.py`) using true-3D multi-material PBR (`18` distinct materials) and mechanical assemblies, audited with unmodified `tools/true3d_audit_viewer.html` (`1226x708`, FOV `27°`, camera `[0.86, 0.22, 1.50]`, exposure `1.05`).

## Key Measurements & Honest Status

- **Artifact**: `assets/models/raw/deltrol_p2s_explorer_v12.glb` (`3,266,096` bytes, `SHA-256: 24412A38281A7337DC09A6C9332605A78147B788135E9C8F477D87543BCFB35A`, `63` GLB nodes, `Missing required nodes: []`, zero billboards / image planes / 2.5D rigs).
- **Framing & Silhouette** (same `< 220` segmentation rule as `ref_printer_box.png`):
  - Ref `426x409` `(27, 52, 453, 461)` vs Cand `423x404` `(396, 174, 819, 578)` (`dW=-0.70%`, `dH=-1.22%`, `Centered IoU = 0.9073`).
- **Same-Pipeline ROI Check (`Post-ACES sRGB uint8`)**: **`13 / 15 PASS`** (`<= 15 RGB/ch`, `01..12` + `15` within `1.2–13.1 RGB/ch`), **`2 FAIL`**: `13_Steel_Rail` (`dMax = 17.0`) and `14_Turbine_Arch` (`dMax = 16.2`).
- **12-Landmark Explicit Matrix**: **`10 / 12 PASS`**, **`2 / 12 FAIL`** (`#7` upper rails/toolhead metallic specular contrast + ROI `17.0`; `#8` turbine arch metallic sheen contrast + ROI `16.2`).
- **Honest Contact-Sheet Assessment**: Marked `verdict: REVISION_REQUIRED` — exterior shell hierarchy (`1.2–7.1 RGB`), right flank/window (`1.9–3.5 RGB`), OLED console (`3.2 RGB`), matte dark floor (`7.2 RGB`), skylight wedge (`7.9 RGB`), and multi-angle roof flushness are visually clean across all 4 views, while interior brushed metals still read softer than the crisp high-contrast chrome highlights of `ref_printer_box.png` without an environment reflection probe in the fixed audit viewer.
- **Untouched Scope**: Confirmed `website/src/**`, `tools/true3d_audit_viewer.html`, `assets/source/printer-hero-reference-2026-11-23.png`, and `reports/ref_printer_box.png` remain untouched via `git status --short`.
