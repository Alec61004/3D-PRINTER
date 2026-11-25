import React, { Suspense, useMemo, useRef, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { ContactShadows, Html, OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { PrinterModel, Y_NOZZLE } from "./PrinterModel";
import { CameraDirector } from "./CameraDirector";
import { PrintSimulation } from "./PrintSimulation";
import { PrinterControlsUI } from "./PrinterControlsUI";

function LoadingCard() {
  return (
    <Html center>
      <div className="scene-status" role="status">
        <span className="status-dot" />
        Đang khởi động buồng in Bambu Lab P2S...
      </div>
    </Html>
  );
}

export function PhotorealPrinterScene({ viewMode = "3d", onToggleMode }) {
  const controlsRef = useRef(null);
  const moltenLightRef = useRef(null);
  const activeNozzleRef = useRef(null);
  const currentCutYRef = useRef(Y_NOZZLE);
  const userInteractingRef = useRef(false);
  const idleTimerRef = useRef(null);

  // States
  const [activePreset, setActivePreset] = useState("overview");
  const [autoOrbitEnabled, setAutoOrbitEnabled] = useState(false);
  const [isGlassHidden, setIsGlassHidden] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [printState, setPrintState] = useState({ progress: 0, currentLayer: 0, totalLayers: 320, isPrinting: false });
  const [printHeadPos, setPrintHeadPos] = useState([0, 0]);
  const [bedProgress, setBedProgress] = useState(0);

  // CAD Standard Clipping Plane
  const clipPlane = useMemo(() => new THREE.Plane(new THREE.Vector3(0, -1, 0), Y_NOZZLE), []);
  const handleToggleAutoOrbit = () => {
    setAutoOrbitEnabled((prev) => {
      const next = !prev;
      userInteractingRef.current = !next;
      return next;
    });
  };

  const handleResetView = () => {
    setActivePreset("overview");
    if (controlsRef.current) {
      controlsRef.current.target.set(0, 0.0, 0);
      controlsRef.current.object.position.set(0.86, 0.22, 1.50);
      controlsRef.current.update();
    }
    userInteractingRef.current = true;
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
    if (autoOrbitEnabled) {
      idleTimerRef.current = setTimeout(() => {
        userInteractingRef.current = false;
      }, 2500);
    }
  };

  return (
    <div
      className="printer-stage-seamless"
      aria-label="Mô hình 3D máy in công nghiệp Bambu Lab P2S"
    >
      <Canvas
        shadows
        dpr={[1, 2]}
        camera={{ position: [0.86, 0.22, 1.50], fov: 27, near: 0.01, far: 50 }}
        gl={{ antialias: true, alpha: true, localClippingEnabled: true }}
        onCreated={({ gl, camera, scene }) => {
          gl.localClippingEnabled = true;
          window.__camera = camera;
          window.__scene = scene;
          gl.setClearColor(0x000000, 0); // Pure transparent canvas
          gl.toneMapping = THREE.ACESFilmicToneMapping;
          gl.toneMappingExposure = 1.05;
          gl.outputColorSpace = THREE.SRGBColorSpace;
        }}
      >
        {/* 1. Neutral Studio Lighting Rig (Pure crisp white, no yellow color cast on body) */}
        <ambientLight intensity={0.55} color="#ffffff" />
        {/* Main Studio Key Softbox (Neutral white highlight on aerospace titanium) */}
        <directionalLight
          castShadow
          position={[2.8, 3.6, 2.6]}
          intensity={1.65}
          color="#f9e8d5"
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        {/* Cool Studio Rim / Fill Light */}
        <directionalLight position={[-2.4, 1.8, 1.6]} intensity={0.65} color="#f3e4d6" />
        {/* Front-facing soft fill for door glass reflections */}
        <directionalLight position={[0, 0.5, 2.6]} intensity={0.35} color="#ffffff" />

        {/* 2. Warm Interior Chamber Lighting (Confined inside chamber, illuminating bed & gantry) */}
        <spotLight position={[0, 0.20, 0]} angle={0.68} penumbra={0.80} intensity={3.8} color="#ffe8d1" />
        <pointLight position={[0, 0.04, 0.02]} intensity={1.8} color="#ffcca0" distance={0.75} />
        {/* Active Nozzle Molten Tip Point Light */}
        <pointLight ref={moltenLightRef} position={[0, Y_NOZZLE, 0]} intensity={0.0} color="#ff8811" distance={0.25} />

        {/* 3. Studio Hemisphere & Ambient Lighting for Crisp Anodized Reflections */}
        <hemisphereLight skyColor="#ffffff" groundColor="#cad2da" intensity={0.60} />

        <Suspense fallback={<LoadingCard />}>
          {/* 4. Photoreal Bambu Lab P2S 3D Model */}
          <PrinterModel
            clipPlane={clipPlane}
            isGlassHidden={isGlassHidden}
            printHeadPos={printHeadPos}
            bedProgress={bedProgress}
            activeNozzleRef={activeNozzleRef}
          />

          {/* 5. Real-time CoreXY Print Simulation */}
          <PrintSimulation
            clipPlane={clipPlane}
            currentCutYRef={currentCutYRef}
            onToolTransformUpdate={setPrintHeadPos}
            onBedProgressUpdate={setBedProgress}
            moltenLightRef={moltenLightRef}
            isPaused={isPaused}
            playbackSpeed={playbackSpeed}
            onProgressUpdate={setPrintState}
          />
        </Suspense>

        {/* 6. Soft Contact Shadow under Rubber Feet (Calibrated to model base height) */}
        <ContactShadows
          position={[0, -0.270, 0]}
          opacity={0.48}
          scale={1.45}
          blur={1.9}
          far={0.50}
          color="#0b131a"
        />

        {/* 7. Precision OrbitControls with Smooth Damping (Constrained to Photoreal 2.5D Depth Cone) */}
        <OrbitControls
          ref={controlsRef}
          makeDefault
          enableDamping
          dampingFactor={0.06}
          enablePan={false}
          enableZoom={true}
          minDistance={0.7}
          maxDistance={2.4}
          minPolarAngle={Math.PI / 3}
          maxPolarAngle={Math.PI / 2 - 0.02}
          // OrbitControls azimuth is absolute around the Y axis. The hero
          // camera is ~0.52 rad, so constrain around that angle rather than
          // around zero; otherwise a small drag can expose the flat depth rig.
          minAzimuthAngle={0.20}
          maxAzimuthAngle={0.84}
          target={[0, 0.00, 0]}
          onStart={() => {
            userInteractingRef.current = true;
            if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
          }}
          onEnd={() => {
            if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
            if (autoOrbitEnabled) {
              idleTimerRef.current = setTimeout(() => {
                userInteractingRef.current = false;
              }, 3000);
            } else {
              userInteractingRef.current = true;
            }
          }}
        />

        {/* 8. Camera Director (3 Presets + Interpolation + Glass Fading) */}
        <CameraDirector
          activePreset={activePreset}
          controlsRef={controlsRef}
          userInteractingRef={userInteractingRef}
          currentCutYRef={currentCutYRef}
          onGlassVisibilityChange={setIsGlassHidden}
        />
      </Canvas>

      {/* 9. Minimalist Glassmorphic UI Controls (Top presets + Bottom navigation) */}
      <PrinterControlsUI
        activePreset={activePreset}
        onSelectPreset={setActivePreset}
        autoOrbitEnabled={autoOrbitEnabled}
        onToggleAutoOrbit={handleToggleAutoOrbit}
        onResetView={handleResetView}
        viewMode={viewMode}
        onToggleMode={onToggleMode}
      />
    </div>
  );
}
