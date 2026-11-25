---
task_id: TASK-010-CONTEXT-LOOP
owner: antigravity
status: completed
created_at: 2026-11-23T18:30:00+07:00
request: Tiếp nhận context dự án Deltrol cho conversation mới và chuẩn bị vòng lặp làm -> kiểm -> phản hồi.
result_path: reports/TASK-010-antigravity-context-response.md
---

# Context handoff — Deltrol Image-to-3D

## Bắt buộc đọc trước khi làm

1. `AGENTS.md`
2. `CODEX.md`
3. `ANTIGRAVITY.md`
4. `bridge/coordinator/state.json`
5. `git status --short` và `git diff --stat`

## Ngữ cảnh hiện tại

- Source of truth: `C:\Users\PC\Downloads\3DPrinter`.
- Codex phụ trách kỹ thuật; Antigravity phụ trách visual, texture, UI/UX.
- Không sửa cùng file khi owner khác đang làm; không xóa/ghi đè dữ liệu ngoài task.
- Hero hiện đang được chuyển sang hướng direct photoreal object: ảnh PNG/WebP nền trong suốt, không card, không badge, không overlay.
- File liên quan hiện tại: `website/src/components/StaticPhotorealPrinter.jsx`, `website/src/styles.css`, `website/public/hero_architectural_printer.png`, `website/public/hero_architectural_printer.webp`.
- `bridge/coordinator/state.json` là state cũ; không coi `DONE/APPROVED` là sign-off mới nếu working tree còn thay đổi.

## Quy tắc vòng lặp

1. Nhận task qua bridge/Reason Network.
2. Đọc context và kiểm tra owner/status trước khi sửa.
3. Chỉ chỉnh visual trong phạm vi task được giao.
4. Ghi artifact/evidence vào `result_path`.
5. Cập nhật task `status: completed` hoặc `blocked`, nêu rõ bằng chứng.
6. Codex sẽ review kỹ thuật và visual sau khi Antigravity hoàn tất.

## Việc cần làm ngay

Chưa sửa file. Hãy xác nhận đã đọc context, báo current owner/working-tree state, và chờ task visual cụ thể tiếp theo.
