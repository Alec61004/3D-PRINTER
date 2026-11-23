---
task_id: TASK-006
parent_task_id: TASK-005
stage_id: STAGE-006
owner: codex
status: completed
completed_at: 2026-11-19T21:23:49+07:00
summary: Built self-contained raw and browser-optimized GLB variants with embedded PNG textures, named logical part roots, centered meter-scale bounds, and local structural validation.
created_by: coordinator
created_at: 2026-11-19T20:02:00+07:00
request: Build and optimize the usable browser-safe GLB from the approved Image-to-3D preparation output.
result_path: assets/models/optimized/deltrol_p2s_optimized.glb
raw_result_path: assets/models/raw/deltrol_p2s_source.glb
report_path: reports/task-006-glb-build-and-optimization.md
response_path: bridge/outbox/TASK-006-codex-response.md
next_stage_on_completion: STAGE-007
---

# TASK-006 — GLB_BUILD_AND_OPTIMIZATION

Build a usable 3D model from the approved Image-to-3D preparation output:

- `assets/generated/antigravity/multiview/`
- `assets/generated/antigravity/multiview/p2s_multiview_metadata.json`
- `reports/task-005-image-to-3d-preparation.md`

## Required outputs

1. Preserve a source/raw GLB at:
   `assets/models/raw/deltrol_p2s_source.glb`
2. Write the browser-safe optimized GLB at:
   `assets/models/optimized/deltrol_p2s_optimized.glb`
3. Write a reproducible build and validation report at:
   `reports/task-006-glb-build-and-optimization.md`
4. Write the normal bridge response at:
   `bridge/outbox/TASK-006-codex-response.md`
5. Update this task to `status: completed` only after all required outputs and checks pass.

## Technical requirements

- Correct orientation with a consistent front/right/top convention.
- Centered origin and sensible real-world scale for browser presentation.
- Browser-safe GLB with valid buffers, materials, textures, and external-reference-free packaging.
- Optimize geometry and texture sizes while preserving the recognizable printer form.
- Keep source/raw and optimized outputs separate; do not overwrite Antigravity assets.
- Where practical, use logical named parts:
  `enclosure`, `door`, `printHead`, `printBed`, `gantryX`, `gantryY`, `printedObject`.
- Validate that the final GLB parses and loads successfully with a local technical check.
- Record limitations and any inferred geometry carried over from the AI reference set.

## Scope boundary

- This task authorizes GLB/model work, including Blender or equivalent local tooling if needed.
- Do not implement the website in this task.
- Do not create TASK-007 manually; the coordinator must create STAGE-007 exactly once after this task completes successfully.
- Do not mark the project `DONE`; the workflow must continue through STAGE-007, STAGE-008, and STAGE-009.
