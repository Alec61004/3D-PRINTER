# Codex audit — TASK-055

- **Task:** `TASK-055-REFERENCE-MATCHED-MECHANICAL-ASSEMBLY`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v23.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified v23 has a different hash and inventory from v22.
- Inspected `task055-mechanical-before-after.png`, the direct front render and the reference/candidate contact sheet.

## Findings

1. The artifact changed, but the actual sampled rail/turbine appearance did not: rail `dMax=35.1`, turbine `dMax=20.4`, unchanged from v22. Right-window glass remains failed at `dMax=26.0`; only 12/15 ROIs pass.
2. The before/after crop shows the new mechanical pieces appearing in a different screen region, while the fixed ROI 13/14 still samples the old pale assembly. The task changed nodes but did not align them to the reference's sampled screen-space locations.
3. The contact sheet still differs globally: the upper assembly is pale and bulky, with the carriage/toolhead offset from the reference; the right window is too dark.
4. Framing passes, but no visual acceptance is possible from unchanged failing ROIs.

## Decision

Retire this free-placement mechanical assembly attempt. Continue with a screen-space calibrated geometry pass: the fixed camera projection must be used to place the actual rail/turbine primitives over ROI 13/14, and the report must include a coverage/ownership overlay proving which primitive supplies those pixels before material tuning.
