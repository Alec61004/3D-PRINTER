---
task_id: TASK-018-3D-ASSET-PIPELINE-PIVOT
owner: antigravity
status: completed
created_at: 2026-11-23T22:00:00+07:00
request: Xây lại hướng asset 3D cho Hero máy in Deltrol bằng pipeline mới, không tiếp tục vá hình học box của GLB hiện tại.
result_path: reports/TASK-018-antigravity-3d-asset-pivot.md
response_path: bridge/outbox/TASK-018-3D-ASSET-PIPELINE-PIVOT-antigravity-response.md
---

# TASK-018 — Pivot pipeline asset 3D

## Mục tiêu

Tạo một asset 3D mới có silhouette và góc front-right 3/4 gần ảnh chuẩn nhất có
thể, thay cho việc tiếp tục sửa các khối hộp trong
`assets/models/optimized/deltrol_p2s_optimized.glb`.

Reference chuẩn:

- `assets/source/printer-hero-reference-2026-11-23.png`

## Bắt buộc

1. Không chỉnh tiếp các `add_box`/shader/camera nhỏ trong GLB hiện tại để che lỗi silhouette.
2. Chọn một hướng mới: asset 3D được tạo lại từ reference đa góc, asset GLB chất lượng cao hơn,
   hoặc mesh có bevel thật từ pipeline tương đương Blender.
3. Giữ đúng các đặc điểm nhìn thấy trong reference: thân bạc/xám trung tính, vỏ kín bo tròn,
   cửa kính lớn phía trước, tay nắm dọc bên phải, khung hông kính rộng, gantry và bàn in nằm
   đúng trong khoang.
4. Nếu chỉ có một góc ảnh và không thể suy ra hình học chắc chắn, ghi rõ giới hạn và đề xuất
   reference bổ sung; không tự ghi PASS.
5. Tạo screenshot desktop mới cùng kích thước với reference và report có verdict đúng một trong
   `PASS`, `REVISION_REQUIRED`, `BLOCKED`.
6. Không sửa source kỹ thuật React/Three.js của Codex. Asset mới phải đặt trong
   `assets/models/raw/` hoặc `assets/generated/antigravity/`; Codex sẽ đưa qua GLB repair harness.

## Tiêu chí audit

- Ưu tiên silhouette, tỷ lệ, góc nhìn và các mảng lớn trước chi tiết vật liệu.
- Không tính build pass, model load được hoặc xoay được là đạt visual.
- Nếu không có cải thiện rõ ràng so với screenshot hiện tại, báo `REVISION_REQUIRED` hoặc
  `BLOCKED` và nêu pipeline thay thế cụ thể.
