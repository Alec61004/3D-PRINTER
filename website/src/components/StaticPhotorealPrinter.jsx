import React, { useState } from "react";
import { PhotorealPrinterScene } from "./Scene";
import { PrinterControlsUI } from "./PrinterControlsUI";

class ModelErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.warn("3D Model Render Error Caught, falling back to photoreal baseline with full UI controls:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="hero-printer-stage" aria-label="Khu vực hiển thị 3D máy in Deltrol (Chế độ 3D Single-View Depth)">
          <div className="printer-direct-wrap">
            <picture>
              <source srcSet="/printer-reference-locked.png" type="image/png" />
              <img
                src="/printer-reference-locked.png"
                alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY"
                className="printer-direct-img"
                width="560"
                height="480"
                loading="eager"
                decoding="async"
              />
            </picture>
          </div>
          <PrinterControlsUI
            activePreset="overview"
            onSelectPreset={() => {}}
            autoOrbitEnabled={false}
            onToggleAutoOrbit={() => {}}
            onResetView={() => {}}
            viewMode="3d"
            onToggleMode={this.props.onToggleMode}
          />
        </div>
      );
    }
    return this.props.children;
  }
}

export function StaticPhotorealPrinter() {
  const initialMode = typeof window !== "undefined" && new URLSearchParams(window.location.search).get("mode") === "3d" ? "3d" : "fidelity";
  const [viewMode, setViewMode] = useState(initialMode);

  if (viewMode === "fidelity" || viewMode === "static") {
    return (
      <div
        className="hero-printer-stage"
        aria-label="Máy in 3D công nghiệp buồng kín Deltrol CoreXY (Reference Fidelity Mode)"
      >
        <div className="printer-direct-wrap">
          <picture>
            <source srcSet="/printer-reference-locked.png" type="image/png" />
            <img
              src="/printer-reference-locked.png"
              alt="Máy in 3D công nghiệp buồng kín Deltrol CoreXY"
              className="printer-direct-img"
              width="560"
              height="480"
              loading="eager"
              decoding="async"
            />
          </picture>
        </div>

        {/* Mode Switcher to 3D Exploration */}
        <div className="static-mode-bar" aria-label="Chuyển chế độ xem">
          <button
            type="button"
            className="ctrl-pill-btn mode-activate-btn"
            onClick={() => setViewMode("3d")}
            title="Kích hoạt chế độ khám phá 3D tương tác"
          >
            <span className="btn-glyph">✦</span>
            <span>Khám phá 3D tương tác</span>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="hero-printer-stage" aria-label="Khu vực hiển thị 3D máy in Deltrol (3D Exploration Mode)">
      <ModelErrorBoundary onToggleMode={() => setViewMode("fidelity")}>
        <PhotorealPrinterScene
          viewMode={viewMode}
          onToggleMode={() => setViewMode("fidelity")}
        />
      </ModelErrorBoundary>
    </div>
  );
}
