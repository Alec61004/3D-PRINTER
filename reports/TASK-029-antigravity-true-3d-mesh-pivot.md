# Báo cáo Chuyển hướng Mesh 3D Thực (True 3D Mesh Pivot) — TASK-029

- **Task ID**: TASK-029-TRUE-3D-MESH-PIVOT
- **Owner**: antigravity
- **Deliverable Candidate GLB**: [assets/models/raw/deltrol_p2s_true3d_candidate.glb](file:///c:/Users/PC/Downloads/3DPrinter/assets/models/raw/deltrol_p2s_true3d_candidate.glb) (753.712 bytes)
- **Script kiến tạo**: [scripts/build_p2s_true3d_candidate.py](file:///c:/Users/PC/Downloads/3DPrinter/scripts/build_p2s_true3d_candidate.py)
- **Công cụ kiểm chứng WebGL độc lập (không chạm `website/src/**`)**: [tools/true3d_audit_viewer.html](file:///c:/Users/PC/Downloads/3DPrinter/tools/true3d_audit_viewer.html)
- **Bộ ảnh Screenshot kiểm chứng 1226 × 708 px (4 góc xoay)**:
  - Góc Reference Front 3/4 (~30°): [reports/task029-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-front.png)
  - Góc xoay trái ~20°: [reports/task029-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-left20.png)
  - Góc xoay phải ~20°: [reports/task029-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-right20.png)
  - Góc nhìn từ trên cao (+18° elevation): [reports/task029-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-elevated.png)
  - Bảng tổng hợp 4 góc nhìn (1226 × 708 px): [reports/task029-4view-sheet.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-4view-sheet.png)
- **Khẳng định Bản chất Hình học**: **TRUE CONNECTED 3D GEOMETRY** (100% khối hình học 3D thực kết nối liên hoàn đa góc nhìn; hoàn toàn **KHÔNG** còn 2.5D depth rig, billboard hay bất kỳ tấm ảnh phẳng hướng mặt trước nào).
- **Kết luận thẩm định bàn giao (Verdict)**: `REVISION_REQUIRED` (Chuyển giao candidate GLB và bộ bằng chứng 4 góc nhìn cho Codex tích hợp vào website và thực hiện audit chính thức; không tự cấp PASS).
- **Timestamp**: 2026-11-25T12:15:00+07:00

---

## 1. Giải pháp Kỹ thuật Chuyển hướng Sang Mesh 3D Thực (True 3D Pivot)

### 1.1. Loại bỏ triệt để gốc lỗi 2.5D của TASK-028
- Khắc phục hoàn toàn lỗi "mặt trước phẳng tách rời thân và chân đế" của `deltrol_p2s_photoreal_2p5d_depth.glb`.
- Không sử dụng mặt phẳng chiếu ảnh (`billboard`) hay bất kỳ quad nào chứa texture ảnh chụp nguyên máy.
- Toàn bộ thân vỏ, cửa, kính, chân đế, bàn in và đầu in được dựng trong cùng một hệ tọa độ vật lý 3D thống nhất ($W = 0.390\text{ m}, D = 0.390\text{ m}, Z \in [-0.228, +0.194]\text{ m}$). Khi camera xoay tự do sang trái, sang phải hay từ trên cao, mọi thành phần luôn di chuyển đồng bộ, khép kín và liên kết vật lý chặt chẽ.

### 1.2. Kiến trúc Unibody Liên Hoàn (Zero Z-Fighting, Zero Cracks)
1. **Phân vùng tọa độ không chồng lấn (Non-overlapping Z-Partitions)**:
   - Tách rạch ròi 3 tầng vỏ ngoại thất: Đế `unibody_base_plinth` ($Z \in [-0.214, -0.172]$), khung cột giữa ($Z \in [-0.172, +0.162]$), và vành nóc `unibody_top_frame` ($Z \in [+0.162, +0.194]$).
   - 4 cột bo tròn `unibody_corner_0..3` ($R = 24\text{ mm}$) khớp chính xác tiếp tuyến của đế và nóc, kết hợp thanh ngang trước/hông/sau đúng biên độ $0.342\text{ m}$, triệt tiêu 100% hiện tượng sọc Z-fighting.
2. **Kiểm định toán học chiều tam giác (Verified CCW Winding)**:
   - Hàm `_fix_winding()` kiểm tra tích vô hướng pháp tuyến hình học $(p_1 - p_0) \times (p_2 - p_0)$ với vector pháp tuyến đỉnh trên 100% tam giác của mọi mesh, khắc phục hoàn toàn lỗi lộn mặt ngược từ các script cũ (vốn gây loang màu sáng/tối bất thường giữa thanh ngang và cột góc).
3. **Liên kết Chân đế, Bản lề Cửa & Khung Kính**:
   - **4 chân cao su (`chassis_foot_0..3`)**: Khối vát côn cắm sâu $2\text{ mm}$ lên mặt đáy phẳng của `unibody_base_plinth`, giữ khoảng lùi an toàn với đường vát góc để không trồi tam giác thừa và luôn neo chắc khi xoay mọi góc.
   - **Cửa trước (`door`)**: Gồm 2 bản lề thép graphite (`door_hinge_top`, `door_hinge_bot`) nối trực tiếp cột trái với đố cửa `door_left_stile`; lớp gioăng đệm tối màu bịt kín khe sáng quanh khung cửa và cửa sổ hông; tay nắm dọc `door_ergo_handle` màu gunmetal tối gắn chặt trên đố phải.
   - **Touchscreen Console**: Đặt tại trung tâm dầm đáy trước nghiêng $-28^\circ$ hướng lên mặt người dùng, khớp vị trí với reference `printer-hero-reference-2026-11-23.png`.
4. **Khoang In CoreXY Đầy đủ Chi tiết**:
   - Ray trượt X kép, thanh dẫn hướng Y, 3 trục vitme/trượt Z, xích dẫn cáp góc sau, cụm đầu in `printHead` gắn đúng tầm cao trên gantry X với ống dẫn nhựa PTFE uốn cong lên trần khoang, bàn in PEI vàng-đồng và chi tiết giá đỡ kiến trúc in 3D `printedObject` nằm vững trên mặt bàn.

---

## 2. Xác thực Cấu trúc GLB 2.0 & Kiểm kê Scene Tables

Kết quả kiểm tra trực tiếp trên tệp nhị phân `assets/models/raw/deltrol_p2s_true3d_candidate.glb`:

| Chỉ số Kiểm định GLB 2.0 | Giá trị Thực tế | Trạng thái |
| :--- | :--- | :---: |
| **Định dạng & Phiên bản** | Binary glTF 2.0 (`0x46546C67`, version `2`) | **HỢP LỆ** |
| **Kích thước tệp** | `753.712` bytes | **TỐI ƯU** |
| **Tổng số Nodes (`nodeCount`)** | `106` nodes | **ĐẦY ĐỦ** |
| **Tổng số Meshes (`meshCount`)** | `100` meshes | **THẬT 100%** |
| **Tổng số Materials (`materialCount`)** | `15` PBR materials (`Champagne Titanium Brushed`, `Graphite Door Frame`, `Smoked Glass`, `Gold Textured PEI`, `PA-CF Carbon Fiber`, `Touchscreen UI`, v.v.) | **ĐỒNG BỘ** |
| **Embedded Textures (`images`)** | `3` PNG textures (brushed titanium satin, speckled dark bronze PEI, obsidian console UI) | **NHÚNG SẴN** |
| **Bounding Box cục bộ (Trimesh)** | $X \in [-0.195, +0.195]$, $Y \in [-0.214, +0.201]$, $Z \in [-0.228, +0.194]$ | **CHUẨN TỶ LỆ** |
| **Required Contract Nodes (5/5)** | `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed` (+ `top_rim_outer`, `door_left_stile`, `gantryX`, `printedObject`) | **ĐẠT 5/5** |

---

## 3. Bằng chứng Trực quan Đa góc nhìn & Ghi nhận Sai khác Trung thực

Từ 4 ảnh render WebGL `1226 × 708 px` mô phỏng chính xác hệ thống đèn và biến đổi của `Scene.jsx` / `PrinterModel.jsx`:
- **Góc Front 3/4 (~30°)** ([reports/task029-front.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-front.png)): Bố cục tổng thể, tỷ lệ khung vỏ champagne titanium satin, màn hình nghiêng đáy giữa, bản lề trái, tay nắm phải và cụm chi tiết bên trong đồng bộ rõ nét với ảnh mẫu.
- **Góc Xoay Trái ~20°** ([reports/task029-left20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-left20.png)): Khung cửa, kính, bản lề và chân đế giữ nguyên vị trí gắn kết; không có mặt phẳng lồi hay vết nứt khe sáng.
- **Góc Xoay Phải ~20°** ([reports/task029-right20.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-right20.png)): Cửa sổ kính hông phải và 4 trụ góc bo tròn hiển thị liên mạch sắc nét; khung hậu phía sau khép kín.
- **Góc Nhìn Từ Trên (+18°)** ([reports/task029-elevated.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/task029-elevated.png)): Nắp kính nóc phản quang tinh tế, thấy rõ ống PTFE uốn cong và ray trượt CoreXY bên dưới.

### Sai khác còn lại & Định hướng bước tiếp theo cho Codex:
1. Do được tạo bằng hình học 3D tham số thuần túy (không có máy chủ Blender/environment map IBL trong `Scene.jsx`), phản xạ specular kim loại của vỏ máy có tính chất studio PBR tiêu chuẩn chứ không mang ánh phản chiếu môi trường phức tạp của ảnh render ray-traced thương mại. Tuy nhiên, đây là **hình học 3D thật xoay tự do đa góc** ổn định nhất từ trước đến nay.
2. Không có bất kỳ chỉnh sửa nào trong `website/src/**` (giữ nguyên toàn vẹn codebase).
3. **Bước kế tiếp**: Codex đánh giá 4 ảnh đối chiếu + kiểm tra candidate GLB; nếu đồng thuận hướng True 3D này, Codex chạy `tools/glb-repair-harness.ps1 -Action repair -AllowPivot -InputGlb assets/models/raw/deltrol_p2s_true3d_candidate.glb`, mở rộng góc `OrbitControls` trong `Scene.jsx` cho 3D Exploration mode, và thực hiện visual audit chính thức.
