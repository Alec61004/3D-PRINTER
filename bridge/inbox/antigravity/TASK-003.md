---
task_id: TASK-003
owner: antigravity
status: completed
type: real_product_visual
created_by: codex
created_at: 2026-11-19T19:01:29+07:00
stage_id: STAGE-003
result_path: assets/generated/antigravity/
response_path: bridge/outbox/TASK-003-antigravity-response.md
---

# TASK-003 — REAL_PRODUCT_VISUAL

## Goal

Create one high-quality photorealistic visual reference for a real enclosed desktop 3D printer.

## Primary reference

Bambu Lab P2S.

This is an AI-generated visual reference, not official Bambu Lab photography and not CAD.

## Visual requirements

- Front-right 3/4 view.
- Entire printer visible.
- Silver/gray exterior.
- Dark front glass door.
- Touchscreen/display on upper-left.
- Print chamber visible.
- Print head mechanically plausible.
- Print bed mechanically plausible.
- Bright neutral studio background.
- Premium industrial product photography.
- No people.
- No marketing text.
- No fake logo.
- No sci-fi redesign.

## Required actions

1. Actually use the available image-generation capability.
2. Save the generated image into `assets/generated/antigravity/`.
3. Create metadata describing all of the following:
   - `task_id`
   - generation tool
   - actual prompt
   - image dimensions
   - format
   - limitations
   - inferred/hallucinated geometry
4. Create a Doop frame named exactly `AG · P2S Reference · Front 3/4`.
5. Return all of the following in the bridge response:
   - local asset path
   - metadata path
   - Doop canvas ID
   - Doop frame ID
6. Write the normal response to `bridge/outbox/TASK-003-antigravity-response.md` and update this task to `completed` after the work is done.

## Review and transition

Codex will review:

- machine proportions
- enclosure geometry
- screen location
- front door
- print bed
- print head
- mechanical plausibility
- visual hallucinations
- suitability for multi-view generation
- suitability as an Image-to-3D reference

The review result must be either `APPROVED` or `REVISION_REQUIRED`.

If `REVISION_REQUIRED`, Codex will create exactly one revision task for Antigravity using the existing asset and specific feedback.

If `APPROVED`, Codex will mark STAGE-003 completed and automatically create TASK-004 for STAGE-004. Antigravity must not create TASK-004 itself.

Maximum attempts: 3.
