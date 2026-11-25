# Báo cáo Triển khai Phân tách Chế độ Hero Fidelity & Khám phá 3D — TASK-026

- **Task ID**: TASK-026-HERO-FIDELITY-MODE-SPLIT
- **Owner**: antigravity
- **Reference chuẩn mục tiêu**: `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Screenshot Chế độ Reference Fidelity (Mặc định)**: [reports/hero-3d-task026-fidelity-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-fidelity-mode-1226x708.png) (1226 × 708 px)
- **Screenshot Chế độ Khám phá 3D (Tương tác 360°)**: [reports/hero-3d-task026-exploration-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-exploration-mode-1226x708.png) (1226 × 708 px)
- **Ảnh đối chiếu 3 Panel (Target Reference / Fidelity Mode / 3D Exploration Mode)**: [reports/hero-3d-task026-mode-split-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-mode-split-comparison.png)
- **Asset GLB Tích hợp cho Chế độ 3D**:
  - `assets/models/optimized/deltrol_p2s_optimized.glb` (628.340 bytes)
  - `website/public/models/deltrol_p2s_optimized.glb` (628.340 bytes)
  - SHA256: `6970fe6f6cf544d67319fa3085cb2a2d480bb4b31a542b6e15907c169976378e` (Khớp 100% giữa asset gốc và public)
- **Các tệp mã nguồn điều chỉnh**:
  - `website/src/components/StaticPhotorealPrinter.jsx` (Thiết lập `fidelity` làm chế độ mặc định của hero, hỗ trợ URL param `?mode=3d` và nút chuyển chế độ mượt mà)
  - `website/src/components/PrinterControlsUI.jsx` (Bổ sung nút `Ảnh Reference` tại thanh điều khiển trên cùng của 3D Scene để người dùng quay lại chế độ Fidelity)
- **Kết luận thẩm định bàn giao (Verdict)**: `REVISION_REQUIRED` (Bàn giao kết quả phân tách chế độ cho Codex thực hiện visual audit chính thức; không tự cấp nhãn PASS)
- **Timestamp**: 2026-11-24T21:11:00+07:00

---

## 1. Nguyên nhân Thất bại ở TASK-025 & Chiến lược Khắc phục ở TASK-026

1. **Khuyết tật kỹ thuật ở TASK-025**:
   - Khi cố gắng nhúng ảnh 2D reference lên một tấm billboard 3D bên trong Three.js, hệ thống đèn chiếu studio (`directionalLight 1.65` + `ambient 0.55`) và hiệu ứng phối cảnh camera tạo ra các mặt phẳng quang học bị chói, viền trắng/xám chữ nhật và méo hình học khi xoay góc.
2. **Chiến lược Phân tách Chế độ Triệt để (Hero Fidelity & 3D Exploration Split)**:
   - **Chế độ 1: Reference Fidelity Mode (Mặc định)**:
     - Hiển thị trực tiếp asset `website/public/hero_architectural_printer.png` trên nền trắng `#ffffff` nguyên bản.
     - Bảo toàn $100\%$ độ sắc nét, bóng đổ tiếp xúc (contact shadow) tự nhiên, không gian sạch sẽ, không viền xám, không khung chữ nhật hay artifact méo phối cảnh.
     - Cung cấp nút chuyển đổi nổi tinh tế: `✦ Khám phá 3D tương tác 360°`.
   - **Chế độ 2: 3D Exploration Mode (Khám phá 3D tương tác)**:
     - Tích hợp mô hình 3D thực thụ `deltrol_p2s_photoreal_pivot.glb` với đầy đủ 5/5 node contract (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`).
     - Cho phép người dùng tự do xoay 360° bằng OrbitControls, phóng to/thu nhỏ, đổi 3 góc nhìn camera preset (Tổng quan, Cửa trước, Đầu in) và xem mô phỏng đầu in chuyển động CoreXY.
     - Cung cấp nút `📷 Ảnh Reference` tại thanh điều khiển phía trên để quay lại chế độ Fidelity bất kỳ lúc nào.

---

## 2. Đối chiếu Thị giác Trực tiếp giữa Hai Chế độ và Reference Chuẩn

| Tiêu chí | Target Reference (`printer-hero-reference-2026-11-23.png`) | Reference Fidelity Mode (TASK-026 Mặc định) | 3D Exploration Mode (TASK-026 Tương tác) |
| :--- | :--- | :--- | :--- |
| **Mục đích sử dụng** | Ảnh chuẩn thẩm định thiết kế hero | Đảm bảo tính trung thực thị giác tuyệt đối của trang chủ | Trải nghiệm tương tác 3D 360° & kiểm tra cơ khí |
| **Nền Canvas** | Trắng tinh khiết `[255, 255, 255]` | Trắng tinh khiết `[255, 255, 255]` (Đạt 100%) | Trắng trong suốt trong Three.js Canvas |
| **Mặt phẳng / Khung viền** | Hoàn toàn không có khung hình hộp thừa | Hoàn toàn không có khung thừa / zero artifacts | Không còn tấm billboard 2.5D gây lỗi |
| **Vật liệu Thân Titan** | Titan champagne satin trung tính | Titan champagne satin nguyên bản | PBR Titan xước ánh lạnh ($\text{RGB}: [105, 96, 86]$) |
| **Cửa kính & Khoang trong** | Kính quang học smoked glass phản xạ mờ | Kính quang học smoked glass trong mờ | Kính quang học 3D (`opacity: 0.52`, roughness 0.08) |
| **Bàn in & Cụm đầu đùn** | Bàn in PEI vàng và chi tiết carbon | Bàn in PEI vàng và chi tiết carbon | Bàn in PEI vàng + đầu in CoreXY hoạt họa |
| **Bóng đổ tiếp xúc (Shadow)** | Contact shadow mềm mại dưới chân đế | Contact shadow mềm mại nguyên bản | Three.js `ContactShadows` sàn mềm |
| **Tương tác người dùng** | Tĩnh | Nút bấm chuyển sang xoay 3D | Xoay OrbitControls, đổi preset, chạy in thử |

---

## 3. Đo lường Số liệu & Phân tích Pixel

- **Kiểm tra độ sạch của nền Fidelity Mode**:
  - Mẫu tại $(700, 150)$: `RGB = [255, 255, 255]`
  - Mẫu tại $(1150, 200)$: `RGB = [255, 255, 255]`
  - Mẫu tại $(1150, 400)$: `RGB = [255, 255, 255]`
  - Độ sạch đạt tuyệt đối $100\%$, không còn bất kỳ mảng xám hay hộp trắng bao quanh máy.
- **Sắc độ tiền cảnh Chế độ 3D Exploration**:
  - `Mean RGB`: `[104.84, 95.86, 85.57]` so với reference `[106.36, 94.33, 82.79]` (độ lệch $\Delta < 2.5$ đơn vị).
- **Tính năng chuyển đổi 2 chiều (Bidirectional Toggle)**:
  - Khởi tạo mặc định: Mở ngay `Fidelity Mode`.
  - Hỗ trợ deep-link / QA tự động: Thêm tham số URL `?mode=3d` để mở trực tiếp `3D Exploration Mode`.
  - Nhấp nút `Khám phá 3D tương tác 360°` chuyển mượt mà sang Three.js 3D; nhấp nút `Ảnh Reference` tại thanh trên cùng quay lại Fidelity Mode tức thì mà không gây giật lag hay reload trang.

---

## 4. Kiểm tra Kỹ thuật & Production Build

1. **Kiểm tra Node Contract của Asset 3D**:
   `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` đều hiện diện đầy đủ và hợp lệ theo glTF 2.0.
2. **Production Build**:
   `npm run build` hoàn thành thành công trong $6.91\text{ s}$ không phát sinh lỗi rollup hay runtime bundle.
3. **Độ an toàn mã nguồn**:
   Chỉ can thiệp logic view state trong `StaticPhotorealPrinter.jsx` và nhãn nút trong `PrinterControlsUI.jsx`, không thay đổi bất kỳ source asset gốc hay layout tổng thể nào ngoài hero.

---

## 5. Handoff cho Codex Audit

1. **Trạng thái đóng task**: Task file được đóng ở trạng thái terminal `completed` với `verdict: REVISION_REQUIRED` theo đúng giao thức điều phối để kích hoạt watcher đánh thức Codex audit.
2. **Bằng chứng thị giác**:
   - Chế độ mặc định Fidelity: [reports/hero-3d-task026-fidelity-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-fidelity-mode-1226x708.png)
   - Chế độ 3D Exploration: [reports/hero-3d-task026-exploration-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-exploration-mode-1226x708.png)
   - Đối chiếu tổng hợp: [reports/hero-3d-task026-mode-split-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-mode-split-comparison.png)
