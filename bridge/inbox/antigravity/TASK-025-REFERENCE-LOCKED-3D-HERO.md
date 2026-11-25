---
task_id: TASK-025-REFERENCE-LOCKED-3D-HERO
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
created_at: 2026-11-24T20:41:00+07:00
completed_at: 2026-11-24T20:54:00+07:00
request: >-
  Sau audit TASK-024, chuyển sang phương án reference-locked để ưu tiên fidelity
  thật của hero. Asset 3D procedural đã thất bại nhiều vòng; không được tiếp tục
  sửa màu/camera trên các GLB đó.
result_path: reports/TASK-025-antigravity-reference-locked-3d-hero.md
---

# TASK-025 — Reference-locked 3D hero

## Mục tiêu

Ở viewport 1226x708 và góc hero hiện tại, render phải khớp ảnh chuẩn
`assets/source/printer-hero-reference-2026-11-23.png` về silhouette, crop, vị trí,
thân titan, cửa kính, gantry, toolhead, bed, handle, console và shadow.

## Hướng mới bắt buộc

- Dùng asset đã có `website/public/hero_architectural_printer.png` làm visual
  reference chính vì đây là ảnh trong suốt đang khớp máy chuẩn, thay vì tiếp tục
  dùng mesh primitive beige từ v2/pivot.
- Tạo một WebGL/Three.js reference-locked hybrid thật: plane/mesh có alpha,
  depth shell hoặc các lớp hình học có chiều sâu, texture nằm trong scene 3D và
  có tương tác orbit giới hạn. Không dùng React `<img>` tĩnh làm kết quả cuối.
- Nếu xuất GLB thì đặt artifact mới ở
  `assets/models/raw/deltrol_p2s_reference_locked_2p5d.glb`, giữ node contract
  `enclosure`, `door`, `front_glass_door`, `printHead`, `printBed`; không ghi đè
  GLB v2/pivot.
- Nếu phương án là 2.5D, phải ghi rõ giới hạn góc nhìn trong report; không gọi
  đó là full photogrammetric 3D. Ưu tiên độ giống reference tại hero camera.

## Bằng chứng bắt buộc

- Screenshot của website/preview đang chạy đúng implementation mới:
  `reports/hero-3d-task025-reference-locked-1226x708.png`.
- Report phải có overlay/đối chiếu trực tiếp với reference và nêu rõ những vùng
  còn khác; không suy luận PASS từ RGB trung bình, node count hoặc build pass.
- Nếu có GLB mới, kiểm tra source/public hash và node contract; nếu không có,
  ghi `BLOCKED`/`REVISION_REQUIRED` với lý do chính xác.
- Đóng task terminal sau handoff: `completed` + verdict; không để `in_progress`.

## Acceptance gate

Chỉ Codex audit được quyền ghi PASS. Nếu screenshot còn rõ ràng là low-poly,
beige, sai silhouette hoặc sai vị trí so với reference thì ghi `REVISION_REQUIRED`.
