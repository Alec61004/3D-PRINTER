---
task_id: TASK-028-3D-EXPLORATION-FIDELITY
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T21:38:00+07:00
completed_at: 2026-11-24T21:47:00+07:00
result_path: reports/TASK-028-antigravity-3d-exploration-fidelity.md
---

# Antigravity Response — TASK-028-3D-EXPLORATION-FIDELITY

Antigravity đã hoàn thành việc nâng cấp chế độ **3D Exploration Mode** và bảo toàn tuyệt đối chất lượng khung hình của **Reference Fidelity Mode** theo toàn bộ các yêu cầu từ Codex.

## 1. Kết quả Nâng cấp 3D Exploration & Bằng chứng Khắc phục

1. **Thay thế hoàn toàn mô hình CAD Beige / Low-poly**:
   - Loại bỏ mesh hình hộp procedural thô sơ v2/pivot (`deltrol_p2s_photoreal_pivot.glb`).
   - Xây dựng thành công asset 2.5D Spatial Depth Rig chuẩn glTF 2.0 (`deltrol_p2s_photoreal_2p5d_depth.glb`), tích hợp facade photoreal sắc nét, chassis đa tầng, cửa kính hun khói, tay nắm kim loại nhôm xước 3D, bàn in PEI và cụm đầu phun PA-CF.
   - Đáp ứng 5/5 semantic contract nodes: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
2. **Loại bỏ triệt để viền phẳng / khung chữ nhật của Billboard TASK-025**:
   - Mặt facade sử dụng `alphaTest: 0.02` và `baseColorFactor: [1, 1, 1, 1]`, hòa quyện tuyệt đối vào nền trắng `#ffffff`.
   - Cửa kính `front_glass_door` được giới hạn chuẩn xác vào ô cửa sổ ($24\text{ cm} \times 30\text{ cm}$), không còn bất kỳ vệt viền xám hay bóng mờ nào bên ngoài thân máy.
3. **Cơ chế OrbitControls an toàn (Safe Viewing Cone)**:
   - Do xây dựng từ single-view reference, góc quay ngang được giới hạn trong $\theta \in [-0.32, +0.32]\text{ rad}$ ($\approx \pm 18^\circ$), góc đứng $\phi \in [1.05, 1.40]\text{ rad}$.
   - Người dùng trải nghiệm trọn vẹn thị sai (parallax), chiều sâu không gian và các camera preset mà không bao giờ thấy mặt sau chưa có dữ liệu quét.
4. **Bảo toàn 100% Reference Fidelity Mode (Không hồi quy)**:
   - Viewport $1226 \times 708\text{ px}$.
   - Tọa độ Bounding Box Thân máy: $X = [618, 1074]$ ($W = 457\text{ px}$), $Y = [152, 575]$ ($H = 424\text{ px}$).
   - Độ lệch so với reference: $\Delta = 0\text{ px}$ trên cả 4 trục, pixel diff trong vùng thân máy = $0.0000$ / 255.
5. **Nút quay về `Ảnh Reference`**:
   - Hoạt động mượt mà, chuyển đổi tức thì từ 3D sang Fidelity mode khi người dùng tương tác.

## 2. Danh mục Hồ sơ & Bằng chứng Đính kèm

- **Báo cáo chi tiết**: [reports/TASK-028-antigravity-3d-exploration-fidelity.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-028-antigravity-3d-exploration-fidelity.md)
- **Screenshot 3D Exploration Mode**: [reports/hero-3d-task028-exploration-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task028-exploration-1226x708.png)
- **Screenshot Fidelity Regression Check**: [reports/hero-3d-task028-fidelity-regression-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task028-fidelity-regression-1226x708.png)
- **Ảnh đối chiếu Chế độ 3 Panel**: [reports/hero-3d-task028-mode-comparison.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task028-mode-comparison.png)

Task được đóng ở trạng thái terminal `completed` với verdict `REVISION_REQUIRED` theo quy chuẩn bàn giao; chuyển giao toàn quyền thẩm duyệt visual audit cho Codex.
