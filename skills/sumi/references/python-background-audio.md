# Background audio: local Python synthesis and reusable sounds

For a new complete film, create story-appropriate background sound with Python synthesis by default. Narration is a separate [provider choice](narration.md) when requested. Explicit silence, supplied music, a different requested method or preserving an approved soundtrack takes precedence. Research-only tasks do not require soundtrack generation. Deliberate quiet passages are part of sound design.

For reusable mood music and acquired effects, use [the local sound library](sound-library.md). It adds12 authored Python music recipes, editable harmony/melody/rhythm parts and an optional user-owned effect cache, with audition/contact/loop review before normal use. This existing generator remains the lightweight no-cache fallback. Normal composition and mixing are offline; one-time third-party acquisition requires its own explicit scope and budget.

## Direction for this skill

Sparse tonal space, breath-like sweeps and restrained physical accents can suit an ink story. Do not claim synthetic tones are authentic traditional instruments; let the actual theme decide whether rhythm or silence belongs.

The bundled eight-second score is a runnable demonstration, not a fixed soundtrack. Write a fresh score for the actual script, duration, action and mood. Vary rhythm, tonal register, harmony, instrumentation and density deliberately. The default is the production method, not one tune or a promise of orchestral realism.

## Film-specific material sound

Design a cue ledger from the approved script and actual output frames before synthesis. Each audible event has a visible or narrative cause, onset/contact frame, material, duration/tail, stereo position, distance, gain and voice overlap. Build selected hero sounds from complementary transient/body/tail layers rather than repeating the same generic whoosh. Sparse, distinctive cues and intentional quiet often read more clearly than continuous noise.

- **Original / emotional stories:** soft tactile brush, cloth, small grounded steps, weather boundaries and a restrained musical motif/resolve. Leave room for intimate narration and pauses.
- **Light / documentaries:** clear illustrative material cues, location ambience and selected explanation/reveal accents; keep facts and narration intelligible. Rhythm supports the argument rather than making every sentence a trailer.
- **Dark / dark stories:** larger brush/liquid gestures and camera-linked air movement, weighted drums/impacts at selected dramatic beats, dark-red motif cues where relevant, and quiet dread/aftershock. Bigger splashes do not mean every sound is louder.

The local renderer now includes original `material_sfx.py` generators: `brush`, `ink_drop`, `splash`, `footstep`, `cloth`, `wood_crack`, `blade`, `drum`, `rain`, `wind`. They are synthetic material impressions, not recordings or authentic instrument reproductions. Use `freq` for appropriate drum/blade/drop pitch variants; gain/pan/timing remain event fields. Different timing/gain/pitch can avoid mechanical repetition, but footfalls must stay aligned to actual landings. A blade cue needs actual contact; a visual brush reveal needs its own tactile onset.

A drum stop needs recognizable strokes/rhythm before the stop. Schedule drum events and their decays so the intended silence is audible; inspecting a silent interval alone is insufficient. A title rise should reach its accent at the visible title landing, and end effects should decay within the approved runtime. Keep rain audible and visible without filling shelter interiors with identical rain. Every important transition is not automatically a drum hit.

Keep separate music/SFX/narration stems, measure the final encode and listen at ordinary playback level. Check the opening/topic, every important contact, the drum-stop contrast when relevant, voice overlap, transitions and final decay in context. If a capable listening modality is unavailable, record that limitation instead of calling the sound amazing from meters. Improve synthesis or use explicitly authorized supplied audio if it fails the story. No third-party audio service, model or installation is needed for these generators.

## Self-contained generator

This skill includes [the generator](../assets/procedural-audio/render_audio.py), [synthesis primitives](../assets/procedural-audio/synth.py), [example score](../assets/procedural-audio/example-score.json) and [MIT license](../assets/procedural-audio/LICENSE). Python standard library only; no API key, external samples or Python package installation is needed. Synthesis is local and consumes no ElevenLabs credits.

Copy `assets/procedural-audio/` into the video's project as `audio-tools/`, retain LICENSE, and adapt its JSON score. Run in that project:

```sh
python3 audio-tools/render_audio.py audio-tools/example-score.json --out audio/background-v1
```

Use a new output directory for each revision. Never render into the installed skill. The output contains aligned `music.wav`, `sfx.wav`, `background.wav`, the exact score and a measurement report. All WAVs are 48 kHz, 16-bit stereo. Use either the combined background or its separate stems, not both together.

## Score contract

- `duration`: seconds, 0.1–120. For longer work render authored sections and assemble them in the film timeline; handle section boundaries and tails intentionally.
- `seed`: integer, for repeatable noise with identical inputs and runtime.
- `beds`: each has `at`, `duration`, `gain` and `chords`. Chords are `[local_seconds, [frequencies_in_Hz]]`, strictly increasing, starting at zero. Choose the harmony rather than randomizing it.
- `events`: each has `at`, `duration`, `kind`, optional `gain`, `pan` (-1 to +1), and `stem` (`music` or `sfx`). Kinds: `pluck`, `bell`, `tone`, `click`, `impact`, `whoosh`, `riser`, `scratch`, plus `brush`, `ink_drop`, `splash`, `footstep`, `cloth`, `wood_crack`, `blade`, `drum`, `rain`, `wind`. Tonal events accept `freq`; sweeps accept `f0` and `f1`. Times and tails must fit the score.
- `ducks`: speech intervals with `start`, `end`, `gain` (0–1), optional `attack` and `release` in seconds. Only music is ducked; lower competing effects separately. Derive intervals from the real narration, not a guessed word count.
- `fade_in` and `fade_out`: seconds; set explicitly for very short sections. `ceiling_db` limits sample peaks with attenuation only. Defaults preserve headroom; they are not loudness mastering or a true-peak guarantee.

Generate event times and duck intervals from the film's timing source. The JSON is an adapter for audio; do not force unrelated scene schemas into it. A riser starts before its intended payoff and reaches it at the sound's end; distinguish this from a hit starting at contact. Inspect the actual waveform and playback, because synthetic timbres have different perceptual attacks.

## Voice and mixing

Generate requested narration through the chosen provider or use supplied audio, honoring secure credentials, saved voice/model preferences and actual language capabilities. Skip voice generation when narration is declined. Keep narration separate from the music and effects. The generator does not itself call ElevenLabs, read credentials, detect speech or mix the voice.

Place all stems in the existing editor/renderer, or mix with FFmpeg. Keep music lower than speech, use the planned duck intervals, and retain silence where the story needs it. Do not normalize each quiet stem independently to full loudness or add both `background.wav` and its component stems. If the narration exceeds the planned duration, retime the film rather than silently truncating it.

Headroom attenuation is applied before PCM conversion with the same gain across stems. This avoids hard-clipping and preserves the stem balance. Loudness and true peak still need measurement on the final mixed/encoded film, with listening for intelligibility, clicks, pumping, abrupt tails and excessive repetition. A quiet score should not be boosted merely to reach a universal LUFS value.

## Review and limitations

Check duration, sample rate, non-silence where intended, exact event placement, fades and all output files. Listen to the complete film and assess the chosen music against the story. Do not report auditory quality from numerical tests alone. If the timbre does not serve the requested result, improve the synthesis or use authorized supplied/generated audio and explain the change.

These primitives provide electronic tones, pads, pulses and designed noise textures; they do not automatically reproduce realistic orchestras, acoustic instruments or field recordings. Suitable alternatives remain available when needed. This bundled generator runs without another skill installed.

## Attribution

`synth.py` is adapted from the existing MIT-licensed whaleyxbt/claude-motion toolkit, with descriptive changes removing fixed per-video accent counts. `render_audio.py` is an original adapter bundled with this skill. The earlier toolkit and approved film scores remain preserved.
