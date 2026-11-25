# Báo cáo Chuyển hướng Pipeline Asset 3D Hero — TASK-018-3D-ASSET-PIPELINE-PIVOT

- **Task ID**: TASK-018-3D-ASSET-PIPELINE-PIVOT
- **Owner**: antigravity
- **Reference chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png` (Kích thước: 1226 × 708 px)
- **Kết luận thẩm định**: `REVISION_REQUIRED`
- **Timestamp**: 2026-11-23T22:06:00+07:00

---

## 1. Mục tiêu & Hướng tiếp cận mới (Pipeline Pivot)

Thay vì tiếp tục vá các khối hộp `add_box` và shader nhỏ trong file GLB cũ (`deltrol_p2s_optimized.glb`), Antigravity đã chuyển hướng sang pipeline tạo hình học mới bằng `trimesh` + `numpy`, xây dựng mesh unibody có các đường cong bo góc liên tục (fillets) và tỷ lệ chuẩn công nghiệp:

- **Script tạo asset mới**: `scripts/generate_pivoted_unibody_glb.py`
- **Asset GLB mới đã tạo**:
  - `assets/models/raw/deltrol_p2s_unibody_pivoted.glb` (33.784 bytes)
  - `assets/generated/antigravity/deltrol_p2s_reference_unibody.glb` (33.784 bytes)
- **Bảo toàn giao ước kỹ thuật (Node Hierarchy Contract)**:
  Asset mới đáp ứng 100% danh sách node bắt buộc của `tools/glb-repair-harness.ps1`:
  `enclosure`, `door`, `printHead`, `printBed`, `front_glass_door`.

---

## 2. Đặc điểm hình học của Asset 3D Mới

| Bộ phận | Giải pháp hình học mới (TASK-018) | Đối chiếu với Ảnh Reference |
| :--- | :--- | :--- |
| **Tỷ lệ tổng thể (Silhouette)** | Tỷ lệ 0.38m W × 0.38m D × 0.46m H (Chiều cao gấp ~1.21 lần chiều rộng). | Khắc phục hoàn toàn tình trạng máy thấp bẹt / quá vuông, đạt dáng đứng thon cao công nghiệp. |
| **Bo góc unibody (Fillets)** | 4 trụ góc đứng sử dụng đường cong trụ tròn bán kính r = 24mm (24 phân đoạn lưới mượt mà), gắn liền với viền nóc và khay đáy bo cong. | Không còn là các thanh hộp vuông ghép rời; đạt độ liền khối của vỏ kim loại dập/đúc. |
| **Vách kính hông (Right side)** | Mặt kính hông mở rộng phủ 85% diện tích vách, loại bỏ các khối panel đặc cồng kềnh. | Cho phép quan sát thông suốt vào lòng buồng in từ góc nhìn 3/4. |
| **Cửa kính & Tay nắm** | Kính cửa trước lớn, trong suốt quang học cao (`opacity: 0.35`), tay nắm dọc màu bạc ở cạnh phải. | Giữ đúng bố cục tay nắm dọc và cửa kính lớn trong ảnh chuẩn. |
| **Mặt nạ đáy & Màn hình** | Mặt nạ đáy trước đồng nhất (`front_bot_fascia`), console màn hình đặt cân đối giữa và nghiêng 25° công thái học. | Khắc phục hiện tượng khuyết vách đáy lệch phải của GLB cũ. |
| **Gantry & Bàn in** | Cụm gantry thép thanh mảnh nằm sát trần khoang, bàn in PEI vàng và mô hình đặt ở cao độ trung tâm buồng in. | Bố cục buồng in thoáng đãng, không bị các cuộn nhựa to chiếm dụng. |

---

## 3. Giới hạn & Đề xuất Reference Bổ sung (Tiêu chí 4)

- **Giới hạn hiện tại**: Dự án hiện chỉ có một ảnh chụp tham chiếu đơn góc 3/4 (`printer-hero-reference-2026-11-23.png`). Từ một góc chụp phối cảnh duy nhất, các thông số kỹ thuật khuất tầm nhìn (mặt sau, chi tiết bản lề cửa, gờ nóc máy) chỉ có thể suy luận theo tiêu chuẩn thiết kế dòng Bambu Lab P1S/X1C.
- **Đề xuất**: Để hoàn thiện 100% độ chính xác cho mesh sản xuất, đề xuất bổ sung thêm:
  1. *Ảnh trực diện mặt trước (Front view)* để khớp chính xác tỷ lệ viền bezel màn hình.
  2. *Ảnh nhìn từ trên xuống (Top-down view)* để xác định chính xác cấu trúc nắp kính trên nóc.

---

## 4. Bằng chứng kiểm tra & Bàn giao Codex

- **Screenshot Desktop đối chiếu (1226 × 708 px — Khớp 1:1 kích thước ảnh reference)**:
  `reports/hero-3d-pivot-1226x708.png`
- **Bàn giao file**:
  Tuân thủ nghiêm ngặt nguyên tắc phân quyền (không sửa code React/Three.js của Codex), asset mới đã được xuất sang `assets/models/raw/deltrol_p2s_unibody_pivoted.glb`. Codex sẽ chạy `tools/glb-repair-harness.ps1 -Action repair` để tối ưu hóa, backup và tích hợp vào website.
- **Kết luận thẩm định**: `REVISION_REQUIRED` (chờ Codex chạy GLB repair harness và thực hiện audit tích hợp).
