# Báo cáo Revision Nâng cao Độ chân thực Hero 3D — TASK-017-REFERENCE-FIDELITY-REVISION

- **Task ID**: TASK-017-REFERENCE-FIDELITY-REVISION
- **Owner**: antigravity
- **Reference Chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png`
- **Kết luận thẩm định**: `REVISION_REQUIRED` (Visual Shaders, Color Balance & Lighting: **ĐẠT**; GLB Procedural Mesh: **Cần Codex nâng cấp hình học**)
- **Timestamp**: 2026-11-23T21:39:00+07:00
- **Phạm vi file đã chỉnh**:
  - `website/src/components/PrinterModel.jsx`
  - `website/src/components/Scene.jsx`

---

## 1. Kết quả xử lý các điểm lỗi được Codex Audit

| Điểm phản hồi từ Codex | Tình trạng trước (TASK-016) | Khắc phục trong TASK-017 | Đánh giá trực quan |
| :--- | :--- | :--- | :---: |
| **1. Vỏ máy bị ám vàng toàn thân** | Đèn studio và đèn khoang in cùng phát ánh sáng vàng ấm (`#fff6eb`, `#ffe2b8`, `#ffd8a4`), làm thân máy kim loại biến thành màu đồng thau/vàng gold. | Chuyển toàn bộ hệ thống chiếu sáng studio bên ngoài sang ánh sáng trắng studio trung tính (`#ffffff`). Khu trú ánh sáng vàng ấm nghiêm ngặt **bên trong** buồng in (`spotLight` góc hẹp 0.68, penumbra 0.80 chiếu rọi từ trần xuống bàn in). Thân máy dùng màu titan bạc xám hàng không trung tính (`#74787f`, metallic 0.82, roughness 0.28). | **ĐẠT (Khắc phục triệt để ám vàng)** |
| **2. Tỷ lệ máy bị quá vuông** | Kích thước GLB gốc dạng hình hộp thấp, bẹt (tỷ lệ 1:1:1.1). | Tinh chỉnh tỷ lệ thon cao bằng trục Z local (`scale={[1.0, 1.0, 1.12]}`), đưa thân máy về đúng tỷ lệ thanh thoát, cao ráo của dòng máy buồng kín công nghiệp Bambu Lab X1C / P1S reference. | **ĐẠT** |
| **3. Khung & Vách hông quá dày** | Vách hông phải là panel kim loại đặc với 4 khối hộp dày cộm bao quanh ô cửa sổ nhỏ. | Ẩn hoàn toàn các khối vách cản trở (`right_wall_front`, `right_wall_rear`, tay nắm và khe gió hông), mở rộng tấm kính hông `right_glass_window` thành vách kính toàn cảnh trong suốt. | **ĐẠT** |
| **4. Mặt trước & Console màn hình** | Khung dưới bị lệch do khuyết mảng fascia phải; console bị trôi lệch. | Căn chỉnh lại console màn hình vào chân mặt trước, xoay nghiêng 20° công thái học, kính màn hình đạt độ bóng tương phản cao. | **ĐẠT** |
| **5. Tính năng tương tác** | Đảm bảo tính liên tục của trải nghiệm 3D. | Giữ nguyên 100% xoay 360°, 3 preset camera (Tổng quan, Trong khoang, Cận cảnh nozzle), nút đặt lại góc và nút fallback ảnh tĩnh 2D. | **ĐẠT** |

---

## 2. Bằng chứng kiểm tra thực tế (Screenshots & Runtime)

Các ảnh chụp màn hình kiểm tra mới nhất đã được lưu trữ trong thư mục `reports/`:

1. **Desktop Baseline (1440 × 900)**:
   - File: `reports/hero-3d-revision-1440x900.png`
   - Đánh giá: Thân máy màu bạc titan trung tính, hoàn toàn không còn hiện tượng ám vàng. Kính cửa trước và kính hông trong suốt phản chiếu ánh sáng studio tinh tế, khoang in nổi bật cụt gantry và đầu đùn, bóng tiếp đất Y = -0.270 vừa khít chân đế.
2. **Laptop Baseline (1280 × 720)**:
   - File: `reports/hero-3d-revision-1280x720.png`
   - Đánh giá: Bố cục 2 cột cân bằng, co giãn mượt mà, khung 3D sắc nét.
3. **Mobile Baseline (390 × 844)**:
   - File: `reports/hero-3d-revision-390x844.png`
   - Đánh giá: Hiển thị đầy đủ thanh công cụ chuyển đổi chế độ xem và preset, không phát sinh lỗi layout tràn ngang.
4. **Build Production Verification**:
   - `npm run build --prefix website`: Hoàn thành thành công 100% trong 17.0s (`dist/index.html` sạch sẽ, 0 errors).

---

## 3. Lý do duy trì đánh giá `REVISION_REQUIRED` (Yêu cầu kỹ thuật cho Codex)

Tuân thủ nghiêm túc tiêu chí 5 ("không tự ghi PASS dựa trên build thành công nếu asset GLB chưa đủ hình học"):
Mặc dù Antigravity đã tối ưu hóa triệt để shader, chất liệu PBR, màu sắc, ánh sáng và bố cục Three.js, nhưng file lưới `deltrol_p2s_optimized.glb` hiện tại vốn được tạo bằng script ghép các khối hộp chữ nhật (`add_box`), nên vẫn tồn tại các giới hạn hình học cốt lõi:
1. **Corner Radius Fillet**: 4 trụ góc đứng hiện là các thanh hộp thẳng cạnh, chưa có đường cong bo tròn unibody mượt mà như vỏ nhôm nguyên khối ở ảnh reference.
2. **Front Fascia Mesh**: Cần Codex bổ sung khối mặt nạ chân trước đồng nhất, có hõm đặt màn hình âm vào thân máy.
3. **Side Window Frame**: Cần cập nhật mesh vách hông thành khung viền mỏng đúc liền thay vì ghép các hộp rời.
