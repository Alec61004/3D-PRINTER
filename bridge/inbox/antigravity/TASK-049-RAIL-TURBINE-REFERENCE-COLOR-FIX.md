---
task_id: TASK-049-RAIL-TURBINE-REFERENCE-COLOR-FIX
owner: antigravity
status: pending
created_at: 2026-11-26T09:00:00+07:00
request: >-
  Continue the Deltrol P2S reference-fidelity loop. TASK-048 was audited by Codex
  and rejected: the v15/v16 diagnostic is visually near-identical, and the exact
  rail and turbine ROI gates still fail (dMax 33.9 and 18.7). Produce a new
  true-3D candidate that materially fixes the dark warm metallic rail/gantry,
  turbine arch and readable mechanical contrast in the reference without using
  a billboard, image plane, or 2.5D cheat.
result_path: assets/models/raw/deltrol_p2s_explorer_v17.glb
---

# TASK-049 — Rail/turbine reference-color fix

## Owner boundary

Antigravity owns the visual/material implementation and the new GLB. Do not edit
Codex-owned website source. Read the fixed fixture and reference criteria before
rendering.

## Non-negotiable acceptance evidence

1. Create `assets/models/raw/deltrol_p2s_explorer_v17.glb`.
2. Render the fixed fixture at `1226x708`, FOV `27°`, camera `[0.86,0.22,1.50]`,
   target `[0,-0.01,0]`, white background, ACES, exposure `1.05`.
3. Produce these files:
   - `reports/task049-explorer-front.png`
   - `reports/task049-explorer-left20.png`
   - `reports/task049-explorer-right20.png`
   - `reports/task049-explorer-elevated.png`
   - `reports/task049-explorer-4view-sheet.png`
   - `reports/task049-reference-candidate-contact-sheet.png`
   - `reports/task049-rail-turbine-before-after.png`
   - `reports/task049-silhouette-overlay.png`
   - `reports/TASK-049-antigravity-rail-turbine-reference-color-fix.md`
   - `bridge/outbox/TASK-049-RAIL-TURBINE-REFERENCE-COLOR-FIX-antigravity-response.md`
4. In the report, list the exact node, mesh, primitive and material index for:
   - every horizontal/vertical rail and gantry primitive;
   - `bracket_swept_arch` / turbine primitive;
   - the toolhead and bed primitives visible in the failing ROI.
5. Show a real before/after render crop proving that the selected primitive pixels
   changed. A material table or numeric claim without direct image evidence is
   insufficient.
6. Target rendered colors at the fixed ROI locations:
   - steel rail approximately `(114,93,80)`;
   - turbine arch approximately `(109,88,73)`;
   while retaining readable dark/warm metallic contrast, not a uniformly white
   emissive mesh.
7. Re-run all 15 ROIs, silhouette/IoU, landmarks and GLB validation. Report
   failures honestly; do not claim PASS from build/load success.

## Pivot guard

This is the second diagnostic/material attempt in the current projection family.
If the exact rail/turbine rendered pixels do not visibly change again, mark the
current projection/material path `PIVOT_REQUIRED` and propose a different asset or
mesh/material construction method in the report. Do not spend another iteration
changing only camera, exposure or generic shader values.
