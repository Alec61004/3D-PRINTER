import React from "react";

export function StaticPhotorealPrinter() {
  return (
    <div
      className="hero-printer-stage"
      aria-label="Máy in 3D công nghiệp buồng kín Deltrol CoreXY"
    >
      <div className="printer-direct-wrap">
        <picture>
          <source srcSet="/hero_architectural_printer.webp" type="image/webp" />
          <img
            src="/hero_architectural_printer.png"
            alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY"
            className="printer-direct-img"
            width="560"
            height="480"
            loading="eager"
            decoding="async"
          />
        </picture>
      </div>
    </div>
  );
}
