> Historical mechanism research only. Current styles are Sumi Original, Sumi Light and Sumi Dark; their current palette/cadence/workflow override this archived study. Load only when a specific mechanism is needed.

# Flow

**A painting performing the story.** Ink forms are born, change shape/density, join, separate and recede as the narrative develops. The viewer should feel the image being painted and transformed, including during the action inside each scene. Use the [category contract](../animation-categories.md); ordinary walking puppets beneath brush transitions do not qualify.

## Two routes, one painting-led identity

**Bristle:** the [muted-trace clip](https://www.pinterest.com/pin/1129559150321978735/) shows parallel dark/light strands bending into broad bands, pooling and becoming denser smoky regions. In the 20 October Chrome samples at approximately 0.99, 1.99 and 2.98 seconds, the strands themselves change curvature and extent. Later samples show darker material reorganizing the striated field. This is not a single progress mask over fixed art.

**Bloom:** the user's [Marco Polo example](https://www.pinterest.com/pin/299348706467886750/) adds recognizable figurative painting. The linked [sequence](https://vimeo.com/121421969) shows landscapes, a bird, bodies, paired creatures and flags composed in dark pigment with translucent feathered edges. Sampled passages around 15–17 seconds build layered terrain; 31–33 retain a recognizable bird while adjacent pale/dark shapes develop; 60–62 organize paired curved creatures; 74–76 move from a flag to a macro wet boundary. Recognizable subjects and abstract material transitions can coexist. This is **not** a requirement for continuous arbitrary object-to-object morphing.

The related [drama title sequence](https://www.pinterest.com/pin/310044755601039843/) broadens dark painted space, isolated red foliage, ink-edged cliffs and large creature forms giving way to a circular motif. It supports atmosphere and tonal variation within the family, not copying its cast or mythology. [Research notes](../motion-study-2026-10-20.md) distinguish timed samples, unavailable sources and unknown original methods. These Asian-inspired production references are not all Japanese historical artworks. Do not claim verified fluid simulation, practical-paint capture, exact drawing cadence or original sound from visual evidence alone.

Select Bristle, Bloom or an explicitly coherent combination for the brief. A literal human story will often benefit from Bloom's identifiable subjects; a poetic interlude may use Bristle. Neither route requires a samurai, monochrome-only image, circular ending, fixed duration or credit typography.

## Shape the story in pigment

Design a recognizable visual anchor for every causal beat: the relationship, carried object, silhouette, light or spatial threshold that must remain understandable. Specify paint states around it: a sparse mark gathers into a person; another trace follows; a wet shadow encroaches; a decisive painted gesture changes that shadow; the remaining forms settle together. These are examples, not a mandatory plot. If the approved story explicitly requires a literal walk, touch or cut, draw that action in changing ink poses and preserve the contact. Metaphor must not erase required actions.

Use anticipation in gathering ink, pressure in widening/darkening strokes, resistance in tension between forms, and aftermath in slow feathering or settling density. Timing may be fast, violent, gentle or patient according to the story. Dark pigment can consume space; clearing or dilution can release it. A complete pose need not move constantly if the material and composition are meaningfully changing. A flat still with a camera move is insufficient.

## Asset contract and code construction

For Bloom, prepare subject silhouettes and any required pose extremes; a local **arrival-time map**, density map, wet-edge texture, dry-core mask and clean paper; optional drawn transition poses. Arrival maps define which regions receive pigment first. Several irregular source fronts can meet, pool or leave dry gaps. They are spatially designed for the subject, not uniform left-to-right gradients.

A practical deterministic approximation:

1. For each local point `p`, compute `age = time - arrival(p)` with stable low-frequency irregularity in the arrival field.
2. Before arrival, expose paper. Around arrival, use a thin translucent leading fringe; behind it build the denser core and local pooled edge. Bound spread to a prepared growth field or distance band.
3. Advance fingers/fringes at unequal rates, then damp them as the ink settles. Introduce an authored boundary displacement/pose progression where the form needs to move. The sequence must change more than alpha.
4. Keep dry paper stable in paper/world coordinates; move subject-bound masks with their pose. Only wet regions advect or change density. Composite pigment, translucent residue and paper without rectangular alpha halos.
5. Cache generated fields/textures and derive time from the frame clock. For genuine numerical diffusion/advection, use stable stepping and baked/checkpointed states; do not simulate forward from arbitrary player state.

This is a controlled painted effect, not a claim of physically exact capillary flow. Avoid a heavy global blur: it removes the very feathering and density distinctions that make wet paint readable.

For Bristle, sample a centre path by arc length; use a coherent bundle of offset strands. Pressure controls width, coverage and darkness; tangents and internal strands deform together. Keep small bristle gaps stable, give pooled tips a designed lag, and inspect tight bends for inverted normals/self-crossing. A moving outer silhouette with static internal stripes fails. A round-capped stroke-reveal can be a construction aid, not the finished look.

## Transitions, camera and physical action

Use a spreading field, travelling strand, dissolving contour, matching dark mass or fresh pigment front to connect scenes. Preserve a meaningful anchor until the next form is readable. Incompatible shapes need intermediary drawings or an authored occlusion; an arbitrary crossfade does not invent a transformation. A cut is allowed when it serves the story; do not force every object to melt.

Camera can linger close enough to see material, follow a paint front, or withdraw to reveal what the painting has become. Let the material lead; constant panning across finished images fails. Tone and density should carry suspense/resolution, not just a LUT change.

Stylization preserves cause and effect. A painted blade still belongs to its grip and meets its target; a severed form separates along the shown cut and remains changed. A falling petal releases, travels and settles. Material dissolution follows the event rather than substituting for it. Diagnostic underlying geometry may be simple, but the final image must read as changing paint throughout the action.

## Sound, captions and proof

Use the project's chosen narration route, preserving approved words and the [duration decision](../script-duration.md). Default original background score/ambience/SFX to [Python synthesis](../python-background-audio.md). Shape filtered noise and tonal movement around gathering, pressure, contact and release; leave space between gestures. Continuous whooshing flattens the film. Sound direction is original, not a reconstruction of unverified source audio. Keep captions stable, readable and timed to the actual take rather than dissolving every letter.

Prove the hardest chosen route before a film: a recognisable Bloom action with expanding/settling edges, or Bristle deformation with coherent inner strands and a legible transformed result. Review source/front/midpoint/settle plus normal-speed playback. Check paper stability, dry/wet separation, identity, masks, contact and persistent consequence. The existing growing-ribbon lab demonstrates only a limited mechanism; it does not certify Bloom or a narrative Flow film.

Reject an unchanged body rig with a brush overlay; uniform opacity reveals; whole-image turbulence; repetitive wipes; unrelated morphs; a beautiful still with camera motion only; or an abstract image that loses the required story. Follow the [category gate](../animation-categories.md), [motion direction](../motion-direction.md), [physics/review](../physics-and-review.md) and [production standard](../production-standard.md).
