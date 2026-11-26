# Codex audit — TASK-053

- **Task:** `TASK-053-CAD-INTERIOR-SOURCE-REBUILD`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v21.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected `task053-interior-before-after.png` and the reference/candidate contact sheet.
- Verified the candidate SHA-256 reported by Antigravity: `84641D7DA27FE993186002694F868F9190528902257C544BAB66394C57B9E4F8`.
- Compared it with the preceding v20 artifact: the hash is identical, so v21 is byte-for-byte the same GLB as v20.

## Findings

1. TASK-053 promised a fresh CAD/Blender source mesh, but the artifact is an exact no-op copy of v20. The source-mesh pivot was not executed.
2. The direct before/after image confirms no visible change. The candidate remains the pale generic interior and fails the same three gates: rail `35.1`, turbine `20.4`, right glass `26.0`; only 12/15 ROIs pass.
3. The report's material proof is not enough because the required geometry/source change never occurred.

## Decision

Reject the handoff and retire the v12–v21 procedural/no-op family. The next task must first prove a different artifact hash and changed mesh/node inventory before visual audit. Then it must use a genuinely different source-asset or manually authored Blender construction method.
