import React, { useEffect, useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { Y_NOZZLE } from "./PrinterModel";

// Preset Camera Definitions matching P2S Reference & User Prompts
export const PRESETS = {
  overview: {
    id: "overview",
    name: "Tổng quan",
    icon: "🌐",
    pos: new THREE.Vector3(0.92, 0.30, 1.45),
    target: new THREE.Vector3(0, -0.01, 0),
    hideGlass: false,
  },
  chamber: {
    id: "chamber",
    name: "Bên trong khoang",
    icon: "🖨️",
    pos: new THREE.Vector3(0.18, 0.08, 0.44),
    target: new THREE.Vector3(0.0, 0.01, 0.0),
    hideGlass: true,
  },
  macro: {
    id: "macro",
    name: "Cận cảnh nozzle",
    icon: "🔬",
    pos: new THREE.Vector3(0.08, Y_NOZZLE + 0.038, 0.22),
    target: new THREE.Vector3(0.0, Y_NOZZLE - 0.005, 0.0),
    hideGlass: true,
  },
};

export function CameraDirector({
  activePreset,
  controlsRef,
  userInteractingRef,
  currentCutYRef,
  onGlassVisibilityChange,
}) {
  const transitionProgress = useRef(1.0); // 1 = settled, < 1 = transitioning
  const startPos = useRef(new THREE.Vector3());
  const startTarget = useRef(new THREE.Vector3());
  const endPos = useRef(new THREE.Vector3());
  const endTarget = useRef(new THREE.Vector3());
  const currentPresetRef = useRef(activePreset);
  const orbitAngleRef = useRef(0.52);

  // Trigger transition when activePreset changes
  useEffect(() => {
    const preset = PRESETS[activePreset] || PRESETS.overview;
    currentPresetRef.current = activePreset;

    if (activePreset === "overview") {
      orbitAngleRef.current = Math.atan2(preset.pos.x, preset.pos.z);
    }

    if (onGlassVisibilityChange) {
      onGlassVisibilityChange(preset.hideGlass);
    }

    if (controlsRef.current) {
      startPos.current.copy(controlsRef.current.object.position);
      startTarget.current.copy(controlsRef.current.target);

      endPos.current.copy(preset.pos);
      endTarget.current.copy(preset.target);

      transitionProgress.current = 0.0;
    }
  }, [activePreset, controlsRef, onGlassVisibilityChange]);

  useFrame((state, delta) => {
    const controls = controlsRef.current;
    if (!controls) return;

    // 1. Smooth Hermite Ease in-out (~1.5s) between camera presets
    if (transitionProgress.current < 1.0) {
      transitionProgress.current = Math.min(transitionProgress.current + delta * 0.85, 1.0);
      const p = transitionProgress.current;
      const ease = p * p * (3 - 2 * p);

      const targetPos = new THREE.Vector3().lerpVectors(startPos.current, endPos.current, ease);
      const targetLook = new THREE.Vector3().lerpVectors(startTarget.current, endTarget.current, ease);

      state.camera.position.copy(targetPos);
      controls.target.copy(targetLook);
      controls.update();
      return;
    }

    // 2. User is interacting manually (Dragging / Touching)
    if (userInteractingRef.current) {
      controls.update();
      return;
    }

    // 3. Settled State Automation
    if (currentPresetRef.current === "overview") {
      // Subtle, slow orbital drift around machine (~0.06 rad/s)
      orbitAngleRef.current += delta * 0.06;
      const r = 1.75;
      const h = 0.30;
      const x = Math.sin(orbitAngleRef.current) * r;
      const z = Math.cos(orbitAngleRef.current) * r;

      state.camera.position.lerp(new THREE.Vector3(x, h, z), 0.03);
      controls.target.lerp(PRESETS.overview.target, 0.03);
      controls.update();
    } else if (currentPresetRef.current === "macro") {
      controls.target.lerp(PRESETS.macro.target, 0.04);
      controls.update();
    } else if (currentPresetRef.current === "chamber") {
      controls.target.lerp(PRESETS.chamber.target, 0.04);
      controls.update();
    }
  });

  return null;
}
