# GLB repair harness

The technical GLB path is reproducible through `tools/glb-repair-harness.ps1`.
It is the Codex-owned handoff for geometry changes after Antigravity reports that
materials and lighting are acceptable but the mesh is still wrong.

## Repair run

From `C:\Users\PC\Downloads\3DPrinter`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 -Action repair
```

The harness backs up the existing GLBs, runs the builder, validates both glTF 2.0
files, checks required scene nodes, verifies source/public hashes, and runs the
website production build. It writes `reports/glb-pipeline-latest.json` and
`reports/glb-pipeline-state.json`.

To integrate a new asset from Antigravity instead of regenerating the legacy
procedural mesh, pass `-InputGlb`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 `
  -Action repair -InputGlb assets/models/raw/deltrol_p2s_unibody_pivoted.glb
```

Build success is not visual approval. A fresh screenshot must be compared against
`assets/source/printer-hero-reference-2026-11-23.png`.

## Record the visual gate

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 `
  -Action record-audit -Verdict REVISION_REQUIRED -ScreenshotPath reports/hero-3d-revision-1440x900.png

powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 `
  -Action record-audit -Verdict PASS -ScreenshotPath reports/hero-3d-revision-1440x900.png
```

Three consecutive `REVISION_REQUIRED` audits set `pivotRequired: true`. A later
repair is blocked until the team chooses a different route, such as a new
multi-view asset, a real beveled Blender mesh, or another model-generation path.

Check the current gate with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\glb-repair-harness.ps1 -Action status
```
