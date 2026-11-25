---
task_id: TASK-017-REFERENCE-FIDELITY-REVISION
owner: antigravity
status: completed
created_at: 2026-11-23T21:35:00+07:00
request: >-
  Revision bắt buộc cho Hero 3D theo cùng reference
  assets/source/printer-hero-reference-2026-11-23.png. Bản TASK-016 đã được
  Codex audit và chưa đạt: screenshot thực tế vẫn vàng/gold, quá vuông và lệch
  hình học so với máy reference. Hãy tiếp tục chỉnh visual/3D, không coi report
  TASK-016 là PASS.
result_path: reports/TASK-017-antigravity-fidelity-revision.md
---

## Bằng chứng lỗi cần sửa

- `reports/hero-3d-reference-1440x900.png` hiện tại không giống ảnh chuẩn:
  vỏ máy vàng quá mạnh, khung/vách quá dày, mặt trước và console sai tỷ lệ,
  buồng in không có bố cục gantry/bàn in giống reference.
- Mục tiêu là ảnh máy màu champagne-bạc/xám bạc, góc 3/4 trước-phải, cửa kính
  lớn, tay cầm dọc bên phải, gantry/nozzle nằm phía trên và bàn in nằm giữa.

## Phạm vi owner

- Được chỉnh visual/3D Hero trong `website/src/components/PrinterModel.jsx`,
  `website/src/components/Scene.jsx`, `website/src/styles.css` và asset 3D
  trong `assets/generated/antigravity/` nếu cần.
- Không chỉnh section nội dung khác, bridge protocol hoặc backend.
- Codex không chỉnh các file này trong lúc task `in_progress`.

## Acceptance criteria

1. Render screenshot desktop mới và đặt cạnh reference để đối chiếu.
2. Màu thân máy phải là bạc/champagne trung tính, không bị cast vàng toàn thân.
3. Silhouette, khung cửa, tay cầm, gantry, nozzle, bàn in và tỷ lệ thân máy
   phải giống reference rõ ràng ở góc overview.
4. Vẫn giữ xoay 3D, preset, reset và fallback 2D.
5. Nếu asset GLB không đủ hình học, phải ghi `BLOCKED`/`REVISION_REQUIRED`
   với lý do cụ thể; không ghi `PASS` dựa trên build thành công בלבד.
6. Chỉ chuyển `completed` sau khi report và outbox response tồn tại.
