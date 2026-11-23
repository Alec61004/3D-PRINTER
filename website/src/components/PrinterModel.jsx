import React, { useMemo } from "react";
import { RoundedBox } from "@react-three/drei";
import * as THREE from "three";

// Bambu Lab P2S Physical Travel Bounds:
// Nozzle tip sits at fixed printing plane: Y = 0.045.
// Bed starts at top (layer 0): Y = 0.038 (just below nozzle tip).
// Bed lowers to bottom at completion (100%): Y = -0.128.
export const Y_NOZZLE = 0.045;
export const Y_BED_TOP = 0.038;
export const Y_BED_BOTTOM = -0.128;
export const TOTAL_TRAVEL = Y_BED_TOP - Y_BED_BOTTOM; // 0.166m

export function PrinterModel({
  materials,
  isGlassHidden = false,
  printHeadPos = [0, 0, 0],
  bedProgress = 0,
  activeNozzleRef,
}) {
  const [headX, headY] = printHeadPos;

  // In Bambu CoreXY, gantry stays at top; bed drops as layers accumulate
  const bedY = Y_BED_TOP - bedProgress * TOTAL_TRAVEL;

  // Generate cable chain link positions arching from right-rear to toolhead
  const chainLinks = useMemo(() => {
    const links = [];
    const count = 12;
    const startX = 0.135;
    const startZ = -0.060;
    const endX = headX + 0.018;
    const endZ = headY - 0.020;

    for (let i = 0; i <= count; i++) {
      const t = i / count;
      // Hermite bezier curve with natural cable arc
      const cx = (1 - t) * startX + t * endX + Math.sin(t * Math.PI) * 0.035;
      const cz = (1 - t) * startZ + t * endZ - Math.sin(t * Math.PI) * 0.020;
      const cy = 0.092 + Math.sin(t * Math.PI) * 0.015;
      links.push([cx, cy, cz]);
    }
    return links;
  }, [headX, headY]);

  return (
    <group name="p2s_printer_root">
      {/* ===================================================================
          1. UNIBODY ENCLOSURE (Satin Anodized Aluminum + Rounded Pillars)
          =================================================================== */}
      <group name="chassis_frame">
        {/* 4 Iconic Vertical Rounded Corner Pillars (16mm radius curvature) */}
        {[-0.170, 0.170].map((x) =>
          [-0.170, 0.170].map((z) => (
            <RoundedBox
              key={`pillar_${x}_${z}`}
              args={[0.044, 0.418, 0.044]}
              radius={0.016}
              smoothness={5}
              position={[x, 0.0, z]}
              material={materials.chassis}
            />
          ))
        )}

        {/* Front Top Header Beam */}
        <RoundedBox
          args={[0.340, 0.046, 0.028]}
          radius={0.006}
          smoothness={4}
          position={[0, 0.188, 0.174]}
          material={materials.chassis}
        />

        {/* Rear Top Beam */}
        <RoundedBox
          args={[0.340, 0.046, 0.028]}
          radius={0.006}
          smoothness={4}
          position={[0, 0.188, -0.174]}
          material={materials.chassis}
        />

        {/* Left & Right Top Beams */}
        <RoundedBox
          args={[0.028, 0.046, 0.340]}
          radius={0.006}
          smoothness={4}
          position={[-0.174, 0.188, 0]}
          material={materials.chassis}
        />
        <RoundedBox
          args={[0.028, 0.046, 0.340]}
          radius={0.006}
          smoothness={4}
          position={[0.174, 0.188, 0]}
          material={materials.chassis}
        />

        {/* Top Tempered Glass Lid (Resting flush in top rim) */}
        {!isGlassHidden && (
          <RoundedBox
            args={[0.334, 0.006, 0.334]}
            radius={0.002}
            smoothness={2}
            position={[0, 0.210, 0]}
            material={materials.glass}
          />
        )}

        {/* Bottom Perimeter Sill & Base Plinth */}
        <RoundedBox
          args={[0.340, 0.032, 0.028]}
          radius={0.005}
          smoothness={3}
          position={[0, -0.194, 0.174]}
          material={materials.chassis}
        />
        <RoundedBox
          args={[0.372, 0.020, 0.372]}
          radius={0.008}
          smoothness={4}
          position={[0, -0.210, 0]}
          material={materials.chassis}
        />

        {/* Chamber Interior Dark Floor */}
        <mesh position={[0, -0.198, 0]} material={materials.chamberInterior}>
          <boxGeometry args={[0.330, 0.006, 0.330]} />
        </mesh>

        {/* 4 Rubber Base Feet */}
        {[-0.155, 0.155].map((x) =>
          [-0.155, 0.155].map((z) => (
            <mesh key={`foot_${x}_${z}`} position={[x, -0.224, z]} material={materials.rubber}>
              <cylinderGeometry args={[0.016, 0.016, 0.008, 20]} />
            </mesh>
          ))
        )}

        {/* Bambu P2S Angled Touchscreen Console at TOP-LEFT (Iconic layout) */}
        <group position={[-0.096, 0.188, 0.186]} rotation={[-0.28, 0, 0]}>
          {/* Beveled Screen Housing */}
          <RoundedBox
            args={[0.096, 0.052, 0.014]}
            radius={0.004}
            smoothness={4}
            position={[0, 0, 0]}
            material={materials.darkTrim}
          />
          {/* High-Resolution Color Screen Display */}
          <mesh position={[0, 0, 0.008]} material={materials.screen}>
            <planeGeometry args={[0.088, 0.044]} />
          </mesh>
        </group>

        {/* Overhead Crisp Neutral-White LED Strip Bar (~4000K) */}
        <mesh position={[0, 0.178, 0.152]} material={materials.ledLight}>
          <boxGeometry args={[0.310, 0.006, 0.012]} />
        </mesh>
        <mesh position={[-0.152, 0.178, 0]} material={materials.ledLight}>
          <boxGeometry args={[0.012, 0.006, 0.280]} />
        </mesh>
        <mesh position={[0.152, 0.178, 0]} material={materials.ledLight}>
          <boxGeometry args={[0.012, 0.006, 0.280]} />
        </mesh>

        {/* Rear Wall Panel with Stepper Motor Mounts */}
        <mesh position={[0, -0.008, -0.174]} material={materials.chamberInterior}>
          <boxGeometry args={[0.314, 0.354, 0.010]} />
        </mesh>
      </group>

      {/* ===================================================================
          2. FRONT GLASS DOOR & SIDE VIEWING WINDOWS
          =================================================================== */}
      <group name="glazing_and_doors">
        {/* Front Tempered Glass Door with Slim Perimeter Gasket */}
        {!isGlassHidden && (
          <group position={[0, -0.008, 0.178]}>
            {/* Hollow Rubber Gasket Frame (Left & Right Stiles, Top & Bottom Rails) */}
            <mesh position={[-0.148, 0, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.010, 0.342, 0.006]} />
            </mesh>
            <mesh position={[0.148, 0, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.010, 0.342, 0.006]} />
            </mesh>
            <mesh position={[0, 0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.286, 0.010, 0.006]} />
            </mesh>
            <mesh position={[0, -0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.286, 0.010, 0.006]} />
            </mesh>

            {/* Clear physical glass pane */}
            <RoundedBox
              args={[0.292, 0.330, 0.004]}
              radius={0.002}
              smoothness={2}
              position={[0, 0, 0.001]}
              material={materials.glass}
            />

            {/* Sleek Aluminum Door Handle on Right Edge */}
            <group position={[0.138, -0.010, 0.010]}>
              <mesh material={materials.polishedAluminum}>
                <cylinderGeometry args={[0.005, 0.005, 0.054, 16]} />
              </mesh>
            </group>
          </group>
        )}

        {/* Right Side Glass Window with Perimeter Trim */}
        {!isGlassHidden && (
          <group position={[0.178, -0.008, 0]}>
            <mesh position={[0, 0, -0.148]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.342, 0.010]} />
            </mesh>
            <mesh position={[0, 0, 0.148]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.342, 0.010]} />
            </mesh>
            <mesh position={[0, 0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.010, 0.286]} />
            </mesh>
            <mesh position={[0, -0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.010, 0.286]} />
            </mesh>
            <RoundedBox
              args={[0.004, 0.330, 0.292]}
              radius={0.002}
              smoothness={2}
              material={materials.glass}
            />
          </group>
        )}

        {/* Left Side Glass Window */}
        {!isGlassHidden && (
          <group position={[-0.178, -0.008, 0]}>
            <mesh position={[0, 0, -0.148]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.342, 0.010]} />
            </mesh>
            <mesh position={[0, 0, 0.148]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.342, 0.010]} />
            </mesh>
            <mesh position={[0, 0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.010, 0.286]} />
            </mesh>
            <mesh position={[0, -0.166, 0]} material={materials.darkTrim}>
              <boxGeometry args={[0.006, 0.010, 0.286]} />
            </mesh>
            <RoundedBox
              args={[0.004, 0.330, 0.292]}
              radius={0.002}
              smoothness={2}
              material={materials.glass}
            />
          </group>
        )}
      </group>

      {/* ===================================================================
          3. Z-AXIS MECHANISM (Precision Leadscrews & Linear Guide Rods)
          =================================================================== */}
      <group name="z_axis_guides">
        {/* Front Dual Stainless Steel Linear Rods */}
        {[-0.125, 0.125].map((x) => (
          <mesh key={`z_rod_${x}`} position={[x, -0.008, 0.085]} material={materials.steelRails}>
            <cylinderGeometry args={[0.005, 0.005, 0.370, 20]} />
          </mesh>
        ))}

        {/* Front Dual Precision Threaded Leadscrews */}
        {[-0.125, 0.125].map((x) => (
          <mesh key={`z_screw_${x}`} position={[x, -0.008, 0.055]} material={materials.leadScrew}>
            <cylinderGeometry args={[0.004, 0.004, 0.370, 20]} />
          </mesh>
        ))}

        {/* Rear Central Leadscrew */}
        <mesh position={[0, -0.008, -0.130]} material={materials.leadScrew}>
          <cylinderGeometry args={[0.004, 0.004, 0.370, 20]} />
        </mesh>
      </group>

      {/* ===================================================================
          4. COREXY GANTRY ASSEMBLY (Fixed at top Y ≈ 0.078)
          =================================================================== */}
      <group name="corexy_gantry">
        {/* Dual Cylindrical X Steel Guide Rods */}
        <mesh position={[0, 0.084, headY - 0.012]} rotation={[0, 0, Math.PI / 2]} material={materials.steelRails}>
          <cylinderGeometry args={[0.005, 0.005, 0.285, 20]} />
        </mesh>
        <mesh position={[0, 0.072, headY + 0.012]} rotation={[0, 0, Math.PI / 2]} material={materials.steelRails}>
          <cylinderGeometry args={[0.005, 0.005, 0.285, 20]} />
        </mesh>

        {/* Dual Y-Axis Steel Linear Rods (Left & Right) */}
        <mesh position={[-0.142, 0.078, 0]} rotation={[Math.PI / 2, 0, 0]} material={materials.steelRails}>
          <cylinderGeometry args={[0.005, 0.005, 0.270, 20]} />
        </mesh>
        <mesh position={[0.142, 0.078, 0]} rotation={[Math.PI / 2, 0, 0]} material={materials.steelRails}>
          <cylinderGeometry args={[0.005, 0.005, 0.270, 20]} />
        </mesh>

        {/* Left & Right Y Gantry Carriages (Moving along Y) */}
        <RoundedBox
          args={[0.024, 0.034, 0.046]}
          radius={0.004}
          smoothness={3}
          position={[-0.142, 0.078, headY]}
          material={materials.chassis}
        />
        <RoundedBox
          args={[0.024, 0.034, 0.046]}
          radius={0.004}
          smoothness={3}
          position={[0.142, 0.078, headY]}
          material={materials.chassis}
        />

        {/* GT2 Rubber Belts */}
        <mesh position={[0, 0.090, headY - 0.020]} material={materials.rubber}>
          <boxGeometry args={[0.290, 0.003, 0.003]} />
        </mesh>

        {/* Articulated Cable Drag Chain (Arching from right-rear to toolhead) */}
        {chainLinks.map(([cx, cy, cz], idx) => (
          <RoundedBox
            key={`chain_link_${idx}`}
            args={[0.012, 0.008, 0.016]}
            radius={0.002}
            smoothness={2}
            position={[cx, cy, cz]}
            material={materials.cableChain}
          />
        ))}
      </group>

      {/* ===================================================================
          5. BAMBU P2S TOOLHEAD (Extruder, Center Circular Fan, Brass Nozzle)
          =================================================================== */}
      <group name="p2s_toolhead" position={[headX, 0.078, headY]}>
        {/* Main Extruder Shroud (Satin Silver-Gray Aluminum) */}
        <RoundedBox
          args={[0.054, 0.062, 0.048]}
          radius={0.006}
          smoothness={4}
          position={[0, -0.010, 0]}
          material={materials.chassis}
        />

        {/* Center Circular Cooling Fan Duct (P2S Core Identity) */}
        <group position={[0, -0.008, 0.025]} rotation={[Math.PI / 2, 0, 0]}>
          {/* Circular outer bezel */}
          <mesh material={materials.darkTrim}>
            <cylinderGeometry args={[0.015, 0.015, 0.003, 24]} />
          </mesh>
          {/* Circular inner intake blades */}
          <mesh position={[0, 0.001, 0]} material={materials.rubber}>
            <cylinderGeometry args={[0.012, 0.012, 0.002, 16]} />
          </mesh>
          {/* Polished center spinner hub */}
          <mesh position={[0, 0.002, 0]} material={materials.polishedAluminum}>
            <cylinderGeometry args={[0.004, 0.004, 0.003, 16]} />
          </mesh>
        </group>

        {/* Aluminum Hotend Heatblock */}
        <mesh position={[0, -0.040, 0]} material={materials.polishedAluminum}>
          <boxGeometry args={[0.020, 0.010, 0.016]} />
        </mesh>

        {/* Machined Brass Extrusion Nozzle */}
        <group ref={activeNozzleRef} position={[0, -0.046, 0]}>
          <mesh material={materials.brassNozzle}>
            <coneGeometry args={[0.004, 0.008, 16]} />
          </mesh>
        </group>

        {/* Dual PTFE Bowden Guide Tubes (Curving upwards and back) */}
        {[-0.008, 0.008].map((tx) => (
          <group key={`ptfe_${tx}`} position={[tx, 0.024, -0.008]}>
            <mesh material={materials.ptfe}>
              <cylinderGeometry args={[0.002, 0.002, 0.032, 12]} />
            </mesh>
          </group>
        ))}
      </group>

      {/* ===================================================================
          6. CANTILEVER BED ASSEMBLY (Moves vertically along Y as bedProgress updates)
          =================================================================== */}
      <group name="p2s_print_bed" position={[0, bedY, 0]}>
        {/* Cantilever Lower Carriage Bracket */}
        <RoundedBox
          args={[0.230, 0.016, 0.160]}
          radius={0.004}
          smoothness={3}
          position={[0, -0.016, -0.020]}
          material={materials.darkTrim}
        />

        {/* Heated Bed Aluminum Baseplate */}
        <RoundedBox
          args={[0.245, 0.012, 0.245]}
          radius={0.003}
          smoothness={3}
          position={[0, -0.006, 0]}
          material={materials.darkTrim}
        />

        {/* Bambu Textured Black Spring Steel PEI Build Plate */}
        <mesh position={[0, 0.001, 0]} material={materials.blackPei}>
          <boxGeometry args={[0.240, 0.002, 0.240]} />
        </mesh>

        {/* Front Ergonomic Pull Tab */}
        <RoundedBox
          args={[0.050, 0.002, 0.016]}
          radius={0.002}
          smoothness={2}
          position={[0, 0.001, 0.126]}
          material={materials.darkTrim}
        />

        {/* =================================================================
            7. PRINTED OBJECT & TREE SUPPORTS (Mounted directly on build plate)
            As bed drops down, object moves down with it and is sliced cleanly
            by the fixed clipping plane at the nozzle height!
            ================================================================= */}
        <group name="printedObject" position={[0, 0.002, 0]}>
          {/* Industrial Robot Arm Spar Part */}
          <group position={[0, 0.045, 0]}>
            {/* Base Pivot Foot */}
            <mesh position={[0, -0.035, 0]} material={materials.printedPart}>
              <cylinderGeometry args={[0.022, 0.024, 0.020, 24]} />
            </mesh>
            <mesh position={[0, -0.035, 0]} material={materials.chamberInterior}>
              <cylinderGeometry args={[0.010, 0.010, 0.022, 16]} />
            </mesh>

            {/* Central Truss Spar with Beveled Cutout */}
            <mesh position={[0, 0.008, 0]} material={materials.printedPart}>
              <boxGeometry args={[0.032, 0.075, 0.032]} />
            </mesh>
            <mesh position={[0, 0.008, 0]} material={materials.chamberInterior}>
              <boxGeometry args={[0.016, 0.045, 0.036]} />
            </mesh>

            {/* Top Swivel Ear */}
            <mesh position={[0, 0.048, 0]} rotation={[0, 0, Math.PI / 2]} material={materials.printedPart}>
              <cylinderGeometry args={[0.018, 0.018, 0.028, 24]} />
            </mesh>
            <mesh position={[0, 0.048, 0]} rotation={[0, 0, Math.PI / 2]} material={materials.chamberInterior}>
              <cylinderGeometry args={[0.008, 0.008, 0.030, 16]} />
            </mesh>
          </group>

          {/* Organic CAD Tree Supports branching from bed */}
          <group name="treeSupport">
            {/* Left Branch */}
            <mesh position={[-0.030, 0.026, 0]} rotation={[0, 0, 0.18]} material={materials.treeSupport}>
              <cylinderGeometry args={[0.004, 0.007, 0.052, 12]} />
            </mesh>
            <mesh position={[-0.020, 0.054, 0]} rotation={[0, 0, -0.32]} material={materials.treeSupport}>
              <cylinderGeometry args={[0.003, 0.004, 0.028, 12]} />
            </mesh>

            {/* Right Branch */}
            <mesh position={[0.030, 0.026, 0]} rotation={[0, 0, -0.18]} material={materials.treeSupport}>
              <cylinderGeometry args={[0.004, 0.007, 0.052, 12]} />
            </mesh>
            <mesh position={[0.020, 0.054, 0]} rotation={[0, 0, 0.32]} material={materials.treeSupport}>
              <cylinderGeometry args={[0.003, 0.004, 0.028, 12]} />
            </mesh>
          </group>
        </group>
      </group>
    </group>
  );
}
