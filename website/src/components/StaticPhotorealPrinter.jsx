import React from "react";

export function StaticPhotorealPrinter() {
  return (
    <div
      className="hero-printer-stage"
      aria-label="Hình ảnh tĩnh chụp sản phẩm máy in 3D công nghiệp Deltrol CoreXY"
    >
      <div className="printer-presentation-wrap">
        <picture>
          <source srcSet="/hero_architectural_printer.webp" type="image/webp" />
          <img
            src="/hero_architectural_printer.png"
            alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY trong không gian kiến trúc tối giản"
            className="printer-photoreal-img"
            width="1024"
            height="764"
            loading="eager"
            decoding="async"
          />
        </picture>
      </div>
    </div>
  );
}
