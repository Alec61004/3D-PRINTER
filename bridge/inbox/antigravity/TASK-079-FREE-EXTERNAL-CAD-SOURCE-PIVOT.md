---
task_id: TASK-079-FREE-EXTERNAL-CAD-SOURCE-PIVOT
owner: antigravity
status: pending
created_at: 2026-11-26T11:36:00+07:00
request: >-
  Pivot away from the failed legacy GLB grafts. Find and evaluate a free,
  redistributable CAD/photogrammetry/source model for an enclosed Bambu P2S-like
  desktop 3D printer or equivalent mechanical enclosure with an upper gantry.
  Use only a source with explicit permission/license evidence; no paid service
  or unlicensed asset. Convert the best source to a real GLB and calibrate it
  against the Deltrol reference under the fixed fixture.
result_path: assets/models/raw/deltrol_p2s_external_free_source.glb
---

# TASK-079 — free external physical source pivot

## Owner boundary

Antigravity owns source discovery, license evidence and visual asset creation.
Do not edit Codex website source. Codex will audit the resulting GLB.

## Source requirements

1. Search public sources for a free/redistributable STEP/OBJ/FBX/GLTF/GLB or
   photogrammetry model. Accept only an explicit license/permission that allows
   this project’s use; record URL, author, license and retrieval date. Do not
   use paid downloads, login-gated assets, or unclear terms.
2. Prefer a source with real upper gantry, chamber, front glass and enclosed
   shell geometry. Do not use a screenshot, billboard, image plane or
   2.5D/depth facade.
3. Convert to GLB in a clean asset pipeline and calibrate scale/orientation to
   the fixed reference. Preserve real connected geometry across front, left20,
   right20 and elevated views. The Deltrol lower shell may be used only if it
   does not reintroduce the proven v33 upper-shadow conflict.
4. Use normal PBR materials and a documented local light setup. No emission,
   global unlit, camera change or exposure trick to pass ROI sampling.

## Required evidence

- `assets/models/raw/deltrol_p2s_external_free_source.glb`
- `reports/task079-source-license.md`
- `reports/task079-source-bakeoff-sheet.png`
- `reports/task079-explorer-front.png`
- `reports/task079-explorer-left20.png`
- `reports/task079-explorer-right20.png`
- `reports/task079-explorer-elevated.png`
- `reports/task079-explorer-4view-sheet.png`
- `reports/task079-reference-candidate-contact-sheet.png`
- `reports/task079-external-source-diagnostic.png`
- `reports/task079-before-after.png`
- `reports/task079-silhouette-overlay.png`
- `reports/TASK-079-antigravity-free-external-cad-source-pivot.md`
- `bridge/outbox/TASK-079-FREE-EXTERNAL-CAD-SOURCE-PIVOT-antigravity-response.md`

Every image must be rendered from the external-source GLB. The contact sheet
must say `CANDIDATE EXTERNAL-FREE-SOURCE` and include the artifact SHA-256; do
not use a stale v31/v33 caption.

## Acceptance gates

- Source is materially different from v33/v2 and license is documented;
- ROI 13 improves materially and reaches `dMax <= 15`, or the report gives a
  measured source limitation and a concrete next source;
- ROIs 01–12, 14 and 15 remain `PASS` and no worse than v33;
- bbox/silhouette/framing are within reference tolerance;
- real 3D continuity holds in all four views;
- no paid/unlicensed source or analytic visual trick.
