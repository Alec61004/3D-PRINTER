# TASK-036-SOURCE-MESH-REFERENCE-CALIBRATION — Antigravity Response

- **Task ID**: `TASK-036-SOURCE-MESH-REFERENCE-CALIBRATION`
- **Status**: `completed`
- **Verdict**: `REVISION_REQUIRED` (ready for Codex visual audit)
- **Completed At**: `2026-11-25T14:14:00+07:00`

## Artifacts

- Calibrated true-3D GLB: [deltrol_p2s_source_geometry_pivot_v5_rev1.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_source_geometry_pivot_v5_rev1.glb) (`1,782,420` bytes, `62` nodes, `56` meshes, `0` missing required nodes, `0` unassigned-material nodes)
- Generator script: [build_p2s_blender_pivot_v5_rev1.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_blender_pivot_v5_rev1.py)
- Report: [TASK-036-antigravity-source-mesh-reference-calibration.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-036-antigravity-source-mesh-reference-calibration.md)
- Audit Screenshots (`1226x708`, captured from `tools/true3d_audit_viewer.html`):
  - [task036-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-front.png)
  - [task036-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-left20.png)
  - [task036-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-right20.png)
  - [task036-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-elevated.png)
  - [task036-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task036-4view-sheet.png)

## Summary

- Kept `website/src/**` untouched (`git status --short website/src` empty).
- Fixed blank material slots on `top_rim_outer`, `left_window_gasket`, and `right_window_gasket` using `Dark Seal Polymer`, removed exterior directional lamp diagonal door-shadowing and coplanar wall interpenetration in the chamber bake, and calibrated champagne-titanium exterior shading.
- Documented remaining proportional/contrast deltas honestly in the report for Codex visual audit (`W/H 1.145 vs Ref 1.042` at ~30° viewer angle, bottom-left interior dark wedge, softer rail metallic sheen).
