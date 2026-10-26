# Brush-and-ink shot specification

## Scene-first pre-production record

- Storyboard and rough timed animatic paths/revisions, observations and unresolved issues:
- Integrated master composition / set geography / camera view / opening and closing state:
- Parent master/hash for derived layers; intact contextual-panel alternative:
- Character/prop ownership, shared support/contact, eyelines and screen direction:
- Asset lookup: exact reuse / supported transform or rig / derive master / pose sheet / new view; reason for each new call:
- Bounded generation batch, minimum usable panel resolution, planned vs actual calls and rejected cells:
- Frame-event ledger: poses/camera/contact, local ink vs scene transition, voice, music duck/recovery, SFX and silence:


For **Sumi Light** or **Sumi Dark**, profile `brush-ink-on-twos-v2`. Read the [shared workflow](../../references/brush-ink-workflow.md) and selected [Light](../../references/styles/sumi-light.md) or [Dark](../../references/styles/sumi-dark.md) policy.

This template records a proposed shot. Blank fields, selected presets and numerical settings do not mean the shot has been implemented, rendered or reviewed. Keep evidence states separate.

## Story and timing

- Project / shot ID:
- Style: `sumi-light` or `sumi-dark`
- Revision and source-lock status:
- Start / end / duration:
- Aspect ratio and pixel dimensions:
- Approved story revision and duration approval:
- Exact spoken words, required displayed text and visible action:
- Emotional purpose / anticipation / action or contact / recovery:
- Style-specific direction: Light story clarity/romance/children’s/documentary colours, or Dark oversized splash-built source forms and camera-led ink journey; common preparation does not imply identical animation:
- Focal subject and the spoken or visual cue that changes attention:
- Quiet beat or deliberate stillness, if applicable, and why:
- Film-wide material master and neighboring-shot comparison; how this scene receives the same planned performance method as the main action:
- Any budget/story conflict resolved in direction before production:

## Source inventory — count visual regions, not files

Declare the planned source/complete-pose count for this shot, sufficient for anticipation, contact and recovery. Count each distinct drawing/atlas region honestly; repeated instances and derived render passes are not new artwork.

| Source ID | File + SHA-256 | Kind / actual role | Board dimensions | `roi_xywh` or complete image | Independent visual-source count | Characters and support/contact in this drawing |
|---|---|---|---|---|---:|---|
| | | | | | | |

- Total distinct static sources used:
- Total complete character/extreme-pose sources used:
- Atlas/region accounting:
- Reference-only masters, never rendered:
- Reused source instances / derived passes:
- Procedural paper, environment, foreground or props used for story and depth:
- Anatomy/proportion/facing/contact comparison against retained complete masters:
- Required holdouts and occlusion, including pale body regions:
- If the budget cannot carry the action clearly, concrete revised direction:

## Depth and internal motion

| Layer | Reference Z | Source IDs or procedural recipe | Motion/depth rate | Support/occlusion relationship |
|---|---:|---|---|---|
| Fixed substrate / distant wash | −500 | | Paper grain remains output-space fixed; distant wash may move. | |
| Transparent midground | −150 | | | |
| Complete hero / shared interaction | 0 | | | |
| Foreground brush silhouettes | +150 | | | |

- Eligible hair/cloth/loose-edge masks:
- Face, hand, rigid-object, planted-foot, grip and contact locks:
- UV/mesh expression and measured amplitude at the final scale:
- Edge boil: seeded 6 or 12Hz exposure-locked field; displacement in actual output pixels:
- Visible internal action during holds:
- Independent foreground/background movement:
- Weather/particle type, story reason, depth, emission and shelter interaction, or omission:
- Deterministic seed/event IDs, clock and any cache/checkpoint requirements:

## Exposure and effect clocks

Required profile: **24fps output/camera/ink/environment; paired-frame character exposures (12/s), including attached props and character edge activity**. Character update rate is not a unique drawing rate.

| Exposure ID | Complete source / pose ID | Character or interaction | Start/end | 12 Hz exposure ticks | Action and support/contact | Hold/reuse reason |
|---|---|---|---|---|---|---|
| | | | | | | |

- Actual output frame of first contact / release / impact:
- Distinct drawing count, separately from ticks:
- One- or two-frame smear, if justified: exact 24fps frames, action vector, extent up to `2.8×`, bristle breakup and protected regions:
- If smear is omitted, story reason and the chosen readable pose-change method:
- No incompatible pose crossfade; how endpoints remain registered:

## Complete-pose sheet / scene sequence

- Connected action plan and required poses, including entry, contact and recovery:
- Generated files / distinct accepted drawings / excluded cells / reused exposures:
- Sheet hash and dimensions / cell ROI coordinates / registration anchor / ground baseline:
- Full limbs/props and padding retained / no neighboring-cell fragments:
- Whole-source comparison and supported crop/part motion:
- Visible action-ink origin, vector, scale, onset/decay and protected regions:

## Palette and pigment

- Light: choose only story-relevant swatches from `#F3EFE6`, `#111114`, `#5A5D64`, `#D3381C`, `#1D3B58`, `#C89B3C`, `#2E6F5E`, `#C94A6A`.
- Dark: white, black and equal-channel neutral greys, with optional selective `dark_red` (recommended `#7A1622`) for blood, eyes or meaningful character/scene details; no other hue or tinted paper. Record accent region/mask, purpose and continuity.
- Selected pigment roles and emotional/physical meaning:
- Multiply/alpha/holdout implementation:
- Pooling rim: approximately two scaled pixels inward, about 25% darker where the range permits; diluted shoulder / irregular edge:
- Negative space and paper continuity:
- Implemented material approximation and its limits; no unsupported true-fluid claim:

## Directed camera

- Setup / supported source view / dominant move or intentional hold:
- Subject and exact spoken or visual cue:
- Start framing → action/contact framing → recovery/end framing:
- Start/end times, endpoint holds and easing:
- Layer-specific parallax and speed-aware foreground blur:
- If using a preset, its adapted values:
  - Low push: ~15° supported tilt; depth ratios `0.1 / 0.5 / 1 / 3.5`.
  - Dutch slash: ~30° roll; ~400 scaled pixels / 0.2 s; specified easing.
  - Z corridor: three reused instances from `+200` to `−600`.
  - Counter-zoom: hero `+25%`, background `−30%`, perimeter brush marks.
- How support/contact stays coherent; no held-pose sliding used as a walk:
- Why the camera helps the story and how it avoids a flat moving card:
- **Dark only:** character importance/emotional turn; chosen wide/medium/face/detail/splash framing and story-supported angle; exact matching view/expression/action source IDs prepared before animation:
- **Dark only:** splash shot's focal target, material cause, reveal/peak/decay and readable recovery; distinguish local action accent from scene transition:
- **Dark only:** shared output-frame cue for source change, camera settle, ink event, narration phrase and sound onset/contact; join/eyeline/registration checks and any extra matching drawings needed for smooth synchronization:

## Transition and recovery

- Boundary ID / outgoing and incoming shot / story reason:
- Local formation point and cause:
- Chosen mechanism or same-world material continuity:
- If reusing the 24-mechanism library: ID / origin / scale / seed / actual compositing role:
- Duration and output frames:
  - Flood: 0.42 s / 10 frames.
  - Dry-brush whip: 0.25 s / 6 frames, ~50 scaled-pixel directional blur.
  - Negative-space erosion/reformation: 0.5 s / 12 frames.
- Onset → propagation → coverage needed for layer exchange → settled resolution:
- Incoming motion already active when revealed:
- Sources/render passes reused:
- Paper continuity:

| Optional action effect | Used or omitted + story reason | Exact frames / parameters / masks |
|---|---|---|
| Two-frame character/camera impact hold; material continues | | |
| One-frame structural value exchange | | |
| Light Cinnabar / Dark selective dark-red preservation mask, if used | | |
| Directional shake with `exp(-15t)` decay after hold | | |
| Derived ghost at `-velocity * 0.08`, opacity ≤0.4, fast decay | | |

Do not invent an impact for grief, sleep or gentle touch. Dark keeps a neutral base and may retain only a declared selective dark-red accent; Light's red/indigo options remain story-dependent.

## Sound and captions

- Approved narration source/hash; wording, speed and timing preserved:
- Music/ambience/SFX method and source:
- Material/contact/weather sound tied to actual frames:
- Quiet recovery and audible tail:
- Complete caption text/times, negative-space placement and protected action:
- Short brush reveal finishes before reading hold:
- Listening and final picture-to-sound review: `not performed` until actually done.

## Limb-motion evidence

Record per-action constraints under `shot.physics.actions`, then hash-bound `proof.physics_trace` and `proof.limb_review` using the [portable physics contract](../../references/physics-gate.md). Apply [limb-motion review](../../references/limb-motion-review.md). For every character action, record: character/view; action and entry/exit frame range; actual final-art full-body clip; consecutive-frame sheet; visible sole/hand/grip overlay; observed support and bend direction; defects; correction/recheck status. Blank or unresolved evidence blocks calling that action ready.

## Implementation and review status

| State | Status / evidence / revision |
|---|---|
| Authored technical specification | |
| Implemented mechanisms | |
| Unimplemented or approximated requirements | |
| Current art/source hashes | |
| Bounded hardest-shot render, when authorized | |
| Adjacent-frame inspection: exact range and observations | |
| Normal-speed playback: exact media and observations | |
| Anatomy/support/contact/release/occlusion | |
| Source-budget / depth / internal movement / palette | |
| Captions / audio listening / runtime / controls | |
| Remaining defects and next concrete correction | |
| User acceptance, only if actually given | |

A completed table, hash match or successful encode cannot initialize a visual pass. Preserve unperformed checks, rejected revisions and unfinished work honestly.

Environmental direction: animate/still decision and reason; local sources/receivers, weather/wind/depth, source-specific masks, protected characters/architecture/text and source-linked sound. Complete [the environment shot record](ENVIRONMENT-SHOT.md); review actual sequences, not only parameters.
