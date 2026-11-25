---
task_id: TASK-021-3D-ASSET-PIPELINE-PIVOT
owner: antigravity
status: completed
created_at: 2026-11-24T06:00:00+07:00
request: >-
  Pivot khỏi pipeline low-poly unibody hiện tại sau 3 lần visual audit không cải thiện.
  Không chỉnh tiếp deltrol_p2s_unibody_pivoted.glb và không chỉ đổi shader/camera.
  Hãy đề xuất và thực hiện một hướng khác để đạt silhouette photoreal front-right 3/4
  giống reference assets/source/printer-hero-reference-2026-11-23.png: (1) asset GLB
  khác có chất lượng cao hơn, hoặc (2) dựng lại mesh bằng phương pháp khác với bevel,
  kính, khung, tay nắm, gantry, toolhead, print bed và console đúng hình học. Nếu
  không thể đạt bằng asset mới, tạo bộ reference đa góc tối thiểu front/side/top và
  ghi rõ giới hạn để Codex chọn pipeline Blender/equivalent. Bắt buộc tạo screenshot
  mới cùng kích thước 1226x708, ghi rõ phương pháp mới, asset source và các node
  contract cần giữ. Không tự ghi PASS nếu silhouette chưa gần reference.
result_path: reports/TASK-021-antigravity-3d-asset-pipeline-pivot.md
---

# TASK-021 — 3D asset pipeline pivot

## Acceptance criteria

- Không tiếp tục chỉnh cùng mesh low-poly hiện tại.
- Có phương pháp/asset thay thế được mô tả và có artifact thật trong workspace.
- Có screenshot mới 1226x708 cùng góc nhìn reference để Codex audit.
- Giữ hoặc nêu rõ kế hoạch ánh xạ node contract: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
- Nếu chưa đạt visual fidelity, ghi `REVISION_REQUIRED`/`BLOCKED`, không ghi `PASS`.
