---
task_id: TASK-013-LOOP-SMOKE
owner: antigravity
status: completed
created_at: 2026-11-23T19:35:00+07:00
request: Kiểm thử một vòng bridge nhỏ, không chỉnh source; xác nhận Antigravity nhận task và ghi artifact.
result_path: reports/TASK-013-antigravity-loop-smoke.md
response_path: bridge/outbox/TASK-013-LOOP-SMOKE-antigravity-response.md
---

# TASK-013 — Bridge Loop Smoke Test

## Việc cần làm

1. Đọc `AGENTS.md` và `ANTIGRAVITY.md`.
2. Xác nhận task này đúng owner `antigravity` và đang ở `pending`.
3. Không chỉnh bất kỳ source, asset, bridge protocol hoặc file website nào.
4. Tạo report tại `reports/TASK-013-antigravity-loop-smoke.md` với kết luận `PASS` và ghi rõ không có source change.
5. Tạo response tại `bridge/outbox/TASK-013-LOOP-SMOKE-antigravity-response.md`.
6. Cập nhật task này thành `completed` sau khi hai artifact đã tồn tại.

Đây là smoke test để xác minh vòng dispatch → nhận task → ghi artifact → đóng task. Không giả lập kết quả và không tạo task tiếp theo.
