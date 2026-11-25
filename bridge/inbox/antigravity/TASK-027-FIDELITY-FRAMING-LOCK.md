---
task_id: TASK-027-FIDELITY-FRAMING-LOCK
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T21:14:00+07:00
completed_at: 2026-11-24T21:31:00+07:00
request: >-
  Tiếp tục từ TASK-026. Fidelity mode đã sạch nhưng screenshot chưa cùng framing
  với reference; 3D mode vẫn là exploration riêng. Căn lại hero để default output
  khớp reference trước khi xét PASS.
result_path: reports/TASK-027-antigravity-fidelity-framing-lock.md
---

# TASK-027 — Fidelity framing lock

## Audit findings phải sửa

- Reference 1226x708 có máy nằm xấp xỉ bbox `x=618..1074, y=152..575`.
- Fidelity screenshot TASK-026 hiện đặt máy thấp/phải hơn và trang đang hiển thị
  header/scroll state khác reference. Không được tuyên bố đạt chỉ vì ảnh máy đẹp.
- 3D exploration vẫn giữ riêng, không được chồng lên Fidelity mode.

## Yêu cầu

- Giữ `Reference Fidelity mode` làm mặc định và dùng asset photoreal trong suốt
  hiện có, nhưng khóa lại stage/crop/position/scale để máy khớp bbox reference ở
  viewport 1226x708; nền trắng, không scrollbar/artifact trong vùng hero.
- Đảm bảo capture dùng cùng trạng thái trang với reference (không tự capture ở
  scroll top khác framing mục tiêu).
- Giữ nút chuyển sang `3D Exploration mode`; 3D mode có thể còn sai photoreal,
  nhưng không được ảnh hưởng default Fidelity mode.
- Không đưa lại billboard GLB TASK-025 vào composition.

## Bằng chứng bắt buộc

- Screenshot mới: `reports/hero-3d-task027-fidelity-framing-1226x708.png`.
- Report phải ghi bbox đo được của máy trong reference và render, chênh lệch px,
  cùng ảnh đối chiếu trực tiếp. Không dùng RGB mean thay cho framing audit.
- Đóng task terminal `completed` với verdict chính xác; không để `in_progress`.

## Acceptance gate

Codex chỉ PASS khi default Fidelity screenshot khớp rõ vị trí/kích thước/crop
reference và không có artifact. Nếu chưa khớp, ghi `REVISION_REQUIRED` để tiếp tục.
