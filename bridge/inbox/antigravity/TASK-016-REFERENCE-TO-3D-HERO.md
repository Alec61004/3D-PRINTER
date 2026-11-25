---
task_id: TASK-016-REFERENCE-TO-3D-HERO
owner: antigravity
status: completed
created_at: 2026-11-23T21:00:00+07:00
request: >-
  Dùng ảnh reference tại assets/source/printer-hero-reference-2026-11-23.png làm
  chuẩn thị giác để hoàn thiện Hero máy in 3D. Bản hiện tại đang bị lệch hình
  dáng/màu/khung máy; không chấp nhận kết quả chỉ xoay được nhưng không giống
  reference. Kiểm tra bản local hiện tại, đối chiếu trực tiếp với reference,
  rồi thực hiện phần visual/3D cần thiết trong phạm vi được cấp.
result_path: reports/TASK-016-antigravity-reference-to-3d-hero.md
---

## Phạm vi owner

- Được phép chỉnh phần visual/3D của Hero trong:
  - `website/src/components/PrinterModel.jsx`
  - `website/src/components/Scene.jsx`
  - `website/src/styles.css`
  - `assets/generated/antigravity/`
- Không chỉnh các section nội dung khác, bridge protocol, backend hoặc file
  ngoài phạm vi trên.
- Codex không chỉnh các file trên trong lúc task đang `in_progress`.

## Tiêu chí bắt buộc

1. Hình dáng phải bám reference: thân máy xám bạc, khung góc bo, cửa kính
   trước lớn, tay cầm bên phải, gantry/nozzle phía trên, bàn in và chi tiết
   bên trong nhìn thấy được.
2. Hero phải dùng asset 3D thực tế (GLB/scene), không quay lại dựng máy bằng
   vài khối hộp procedural để giả lập hình dáng.
3. Giữ được xoay 360°, preset camera, reset và fallback ảnh 2D.
4. Chạy build và ghi rõ bằng chứng screenshot/runtime trong report.
5. Không tự ghi `PASS` nếu chưa đối chiếu trực tiếp với ảnh reference; nếu
   asset hiện tại không đủ fidelity thì ghi `REVISION_REQUIRED` và nêu chính
   xác phần cần bổ sung.

## Quy trình bàn giao

- Chuyển task sang `in_progress` trước khi bắt đầu.
- Tạo report tại `result_path`, ghi asset/file đã chỉnh và bằng chứng.
- Chỉ khi artifact và report tồn tại mới chuyển task sang `completed`.
- Tạo phản hồi riêng tại `bridge/outbox/TASK-016-REFERENCE-TO-3D-HERO-antigravity-response.md`.
