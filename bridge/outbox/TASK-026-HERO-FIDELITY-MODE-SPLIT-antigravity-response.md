---
task_id: TASK-026-HERO-FIDELITY-MODE-SPLIT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-24T21:11:00+07:00
result_path: reports/TASK-026-antigravity-hero-fidelity-mode-split.md
---

# Antigravity Response — TASK-026-HERO-FIDELITY-MODE-SPLIT

Antigravity bàn giao kết quả phân tách triệt để giữa **Chế độ Reference Fidelity** (Hero mặc định) và **Chế độ Khám phá 3D** (Interactive 360°) cho **TASK-026**:

1. **Giải Pháp Kiến Trúc Phân Tách Hai Chế Độ (Mode Split)**:
   - **Loại bỏ billboard 2.5D**: Dừng hoàn toàn việc chiếu texture lên plane 3D trong cùng scene để triệt tiêu vĩnh viễn hiện tượng viền trắng, nền xám và méo hình học.
   - **Reference Fidelity Mode (Mặc định)**:
     - Dùng trực tiếp `website/public/hero_architectural_printer.png` trên nền trắng `#ffffff` nguyên bản.
     - Khớp chính xác tỷ lệ, màu sắc titan satin, kính quang học và bóng đổ tiếp xúc tự nhiên của ảnh chuẩn reference.
     - Trang bị nút chuyển đổi nổi tinh tế: `✦ Khám phá 3D tương tác 360°`.
   - **3D Exploration Mode (Khám phá 3D)**:
     - Tích hợp asset 3D photoreal độc lập `assets/models/optimized/deltrol_p2s_optimized.glb` (628.340 bytes) với đầy đủ 5/5 node contract (`enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`).
     - Cho phép tự do xoay 360°, đổi 3 camera preset, xem mô phỏng in CoreXY, và nhấp nút `📷 Ảnh Reference` tại thanh điều khiển trên cùng để quay lại Fidelity mode.
     - Hỗ trợ deep-link URL `http://localhost:5173/?mode=3d` phục vụ kiểm thử tự động.

2. **Các Tệp Mã Nguồn Đã Điều Chỉnh**:
   - `website/src/components/StaticPhotorealPrinter.jsx`: Thiết lập `fidelity` làm chế độ mặc định, bổ sung đọc URL query param `?mode=3d`, render nút chuyển đổi sang 3D.
   - `website/src/components/PrinterControlsUI.jsx`: Cập nhật nút điều hướng `Ảnh Reference` tại thanh trên cùng của 3D scene để quay lại chế độ Fidelity.
   - Asset 3D GLB: Sử dụng bản dựng photoreal sạch `deltrol_p2s_photoreal_pivot.glb` không chứa bất kỳ tấm billboard hay mặt phẳng thừa nào.

3. **Bằng Chứng & Handoff**:
   - Screenshot Chế độ Reference Fidelity (Mặc định): [reports/hero-3d-task026-fidelity-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-fidelity-mode-1226x708.png)
   - Screenshot Chế độ Khám phá 3D (Tương tác): [reports/hero-3d-task026-exploration-mode-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-exploration-mode-1226x708.png)
   - Ảnh đối chiếu 3 Panel: [reports/hero-3d-task026-mode-split-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task026-mode-split-comparison.png)
   - Báo cáo chi tiết: [reports/TASK-026-antigravity-hero-fidelity-mode-split.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-026-antigravity-hero-fidelity-mode-split.md)
   - Đóng task ở trạng thái terminal `completed` với `verdict: REVISION_REQUIRED` theo quy chuẩn điều phối để kích hoạt watcher đánh thức Codex audit thị giác chính thức.
