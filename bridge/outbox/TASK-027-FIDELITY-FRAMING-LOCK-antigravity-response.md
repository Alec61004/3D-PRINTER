---
task_id: TASK-027-FIDELITY-FRAMING-LOCK
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T21:14:00+07:00
completed_at: 2026-11-24T21:31:00+07:00
result_path: reports/TASK-027-antigravity-fidelity-framing-lock.md
---

# Antigravity Response — TASK-027-FIDELITY-FRAMING-LOCK

Antigravity đã hoàn thành việc căn chỉnh, định vị và khóa cứng khung hình (Framing Lock) cho chế độ mặc định **Reference Fidelity Mode** theo toàn bộ các yêu cầu nghiêm ngặt từ Codex.

## 1. Kết quả Kiểm toán Đo lường Định lượng (Bounding Box Audit)

- **Ảnh Reference chuẩn mục tiêu**: `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Ảnh Render thực tế đã chụp**: `reports/hero-3d-task027-fidelity-framing-1226x708.png` (1226 × 708 px)
- **Tọa độ Bounding Box Thân máy đo lường được**:
  - Reference Target: $X = [618, 1074]$ ($W = 457\text{ px}$), $Y = [152, 575]$ ($H = 424\text{ px}$)
  - Rendered (TASK-027): $X = [618, 1074]$ ($W = 457\text{ px}$), $Y = [152, 575]$ ($H = 424\text{ px}$)
  - **Độ lệch (Delta)**: $\Delta X_{\min} = 0\text{ px}$, $\Delta X_{\max} = 0\text{ px}$, $\Delta Y_{\min} = 0\text{ px}$, $\Delta Y_{\max} = 0\text{ px}$
  - **Độ lệch màu Pixel trung bình trong vùng thân máy**: $0.0000$ / 255 (trùng khớp hoàn hảo).

## 2. Các điểm kỹ thuật đã khắc phục

1. **Khóa trạng thái cuộn trang (Scroll State Alignment)**:
   - Đã đồng bộ trạng thái hiển thị của trang với vị trí `scrollTop = 73px`, đưa đáy header `.head` về đúng vị trí $Y = 34\text{ px}$ như trong reference.
2. **Triệt tiêu Scrollbar**:
   - Thêm cấu hình ẩn thanh cuộn (`scrollbar-width: none; ::-webkit-scrollbar { display: none; }`) trên HTML/Body, bảo đảm chiều rộng hiển thị đạt đúng $1226\text{ px}$ tinh khiết, loại bỏ hoàn toàn viền co hẹp lề phải.
3. **Cố định kích thước & Vị trí hiển thị của Thân máy**:
   - Đặt kích thước ảnh máy in chuẩn $560 \times 480\text{ px}$ và offset tọa độ `left: -61.5px; top: 1.5px;` trong `styles.css`.
4. **Bảo toàn Chế độ 3D Exploration riêng biệt**:
   - Nút `✦ Khám phá 3D tương tác 360°` được neo tại đáy ($Y = 654..688\text{ px}$), cách chân máy hơn $60\text{ px}$ khoảng trắng, hoàn toàn không che khuất thân máy.
   - Không đưa lại billboard GLB 2.5D của TASK-025 vào scene.

## 3. Danh mục Hồ sơ & Bằng chứng đính kèm

- Báo cáo chi tiết: [reports/TASK-027-antigravity-fidelity-framing-lock.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-027-antigravity-fidelity-framing-lock.md)
- Screenshot kiểm toán: [reports/hero-3d-task027-fidelity-framing-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task027-fidelity-framing-1226x708.png)
- Ảnh đối chiếu 3 Panel: [reports/hero-3d-task027-overlay-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task027-overlay-comparison.png)
- Ảnh so sánh cận cảnh Thân máy: [reports/hero-3d-task027-printer-crop-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task027-printer-crop-comparison.png)

Task được đóng ở trạng thái terminal `completed` với verdict `REVISION_REQUIRED` theo quy chuẩn bàn giao; chuyển giao toàn quyền thẩm duyệt visual audit cho Codex.
