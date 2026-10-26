# A library of 24 authored ink mechanisms

These are original authored adaptations for Japanese Sumi storytelling. They are not 24 techniques verified in the supplied reference films, new primary Sumi methods, or finished-film approvals. The same fixed view, white field and black pigment expose the differences in geometry and movement. The implementation is deterministic geometry with soft density edges, not a physical fluid solver.

The reusable files live in `assets/ink-transitions/`. `catalog.mjs` is the machine-readable catalogue, `fields.mjs` supplies density fields, and `index.html` is a local interactive gallery. The gallery is a mechanism study; its simple procedural marks are not finished character artwork or a demonstration of final compositing quality.

The [recorded splash library](ink-footage.md) adds supplied alpha footage for Light/Dark. Its seven clips are media variants, not additions to these 24 procedural mechanism IDs. Original retains its own treatment.

## Choose a few that belong to the story

For a typical 30-second film, begin with three major mechanisms and use a fourth only when it serves a distinct story beat. This is a restraint default, not a quota or a universal cap on longer films. Reuse a selected material behavior with a new, meaningful origin instead of showcasing the whole catalogue.

A new scene does not automatically need a large transition. A small splash can start a scene; a slight wash, retained stain, local brush growth or quiet settlement can carry the next action. Mark those boundaries as material continuity with their visible cause and destination. Do not add a full-frame event solely to satisfy a boundary count. A fast leftward slide, uniform fade or renamed wavy wipe is not sufficient evidence of ink behavior.

Choose the mechanism after deciding what the viewer must see:

1. Bind the visible cause to the spoken or visual beat: a rain drop, touch, root, departure or held memory.
2. Place its pigment mass at that cause, with a clear destination and a motivated delay or duration.
3. Keep faces, hands, feet and contact readable. Rain must visibly fall and affect surfaces; traffic must visibly pass; a caring touch must visibly make contact. A decorative wash cannot replace these world actions.
4. Use negative space for the material event and captions. Preserve the single underlying paper throughout.
5. Keep most local events quiet. Sound intensity below is relative editorial emphasis, not a digital gain or a percentage of a final mix.
6. Inspect adjacent frames and normal-speed playback with the actual scene artwork. Selective drawing holds and continuous material simulation are separate clocks.

For the puppy teaser, plausible choices are a local `drop-bloom` for the first presence, `root-branch` or `sheltering-arc` for refuge, and a small `water-lift` for loss. These are recommendations, not proof that the current film uses them. Rain, cold posture, the deer's guidance, grief and the girl's touch still need their own visible performances.

## Catalogue

Durations are starting ranges for one local event, not mandatory scene lengths. The complete metadata includes cause, mass geometry, reveal, story use and sound in `catalog.mjs`.

| ID and name | Cause and changing mass | Reveal / story use | Seconds | Sound emphasis |
|---|---|---|---|---|
| `drop-bloom` · Single drop bloom | One drop expands a dense centre and dilute shoulder | Local discovery or quiet beginning | 0.8–2.2 | Soft drop · 0.20 |
| `twin-pools` · Two pools meet | Separate lobes gain a joining neck | Meeting and connection | 1.2–2.8 | Two drops, wet pull · 0.20 |
| `satellite-splatter` · Drop and satellites | An impact creates a main pool and unequal delayed droplets | Rain impact or surprise | 0.35–1.4 | Short splatter · 0.35 |
| `capillary-fan` · Capillary fan | A reservoir feeds fine rooted fingers | Gradual realization or seeking shelter | 1.3–3.2 | Light wet drag · 0.12 |
| `river-confluence` · Converging streams | Curved tributaries reach a thickening common basin | Several causes reaching a consequence | 1.4–3.2 | Low trickle · 0.15 |
| `porous-seep` · Porous seep | Unequal short columns wick from a local contact band | Damp ground or a slow arrival | 1.5–3.4 | Damp paper · 0.08 |
| `root-branch` · Rooted branching | A stem grows ordered tapering branches | Shelter, ancestry or a route | 1.1–3.0 | Soft bristle drag · 0.15 |
| `vein-network` · Connected veins | Linked channels and loops fill their junctions | Systems or a connected map | 1.5–3.5 | Fine paper texture · 0.10 |
| `islands-gather` · Islands gather | Unequal separated deposits enlarge and join | Memories or fragments forming a whole | 1.0–2.8 | Muted drop ticks · 0.15 |
| `fibre-weave` · Fibres interlace | Two bent fibre families cross while leaving gaps | A relationship or explanation being built | 1.3–3.0 | Fine brush strokes · 0.12 |
| `pigment-migration` · Pigment migrates | A source shrinks as droplets follow a curve into a destination | Giving or carrying care forward | 1.1–2.6 | Wet pull, gentle landing · 0.18 |
| `ripple-transfer` · Ring carries pigment | A water contact pushes a ring and uneven deposits outward | A touch and its consequence | 0.7–2.0 | Soft tap · 0.18 |
| `dry-bristle` · Dry bristle comb | Unequal short ribbons leave broken paper gaps | A decisive word or brief emphasis | 0.25–0.9 | Dry scrape · 0.25 |
| `calligraphic-hook` · Calligraphic hook | A pressure-changing ribbon turns and tapers | A decision or redirected path | 0.5–1.6 | Controlled stroke · 0.20 |
| `sheltering-arc` · Sheltering arc | Two marks curve around an open paper pocket | Protection or refuge | 0.9–2.4 | Two soft strokes · 0.15 |
| `stipple-join` · Dots find a path | Staggered contacts thicken along a bent route | Footsteps or accumulating evidence | 0.8–2.3 | Sparse taps · 0.12 |
| `neck-and-separate` · A neck separates | Two lobes draw apart and their neck thins and breaks | Departure or parting | 1.1–2.9 | Quiet pull or silence · 0.10 |
| `petal-turn` · Petal assembly | Unequal broad marks turn around a centre and settle | Growth or renewed life | 1.2–3.0 | Soft bristle flutter · 0.10 |
| `hollow-opens` · A hollow opens | A wash grows and its heart clears into an irregular annulus | Refuge or absence revealed by negative space | 1.1–2.7 | Drop then quiet clearing · 0.13 |
| `paper-window` · A paper window | Corner reservoirs connect into a broken enclosure | A letter, interior or inset | 1.2–3.1 | Low paper texture · 0.10 |
| `water-lift` · Water lifts ink | A clean-water hole grows through an existing wash | Emotional release or making room | 1.2–3.2 | Soft water · 0.10 |
| `wick-away` · Ink wicks away | A broad stain drains into a thread and terminal deposit | Retreat or one remaining thought | 1.4–3.4 | Absorption, almost silent · 0.06 |
| `evaporation-islands` · Evaporating islands | Clearing holes break a wash into lasting dark regions | Time passing or fading recollection | 1.6–3.8 | Usually silence · 0.04 |
| `settled-recede` · Shoulder recedes | A dilute edge contracts around a held dense core | An accepted touch or final pause | 1.2–3.0 | Quiet tail or silence · 0.05 |

## Renderer-neutral API

```js
import {prepare, sample, renderMatte} from "./ink-transitions/fields.mjs";
import {TRANSITIONS, BY_ID, SELECTION_GUIDE} from "./ink-transitions/catalog.mjs";

// Use the film's clock. Quantize drawing changes separately.
const t = Math.max(0, Math.min(1, (timeSeconds - eventStart) / eventDuration));
const field = prepare("drop-bloom", t, width, height, 1827, {
  origin: [0.32, 0.60], // normalized position of the local field's centre
  scale: 0.45          // relative size; 1 uses the catalogue's default footprint
});
const density = field.density(pixelX, pixelY); // 0..1 visible pigment
renderMatte(canvasContext, field); // white=pigment, black=none, alpha=255

// Convenience for isolated queries; do not reconstruct the field per pixel.
const sameDensity = sample(
  "drop-bloom", t, pixelX, pixelY, width, height, 1827,
  {origin: [0.32, 0.60], scale: 0.45}
);
```

`prepare(mode, t, width, height, seed=1, options={})` builds a field once. `density(x,y)` accepts pixel coordinates. `sample(mode,t,x,y,width,height,seed=1,options={})` is the same calculation but rebuilds the field, so prefer `prepare` for image loops. Progress is clamped to 0–1; dimensions must be finite and positive. Out-of-domain or non-finite coordinates return zero. Choose and retain an integer seed. There is no random state, elapsed-time accumulator, network call or installation dependency.

The normalized geometry follows the supplied width and height: changing their aspect ratio stretches the field. For a circular event in a wide film, evaluate a square local region and place it within the composition. A small preview raster is sufficient for a feathered material matte; cache or pre-render higher-resolution mattes for expensive scenes. Review the actual final sampling scale for visible banding and aliasing.

`renderMatte(context, field, {invert:false})` paints opaque grayscale into a matching Canvas; it does not composite the scene. The caller can use luminance as a reveal mask, visible wash, erosion mask or pigment texture. Black-on-white gallery rendering deliberately inverts that matte to show ink. `water-lift`, `wick-away`, `evaporation-islands` and `settled-recede` begin with existing material and withdraw it. Some transformation modes also begin with material. Never force every field to begin blank or treat every increasing value as an incoming scene.

Scene-to-scene object migration needs approved source and destination artwork, retained silhouette anchors and a reviewed change between them. The `pigment-migration` field provides a transfer pattern; it does not infer an object morph, preserve body anatomy or generate correct acting. Whole-pose and contact checks remain necessary.

## Local preview and checks

Serve the folder through a loopback-only server from the skill root:

```sh
python3 -m http.server 4231 --bind 127.0.0.1 --directory assets/ink-transitions
```

Open `http://127.0.0.1:4231/` in Chrome. The slider seeks all 24 mechanisms; the family menu narrows the view. **Play all** uses a normalized three-second event and a brief final hold for comparison, not each catalogue duration. Offscreen cards skip repainting until they enter view. No sound is generated by the gallery; sound descriptions are direction only.

Run the independent numerical checks with existing Node:

```sh
node assets/ink-transitions/test-fields.mjs
```

The tests check deterministic seeking, finite 0–1 density, local placement, temporal field differences across all 276 pairs, birth growth, water removal, persistent cores and hollow opening. Numerical differences establish that fields differ, not that each is artistically successful or physically realistic.

For film approval, save the selected mechanism IDs, origin/scale/seed, scene cause, major/local classification, source-art hashes and timing. Review the actual boundary or continuity frames and normal-speed scene. Record any hidden face/contact, illegible caption, absent rain/traffic consequence, distractingly large wash or unsuitable sound as an unresolved issue until corrected. This library never writes an AI review pass.
