# Living environments — all three Sumi styles

Use before scene artwork/motion planning. This extends the existing scene-first,
Living Frames, character/camera and local sound systems. Keep the current engine:
Python prepares deterministic parameters/assets; Canvas/Remotion can composite
with the bundled adapter. A Python picture renderer can consume the same plan.
Do not describe the current film compositor as Python-only or replace it to add
atmosphere. Environmental motion also works in character-free scenes.

## Direct the environment

For every new shot, choose `animate` or deliberate `still` with a story reason.
Record place, time, weather, visible light sources, wind direction, moving
objects, rigid architecture, subject/text holdouts, effect depth and timing.
Choose `subtle`, `natural` or `dramatic` from the scene; quiet emotion may need
only one candle and very slow dust. Darkness does not require constant activity.

Start with the approved complete master → existing layers/masks → reusable
compatible textures → procedural particles/light → bounded local resampling →
targeted new art only when missing pixels/view information actually require it.
Respect the scene's actual time and geography: a night window needs a matching night sky, not a new sunset or mountain silhouette. Window bars, lamps and rigid architecture stay anchored; light/shadow/reflection receivers share their source driver.

Keep full source/mask/plate hashes. Source changes need new reviewed coordinates
or a verified shared registration; do not inherit targets across unrelated panels.

Use the [environment shot record](../assets/templates/ENVIRONMENT-SHOT.md) and
[editable plan](../assets/templates/environment-plan.json). Coordinates are
source-space `[left,top,right,bottom]`; masks are local RGBA/alpha images scaled
to that rectangle. Match mask aspect/registration to the source, inspect its
edges and protect skin, hands, text, fine patterns and rigid supports. Declare
intentional character illumination separately when the character shares the
source light. A mask file/hash alone does not prove a correct silhouette.

## Connected motion and material

- **Fire/candles:** keep candle/torch supports fixed. Author only the flame patch;
  one seeded driver controls its small shape/brightness changes and the local
  light, shadow and reflection receivers. Different candles get independent
  drivers. Receiver patches must correspond to actual walls, cloth, goblets,
  water or metal; match shadow direction to source/occluder geometry. The helper
  supplies coupled parameters, not ray tracing or automatic shadow geometry.
- **Lighting/colour:** use local source-related masks, limited brightness and
  palette-preserving tones. A passing cloud may affect the moonlit receiver;
  link its driver. No full-picture colour cycling or scene-wide exposure pulse.
  Shared source lighting can affect character and set together; unrelated haze
  cannot arbitrarily recolour faces or erase pale clothing.
- **Atmosphere:** mist/haze/smoke, dust, embers, rain and snow use authored
  depth, scale, direction and shelter/occlusion. Nearby particles can travel
  faster than distant ones under comparable camera conditions. Wind/humidity
  belongs to the world; do not send every layer in conflicting directions.
  The adapter's soft puffs/particles are small 2D approximations. Use retained
  painted textures/layers when the procedural result looks digitally filtered.
- **Clouds/parallax:** meaningful painted shapes need matching extracted layers
  plus a clean plate to replace their original location. Retain perspective,
  bounds/overscan and near/middle/far relationships under the existing camera.
  Never deform a castle or slide a duplicate cloud over its unremoved original.
- **Cloth/ripples:** apply small bounded movement only to loose cloth or the
  water/reflection surface. Fix attachments and shore/rigid boundaries; use a
  supported extracted layer for motion that exposes hidden areas.
- **Texture:** optional restrained local exposure-stepped pigment/edge variation
  for Light/Dark, disabled around faces, lettering and architecture. Original
  retains its painted identity with no automatic texture-boil/splash treatment.
  Texture motion cannot supply missing character action.

Preserve each style: Original uses delicate Sumi-e/Sumi Anime painted atmosphere,
Light retains colourful story/documentary clarity, Dark retains broad ink forms,
stronger source-motivated drama and a neutral base/selective dark red. Do not
apply Original/Light's warm colour overlay to Dark. Story-selected colours and
material direction remain the selected style's responsibility.

## Parameters and existing compositor

The [Python sampler](../scripts/environment_motion.py) uses one output-frame
clock, coherent seeded low-frequency drivers, timing offsets, start/stop fades,
intensity and source-pixel drift/depth controls. Direct seeking matches forward
sampling; it does not create unrelated random values per output frame. Cached
parameters can be reused. Fade-out is an authored settling envelope, not a
claim of physical spring/cloth dynamics. Avoid a visible cyclic reset; choose
non-looped drift or a reviewed life/rebirth interval with invisible boundaries.

Original stays30fps/20 designed character states; Light/Dark stay24fps/on-twos.
Environment can update at30/24fps while character poses hold. That means changing
light/atmosphere, not a scene transition per frame, and does not count as new
character drawings. One master can support150 output frames over5seconds.

```sh
python3 /absolute/path/to/validate_environment_plan.py /project/environment-plan.json
python3 /absolute/path/to/environment_motion.py /project/environment-plan.json /project/environment-samples.json
```

The sampler refuses an existing output and invalid assets/bounds/timing. Use
shot-local frames; bind the plan to its actual source and output frame range.
`animate` requires a nonempty valid plan. `still` with a reason is valid without
an effect. New4.8plans carry this decision in `shot.environment`; historical
plans keep their earlier contract. [Plan validation](../scripts/validate_shot_plan.py)
checks environment evidence alongside existing character/physics checks.

The [Canvas adapter](../assets/motion-core/environment-canvas.mjs) reuses the
existing bounded patch sampler. Load raster masks, extracted layers and clean
plates in an asset map, supply the current baked frame and use the appropriate
`background`, `foreground` and `lighting` passes. Put world-space effects inside
the same camera transform as the artwork. Draw captions/titles afterwards.

For separated artwork: base/clean plates → background geometry/atmosphere →
characters → foreground occlusion/atmosphere → source-linked lighting/reflections
→ selected style grading/camera finishing → text. Adapt order to actual depth.
For an integrated master that already contains characters, its background pass
cannot magically go behind them: supply masks/holdouts or keep the effect in
visible background-only regions. Do not repaint over existing character acting
with a later source patch. Real source-specific masks and reviewed stacking are
required; the adapter does not discover layers, lights or anatomy.

## Sound and review

Reuse the [offline sound bank](sound-library.md) for appropriate wind, fire or
weather ambience, aligned to visible causes and actual scene timing. Keep the
existing voice/music/SFX stems and duck/recovery. No sound per tiny flicker; no
new provider call from ordinary reuse. Cached recordings are not generic bundled assets or automatically
audition-approved. Use the user's compatible reviewed bank or an explicitly labelled review draft; synthetic Python music
and cached provider effects are distinct sources.

Before reusing a preset in a film, compare original/derived art, masks, motion
extrema and consecutive frames at normal speed. Check rigid landmarks, occlusion,
source/receiver timing, reflection placement, shadow direction, palette, edges,
readable acting/captions and visible-but-subtle motion. Inspect scene joins,
exact seeking and rendering cost. Measure flicker/changed-pixel localization as
bounded diagnostics; reduce/remove anything that looks like a digital filter.

A representative candle table and quiet hall make useful before/after proofs;
they are examples, not compulsory locations or a new film authorization. Keep
previews and old films separate. Record reused/new assets, generation calls,
modified modules, frame time, observations and unresolved issues. Final proof
records require actual clip/adjacent frames/hash-bound observations, never a
prefilled visual pass. The validator checks data/provenance; it does not certify
natural lighting, motion, physics, sound or aesthetics.


## Visibility at delivery size —25October2026 correction

For an `animate` decision, require a clearly observable temporal change at normal
playback and the intended display size in **Original, Light and Dark**. An effect
that exists only in a pixel difference or a magnified crop has not met the brief.
Choose one primary environmental action the viewer can name: a painted cloud
crossing a window, a light pool travelling over stone, a readable candle-light
rise/fall with changing reflections, or a moving mist bank. Keep secondary detail
restrained. Increase the cause's travel, area or material contrast when it is too
faint; do not shake the whole image, add unrelated colours or overwhelm acting.
Deliberate stillness still needs a story reason; it is not a substitute for a
failed animated proof.

Tiny prototype amplitudes are not mandatory defaults. A technically changing
but imperceptible proof does not pass the visibility brief.
Use full-frame after-motion clips plus an accessible before view, rather than
shrinking every change inside a small side-by-side presentation. Inspect more
than the fade-in: measure temporal change between active frames, then review
normal-speed playback. An observed change versus frame0 alone may merely be a
static added glow.

`light_travel` specifies receiver-space travel in pixels, distinct from a tiny
flame deformation. `variation` controls coherent local intensity contrast.
Cloud layers need matching overscan and a clean plate; the adapter samples a
moving window inside the retained painted texture, preserving architecture and
window-bar holdouts. `painted_atmosphere` can advect a compatible alpha texture
for visible ink mist/smoke without replacing the existing scene. `holdouts` names
protected regions to clear during additive/layer compositing; actual rendered
holdout pixels still require checking. Never use these fields to waive body or
structural deformation checks. Different source views need fresh masks.

At proof stage, record `visibility` with `normal_speed_visible:true`, the actual
`display_size`, primary `mechanism`, its `time_window` and concrete `observation`.
Keep this pending until someone inspects the real sequence. Data checks cannot
turn a faint output into a perceptually passing one, and a technical reviewer
must not record owner acceptance unless it was explicitly given.

For a proof that appears blank or dark only during playback, use [the visible playback review and short-proof fallback](review-playback.md). Confirm moving images at intermediate times; a loaded poster, readyState or an advancing timer does not establish visible playback.
