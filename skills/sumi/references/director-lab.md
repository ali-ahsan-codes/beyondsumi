> Historical nine-study lab (2.2.0). It remains a bounded mechanism experiment, not proof of Sumi Original, Sumi Light, Sumi Dark or corrected character anatomy. Its archived controls are not the current three-style selector.

# Director lab, Teach Mode and material mixing

Run `python3 scripts/serve_director_lab.py --port 4198` from the installed skill, then open the printed **127.0.0.1** address in Chrome. The server binds only to loopback. No dependencies, voice models, API calls or uploads are needed. The lab is silent. It is a local training/implementation tool, not the requested film itself.

The nine original studies use 13 separate authored SVG image assets and independent scene functions: Sumo planted reach, Wash deposited/advected ink, Grain scale-to-gaze, Print botanical plates, Noir a travelling light reveal, Mist a subject discovered through fog, Sketch invitation/received gaze, Flow pool-to-heron pigment and bristles, Scenic projected painted cards with a small character gesture. These are **bounded mechanism examples**. The full style definitions require richer story-specific acting, illustration, editing, sound and proof than these examples provide. Never deliver them as a finished story or claim Pinterest-level quality from them.

Teach Mode follows the same five-step [image-first workflow](image-first-workflow.md), with linked source artwork and style-specific strict/economical decisions. Use the timeline, exact time + Go and one-frame advance to inspect transitions. The clean preview/save excludes diagnostics. Normal playback uses elapsed time and can skip preview frames on a slow machine; deterministic `renderFrame(time, options)` supports exact sampling. This is not an MP4 exporter. Use the existing film/Remotion workflow for complete production.

## What actually runs

| Mechanism | Implementation and inspection | Boundary |
|---|---|---|
| Core | One clock, style-specific pose exposure, higher-cadence critical Sumo reach, analytical IK, deterministic material replay | Not a universal animation/physics solver; project actions need their own rigs/poses |
| Sumo | Image body, independently reached arm, anchored authored cloth curve; actual targets/support markers | Cloth is a directed curve with decaying oscillation, not a full collision-aware cloth simulation |
| Wash | CPU fixed-step 80×45 semi-Lagrangian advection, pressure projection, vorticity confinement and positive anisotropic diffusion tensor; actual four-buffer inspector | Low-resolution approximation; no GPU ping-pong FBOs, exact paper fibres or full Wash choreography claimed |
| Grain | Seeded progressive best-candidate 64×64 rank tile, object surface stipple, subdued temporal offset noise, real Bayer and white-noise comparisons, 800% loupe | Blue-noise approximation; no certified spectral distribution, rotating CMY print screens or proprietary texture array |
| Print | Three actual image plates, Multiply compositing and fixed-step damped registration lag; isolated/exploded plate views | Multiply is a practical pigment approximation, not Kubelka–Munk; the exploded diagram is a teaching layout |
| Noir | Value threshold, Sobel-oriented edge hatching and colour mask, actual luminance histogram/threshold/colour bounds | CPU mask routing rather than GPU stencil; no physically derived rim light or bloom pass |
| Mist | Soft imagery, procedural layered opacity, domain-warped fBm, advected subject wake; actual opacity layers and wake inspector | 2D procedural fog, not volumetric 3D raymarching; layer bands approximate depth |
| Sketch | Image bodies, arm IK, reachable endpoint, line weight by arm extension, time-derived construction echoes, movable gaze target | Echoes are recomputed from the clock, not a mutable history ring buffer; line tension is a visual mapping |
| Flow | Image-alpha-derived approximate jump-flood SDFs; boundary interpolation, field-driven edge variation, edge pooling and coherent curved bristle strands; actual SDF/curl views | Designed capillary/coffee-edge approximation; Canvas paths, not GPU triangle instancing; more drawings required for complex figurative acting |
| Scenic | Explicit card positions/depth, perspective projection, depth grading/soft distant layers, character gesture, orbitable diagnostic stage and camera frustum | Honest 2.5D; no full 3D character, geometry engine or painterly bokeh shader |
| Material blend | Nonnegative normalized nine-way weights mix effects on one primary scene. Automatic Sketch → Noir material transition | Does not mix two finished movies by opacity or invent hybrid choreography. The primary director remains fixed; a production hybrid still needs its own approved motion plan |

The CPU/Canvas backend was chosen for a dependency-free, inspectable first implementation and small reusable image fields. It is **not** a claim that every proposed GPU technique has been implemented. Scale up a specific bottleneck only when measured, with a representative shot and the same visible quality checks. All source behavior is original code adaptation; reference studios' solvers, cadence and pipeline are not verified.

The underlying methods are informed by [NVIDIA GPU Gems' stable-fluid description](https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-triangles/chapter-38-fast-fluid-dynamics-simulation-gpu) and [Rong and Tan's approximate jump-flooding work](https://www.comp.nus.edu.sg/~tants/jfa.html). This implementation uses CPU arrays for these methods; [WebGL2](https://registry.khronos.org/webgl/specs/latest/2.0/) is an available future backend, not a dependency or current capability claim.

## Reuse and verify

Import `DirectorEngine` from `assets/director-lab/engine.mjs`, instantiate with an 800×450 canvas, await `init()`, then call `renderFrame(seconds, {style, weights, economy, ...})`. The bundled scenes are bounded to 12 seconds. `diagnose(otherCanvas, options)` writes a separate teaching view. Replace/extend scene functions and assets for a new film instead of stretching a study to fill narration. For production assets/proofs, use `scripts/validate_shot_plan.py` at the workflow gates; it checks structure/files, not visual quality or human consent.

Run `node assets/director-lab/test-core.mjs` and `python3 scripts/test_shot_plan.py` for numerical/contract regression. Recheck UI controls, exact seeking, normal playback and exported film separately when changed. A saved PNG, source inspection or successful encoding cannot establish smoothness or completed filmmaking.
