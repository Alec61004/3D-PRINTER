---
task_id: TASK-019-UNIBODY-ASSET-REVISION
owner: antigravity
status: completed
created_at: 2026-11-24T05:13:00+07:00
request: Revision asset unibody mới theo audit tích hợp, ưu tiên giống reference ở góc front-right 3/4 và chi tiết khoang.
result_path: reports/TASK-019-antigravity-unibody-revision.md
response_path: bridge/outbox/TASK-019-UNIBODY-ASSET-REVISION-antigravity-response.md
---

# TASK-019 — Revision asset unibody sau audit tích hợp

## Reference và evidence

- Reference chuẩn: `assets/source/printer-hero-reference-2026-11-23.png`
- Screenshot audit hiện tại: `reports/hero-3d-pivot-1226x708.png`
- Asset cần revision: `assets/models/raw/deltrol_p2s_unibody_pivoted.glb`
- Pipeline tạo asset: `scripts/generate_pivoted_unibody_glb.py`

Audit đã xác nhận asset mới tốt hơn GLB cũ ở silhouette và màu trung tính, nhưng
chưa đạt fidelity ảnh chuẩn. Đây là revision đầu tiên của pipeline mới, không quay
lại vá `reports/build_detailed_industrial_glb.py`.

## Bắt buộc sửa

1. Khóa đúng góc front-right 3/4 như reference: nhìn rõ mặt trước kính và cạnh phải,
   không để mặt bên trống chiếm ưu thế.
2. Cửa kính trước phải có khung và tay nắm dọc ở cạnh phải; không dùng chi tiết tay
   nắm nằm ngang hoặc để cửa thành một mặt phẳng trống.
3. Bổ sung hình học lớn bên trong khoang: hai thanh gantry ngang, cụm đầu in/nozzle,
   bàn in PEI và vật thể đang in. Các chi tiết phải là mesh thật trong GLB, không chỉ
   đặt bằng overlay React.
4. Giữ vỏ bạc/xám trung tính, bo góc liên tục, side glass lớn và mặt console dưới
   trước. Không biến máy thành hộp xám rỗng.
5. Giữ các node contract: `enclosure`, `door`, `printHead`, `printBed`,
   `front_glass_door`.
6. Không sửa React/Three.js của Codex. Cập nhật asset/script trong phạm vi
   `assets/models/raw/`, `assets/generated/antigravity/` hoặc `scripts/`.
7. Tạo screenshot 1226 × 708 mới và report verdict `PASS`, `REVISION_REQUIRED`
   hoặc `BLOCKED`; không ghi PASS nếu chỉ build/load thành công.
