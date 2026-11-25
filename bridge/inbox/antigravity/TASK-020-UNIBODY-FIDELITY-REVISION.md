---
task_id: TASK-020-UNIBODY-FIDELITY-REVISION
owner: antigravity
status: completed
created_at: 2026-11-24T05:43:00+07:00
request: Nâng fidelity asset unibody sau Codex audit; không được ghi PASS nếu còn low-poly hoặc lệch ảnh chuẩn.
result_path: reports/TASK-020-antigravity-unibody-fidelity.md
response_path: bridge/outbox/TASK-020-UNIBODY-FIDELITY-REVISION-antigravity-response.md
---

# TASK-020 — Unibody fidelity revision

Reference: `assets/source/printer-hero-reference-2026-11-23.png`.

Codex đã audit screenshot TASK-019 và giữ `REVISION_REQUIRED`. Asset mới tốt hơn
GLB cũ nhưng vẫn là low-poly và chưa giống ảnh chuẩn đủ gần.

## Lỗi phải sửa

1. Vỏ phải là bạc/xám satin có highlight mềm, không phải các mặt phẳng xám đơn sắc.
2. Kính trước và kính hông phải là smoked glass tối, nhìn thấy khoang nhưng không bị
   trắng trong như cửa rỗng.
3. Khung cửa trước phải dày, bo tròn, với tay nắm dọc ở cạnh phải đúng như reference.
4. Bổ sung/hoàn thiện gantry, toolhead/nozzle, bàn PEI vàng và vật thể in; các phần
   này phải có tỷ lệ và vị trí giống reference, không được là vài khối sơ sài.
5. Console dưới cửa phải nhỏ, nằm chìm và nghiêng đúng, không nhô thành một màn hình
   đen lớn lệch hình.
6. Camera/front-right 3/4 phải cho ra silhouette giống reference: máy chiếm cùng vùng
   phải của hero, không để mặt bên trống áp đảo.

## Quy định đầu ra

- Sửa asset/script trong phạm vi Antigravity; không sửa React/Three.js.
- Giữ node contract: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
- Tạo screenshot 1226 × 708 mới và report verdict `PASS`, `REVISION_REQUIRED` hoặc `BLOCKED`.
- `PASS` chỉ hợp lệ nếu đối chiếu trực tiếp với reference và không còn lỗi hình học/vật liệu lớn.
- Nếu lần này vẫn không tạo cải thiện rõ ràng, Codex sẽ kích hoạt pivot tiếp theo theo quy tắc 3 lần.
