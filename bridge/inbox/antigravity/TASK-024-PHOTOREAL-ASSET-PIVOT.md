---
task_id: TASK-024-PHOTOREAL-ASSET-PIVOT
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T20:32:00+07:00
completed_at: 2026-11-24T20:38:00+07:00
request: >-
  Tiếp tục vòng lặp visual của Deltrol 3D printer sau audit TASK-023.
  TASK-023 có GLB kỹ thuật hợp lệ nhưng render vẫn là low-poly/beige và không
  đạt reference photoreal. Đây là pivot sau chuỗi revision không cải thiện;
  không tiếp tục vá material/camera trên cùng asset v2.
result_path: reports/TASK-024-antigravity-photoreal-asset-pivot.md
---

# TASK-024 — Photoreal asset pivot

## Mục tiêu bắt buộc

Tạo một asset/render 3D mới nhìn sát ảnh chuẩn `assets/source/printer-hero-reference-2026-11-23.png`
ở viewport 1226x708, đúng góc front-right 3/4 và đúng vị trí máy trong hero.
Mục tiêu là silhouette và bề mặt photoreal trước; không coi build/load/rotate là đạt.

## Hướng xử lý

- Bỏ asset procedural/low-poly v2 hiện tại; không tiếp tục chỉnh màu để che sai
  hình học.
- Dùng một mesh/asset photoreal thật từ pipeline khác (Blender/equivalent,
  image-to-3D hoặc asset miễn phí phù hợp), rồi xuất GLB thật cho Three.js.
- Nếu không thể có mesh photoreal đủ fidelity trong lượt này, ghi BLOCKED với
  blocker cụ thể và tạo phương án 2.5D depth-layer chỉ như fallback có nhãn;
  không giả lập PASS.
- Giữ tương tác 3D và node contract tối thiểu:
  `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`.
- Không dùng ảnh phẳng làm kết quả cuối nếu vẫn tuyên bố 3D; ảnh chỉ được dùng
  làm reference/placeholder hoặc fallback rõ ràng.

## Bằng chứng bắt buộc

- Ghi đè/integrate artifact mới vào đường dẫn ổn định sau khi kiểm tra quyền sở hữu:
  `assets/models/raw/deltrol_p2s_photoreal_pivot.glb` và để harness tạo bản
  optimized/public.
- Chụp screenshot mới đúng 1226x708 của website đang load chính asset mới:
  `reports/hero-3d-task024-pivot-1226x708.png`.
- Report phải so sánh trực tiếp với reference về silhouette, tỷ lệ, vật liệu,
  kính, cửa, handle, gantry, toolhead, bed, console và shadow.
- Sau khi ghi report và outbox, đóng task ở trạng thái terminal (`completed` với
  `verdict: REVISION_REQUIRED`/`BLOCKED`, hoặc `PASS` chỉ khi đã thật sự đạt).
  Không để `in_progress` sau handoff vì watcher chỉ đánh thức Codex ở terminal state.

## Acceptance gate

Chỉ Codex audit mới được quyết định PASS. Nếu screenshot còn khác rõ về silhouette
hoặc hình học chính, ghi `REVISION_REQUIRED`; không đánh tráo bằng số RGB trung bình
hoặc build thành công.
