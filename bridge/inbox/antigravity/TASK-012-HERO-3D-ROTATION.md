---
task_id: TASK-012-HERO-3D-ROTATION
owner: antigravity
status: completed
created_at: 2026-11-23T19:25:00+07:00
request: Tích hợp chế độ 3D tương tác cho Hero để người dùng xoay máy in theo nhiều góc; Codex sẽ audit sau.
result_path: reports/TASK-012-antigravity-3d-rotation.md
response_path: bridge/outbox/TASK-012-HERO-3D-ROTATION-antigravity-response.md
---

# TASK-012 — Hero 3D Rotation Implementation

## Context

Đọc trước:

1. `AGENTS.md`
2. `CODEX.md`
3. `ANTIGRAVITY.md`
4. `bridge/inbox/antigravity/TASK-011-HERO-VISUAL-QA.md`
5. `reports/TASK-011-antigravity-visual-qa.md`
6. `reports/TASK-011-codex-review.md`

## Mục tiêu

Đưa Hero từ ảnh photoreal tĩnh thành trải nghiệm có thể xem máy in 3D theo nhiều góc. Giữ nguyên chất lượng direct photoreal đã được duyệt làm baseline; không biến Hero thành một card demo nặng hoặc làm mất bố cục editorial hiện tại.

## Phạm vi owner Antigravity

Được chỉnh phần integration visual/UI trong các file:

- `website/src/App.jsx`
- `website/src/components/StaticPhotorealPrinter.jsx`
- `website/src/components/Scene.jsx`
- `website/src/components/PrinterControlsUI.jsx`
- `website/src/styles.css`

Có thể dùng lại model/scene hiện có trong `website/` và asset `website/public/models/deltrol_p2s_optimized.glb`; không tạo asset giả để thay thế model thật.

Không chỉnh:

- `assets/` do Antigravity khác sở hữu.
- pipeline Blender/GLB gốc hoặc backend.
- bridge protocol, task file của Codex, hoặc sign-off kỹ thuật của Codex.

## Acceptance criteria

1. Hero có chế độ 3D thật, cho phép xoay bằng drag chuột và touch swipe; không chỉ giả lập bằng CSS hoặc nhiều ảnh phẳng.
2. Có trạng thái loading/error rõ ràng và fallback về ảnh photoreal đã duyệt nếu model không tải được.
3. Có reset góc nhìn; auto-orbit chỉ là tùy chọn nhẹ và không giành quyền điều khiển khi người dùng đang kéo.
4. Giữ đủ silhouette, chân máy, contact shadow và bố cục direct trên nền trắng; không quay lại card wrapper/overlay thừa.
5. Desktop và mobile không crop, không tràn ngang, controls không che nội dung chính.
6. Không có lỗi console/asset 404 hiển nhiên; chạy build phù hợp.
7. Ghi screenshot/evidence vào `reports/`, tạo report tại `result_path`, cập nhật task thành `completed` hoặc `blocked`, và ghi response tại `response_path`.

Antigravity thực hiện implementation visual/UI. Codex sẽ audit code, interaction, asset loading, responsive và kết quả cuối; không tự ghi response thay Antigravity.

## Vòng lặp hoàn thiện bắt buộc

Đây là task dạng iterative handoff, không kết thúc chỉ vì một lần build thành công:

1. Antigravity implement và ghi report `READY_FOR_CODEX_AUDIT` hoặc `BLOCKED`.
2. Codex audit trực tiếp code, browser interaction, desktop/mobile và asset/console evidence.
3. Nếu có bất kỳ lỗi hoặc lệch visual nào, Codex ghi rõ `REVISION_REQUIRED`, tạo task revision mới với feedback cụ thể, rồi dispatch bằng `tools/dispatch-antigravity-task.ps1`.
4. Antigravity chỉ sửa trong owner scope của revision và gửi lại evidence.
5. Lặp lại từ bước 2 cho đến khi Codex ghi `PASS`; chỉ khi đó mới đóng vòng TASK-012.

Không dùng `bridge/coordinator/state.json` cũ làm sign-off cho vòng lặp mới. Mỗi lần lặp phải có report/evidence riêng và không được giả lập phản hồi của agent còn lại.
