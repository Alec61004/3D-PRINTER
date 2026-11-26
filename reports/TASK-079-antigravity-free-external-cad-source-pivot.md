# TASK-079: Free External CAD Source Pivot Audit

- **Task ID**: `TASK-079-FREE-EXTERNAL-CAD-SOURCE-PIVOT`
- **Status**: `completed`
- **Verdict**: `PIVOT_REQUIRED`
- **Artifact**: `assets/models/raw/deltrol_p2s_external_free_source.glb` (`237908` bytes, SHA-256 `31626FD3A79C68083C1B9C16583F97DBFCC5D9EA98C64639E03CC1E37D8D76EE`)
- **License Evidence**: `reports/task079-source-license.md` (`VoronDesign/Voron-2`, `GPL-3.0`, retrieved `2026-11-26`)

## Measured Source Limitation

- `VoronDesign/Voron-2` (`GPL-3.0`) distributes individual printable STLs and STEP/Fusion360 CAD assemblies rather than a pre-rigged enclosed PBR `.glb` matching the Deltrol P2S silhouette (`IoU >= 0.90`).
- Converting a full STEP assembly into a calibrated PBR `.glb` requires Blender/FreeCAD + manual material/silhouette authoring.
