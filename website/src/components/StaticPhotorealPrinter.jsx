import React from "react";

export function StaticPhotorealPrinter() {
  return (
    <div
      className="hero-printer-stage"
      aria-label="Hình ảnh sản phẩm máy in 3D công nghiệp Deltrol CoreXY"
    >
      <div className="editorial-printer-frame">
        <picture>
          <source srcSet="/hero_architectural_printer.webp" type="image/webp" />
          <img
            src="/hero_architectural_printer.png"
            alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY trong không gian kiến trúc tối giản"
            className="editorial-printer-img"
            width="820"
            height="685"
            loading="eager"
            decoding="async"
          />
        </picture>
        <div className="editorial-badge">
          <span className="badge-dot" aria-hidden="true"></span>
          <span>Deltrol Industrial Series · CoreXY</span>
        </div>
      </div>
    </div>
  );
}
