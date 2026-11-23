# Deltrol Image-to-3D — Quy tắc phối hợp

## Mục đích

Workspace này dùng để phối hợp giữa Codex và Google Antigravity Desktop cho dự án Deltrol Image-to-3D. Mọi trao đổi nhiệm vụ phải được thực hiện bằng file trong thư mục `bridge/`.

## Phân quyền

- **Codex** phụ trách kỹ thuật: kiến trúc, React, Three.js, Blender, GLB, xử lý model và review kỹ thuật.
- **Antigravity** phụ trách ảnh AI, texture, visual direction và UI/UX.
- Mỗi file chỉ có một owner tại một thời điểm. Không được hai agent đồng thời chỉnh sửa cùng một file.
- Agent nhận task chỉ được ghi output vào đường dẫn đã nêu trong task hoặc đường dẫn con phù hợp do owner của task chỉ định.
- Không xóa hoặc ghi đè dữ liệu hiện có nếu chưa có yêu cầu rõ ràng và kiểm tra phạm vi.
- Không tự động điều khiển Antigravity qua API nội bộ, token hoặc CLI không được hỗ trợ.
- Không sử dụng dịch vụ trả phí.
- Không tự giả lập phản hồi của agent khác. Chỉ phản hồi khi agent đó đã ghi file phản hồi.

## Cấu trúc workspace

- `bridge/inbox/codex/`: task gửi cho Codex.
- `bridge/inbox/antigravity/`: task gửi cho Antigravity.
- `bridge/outbox/`: phản hồi đã hoàn thành hoặc artifact manifest được gửi lại cho agent khác.
- `bridge/logs/`: log phối hợp append-only, nếu cần.
- `assets/source/`: ảnh hoặc dữ liệu nguồn do người dùng cung cấp.
- `assets/generated/antigravity/`: ảnh/visual/texture do Antigravity tạo.
- `assets/models/raw/`: model 3D đầu vào chưa tối ưu.
- `assets/models/optimized/`: model 3D đã tối ưu.
- `website/`: mã nguồn website.
- `reports/`: báo cáo, review và kết quả kiểm thử.

## Giao thức task bằng file

Task dùng JSON (`.json`) hoặc Markdown có front matter (`.md`). Tối thiểu phải có các trường:

```yaml
task_id: TASK-XXX
owner: codex | antigravity
status: pending | in_progress | blocked | completed | cancelled
created_at: ISO-8601 timestamp
request: Mô tả yêu cầu
result_path: Đường dẫn tương đối tới kết quả dự kiến
```

Quy trình:

1. Agent gửi task ghi file vào đúng thư mục `bridge/inbox/<owner>/`.
2. Agent nhận task đổi `status` sang `in_progress` trong chính task file khi bắt đầu xử lý.
3. Agent nhận task tạo kết quả tại `result_path`, sau đó cập nhật `status: completed` và ghi tóm tắt kết quả.
4. Nếu không thể thực hiện, dùng `status: blocked`, nêu lý do và không tự đoán kết quả.
5. Phản hồi gửi cho agent tạo task được ghi vào `bridge/outbox/` bằng file riêng, có cùng `task_id`.
6. Trước khi chỉnh sửa, agent phải kiểm tra task chưa bị owner khác khóa/đang xử lý. Không chỉnh sửa task hoặc artifact đang được agent khác sử dụng.

## Quy ước đặt tên

- Task: `TASK-XXX.md` hoặc `TASK-XXX.json`.
- Phản hồi: `TASK-XXX-<owner>-response.md`.
- Artifact nên dùng tên ổn định, mô tả được nội dung và đặt đúng thư mục theo phân quyền.

## Trạng thái khởi tạo

`TASK-001` là task kiểm thử giao tiếp đầu tiên gửi cho Antigravity. Codex không được ghi phản hồi thay Antigravity.


## DOOP MCP — QUY TẮC PHỐI HỢP

Cả Codex Desktop và Antigravity Desktop đã được kết nối tới cùng Doop workspace qua MCP.

Doop được sử dụng cho:
- Live visual review.
- UI/UX design.
- Visual reference.
- Screenshot review.
- Frame comparison.
- Design feedback.
- Prototype presentation.

Doop KHÔNG phải nơi lưu source code duy nhất.

Source of truth vẫn là:

C:\Users\PC\Downloads\3DPrinter

### Phân quyền

Antigravity:
- Chủ yếu tạo visual, ảnh AI, texture, UI concept.
- Có thể tạo frame mới trên Doop.
- Không tự sửa frame kỹ thuật do Codex đang sở hữu.

Codex:
- Review visual.
- Kiểm tra layout, tỷ lệ, tính hợp lý kỹ thuật.
- Tạo hoặc chỉnh frame demo kỹ thuật khi cần.
- Không tự thay visual đã được Antigravity tạo nếu chưa review hoặc có lý do kỹ thuật.

### Frame ownership

Tên frame nên có prefix:

AG — frame do Antigravity sở hữu.
CX — frame do Codex sở hữu.
SHARED — frame đã được hai bên thống nhất.

Ví dụ:

AG · P2S Reference · Front 3/4
AG · P2S Interior Concept
CX · Three.js Viewer Prototype
CX · GLB Integration Test
SHARED · Deltrol Hero · Approved

Không chỉnh frame do agent khác đang làm nếu chưa có task hoặc review request.

### Review workflow

1. Agent tạo frame.
2. Lưu asset thật vào shared workspace.
3. Gửi task review qua bridge.
4. Reviewer mở frame bằng Doop MCP.
5. Reviewer kiểm tra screenshot và inspect data.
6. Reviewer trả:
   - APPROVED
   hoặc
   - REVISION_REQUIRED
7. Chỉ owner của frame thực hiện revision, trừ khi task cho phép agent khác sửa.

### Không được làm

- Không dùng Doop làm bridge thay cho shared folder.
- Không lưu asset quan trọng chỉ trong Doop.
- Không để hai agent sửa cùng một frame đồng thời.
- Không tự approve thiết kế của chính mình.
- Không xóa frame của agent khác nếu chưa có yêu cầu.