---
task_id: TASK-082-BLENDER-PATH-CORRECTED-CAD-RETRY
owner: antigravity
status: pending
created_at: 2026-11-26T12:36:00+07:00
request: >-
  Retry TASK-081 with the corrected installed Blender executable. TASK-081 was
  blocked because it checked the wrong path; Blender is present and verified as
  version 5.3.0 at
  C:/Users/PC/AppData/Local/Programs/Blender/blender-5.3.0-windows-x64/blender.exe.
  Use this executable to convert a complete free/licensed CAD assembly if one
  can be obtained. Do not use an isolated STL part. If no qualifying complete
  source exists, report BLOCKED for the source/license reason only.
result_path: assets/models/raw/deltrol_p2s_free_complete_source_v3.glb
---

# TASK-082 — corrected Blender CAD conversion retry

## Owner boundary

Antigravity owns source discovery/conversion and evidence. Do not edit Codex
website source. Codex will audit the handoff.

## Correct tool path

Use and verify exactly:

`C:/Users/PC/AppData/Local/Programs/Blender/blender-5.3.0-windows-x64/blender.exe`

Expected command output begins with `Blender 5.3.0`.

## Source gate

1. Use a complete P2S or genuinely useful enclosed CoreXY assembly with
   explicit free/redistributable license. Do not use a single STL/part,
   preview screenshot, login-gated download or unclear license.
2. If STEP/F3D/OBJ/FBX is found, convert it with the verified Blender path and
   record the exact source URL, author, license, retrieval date and file list.
3. Evaluate the complete converted GLB under the fixed fixture and render all
   required views. No billboard, image plane, screenshot texture, projected
   reference, emission, global unlit, camera or exposure trick.

## Required evidence

- `assets/models/raw/deltrol_p2s_free_complete_source_v3.glb` if found
- `reports/task082-source-license.md`
- `reports/task082-source-file-manifest.md`
- `reports/task082-source-bakeoff-sheet.png`
- `reports/task082-explorer-front.png`
- `reports/task082-explorer-left20.png`
- `reports/task082-explorer-right20.png`
- `reports/task082-explorer-elevated.png`
- `reports/task082-explorer-4view-sheet.png`
- `reports/task082-reference-candidate-contact-sheet.png`
- `reports/task082-before-after.png`
- `reports/task082-silhouette-overlay.png`
- `reports/TASK-082-antigravity-blender-path-corrected-cad-retry.md`
- `bridge/outbox/TASK-082-BLENDER-PATH-CORRECTED-CAD-RETRY-antigravity-response.md`

Every image must identify the real source and SHA-256. Contact sheet label:
`CANDIDATE EXTERNAL-FREE-SOURCE-v3`.

## Acceptance gates

- Blender executable verified and actually used;
- complete source/license verified;
- source materially differs from v33 and is useful for upper geometry;
- fixed-fixture evidence complete;
- ROI 13 materially improves with coherent real 3D geometry;
- if no source qualifies, report the exact source/license blocker, not a
  false tooling blocker.
