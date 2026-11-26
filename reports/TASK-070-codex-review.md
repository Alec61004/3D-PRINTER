# Codex audit — TASK-070

- **Task:** `TASK-070-DEPTH-CALIBRATED-RAIL-PLACEMENT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v38.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the rail-depth diagnostic, before/after, direct contact sheet, and
  fresh v38 front render.
- Verified v38 has a new hash and the rail is in front of the roof-glass hit.

## Findings

1. The depth placement is the first real movement of the failing ROI:
   `13_Steel_Rail` reaches `dMax=10.2 PASS` at `t=1.600`.
2. The placement is not acceptable as a product model. The rail assembly
   protrudes above the shell, changing the bbox height `404→423` (`+3.42%`)
   and visibly creating detached vertical pieces above the roof.
3. Five formerly passing regions fail: ROI 02 `74.3`, ROI 03 `206.2`, ROI 08
   `34.2`, ROI 11 `16.8`, and ROI 12 `29.7`; overall is only `10/15 PASS`.
4. The contact sheet still carries the stale caption `CANDIDATE v31` rather
   than v38, so evidence labeling remains a required fix.

## Decision

Keep v38's depth relationship as the useful lead, but do not accept the
protruding geometry. The next task must integrate the rail into the shell
envelope by rebuilding/reshaping the upper roof, chamber ceiling and rail
mounts (or shortening/repositioning the assembly with measured screen-space
calibration). It must preserve ROI 13's pass while restoring all other ROI
passes and the reference bbox/silhouette.

