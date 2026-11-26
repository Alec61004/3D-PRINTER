---
task_id: TASK-081-BLENDER-CAD-CONVERSION-RETRY
owner: antigravity
status: blocked
verdict: BLOCKED
completed_at: 2026-11-26T12:31:35+07:00
created_at: 2026-11-26T11:52:00+07:00
request: >-
  Retry TASK-080 now that Blender LTS 4.5.10 is installed at
  C:/Users/PC/AppData/Local/Programs/Blender. Find a complete free or
  redistributable P2S/CAD/enclosed-CoreXY assembly, convert its STEP/OBJ/FBX
  source to GLB with Blender, and evaluate it under the fixed fixture. Do not
  use an isolated STL part. If no complete licensed source can be found,
  report BLOCKED with exact evidence instead of creating a fake candidate.
result_path: assets/models/raw/deltrol_p2s_free_complete_source_v2.glb
---

# TASK-081 — Blender CAD conversion retry

## Owner boundary

Antigravity owns source discovery/conversion and evidence. Do not edit Codex
website source. Codex will audit the resulting source.

## Tooling

- Blender executable: `C:/Users/PC/AppData/Local/Programs/Blender/blender.exe`
- FreeCAD may be used if available, but do not install paid tools/services.

## Non-negotiable source gate

1. Use a complete enclosed P2S or genuinely useful enclosed CoreXY assembly,
   not an individual Voron/printable STL part. Record URL, author, license,
   retrieval date and every source file used.
2. If source is STEP/F3D/OBJ/FBX, use Blender 4.5.10 or a free local converter
   to produce a real connected GLB. Verify node/mesh counts and materials.
3. Calibrate against the fixed fixture: 1226x708, FOV 27°, eye
   `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white background, ACES,
   exposure 1.05. Include front/left20/right20/elevated renders.
4. No billboard, image plane, screenshot texture, projected reference, 2.5D
   facade, emission, global unlit, camera or exposure trick.

## Required evidence

- `assets/models/raw/deltrol_p2s_free_complete_source_v2.glb` if found
- `reports/task081-source-license.md`
- `reports/task081-source-file-manifest.md`
- `reports/task081-source-bakeoff-sheet.png`
- `reports/task081-explorer-front.png`
- `reports/task081-explorer-left20.png`
- `reports/task081-explorer-right20.png`
- `reports/task081-explorer-elevated.png`
- `reports/task081-explorer-4view-sheet.png`
- `reports/task081-reference-candidate-contact-sheet.png`
- `reports/task081-before-after.png`
- `reports/task081-silhouette-overlay.png`
- `reports/TASK-081-antigravity-blender-cad-conversion-retry.md`
- `bridge/outbox/TASK-081-BLENDER-CAD-CONVERSION-RETRY-antigravity-response.md`

Every image must identify the actual source and SHA-256. The contact sheet
must say `CANDIDATE EXTERNAL-FREE-SOURCE-v2`, never v31/v33.

## Acceptance gates

- complete source and explicit license verified;
- source is materially different from v33 and useful for upper geometry;
- fixed-fixture evidence is complete;
- ROI 13 materially improves, ideally `dMax <= 15`, with other gates checked;
- if no qualifying source exists even with Blender installed, mark `BLOCKED`
  and document the exact source/tool/license blocker.
