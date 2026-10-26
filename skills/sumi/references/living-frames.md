# Living Frames — selective cinematic motion

Shared addition,24October2026. Read alongside [scene-first production](scene-first-workflow.md) and the selected style guide. Preserve the existing renderer, image-first action preparation, narration and sound system. `living_frame` is a shot strategy, not a fourth style or a requirement for every shot.

Use it for listening, watching, thought, emotional close-ups, anticipation and atmosphere when small acting carries the shot. Use `whole_pose` for substantial locomotion/action, and `mixed` when major action settles into a living frame. A frozen picture with a zoom does not qualify. Establish what changes emotionally and physically before choosing movement.

Read [expression and action continuity](expression-and-action-continuity.md) for emotion-led primary acting, supported face/hand changes and whole-film target coverage. Secondary motion never supplies missing primary action.

## Master and motion plan

Reuse an approved complete scene with correct perspective, identity, lighting, furniture, contact and occlusion. Choose one/two primary details, up to two supportive motions, optional scene-specific atmosphere and a motivated camera move or intentional camera stillness. Not every layer should move. Record targets, anchors, amplitudes, event times/settle, protected face/grip/support/prop regions and expected consequences in the shot record. Independent phases avoid synchronized wobbling; allow deliberate complete stillness when it carries meaning.

Prefer compatible approved master → existing expression/pose → safe source-derived layers/rig → local Python/renderer articulation → appropriate procedural atmosphere → existing style-compatible camera/transition → targeted new art. Do not regenerate a whole scene to move hair. If extraction exposes hidden pixels, derive a clean plate/inpaint only that area. Keep source/master/mask/plate hashes and registration. If separation cannot preserve the painting, use another supported motion or a targeted correction. Never leave seams, floating fragments or invented anatomy.

The bundled [motion sampler](../scripts/living_frames.py) supplies deterministic timing/displacement parameters; it does not find hair/eyes or create a rig automatically. The [planning validator](../scripts/validate_living_frames.py) checks evidence and cadence, not pixel/anatomy quality. The [Canvas micro-motion adapter](../assets/motion-core/living-frame-canvas.mjs) can reuse the current Canvas/Remotion renderer for bounded hair/cloth/breath patches; Python parameters support other engines. Use `validateTargets` with authored protected regions before drawing. Patch borders are fixed, and the entire patch is resampled without exposing hidden pixels; this does not replace clean plates for independent layer extraction or an expression rig. Re-author/review targets for every changed source pose/view: do not reuse coordinates blindly across sheets. An adapter in the existing renderer must apply the authored masks/mesh/expressions. Test actual composed frames and normal-speed playback before reusing a motion.

## Behaviours

- **Hair:** scalp fixed; only selected tips/loose strands move, with tapered displacement, staggered phase, gust and settling. Never translate the entire hairstyle rigidly.
- **Cloth:** fix seams/shoulder/waist attachment and grips; move loose sleeve/scarf/coat regions at different amplitudes. Tight fabric moves less. Do not move the body to simulate fabric.
- **Breath:** minute chest/collar/shoulder response, emotion-specific rate; protect neck/head/hands/seat/feet. No whole-picture bob.
- **Eyes/face:** intentional blink times with close/hold/open phases, authored gaze/eyebrow/tension states. Irregular timings, not a metronome. Never deform an eye into a blink without a supported closed-lid drawing/rig. Tears and trembling should follow emotion and settle.
- **Environment:** only details belonging to the scene—rain, cloud, dust, smoke, leaves, ripple, fire or light. Preserve indoor/outdoor geography and protected caption/face visibility. No automatic ink boil on Original characters.
- **Camera:** supported slow push, track, reframing, depth/focus shift or stillness. A new angle needs matching art; parallax needs valid layers/hidden pixels. Camera/light/weather changes do not count as character states.

## Cadence and counting

**Original:**30fps output,20 designed character states per animated second, normally alternating two/one output-frame exposures. State boundaries are `ceil(k*30/20)`; `floor(frame*20/30)` selects the state. Complete drawings and supported source-derived acting can supply these states. Count new image calls, source drawings/regions, derived character states, cycle reuses and output exposures separately. Twenty state evaluations, renamed files, empty parameter changes or camera/texture-only changes are not20 new drawings. A five-second living frame does not need150 newly generated illustrations. Deliberate stillness is labelled and reviewed, not used to omit required action.

**Light/Dark:**24fps/on-twos, up to12 character state changes/s, with motivated longer paired holds. Shared selective-motion preparation does not change the rate or impose20 states on these styles. Camera/environment/material can follow the output clock independently; this never means a transition on every frame.

Preserve identities: Original pure painted Sumi-e/Sumi Anime, clean edits/mist and no animated splash treatment; Light colourful storytelling/documentary brush/ink, clear explanation; Dark broad splash-built forms, stronger camera-led drama, neutral ink with selective dark red. Local ink motion follows existing story events and reading intervals, not every frame by default.

## Review and savings

Inspect original vs derived frame, scalp/cloth anchors, face/grips/feet, clean plate exposure, edge seams, entry/exit and occlusion at extrema and actual export. Review whether the selected detail communicates feeling, whether holds advance the story, and whether repeated cycles are visibly distracting. Check actual source counts before claiming savings. Cadence/provenance checks alone cannot certify smooth motion, acting, physics or sound.

Environmental motion: use [the shared living-environment plan](living-environments.md) before rendering. Select local story-led motion or deliberate stillness, retain this style’s palette/cadence, and bind effects/masks to each actual source.
