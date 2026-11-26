# Codex audit — TASK-076

- **Task:** `TASK-076-LEGACY-SOURCE-ASSET-BAKEOFF`
- **Artifact:** `assets/models/raw/deltrol_p2s_legacy-source-bakeoff.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the bake-off report, metrics and outbox response.
- Inspected the four-source bake-off sheet, selected-source contact sheet,
  before/after and selected 4-view render.
- Verified the selected artifact hash.

## Findings

1. None of the legacy complete assets beats v33 globally. v33 remains the best
   baseline at IoU `0.9073`, `14/15 PASS`.
2. `deltrol_p2s_photoreal_v2.glb` is nevertheless the strongest measured
   upper-rail source: ROI 13 `dMax=24.3`, closer than v33 `34.7`, while the
   other legacy sources are worse (`57.1`, `90.2`, `13.4` but only `2/15`
   overall for optimized). This is a useful component source, not a viable
   whole-model replacement.
3. The selected bake-off copy is `true3d_candidate_v3`, not the best rail
   source, and its contact caption again says `CANDIDATE v31`; the evidence is
   not a final candidate.

## Decision

Use the measured best component source rather than replacing the whole model:
graft the upper chamber/gantry/rail geometry from `photoreal_v2.glb` onto the
v33 lower shell, then reapply the fixed visual gates. Do not carry photoreal_v2
glass/shell/materials that caused its low IoU.

