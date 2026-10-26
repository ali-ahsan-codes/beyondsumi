# Recorded splash library — Light and Dark

The public distribution excludes the owner-supplied recorded clips because standalone redistribution documentation has not been supplied. Default to the included authored24ink-transition mechanisms; this preserves the three-style direction without shipping source reference footage. The optional import adapter/gallery remain, with an empty catalogue until a user supplies licensed media. Existing owner films/private clips are preserved.

For a documented user-owned import, use the [catalogue](../assets/ink-footage/catalog.json), [gallery](../assets/ink-footage/index.html) and [Canvas adapter](../assets/ink-footage/composite.mjs) when a real recorded splash suits the story. The user supplied three videos and described them as royalty free. The catalogue preserves source names, hashes and extraction ranges; no separate license document was supplied/verified. Intro titles, numbered labels, outro and original audio are excluded. These supplied assets are distinct from private screenshots of other research references.

There are seven extracted clips: five numbered bloom variants, one multi-bloom and one directional sweep. The first two numbered blooms are visually similar; do not call these seven unrelated animation mechanisms. All are 1280×720 at 24fps. Each has a black-pigment **alpha WebM**, a grayscale **MP4 matte** and a transparent PNG poster. Recolour the alpha; do not paint over a green rectangle or import the source's paper.

The source pack had green pigment on white, while the sweep had white pigment on green. Extraction uses green dominance to keep the desired material, with calibrated noise floor/foreground values. The final clips contain no green RGB pigment. Keep semi-transparent bristles and dilute edges; a hard threshold loses the material. Do not claim these 720p files are 4K because a source title says 4K.

## Selection and pacing

- **Original:** retain its preserved Sumi-e identity. Do not add this splash treatment or replace its character art by default.
- **Light:** tint pigment using a story-selected carbon/mineral color; the same wet-brush language must appear in characters and backgrounds.
- **Dark:** neutral black/white/grey base plus selective dark red for meaningful blood, eyes or character/scene accents. The adapter permits neutral ink and dark red (recommended `#7A1622`), rejecting other hues; intentional placement and visual review are still required.
- **Blooms:** local title/character/detail reveals or elements in a composed scene transition. They leave transparent corners and do **not** provide a full-screen cover by themselves.
- **Multi-bloom:** an accumulation/discovery or richer local reveal. Avoid repeating the same recognizable pattern at every scene boundary.
- **Edge sweep:** optional only. It travels across the screen and must not become the fast recurring side wipe previously rejected by the user.

Choose transitions at meaningful scene changes, surprises or shifts of attention, not as a constant overlay. For an energetic scene exchange, about 12–24 output frames is a starting range, not a forced duration. Gentle material formation can take longer. Choose a useful source range and mapping, review the real movement and let the action remain visible. Do not squeeze every six-second source bloom into six frames. A library's native duration is not a prescribed film duration.

Use a transition's **own output-frame interval**. Do not derive its elapsed time from a narration-retimed story clock: that caused inconsistent two-to-thirteen-frame reveals in a previous comparison. Incoming scene movement should already be active while revealed. Sync a restrained wet hit/brush sound to visible deposition, not to every alpha frame.

## Composite correctly

For a visible pigment overlay, decode the alpha video, colour its RGB through `source-in`, then composite it on the film's persistent paper/scene. For revealing artwork, use alpha as `destination-in` on the incoming layer. The adapter supports either true alpha or grayscale-matte decoding. Choose the MP4 matte fallback if the renderer's WebM decoder discards alpha; never accept an opaque rectangle as a substitute.

An ink overlay is not automatically a scene transition. Keep the outgoing scene until sufficient incoming coverage exists. Compose overlapping blooms, prepare a larger appropriate matte, or use a motivated full-cover event; inspect all corners and visible subject areas. Do not switch to the full incoming frame while a local bloom covers only its centre. Do not enlarge a tiny bloom so far that bristles become distracting pixels. The edge sweep is the only supplied full-cover candidate, and still needs compositing review at its actual frame range.

```js
import {createInkPainter, sourceFrame} from './ink-footage/composite.mjs';
const painter = createInkPainter(1280,720);
const frame = sourceFrame(outputFrame, {startFrame:120,durationFrames:24,sourceFrames:165});
// Load/seek the chosen media to this exact frame and wait for decode first.
// For deterministic export, a prepared image sequence is also suitable.
if(frame !== null) painter.overlay(ctx, decodedFrame, {
  style:'light', color:'#1d3b58', kind:'alpha', x:0,y:0,w:1920,h:1080
});
```

The adapter does not seek a video or synchronize its browser clock; the caller must supply the film-clock frame. Its mapping holds the final source frame rather than looping automatically. For narrative transitions, explicitly end/remove the effect only when the scene exchange is complete.

## Portable use and proof

Light/Dark initializers copy this asset folder into `public/ink-footage`. Original does not activate or copy it into public media automatically; its reference-guide tree may retain linked library documentation/assets. Other engines can use the alpha video or matte directly; no AI video service or extra key is needed. The public packages contain the adapter and an empty import catalogue, not those recordings.

Run `python3 assets/ink-footage/serve.py --port 4251` from the skill root and open `http://127.0.0.1:4251/` in Chrome. The included server supports video byte ranges for seeking. Verify real transparency on light, dark and checker backgrounds, recolouring, first/last frames, source seek, edge quality and actual scene exchange. Numerical alpha checks establish file behavior, not artistic suitability. Save chosen asset/hash, source in/out, film output frames, tint, scale/origin, coverage strategy, scene cause and sound cue in the shot record. Unknown or missing visual review remains unverified. None of this authorizes a new film by itself.


## Reference-led action accents and transitions

For authorized Light/Dark production, choose the relevant passages from the user's supplied Marco Polo Title Sequence and Original Ink painting animation The White Moon references, and consult saved studies; inspect the actual passage again where timing or shape is uncertain. Do not claim an exhaustive new study without doing it. Use their stroke-built movement and organic scene exchange as motion direction, not reusable footage/art. The separate user-supplied splash clips in this library can provide permitted matte/alpha material.

Keep two layers of direction distinct: local sword/step/landing ink accents track the action; larger ink birth, brush deposition, wash or motivated shape change connects scenes. Plan event timing, origin, coverage and decay. Use the recorded bloom or other suited mechanism, not a default repeated left wipe. Full-frame coverage must be checked before changing the underlying scene. Avoid distracting overuse; action, captions and narration must remain readable. The connected action-frame guide describes where supported cutout in-betweens may supplement drawings.
