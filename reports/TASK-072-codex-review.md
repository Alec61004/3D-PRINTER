# Codex audit — TASK-072

- **Task:** `TASK-072-REFERENCE-DERIVED-UPPER-ROOF-REBUILD`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v40.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the upper-roof diagnostic, before/after, direct contact sheet, and
  fresh v40 front render.
- Verified v40 is a new binary from v33.

## Findings

1. v40 restores the numeric baseline (`14/15 PASS`, IoU `0.9073`) but does not
   improve the failing landmark. ROI 13 is unchanged at `(79.6,64.5,54.2)`,
   `dMax=34.7 FAIL`.
2. Recessing `top_roof_glass` by `0.025m` still leaves the rail in the upper
   roof overhang shadow. The direct render shows no visible rail correction.
3. The strongest successful lead remains v38's depth placement (`ROI 13
   dMax=10.2`), but its mesh cannot fit the current roof/shell relationship.
   Incremental edits to the current upper roof have therefore exhausted their
   useful search space.
4. The contact sheet again says `CANDIDATE v31` instead of v40, so evidence
   labeling remains disqualifying.

## Decision

The incremental upper-roof/ceiling patch path is retired after repeated
non-improvement. The next task must build a fresh reference-derived upper
chamber/rail source mesh as a coherent assembly, with the exterior shell
envelope locked first and the v38 visible-depth rail relationship used only
as a measured constraint. Do not keep patching the current roof nodes.

