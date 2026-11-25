# Báo cáo Hiệu chỉnh Độ trung thực Photoreal trên Mesh 3D Thực — TASK-031

- **Task ID**: TASK-031-TRUE-3D-PHOTOREAL-FIDELITY
- **Owner**: antigravity
- **Deliverable Candidate V3 GLB**: [assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_true3d_candidate_v3.glb) (`898.956` bytes)
- **Script kiến tạo V3**: [scripts/build_p2s_true3d_candidate_v3.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_true3d_candidate_v3.py)
- **Reference chuẩn mục tiêu**: [assets/source/printer-hero-reference-2026-11-23.png](file:///c:/Users/PC/Downloads/3DPrinter/assets/source/printer-hero-reference-2026-11-23.png)
- **Bộ ảnh Screenshot kiểm chứng 1226 × 708 px (4 góc xoay)**:
  - Front Reference 3/4 (~30°): [reports/task031-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task031-front.png)
  - Rotated ~20° Left: [reports/task031-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task031-left20.png)
  - Rotated ~20° Right: [reports/task031-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task031-right20.png)
  - Elevated Angle (+18°): [reports/task031-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task031-elevated.png)
  - Tổng hợp 4 góc nhìn: [reports/task031-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task031-4view-sheet.png)
- **Khẳng định Image Plane / Billboard**: **HOÀN TOÀN KHÔNG SỬ DỤNG IMAGE PLANE, BILLBOARD HAY 2.5D FACADE.** Mô hình được cấu thành từ **100% True Connected 3D Geometry** (`111` meshes kết nối chặt chẽ trong cùng không gian vật lý 3D). Toàn bộ texture PNG nhúng bên trong chỉ là bản đồ bề mặt vật liệu (silky champagne metal highlight wrap, PEI speckle, standby console glass).
- **Kết luận thẩm định bàn giao (Verdict)**: `REVISION_REQUIRED` (Bàn giao candidate V3 và hồ sơ bằng chứng cho Codex tích hợp và kiểm định độc lập; tuyệt đối không tự cấp PASS).
- **Timestamp**: 2026-11-25T12:32:00+07:00

---

## 1. Các Cải tiến Photoreal True-3D Cốt lõi trong V3 (TASK-031)

1. **Dải Specular Kim loại Champagne Mượt (Loại bỏ hoàn toàn sọc nhựa beige)**:
   - Xóa bỏ hạt nhiễu ngang thô (gây cảm giác vân nhựa/gỗ ở bản V2) và thay bằng 4 dải bản đồ vật liệu kim loại lụa mượt:
     - `Champagne Pillar Highlight`: Áp dụng ánh xạ UV trụ liên tục dọc cung bo tròn $90^\circ$ của cột trước-phải (`unibody_corner_3`), tái tạo dải phản quang bạc-champagne mềm mại chạy dọc mũi trụ bo tròn như ảnh gốc.
     - `Champagne Pillar Left`: Cột mép trái mảnh sắc nét với dải sáng satin champagne chạy dọc cạnh ngoài làm nổi bật phần cửa kính.
     - `Champagne Metal Front`: Mặt trán trên và dầm đáy dưới mượt mịn với độ chuyển sáng studio nhẹ từ trên-trái sang phải.
     - `Champagne Side Shaded`: Vách hông phải tối màu gunmetal-champagne tự nhiên, tạo chiều sâu khối 3/4 rõ rệt.
2. **Triệt tiêu hoàn toàn vệt sáng viền kính hông & tai console**:
   - Đẩy viền gioăng tối `right_gasket_*` sát ra mặt ngoài vách hông để che kín gờ ngang phản sáng bên trong khung, loại bỏ 100% đường chỉ sáng dọc mép kính hông phải thấy ở TASK-030.
   - Thu gọn phần đế chìm `screen_dock_wedge` vào sâu phía sau `screen_metal_rim`, loại bỏ hoàn toàn 2 góc đen nhô ở viền trên màn hình console.
3. **Định tỷ lệ 3/4 chuẩn P2S (`W = 0.415, D = 0.356, Z ∈ [-0.202, +0.192]`)**:
   - Khớp tỷ lệ mặt trước rộng (~72%) so với chiều sâu hông phải (~28%) và chiều cao đứng ở góc nhìn 3/4.
4. **Khoang In CoreXY Ánh Hổ Phách Ấm & Chi tiết Kỹ thuật Sắc nét**:
   - Mở thoáng dải trần giữa để nguồn sáng spot trên trần khoang rọi thẳng xuống hệ 3 ray trượt thép X, cụm đầu đùn `printHead` mặt satin champagne có vòng quạt tròn và đầu phun đồng, ống PTFE trắng cong, dây xích dẫn cáp, bàn in PEI vàng-đồng và chi tiết in vòm 15 gân support đứng bên dưới.

---

## 2. Xác thực Cấu trúc GLB 2.0 & Kiểm kê Contract Nodes

| Chỉ số Kiểm định (`deltrol_p2s_true3d_candidate_v3.glb`) | Giá trị Thực tế | Trạng thái |
| :--- | :--- | :---: |
| **Định dạng & Phiên bản** | Binary glTF 2.0 (`0x46546C67`, v2) | **HỢP LỆ** |
| **Dung lượng tệp** | `898.956` bytes | **ĐẠT** |
| **Tổng Nodes / Meshes** | `117` nodes / `111` meshes | **TRUE 3D** |
| **Materials / Embedded Textures** | `22` PBR materials / `6` PNG textures | **ĐỒNG BỘ** |
| **Required Contract Nodes (5/5)** | `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` (+ `top_rim_outer`, `door_left_stile`, `gantryX`, `printedObject`) | **ĐẠT 5/5** |
| **Website Source Integrity (`website/src/**`)** | `0` tệp bị chỉnh sửa | **TUÂN THỦ** |

---

## 3. Đánh giá Gắn kết 4 Góc nhìn & Sai khác Trung thực Còn lại

- **Gắn kết vật lý ở mọi góc (`front`, `left20`, `right20`, `elevated`)**: Mọi bộ phận (khung unibody, cột góc, chân váy, chân đế cao su, bản lề trái, đố cửa, kính trước/hông/nóc, tay nắm phải, console, hệ thống CoreXY) đều giữ nguyên liên kết khép kín không đứt gãy, không tấm ảnh phẳng lồi.
- **Sai khác còn lại so với ảnh reference gốc (`printer-hero-reference-2026-11-23.png`)**:
  1. **Độ phản quang kính & ánh sáng IBL của Scene**: Do `PrinterModel.jsx` cố định độ đục `Smoked Glass` ở `opacity: 0.52` (`#12161a`, `map: null`) và `Scene.jsx` không sử dụng HDR `<Environment>` map, khoang in nhìn xuyên qua kính còn hơi dịu hơn độ rực hổ phách và vệt phản chiếu chéo của ảnh studio gốc.
  2. **Cao độ & góc pitch camera**: Vị trí camera mặc định trong `Scene.jsx` (`[0.86, 0.22, 1.50]`) có góc chúc xuống ($7.25^\circ$) lớn hơn đôi chút so với góc ngang gần chân đế của reference ($\sim 4.5^\circ$), làm phần chân đế trước và chân cao su trông khép thấp hơn một chút so với bản chụp gốc.
  3. Codex có thể cân nhắc chỉnh nhẹ độ trong kính hoặc thêm `<Environment>` Studio softbox trong `Scene.jsx` nếu muốn tăng độ bóng phản xạ cho mô hình true-3D V3 khi tích hợp.
