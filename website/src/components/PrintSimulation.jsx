import React, { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { Y_NOZZLE } from "./PrinterModel";

export function PrintSimulation({
  clipPlane,
  currentCutYRef,
  onToolTransformUpdate,
  onBedProgressUpdate,
  moltenLightRef,
  isPaused = false,
  playbackSpeed = 1.0,
  onProgressUpdate,
}) {
  const elapsedRef = useRef(0);

  useFrame((_, delta) => {
    if (isPaused) return;

    const baseCycle = 22.0;
    elapsedRef.current = (elapsedRef.current + delta * playbackSpeed) % baseCycle;
    const time = elapsedRef.current;

    // Timeline phases:
    // 0.0s - 3.5s: Homing / prep, bed at top, object 100% sliced (invisible)
    // 3.5s - 18.0s: Active extrusion, bed descends, revealing part layer by layer
    // 18.0s - 22.0s: Finished part presentation, toolhead parks
    let progress = 0;
    if (time < 3.5) {
      progress = 0;
    } else if (time < 18.0) {
      progress = (time - 3.5) / 14.5;
    } else {
      progress = 1.0;
    }

    const isPrinting = progress > 0 && progress < 1.0;

    // Clipping plane fixed at nozzle extrusion plane (Py <= Y_NOZZLE is visible)
    if (clipPlane) {
      clipPlane.constant = Y_NOZZLE;
    }
    if (currentCutYRef) {
      currentCutYRef.current = Y_NOZZLE;
    }

    // Toolhead CoreXY motion at fixed nozzle height
    const speed = 7.5;
    const radius = 0.032;
    const headX = isPrinting ? (radius * Math.sin(time * speed) * Math.cos(time * 2.2)) : 0;
    const headY = isPrinting ? (radius * 0.45 * Math.cos(time * speed)) : 0;

    if (onToolTransformUpdate) {
      onToolTransformUpdate([headX, headY]);
    }

    if (onBedProgressUpdate) {
      onBedProgressUpdate(progress);
    }

    // Dynamic molten extrusion tip glow (subtle, realistic ~1.5 intensity)
    if (moltenLightRef?.current) {
      moltenLightRef.current.position.set(headX, Y_NOZZLE - 0.004, headY);

      if (isPrinting) {
        moltenLightRef.current.intensity = 1.5 + 0.4 * Math.sin(time * 28);
      } else {
        moltenLightRef.current.intensity = 0.0;
      }
    }

    // Report layer telemetry to UI
    if (onProgressUpdate) {
      const currentLayer = Math.round(progress * 320);
      onProgressUpdate({
        progress,
        currentLayer,
        totalLayers: 320,
        isPrinting,
      });
    }
  });

  return null;
}
