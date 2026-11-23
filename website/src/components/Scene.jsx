import React, { Suspense, useMemo, useRef, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { ContactShadows, Environment, Html, OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import { createPhotorealMaterials } from "./Materials";
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

export function PhotorealPrinterScene() {
  const controlsRef = useRef(null);
  const moltenLightRef = useRef(null);
  const activeNozzleRef = useRef(null);
  const currentCutYRef = useRef(Y_NOZZLE);
  const userInteractingRef = useRef(false);
  const idleTimerRef = useRef(null);

  // States
  const [activePreset, setActivePreset] = useState("overview");
  const [isGlassHidden, setIsGlassHidden] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [printState, setPrintState] = useState({ progress: 0, currentLayer: 0, totalLayers: 320, isPrinting: false });
  const [printHeadPos, setPrintHeadPos] = useState([0, 0]);
  const [bedProgress, setBedProgress] = useState(0);

  // CAD Standard Clipping Plane (Normal pointing up, clips anything above Y_NOZZLE)
  const clipPlane = useMemo(() => new THREE.Plane(new THREE.Vector3(0, -1, 0), Y_NOZZLE), []);
  // High-Fidelity PBR Materials for P2S
  const materials = useMemo(() => createPhotorealMaterials(clipPlane), [clipPlane]);

  const handlePointerDown = () => {
    userInteractingRef.current = true;
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
  };

  const handlePointerUp = () => {
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
    idleTimerRef.current = setTimeout(() => {
      userInteractingRef.current = false;
    }, 3000); // 3 seconds idle resumes auto-orbit as specified
  };

  return (
    <div
      className="printer-stage-seamless"
      aria-label="Mô hình 3D máy in công nghiệp Bambu Lab P2S"
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onPointerLeave={handlePointerUp}
    >
      <Canvas
        shadows
        dpr={[1, 2]}
        camera={{ position: [0.92, 0.30, 1.45], fov: 27, near: 0.01, far: 50 }}
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
        {/* 1. Studio Lighting Rig matching P2S Reference Photography */}
        <ambientLight intensity={0.42} />
        {/* Main Studio Key Softbox */}
        <directionalLight
          castShadow
          position={[2.8, 3.6, 2.6]}
          intensity={1.5}
          color="#ffffff"
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        {/* Cool Studio Rim / Fill Light */}
        <directionalLight position={[-2.4, 1.8, 1.6]} intensity={0.75} color="#d4e8fa" />
        {/* Front-facing soft fill for door glass reflections */}
        <directionalLight position={[0, 0.5, 2.5]} intensity={0.35} color="#ffffff" />
        {/* Warm & Crisp Interior LED spots lighting up the print chamber */}
        <spotLight position={[0, 0.20, 0]} angle={0.88} penumbra={0.7} intensity={1.8} color="#fffcf5" />
        <pointLight position={[0, 0.10, 0]} intensity={0.9} color="#ffffff" distance={0.75} />
        {/* Active Nozzle Molten Tip Point Light */}
        <pointLight ref={moltenLightRef} position={[0, Y_NOZZLE, 0]} intensity={0.0} color="#ff8811" distance={0.25} />

        {/* 2. Studio Equirectangular Environment for Physical Reflections */}
        <Environment preset="studio" />

        <Suspense fallback={<LoadingCard />}>
          {/* 3. Photoreal Bambu Lab P2S 3D Model */}
          <PrinterModel
            materials={materials}
            isGlassHidden={isGlassHidden}
            printHeadPos={printHeadPos}
            bedProgress={bedProgress}
            activeNozzleRef={activeNozzleRef}
          />

          {/* 4. Real-time CoreXY Print Simulation */}
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

        {/* 5. Realistic Soft Contact Shadow under Rubber Feet */}
        <ContactShadows
          position={[0, -0.228, 0]}
          opacity={0.42}
          scale={1.38}
          blur={1.8}
          far={0.45}
          color="#0b1821"
        />

        {/* 6. Precision OrbitControls with Smooth Damping */}
        <OrbitControls
          ref={controlsRef}
          makeDefault
          enableDamping
          dampingFactor={0.06}
          enablePan={false}
          enableZoom={activePreset !== "overview"}
          minDistance={0.25}
          maxDistance={2.4}
          minPolarAngle={0.25}
          maxPolarAngle={Math.PI / 2 - 0.02}
          target={[0, -0.01, 0]}
        />

        {/* 7. Camera Director (3 Presets + Interpolation + Glass Fading) */}
        <CameraDirector
          activePreset={activePreset}
          controlsRef={controlsRef}
          userInteractingRef={userInteractingRef}
          currentCutYRef={currentCutYRef}
          onGlassVisibilityChange={setIsGlassHidden}
        />
      </Canvas>

      {/* 8. Minimalist Glassmorphic UI Controls (Top presets + Bottom playback) */}
      <PrinterControlsUI
        activePreset={activePreset}
        onSelectPreset={setActivePreset}
        isPaused={isPaused}
        onTogglePause={() => setIsPaused((p) => !p)}
        playbackSpeed={playbackSpeed}
        onChangeSpeed={setPlaybackSpeed}
        printState={printState}
      />
    </div>
  );
}
