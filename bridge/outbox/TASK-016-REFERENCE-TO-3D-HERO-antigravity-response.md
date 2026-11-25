---
task_id: TASK-016-REFERENCE-TO-3D-HERO
owner: antigravity
status: completed
verdict: REVISION_REQUIRED
completed_at: 2026-11-23T21:30:15+07:00
result_path: reports/TASK-016-antigravity-reference-to-3d-hero.md
---

# Antigravity Response — TASK-016-REFERENCE-TO-3D-HERO

Antigravity đã hoàn thành đối chiếu trực tiếp và tinh chỉnh toàn diện Hero 3D theo ảnh reference `assets/source/printer-hero-reference-2026-11-23.png`:

1. **Các cải tiến visual đã hoàn thành trong phạm vi owner**:
   - **Tư thế máy**: Khắc phục lỗi sai trục Z-up/Y-up bằng `rotation={[-Math.PI / 2, 0, 0]}`, đưa máy về tư thế đứng thẳng chuẩn xác.
   - **Vật liệu PBR Titanium**: Chuyển đổi toàn bộ vỏ máy sang màu nhôm xước champagne-bạc satin (`#8e8a84`, metallic 0.78, roughness 0.30) loại bỏ màu đen than chì và ống trắng nhựa trước đó.
   - **Kính cửa & Buồng in**: Tăng độ trong suốt kính khói (`opacity: 0.42`), hiển thị rõ ràng gantry, đầu đùn, bàn in PEI vàng và mô hình in.
   - **Ánh sáng ấm**: Thiết lập đèn spotlight và point light buồng in vàng ấm (`#ffdca8`, `#ffc882`) bám sát ảnh chụp studio reference.
   - **Ẩn cuộn nhựa thừa**: Ẩn spools to trong khoang để không gian buồng in thanh thoát như thiết kế chuẩn.
   - **Shadows & Build**: Căn chỉnh `ContactShadows` tiếp đất hoàn hảo dưới chân máy; build production thành công 100%.

2. **Kết luận theo tiêu chí bắt buộc**: `REVISION_REQUIRED`
   - *Lý do*: Theo tiêu chí 5 ("không tự ghi PASS nếu chưa đối chiếu trực tiếp với reference; nếu asset hiện tại không đủ fidelity thì ghi REVISION_REQUIRED"), phần vật liệu, ánh sáng và tư thế đã đạt, nhưng file lưới GLB gốc (`deltrol_p2s_optimized.glb`) cần Codex cập nhật lại vách kính hông to hơn và mặt nạ đáy đối xứng.
   - *Yêu cầu bổ sung cụ thể cho Codex*: Đã nêu chi tiết tại Section 3 của [reports/TASK-016-antigravity-reference-to-3d-hero.md](file:///c:/Users/PC/Downloads/3DPrinter/reports/TASK-016-antigravity-reference-to-3d-hero.md).

3. **Artifacts & Evidence**:
   - Báo cáo chi tiết: `reports/TASK-016-antigravity-reference-to-3d-hero.md`
   - Bằng chứng thực tế:
     - `reports/hero-3d-reference-1440x900.png`
     - `reports/hero-3d-reference-1280x720.png`
     - `reports/hero-3d-reference-390x844.png`
