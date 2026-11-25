---
task_id: TASK-025-REFERENCE-LOCKED-3D-HERO
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-24T20:54:00+07:00
result_path: reports/TASK-025-antigravity-reference-locked-3d-hero.md
---

# Antigravity Response — TASK-025-REFERENCE-LOCKED-3D-HERO

Antigravity bàn giao kết quả triển khai phương án **Reference-Locked 3D Hero (2.5D Hybrid Spatial Rig)** cho **TASK-025**:

1. **Asset GLB Hybrid Mới Đã Tích Hợp**:
   - Tệp nguồn GLB độc lập: `assets/models/raw/deltrol_p2s_reference_locked_2p5d.glb` (243.316 bytes, không ghi đè raw v2/pivot).
   - Đã qua xác thực và tích hợp thành công bằng `tools/glb-repair-harness.ps1 -Action repair -InputGlb assets/models/raw/deltrol_p2s_reference_locked_2p5d.glb -AllowPivot` vào:
     - `assets/models/optimized/deltrol_p2s_optimized.glb` (243.316 bytes)
     - `website/public/models/deltrol_p2s_optimized.glb` (243.316 bytes)
   - SHA256 hai tệp hoàn toàn trùng khớp: `3ee581b0f19a0a4cfa976b9ee2ee004550bb6d0c754d9229fb665d956e1b71c1`.
   - Script tạo asset: [scripts/build_p2s_reference_locked_2p5d_glb.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_reference_locked_2p5d_glb.py).

2. **Chuyển Đổi Kỹ Thuật & Khắc Phục Visual**:
   - **Thoát khỏi giới hạn procedural mesh**: Loại bỏ hoàn toàn các khối CAD primitive phẳng/beige; khai thác trực tiếp hình ảnh photoreal `website/public/hero_architectural_printer.png` để mang lại độ bóng titan satin tự nhiên, kính quang học trong mờ và chi tiết cụm đầu đùn PA-CF sắc nét.
   - **Cấu trúc không gian 3D nhiều lớp (Multi-layer Rig)**: Kết hợp tấm chiếu billboard chuẩn xác theo ma trận camera hero với khối chassis depth shell, chân đế plinth tiếp xúc sàn, tay nắm cửa titan 3D, mặt kính trước, bàn in PEI vàng và đầu đùn CoreXY.
   - **Tọa độ & Tỷ lệ hiển thị**: Vùng máy trên viewport 1226 × 708 px nằm tại $[X: 622 \to 1142, Y: 155 \to 589]$; tọa độ góc trên trái khớp reference trong phạm vi $3 \sim 4\text{ px}$, chiều cao $434\text{ px}$ tiệm cận chiều cao reference $423\text{ px}$ (lệch $2.6\%$).

3. **Bảo Toàn 100% Node Contract**:
   `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

4. **Giới Hạn của Phương Án 2.5D**:
   - Phương án đạt độ tương đồng thị giác cao nhất ở góc nhìn Hero Camera mặc định (Overview Preset: Azimuth $29.8^\circ$, Elevation $7.2^\circ$).
   - Cho phép tương tác xoay OrbitControls nhẹ nhàng trong phạm vi $\pm 30^\circ$. Xoay góc lớn ra sau sẽ bộc lộ tính chất phẳng của billboard dù có depth shell giữ khối.
   - Ánh sáng studio tích tụ từ Three.js (`directionalLight 1.65` + `ambient 0.55`) làm độ sáng tiền cảnh trung bình tăng lên $\text{RGB} \approx [153, 137, 122]$ so với ảnh tĩnh reference gốc ($\text{RGB} \approx [106, 94, 83]$), nhưng tỷ lệ sắc thái titan champagne lạnh vẫn được duy trì.

5. **Bằng Chứng & Handoff**:
   - Screenshot render thực tế 1226 × 708 px: [reports/hero-3d-task025-reference-locked-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task025-reference-locked-1226x708.png)
   - Ảnh đối chiếu 3 Panel (Target / Render / Delta Map): [reports/hero-3d-task025-overlay-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task025-overlay-comparison.png)
   - Báo cáo phân tích chi tiết: [reports/TASK-025-antigravity-reference-locked-3d-hero.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-025-antigravity-reference-locked-3d-hero.md)
   - Đóng task ở trạng thái terminal `completed` với `verdict: REVISION_REQUIRED` theo quy chuẩn để kích hoạt watcher đánh thức Codex audit thị giác chính thức.
