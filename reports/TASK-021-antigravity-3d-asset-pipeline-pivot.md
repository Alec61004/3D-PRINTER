# Báo cáo Chuyển đổi Pipeline 3D Asset — TASK-021-3D-ASSET-PIPELINE-PIVOT

- **Task ID**: TASK-021-3D-ASSET-PIPELINE-PIVOT
- **Owner**: antigravity
- **Reference chuẩn**: `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Screenshot đối chiếu hiện trạng**: `reports/hero-3d-pivot-task021-1226x708.png` (1226 × 708 px)
- **Kết luận thẩm định (Verdict)**: `REVISION_REQUIRED` (Pivot bắt buộc: Chấm dứt can thiệp CSG procedural unibody, bàn giao trọn bộ Multi-view Blueprint cho pipeline Blender/CAD của Codex)
- **Timestamp**: 2026-11-24T06:05:00+07:00

---

## 1. Quyết định Chính thức Pivot khỏi Pipeline Procedural Trimesh

Tuân thủ nghiêm ngặt quy tắc **3-Strike Rule** trong `AGENTS.md` và kết quả giám sát từ harness `tools/glb-repair-harness.ps1` (sau TASK-018, TASK-019 và TASK-020 ghi nhận `visualFailureCount: 3`, `pivotRequired: true`):

1. **Chấm dứt hoàn toàn can thiệp vào asset cũ**:
   - Dừng chỉnh sửa tệp `assets/models/raw/deltrol_p2s_unibody_pivoted.glb` và script `scripts/generate_pivoted_unibody_glb.py`.
   - Không tiếp tục vá shader, vật liệu hay tinh chỉnh thông số camera trong Three.js để che lấp khiếm khuyết hình học.
2. **Nguyên nhân kỹ thuật căn bản**:
   - Phương pháp dựng hình CSG procedural thông qua các khối hộp (box) và hình trụ (cylinder) ghép nối bằng thư viện `trimesh` đã chạm ngưỡng giới hạn toán học:
     - Không hỗ trợ độ cong tiếp tuyến G2 (G2 continuous curvature fillets) và bo góc cầu 3 chiều (spherical corner blend caps) cần thiết cho khung nhôm unibody cao cấp.
     - Thiếu độ vát mép (bevels) cơ khí trên các đố cửa và khe tiếp giáp khung-kính.
     - Không thể thể hiện chân thực cụm đầu in CoreXY khí động học, họng quạt gió tản nhiệt, xích dẫn cáp cuộn (cable drag chain), và các chi tiết dập nổi tinh xảo nếu không có UV unwrap và normal map chuyên nghiệp.

---

## 2. Lựa chọn Hướng đi Mới: Pipeline Dựng Mesh Chuyên Nghiệp (Blender / CAD)

Căn cứ theo phân định trách nhiệm tại `AGENTS.md`:
- **Codex** sở hữu quyền kỹ thuật về Blender, mesh modeling, Three.js và GLB optimization.
- **Antigravity** sở hữu visual direction, visual assets, AI generation và tài liệu đặc tả mỹ thuật.

Antigravity bàn giao trọn vẹn gói tài nguyên **Multi-view Orthographic Reference Dataset** đã được chuẩn hóa độ phân giải cao và lưu trữ sẵn sàng trong workspace tại `assets/generated/antigravity/multiview/`:

| Góc nhìn (View) | Tệp Artifact | Kích thước | Vai trò thiết kế & Thông số hình học trích xuất |
| :--- | :--- | :---: | :--- |
| **Front Elevation** | `p2s_multiview_front.jpg` | 1200 × 896 | Mặt đứng vuông góc: Tỷ lệ khung ngoài (W:H:D ~ 389 × 389 × 457 mm), vị trí bản lề cửa bên trái, đố cửa dày 20mm, vị trí trục vitme Z kép đối xứng. |
| **Right Elevation** | `p2s_multiview_right.jpg` | 1200 × 896 | Mặt hông phải: Vách kính phẳng quang học smoked glass, bán kính uốn cong của xích dẫn cáp CoreXY, vị trí gá động cơ bước. |
| **Top Plan View** | `p2s_multiview_top.jpg` | 1200 × 896 | Mặt phẳng nóc: Nắp kính cường lực phẳng trong suốt, hệ ray trượt song song trục X/Y, vị trí cụm đầu in trung tâm và ốc định vị puly. |
| **Left Elevation** | `p2s_multiview_left.jpg` | 1200 × 896 | Mặt hông trái: Độ nghiêng công thái học của màn hình cảm ứng (~15°), điểm ngàm thanh dẫn hướng trục Z bên trái. |
| **Rear Elevation** | `p2s_multiview_rear.jpg` | 1200 × 896 | Mặt sau: Lưới tổ ong thoát nhiệt quạt gió chính, các vị trí ốc gia cố khung sau, cổng dẫn ống dẫn nhựa PTFE. |
| **Perspective 3/4** | `p2s_multiview_front_right_3_4.jpg` | 1200 × 896 | Góc 3/4 tham chiếu chuẩn: Chiều sâu lòng khoang in, tỷ lệ mặt kính trước (60%) và vách kính hông (40%), hiệu ứng phản xạ highlight titan satin. |
| **Metadata & Specs** | `p2s_multiview_metadata.json` | 5.531 bytes | Toàn bộ metadata, màu sắc Hex, PBR properties, và link frame Doop liên kết. |

---

## 3. Kế hoạch Ánh xạ Node Contract Bắt buộc cho Model Mới

Bất kỳ model GLB mới nào được dựng từ Blender hoặc nhập từ nguồn CAD chất lượng cao phải bảo đảm cây phân cấp đối tượng (Scene Graph) chứa đúng các node contract sau để tương thích 100% với `tools/glb-repair-harness.ps1` và logic animation Three.js trong `website/src/components/ThreeViewer.jsx`:

```
Scene
├── enclosure          (Mesh/Group: Toàn bộ thân vỏ nhôm unibody màu titan xám bạc satin #aeb2b8, 4 trụ bo góc tròn mềm)
├── door               (Group: Cụm cửa trước quay quanh trục bản lề bên trái)
│   ├── front_glass_door  (Mesh: Mặt kính cường lực màu khói smoked glass tối màu, PBR transmission/opacity)
│   └── door_handle       (Mesh: Tay nắm dọc kim loại titan phay xước cạnh phải)
├── printHead          (Group/Mesh: Cụm đầu in CoreXY di chuyển theo trục X/Y trong Three.js animation)
└── printBed           (Group/Mesh: Bàn in gia nhiệt di chuyển theo trục Z, kèm tấm flex PEI vàng kim loại và vật thể in)
```

**Các node bổ sung được khuyến nghị để đạt photorealism tuyệt đối:**
- `right_glass_window`: Mặt kính hông phải (smoked glass).
- `left_glass_window`: Mặt kính hông trái (smoked glass).
- `top_roof_glass`: Nắp kính nóc phẳng trong suốt.
- `screen_bezel` & `screen_display`: Màn hình điều khiển nhúng chìm vào dầm đáy trước, nghiêng 15-25°.
- `gantryX`: Thanh dầm ngang mang ray trượt cho `printHead`.
- `printedObject`: Chi tiết cơ khí đang được in trên mặt bàn PEI.

---

## 4. Bằng chứng Đo lường & Đối chiếu Hiện trạng

- **Ảnh mẫu chuẩn (Target Reference)**:
  `assets/source/printer-hero-reference-2026-11-23.png` (1226 × 708 px)
- **Ảnh chụp màn hình thực tế hiện tại (Desktop Screenshot)**:
  `reports/hero-3d-pivot-task021-1226x708.png` (1226 × 708 px, chụp trực tiếp tại viewport 1226 × 708 px của Chrome DevTools).
- **Nhận định thẩm mỹ**:
  Mặc dù asset unibody procedural ở TASK-020 đã có bố cục tổng thể và màu sắc tiến gần hơn, nhưng các cạnh ghép nối hình trụ - khối hộp vẫn lộ rõ bản chất đa giác thô, các đường bo góc thiếu sự mượt mà quang học của sản phẩm đúc/dập công nghiệp thực tế. Do đó, việc chuyển đổi sang Blender là con đường duy nhất để giải quyết dứt điểm vấn đề silhouette.

---

## 5. Handoff sang Codex

1. **Trạng thái task**: Hoàn thành phần trách nhiệm của Antigravity (xác nhận pivot, đóng băng pipeline procedural cũ, cung cấp trọn gói multi-view reference và node contract).
2. **Hành động tiếp theo cho Codex**:
   - Sử dụng bộ ảnh tham chiếu trong `assets/generated/antigravity/multiview/` để dựng mesh chuẩn trong Blender (hoặc nạp asset CAD tương đương).
   - Đảm bảo export GLB giữ nguyên các node bắt buộc: `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
   - Chạy `tools/glb-repair-harness.ps1 -Action repair` để tích hợp asset mới vào website và audit visual.
