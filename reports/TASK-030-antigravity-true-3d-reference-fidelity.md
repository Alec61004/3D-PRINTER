# Báo cáo Hiệu chỉnh Trung thực Reference trên Mesh 3D Thực — TASK-030

- **Task ID**: TASK-030-TRUE-3D-REFERENCE-FIDELITY
- **Owner**: antigravity
- **Deliverable Candidate V2 GLB**: [assets/models/raw/deltrol_p2s_true3d_candidate_v2.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_true3d_candidate_v2.glb) (`753.620` bytes)
- **Script kiến tạo V2**: [scripts/build_p2s_true3d_candidate_v2.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_true3d_candidate_v2.py)
- **Reference chuẩn mục tiêu**: [assets/source/printer-hero-reference-2026-11-23.png](file:///c:/Users/PC/Downloads/3DPrinter/assets/source/printer-hero-reference-2026-11-23.png)
- **Bộ ảnh đối chiếu 1226 × 708 px (4 góc xoay)**:
  - Front Reference 3/4 (~30°): [reports/task030-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task030-front.png)
  - Rotated ~20° Left: [reports/task030-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task030-left20.png)
  - Rotated ~20° Right: [reports/task030-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task030-right20.png)
  - Elevated Angle (+18°): [reports/task030-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task030-elevated.png)
  - Tổng hợp 4 góc nhìn: [reports/task030-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task030-4view-sheet.png)
- **Khẳng định Image Plane / 2.5D**: **KHÔNG SỬ DỤNG BẤT KỲ IMAGE PLANE HAY BILLBOARD 2.5D NÀO.** Toàn bộ vật thể là **100% True Connected 3D Geometry** gồm `108` meshes kết nối chặt chẽ trong cùng không gian vật lý 3D; chỉ sử dụng texture bề mặt vật liệu (brushed titanium, speckled PEI, dark standby screen UI) phủ đúng UV lên khối 3D.
- **Kết luận thẩm định bàn giao (Verdict)**: `REVISION_REQUIRED` (Chuyển giao candidate V2 và hồ sơ 4 góc nhìn cho Codex tích hợp vào website và thực hiện visual audit độc lập; không tự cấp PASS).
- **Timestamp**: 2026-11-25T12:24:00+07:00

---

## 1. Các Cải tiến Reference-Fidelity Cốt lõi từ TASK-029 lên V2

1. **Tỷ lệ khung hình Front 3/4 chuẩn khớp Reference (`W/H ~ 1.05`)**:
   - Đo từ `printer-hero-reference-2026-11-23.png`, tỷ lệ thân máy góc 3/4 đạt $W/H = 1.049$ (trước đây TASK-029 bị cao gầy ở $0.963$).
   - Hiệu chỉnh kích thước nguyên bản $W = 0.402\text{ m}, D = 0.402\text{ m}, Z \in [-0.198, +0.182]$ (tính cả hệ số scale `Z = 1.12` của `PrinterModel.jsx`), tái tạo chuẩn xác dáng vuông vức bề thế của Bambu Lab P2S.
2. **Xóa bỏ hoàn toàn đường rãnh ngang V-groove trên thân Unibody**:
   - Thay cấu trúc chẻ tầng giữa đế/trụ/nóc bằng vỏ ngoại thất phẳng đứng liên mạch (`Z_leg_bot` tới `Z_door_top`), nối tiếp hoàn toàn với vành nóc có vát mép trên tinh tế `2.5 mm`.
   - Áp dụng hình học bất đối xứng đúng chuẩn máy thực: cột mép trái sắc nét (`R_left = 14 mm`) mang 2 bản lề kim loại champagne, cột mũi phải bo tròn đầy đặn (`R_right = 26 mm`).
3. **Chân váy vát cung (Side Skirt Arch) & Chân đế cao su liền khối**:
   - Thay kiểu đế phẳng đặt lên 4 cục đệm thô bằng phần váy kim loại đúc liền khối vát cong ở hai hông (tạo 4 chân góc hữu cơ giống hệt góc phải dưới của reference), gắn cùng miếng đệm cao su mỏng phía dưới và dầm trước thẳng vững chắc.
4. **Vật liệu Champagne Titanium Phay xước + Màn hình Console viền kim loại**:
   - Hiệu chỉnh sắc độ texture titanium phay xước ngang (`RGB [156, 148, 138]`, `metallic: 0.36`, `roughness: 0.25`) và sửa toàn bộ UV đa giác để thớ kim loại chạy ngang đồng nhất, loại bỏ cảm giác nhựa beige phẳng.
   - Dựng màn hình console nghiêng $-30^\circ$ tại chính giữa dầm đáy với đường viền mạ kim loại champagne mảnh bao quanh mặt kính đen bóng và rãnh gờ tối phía dưới, khớp sát tạo hình trên ảnh reference.
5. **Tầm nhìn Khoang CoreXY & Chi tiết In 3D**:
   - Hạ cao độ cụm ray X (`gantry_z = 0.064`) và đầu đùn `printHead` xuống trọn vẹn bên dưới thanh viền cửa trên để thấy rõ cả **3 thanh ray thép ngang**, khối đầu đùn phủ mặt champagne, ống nhựa PTFE cong trắng, xích dẫn cáp trên cao, bàn in PEI vàng đồng có gờ trước và giá đỡ khí động học `printedObject` kèm **13 cánh gân support đứng tinh xảo** bên dưới.

---

## 2. Xác thực Cấu trúc GLB 2.0 & Kiểm kê Contract Nodes

| Chỉ số Kiểm định (`deltrol_p2s_true3d_candidate_v2.glb`) | Giá trị Thực tế | Trạng thái |
| :--- | :--- | :---: |
| **Định dạng & Phiên bản** | Binary glTF 2.0 (`0x46546C67`, v2) | **HỢP LỆ** |
| **Dung lượng tệp** | `753.620` bytes | **TỐI ƯU** |
| **Tổng Nodes / Meshes** | `114` nodes / `108` meshes | **TRUE 3D** |
| **Materials / Embedded Textures** | `16` PBR materials / `3` PNG textures | **ĐỒNG BỘ** |
| **Required Contract Nodes (5/5)** | `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` (+ `top_rim_outer`, `door_left_stile`, `gantryX`, `printedObject`) | **ĐẠT 5/5** |
| **Website Source Integrity (`website/src/**`)** | `0` tệp bị chỉnh sửa | **TUÂN THỦ** |

---

## 3. Đánh giá Gắn kết 4 Góc nhìn & Sai khác Còn lại

- **Tính toàn vẹn kết nối ở mọi góc (`front`, `left20`, `right20`, `elevated`)**: Cửa kính trước, 2 bản lề trái, tay nắm phải, kính hông, nắp kính nóc, chân đế và màn hình console đều khóa chặt vào khung unibody không có hiện tượng bung tách, hở sáng khe cửa hay mặt phẳng chữ nhật thừa.
- **Sai khác trung thực cần Codex ghi nhận khi tích hợp**:
  1. Ở mép đứng bên phải của khung kính hông phải (`task030-front.png`), vẫn còn một đường chỉ mảnh phản xạ sáng `~1–2 px` giữa gioăng cửa sổ và mép trụ sau.
  2. Do `Scene.jsx` hiện dùng hệ thống đèn hướng (Directional/Spot/Point Light) mà chưa có `<Environment>` IBL HDR map, độ phản xạ bóng kim loại trên trụ cong vẫn dịu hơn so với ánh phản chiếu studio ray-traced của ảnh gốc `printer-hero-reference-2026-11-23.png`. Codex có thể bổ sung Environment/PMREM nhẹ ở tầng `Scene.jsx` nếu muốn tăng độ bóng kim loại khi tích hợp V2.
