# TASK-015 — Replace Procedural Hero With Reference GLB

## Finding

The previous Hero was interactive but did not visually match the reference because
`PrinterModel.jsx` constructed a simplified procedural enclosure from `RoundedBox`
and primitive meshes. The existing `public/models/deltrol_p2s_optimized.glb` was
never loaded.

## Change

- Replaced the procedural printer body with the existing GLB asset.
- Preserved the shared contracts for camera presets, glass visibility, print-head
  motion, bed travel and clipping-plane simulation.
- Enabled mesh shadows and cloned embedded materials per model instance.
- Kept the 2D photoreal fallback unchanged.

## Verification

- `npm run build`: passed.
- Local GLB load: passed at `http://127.0.0.1:5173/`.
- Browser console: no errors or warnings observed after loading the model.
- The rendered Hero now exposes the asset's enclosure, door, gantry, print bed,
  spools, nozzle and internal assemblies instead of the old simplified box model.

## Remaining

The GLB is now the correct technical source, but final visual matching against the
Vercel reference still needs a desktop screenshot pass for camera framing, color
balance and scale. Those are tuning items, not a missing-model problem anymore.
