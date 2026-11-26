# Codex audit — TASK-075

- **Task:** `TASK-075-CLEAN-SOURCE-UPPER-ASSET-PIVOT`
- **Artifact:** `assets/models/raw/deltrol_p2s_clean_upper_asset_v1.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the clean-source report, source manifest and outbox response.
- Inspected the clean-source diagnostic, before/after, direct contact sheet,
  and fresh front render.
- Verified the artifact hash differs from v33.

## Findings

1. The reported clean source still removes old nodes and adds one small rail
   mesh at the same old AABB, but the fixed front render is unchanged. ROI 13
   remains `(79.6,64.5,54.2)`, `dMax=34.7 FAIL`; overall remains `14/15 PASS`,
   IoU `0.9073`.
2. The diagnostic still shows the exterior upper-shell shadow, proving the
   effective physical source was not replaced in the rendered scene.
3. The contact sheet remains mislabeled `CANDIDATE v31` instead of the clean
   asset label, so evidence integrity is still invalid.

## Decision

Retire the v33-derived upper-asset path. The workspace contains several older
physical source candidates; the next task will render and compare those actual
assets under the fixed fixture, select a genuinely different source if one is
better, and only then integrate it. No more metadata-only upper-node edits.

