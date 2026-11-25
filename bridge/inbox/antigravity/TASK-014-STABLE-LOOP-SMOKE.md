---
task_id: TASK-014-STABLE-LOOP-SMOKE
owner: antigravity
status: completed
created_at: 2026-11-23T20:00:00+07:00
request: Kiểm thử dispatch vào session Antigravity cố định; không chỉnh source, chỉ ghi nhận đã nhận đúng task.
result_path: reports/TASK-014-antigravity-stable-loop-smoke.md
response_path: bridge/outbox/TASK-014-STABLE-LOOP-SMOKE-antigravity-response.md
---

# TASK-014 — Stable Session Loop Smoke Test

## Instructions

1. Đọc `AGENTS.md` và `ANTIGRAVITY.md`.
2. Xác nhận task có `owner: antigravity` và bắt đầu bằng cách chuyển `status: pending` thành `status: in_progress`.
3. Không chỉnh sửa bất kỳ file source, asset, website hoặc bridge protocol nào khác.
4. Tạo report tại `reports/TASK-014-antigravity-stable-loop-smoke.md` với kết luận `PASS`, ghi rõ session đã nhận task và không có source change.
5. Tạo response tại `bridge/outbox/TASK-014-STABLE-LOOP-SMOKE-antigravity-response.md`.
6. Chỉ sau khi hai artifact tồn tại, cập nhật task này thành `status: completed`.

Không tạo task mới và không giả lập phản hồi của Codex.
