---
task_id: TASK-011-HERO-VISUAL-QA
owner: antigravity
status: completed
created_at: 2026-11-23T18:40:00+07:00
request: Thực hiện visual implementation và polish có kiểm soát cho Hero direct photoreal object; Codex sẽ review sau.
result_path: reports/TASK-011-antigravity-visual-qa.md
---

# TASK-011 — Hero Visual Implementation

## Context

Đây là bước tiếp theo sau `TASK-010-CONTEXT-LOOP`. Đọc trước:

1. `AGENTS.md`
2. `CODEX.md`
3. `ANTIGRAVITY.md`
4. `bridge/coordinator/state.json`
5. `bridge/outbox/TASK-010-CONTEXT-LOOP-antigravity-response.md`

## Phạm vi owner

Antigravity được phép kiểm tra và chỉ chỉnh visual trong các file:

- `website/src/components/StaticPhotorealPrinter.jsx`
- `website/src/styles.css`
- `website/public/hero_architectural_printer.png`
- `website/public/hero_architectural_printer.webp`

Không chỉnh GLB, Three.js logic, backend, bridge protocol hoặc file Codex đang sở hữu.

## Việc cần làm

1. Mở local app và dùng các viewport 1440×900, 1280×720 và 390×844 để làm baseline.
2. Thực hiện visual polish theo hướng đã chốt: printer là direct photoreal object, nền trong suốt, không card wrapper, không badge/overlay thừa.
3. Bảo đảm đủ thân máy, chân máy, contact shadow, tỷ lệ trong hero, không crop và không asset 404.
4. Chỉ chỉnh trong phạm vi owner ở trên; không chạm GLB/Three.js/backend/bridge.
5. Chạy kiểm tra phù hợp, ghi screenshot/evidence vào `result_path` hoặc đường dẫn con của `reports/`.
6. Cập nhật task thành `completed` hoặc `blocked`, nêu rõ file đã sửa và bằng chứng để Codex review.

## Acceptance criteria

- Hero không quay lại card/container hoặc overlay không được yêu cầu.
- Máy giữ đúng silhouette, đủ các điểm tiếp xúc và không bị crop ở desktop/mobile.
- Không có lỗi console/asset load hiển nhiên trong phạm vi visual.
- Báo cáo phải phân biệt rõ: `PASS`, `REVISION_REQUIRED`, hoặc `BLOCKED`.

Antigravity chịu trách nhiệm làm visual. Codex sẽ review kỹ thuật và so sánh kết quả sau khi task hoàn tất; Antigravity không tự ghi sign-off thay Codex.
