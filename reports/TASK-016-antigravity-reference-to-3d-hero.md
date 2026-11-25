# Báo cáo Đối chiếu & Hoàn thiện Hero 3D theo Reference — TASK-016-REFERENCE-TO-3D-HERO

- **Task ID**: TASK-016-REFERENCE-TO-3D-HERO
- **Owner**: antigravity
- **Reference Chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png`
- **Kết luận thẩm định**: `REVISION_REQUIRED` (Visual Materials & Lighting: **PASS**; Mesh Geometry Fidelity: **Cần cập nhật GLB**)
- **Timestamp**: 2026-11-23T21:30:00+07:00
- **Phạm vi file đã chỉnh**:
  - `website/src/components/PrinterModel.jsx`
  - `website/src/components/Scene.jsx`

---

## 1. Đối chiếu trực tiếp với Ảnh Reference (`printer-hero-reference-2026-11-23.png`)

| Thành phần thị giác | Ảnh Reference | Trạng thái cũ (TASK-015) | Cải tiến Antigravity (TASK-016) | Đánh giá |
| :--- | :--- | :--- | :--- | :---: |
| **Tư thế máy (Orientation)** | Máy đứng thẳng vuông vắn, góc nhìn 3/4 trước-phải. | Model GLB bị xoay sai trục (Z-up vs Y-up), nằm ngửa/nghiêng 90°. | Áp dụng `rotation={[-Math.PI / 2, 0, 0]}` đưa máy đứng thẳng đúng chiều vật lý. | **PASS** |
| **Màu sắc & Chất liệu vỏ** | Nhôm xước champagne-bạc / titanium satin (`#8e8a84`, metallic ~0.78, roughness ~0.30). | Bị texture tối nhân bản đè lên thành xám đen/than chì, góc bo trắng bóng. | Thay thế toàn bộ vật liệu PBR unibody titanium chuẩn, xóa map nhân bản tối. | **PASS** |
| **Kính cửa trước & Buồng in** | Kính khói trong suốt, nhìn rõ cụm gantry, đầu in và mô hình trên bàn in. | Kính đen mờ (opacity 0.72) che kín hoàn toàn chi tiết buồng in. | Điều chỉnh Smoked Glass sang `opacity: 0.42, roughness: 0.05, metalness: 0.22`, nhìn rõ bàn in và đầu đùn. | **PASS** |
| **Ánh sáng buồng in** | Ánh sáng vàng ấm (tungsten / amber) rực rỡ bên trong khoang in. | Ánh sáng trắng lạnh, tối. | Bổ sung Spotlight và Point light nội thất ấm áp (`#ffdca8`, `#ffc882`), tạo độ sâu studio. | **PASS** |
| **Tay cầm cửa** | Thanh dọc màu bạc kim loại ở cạnh phải cánh cửa. | Có trong GLB nhưng bị chìm. | Định dạng PBR riêng cho `door_handle` (`#c8c2b8`, metalness 0.88, roughness 0.20). | **PASS** |
| **Bàn in & Chi tiết in** | Bàn in PEI vàng rực, mô hình in nổi bật. | Cuộn nhựa to chèn kín bên trong. | Ẩn cuộn nhựa bên trong khoang (`nodes.spools.visible = false`), định vị bàn in PEI vàng và mô hình ở độ cao chuẩn. | **PASS** |
| **Hình học vách hông phải** | Kính lớn trong suốt chiếm phần lớn diện tích vách bên phải. | Vách kim loại đặc chỉ có một ô cửa sổ nhỏ khoét ở giữa (`right_wall_top/bot/front/rear`). | Đã chỉnh kính hông trong suốt, nhưng khung kim loại GLB hiện tại khoét ô nhỏ. | **REVISION_REQUIRED** |
| **Mặt nạ dưới & Console** | Console màn hình đặt chìm nghiêng giữa đáy cửa trước. | Khung dưới bị lệch do GLB gốc chỉ có `front_bot_fascia_left`. | Nghiêng console 24° (`rotation.x = 0.38`), cần mesh GLB hoàn thiện mặt fascia phẳng đều. | **REVISION_REQUIRED** |

---

## 2. Bằng chứng kiểm tra thực tế (Screenshots & Runtime)

1. **Desktop Baseline (1440 × 900)**:
   - File: `reports/hero-3d-reference-1440x900.png`
   - Đánh giá: Thân máy màu titan champagne satin chuẩn xác, buồng in sáng ấm, tay cầm và kính hiển thị rõ ràng, bóng tiếp đất (`ContactShadows` tại Y = -0.242) ăn khớp với đế cao su.
2. **Laptop Baseline (1280 × 720)**:
   - File: `reports/hero-3d-reference-1280x720.png`
   - Đánh giá: Tỷ lệ co giãn mượt mà, OrbitControls phản hồi tức thì, không giật lag.
3. **Mobile Baseline (390 × 844)**:
   - File: `reports/hero-3d-reference-390x844.png`
   - Đánh giá: Giao diện điều khiển (Ảnh 2D / 3D, Preset, Tự xoay, Đặt lại góc) hiển thị đầy đủ, không gây lỗi tràn trang.
4. **Build Production Verification**:
   - `npm run build --prefix website`: Thành công 100% trong 5.79s (`dist/index.html` bundled sạch sẽ, 0 errors).

---

## 3. Nội dung cụ thể cần bổ sung (Dành cho Codex nâng cấp GLB)

Để đạt 100% fidelity hình học như ảnh reference:
1. **Side Glass Geometry**: Mở rộng `right_glass_window` bao phủ 85% diện tích vách bên phải (giảm bề rộng viền `right_wall_front` và `right_wall_rear` từ 0.07m xuống 0.02m) để buồng in thông thoáng từ góc nhìn bên hông.
2. **Front Fascia Symmetry**: Bổ sung `front_bot_fascia_right` cân xứng với `front_bot_fascia_left` để console màn hình nằm khít chính giữa mặt trước.
3. **Corner Radius Fillet**: Tăng độ vát bo cong mềm cho 4 trụ góc unibody thay cho khối hộp vuông cắt cạnh.
