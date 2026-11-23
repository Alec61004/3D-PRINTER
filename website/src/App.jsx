import React, { useState } from "react";
import { StaticPhotorealPrinter } from "./components/StaticPhotorealPrinter";
import "./styles.css";

export default function App() {
  const [activeNav, setActiveNav] = useState("materials");

  return (
    <div className="app-shell" id="top">
      {/* 1. Topline Utility Bar */}
      <div className="topline">
        <span>DELTROL · 3D PRINTING SOLUTIONS</span>
        <span>KHÁM PHÁ <b>·</b> SO SÁNH <b>·</b> LỰA CHỌN</span>
      </div>

      {/* 2. Navigation Header (Height ~80px) */}
      <header className="head">
        <a className="logo" href="#top" aria-label="Deltrol Controls">
          <img 
            src="/deltrol_logo.webp" 
            alt="Deltrol Controls" 
            onError={(e) => { e.currentTarget.src = "/logo.svg"; }}
          />
        </a>

        <nav className="nav" aria-label="Chính">
          <a 
            className={activeNav === "materials" ? "active" : ""} 
            href="#materials" 
            onClick={() => setActiveNav("materials")}
          >
            Vật liệu
          </a>
          <a 
            className={activeNav === "technology" ? "active" : ""} 
            href="#technology" 
            onClick={() => setActiveNav("technology")}
          >
            Công nghệ
          </a>
          <a 
            className={activeNav === "market" ? "active" : ""} 
            href="#market" 
            onClick={() => setActiveNav("market")}
          >
            Thị trường
          </a>
          <a 
            className={activeNav === "compare" ? "active" : ""} 
            href="#compare" 
            onClick={() => setActiveNav("compare")}
          >
            Lựa chọn
          </a>
        </nav>

        <a className="head-cta" href="#compare">
          So sánh máy <span>↗</span>
        </a>
      </header>

      {/* 3. Hero Section (2-Column Grid ~55% / 45%) */}
      <section className="hero">
        {/* Left Column: Copy */}
        <div className="copy">
          <div className="eyebrow">— GIẢI PHÁP LỰA CHỌN MÁY IN 3D</div>
          <h1>
            Lựa chọn <em>máy in 3D</em><br />
            cho nhà máy của bạn.
          </h1>
          <p className="lead">
            Khám phá các công nghệ in 3D, vật liệu phổ biến và những mẫu máy dành cho sản xuất, chế tạo mẫu và đồ gá trong nhà máy. So sánh thông số, chi phí và khả năng hỗ trợ để lựa chọn thiết bị phù hợp với nhu cầu thực tế.
          </p>
          <div className="buttons">
            <a href="#materials" className="btn-primary">
              Khám phá giải pháp
            </a>
            <a href="#compare" className="btn-secondary">
              So sánh các mẫu máy <span>→</span>
            </a>
          </div>
          <div className="micro">
            <span>04 nhóm nội dung</span>
            <span>Thông tin có dẫn nguồn</span>
            <span>Cập nhật 19/11/2026</span>
          </div>
        </div>

        {/* Right Column: Static Photoreal Industrial 3D Printer (Phase 1) */}
        <StaticPhotorealPrinter />
      </section>

      {/* 4. 3-Column Stats Strip below Hero */}
      <section className="stats">
        <div className="stat-item">
          <span className="stat-label">NGÂN SÁCH THAM KHẢO / MÁY</span>
          <span className="stat-value">2.000–3.000 USD</span>
          <span className="stat-caption">Chưa gồm chi phí đưa về Việt Nam</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">CÔNG NGHỆ ĐANG TÌM HIỂU</span>
          <span className="stat-value">FDM / FFF</span>
          <span className="stat-caption">Đùn sợi nhựa nóng chảy</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">TỶ GIÁ QUY ĐỔI THAM KHẢO</span>
          <span className="stat-value">1 USD ≈ 25.900 ₫</span>
          <span className="stat-caption">Cần cập nhật theo ngày mua hàng</span>
        </div>
      </section>

      {/* 5. Additional Detailed Content Sections */}
      <section className="content-section" id="materials">
        <div className="section-head">
          <div className="eyebrow">— VẬT LIỆU IN CÔNG NGHIỆP</div>
          <h2>Vật liệu nhựa kỹ thuật &amp; sợi carbon gia cường</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>PA-CF (Polyamide + Carbon Fiber)</h3>
            <p>Vật liệu composite độ bền cao, chịu nhiệt và kháng va đập vượt trội, chuyên dụng cho đồ gá cơ khí và chi tiết chịu lực trong nhà máy.</p>
          </div>
          <div className="info-card">
            <h3>PETG / PETG-CF</h3>
            <p>Kháng hóa chất, độ ổn định kích thước cao, dễ in và chống ẩm tốt, phù hợp cho vỏ bảo vệ và linh kiện tự động hóa.</p>
          </div>
          <div className="info-card">
            <h3>TPU / Cao su kỹ thuật</h3>
            <p>Độ đàn hồi linh hoạt, chống mài mòn, tối ưu cho đệm chống sốc, con lăn, gioăng làm kín và tay kẹp robot.</p>
          </div>
        </div>
      </section>

      <section className="content-section" id="technology">
        <div className="section-head">
          <div className="eyebrow">— CÔNG NGHỆ &amp; CƠ CẤU VẬN HÀNH</div>
          <h2>Kiến trúc CoreXY buồng kín công nghiệp</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>Hệ chuyển động CoreXY</h3>
            <p>Đầu đùn di chuyển nhanh và nhẹ trên thanh trượt bi tuyến tính, triệt tiêu rung động và đạt tốc độ gia công lên đến 250–500 mm/s.</p>
          </div>
          <div className="info-card">
            <h3>Buồng in gia nhiệt kín</h3>
            <p>Duy trì nhiệt độ buồng ổn định 50–70°C, ngăn ngừa hiện tượng co ngót, nứt vỡ lớp in khi gia công các loại nhựa kỹ thuật cao cấp.</p>
          </div>
          <div className="info-card">
            <h3>Cân bàn tự động đa điểm</h3>
            <p>Cảm biến quét bề mặt PEI độ chính xác micromet, bù sai số tự động đảm bảo lớp bám đầu tiên hoàn hảo 100%.</p>
          </div>
        </div>
      </section>

      <section className="content-section" id="compare">
        <div className="section-head">
          <div className="eyebrow">— SO SÁNH &amp; LỰA CHỌN MÁY</div>
          <h2>Bảng phân tích thiết bị theo nhu cầu thực tế</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>Dòng Chế tạo mẫu nhanh (Prototyping)</h3>
            <p>Tối ưu chi phí đầu tư ban đầu, thời gian triển khai nhanh, phù hợp cho phòng R&amp;D kiểm tra ý tưởng trước sản xuất hàng loạt.</p>
          </div>
          <div className="info-card">
            <h3>Dòng Sản xuất đồ gá (Jig &amp; Fixture)</h3>
            <p>Độ chính xác cao, lặp lại ổn định, hỗ trợ vật liệu composite sợi carbon, thay thế trực tiếp đồ gá kim loại gia công CNC.</p>
          </div>
          <div className="info-card">
            <h3>Dòng Hoạt động liên tục 24/7</h3>
            <p>Kết cấu khung nhôm đúc nguyên khối, giám sát camera AI, tự động cảnh báo lỗi sợi nhựa và duy trì uptime nhà xưởng tối đa.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
