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

## Đánh thức session Antigravity

Sau khi tạo task mới trong `bridge/inbox/antigravity/`, Codex phải dispatch task tới session Antigravity bằng helper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\dispatch-antigravity-task.ps1 -TaskPath .\bridge\inbox\antigravity\TASK-XXX.md
```

Helper chỉ gửi một wake/handoff message trỏ tới task file bằng Reason Network; nội dung task và quyền chỉnh sửa vẫn lấy từ file trong `bridge/`. Nếu session đang idle, message được xếp hàng và sẽ được nhận ở tool/turn boundary kế tiếp. Không tự tạo phản hồi thay Antigravity.

Sau khi dispatch, helper khởi chạy watcher một lần cho đúng task đó. Khi task chuyển sang `completed`, `blocked` hoặc `cancelled` và đồng thời tồn tại cả report lẫn outbox response, watcher queue một prompt vào Codex thread đã đăng ký trong `bridge/coordinator/codex-thread.json` bằng `codex queue --resume` qua app-server localhost. Nếu queue trực tiếp đã nhận message thì không coi việc Reason Network không còn session là lỗi; Reason Network `--notify` chỉ là fallback best-effort. Codex phải đọc artifact và audit, không coi message là bằng chứng hoàn thành.

### Quy tắc dừng revision visual

- Mỗi revision visual bắt buộc có screenshot mới và đối chiếu với reference cùng kích thước/góc nhìn.
- Nếu **3 revision liên tiếp** không tạo ra cải thiện rõ ràng ở silhouette hoặc hình học chính, không tiếp tục vá shader, camera hay thêm box vào cùng asset.
- Khi chạm ngưỡng 3 lần, đánh dấu `REVISION_REQUIRED`/`BLOCKED` và chuyển hướng sang pipeline khác: dựng lại mesh bằng Blender/equivalent, dùng asset 3D khác, hoặc yêu cầu thêm reference đa góc.
- Build pass, model load được hoặc xoay được không được tính là cải thiện visual.

### Quy tắc persistent: Codex giữ vòng lặp đến khi đạt reference

- Đây là quy tắc điều phối của **Codex**, không chỉ là hướng dẫn cho Antigravity. Antigravity chỉ thực thi visual task và bàn giao artifact; Codex là người quyết định đạt hay chưa đạt.
- Sau mỗi handoff, Codex phải đọc task report, outbox response, artifact và screenshot mới; tự đối chiếu với reference cùng kích thước/góc nhìn. Không tin verdict `completed`/`PASS` nếu chưa có bằng chứng visual.
- Khi Antigravity đã ghi đủ report + outbox cho một handoff, agent phải đóng task handoff ở trạng thái terminal (`completed` với `verdict: REVISION_REQUIRED`/`BLOCKED`, hoặc `completed` với `PASS`), đồng thời ghi `completed_at`. Không giữ task ở `in_progress` trong lúc chờ Codex audit; watcher chỉ đánh thức Codex từ trạng thái terminal.
- Nếu hình chưa đạt reference, Codex phải tạo/giao revision tiếp theo trong cùng vòng lặp; không kết thúc chỉ vì build pass, GLB load được hoặc Antigravity đã báo xong.
- Ngưỡng 3 revision chỉ khóa **hướng/pipeline hiện tại**. Sau đó Codex phải pivot sang asset, phương pháp dựng, pipeline hoặc bộ reference khác rồi tiếp tục vòng lặp; không được dừng mục tiêu toàn dự án.
- Chỉ được kết thúc khi Codex audit xác nhận hình học, silhouette, tỷ lệ, vật liệu, camera và các chi tiết chính đã đạt tiêu chí reference; nếu chưa đạt thì trạng thái vẫn là `REVISION_REQUIRED`/`PIVOT_REQUIRED` và phải có task kế tiếp.
- Quy tắc này là persistent cho các lượt Codex sau, kể cả khi cách nhau nhiều giờ hoặc conversation mới; luôn đọc lại `AGENTS.md` và policy tại `bridge/coordinator/visual-acceptance-policy.md` trước khi quyết định dừng.

### GLB repair harness

- Mọi lần Codex sửa GLB sau handoff hình học phải chạy `tools/glb-repair-harness.ps1 -Action repair`.
- Harness bắt buộc backup GLB cũ, regenerate, validate glTF 2.0 + node bắt buộc, kiểm tra hash source/public và chạy production build website.
- Sau đó phải ghi screenshot audit bằng `-Action record-audit`; không được ghi PASS chỉ vì build thành công.
- Harness tự khóa repair tiếp theo khi đã có 3 `REVISION_REQUIRED` liên tiếp và yêu cầu pivot sang asset/method khác.

### Quy tắc chống spam conversation

- Không dùng scheduled automation chạy định kỳ để quét inbox. Antigravity tạo conversation mới cho mỗi lượt schedule, kể cả khi không có task.
- Scheduler phải để `paused`; khi Codex tạo task mới, Codex gọi `dispatch-antigravity-task.ps1` tới session ổn định `pc/3dprinter-antigravity`.
- Vòng lặp review/revision cũng dispatch qua cùng session ổn định. Khóa `bridge/coordinator/antigravity-worker.lock` và guard `status: in_progress` là lớp chống chạy chồng.
- Conversation sidebar chỉ là log; trạng thái chuẩn phải đọc từ task file, report và response trong workspace.
- Antigravity idle wake cần Reason Network sidecar ở trạng thái `Up`. Trên máy Windows này, sidecar cần executable thật `agentapi` trên `PATH`; shim tại `%USERPROFILE%\\.local\\bin\\agentapi.exe` gọi native `language_server.exe agentapi`.

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
