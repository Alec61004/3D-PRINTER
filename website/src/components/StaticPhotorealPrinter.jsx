import React from "react";

export function StaticPhotorealPrinter() {
  return (
    <div
      className="hero-printer-stage"
      aria-label="Hình ảnh tĩnh chụp sản phẩm máy in 3D công nghiệp Deltrol CoreXY"
    >
      <div className="printer-presentation-wrap">
        <picture>
          <source srcSet="/printer_photoreal_seamless.webp" type="image/webp" />
          <img
            src="/printer_photoreal_seamless.png"
            alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY đang in đồ gá carbon PA-CF"
            className="printer-photoreal-img"
            width="2760"
            height="2020"
            loading="eager"
            decoding="async"
          />
        </picture>
      </div>
    </div>
  );
}
