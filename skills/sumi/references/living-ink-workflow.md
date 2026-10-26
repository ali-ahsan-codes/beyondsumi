# Living Ink — preserved material technique
> Technique reference, superseded as a primary style. The active styles are **Sumi Original, Sumi Light, Sumi Dark**. Combine the useful paper, pigment, weather, camera, acting, caption and sound lessons below with [the current brush-ink profile](brush-ink-workflow.md). For Light/Dark that profile overrides this historical guide's one-accent limit, drawing-budget suggestions and cadence prescriptions: Light may use selected mineral colours; Dark uses a neutral base with selective dark red under its current style guide. Do not offer Living Ink as a fourth style or treat its unfinished film as a passed example.

Current production authority: [24fps with character animation on twos](brush-ink-workflow.md). Older numerical drawing caps/cadences below are historical guidance when they conflict. Plan enough checked drawing states for the actual action and keep source count separate from exposure count.

Current Living Ink direction, 20 October 2026. Read this when `living-ink` is selected. The other three Japanese Sumi methods remain unchanged. This is a production workflow, not proof that a particular film has passed it.

## What makes it Living Ink

The wet pigment carries the scene: dense reservoirs feed diluted shoulders, uneven fringes advance into paper, masses gather or separate, and a prior mark has a visible consequence. Recognition anchors—eyes, hands, paws, a face or a meaningful prop—can remain dry and stable. Whole-pose acting may support the material, but it must not become an unchanged puppet behind a moving fog layer.

A birth matte alone is insufficient. Specify at least one meaningful **inside-shot change of mass, density or structure**, including its start, intermediate state and consequence. A road wash might gather into roots as a rescued puppy reaches a tree. That ink transformation complements the visible rescue; it cannot replace the required nudge or safe arrival.

**Make a movie, not illustrated slides.** Scene direction includes foreground/midground/background depth, purposeful camera framing and movement, environmental behavior and character response. The neutral fixed-camera proof is a diagnostic, not a restriction on the finished film's cinematography. A low view can make a puppy vulnerable; a closer supported view can emphasize touch; a wider travelling view can express companionship; stillness can serve grief. Use only angles supported by the actual artwork. Do not fake a new view by rotating a flat card, or repeat the same caption-column/figure-panel layout in every scene.

Tie important narration to **visible scene evidence**. If a line says rain, readable rain must fall in that scene: depth-varied streaks, puddle ripples, passing spray and wet surroundings can make it relatable. Shelter should visibly alter exposure to that rain. If the line says someone stops, show the attention/action change. For each important beat record the spoken time, required visible action, environmental effect, camera/framing, physical consequence and synchronized sound. The critic must check these in the rendered shot, not just in its written description.

Sumi Brush primarily deposits ordered strokes. Drawn Acting primarily changes complete poses. Sumi Graphic primarily transforms visual relationships to explain something. Living Ink primarily evolves pigment masses. These distinctions must survive a fixed-camera, black-on-white proof.

## Story first, then one material direction

1. Identify the protagonist, emotional turn, required actions, important words and approved duration. Preserve the user's actual narrative. Choose where to hold, where a physical action must be readable, and where an ink metaphor can connect scenes.
2. Pick one accent **from its meaning in this story**. Crimson can mean danger, resolve or a recurring object; gold can mean care or warmth. Neither is compulsory. Explain its first appearance, recurrence and absence. Do not introduce multiple unrelated colours.
3. Keep black, charcoal and paper dominant. Approximately 85% monochrome / at most 15% accent is a directional composition target, not a forced pixel quota. Aim for 30–40% useful blank paper or very pale wash; a close detail or transition can briefly differ. Judge silhouettes and legibility, not a fabricated numerical score.
4. Use one high-resolution original rice-paper substrate for the whole cut. Keep its grain in screen space while scene layers move. Wash pigment off that same sheet; do not flash a new paper texture at each scene boundary.
5. Present script, story-specific staging, camera, material transitions, sound, duration and costs. Follow the user's approval/delegation and the duration contract. A generic example or source technique is not a new story or permission to change the runtime.

## Image preparation

Save complete character masters, alternate views and necessary **whole interaction poses** before animation. Compare identity, body proportions, facing, near/far limbs, joints, hands/paws and support. Never assemble unrelated generated limb fragments. A prompt suffix is a useful reminder, not an identity guarantee. Use the actual master as a reference and inspect every changed pose.

Separate four layer roles:

| Role | Prepare | Motion rule |
|---|---|---|
| Paper | One original high-resolution texture | Stable grain throughout; it does not swim with the camera. |
| Environment | Sparse wash forms, paths, roots, branches or architecture | Local pigment evolution and restrained depth/parallax where meaningful. |
| Subject | Complete checked poses and props, including contact states | Purposeful pose changes plus localized material motion; protect recognition/contact regions. |
| Foreground | Necessary particles, ink events and typography | Event-driven movement with direction, lifetime and consequence. Leave this role empty when unnecessary. |

White-background drawings can be composited with Multiply: ideal white is neutral and grey/black darkens the underlying layer. It is **not alpha transparency**. Pale character interiors may allow the background through; use appropriate holdouts/occlusion masks where the body must block it. Off-white backgrounds can leave a rectangle. Correct the actual background while preserving light washes and anti-aliased edges; do not blindly clip every asset at input level 235. Test over both light and dark scene regions. [Adobe's blend-mode documentation](https://helpx.adobe.com/my_en/after-effects/desktop/work-with-layers/work-with-layer-blending-modes/blending-modes-layer-styles.html).

A reusable original-art prompt suffix can describe: traditional Japanese ink wash, pressure-varied brush marks, dense black cores, translucent charcoal washes, restrained broken contours, carefully reserved white shapes, one specified accent and no glossy digital finish. Pair this with explicit subject/reference/pose constraints. Do not force historic costume onto a contemporary story. Reference-artist names, AI-video instructions and claimed generation times in supplied material are source proposals, not mandatory execution commands.

## Few drawings, distinct motion

Use [the balanced drawing and camera standard](animation-density-and-camera.md) to avoid under-animating scenes. Economy means a sufficient set of meaningful poses and focused reuse, not a fixed tiny count for every action. Plan short micro-reactions, intermediate movement and settling; map character focus/framing to actual spoken cues. Additional whole drawings support Living Ink's evolving material rather than replacing it.

Separate four quantities in the plan: unique drawings, drawing exposure, material simulation cadence and encoded output fps.

- Use a nominal **8–12 drawing exposures per second**, with deliberate longer holds where appropriate. Two or three poses can work for a blink, breath or offered hand. A change of view, rescue contact or weight transfer may need more drawings.
- Pose A/B/C should express different meaningful states, not arbitrary outline noise. Do not loop a death, one-time rescue or acceptance gesture as if it were breathing.
- Keep line boil small and local. A generic displacement amount/evolution copied from another resolution can reverse fingers, float feet or melt a face. Lock recognition and contact regions; inspect adjacent frames after the final transform.
- Material can update at a separate cadence and be cached. Encode at an appropriate delivery rate such as 24 or 30fps; a higher output rate does not itself make ink artwork wrong. Quantized layer timing is independent of composition timing. [Adobe's time-effects documentation](https://helpx.adobe.com/in/after-effects/desktop/apply-effects-and-animation-presets/list-of-effects/time-effects.html).
- Economy comes from reused approved drawings, cached fields and focused revisions. Fewer encoded frames do not establish measured token savings.

The default execution path is original still art plus authored SVG, Canvas, shader or Remotion code. External AI video is not part of this workflow unless the user explicitly selects it. Do not silently introduce Kling, Runway or another paid service because an attachment mentions them.

## Material and transitions

Direct cause, location, direction, timing and resolution. Use stable seeds and one authoritative frame clock. A random-access frame must agree with playback; use analytic fields or baked/checkpointed simulation.

| Event | Visible progression | Safeguard |
|---|---|---|
| Ink-drop birth | Small dense bead → irregular growing reservoir → recognizable scene with diluted margins | Avoid a uniform radial circle or a generic opacity fade. |
| Brush action bridge | Pressure-shaped fast slash carries scene A into B | Use at an energetic story turn. “Six frames” is an example, not a universal duration at every fps. |
| Water wash | Water loosens local pigment, edges retreat and pale channels open on the existing paper | Show actual local recession; a uniform fade to white alone does not meet this chosen direction. |
| Object-to-object ink morph | Shared mass/correspondence connects one recognizable object to the next | Define intermediate topology. Do not melt living anatomy during a required physical action. |

For this refined Living Ink direction, organic material events join scenes; avoid standard hard cuts, cross-dissolves and generic swipes. The references themselves contain hard cuts and fades, so this is **our chosen adaptation**, not a claim that every source obeys it.

Transitions are secondary to the story. Start an opening splash or bloom where the scene forms, rather than automatically wiping from an edge. Avoid fast left/right slides disguised with a wavy border. Do not cover every pose replacement, camera move or spoken phrase with another effect. A short 30-second film will often need only three or four major material events, with local ink continuity between them; the exact count follows the story. A continuing path or receding wash can join beats without obscuring the actors. Use the [24-mechanism transition catalogue](ink-transitions.md) as a choice set, not a quota. Its mechanisms are original authored adaptations, not a claim that 24 transitions were observed in the references.

Keep opaque core, diluted shoulder and small irregular frontier distinguishable. Change ownership and structure where the story calls for it. Do not run every contour at equal speed or add unrelated particles everywhere. A cloth/branch/trailing wash can move while a hand remains stable. Contact needs correct geometry before material polish.

## Voice, sound and ink words

Recommend measured, intimate narration with room around heavy lines, subject to the approved recording and runtime. Do not slow, regenerate or rewrite an approved take to force a generic 1–1.5-second pause rule. If the proposed performance cannot fit, return to the user's duration choice.

Design three purposeful sound layers: tactile brush/drop/paper events at visible material changes; world foley at actual action/contact; sparse score shaped by the story. Default to the bundled local Python synthesis kit. Describe its plucked, breath-like or drum-like timbres honestly; they are not authenticated recordings of koto, shakuhachi or taiko. Supplied music or explicit silence overrides the default.

Keep speech clear. Gentle tonal/reverb processing is optional, never an excuse to obscure consonants or add a long tail beyond the cut. Preserve the source take and review the mixed export.

Remove unnecessary transition whooshes, delayed contact cues and empty waiting between beats. A purposeful silent reaction still has visible performance and environmental continuity; it is not an accidental dead gap. Match sound to the actual final action timing, not merely the shot boundary. Rain can recede and sound distant inside shelter without disappearing from the outside world. Do not silently rewrite or rush approved narration to solve pacing; resolve a genuine runtime conflict through the duration contract.

Use brush-like ink typography in reserved space, with a short material reveal and a stable readable hold. Check an installed/licensed font before adding software. Do not make every caption the same bottom-centred pop-up. Keep contrast and reading order consistent even when composition moves the text. Full approved subtitles and selective large key phrases are different layers: a few power words must not silently replace required text. Accent only a meaningful word or motif; reveal text early enough to read it. Avoid captions over faces, touch points or required actions.

## AI director/critic and evidence gate

The assistant performs direction; an independent AI critic is preferable for difficult shots. This skill does not ship a standalone vision model or claim to verify pixels with JSON. Give the critic:

- Approved story, exact words, timing and source-study limits.
- Actual master/whole-pose art and annotated anatomy/contact comparisons.
- Real consecutive frames around difficult action and every material transition.
- Current neutral-background and final-art clips at normal speed.
- Captions, approved voice and final sound with honest listening coverage.

The critic must state concrete observations, evidence times and unresolved issues for story, Japanese Sumi identity, pigment evolution, paper continuity, anatomy/contact, material transitions, captions and sound. Do not prefill a passing review. A stale review becomes invalid when source/art/timing changes.

Use [the review schema](living-ink-review-schema.md) and the standard `scripts/validate_shot_plan.py` assets/proof stages. The deterministic gate verifies completeness, hashes and evidence linkage; it cannot establish artistic truth. Prove the hardest contact and material passage first, then review the remaining shots and final export. Tests, encoding and a plausible prompt do not certify the result. Disclose unperformed playback/listening and do not promise zero errors.

## What the supplied references actually support

The 20 October local study extracted every decoded frame of both supplied files, then visually inspected whole-timeline samples and selected adjacent-frame windows. Extraction is not equivalent to inspecting every image.

- **The White Moon:** 12,706 decoded frames; timeline samples at two-second spacing and 168 consecutive frames at 104–106s, 122–125s and 370–372s. Stable local paper, line/fill acting, a local approximately 12-pose-updates-per-second passage and oar/ripple contact are useful. The studied transition fades through white; the source uses several colours and variable density. A global 85/15 rule, fixed four-layer production and all-film stepped cadence were not established.
- **Marco Polo Title Sequence:** 2,329 decoded frames; 260 unique inspected frames including 216 consecutive frames around 25–27s, 56–60.5s and 75.5–78s. Wet-looking reservoirs, diluted shoulders, fringes, held silhouettes and strong negative spaces are useful. Hard cuts occur at 25.984s, 58.559s and 76.618s. Camera/focus and material change are entangled; the production toolchain is unknown.

The private research sheets stay in the project, outside portable packages. These bounded observations inform an original workflow; they do not establish source-equivalent animation or a completed film.
