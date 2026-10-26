> Current: use `--style sumi-original|sumi-light|sumi-dark`. New Original adaptations use 30fps with action-driven sources and variable exposures; Light/Dark use 24fps/on-twos. Original historical browser sources keep their separate elapsed-time behavior. Dark permits selective dark-red accents under its current guide. These commands are for authorized future production; editing this guide starts no film.

# Bundled Remotion production workflow

Sumi carries its own engine starter and helpers. This skill can create a video without another style skill or an installed Remotion skill. Optional host skills may add current engine guidance. The starter is scaffolding; the initializer is checked separately from finished-film behavior and are not a finished film or a visual template to repeat.

## Start a portable project

For a new code-rendered video, use the bundled Remotion route by default. Preserve a user's explicitly chosen engine and suitable existing projects. Never migrate or overwrite an approved film merely to use this starter.

Resolve the skill path from its actual installed location:

```sh
python3 /absolute/path/to/this-skill/scripts/new_remotion_project.py /absolute/path/to/new-film --style sumi-light --aspect 9:16 --seconds 30 --title "Current story"
```

Use `--style sumi-dark` for the shared 24fps/on-twos workflow with a neutral base and selective dark red. Use `--style sumi-original` for a new Original adaptation at 30fps with action-driven sources and variable exposures; record that it preserves the historical art identity rather than retiming the recovered browser baseline. Select one style and destination for the approved project.

The helper refuses an existing destination, copies the starter plus this skill's independent Python audio kit, and configures the requested format. It does not install dependencies, change account settings or make paid calls. In the new project:

```sh
# Only after approval for missing third-party packages:
npm ci
npm run typecheck
npm run studio -- --port=4182
```

Open the reported localhost URL in Chrome before developing the film and keep Studio running while working. If a port is occupied, select another unused port; do not kill another project's server. Use environment permissions when needed. Runtime prerequisites and licensing are recorded in the copied `DEPENDENCIES.md`; npm and a compatible render browser may require downloading. Packages and browser binaries are installed dependencies, not included offline binaries.

`project.json` holds dimensions, FPS, duration and audio placements. `src/index.tsx` registers Film explicitly. `src/Film.tsx` initially contains an animated engine check, which must be replaced with the current story. `npm run audio:demo` creates a local, non-paid synthesized score and attaches it for an engine test. It refuses to replace an existing demo score. Do not deliver this generic check as the requested film.

## Direct and edit the film

Use this skill's art direction and review references. Write a fresh shot/beat plan from the user's words. Separate visual text, narration, asset origins and timing. Assign persistent identities and anchors to characters, objects, captions and cameras. Keep a single frame clock and derive all animated state from frame/FPS, including seeking and exports. Avoid CSS animation, timers, unseeded randomness and accumulated transforms in exported scenes.

Author each meaningful scene as its own React component and independently editable clips as separate JSX nodes/Sequences. Use Img/staticFile for local images, SVG or Canvas for geometry, and parent transforms for attached layers. Add story-specific cameras, motion curves, anticipation/contact/follow-through, shadows and depth as needed. Do not rely on atmosphere or a camera zoom to substitute for action. The current styles are Sumi Original, Sumi Light and Sumi Dark. All three use the complete-pose sheet/crop method and style-selected output (Original30fps/20 designed character states per animated second, with action-driven sources and supported derived motion; Light/Dark 24fps) with variable Original exposures and paired Light/Dark states. Light/Dark share the brush-ink profile; new Original adaptations preserve their source-informed art identity. Read the selected style profile; sharing an engine does not dictate every shot.

Keep source assets under public/ with portable relative paths. Generate separate subjects/backgrounds/props where independent animation is needed. Use the host image tool when available; supplied imagery, original SVG and procedural graphics are also valid. Wait for decoded assets and font loading before rendering. Preserve Urdu shaping/RTL. Recompose each requested aspect ratio; resizing the same layout is not sufficient.

Studio provides composition selection, frame navigation, playback and export. Edits to authored code update its preview. Do not promise a general CapCut-like drag-and-drop editor or newer Studio interactivity APIs without implementing and verifying them against the installed version.

## Reusable animation and caption components

`src/components.tsx` includes an image/content layer with a shared transform for attached children, frame-derived smooth motion, a fade-through transition, a local-font loading hook and a caption track. Use them where they fit; author additional mechanics from the story. They are not a physics engine or a substitute for character rigs, real maps or good choreography. `AssetLayer` holds its initial/final poses outside the motion interval; use Sequence when a layer should only exist during a shot.

Set `project.json` captions to an array of `{ "start": 1.2, "end": 3.4, "text": "A meaningful phrase." }`. Times are seconds, `[start,end)`. Use actual narration alignment; keep purposeful gaps and avoid overlapping captions unless composing them deliberately. CaptionTrack preserves whole-string shaping and accepts `direction="rtl"` plus a supplied local font for Urdu. Load fonts through `useLocalFont` at the composition's top level and inspect real glyph output. Fonts and generated artwork are story assets, not mandatory files shipped with the skill.

## Narration without a hidden plugin dependency

Read [narration choices](narration.md) first. The following commands apply only to a selected ElevenLabs route. Voicebox, supplied audio and no narration are equally valid; none requires this helper. Model/endpoint compatibility must be verified before a paid request.

Prefer the connected ElevenLabs Voice plugin when available. The bundled `scripts/elevenlabs_voice.py` is also a standalone stdlib CLI copied from the user's ElevenLabs Voice implementation (v1.1.1); it does not register a plugin. Read preferences, resolve the requested voice, discover model/language support, then generate only when narration is requested:

```sh
python3 scripts/elevenlabs_voice.py preferences
python3 scripts/elevenlabs_voice.py check
python3 scripts/elevenlabs_voice.py voices --search "requested voice"
python3 scripts/elevenlabs_voice.py models
python3 scripts/elevenlabs_voice.py generate --text-file narration.txt --voice-id VERIFIED_VOICE_ID --model-id VERIFIED_MODEL_ID --output-directory /absolute/path/to/film/audio --name narration
```

Replace verified IDs; never ship or invent account-specific defaults. Credentials are read from ELEVENLABS_API_KEY or the existing macOS Keychain item. For new macOS setup, `python3 scripts/elevenlabs_voice.py setup --gui` uses a masked prompt. On other platforms configure the environment securely. Never place keys in browser code, command arguments, source, exported archives or chat. Existing saved voice/model preferences remain external to the bundle. Do not set a persistent default without user intent.

Generation saves MP3, alignment/subtitles where available, exact script and receipt. Timeouts or uncertain outcomes require receipt inspection, not automatic paid retries. A rejected clone remains selected; report the actual denial and let the user choose a fallback. Account permissions and credits cannot be bundled. Research, installation and skill audits do not authorize paid test narration.

Copy the chosen audio into public/, measure its decoded duration, align beats/captions to actual phrase times and preserve speech tails. Do not force narration into an arbitrary duration by truncating it. The shared CLI uses discovered model capabilities; for advanced language/settings options use its call_tool Python API or the connected plugin's declared schema, not guessed CLI flags.

## Background audio and timeline integration

Read [python-background-audio.md](python-background-audio.md). The initializer places that skill's generator in audio-tools/. Author a new JSON score for this story; never reuse the smoke-test score as an automatic soundtrack. Render sections for films beyond the generator's 120-second limit. Keep events, music ducks, narration, captions and visual contact times on the same story clock.

`project.json` audio entries use public-relative paths and seconds:

```json
{"src":"narration.mp3","startSeconds":0.2,"durationSeconds":8.6,"volume":1,"trimBeforeSeconds":0}
```

The duration is a placement limit: measure the source and ensure it includes the complete speech. Place either the combined background WAV or its separate stems, not both. Audio volume is a linear multiplier, not decibels. Set musical ducking in the authored Python score. If you mix/master externally, attach just that finished mix. Review levels, true peak and intelligibility; numerical loudness checks do not replace listening.

## Render and review

```sh
npm run typecheck
npm run still -- --frame=45
npm run draft
npm run render
npm run review
npm run serve -- --port=4183
```

The explicit composition is Film; update the commands if renaming it. The review script checks actual dimensions, FPS, picture duration, expected audio presence and decoding; it creates a contact sheet, stream report and loudness analysis. It intentionally leaves visual, playback and listening judgments pending.

Inspect full playback, slow or sample fast transitions, test Play/Pause/Replay, verify captions, contact geometry and the final hold. Open the finished-film player in Chrome at the reported URL; keep it running when localhost delivery is requested. Its controls are outside the picture. Report missing review modalities honestly. A passing starter or script cannot certify a later film's story, graphics or physics.

Deliver the rendered MP4, source project, asset origins and a review record for the final revision. Preserve earlier approved films. External publishing or YouTube uploads are separate actions, performed only when requested.

## Version and API references

The included lockfile retains the previously checked4.0.516 stack. That historical check does not validate the new4.0.0 catalogue/profile changes; focused 4.1.0 initializer/cadence checks are recorded separately. Retain compatible existing dependencies; upgrade Remotion packages together and test changes before using new APIs. Official references: [CLI](https://www.remotion.dev/docs/cli), [frame animation](https://www.remotion.dev/docs/animating-properties), [audio](https://www.remotion.dev/docs/html5-audio), [ElevenLabs speech with timing](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps). APIs and service permissions can change.

## Motion proof before full render

The initializer also bundles `motion-tools/motion-core.mjs` and its tests. Run `node motion-tools/test-motion-core.mjs` for bounded helper checks, then validate actual shot geometry and visible artwork using [physics-and-review.md](physics-and-review.md). `storyPlanStatus` and `motionProofStatus` start incomplete; changing those labels does not constitute review. Resolve [script/runtime conflicts](script-duration.md), author the chosen treatment's independent shot plan, and pass its hardest representative motion proof before producing the full film. The starter composition is an engine demonstration, never the requested story.
