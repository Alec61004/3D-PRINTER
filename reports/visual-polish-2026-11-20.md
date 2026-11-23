# Visual polish pass — Deltrol Image-to-3D

Date: 2026-11-20
Owner: Codex

## Changes

- Reworked the viewer presentation into a darker industrial product-showcase treatment so the silver enclosure and glass door read clearly.
- Added a lit presentation floor, stronger key/fill lighting, ACES tone mapping, shadows, and mesh shadow flags.
- Expanded the procedural GLB with enclosure base/fascia, door stiles and handle mounts, fan hub/slots, bed mounts, Z guides, carriages, toolhead cooling detail, screen chin, and interior light bar.
- Added product lockup, reference tag, technical-view label, clearer status hierarchy, dark viewer controls, and feature bullets.
- Preserved all existing rotate, zoom, pan, reset camera, auto-rotate, loading/error, and printer-animation behavior.

## Verification

- `npm run build`: passed.
- Optimized GLB: `assets/models/optimized/deltrol_p2s_optimized.glb` — 103,544 bytes.
- Served GLB matches optimized GLB SHA-256: `30d740464d65fb95d5345fdfa9bfa72feaaa77d9aa6fab2a470b4cc336afab1d`.
- Local preview loaded successfully at `http://127.0.0.1:4173/` with model status `READY`.

## Scope note

This is a Codex-owned presentation and technical polish pass. Antigravity-owned visual assets and Doop frames were not modified.
