# Persistent Visual Acceptance Policy

## Owner of the loop

Codex owns the review loop and the final visual verdict. Antigravity is the execution partner: it creates or revises visual assets, GLB files, textures, and screenshots according to a task. An Antigravity completion message is a handoff signal, not proof of acceptance.

## Required loop

For every handoff, Codex must:

1. Read the task file, report, outbox response, artifact manifest, and newest screenshot.
2. Compare the rendered result against the reference at the same viewport and camera angle.
3. Audit silhouette, proportions, primary geometry, materials, lighting, camera, and required interaction/asset contracts.
4. Mark the result accepted only when the visual evidence supports it.
5. If it is not close enough, issue the next revision task in the same stable Antigravity session and keep the loop active.

## Handoff state machine

`in_progress` means the executor is still working. Once the report, outbox response,
artifact and screenshot are written, the executor must close that handoff with a
terminal task state and `completed_at`: use `completed` plus
`verdict: REVISION_REQUIRED` or `verdict: BLOCKED` when Codex still has to audit or
continue, and reserve `PASS` for Codex's own audit. Keeping a ready handoff at
`in_progress` prevents the completion watcher from waking Codex.

## Three-strike meaning

Three consecutive revisions without meaningful improvement only retires the current approach. It does **not** stop the project or the acceptance loop. Codex must pivot to another asset, reconstruction method, pipeline, or reference set and continue until the target is accepted or a concrete external blocker is documented.

## Stop condition

Never stop merely because a build passes, a model loads, a model rotates, or an agent reports `completed`. Stop only after Codex's own audit records an evidence-backed `APPROVED`/`PASS`. If the result is not accepted, the next action must be a revision or pivot task.

## Persistence

This policy is part of the workspace source of truth. Read it together with `AGENTS.md` before continuing or closing a visual task, including after a long idle period or when resuming from a new conversation.
