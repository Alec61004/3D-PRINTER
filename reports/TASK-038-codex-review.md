# Codex audit — TASK-038 HYBRID REFERENCE + TRUE-3D EXPLORER

- **Reference hero audited:** `assets/source/printer-hero-reference-2026-11-23.png`
- **Explorer audited:** `assets/models/raw/deltrol_p2s_explorer_v6.glb`
- **Evidence read:** TASK-038 report, outbox response, and all four explorer screenshots.
- **Audit verdict:** `HYBRID_APPROVED_FOR_INTEGRATION`

## Reference hero

The source reference is unchanged and its SHA-256 matches the handoff (`2D8B25482C66E54FDA31073A6C5EA2382BE0F1AD709636FEC63064EF42E8D7E0`). It remains the only pixel-exact representation of the supplied screenshot and is therefore used for the default fidelity presentation.

## Explorer

The v6 GLB is a real connected 3D asset with the required contract nodes. The four submitted views show no detached panel, floating foot, white wedge or black bake triangle. It is suitable as an exploration asset, but it is not pixel-identical to the reference and must not be presented as such.

## Integration decision

Integrate two explicit modes:

1. Reference Fidelity: serve the locked reference-derived printer crop/image.
2. 3D Exploration: lazy-load the v6 connected GLB and allow the tested rotation cone.

This preserves exact visual fidelity and honest 3D interaction without conflating the two artifacts.
