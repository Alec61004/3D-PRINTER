# Codex audit — TASK-071

- **Task:** `TASK-071-RAIL-SHELL-ENVELOPE-INTEGRATION`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v39.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the shell-fit diagnostic, before/after, direct contact sheet, and
  fresh v39 front render.
- Verified v39 is a new binary and includes a compact rail assembly.

## Findings

1. The compact rail no longer shows the obvious large roof protrusion, but it
   still conflicts with the shell envelope: bbox top shifts `174→167` (`+7px`)
   and the front visual remains unlike the reference.
2. The rail did not pass after compaction: ROI 13 is `dMax=20.1 FAIL`.
   Overall is `11/15 PASS`; ROIs 03, 08 and 12 also fail. Therefore the
   successful v38 depth placement was not preserved by this fit.
3. The report proves a binary conflict in the existing source mesh: depth
   behind the roof glass occludes the rail, while depth in front of it changes
   the exterior contour. This cannot be solved by another small rail scale or
   material adjustment.
4. The contact sheet still says `CANDIDATE v31` rather than v39, which remains
   an evidence-integrity failure.

## Decision

Retire the current upper-roof source mesh relationship. The next revision must
be a reference-derived rebuild of the upper roof/chamber opening and its
interior rail mounting surfaces, with the outer shell contour locked to the
reference. This is a new source reconstruction pivot, not another placement
or shader patch.

