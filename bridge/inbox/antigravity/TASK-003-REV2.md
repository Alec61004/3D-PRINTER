---
task_id: TASK-003-REV2
parent_task_id: TASK-003
stage_id: STAGE-003
owner: antigravity
status: completed
type: real_product_visual_revision
created_by: codex
created_at: 2026-11-19T19:34:30+07:00
attempt: 3
max_attempts: 3
result_path: assets/generated/antigravity/p2s_reference_front_right_3_4_rev2.jpg
metadata_path: assets/generated/antigravity/p2s_reference_front_right_3_4_rev2_metadata.json
response_path: bridge/outbox/TASK-003-REV2-antigravity-response.md
---

# TASK-003-REV2 — Final STAGE-003 revision

Create one clean final visual reference for the existing Doop frame `AG · P2S Reference · Front 3/4`.

## Blocking defects from REV1

- The response and metadata pointed to the original `p2s_reference_front_right_3_4.jpg` instead of the revised asset.
- `p2s_reference_front_right_3_4_rev1.jpg` contains a large black rectangular edit covering the front chamber; it is not suitable for Image-to-3D reference.
- The Doop frame displayed an asset inconsistent with the claimed revision, including visible UI/bed text.

## Required final result

1. Generate/save a single clean image at exactly:
   `assets/generated/antigravity/p2s_reference_front_right_3_4_rev2.jpg`
2. The image must have no black masking rectangle, no image-edit artifacts, no marketing/product text, no fake logo, and no readable branded text on the touchscreen or print bed.
3. Keep the dark front glass door visibly closed while preserving enough realistic visibility of the chamber, print head, and print bed for mechanical reference.
4. Create matching metadata at exactly:
   `assets/generated/antigravity/p2s_reference_front_right_3_4_rev2_metadata.json`
   It must contain the correct task ID, actual generation tool, actual prompt, dimensions, format, limitations, and inferred/hallucinated geometry for the REV2 asset.
5. Update the existing Doop frame `AG · P2S Reference · Front 3/4` to use the REV2 asset. Do not create a duplicate frame. Return the existing canvas ID and frame ID.
6. Write the normal bridge response at:
   `bridge/outbox/TASK-003-REV2-antigravity-response.md`
   The response must point to the REV2 asset and matching metadata, and must mark this task `completed` only after all deliverables are consistent.

This is attempt 3 of 3. Do not create TASK-004. Codex will approve or block STAGE-003 after the final review.
