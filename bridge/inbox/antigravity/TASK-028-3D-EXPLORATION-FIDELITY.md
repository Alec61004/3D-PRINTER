---
task_id: TASK-028-3D-EXPLORATION-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T21:38:00+07:00
completed_at: 2026-11-24T21:47:00+07:00
request: >-
  Nâng riêng 3D Exploration mode sau khi Fidelity mode đã được Codex audit PASS.
  Không được làm thay đổi hoặc làm hỏng Reference Fidelity mode đã đạt framing.
result_path: reports/TASK-028-antigravity-3d-exploration-fidelity.md
---

# TASK-028 — 3D exploration fidelity

## Trạng thái hiện tại

- Reference Fidelity mode của TASK-027 đã PASS ở vùng máy: pixel diff 0 trong
  bbox reference.
- 3D Exploration mode vẫn render GLB beige/low-poly, không đạt hình photoreal.

## Yêu cầu

- Chỉ sửa implementation/asset khi URL `?mode=3d` hoặc khi người dùng bấm
  `Khám phá 3D`; không thay đổi default Fidelity mode.
- Tìm một hướng 3D trung thực hơn: mesh/asset photoreal thật nếu có thể. Nếu
  chỉ có một góc reference, có thể dùng single-view depth/2.5D trong WebGL với
  orbit giới hạn rõ ràng, nhưng phải ghi trung thực là 2.5D; không tuyên bố
  full 360° nếu mặt sau không có dữ liệu.
- Không dùng lại billboard TASK-025 gây mặt phẳng trắng, không quay lại GLB
  procedural beige v2/pivot như kết quả cuối.
- Nút quay về `Ảnh Reference` phải hoạt động và Fidelity mode phải giữ nguyên
  screenshot PASS.

## Bằng chứng bắt buộc

- Screenshot 3D mode đúng 1226x708:
  `reports/hero-3d-task028-exploration-1226x708.png`.
- Screenshot Fidelity regression check:
  `reports/hero-3d-task028-fidelity-regression-1226x708.png`.
- Report phải nêu rõ loại 3D (full mesh hay 2.5D), giới hạn góc nhìn, và các
  sai khác còn lại. Build pass không đủ để PASS.
- Đóng task ở trạng thái terminal `completed` với verdict chính xác; không để
  `in_progress`.

## Acceptance gate

Codex chỉ PASS phần 3D nếu screenshot mặc định của 3D mode không còn low-poly/
beige và Fidelity regression vẫn khớp reference. Nếu chưa đạt, ghi
`REVISION_REQUIRED` và đề xuất hướng tiếp theo.
