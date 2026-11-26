---
task_id: TASK-067-RAIL-PRIMITIVE-IDENTIFICATION-PIVOT
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T10:08:15+07:00
created_at: 2026-11-26T10:12:00+07:00
request: >-
  Pivot from the failed v34 guessed material-index edit. Starting from the
  v33 numeric base, identify the actual render primitive that covers fixed
  ROI 13 (Steel Rail) using an object/depth/material-ID diagnostic at the
  mandated fixture camera. Do not infer ownership from node names alone:
  mesh 43 and mesh 44 share material 12, and v34 proved that editing that
  shared material breaks the right-window glass while not fixing ROI 13.
result_path: assets/models/raw/deltrol_p2s_explorer_v35.glb
---

# TASK-067 — identify the actual rail primitive, then isolate it

## Owner boundary

Antigravity owns the visual/asset revision and evidence. Do not edit Codex
website source. Codex will audit the artifact after the terminal handoff.

## Required pivot

1. Start from `assets/models/raw/deltrol_p2s_explorer_v33.glb`, not v34.
2. Use the fixed fixture (`tools/true3d_audit_viewer.html`, 1226x708,
   FOV 27°, camera `[0.86,0.22,1.50]`, target `[0,-0.01,0]`, white
   background, ACES, exposure 1.05) to produce an object/depth/material-ID
   diagnostic for ROI 13 `(493,300)-(518,305)`.
3. Record the actual node, mesh, primitive index, material index and depth
   responsible for those pixels. If the pixels are a shadow, glass layer or
   occlusion rather than the rail, report that explicitly and pivot to the
   real visible rail geometry; do not alter unrelated materials.
4. Split a shared primitive/material assignment when necessary. The repair
   must remain real connected mechanical 3D geometry. A thin rail-shaped
   mechanical mesh is allowed only when it is geometrically aligned to the
   existing rail in all required views; no billboard, screenshot, image plane,
   emission trick, global unlit interior, camera/exposure change, or 2.5D
   overlay.
5. Set the isolated rail material to a warm dark steel that moves ROI 13
   toward reference `(114.3,96.3,85.6)` while preserving v33's turbine,
   right-window glass, skylight and chamber-upper values. Restore v33 values
   for any material changed by v34 before testing.

## Required evidence

- `assets/models/raw/deltrol_p2s_explorer_v35.glb`
- `reports/task067-explorer-front.png`
- `reports/task067-explorer-left20.png`
- `reports/task067-explorer-right20.png`
- `reports/task067-explorer-elevated.png`
- `reports/task067-explorer-4view-sheet.png`
- `reports/task067-reference-candidate-contact-sheet.png`
- `reports/task067-rail-object-id-diagnostic.png`
- `reports/task067-before-after.png`
- `reports/task067-silhouette-overlay.png`
- `reports/TASK-067-antigravity-rail-primitive-identification-pivot.md`
- `bridge/outbox/TASK-067-RAIL-PRIMITIVE-IDENTIFICATION-PIVOT-antigravity-response.md`

Every image must be rendered from v35. The contact sheet must say
`CANDIDATE v35` and include the v35 SHA-256. The report must include old/new
hashes, the object-ID/depth mapping, all 15 ROIs, 12 landmarks, GLB
validation, and a note proving the rail crop pixels differ from v33.

## Acceptance gates

- ROI 13 `dMax <= 15`;
- ROIs 07, 11, 12 and 14 remain `dMax <= 15` and no worse than v33;
- centered IoU `>= 0.90`, silhouette and primary geometry preserved;
- direct v35 contact sheet visibly approaches the reference;
- no shared-material spill, no mislabeled evidence, and no analytic trick.

If the ID pass proves ROI 13 is not a rail surface, report the proven owner
and use that evidence to define the next real-geometry pivot; do not fabricate
a PASS.
