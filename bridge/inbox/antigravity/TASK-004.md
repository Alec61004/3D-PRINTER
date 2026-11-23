---
task_id: TASK-004
parent_task_id: TASK-003-REV2
stage_id: STAGE-004
owner: antigravity
status: completed
type: multiview_reference
created_by: codex
created_at: 2026-11-19T19:40:21+07:00
max_attempts: 3
result_path: assets/generated/antigravity/multiview/
response_path: bridge/outbox/TASK-004-antigravity-response.md
---

# TASK-004 — MULTIVIEW_REFERENCE

Create a consistent multi-view reference set for the same enclosed desktop 3D printer from the approved STAGE-003 asset:

`assets/generated/antigravity/p2s_reference_front_right_3_4_rev2.jpg`

## Requirements

- Preserve the approved printer identity, proportions, silver/gray enclosure, dark closed front glass door, upper-left touchscreen, chamber, print head, and print bed.
- Generate consistent views suitable for Image-to-3D preparation: front, rear, left, right, top, and a matching front-right 3/4 anchor view.
- Keep camera scale, lighting, neutral studio background, materials, and geometry consistent across views.
- Do not introduce logos, marketing text, people, sci-fi redesigns, or contradictory geometry.
- Save all generated images and metadata under `assets/generated/antigravity/multiview/`.
- Metadata must include task ID, generation tool, actual prompt(s), dimensions, format, limitations, and inferred/hallucinated geometry for each view.
- Create corresponding Doop frames with `AG · P2S Multiview · <View>` naming and return each local asset path, metadata path, canvas ID, and frame ID.
- Write the normal bridge response to `bridge/outbox/TASK-004-antigravity-response.md` and mark this task `completed` when all deliverables are ready.

Codex will review cross-view consistency and return `APPROVED` or `REVISION_REQUIRED`. Do not create TASK-005; Codex advances the workflow after review.
