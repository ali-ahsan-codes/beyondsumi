# Shared brush-and-ink workflow

Follow [scene-first cinematic production](scene-first-workflow.md) before finished generation: integrated shot master, matching supported views, storyboard/animatic/layout, reusable assets, action-driven poses and actual sound events. Derive layers from coordinated compositions; intact contextual panels are valid when separation adds nothing.

**Applies to Sumi Light and Sumi Dark.** The active catalogue is **Sumi Original, Sumi Light, Sumi Dark**. Read the selected style's palette rules: [Light](styles/sumi-light.md) or [Dark](styles/sumi-dark.md). This profile does not silently replace Sumi Original's separate direction.

Profile identifier: `brush-ink-on-twos-v2`.

This document adopts the user's supplied brush-animation specification as an **authored technical target**. It is not a claim that a renderer, shader, example film or review gate implements and passes every requirement. A selected implementation must be recorded per shot. A missing capability remains missing until it is built and reviewed; a configuration field or successful export cannot certify its pixels.

No film production, paid generation, model download, rendering or testing starts merely because this guide is read or revised. Preserve existing films and approved story, duration and voice records. In particular, previous Sumi films and their rejected or unfinished status do not become approved demonstrations of this profile.

## Onboarding and Teach Mode

Use the normal [onboarding](onboarding.md) and [memory](memory.md) flow. The welcome offers exactly Sumi Original, Sumi Light and Sumi Dark through the current single atlas; it explains free/paid requirements, detects available tools, offers ElevenLabs, Voicebox, supplied narration or no narration, and asks before missing third-party installations or downloads. A documentation task does not run setup or generate demonstration media. Preserve existing preferences and authorizations without repeating completed onboarding.

Teach Mode uses this same source budget, clock separation, whole-character protection and shot specification. Explain one story-relevant operation at a time, show its source/region and masks when a demonstration is authorized, and distinguish a diagnostic overlay from the clean image. The [historical lab](director-lab.md) and its implementation notes can supply bounded techniques, but its nine studies and the former four methods are not the current selector or certified Light/Dark films. Do not present a generic lab loop as a completed story.

## Direct the story before building effects

Follow [the director workflow](director-workflow.md), [duration contract](script-duration.md), [character integrity](character-integrity.md) and [production standard](production-standard.md). The director chooses the scene's emotional action, staging, focal subject, camera, atmosphere, transition and sound. Ask the user only for missing general choices or a required approval, not for routine technical direction already delegated.

Preserve approved wording, displayed text, runtime and required visible actions. If the complete story cannot fit its approved duration, present the actual full-length estimate and a concrete shorter alternative before dependent production; do not cut or accelerate it silently.

Build a [shot specification](../assets/templates/BRUSH-INK-SHOT.md) for each directed beat. The action presets below suit a decisive action scene. Grief, sleep, hesitation, shelter and gentle touch may need a restrained camera, a held complete pose and very small secondary motion. State why an effect is omitted. Do not force an impact, flash, whip, smear or particle stream into every scene.

## Drawing budget and scene coverage

The current profile is `brush-ink-on-twos-v2`. New Sumi films use 24fps with character animation exposed on twos. This supersedes the 4.0.0 60/12/8 profile and its fixed four-source/two-extreme cap for new projects. Preserve old projects and their recorded clocks unchanged.

Plan each shot around anticipation, action, contact and recovery. Establish who/where/why; show the effect of each important action before leaving it. When narration is chosen, connect each spoken event to a readable visual event. More stills alone are not more performance: use whole action drawings, meaningful breakdowns, expressions and supported angles. Add foreground/midground/background geography, weather and reacting props where they clarify the story. Avoid decorative density around contact or captions.

Set a shot-specific source and complete-pose allowance before production. Reuse checked masters and cycles; spend new drawings on changes that need them. No arbitrary source cap may force omitted action or warped anatomy. Changes to approved wording, duration or required events still need user approval; routine drawing allocation within delegated direction does not.

Count each distinct whole pose/expression/atlas region as a source, even inside one file. Record path, SHA-256, role, dimensions and region. Reused instances count once per shot; separate shots still inventory their use. Procedural states, render frames, source artwork and exposure slots are separate counts. Derived rig parts must come from a checked intact master with an assembled overlay, never independently generated limbs.

## The exposure clocks

| Clock | Current default | Meaning |
|---|---:|---|
| Output, camera, flowing ink, environment | 24fps | One deterministic frame clock. |
| Character pose, attached props, cloth and eligible edge activity | On twos, at most 12 changes/s | Evaluate one state for frames 0/1, another for 2/3, and so on. |
| Optional slower character edge variation | 6 or 12Hz | Must remain inside the paired exposure; 8Hz is not pair-aligned. |

A 60-second film contains 1,440 output frames and up to 720 two-frame exposure slots. This does **not** require 720 separately generated pictures: a cycle may reuse drawings; deliberate holds span multiple pairs; computed poses must be identified as source-derived articulation, not fresh hand drawing. Exporting unchanged stills at 24fps does not satisfy acting. Do not claim measured token savings from fps alone.

```js
const outputTime = frame / 24;
const exposure = Math.floor(frame / 2);
const characterFrame = exposure * 2;
const characterTime = characterFrame / 24;
```

Evaluate character translation, joint transforms, expressions, cloth, attached props and contour variation from that same character time. Use output time for camera and independent weather/ink. A shared contacting pair must use compatible clocks and transforms. Do not quantize only the torso while hands or feet drift on intervening frames. The bundled `assets/motion-core/exposure-clock.mjs` implements clock arithmetic; it does not generate drawings or certify anatomy.

For narration-led retiming, map the output-time exposure pair into story time **after** quantizing the output frame. Quantizing a stretched story clock can skip pairs or change a pose between frames of one pair. Quantize important contact/cut events deliberately and align audio to the actual output frame. Seed randomness; seeking and out-of-order evaluation must reproduce the same state.

The 24fps/on-twos definition is supported by Sharifuddin, Perumal & Hamid (2023), [Investigating How Frame Rates in Different Styles of Animation Affect the Psychology of the Audience](https://doi.org/10.33093/ijcm.2023.4.2.2). This supports exposure terminology, not a guarantee of quality. The accompanying Instagram reference was not accessible during the revision and is not claimed as a studied motion reference.

## Build real layers and protected complete characters

Use the depth arrangement as a consistent relative coordinate convention:

| Layer | Reference Z | Function |
|---|---:|---|
| Washi substrate and distant wash | −500 | Continuous paper; distant environment establishes scale and space. |
| Transparent midground | −150 | Trees, walls, ground structures or other story-specific surroundings. |
| Hero / shared interaction plane | 0 | Complete character drawings and their actual support/contact. |
| Foreground brush silhouettes | +150 | Framing and depth, with purposeful independent movement. |

Keep the paper grain in a constant output-space coordinate system across the cut. The distant wash can move behind it at its assigned parallax rate; the paper must not slide, boil or reset with every scene. Procedural paper may be cached once with a fixed seed.

Prepare complete character masters and whole action drawings first. Match identity, facing, proportions, body volume, lighting/value design, limb order, planted supports and shared contact. Never assemble independently generated limbs. Any permitted parts or rig must come from a checked complete drawing and retain a verified assembled overlay; a source-image budget does not waive these rules.

Distinguish camera motion from walking. Translating a held character while planted feet slide is not a walk. Parallax does not establish correct depth by itself. Contacting characters and their support plane need compatible transforms and occlusion.

Multiply pigment over paper, but provide meaningful transparency and holdouts. Multiply alone makes pale bodies transparent to dark objects behind them. Cars, branches or ground ink must not show through a face, hand, pale torso or planted limb. Review actual transformed frames, including the full approach/contact/release window.

## Internal movement and brush edges

Apply bounded UV or mesh motion only to masks where the artwork supports it: hair ends, loose sleeves, cloth, fur fringe and broken brush edges. Use the supplied wind expression as an adjustable starting recipe:

```glsl
uv.x += sin(uv.y * 8.0 - characterTime * 5.0) * 0.015 * windMask;
```

The amplitude is normalized UV distance and must be checked at the actual image scale; `0.015` is not automatically appropriate for every face-sized subject or crop. Taper masks smoothly. Lock faces, hands, rigid props, planted feet, grip points and contact boundaries. Moving only a free cloth edge must not drag the wrist or imply that a supported body is breathing through its shoes.

Use subtle seeded contour boil held on the character exposure grid at 6 or 12 Hz, approximately **2–2.5 output pixels at a 1080-pixel short dimension**. Scale pixel-based recipes with `min(width, height) / 1080` and inspect the final resolution. Apply boil to eligible ink edges rather than to the whole image or its internal features. A corpse, sleeping body or exact hand contact must not acquire involuntary motion from a global filter.

Use depth-aware particles only when they belong to the scene: rain, drifting petals, embers or ink droplets are examples, not mandatory decoration. Vary size, drift, opacity and depth deterministically. A particle overlay is not a substitute for the required action. Weather must be legible when the story depends on it, and shelter must block or change that weather causally.

## Pigment and material behavior

Keep expressive brush silhouettes, broken dry-brush marks, translucent washes, irregular feathered edges, fibrous paper and deliberate negative space. Black ink establishes structure; the selected style determines whether color is allowed.

For a wet wash, target an approximately **two-pixel rim measured inward from its boundary**, with about **25% lower luminance than the interior** where the value range permits it. Use the same resolution scale as other pixel-based effects. Retain a diluted shoulder and irregular fibers; avoid a uniform vector outline or concentric graphic bands. Dark interiors should not simply clip into featureless black.

A contour, shader field or Canvas deposit is an authored material approximation unless an actual fluid solver is implemented. Do not call displacement, a reveal mask or a changing opacity a measured physical fluid simulation.

**Flow, Wash, Mist, Kasure, Sketch, Print, Scenic and Noir** are compatible procedural behavior vocabulary: currents, pigment bloom, translucent atmosphere, broken bristles, contour activity, woodblock-like texture, layered scenery and stark silhouettes. They are not additional primary styles. Historical Sumi Brush, Living Ink, Drawn Acting and Sumi Graphic documentation can inform technique; it does not restore the former four-choice catalogue.

## Direct the camera from the action

Choose one dominant setup or an intentional held view, identify its subject and spoken or visual cue, and state its purpose. Plan anticipation, action, contact/impact and recovery. End a move with a readable hold where the story needs it.

Use supported views from the actual artwork. A flat card cannot reveal an unseen face, side or limb by being rotated in 3D. A new required view is a source-image decision and counts toward the budget. A beautiful still with only a slow pan or zoom does not satisfy the internal-motion requirement.

Available presets, adapted to the story:

| Preset | Authored target | Use and limits |
|---|---|---|
| Low-angle parallax push | Forward push, approximately 15° upward camera tilt; background `0.1×`, midground `0.5×`, hero `1×`, foreground `3.5×`; foreground blur follows its speed. | Use only if source perspective supports it. Keep shared support/contact transforms coherent. A quiet scene can use a smaller move or held endpoint. |
| Dutch-angle slash | Approximately 30° roll; about 400 scaled pixels along the action vector over 0.2 s; easing `cubic-bezier(0.16, 1, 0.3, 1)`. | A decisive, motivated action preset. Settle into a readable impact composition; do not use it to disguise a faulty pose. |
| Z-corridor flight | Recycle three instances of existing transparent mist or bamboo between `Z = +200` and `Z = −600`, varying scale and opacity. | Instances reuse sources. Use only scenery appropriate to the story; preserve a coherent travel direction and avoid obvious loops. |
| Awakening counter-zoom | Hero scale `+25%`, background scale `−30%`, with procedural radial brush marks around the perimeter. | A strong emotional or action emphasis. Do not stretch anatomy, disturb planted contacts or turn every quiet realization into an impact. |

When independent depth is chosen, it must be visible, purposeful and supported by coordinated sources. An intact contextual performance is also valid; do not force separation into unrelated layers merely to tick a depth box. The director may choose a restrained push, a detail view, a lateral environmental shift or deliberate stillness when the listed action presets would harm the scene. Record that choice and the visible internal/material action that carries the shot.

## Pose changes, transitions and recovery

Never crossfade two incompatible whole poses to fake a continuous body. Register the endpoints before planning a bridge.

For a fast, story-appropriate action, the dry-brush smear preset lasts **one or two output frames at 24fps (0.042–0.083s)**. Derive it from the outgoing character render pass, extend its transient ink silhouette by up to `2.8×` along the action vector, break it into bristle streaks, and expose the checked follow-through pose. The smear is abstract motion residue, not a new anatomical pose. Do not stretch a held face, hand, grip or planted body to supply missing acting. Gentle contact may use a registered exposure change and restrained local ink instead; if it reads as a jump, allocate the needed checked breakdown or resolve the direction.

Use scene transitions sparingly, for a stated story change:

| Transition | Target duration | Material action |
|---|---:|---|
| Ink flood | approximately 0.42 s / 10 frames | A noisy threshold expands from the actual action or scene-formation point, covers the required outgoing region, then recedes into the incoming scene. Carbon ink works in both styles; Light may use crimson, and Dark may use selective deep dark red when the story justifies that accent. |
| Dry-brush whip | 0.25 s / 6 frames | Directional blur of about 50 scaled pixels and irregular bristle slits cover the layer exchange. |
| Negative-space dissolve | 0.5 s / 12 frames | Outgoing pigment erodes toward bare paper; an irregular signed-distance ramp gathers the incoming silhouettes. This is material erosion/reformation, not a character-pose opacity crossfade. |

Author these with shaders or Canvas/math and reuse existing assets. The incoming scene must already have its planned internal motion when revealed. Prefer local propagation from the place the scene forms; a generic sideways wipe is not automatically ink. Full coverage is only required where the chosen transition needs to conceal a layer exchange. Same-world continuity can retain its wash without a new major transition at every shot or pose.

Retain the [24 authored ink mechanisms](ink-transitions.md) as a reusable geometry and propagation library, not 24 primary styles or a requirement to use 24 events in a film. Its drop bloom, sheltering arc, root branch, water lift and settled recession can support the selected transition or a quieter local scene change. Begin a typical 30-second plan with a few purposeful major events and use retained material for continuity; adjust to the story rather than a quota. Record the actual mechanism ID, origin, scale, seed, timing, cause and destination. Library density fields do not automatically composite correct characters, supply missing weather/action or satisfy this new technical profile's final-art review.

For a justified impact, the optional recovery package is:

1. Freeze the camera and main character action for **two output frames / approximately 0.083s**, while pigment and particles continue.
2. Exchange dark structural ink and light paper values for **one output frame / approximately 0.042s**. In Light, an explicit Cinnabar mask may preserve its red pigment; in Dark, preserve only the authored dark-red accent mask when used. The remaining Dark layers stay neutral.
3. After the hold, evaluate directional shake from the impact event clock: `amplitude * exp(-15 * t) * sin(frequency * t)`. Scale amplitude to output resolution and let it settle; do not move support points independently.
4. Reuse the character render pass for a quickly fading, dry-brush-broken ghost at `-velocity * 0.08`, with opacity no greater than `0.4`. Light may use red or indigo; Dark uses neutral grey/black or a localized dark-red accent with a story reason.

These are action presets, not compulsory decoration. State `omitted` with the story reason for quiet shots. Never add a physical impact or cause of death that the approved story did not contain.

## Sound, captions and evidence

Preserve approved voice wording, timing and natural speed. Use saved narration preferences and the existing approval flow. Default complete-film background music, ambience and effects to [local Python synthesis](python-background-audio.md) unless the user chooses another source or silence. Describe synthetic sound honestly.

Tie atmosphere and tactile sound to actual weather, material propagation, support and contact. Do not add a transition hit for every drawing change. Let grief, hesitation and recovery have purposeful quieter sound. Inspect final picture-to-sound timing and listen; waveform measurements are not listening.

Place complete-word captions in useful negative space after composing the scene. Protect faces, contact points, action paths and important props. A short brush reveal should finish early, leaving a stable reading hold. Caption movement and camera should not compete for the same attention.

Before a later authorized full production render, prove the hardest representative shot with final art. Review adjacent frames and normal-speed motion, actual support/contact/release, anatomy, occlusion, source count, independent depth, internal movement, palette, transition continuity, captions, audio and final runtime/controls. Check a fixed-camera monochrome view where it helps distinguish real motion from color or camera dressing.

Record **authored**, **implemented**, **rendered**, **visually inspected** and **accepted** as different states. Include source hashes, exposure/camera cues, effect settings or omission reasons, and the exact reviewed media. Mark unperformed playback or listening plainly. This document and the shot template do not initialize a passing review. Technical checks and project-specific production evidence are recorded separately.
