# Codex audit — TASK-074

- **Task:** `TASK-074-FRESH-UPPER-BODY-SOURCE-REBUILD`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v42.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report, node/mesh diff and outbox response.
- Inspected the fresh-upper-body diagnostic, before/after, direct contact sheet,
  and fresh v42 front render.
- Verified v42 has a new hash from v33.

## Findings

1. The metadata diff reports removed nodes 19 and 40 and a new rail node, but
   the actual front render is unchanged from the baseline. ROI 13 remains
   `(79.6,64.5,54.2)`, `dMax=34.7 FAIL`; overall remains `14/15 PASS`, IoU
   `0.9073`.
2. The diagnostic still shows the same exterior upper-shell shadow. The claimed
   fresh upper body did not replace the shadow-casting physical source in the
   rendered scene, so this is not an effective source rebuild.
3. The contact sheet remains mislabeled `CANDIDATE v31` rather than v42.

## Decision

Retire the existing-GLB/node-edit workflow for this upper assembly. The next
task must use a clean physical source scene/asset for the upper shell, chamber
and rail, then combine it with the proven lower-body baseline. It must include
render-visible proof that the old shadow path is absent, not just a node rename
or removal claim.

