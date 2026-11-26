# Codex audit — TASK-067

- **Task:** `TASK-067-RAIL-PRIMITIVE-IDENTIFICATION-PIVOT`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v35.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Inspected the object-ID/depth diagnostic, before/after, direct contact sheet,
  and fresh v35 front render.
- Compared v35 and v33 SHA-256 values and confirmed they are identical.

## Findings

1. The raycast is useful and conclusive: ROI 13 does not hit a steel rail.
   At the sampled pixels it hits `top_roof_glass` (node 40 / mesh 38 / mat 2),
   then `interior_ceiling_liner` (node 19 / mesh 18 / mat 5), then the rear
   electronics box. No rail primitive is present at that screen region.
2. v35 is a no-op relative to v33 (`SHA-256` is identical), so the hard rail
   failure remains `dMax=34.7`; this is a valid diagnostic handoff but not a
   visual improvement.
3. The baseline remains `14/15 PASS`, IoU `0.9073`, with ROI 13 as the only
   hard failure. The direct render still differs materially from the reference
   in the upper interior rail/mechanical landmark.
4. The contact sheet again says `CANDIDATE v31` despite being labeled as the
   task's v35 render. This evidence-integrity defect must be fixed next time.

## Decision

Keep v33/v35 as the numeric baseline and pivot to real geometry. The next task
must add a connected, rail-shaped mechanical 3D mesh at the proven world-space
location under the roof glass, with an isolated material, and verify it in all
four views. It must not be a billboard, image plane, projected texture,
emission trick, global material edit, or camera/exposure change.

