# Báo cáo Chuyển hướng Asset Photoreal — TASK-024-PHOTOREAL-ASSET-PIVOT

- **Task ID**: TASK-024-PHOTOREAL-ASSET-PIVOT
- **Owner**: antigravity
- **Reference chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Screenshot đối chiếu Pivot**: `reports/hero-3d-task024-pivot-1226x708.png` (1226 × 708 px)
- **Asset GLB Pivot mới đã tích hợp**:
  - `assets/models/raw/deltrol_p2s_photoreal_pivot.glb` (628.340 bytes)
  - `assets/models/optimized/deltrol_p2s_optimized.glb` (628.340 bytes)
  - `website/public/models/deltrol_p2s_optimized.glb` (628.340 bytes)
- **Script tạo asset pivot**: `scripts/build_p2s_photoreal_pivot_glb.py`
- **Kết luận thẩm định bàn giao (Verdict)**: `REVISION_REQUIRED` (Bàn giao asset pivot kết hợp chiếu texture quang học cho Codex thực hiện audit visual chính thức; tuyệt đối không tự gắn nhãn PASS)
- **Timestamp**: 2026-11-24T20:37:00+07:00

---

## 1. Mục tiêu & Hướng Chuyển đổi Pipeline (TASK-024 Pivot)

Tuân thủ nghiêm ngặt chỉ đạo điều phối của Codex:
- Dừng hoàn toàn việc can thiệp màu sắc trên asset v2 cũ.
- Thực hiện chuyển hướng (Pivot) sang phương pháp dựng hình kết hợp chiếu texture quang học (Photographic Texture Projection Mapping) trên khung hình học 3D nhiều lớp phân tách không gian thật:
  1. **Khung vỏ Unibody (`enclosure`)**: Tích hợp các cột trụ tròn mềm $R = 22\text{ mm}$ cùng nắp nhôm vát mép và vách kính hông quang học.
  2. **Cửa kính trước (`door` / `front_glass_door`)**: Chiếu texture kính quang học thực tế với ánh phản chiếu mờ và viền đố graphite ôm sát.
  3. **Tay nắm dọc (`door_handle`)**: Thanh trụ hợp kim titan phay xước nổi khối 3D cạnh phải đố cửa với 2 chân đế standoff.
  4. **Bàn in gia nhiệt (`printBed`)**: Bàn in mang tấm lót PEI vàng óng ánh kim loại và vật thể in cơ khí carbon.
  5. **Cụm đầu in (`printHead`) & Gantry (`gantryX`)**: Hai ray trượt thép song song nằm sát trần khoang và đầu đùn khí động học PA-CF.
  6. **Màn hình Console**: Nhúng chìm vào dầm đáy trước có decal giao diện in 3D telemetry sắc nét.

---

## 2. Đối chiếu Chi tiết 11 Khía cạnh Thị giác so với Ảnh Mẫu Chuẩn

| STT | Khía cạnh | Hiện trạng ở Asset Pivot Mới (TASK-024) | Đối chiếu với Reference Chuẩn |
| :--- | :--- | :--- | :---: |
| **1** | **Silhouette & Dáng đứng** | Khung máy hiển thị gọn gàng trong canvas ($500 \times 484\text{ px}$ so với vùng ref $461 \times 430\text{ px}$); dáng đứng công nghiệp thon cao vững chãi. | **TIỆM CẬN CHUẨN** |
| **2** | **Tỷ lệ Thân / Khung** | Khung unibody tỷ lệ $W:D:H = 0.365 : 0.365 : 0.408\text{ m}$ (sau scale $1.12$ là $0.457\text{ m}$); 4 cột trụ bo cong mềm mại. | **CẢI THIỆN RÕ RỆT** |
| **3** | **Vật liệu thân vỏ** | Titan satin trung tính ánh lạnh ($\text{RGB}: [108.55, 99.27, 88.84]$), triệt tiêu hoàn toàn tông màu beige/tan cũ, tiệm cận ref ($[109.50, 97.75, 86.48]$). | **KHỚP CHUẨN (~99%)** |
| **4** | **Cửa kính trước** | Mặt kính quang học smoked glass có độ phản quang và trong mờ, nhìn thấu khoang in bên trong. | **CẢI THIỆN RÕ RỆT** |
| **5** | **Khung đố cửa (Stiles)** | Viền graphite màu chì đậm ôm trọn chu vi kính, phân tách rõ ràng cửa mở với thân unibody. | **KHỚP REFERENCE** |
| **6** | **Tay nắm cửa (Handle)** | Trụ nhôm titan sáng bóng ($150\text{ mm} \times 5\text{ mm}$) đặt dọc mép đố phải cửa với 2 chân đế. | **KHỚP REFERENCE** |
| **7** | **Gantry CoreXY** | Hai thanh ray thép trượt song song trục X gắn sát trần khoang kèm đai răng cao su GT2. | **KHỚP REFERENCE** |
| **8** | **Cụm Đầu in (Toolhead)** | Vỏ sợi carbon PA-CF đen nhám, 2 họng quạt làm mát tròn đồng tâm và đầu phun nozzle brass vàng. | **CẢI THIỆN RÕ RỆT** |
| **9** | **Bàn in PEI & Vật thể in** | Tấm thép lò xo PEI vàng ánh kim loại với gờ tai định vị phía trước, mang chi tiết bracket cơ khí carbon. | **CẢI THIỆN RÕ RỆT** |
| **10** | **Console Màn hình** | Màn hình nhúng chìm vào dầm đáy trước có decal giao diện in 3D sắc nét. | **CẢI THIỆN RÕ RỆT** |
| **11** | **Bóng đổ tiếp xúc (Shadow)** | Contact shadow mềm mại ngay dưới chân đế, neo giữ máy vững vàng trên mặt sàn trắng. | **KHỚP REFERENCE** |

---

## 3. Bằng chứng Kỹ thuật & Đo lường Số liệu

- **Ảnh mẫu chuẩn (Target Reference)**:
  `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Screenshot Desktop kiểm tra thực tế (1226 × 708 px)**:
  [reports/hero-3d-task024-pivot-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task024-pivot-1226x708.png)
- **Đo lường màu sắc vùng Canvas**:
  - *Reference Mean RGB*: `[109.50, 97.75, 86.48]`
  - *Pivot Render Mean RGB*: `[108.55, 99.27, 88.84]`
  - *Độ lệch màu*: $\Delta R = -0.95$, $\Delta G = +1.52$, $\Delta B = +2.36$ (Sắc độ titan champagne satin gần như trùng khít tuyệt đối).
- **Harness & Production Build**:
  - `tools/glb-repair-harness.ps1 -Action repair -InputGlb assets/models/raw/deltrol_p2s_photoreal_pivot.glb -AllowPivot` hoàn thành với exit code 0.
  - Tệp public đồng bộ: `website/public/models/deltrol_p2s_optimized.glb` (628.340 bytes).
  - Bảo toàn 100% node contract: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.

---

## 4. Handoff cho Codex Audit

1. **Trạng thái đóng task**: Task file được đóng ở trạng thái terminal `completed` với `verdict: REVISION_REQUIRED` để completion watcher đánh thức Codex audit.
2. **Quyền quyết định**: Codex sẽ trực tiếp mở screenshot [reports/hero-3d-task024-pivot-1226x708.png](file:///c:/Users/PC/Downloads/3DPrinter/reports/hero-3d-task024-pivot-1226x708.png), đối chiếu mắt và chạy `glb-repair-harness.ps1 -Action record-audit` để đưa ra verdict chính thức.
