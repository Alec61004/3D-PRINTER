---
task_id: TASK-026-HERO-FIDELITY-MODE-SPLIT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T20:57:00+07:00
completed_at: 2026-11-24T21:11:00+07:00
request: >-
  Sửa hướng triển khai sau khi TASK-025 bị audit fail. Không tiếp tục texture
  billboard trên GLB trong cùng composition vì nó tạo mặt phẳng trắng lệch và
  phá silhouette. Tách rõ chế độ fidelity của hero và chế độ khám phá 3D.
result_path: reports/TASK-026-antigravity-hero-fidelity-mode-split.md
---

# TASK-026 — Hero fidelity mode + 3D exploration mode

## Nguyên nhân đã xác nhận

Screenshot TASK-025 có billboard bị scale/alpha/composite sai: mặt phẳng trắng
khổng lồ che máy, nền xám và vị trí không khớp reference. Không được sửa tiếp
shader/material/camera trên `reflocked_hero_billboard`.

## Hướng triển khai

- Dùng `website/public/hero_architectural_printer.png` theo đúng alpha/crop của
  ảnh gốc làm **Reference Fidelity mode** mặc định của hero; không ép ảnh này lên
  plane 3D méo phối cảnh.
- Giữ GLB/Three.js riêng trong **3D Exploration mode** sau một nút/chuyển chế độ
  rõ ràng. Mode 3D được phép xoay/tương tác nhưng không được giả vờ là pixel-match
  với một ảnh đơn góc nhìn.
- Không được để GLB hoặc billboard hỏng render chồng lên nhau trong Fidelity mode.
- Căn ảnh máy theo reference ở viewport 1226x708: không nền xám, không khung chữ
  nhật, không mặt phẳng thừa, không lệch crop; shadow phải nằm đúng vùng ảnh.
- Nếu chỉnh React/CSS, chỉ chạm các file component/style của hero và ghi rõ file
  đã đổi; không đổi source asset của reference.

## Bằng chứng bắt buộc

- Screenshot mới của Fidelity mode đúng 1226x708:
  `reports/hero-3d-task026-fidelity-mode-1226x708.png`.
- Nếu có screenshot 3D mode, lưu thêm
  `reports/hero-3d-task026-exploration-mode-1226x708.png` để chứng minh toggle
  không làm hỏng hero mặc định.
- Report phải đối chiếu pixel/crop với reference và nói rõ hai mode; không dùng
  RGB trung bình hoặc build pass để tuyên bố PASS.
- Đóng task ở trạng thái terminal `completed` với verdict chính xác; không để
  `in_progress` sau handoff.

## Acceptance gate

Codex chỉ PASS khi Fidelity mode giống reference sạch, không có artifact thừa,
và 3D mode vẫn mở được riêng. Nếu còn lỗi compositing hoặc ảnh không khớp,
ghi `REVISION_REQUIRED`.
