import React, { useEffect, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { useGLTF } from "@react-three/drei";
import * as THREE from "three";

// Shared animation contract used by PrintSimulation and CameraDirector.
export const Y_NOZZLE = 0.045;
export const Y_BED_TOP = 0.038;
export const Y_BED_BOTTOM = -0.128;
export const TOTAL_TRAVEL = Y_BED_TOP - Y_BED_BOTTOM;

const MODEL_URL = "/models/deltrol_p2s_optimized.glb";

// PBR Material Palette strictly calibrated to neutral champagne-silver aerospace finish
// Reference: assets/source/printer-hero-reference-2026-11-23.png
const TITANIUM_BODY = new THREE.Color("#aeb4ba");       // Reference neutral satin titanium
const TITANIUM_BEVEL = new THREE.Color("#d1d5da");      // Soft highlighted outer corner chamfers
const TITANIUM_HANDLE = new THREE.Color("#dbe0e6");     // Door vertical handle bar (bright silver)
const SMOKED_GLASS = new THREE.Color("#12161a");        // Optical smoked glass with subtle reflection
const DARK_CHASSIS_INTERIOR = new THREE.Color("#1a1d22"); // Clean interior rear panel
const GOLD_PEI_BED = new THREE.Color("#d8a536");        // Textured gold PEI build plate
const CARBON_FIBER_ARM = new THREE.Color("#26292f");    // Printed architectural structure
const BONE_WHITE_SUPPORT = new THREE.Color("#e2dfd8");  // Tree supports
const BRASS_HOTEND = new THREE.Color("#e2af34");        // Dual brass nozzles
const PRECISION_STEEL = new THREE.Color("#dbe0e6");     // Precision steel linear guides

function cloneMaterial(material) {
  if (Array.isArray(material)) return material.map((entry) => entry.clone());
  return material?.clone?.() || material;
}

export function PrinterModel({
  clipPlane,
  isGlassHidden = false,
  printHeadPos = [0, 0],
  bedProgress = 0,
  activeNozzleRef,
}) {
  const { scene } = useGLTF(MODEL_URL);
  const model = useMemo(() => {
    const clone = scene.clone(true);
    const index = {};

    clone.traverse((object) => {
      if (object.name) index[object.name] = object;
      if (!object.isMesh) return;

      object.castShadow = true;
      object.receiveShadow = true;
      object.material = cloneMaterial(object.material);

      const materials = Array.isArray(object.material) ? object.material : [object.material];
      for (const material of materials) {
        if (!material) continue;
        material.needsUpdate = true;

        // 0. Photoreal Facade (Preserve transparent photoreal PNG texture, zero white borders)
        if (material.name === "Photoreal_Facade_PBR" || object.name === "photoreal_facade_layer") {
          material.transparent = true;
          material.alphaTest = 0.02;
          material.depthWrite = true;
          material.roughness = 0.35;
          material.metalness = 0.15;
          material.side = THREE.DoubleSide;
        }
        // 1. Smoked Glass Panels (Door window and legacy side windows)
        else if (
          material.name === "Smoked Glass" ||
          material.name === "Smoked Optical Glass" ||
          material.name === "Smoked Door Glass" ||
          object.name === "front_glass_window" ||
          object.name === "front_glass_door" ||
          object.name === "left_glass_window" ||
          object.name === "right_glass_window" ||
          object.name === "top_roof_glass"
        ) {
          // Keep the source asset's optical texture when available; the
          // procedural fallback has no useful map and still gets the calibrated tint.
          material.color.copy(SMOKED_GLASS);
          material.transparent = true;
          material.depthWrite = false;
          material.opacity = 0.52; // Smoked optical glass: dark enough to match the reference, still showing the chamber
          material.roughness = 0.08;
          material.metalness = 0.42;
          material.map = null;
        }
        // 2. Door Handle (Distinct vertical silver handle on right stile)
        else if (object.name.startsWith("door_handle") || material.name === "Silver Handle Bar") {
          material.map = null;
          material.color.copy(TITANIUM_HANDLE);
          material.metalness = 0.92;
          material.roughness = 0.15;
        }
        // 3. New photoreal GLB material names: keep the graphite door frame
        // dark instead of letting the generic door_ exterior rule recolor it.
        else if (material.name === "Graphite Door Frame") {
          material.map = null;
          material.color.set("#25282d");
          material.metalness = 0.62;
          material.roughness = 0.24;
        }
        // Polished aluminum is used by the handle, corner caps and small
        // mechanical details in the new handoff asset.
        else if (material.name === "Polished Aluminum") {
          material.map = null;
          material.color.copy(TITANIUM_HANDLE);
          material.metalness = 0.9;
          material.roughness = 0.16;
        }
        // The generated touchscreen material already contains the correct UI
        // decal; preserve its map and only tune the optical response.
        else if (material.name === "Touchscreen UI") {
          material.roughness = 0.12;
          material.metalness = 0.55;
          material.emissive = new THREE.Color("#0a1826");
          material.emissiveIntensity = 0.35;
        }
        // 3. Exterior Titanium Unibody & Structural Frame (Neutral silver-gray, NO yellow tint)
        else if (
          object.name.startsWith("corner_post") ||
          object.name.startsWith("corner_cap") ||
          object.name === "top_rim_outer" ||
          object.name === "base_plinth" ||
          object.name === "bottom_panel" ||
          object.name === "front_top_beam" ||
          object.name.startsWith("front_bot_fascia_") ||
          object.name.startsWith("door_") ||
          object.name.startsWith("left_wall") ||
          object.name.startsWith("right_wall") ||
          material.name === "Silver Aluminum Frame" ||
          material.name === "Chamfered Corner Caps" ||
          material.name === "Titanium Satin Unibody" ||
          material.name === "Silver Enclosure" ||
          material.name === "Brushed Steel"
        ) {
          if (material.name === "Titanium Satin Unibody") material.map = null;
          material.color.copy(object.name.startsWith("corner_cap") ? TITANIUM_BEVEL : TITANIUM_BODY);
          material.metalness = 0.82;
          material.roughness = 0.28;
        }
        // 4. Print Bed & PEI Build Plate
        else if (object.name === "build_plate" || material.name === "Gold Textured PEI" || material.name === "PEI Build Plate") {
          if (!material.map) material.color.copy(GOLD_PEI_BED);
          material.metalness = 0.65;
          material.roughness = 0.35;
        }
        // 5. Printed Architectural Model on Bed
        else if (/^arm_/.test(object.name) || object.name === "printedObject" || material.name === "PA-CF Carbon Fiber" || material.name === "Printed Object") {
          if (!material.map) material.color.copy(CARBON_FIBER_ARM);
          material.metalness = 0.25;
          material.roughness = 0.38;
        }
        // 6. Tree Supports
        else if (/^tree_/.test(object.name) || object.name === "treeSupport" || material.name === "White Tree Support") {
          material.map = null;
          material.color.copy(BONE_WHITE_SUPPORT);
          material.metalness = 0.05;
          material.roughness = 0.55;
        }
        // 7. Brass Dual Nozzles
        else if (/^nozzle_/.test(object.name) || material.name === "Brass Nozzle") {
          material.map = null;
          material.color.copy(BRASS_HOTEND);
          material.metalness = 0.92;
          material.roughness = 0.18;
        }
        // 8. Ground Precision Steel Guide Rails & Lead Screws
        else if (/^(x_guide|y_guide|z_lead)/.test(object.name) || material.name === "Linear Guide Steel") {
          material.map = null;
          material.color.copy(PRECISION_STEEL);
          material.metalness = 0.96;
          material.roughness = 0.10;
        }
        // 9. Rear Panel & Interior Frame
        else if (object.name === "rear_panel" || material.name === "Chassis Matte Dark" || material.name === "Chassis Dark Gray") {
          material.map = null;
          material.color.copy(DARK_CHASSIS_INTERIOR);
          material.metalness = 0.45;
          material.roughness = 0.48;
        }
        // 10. Front Touchscreen Console
        else if (object.name === "screen_bezel") {
          material.map = null;
          material.color.set("#15181c");
          material.roughness = 0.35;
          material.metalness = 0.40;
        } else if (object.name === "screen_display") {
          material.roughness = 0.10;
          material.metalness = 0.70;
        }
      }
    });

    clone.userData.nodeIndex = index;
    return clone;
  }, [scene]);

  const nodes = model.userData.nodeIndex;
  const isPhotorealHandoff = Boolean(nodes.top_rim_outer && nodes.door_left_stile);

  // Clean layout matching reference: hide internal spools, expand side windows, position screen
  useEffect(() => {
    // 1. Hide internal spools to keep the chamber clean & spacious
    if (nodes.spools) {
      nodes.spools.visible = false;
    }

    if (isPhotorealHandoff) return;

    // Legacy layout adjustments for the original source mesh only. The
    // photoreal handoff already contains correctly placed walls, glass and UI.
    // 2. Expand side windows to full glass panel by removing bulky side wall blocking blocks
    if (nodes.right_wall_front) nodes.right_wall_front.visible = false;
    if (nodes.right_wall_rear) nodes.right_wall_rear.visible = false;
    if (nodes.right_handle) nodes.right_handle.visible = false;
    if (nodes.right_vent) nodes.right_vent.visible = false;

    if (nodes.left_wall_front) nodes.left_wall_front.visible = false;
    if (nodes.left_wall_rear) nodes.left_wall_rear.visible = false;
    if (nodes.left_handle) nodes.left_handle.visible = false;
    if (nodes.left_vent) nodes.left_vent.visible = false;

    // Scale the side glass windows to fill the entire side aperture
    if (nodes.right_glass_window) {
      nodes.right_glass_window.scale.set(1.0, 1.65, 1.05);
    }
    if (nodes.left_glass_window) {
      nodes.left_glass_window.scale.set(1.0, 1.65, 1.05);
    }

    // 3. Ergonomic angled touchscreen console centered at bottom front
    if (nodes.screen_bezel) {
      nodes.screen_bezel.position.set(0.04, -0.198, -0.185);
      nodes.screen_bezel.rotation.x = 0.35;
    }
    for (const screenNode of [nodes.screen_display, nodes.screen_surface]) {
      if (!screenNode) continue;
      screenNode.position.set(0.04, -0.207, -0.185);
      screenNode.rotation.x = 0.35;
    }
  }, [isPhotorealHandoff, nodes]);

  useEffect(() => {
    model.traverse((object) => {
      if (!object.isMesh) return;
      const materials = Array.isArray(object.material) ? object.material : [object.material];
      const isGlass = materials.some((material) => material?.name === "Smoked Glass");
      if (isGlass) object.visible = !isGlassHidden;
    });
  }, [isGlassHidden, model]);

  useEffect(() => {
    if (activeNozzleRef) activeNozzleRef.current = nodes.nozzle_active || null;
    return () => {
      if (activeNozzleRef) activeNozzleRef.current = null;
    };
  }, [activeNozzleRef, nodes]);

  useFrame(() => {
    const [headX, headZ] = printHeadPos;
    if (nodes.printHead) {
      nodes.printHead.position.x = headX;
      nodes.printHead.position.y = headZ;
    }
    // Legacy presentation offsets are not applied to the photoreal handoff;
    // its bed and printed object are already authored in the correct place.
    if (!isPhotorealHandoff) {
      if (nodes.printBed) {
        nodes.printBed.position.z = -0.04;
      }
      if (nodes.printedObject) {
        nodes.printedObject.position.z = -0.04;
      }
      if (nodes.treeSupport) {
        nodes.treeSupport.position.z = -0.04;
      }
    }
  });

  // Vertical aspect ratio enhancement: scale Z (height in local model space) by 1.12 to match reference proportions
  return (
    <primitive
      object={model}
      name="deltrol_p2s_glb"
      rotation={[-Math.PI / 2, 0, 0]}
      scale={[1.0, 1.0, 1.12]}
    />
  );
}

useGLTF.preload(MODEL_URL);
