# Codex audit — TASK-051

- **Task:** `TASK-051-INTERIOR-MECHANICS-REFERENCE-REBUILD`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v19.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected `task051-interior-before-after.png`, the direct front render and the reference/candidate contact sheet.
- Verified the fixed-fixture framing: `423x404`, centered IoU `0.9073`.

## Findings

1. Rail remains a hard failure at `dMax=33.4`; turbine improves only to `dMax=15.8`, still over the `15` gate. Only 13/15 ROIs pass.
2. The direct before/after image shows almost no meaningful change between v18 and v19 in the upper gantry/rail assembly. The candidate still reads as a pale generic frame instead of the reference's dark warm mechanical interior.
3. The task contract explicitly prohibited global emission, but the reported rail, gantry and turbine materials all use `emissive_scale=1.0`. This is a contract violation and explains why the direct visual evidence remains inconsistent with the intended material path.
4. The right-window glass was restored (`dMax=5.5`), so that part should be preserved in the next pivot.

## Decision

Retire the current v18/v19 interior family. Continue with a fresh interior source mesh/material construction and a hard GLB-level check that the rail/turbine materials have no emissive contribution. Do not copy v19 and adjust another shader constant.
