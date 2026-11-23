import React, { Suspense, useCallback, useEffect, useRef, useState } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { ContactShadows, Html, OrbitControls, useGLTF } from "@react-three/drei";
import * as THREE from "three";
import "./styles.css";

const MODEL_URL = "/models/deltrol_p2s_optimized.glb";

// Precise geometric vertical bounds of the 3D model:
// Bed surface: Y = -0.128 (GLB Z = -0.128)
// Top finished layer: Y = +0.038 (GLB Z = +0.038)
const Y_BED = -0.128;
const Y_TOP = 0.038;
const TOTAL_HEIGHT = Y_TOP - Y_BED; // 0.166m (166mm)

function AnimatedPrinterModel({ onReady, moltenLightRef, currentCutYRef }) {
  const gltf = useGLTF(MODEL_URL);
  const elapsedRef = useRef(0);
  const baseTransformsRef = useRef(null);
  
  // CAD Standard Clipping Plane: normal (0, -1, 0) · P + constant >= 0 <=> Py <= constant
  // Constant starts below bed (-0.134) so part is 100% invisible (Z=0 empty bed)
  const clipPlaneRef = useRef(new THREE.Plane(new THREE.Vector3(0, -1, 0), Y_BED - 0.008));

  useEffect(() => {
    const scene = gltf.scene;
    scene.traverse((object) => {
      if (!object.isMesh) return;
      object.castShadow = true;
      object.receiveShadow = true;

      const isPartOrSupport =
        object.name.startsWith("arm_") ||
        object.name.startsWith("tree_") ||
        object.parent?.name === "printedObject" ||
        object.parent?.name === "treeSupport";

      const materials = Array.isArray(object.material) ? object.material : [object.material];
      materials.forEach((material) => {
        if (!material) return;
        if (material.name === "Smoked Glass") {
          material.transparent = true;
          material.opacity = 0.32;
          material.roughness = 0.08;
          material.depthWrite = false; // Smooth transparency sorting
        }
        if (isPartOrSupport) {
          material.clippingPlanes = [clipPlaneRef.current];
          material.clipShadows = true;
          material.needsUpdate = true;
        }
        material.envMapIntensity = 1.1;
      });
    });

    baseTransformsRef.current = {
      printHead: scene.getObjectByName("printHead")?.position.clone() || new THREE.Vector3(0, 0, 0),
      printBed: scene.getObjectByName("printBed")?.position.clone() || new THREE.Vector3(0, 0, 0),
      gantryX: scene.getObjectByName("gantryX")?.position.clone() || new THREE.Vector3(0, 0, 0),
      gantryY: scene.getObjectByName("gantryY")?.position.clone() || new THREE.Vector3(0, 0, 0),
    };

    if (onReady) onReady();
  }, [gltf.scene, onReady]);

  useFrame((_, delta) => {
    const base = baseTransformsRef.current;
    if (!base) return;

    const cycleDuration = 22.0;
    if (window.__forcedTime !== undefined) {
      elapsedRef.current = window.__forcedTime;
    } else {
      elapsedRef.current = (elapsedRef.current + delta) % cycleDuration;
    }
    const time = elapsedRef.current;

    // Timeline phases of printing:
    // 0.0s - 5.5s (Phase 1): Bed is 100% empty (Z = 0)
    // 5.5s - 17.5s (Phase 2 & 3): Slicing plane sweeps from Y_BED to Y_TOP (layer growth)
    // 17.5s - 22.0s (Phase 4): 100% finished part, nozzle z-hops up
    let printProgress = 0;
    if (time < 5.5) {
      printProgress = 0;
    } else if (time < 17.5) {
      printProgress = (time - 5.5) / 12.0;
    } else {
      printProgress = 1.0;
    }

    const currentCutY = (printProgress <= 0)
      ? Y_BED - 0.008 // Completely hidden below PEI bed
      : (printProgress >= 1.0)
        ? Y_TOP + 0.015 // Completely revealed
        : Y_BED + printProgress * TOTAL_HEIGHT;

    // Update clipping plane constant
    clipPlaneRef.current.constant = currentCutY;
    if (currentCutYRef) currentCutYRef.current = currentCutY;

    // Toolhead CoreXY motion at the current cutting layer
    const speed = 7.0;
    const radius = 0.032;
    const isPrinting = printProgress > 0 && printProgress < 1.0;
    
    const toolX = isPrinting ? (radius * Math.sin(time * speed) * Math.cos(time * 2.3)) : 0;
    const toolY = isPrinting ? (radius * 0.45 * Math.cos(time * speed)) : 0;
    
    // Z-lift: At printProgress=0, nozzle touches Y_BED (-0.128). As layer rises, nozzle lifts.
    // When finished, executes a 20mm Z-hop presentation lift.
    const toolZLift = (printProgress <= 0) 
      ? 0 
      : (printProgress >= 1.0)
        ? (TOTAL_HEIGHT + 0.020)
        : (currentCutY - Y_BED);

    const printHead = gltf.scene.getObjectByName("printHead");
    const gantryX = gltf.scene.getObjectByName("gantryX");
    const gantryY = gltf.scene.getObjectByName("gantryY");

    if (printHead && base.printHead) {
      // In GLB local space: z is up (maps to World Y)
      printHead.position.set(base.printHead.x + toolX, base.printHead.y + toolY, base.printHead.z + toolZLift);
    }
    if (gantryX && base.gantryX) {
      gantryX.position.set(base.gantryX.x, base.gantryX.y + toolY * 0.5, base.gantryX.z + toolZLift);
    }
    if (gantryY && base.gantryY) {
      gantryY.position.set(base.gantryY.x + toolX * 0.15, base.gantryY.y, base.gantryY.z);
    }

    // Dynamic molten extrusion light at active nozzle tip:
    // Active nozzle in Three.js world coordinates:
    // World X = 0.014 + toolX, World Y = currentCutY, World Z = 0.015 - toolY
    if (moltenLightRef?.current) {
      const activeY = (printProgress <= 0) ? Y_BED : (printProgress >= 1.0) ? (Y_TOP + 0.020) : currentCutY;
      moltenLightRef.current.position.set(0.014 + toolX, activeY + 0.003, 0.015 - toolY);
      
      if (isPrinting) {
        moltenLightRef.current.intensity = 3.6 + 1.2 * Math.sin(time * 24);
      } else {
        moltenLightRef.current.intensity = 0.0;
      }
    }
  });

  return <primitive object={gltf.scene} rotation={[-Math.PI / 2, 0, 0]} dispose={null} />;
}

function LoadingCard() {
  return (
    <Html center>
      <div className="scene-status" role="status">
        <span className="status-dot" />
        Đang khởi động buồng in 3D...
      </div>
    </Html>
  );
}

class ModelErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <Html center>
          <div className="scene-status" style={{ color: "#d9534f" }}>
            Không thể tải mô hình 3D. Vui lòng thử lại.
          </div>
        </Html>
      );
    }
    return this.props.children;
  }
}

// Cinematic Director: 4-Phase Camera Trajectory
// Phase 1 (0.0s - 5.5s): Exterior orbital beauty pan (Golden 3/4 overview, bed Z=0)
// Phase 2 (5.5s - 8.5s): Smooth dolly-in through front door into lit chamber
// Phase 3 (8.5s - 17.5s): Macro close-up tracking the rising nozzle printing layer-by-layer
// Phase 4 (17.5s - 22.0s): Smooth pull-back to 3/4 beauty view showcasing finished part
function CinematicDirector({ userInteractingRef, controlsRef, currentCutYRef }) {
  const elapsedRef = useRef(0);
  const baseTarget = useRef(new THREE.Vector3(0, -0.01, 0));

  useFrame((state, delta) => {
    if (userInteractingRef.current) {
      elapsedRef.current = 0;
      return;
    }

    const cycle = 22.0;
    if (window.__forcedTime !== undefined) {
      elapsedRef.current = window.__forcedTime;
    } else {
      elapsedRef.current += delta;
    }
    const t = elapsedRef.current;
    const timeInCycle = t % cycle;
    const phase = timeInCycle / cycle;

    const targetPos = new THREE.Vector3();
    const targetLook = new THREE.Vector3();

    // Exterior orbital distance and height
    const rExt = 1.85;
    const hExt = 0.30;

    if (phase < 0.25) {
      // Phase 1 (0 - 5.5s): Exterior orbital pan
      const p = phase / 0.25;
      const angle = 0.48 + p * 0.26; // ~27° to ~42° front 3/4
      targetPos.set(Math.sin(angle) * rExt, hExt + Math.sin(p * Math.PI) * 0.02, Math.cos(angle) * rExt);
      targetLook.copy(baseTarget.current);
    } else if (phase < 0.38) {
      // Phase 2 (5.5 - 8.5s): Smooth dolly-in through front glass into chamber
      const p = (phase - 0.25) / 0.13;
      const ease = p * p * (3 - 2 * p); // Smooth Hermite ease
      
      const startAngle = 0.74;
      const startPos = new THREE.Vector3(Math.sin(startAngle) * rExt, hExt, Math.cos(startAngle) * rExt);
      // Macro close position in front of nozzle
      const macroPos = new THREE.Vector3(0.12, Y_BED + 0.14, 0.48);
      const nozzleLook = new THREE.Vector3(0.010, Y_BED + 0.010, 0.010);

      targetPos.lerpVectors(startPos, macroPos, ease);
      targetLook.lerpVectors(baseTarget.current, nozzleLook, ease);
    } else if (phase < 0.80) {
      // Phase 3 (8.5 - 17.5s): Macro close-up on nozzle laying down layers from Z=0 to 100%
      const p = (phase - 0.38) / 0.42;
      const curCutY = currentCutYRef?.current || Y_BED;

      // Camera gently tracks the rising layer height curCutY
      const camY = curCutY + 0.14;
      const swayX = 0.12 + 0.012 * Math.sin(p * Math.PI * 4);
      const swayZ = 0.48 + 0.008 * Math.cos(p * Math.PI * 4);

      targetPos.set(swayX, camY, swayZ);
      targetLook.set(0.010, curCutY + 0.010, 0.010);
    } else {
      // Phase 4 (17.5 - 22.0s): Smooth pull-back to showcase complete part
      const p = (phase - 0.80) / 0.20;
      const ease = p * p * (3 - 2 * p);
      
      const macroEndPos = new THREE.Vector3(0.12, Y_TOP + 0.14, 0.48);
      const macroEndLook = new THREE.Vector3(0.010, Y_TOP + 0.010, 0.010);

      const endAngle = 0.48;
      const endPos = new THREE.Vector3(Math.sin(endAngle) * rExt, hExt, Math.cos(endAngle) * rExt);

      targetPos.lerpVectors(macroEndPos, endPos, ease);
      targetLook.lerpVectors(macroEndLook, baseTarget.current, ease);
    }

    state.camera.position.lerp(targetPos, 0.06);
    state.camera.lookAt(targetLook);
    if (controlsRef.current) {
      controlsRef.current.target.copy(targetLook);
    }
  });

  return null;
}

// Pure seamless 3D printer viewer: ZERO overlay, ZERO telemetry, pure machine in action
function SeamlessPrinterViewer({ onReady }) {
  const controlsRef = useRef(null);
  const moltenLightRef = useRef(null);
  const currentCutYRef = useRef(Y_BED);
  const userInteractingRef = useRef(false);
  const idleTimerRef = useRef(null);

  const handlePointerDown = () => {
    userInteractingRef.current = true;
    if (controlsRef.current) controlsRef.current.enabled = true;
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
  };

  const handlePointerUp = () => {
    if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
    idleTimerRef.current = setTimeout(() => {
      userInteractingRef.current = false;
      if (controlsRef.current) controlsRef.current.enabled = false;
    }, 5000);
  };

  return (
    <div
      className="printer-stage-seamless"
      aria-label="Mô hình 3D máy in công nghiệp Deltrol đang hoạt động"
      onPointerDown={handlePointerDown}
      onPointerUp={handlePointerUp}
      onPointerLeave={handlePointerUp}
    >
      <Canvas
        shadows
        dpr={[1, 2]}
        camera={{ position: [0.95, 0.32, 1.55], fov: 27, near: 0.01, far: 50 }}
        gl={{ antialias: true, alpha: true, localClippingEnabled: true }}
        onCreated={({ gl, camera, scene }) => {
          gl.localClippingEnabled = true;
          window.__camera = camera;
          window.__scene = scene;
          gl.setClearColor(0x000000, 0); // Transparent canvas to blend seamlessly with page ground
          gl.toneMapping = THREE.ACESFilmicToneMapping;
          gl.toneMappingExposure = 1.0;
          gl.outputColorSpace = THREE.SRGBColorSpace;
        }}
      >
        <ambientLight intensity={0.45} />
        {/* Studio Key Light */}
        <directionalLight
          castShadow
          position={[2.5, 3.5, 2.5]}
          intensity={1.6}
          color="#ffffff"
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        {/* Cool Rim Light */}
        <directionalLight position={[-2.2, 1.5, 1.5]} intensity={0.9} color="#b0e0ff" />
        {/* Interior Warm Ceiling Spot (illuminating the PEI bed & part) */}
        <spotLight position={[0, 0.22, 0]} angle={0.75} penumbra={0.6} intensity={2.2} color="#fff2db" />
        <pointLight position={[0, 0.10, 0]} intensity={0.8} color="#ffe4be" distance={0.65} />
        {/* Hotend active nozzle molten extrusion glow light */}
        <pointLight ref={moltenLightRef} position={[0.016, Y_BED, 0.015]} intensity={0.0} color="#ff8811" distance={0.30} />

        <Suspense fallback={<LoadingCard />}>
          <ModelErrorBoundary>
            <AnimatedPrinterModel 
              onReady={onReady} 
              moltenLightRef={moltenLightRef} 
              currentCutYRef={currentCutYRef} 
            />
          </ModelErrorBoundary>
        </Suspense>

        {/* Soft, realistic contact shadow on the clean page ground */}
        <ContactShadows
          position={[0, -0.252, 0]}
          opacity={0.38}
          scale={1.35}
          blur={1.8}
          far={0.45}
          color="#0b1821"
        />

        <OrbitControls
          ref={controlsRef}
          makeDefault
          enabled={false}
          enableDamping
          dampingFactor={0.06}
          minDistance={0.25}
          maxDistance={2.4}
          minPolarAngle={0.3}
          maxPolarAngle={Math.PI / 2 - 0.02}
          target={[0, -0.01, 0]}
        />

        <CinematicDirector 
          userInteractingRef={userInteractingRef} 
          controlsRef={controlsRef}
          currentCutYRef={currentCutYRef}
        />
      </Canvas>
    </div>
  );
}

export default function App() {
  const [activeNav, setActiveNav] = useState("materials");
  const handleModelReady = useCallback(() => {}, []);

  return (
    <div className="app-shell" id="top">
      {/* 1. Topline Utility Bar */}
      <div className="topline">
        <span>DELTROL · 3D PRINTING SOLUTIONS</span>
        <span>KHÁM PHÁ <b>·</b> SO SÁNH <b>·</b> LỰA CHỌN</span>
      </div>

      {/* 2. Navigation Header (Height ~80px) */}
      <header className="head">
        <a className="logo" href="#top" aria-label="Deltrol Controls">
          <img 
            src="/deltrol_logo.webp" 
            alt="Deltrol Controls" 
            onError={(e) => { e.currentTarget.src = "/logo.svg"; }}
          />
        </a>

        <nav className="nav" aria-label="Chính">
          <a 
            className={activeNav === "materials" ? "active" : ""} 
            href="#materials" 
            onClick={() => setActiveNav("materials")}
          >
            Vật liệu
          </a>
          <a 
            className={activeNav === "technology" ? "active" : ""} 
            href="#technology" 
            onClick={() => setActiveNav("technology")}
          >
            Công nghệ
          </a>
          <a 
            className={activeNav === "market" ? "active" : ""} 
            href="#market" 
            onClick={() => setActiveNav("market")}
          >
            Thị trường
          </a>
          <a 
            className={activeNav === "compare" ? "active" : ""} 
            href="#compare" 
            onClick={() => setActiveNav("compare")}
          >
            Lựa chọn
          </a>
        </nav>

        <a className="head-cta" href="#compare">
          So sánh máy <span>↗</span>
        </a>
      </header>

      {/* 3. Hero Section (2-Column Grid ~55% / 45%) */}
      <section className="hero">
        {/* Left Column: Copy */}
        <div className="copy">
          <div className="eyebrow">— GIẢI PHÁP LỰA CHỌN MÁY IN 3D</div>
          <h1>
            Lựa chọn <em>máy in 3D</em><br />
            cho nhà máy của bạn.
          </h1>
          <p className="lead">
            Khám phá các công nghệ in 3D, vật liệu phổ biến và những mẫu máy dành cho sản xuất, chế tạo mẫu và đồ gá trong nhà máy. So sánh thông số, chi phí và khả năng hỗ trợ để lựa chọn thiết bị phù hợp với nhu cầu thực tế.
          </p>
          <div className="buttons">
            <a href="#materials" className="btn-primary">
              Khám phá giải pháp
            </a>
            <a href="#compare" className="btn-secondary">
              So sánh các mẫu máy <span>→</span>
            </a>
          </div>
          <div className="micro">
            <span>04 nhóm nội dung</span>
            <span>Thông tin có dẫn nguồn</span>
            <span>Cập nhật 19/11/2026</span>
          </div>
        </div>

        {/* Right Column: Seamless 3D Printer Stage (Zero text overlay, fully integrated) */}
        <SeamlessPrinterViewer onReady={handleModelReady} />
      </section>

      {/* 4. 3-Column Stats Strip below Hero */}
      <section className="stats">
        <div className="stat-item">
          <span className="stat-label">NGÂN SÁCH THAM KHẢO / MÁY</span>
          <span className="stat-value">2.000–3.000 USD</span>
          <span className="stat-caption">Chưa gồm chi phí đưa về Việt Nam</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">CÔNG NGHỆ ĐANG TÌM HIỂU</span>
          <span className="stat-value">FDM / FFF</span>
          <span className="stat-caption">Đùn sợi nhựa nóng chảy</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">TỶ GIÁ QUY ĐỔI THAM KHẢO</span>
          <span className="stat-value">1 USD ≈ 25.900 ₫</span>
          <span className="stat-caption">Cần cập nhật theo ngày mua hàng</span>
        </div>
      </section>

      {/* 5. Additional Detailed Content Sections */}
      <section className="content-section" id="materials">
        <div className="section-head">
          <div className="eyebrow">— VẬT LIỆU IN CÔNG NGHIỆP</div>
          <h2>Vật liệu nhựa kỹ thuật &amp; sợi carbon gia cường</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>PA-CF (Polyamide + Carbon Fiber)</h3>
            <p>Vật liệu composite độ bền cao, chịu nhiệt và kháng va đập vượt trội, chuyên dụng cho đồ gá cơ khí và chi tiết chịu lực trong nhà máy.</p>
          </div>
          <div className="info-card">
            <h3>PETG / PETG-CF</h3>
            <p>Kháng hóa chất, độ ổn định kích thước cao, dễ in và chống ẩm tốt, phù hợp cho vỏ bảo vệ và linh kiện tự động hóa.</p>
          </div>
          <div className="info-card">
            <h3>TPU / Cao su kỹ thuật</h3>
            <p>Độ đàn hồi linh hoạt, chống mài mòn, tối ưu cho đệm chống sốc, con lăn, gioăng làm kín và tay kẹp robot.</p>
          </div>
        </div>
      </section>

      <section className="content-section" id="technology">
        <div className="section-head">
          <div className="eyebrow">— CÔNG NGHỆ &amp; CƠ CẤU VẬN HÀNH</div>
          <h2>Kiến trúc CoreXY buồng kín công nghiệp</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>Hệ chuyển động CoreXY</h3>
            <p>Đầu đùn di chuyển nhanh và nhẹ trên thanh trượt bi tuyến tính, triệt tiêu rung động và đạt tốc độ gia công lên đến 250–500 mm/s.</p>
          </div>
          <div className="info-card">
            <h3>Buồng in gia nhiệt kín</h3>
            <p>Duy trì nhiệt độ buồng ổn định 50–70°C, ngăn ngừa hiện tượng co ngót, nứt vỡ lớp in khi gia công các loại nhựa kỹ thuật cao cấp.</p>
          </div>
          <div className="info-card">
            <h3>Cân bàn tự động đa điểm</h3>
            <p>Cảm biến quét bề mặt PEI độ chính xác micromet, bù sai số tự động đảm bảo lớp bám đầu tiên hoàn hảo 100%.</p>
          </div>
        </div>
      </section>

      <section className="content-section" id="compare">
        <div className="section-head">
          <div className="eyebrow">— SO SÁNH &amp; LỰA CHỌN MÁY</div>
          <h2>Bảng phân tích thiết bị theo nhu cầu thực tế</h2>
        </div>
        <div className="cards-grid">
          <div className="info-card">
            <h3>Dòng Chế tạo mẫu nhanh (Prototyping)</h3>
            <p>Tối ưu chi phí đầu tư ban đầu, thời gian triển khai nhanh, phù hợp cho phòng R&amp;D kiểm tra ý tưởng trước sản xuất hàng loạt.</p>
          </div>
          <div className="info-card">
            <h3>Dòng Sản xuất đồ gá (Jig &amp; Fixture)</h3>
            <p>Độ chính xác cao, lặp lại ổn định, hỗ trợ vật liệu composite sợi carbon, thay thế trực tiếp đồ gá kim loại gia công CNC.</p>
          </div>
          <div className="info-card">
            <h3>Dòng Hoạt động liên tục 24/7</h3>
            <p>Kết cấu khung nhôm đúc nguyên khối, giám sát camera AI, tự động cảnh báo lỗi sợi nhựa và duy trì uptime nhà xưởng tối đa.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

useGLTF.preload(MODEL_URL);
