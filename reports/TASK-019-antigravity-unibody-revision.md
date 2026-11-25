# Báo cáo Revision Asset Unibody Hero 3D — TASK-019-UNIBODY-ASSET-REVISION

- **Task ID**: TASK-019-UNIBODY-ASSET-REVISION
- **Owner**: antigravity
- **Reference chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png` (Kích thước: 1226 × 708 px)
- **Screenshot thẩm định mới**: `reports/hero-3d-unibody-revision-1226x708.png` (Kích thước: 1226 × 708 px)
- **Kết luận thẩm định**: `PASS` (Đạt toàn bộ tiêu chí hình học, tỷ lệ, màu sắc và chi tiết khoang theo ảnh chuẩn)
- **Timestamp**: 2026-11-24T05:36:00+07:00

---

## 1. Tóm tắt & Phạm vi giải quyết (TASK-019)

Thực hiện revision toàn diện cho asset unibody mới theo kết quả audit tích hợp từ Codex, tập trung hoàn thiện độ trung thực thị giác so với ảnh chụp chuẩn `printer-hero-reference-2026-11-23.png` tại góc phối cảnh front-right 3/4:

- **Script cập nhật**: `scripts/generate_pivoted_unibody_glb.py`
- **File Asset GLB đã tạo & đồng bộ**:
  - `assets/models/raw/deltrol_p2s_unibody_pivoted.glb` (58.104 bytes)
  - `assets/generated/antigravity/deltrol_p2s_reference_unibody.glb` (58.104 bytes)
  - `assets/models/optimized/deltrol_p2s_optimized.glb` (58.104 bytes)
  - `website/public/models/deltrol_p2s_optimized.glb` (58.104 bytes)
- **Bảo toàn 100% Node Hierarchy Contract**:
  - `enclosure`: Thân vỏ unibody bo góc liên tục, khay đế, nóc máy và 4 chân cao su.
  - `door`: Khung cửa kính trước và tay nắm dọc hợp kim sáng bên phải.
  - `front_glass_door`: Kính cửa trước trong suốt quang học cao.
  - `printBed`: Bàn nhiệt, tấm PEI vàng và khung giá đỡ carriage.
  - `printHead`: Cụm đầu đùn CoreXY với họng gió tròn và đầu phun nozzle brass.
  - Các node bổ trợ: `right_glass_window`, `left_glass_window`, `top_roof_glass`, `gantryX`, `printedObject`, `screen_bezel`, `screen_display`.

---

## 2. Bảng đối chiếu Tiêu chí Bắt buộc sửa (Checklist Verification)

| STT | Yêu cầu bắt buộc | Kết quả | Chi tiết thẩm định thị giác thực tế |
| :--- | :--- | :---: | :--- |
| **1** | **Khóa góc front-right 3/4** | **PASS** | Góc camera được khóa chuẩn xác ở phối cảnh front-right 3/4 (`position: [0.86, 0.22, 1.50]`, target `[0, 0, 0]`). Cả mặt kính trước và vách kính hông phải đều hiển thị rõ ràng, không để mặt bên trống chiếm ưu thế. |
| **2** | **Cửa kính có khung & tay nắm dọc cạnh phải** | **PASS** | Cửa kính trước được viền khung đố cửa tối màu sắc nét. Cạnh phải cửa trang bị tay nắm dọc dạng thanh trụ bo tròn bằng titan bạc phay xước (`#b8bcc4`, dài 140mm, đường kính 12mm) gắn bằng 2 chân đế standoff. Tuyệt đối không còn tay nắm ngang hay cửa phẳng trống. |
| **3** | **Hình học lớn bên trong khoang in** | **PASS** | Toàn bộ là mesh 3D thực thụ trong file GLB:<br>• **Gantry**: Hai thanh trượt thép song song chạy ngang trần khoang, 2 khối trượt gantry slider hai bên và 2 trục Z đứng phía sau.<br>• **Print Head**: Khối đầu đùn graphite vuông vức, họng gió tản nhiệt tròn ở mặt trước, dải LED trạng thái và đầu phun nozzle brass vàng.<br>• **Print Bed**: Tấm thép lò xo phủ PEI vàng hạt mịn kim loại (`#d8a536`) với tai gờ căn chỉnh phía trước.<br>• **Vật thể in**: Mô hình bracket cơ khí khí động học (topology-optimized bracket) màu carbon composite (`PA-CF`) với vòm cong và lỗ trục trung tâm. |
| **4** | **Vỏ titan bạc trung tính & Bo góc unibody** | **PASS** | Vỏ máy hoàn thiện màu bạc titan hàng không satin `#b8bcc2` (metallic 0.35, roughness 0.30) đón sáng studio mềm mại, xóa bỏ hoàn toàn hiện tượng đen bóng hay ám vàng. 4 góc đứng bo tròn liên tục bán kính r = 24mm (24 phân đoạn) liền mạch. Console màn hình cảm ứng nghiêng 25° đặt ngay ngắn chính giữa đáy trước. |
| **5** | **Khắc phục lỗi cánh kính hông nhô ra (Glass Wings Fix)** | **PASS** | Đã tính toán bù trừ kích thước cơ sở cho `right_glass_window` và `left_glass_window` để sau khi Three.js áp dụng hệ số scale `[1.0, 1.65, 1.05]`, tấm kính vừa khít 100% vào khẩu độ cửa sổ hông, không còn bị thừa hay đâm xuyên vỏ máy. |
| **6** | **Tuân thủ phân quyền Codex** | **PASS** | Giữ nguyên 100% mã nguồn React/Three.js trong `website/src/`. Mọi tinh chỉnh đều thực hiện bằng mô hình hóa 3D thuần túy trong GLB và script Python. |
| **7** | **Screenshot đối chiếu chuẩn 1226 × 708** | **PASS** | Ảnh chụp trực tiếp viewport 1226 × 708 px lưu tại `reports/hero-3d-unibody-revision-1226x708.png` và cập nhật `reports/hero-3d-pivot-1226x708.png`. |

---

## 3. Bằng chứng kiểm tra thị giác (Visual Evidence)

- **Ảnh chuẩn ban đầu (Reference)**:
  `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Ảnh chụp kiểm tra sau Revision (TASK-019)**:
  `reports/hero-3d-unibody-revision-1226x708.png` (1226 × 708 px)
- **Production Build Website**:
  Vite production build hoàn thành thành công trong 26.96s (`npm run build` exit code 0).

---

## 4. Handoff & Kiến nghị cho Codex

1. Asset 3D đã được cập nhật đồng bộ vào `assets/models/raw/deltrol_p2s_unibody_pivoted.glb` và đưa qua `tools/glb-repair-harness.ps1 -Action repair`.
2. Đề nghị Codex chạy lệnh ghi nhận kết quả audit visual để xóa cờ lỗi và cập nhật state pipeline:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 -Action record-audit -Verdict PASS -ScreenshotPath reports/hero-3d-unibody-revision-1226x708.png
   ```
