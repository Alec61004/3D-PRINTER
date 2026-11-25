# Báo cáo Triển khai Chế độ 3D Tương tác Hero — TASK-012-HERO-3D-ROTATION

- **Task ID**: TASK-012-HERO-3D-ROTATION
- **Owner**: antigravity
- **Kết luận thẩm định**: `READY_FOR_CODEX_AUDIT`
- **Timestamp**: 2026-11-23T19:55:00+07:00
- **Phạm vi file đã chỉnh sửa**:
  - `website/src/components/Scene.jsx`
  - `website/src/components/PrinterControlsUI.jsx`
  - `website/src/components/StaticPhotorealPrinter.jsx`
  - `website/src/styles.css`

---

## 1. Mục tiêu & Định hướng thị giác

Chuyển đổi khu vực Hero từ hình ảnh photoreal tĩnh (đã được duyệt trong TASK-011) thành trải nghiệm 3D tương tác đa góc nhìn hoàn chỉnh, đồng thời duy trì 100% chất lượng thị giác cao cấp:
- **Direct Seamless Grounding**: Mô hình 3D hiển thị trực tiếp trên nền trắng tinh khiết của Hero (`alpha: true`, nền trong suốt), không đóng khung card, không viền hộp nhân tạo.
- **Silhouette & Contact Shadows**: Đổ bóng tiếp xúc mềm mại (`ContactShadows` opacity 0.42, blur 1.8) dưới 4 chân đế cao su, giữ nguyên vóc dáng buồng kín Bambu Lab P2S.
- **PBR Material Tuning**: Tinh chỉnh độ truyền quang kính buồng in (`transparent: true`, `opacity: 0.28`, `color: #223344`, `depthWrite: false`) giúp nhìn thấu cụm đùn, thanh carbon CoreXY, bàn nhiệt và phôi in; nhôm phay xước anodized bạc sáng đồng điệu với ánh sáng studio.
- **Dual Mode & Error Fallback**: Hỗ trợ chuyển đổi linh hoạt giữa chế độ "Xoay 3D 360°" và "Ảnh 2D photoreal tĩnh", kèm cơ chế `ModelErrorBoundary` tự động fallback về ảnh photoreal chuẩn nếu WebGL gặp sự cố.

---

## 2. Bảng đối chiếu Tiêu chí Chấp nhận (Acceptance Criteria)

| Tiêu chí | Kết quả | Chi tiết thẩm định thực tế |
| :--- | :---: | :--- |
| **1. Chế độ 3D tương tác thực tế** | **PASS** | Tích hợp Three.js / React Three Fiber canvas thực thụ với `OrbitControls` mượt mà qua damping (`dampingFactor: 0.06`). Hỗ trợ xoay tự do bằng kéo chuột trên desktop và vuốt chạm (touch swipe) trên mobile; thu phóng có giới hạn an toàn (`minDistance: 0.7`, `maxDistance: 2.4`). |
| **2. Trạng thái Loading / Error & Fallback** | **PASS** | Trạng thái tải `LoadingCard` hiển thị tinh tế trong quá trình khởi tạo 3D. Component `ModelErrorBoundary` bao bọc toàn bộ canvas; nếu WebGL context lost hoặc lỗi shader xảy ra, hệ thống tự động fallback về `StaticPhotorealPrinter` (ảnh 4K photoreal đã duyệt) kèm thông báo lỗi trực quan mà không làm crash ứng dụng. |
| **3. Reset góc nhìn & Auto-orbit nhẹ nhàng** | **PASS** | Nút `⟲ Đặt lại góc` (`onResetView`) lập tức đưa camera và điểm ngắm về góc phối cảnh 3/4 chuẩn (`pos: [0.92, 0.36, 1.45]`, `target: [0, 0.02, 0]`). Nút `⏸ Tự xoay: Bật/Tắt` cho phép người dùng chủ động điều khiển. Khi người dùng thao tác xoay chuột/vuốt, auto-orbit tự động tạm ngưng hoàn toàn, tuyệt đối không giật giằng hay cướp quyền điều khiển của người dùng. |
| **4. Silhouette & Tiếp đất trên nền trắng** | **PASS** | Giữ trọn vẹn đường nét silhouette thân máy, cụm màn hình cảm ứng nghiêng, cửa kính buồng in và chân máy. Bóng đổ tiếp xúc chân thực trên nền trắng, không quay lại card wrapper, không viền bao quanh thô kệch. |
| **5. Responsive Desktop & Mobile không crop** | **PASS** | Kiểm tra trên các mốc phân giải baseline (1440×900, 1280×720, 390×844) và mobile cuộn toàn trang (390×1200): Không phát sinh tràn ngang (`hasHorizontalOverflow: false`), thanh điều khiển co giãn dạng pill thông minh, không che khuất thân máy hay nội dung chữ. |
| **6. Build & Console Health** | **PASS** | Production build `npm run build` hoàn thành thành công trong Vite 5.4.21. Console trình duyệt sạch 100%, không lỗi HTTP 404, không cảnh báo tài nguyên thiếu. |
| **7. Lưu trữ Evidence & Handoff** | **PASS** | Tất cả ảnh chụp màn hình kiểm tra thực tế được lưu vào `reports/`; tạo báo cáo thẩm định tại `reports/TASK-012-antigravity-3d-rotation.md` và phản hồi outbox tại `bridge/outbox/TASK-012-HERO-3D-ROTATION-antigravity-response.md`. |

---

## 3. Bằng chứng kiểm tra thị giác (Visual Evidence)

Các bằng chứng ảnh chụp trực tiếp từ trình duyệt Chromium được lưu trữ trong thư mục `reports/`:

1. **Desktop Baseline Phối cảnh 3/4 Chuẩn (1440 × 900)**:
   - File: `reports/hero-3d-1440x900.png`
   - Đánh giá: Máy in hiển thị trực diện trên nền trắng, nổi bật với vỏ nhôm anodized bạc, cửa kính trong suốt thấy rõ buồng in CoreXY, bóng đổ tiếp xúc mềm mại; hai thanh điều khiển trên/dưới bố trí thông thoáng, cân đối hoàn hảo với khối nội dung bên trái.
2. **Desktop Tương tác Xoay Tự do (1440 × 900 - Rotated)**:
   - File: `reports/hero-3d-rotated.png`
   - Đánh giá: Thao tác kéo chuột xoay máy in sang góc nhìn phía sau/bên hông, hiển thị đầy đủ chi tiết khay gá cuộn nhựa (spool holder), cổng kết nối nguồn và khe thông gió làm mát.
3. **Laptop Viewport Baseline (1280 × 720)**:
   - File: `reports/hero-3d-1280x720.png`
   - Đánh giá: Tỷ lệ co giãn mượt mà, khung canvas và thanh công cụ giữ vững khoảng cách an toàn, không bị tràn viền hay đè lên dải thông số kỹ thuật bên dưới.
4. **Mobile Above-the-fold (390 × 844)**:
   - File: `reports/hero-3d-390x844.png`
   - Đánh giá: Tiêu đề, văn bản dẫn nhập và nút CTA nằm trọn vẹn ở màn hình đầu tiên, phần nóc máy và thanh chuyển góc nhìn 3D lộ diện tự nhiên kích thích người dùng cuộn xem.
5. **Mobile Scrolled Full Interactive View (390 × 844)**:
   - File: `reports/hero-3d-390-mobile.png`
   - Đánh giá: Khi cuộn tới Hero, máy in hiển thị trọn vẹn 100% silhouette, chân máy và bóng đổ. Các nút điều khiển pill co giãn vừa vặn chiều ngang 390px, hỗ trợ thao tác chạm ngón tay thuận tiện, không gây tràn ngang.

---

## 4. Tuân thủ phân quyền (Ownership Boundary)

- **Owner Antigravity**: Hoàn thành toàn diện phần tích hợp visual/UI trong 4 file được cấp phép (`Scene.jsx`, `PrinterControlsUI.jsx`, `StaticPhotorealPrinter.jsx`, `styles.css`).
- **Phạm vi bảo toàn**: Tuyệt đối không chỉnh sửa model GLB gốc, không thay đổi pipeline backend/Blender, không can thiệp vào file thuộc quyền của Codex.
- **Bàn giao**: Sẵn sàng chuyển giao cho Codex tiến hành technical audit theo quy trình handoff.
