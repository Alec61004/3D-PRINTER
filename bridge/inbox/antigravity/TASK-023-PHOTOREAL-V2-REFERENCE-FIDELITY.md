---
task_id: TASK-023-PHOTOREAL-V2-REFERENCE-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T10:30:00+07:00
request: >-
  Tiếp tục vòng visual revision cho asset photoreal_v1. Không dừng vì TASK-022 đã
  completed/blocked. Mục tiêu là render 3D giống reference
  assets/source/printer-hero-reference-2026-11-23.png ở cùng viewport 1226x708,
  góc front-right 3/4. Sửa trực tiếp asset/pipeline visual hiện tại và bàn giao
  GLB thật dùng được cho Three.js nếu có thể; không chỉ bàn giao JPG.
result_path: reports/TASK-023-antigravity-photoreal-v2-reference-fidelity.md
---

# TASK-023 — Photoreal v2 reference fidelity

## Audit findings to fix

- Bản `assets/models/raw/deltrol_p2s_photoreal_v1.glb` đã có node contract nhưng
  render hiện tại vẫn lệch reference: thân quá beige/tan, khung/cửa chưa đọc như
  unibody titan satin đóng kín, kính và nội thất bị quá tối/không đúng tỷ lệ,
  console/handle/gantry chưa khớp.
- Không dùng lại hack layout cũ để ẩn wall/glass hoặc ép screen/bed sai tọa độ.
- Kiểm tra đúng asset đang được website load, không chỉ kiểm tra source file.

## Acceptance criteria

- Có GLB thật v2 hoặc artifact visual/mesh rõ ràng trong workspace; nếu chưa thể
  tạo GLB thì ghi `BLOCKED` với blocker chính xác, không giả lập PASS.
- Giữ node contract: `enclosure`, `door`, `front_glass_door`, `printHead`,
  `printBed`.
- Có screenshot mới 1226x708 của chính website/preview và đối chiếu cùng reference.
- Report phải nêu cụ thể trước/sau ở silhouette, tỷ lệ, vật liệu, kính, cửa,
  gantry, toolhead, bed và console.
- Không tạo conversation mới; task này tiếp tục trên session Antigravity ổn định.
- Nếu revision này vẫn chưa đạt, ghi `REVISION_REQUIRED` và để Codex dispatch
  revision tiếp theo; không tự kết thúc bằng `PASS` chỉ vì build/load thành công.
