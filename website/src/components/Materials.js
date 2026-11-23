import * as THREE from "three";

// ---------------------------------------------------------------------------
// 1. Procedural Texture Generators for Bambu Lab P2S
// ---------------------------------------------------------------------------

export function createNoiseTexture(size = 256, intensity = 22) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  const imgData = ctx.createImageData(size, size);
  const data = imgData.data;

  for (let i = 0; i < data.length; i += 4) {
    const val = 128 + (Math.random() - 0.5) * intensity;
    data[i] = val;
    data[i + 1] = val;
    data[i + 2] = val;
    data[i + 3] = 255;
  }
  ctx.putImageData(imgData, 0, 0);

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(4, 4);
  return texture;
}

export function createBlackPeiTexture(size = 256) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  const imgData = ctx.createImageData(size, size);
  const data = imgData.data;

  for (let i = 0; i < data.length; i += 4) {
    // Micro-pebbled texture for Bambu textured PEI plate
    const noise = (Math.random() - 0.5) * 32;
    const v = Math.max(18, Math.min(65, 34 + noise));
    data[i] = v;
    data[i + 1] = v;
    data[i + 2] = v + 2;
    data[i + 3] = 255;
  }
  ctx.putImageData(imgData, 0, 0);

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(8, 8);
  return texture;
}

export function createBrushedTexture(size = 256) {
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#a0a8b0";
  ctx.fillRect(0, 0, size, size);

  // Subtle horizontal brushing lines
  for (let y = 0; y < size; y++) {
    const brightness = 150 + (Math.random() - 0.5) * 30;
    ctx.strokeStyle = `rgb(${brightness},${brightness},${brightness})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(size, y);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 6);
  return texture;
}

export function createP2STouchscreenTexture(progress = 0.45, tempNozzle = 245, tempBed = 65) {
  const w = 512;
  const h = 256;
  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext("2d");

  // Modern Bambu dark UI background
  ctx.fillStyle = "#0c1015";
  ctx.fillRect(0, 0, w, h);

  // Status header bar
  ctx.fillStyle = "#18212d";
  ctx.fillRect(16, 52, w - 32, 2);

  // Brand and Model
  ctx.font = "bold 20px 'DM Sans', -apple-system, sans-serif";
  ctx.fillStyle = "#f1f5f9";
  ctx.fillText("DELTROL P2S PRO", 24, 38);

  ctx.font = "600 15px 'DM Sans', sans-serif";
  ctx.fillStyle = "#38bdf8";
  ctx.fillText("READY / PRINTING", w - 170, 38);

  // Status items
  ctx.font = "15px 'DM Sans', sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("NOZZLE:", 24, 94);
  ctx.fillStyle = "#f59e0b";
  ctx.font = "bold 17px 'DM Sans', sans-serif";
  ctx.fillText(`${tempNozzle}°C / 245°C`, 120, 94);

  ctx.font = "15px 'DM Sans', sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("HOTBED:", 24, 134);
  ctx.fillStyle = "#38bdf8";
  ctx.font = "bold 17px 'DM Sans', sans-serif";
  ctx.fillText(`${tempBed}°C / 65°C`, 120, 134);

  ctx.font = "15px 'DM Sans', sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("SPEED:", 24, 174);
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "bold 17px 'DM Sans', sans-serif";
  ctx.fillText("250 mm/s (CoreXY)", 120, 174);

  ctx.font = "15px 'DM Sans', sans-serif";
  ctx.fillStyle = "#94a3b8";
  ctx.fillText("PROGRESS:", 24, 214);
  ctx.fillStyle = "#e2e8f0";
  ctx.font = "bold 17px 'DM Sans', sans-serif";
  ctx.fillText("LỚP 144 / 320", 120, 214);

  // Right Circular Progress Gauge (matching Bambu screen UI)
  const cx = w - 95;
  const cy = 150;
  const radius = 54;

  ctx.lineWidth = 10;
  ctx.strokeStyle = "#1e293b";
  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.stroke();

  // Progress arc
  const pct = Math.min(Math.max(progress, 0), 1);
  ctx.strokeStyle = "#38bdf8";
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.arc(cx, cy, radius, -Math.PI / 2, -Math.PI / 2 + pct * Math.PI * 2);
  ctx.stroke();

  ctx.font = "bold 26px 'DM Sans', sans-serif";
  ctx.fillStyle = "#ffffff";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(`${Math.round(pct * 100)}%`, cx, cy);

  const texture = new THREE.CanvasTexture(canvas);
  texture.anisotropy = 4;
  return texture;
}

// ---------------------------------------------------------------------------
// 2. High-Fidelity Photoreal Material Collection for Bambu P2S
// ---------------------------------------------------------------------------

export function createPhotorealMaterials(clipPlane) {
  const noiseTex = createNoiseTexture(256, 18);
  const blackPeiTex = createBlackPeiTexture(256);
  const brushedTex = createBrushedTexture(256);
  const screenTex = createP2STouchscreenTexture(0.45);

  // 1. Satin Anodized Silver-Gray Aluminum Unibody Chassis (P2S Core Identity)
  const chassisMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#9da5ad"),
    metalness: 0.68,
    roughness: 0.35,
    roughnessMap: brushedTex,
  });

  // 2. Matte Dark Charcoal Accents & Gaskets (Door rim, frame seals, hinges)
  const darkTrimMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#181b20"),
    roughness: 0.62,
    metalness: 0.20,
    roughnessMap: noiseTex,
  });

  // 3. Polished Aluminum Frame & Door Handle
  const polishedAluminumMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#d2d8df"),
    metalness: 0.88,
    roughness: 0.18,
  });

  // 4. Crystal-Clear Tempered Physical Glass (Transmission PBR)
  const glassMat = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color("#e6f1f8"),
    transmission: 0.98,
    opacity: 1.0,
    transparent: true,
    roughness: 0.02,
    ior: 1.50,
    thickness: 0.012,
    attenuationColor: new THREE.Color("#9ec9e8"),
    attenuationDistance: 1.2,
    depthWrite: false,
    reflectivity: 0.88,
  });

  // 5. Solid Textured Matte Black Spring Steel PEI Build Plate (P2S standard)
  const blackPeiMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#15181b"),
    map: blackPeiTex,
    metalness: 0.18,
    roughness: 0.85,
  });

  // 6. Polished Brass Nozzle (Warm metallic, non-emissive)
  const brassNozzleMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#dfa932"),
    metalness: 0.96,
    roughness: 0.18,
  });

  // 7. Precision Ground Steel Guide Rails & Leadscrews
  const steelRailsMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#e4ebf2"),
    metalness: 0.98,
    roughness: 0.10,
  });

  // 8. Lead Screws (Slightly darker threaded steel)
  const leadScrewMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#c5cbd2"),
    metalness: 0.94,
    roughness: 0.22,
  });

  // 9. Black Rubber Timing Belts & Anti-Vibration Feet
  const rubberMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#121417"),
    roughness: 0.88,
    metalness: 0.05,
  });

  // 10. Cable Drag Chain (Articulated Carbon-Black Links)
  const cableChainMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#1b1e22"),
    roughness: 0.58,
    metalness: 0.25,
  });

  // 11. PTFE White Filament Bowden Guide Tubes
  const ptfeMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#f8fafc"),
    roughness: 0.28,
    metalness: 0.02,
  });

  // 12. Bambu Touchscreen Display
  const screenMat = new THREE.MeshBasicMaterial({
    map: screenTex,
  });

  // 13. Overhead Interior LED Light Strip (~4000K crisp neutral white)
  const ledLightMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#ffffff"),
    emissive: new THREE.Color("#fffaf0"),
    emissiveIntensity: 2.2,
    roughness: 0.2,
  });

  // 14. Printed PA-CF Carbon Fiber Part (With CAD Clipping Plane)
  const printedPartMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#24282c"),
    roughness: 0.42,
    metalness: 0.28,
    roughnessMap: noiseTex,
    clippingPlanes: clipPlane ? [clipPlane] : [],
    clipShadows: true,
  });

  // 15. Tree Support Material
  const treeSupportMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#e8e5dc"),
    roughness: 0.52,
    metalness: 0.05,
    clippingPlanes: clipPlane ? [clipPlane] : [],
    clipShadows: true,
  });

  // 16. Interior Chamber Dark Floor & Rear Wall
  const chamberInteriorMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color("#15181c"),
    roughness: 0.65,
    metalness: 0.30,
  });

  return {
    chassis: chassisMat,
    darkTrim: darkTrimMat,
    polishedAluminum: polishedAluminumMat,
    glass: glassMat,
    blackPei: blackPeiMat,
    brassNozzle: brassNozzleMat,
    steelRails: steelRailsMat,
    leadScrew: leadScrewMat,
    rubber: rubberMat,
    cableChain: cableChainMat,
    ptfe: ptfeMat,
    screen: screenMat,
    ledLight: ledLightMat,
    printedPart: printedPartMat,
    treeSupport: treeSupportMat,
    chamberInterior: chamberInteriorMat,
  };
}
