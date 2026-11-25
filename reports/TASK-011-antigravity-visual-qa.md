# Báo cáo Kiểm tra & Thẩm định Visual Hero — TASK-011-HERO-VISUAL-QA

- **Task ID**: TASK-011-HERO-VISUAL-QA
- **Owner**: antigravity
- **Kết luận thẩm định**: `PASS`
- **Timestamp**: 2026-11-23T19:20:00+07:00
- **Phạm vi kiểm tra**:
  - `website/src/components/StaticPhotorealPrinter.jsx`
  - `website/src/styles.css`
  - `website/public/hero_architectural_printer.png`
  - `website/public/hero_architectural_printer.webp`

---

## 1. Kết quả thẩm định Acceptance Criteria

| Tiêu chí | Kết quả | Chi tiết thẩm định |
| :--- | :---: | :--- |
| **Direct Photoreal Object** | **PASS** | Không sử dụng container card, không viền khung nhân tạo, không status badge hay overlay text đè lên máy. Máy in 3D đứng trực tiếp trên nền trắng của trang web. |
| **Silhouette & Grounding** | **PASS** | Thân máy đầy đủ chi tiết (buồng kín, gantry CoreXY, bàn in, đầu in, màn hình điều khiển, chân đế hai bên). Contact shadow mềm mại tự nhiên trong kênh alpha RGBA (0-255) tiếp đất vững chắc, không bị cụt hay cắt phẳng chân máy. |
| **Tỷ lệ & Không bị crop** | **PASS** | Kiểm tra trên cả 3 viewport baseline (1440×900, 1280×720, 390×844) và mobile full view (390×1200): máy giữ trọn vẹn silhouette, không bị clipping bất kỳ cạnh nào. |
| **Asset & Console Health** | **PASS** | Cả định dạng PNG (198KB) và WebP (36KB) tải trơn tru (HTTP 200), kích thước chuẩn 560×480px. Console DevTools sạch 100% (không cảnh báo 404 hay lỗi render). |
| **Production Build** | **PASS** | `npm run build --prefix website` hoàn thành thành công trong 783ms, không phát sinh lỗi đóng gói hay bundle break. |

---

## 2. Bằng chứng kiểm tra thực tế (Visual Evidence)

Tất cả ảnh chụp màn hình kiểm tra thực tế đã được lưu trữ trong thư mục `reports/`:

1. **Desktop Baseline (1440 × 900)**:
   - File: `reports/hero-qa-1440x900.png`
   - Đánh giá: Bố cục 2 cột cân xứng giữa nội dung chữ bên trái và máy in bên phải. Khoảng đệm `padding: 32px 48px 32px 16px` giữ khoảng cách thông thoáng với thanh điều hướng và stats bar bên dưới.
2. **Laptop Baseline (1280 × 720)**:
   - File: `reports/hero-qa-1280x720.png`
   - Đánh giá: Tỷ lệ co giãn mượt mà qua `max-height: 580px; object-fit: contain;`, không lệch dòng hay tràn giao diện.
3. **Mobile Above-the-fold Baseline (390 × 844)**:
   - File: `reports/hero-qa-390x844.png`
   - Đánh giá: Khối tiêu đề và nút CTA nằm trọn vẹn trong màn hình đầu tiên, phần nóc máy in xuất hiện tự nhiên mời gọi thao tác cuộn.
4. **Mobile Full Scrolled View (390 × 1200)**:
   - File: `reports/hero-qa-390-mobile.png`
   - Đánh giá: Khi cuộn xuống trên mobile, máy in hiển thị trọn vẹn 100% thân máy, chân máy và bóng đổ tiếp đất, căn giữa ngay ngắn trên dải stats 3 cột phía dưới.

---

## 3. Tuân thủ phân quyền (Ownership Boundary)

- **Các file thuộc phạm vi**: Duy trì tính tối giản, chuẩn mực trực quan cao nhất cho `StaticPhotorealPrinter.jsx`, `styles.css` và hai file asset ảnh.
- **Không xâm lấn**: Không chỉnh sửa file GLB, Three.js viewer, backend hay các file thuộc quyền quản lý của Codex.
- **Bàn giao**: Chuyển giao toàn bộ kết quả cho Codex review kỹ thuật và visual tổng thể.
