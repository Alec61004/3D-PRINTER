import React from "react";
import { PRESETS } from "./CameraDirector";

export function PrinterControlsUI({
  activePreset,
  onSelectPreset,
  autoOrbitEnabled = true,
  onToggleAutoOrbit,
  onResetView,
  viewMode = "3d",
  onToggleMode,
}) {
  return (
    <div className="printer-ui-overlay" aria-label="Bộ điều khiển 3D máy in Deltrol">
      {/* Top Header: Mode Switcher & Camera Angle Presets */}
      <div className="preset-bar">
        {onToggleMode && (
          <button
            type="button"
            className="preset-btn mode-switch-btn"
            onClick={onToggleMode}
            title={viewMode === "3d" ? "Quay lại chế độ Reference Fidelity chuẩn" : "Bật chế độ khám phá 3D tương tác"}
          >
            <span className="preset-icon">{viewMode === "3d" ? "📷" : "✦"}</span>
            <span className="preset-text">{viewMode === "3d" ? "Ảnh Reference" : "Khám phá 3D"}</span>
          </button>
        )}

        {onToggleMode && <span className="preset-divider" aria-hidden="true" />}

        {Object.values(PRESETS).map((preset) => {
          const isActive = activePreset === preset.id;
          return (
            <button
              key={preset.id}
              type="button"
              className={`preset-btn ${isActive ? "active" : ""}`}
              onClick={() => onSelectPreset(preset.id)}
              title={`Chuyển góc nhìn: ${preset.name}`}
            >
              <span className="preset-icon">{preset.icon}</span>
              <span className="preset-text">{preset.name}</span>
            </button>
          );
        })}
      </div>

      {/* Bottom Bar: Reset View, Auto-orbit Toggle & Interaction Telemetry */}
      <div className="playback-bar printer-bottom-bar">
        <div className="playback-left">
          {onResetView && (
            <button
              type="button"
              className="ctrl-pill-btn reset-btn"
              onClick={onResetView}
              title="Đặt lại góc nhìn mặc định 3/4"
            >
              <span className="btn-glyph">⟲</span>
              <span>Đặt lại góc</span>
            </button>
          )}

          {onToggleAutoOrbit && (
            <button
              type="button"
              className={`ctrl-pill-btn orbit-btn ${autoOrbitEnabled ? "active" : ""}`}
              onClick={onToggleAutoOrbit}
              title={autoOrbitEnabled ? "Tạm dừng tự động xoay" : "Bật tự động xoay"}
              aria-pressed={autoOrbitEnabled}
            >
              <span className="btn-glyph">{autoOrbitEnabled ? "⏸" : "⟳"}</span>
              <span>{autoOrbitEnabled ? "Tự xoay: Bật" : "Tự xoay: Tắt"}</span>
            </button>
          )}
        </div>

        <div className="playback-status">
          <span className="status-dot printing" />
          <span className="status-label">Kéo chuột hoặc vuốt để khám phá mô hình 3D</span>
        </div>
      </div>
    </div>
  );
}
