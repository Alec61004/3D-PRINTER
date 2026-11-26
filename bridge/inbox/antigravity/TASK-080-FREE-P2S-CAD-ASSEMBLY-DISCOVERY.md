---
task_id: TASK-080-FREE-P2S-CAD-ASSEMBLY-DISCOVERY
owner: antigravity
status: blocked
verdict: BLOCKED
completed_at: 2026-11-26T10:39:45+07:00
created_at: 2026-11-26T11:44:00+07:00
request: >-
  Find a complete free/redistributable CAD or mesh assembly for Bambu P2S or a
  genuinely equivalent enclosed desktop CoreXY printer with upper gantry,
  chamber, front/right glass and shell geometry. Do not use individual Voron
  parts or unrelated printable components. Verify license/permission, download
  the complete assembly, convert it to GLB and evaluate it under the fixed
  fixture. If no qualifying source exists, produce a concrete BLOCKED report
  with the search evidence instead of fabricating a candidate.
result_path: assets/models/raw/deltrol_p2s_free_complete_source.glb
---

# TASK-080 — complete free P2S/CAD assembly discovery

## Owner boundary

Antigravity owns source discovery and conversion. Do not edit Codex website
source. Codex will audit the source/license and rendered result.

## Source gate

1. Accept only a complete assembly, not a single STL/part. It must contain a
   recognizable enclosed printer body plus upper gantry/chamber geometry.
2. Record the exact URL, author, license/permission, retrieval date and source
   file list. No paid download, login-gated asset, unclear license or scraped
   preview image.
3. If a P2S-specific CAD source is unavailable, an equivalent enclosed
   CoreXY printer is allowed only if its shell/gantry topology is materially
   useful for the Deltrol reference. Explain the mismatch before conversion.
4. Convert the complete source to GLB with real connected meshes. No
   billboard, image plane, screenshot texture, projected reference or 2.5D
   facade.

## Required evidence

- `assets/models/raw/deltrol_p2s_free_complete_source.glb` if a source is found
- `reports/task080-source-license.md`
- `reports/task080-source-file-manifest.md`
- `reports/task080-source-bakeoff-sheet.png`
- `reports/task080-explorer-front.png`
- `reports/task080-explorer-left20.png`
- `reports/task080-explorer-right20.png`
- `reports/task080-explorer-elevated.png`
- `reports/task080-explorer-4view-sheet.png`
- `reports/task080-reference-candidate-contact-sheet.png`
- `reports/task080-before-after.png`
- `reports/task080-silhouette-overlay.png`
- `reports/TASK-080-antigravity-free-p2s-cad-assembly-discovery.md`
- `bridge/outbox/TASK-080-FREE-P2S-CAD-ASSEMBLY-DISCOVERY-antigravity-response.md`

If no qualifying source exists, omit the GLB, set the report/response verdict
to `BLOCKED`, list all searched sources and explain why each failed the
complete-assembly/license gate.

## Acceptance gates

- Complete source and explicit license are verified;
- source is materially different from v33 and useful for upper geometry;
- fixed-fixture evidence is complete and correctly labeled;
- if evaluated as candidate, ROI 13 improves and the 3D asset is coherent in
  all four views;
- no isolated-part or unlicensed-source substitution.
