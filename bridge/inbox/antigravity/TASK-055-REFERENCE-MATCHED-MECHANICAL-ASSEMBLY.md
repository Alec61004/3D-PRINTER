---
task_id: TASK-055-REFERENCE-MATCHED-MECHANICAL-ASSEMBLY
owner: antigravity
status: completed
verdict: PIVOT_REQUIRED
completed_at: 2026-11-26T09:19:05+07:00
created_at: 2026-11-26T10:10:00+07:00
request: >-
  Continue after TASK-054. v22 is a real changed asset but still visually fails:
  rail dMax=35.1, turbine dMax=20.4 and right-window glass dMax=26.0. Build a
  new independent mechanical assembly that matches the reference's compact
  warm-dark rail/gantry/toolhead/bed/turbine arrangement. Do not simply add pale
  bars to v22; the exact sampled rail/turbine pixels must visibly change while
  the right-window glass is restored.
result_path: assets/models/raw/deltrol_p2s_explorer_v23.glb
---

# TASK-055 — Reference-matched mechanical assembly

## Owner boundary

Antigravity owns the new interior mesh/material asset. Do not edit Codex-owned
website source. Use the fixed fixture and reference criteria.

## Required construction

1. Start from an independent mechanical assembly method, not a copy of v22's
   injected `cad_upper_rail_*` nodes. The report must identify the new source
   method and the newly modeled nodes.
2. Model the reference-visible upper assembly as a compact, warm-dark mechanical
   system: three horizontal steel/bronze rails with correct thickness and
   spacing, a centered carriage/toolhead with a dark intake face, and readable
   support hardware. Avoid the pale generic bars and black circular artifact
   visible in v22.
3. Model the lower bed/turbine as a compact dark graphite bed with a warm bronze
   printed arch/turbine in the reference position and scale.
4. Keep all rail/turbine materials non-emissive. Use viewer-driven color and
   contrast; no projected screenshot, billboard, image plane, or 2.5D cheat.
5. Restore the right-window glass to the accepted warm smoked appearance and
   preserve the outer shell, pillar, door/handle, console and framing.

## Mandatory preflight and evidence

- v23 SHA-256 and node/mesh inventory must differ from v22.
- Report exact nodes/primitives/materials used by every sampled rail/turbine
  region and prove no emissive contribution in the actual GLB JSON.
- Before rendering, compare the sampled rail/turbine ROI pixels against v22 and
  stop/rework if they are byte-for-byte unchanged.
- Produce:
  - `assets/models/raw/deltrol_p2s_explorer_v23.glb`
  - `reports/task055-explorer-front.png`
  - `reports/task055-explorer-left20.png`
  - `reports/task055-explorer-right20.png`
  - `reports/task055-explorer-elevated.png`
  - `reports/task055-explorer-4view-sheet.png`
  - `reports/task055-reference-candidate-contact-sheet.png`
  - `reports/task055-mechanical-before-after.png`
  - `reports/task055-silhouette-overlay.png`
  - `reports/TASK-055-antigravity-reference-matched-mechanical-assembly.md`
  - `bridge/outbox/TASK-055-REFERENCE-MATCHED-MECHANICAL-ASSEMBLY-antigravity-response.md`

## Acceptance gates

- rail ROI near `(114,93,80)`, `dMax <= 15`;
- turbine ROI near `(109,88,73)`, `dMax <= 15`;
- right-window glass `dMax <= 15`;
- centered IoU `>= 0.90`, exterior silhouette retained;
- direct contact sheet clearly resembles the reference's upper mechanics and
  lower printed object;
- the direct before/after must show a real change in the sampled mechanical
  pixels, not only a changed hash.

If the independent assembly still fails, report `PIVOT_REQUIRED` with the next
source strategy; do not repeat v22's pale-bar construction.
