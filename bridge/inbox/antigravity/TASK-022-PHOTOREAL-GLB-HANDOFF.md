---
task_id: TASK-022-PHOTOREAL-GLB-HANDOFF
owner: antigravity
status: in_progress
created_at: 2026-11-24T10:00:00+07:00
request: >-
  Tạo hoặc bàn giao một GLB photoreal mới cho máy in Deltrol/Bambu P2S, khác asset
  procedural low-poly đã bị khóa. Không chỉ bàn giao JPG/reference. GLB phải dùng
  cho Three.js trực tiếp, có vật liệu/texture đủ để thân titan satin, kính smoked,
  tay nắm, gantry, toolhead, print bed và console giống reference
  assets/source/printer-hero-reference-2026-11-23.png ở góc front-right 3/4.
  Giữ node contract enclosure, door, front_glass_door, printHead, printBed; nếu
  asset nguồn không có đúng node thì phải tạo mapping/rename trong GLB. Tạo
  screenshot mới 1226x708 và ghi rõ asset source, giới hạn và kết quả thật; không
  ghi PASS nếu chỉ có reference ảnh hoặc model vẫn low-poly.
result_path: reports/TASK-022-antigravity-photoreal-glb-handoff.md
---

# TASK-022 — Photoreal GLB handoff

## Acceptance criteria

- Có file GLB thật trong `assets/generated/antigravity/` hoặc đường dẫn artifact được nêu rõ.
- GLB có đủ node contract bắt buộc.
- Screenshot 1226x708 cho thấy GLB thật đang render trong website/preview.
- Không chỉnh lại `deltrol_p2s_unibody_pivoted.glb` hoặc script procedural cũ.
- Nếu không thể tạo GLB dùng được, ghi `BLOCKED` và nêu chính xác blocker thay vì giả lập PASS.
