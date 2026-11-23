import React from "react";
import { PRESETS } from "./CameraDirector";

export function PrinterControlsUI({
  activePreset,
  onSelectPreset,
  isPaused,
  onTogglePause,
  playbackSpeed,
  onChangeSpeed,
  printState,
}) {
  const { progress = 0, currentLayer = 0, totalLayers = 320, isPrinting = false } = printState || {};
  const percent = Math.round(progress * 100);

  return (
    <div className="printer-ui-overlay" aria-label="Bộ điều khiển 3D máy in Deltrol">
      {/* 1. Top Preset Camera Buttons */}
      <div className="preset-bar">
        {Object.values(PRESETS).map((preset) => {
          const isActive = activePreset === preset.id;
          return (
            <button
              key={preset.id}
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

      {/* 2. Bottom Interactive Printing Telemetry & Speed Bar */}
      <div className="playback-bar">
        <div className="playback-left">
          <button
            className="play-btn"
            onClick={onTogglePause}
            title={isPaused ? "Tiếp tục in" : "Tạm dừng"}
          >
            {isPaused ? "▶ Tiếp tục" : "⏸ Tạm dừng"}
          </button>

          <div className="speed-pills">
            {[1, 2, 5].map((s) => (
              <button
                key={s}
                className={`speed-btn ${playbackSpeed === s ? "active" : ""}`}
                onClick={() => onChangeSpeed(s)}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>

        <div className="playback-status">
          <span className={`status-dot ${isPrinting ? "printing" : ""}`} />
          <span className="status-label">
            {progress <= 0
              ? "Bàn in sẵn sàng (Z = 0)"
              : progress >= 1.0
              ? "Hoàn tất 100% phôi PA-CF"
              : `Lớp ${currentLayer} / ${totalLayers} (${percent}%)`}
          </span>
        </div>
      </div>
    </div>
  );
}
