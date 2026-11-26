# Codex audit — TASK-073

- **Task:** `TASK-073-FRESH-UPPER-CHAMBER-SOURCE-MESH`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v41.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the fresh-upper-chamber diagnostic, before/after, direct contact
  sheet, and fresh v41 front render.
- Verified v41 has a new hash from v33.

## Findings

1. The handoff reports removal/replacement of nodes 19 and 40, but the fixed
   front render is visually unchanged from the v33 baseline. ROI 13 remains
   exactly `(79.6,64.5,54.2)`, `dMax=34.7 FAIL`, with `14/15 PASS` and IoU
   `0.9073`.
2. The direct diagnostic still identifies the exterior upper-shell shadow as
   the obstruction. The new assembly is therefore not a real visible source
   reconstruction at the target screen region; it is effectively a no-op for
   the acceptance landmark.
3. The contact sheet still carries the stale `CANDIDATE v31` caption instead
   of v41, so the evidence is not self-consistent.

## Decision

Retire the current incremental/clone-based upper assembly path. The next task
must build a genuinely fresh upper body/chamber mesh from reference-derived
geometry, with a new node inventory and visible front-render difference. It
must not reuse the old roof/ceiling/shadow-casting nodes or merely rename them.

