# Motion recipes for Sumi variations

Current routing: apply [animation-categories.md](animation-categories.md) and the selected style guide first. These mechanics are implementation options, not complete category proofs. Existing lab clips do not certify Bloom Flow, dense Mist, TV-like Grain, Wash-family Print/Noir or Scenic 2D/3D acting.


The reference appearance does not identify the original toolchain. These are our code-rendered adaptations. Pick the simplest renderer that supports the shot; the independent Remotion bundle handles timing, captions, sound and export. A raster illustration may provide texture and detail while code owns transforms, masks and interaction.

## Coordinate and material contract

For every moving layer record bounds, pivot, parent, depth, alpha, hidden-area coverage and intended material. Keep scene geometry in design pixels or world units. Apply parent transforms once. Keep surface paper stable in screen space if it represents the film substrate; keep pigment/grain and garment pattern in the painted object's coordinates. Parent mask, shadow and attached prop to the same transformation where appropriate.

## Timing

Use absolute frame/seconds. A useful smooth transition is `s(u)=u*u*(3-2*u)` for clamped u in [0,1]; quintic easing also makes acceleration continuous at the ends. Easing is not physics. Use it for directed poses/camera; use a trajectory with known velocity for released objects. Do not ease an airborne object to a stop before contact.

Choose start/end poses, event times and any holds from story rhythm. A spring is useful for a light flexible detail, but inappropriate as a universal entrance. Motion blur or drawn smears can support fast movement; they cannot conceal a missing contact pose. Review at final frame rate and closely around contact, not only at polished keyframes.

## Attach, detach, settle

Before detach time, compute world position from the moving parent anchor. At detach, preserve position and inherit the anchor's velocity. Afterwards use gravity and drag. Solve or bracket the first floor contact; clamp to contact and animate an appropriate settle, not an endlessly penetrating trajectory. Particles and sound share the event. For held props, ownership changes at an explicit handoff; there must never be a duplicate still attached to the previous hand.

For cloth/branches, roots are fixed in the correct parent space. A designed curve is often adequate. For simulation use fixed steps, length constraints and damping, bake from a known initial state and interpolate cached samples. Seek order must not affect the frame. The old prototype's history-dependent cloth is not a reusable implementation.

## Stance and anatomy

A two-link IK solver keeps segment lengths while a stance foot remains fixed. Clamp reach within the limb's feasible range and place hips accordingly; do not stretch a leg to hide an unreachable target. Choose the bend side deliberately. Switch contacts with overlap and a visible weight transfer. A good numeric constraint does not prove a natural gait; inspect the silhouette and balance. Use additional drawings for foreshortening and major turns.

## Brush, grain and masks

Cache a seeded material tile or texture. Reveal a pressure-varying ribbon by arc length, keeping its bristle offsets coherent. Put granular shading inside a clean shape. For soft ink, keep core/edge layers separate and protect focal details. Render large layers once where possible; avoid several full-resolution turbulence filters on every character each frame. Measure performance with actual delivery resolution and assets.

Morph only compatible shapes with intentional point correspondence. Use an occluding brush mass, match cut or authored intermediate for incompatible subjects. Inspect the middle of every transition for duplicate faces, empty holes, edge halos and lost direction.

## Bundled implementation probes

`assets/motion-lab/motion.mjs` provides pure timing, seeded randomness, exact two-link IK and a branch-release trajectory with continuous position/velocity and persistent floor contact. `studies.mjs` renders nine original schematic studies on Canvas. `test-motion.mjs` checks numerical continuity, reachable IK lengths and deterministic rendering inputs. Run:

```sh
node assets/motion-lab/test-motion.mjs
python3 -m http.server 4193 --bind 127.0.0.1 --directory .
```

Run from the Sumi skill folder. Open `http://localhost:4193/assets/motion-lab/` in Chrome. Choose each study; play, pause, seek and replay. `?style=wash&t=3` opens a paused review frame. The studies are silent on purpose because they test motion mechanisms; complete films still use the default Python score/effects and the selected narration route when requested. They contain no external assets, credentials or network dependencies.

These probes demonstrate bounded mechanics and rendering routes, not nine finished stories or full fidelity to the reference films. A film must pass its own [graphics, physics, audio, runtime and export review](production-standard.md#review-gate-before-publishing-or-calling-a-film-final).

## Production contact helpers

The additional [motion-core](../assets/motion-core/motion-core.mjs) library covers scale-aware world-space feet, two-link IK with unreachable-target reporting, full attachment transforms, release momentum, a sampled blade sweep and a deterministic drag/flutter petal bake. Its [tests](../assets/motion-core/test-motion-core.mjs) check these specific invariants. Choose subframe resolution and collider detail for the actual shot. The earlier motion lab remains a mechanism teaching asset; neither library nor lab proves film quality. Apply [physics-and-review.md](physics-and-review.md) to finished shots and use separate style direction from [motion-direction.md](motion-direction.md).
