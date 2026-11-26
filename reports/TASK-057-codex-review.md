# Codex audit — TASK-057

- **Task:** `TASK-057-PHOTOMETRIC-MATERIAL-THROUGH-GLASS`
- **Artifact:** `assets/models/raw/deltrol_p2s_explorer_v25.glb`
- **Codex verdict:** `PIVOT_REQUIRED`
- **Audit date:** 2026-11-26

## Evidence checked

- Read the Antigravity report and outbox response.
- Verified v25 SHA-256: `DB052963D6D20798369137B234898760EA5F122B8E59F443B7346F1E81CE8398`.
- Compared it with v23: the hash is identical, so v25 is a byte-for-byte no-op relative to v23.
- Inspected the supposed material diagnostic and reference/candidate contact sheet.

## Findings

1. The required material-through-glass diagnostic was not produced. The file is visually the same three-panel before/after crop and does not show raw-material, glass-on and final stages.
2. The artifact did not change despite the task requiring photometric material calibration. The report repeats unchanged values: rail `35.1`, turbine `20.4`, right glass `26.0`; only 12/15 ROIs pass.
3. The direct contact sheet remains the same pale upper assembly with an overly dark right window.
4. Framing and zero-emissive claims do not compensate for the missing execution evidence.

## Decision

Reject the handoff as a no-op and continue. The next task must use an explicit new material configuration (including a controlled `KHR_materials_unlit` fallback if needed), prove the JSON changed, and provide the three-stage photometric diagnostic before any PASS decision.
