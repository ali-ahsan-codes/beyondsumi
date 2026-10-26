# Reusable local sound library

Use for all three Sumi styles. Choose sound from the story, material, location,
emotion and timing. The sound library is separate from narration and from the
picture engine. It does not change the approved words, duration, FPS or acting.

Read [the sound-choice priority](sound-routing.md) before preparing cues: ask library-first versus Python-only, reuse a suitable cache, offer connected/approved ElevenLabs for missing effects, then local Python fallback.

## What is included

[Sound tools](../assets/sound-library/library.py) run with Python standard
library. [Twelve original mood recipes](../assets/sound-library/catalog.json)
cover tenderness, love, grief, hope, wonder, journey, documentary, mystery,
suspense, dread, battle and resolution. Each has an authored motif, chord
sequence, tempo, voicing and rhythmic treatment. [The composer](../assets/sound-library/music.py)
renders separate harmony, melody and rhythm WAVs plus a preview and note ledger.
These are synthetic instrument impressions; do not describe them as a recorded
orchestra, real Japanese instruments or guaranteed finished film music.

The user package contains ready-made12Python music themes and their editable parts/recipes. The catalogue also contains32 custom effect acquisition prompts, not32 bundled
recordings. A user's acquired effects live in their own local library. Existing
compatible reviewed audio should be reused before another generation. Never
automatically spend credits to fill a library at install or first film use.

## Build once and reuse offline

Choose an external user library directory. Do not write generated audio into an
installed skill or silently copy one person's library into a generic package.

```sh
python3 /absolute/path/to/sumi/assets/sound-library/library.py build-music --root /absolute/path/to/user-sound-bank
python3 /absolute/path/to/sumi/assets/sound-library/library.py list --root /absolute/path/to/user-sound-bank
```

No model, API call, package installation or PortAudio is needed for composition,
cataloguing and mixing. FFmpeg is used to convert imported audio to48kHz/16-bit
stereo PCM. Reuse an available installation; follow setup approval if absent.
Keep originals, prompts, receipts, hashes and prepared WAVs. Hash-check before
reuse. A changed recipe/composer requires a new library revision, preserving the
old one. The small [procedural engine](python-background-audio.md) remains a
no-cache fallback and a source of precisely authored supplementary layers.

## Optional one-time acquisition

When the user chooses ElevenLabs for effects, use the independent
[acquisition helper](../assets/sound-library/generate_sfx.py), not the offline
renderer. Read the exact prompts/durations/model/output format, current official
pricing and account state. Obtain a concrete batch/budget authorization when
not already covered. Credentials come from the existing environment or approved
Keychain connection, never from chat or project files. The approval file binds
to the exact catalogue hash and total duration/count; it is private project data.

One call produces one effect. Reuse completed hash-matching receipts, stop on
failure/uncertainty, and never automatically retry. An uncertain receipt can
represent a charge. Inspect/recover saved data before any further paid action.
Record provider-reported credits and distinguish the published-price estimate
from a verified invoice. Models/terms/prices can change; verify official sources
before a new acquisition, not before ordinary offline reuse. Do not claim AI
output is exclusive or grants unrestricted redistribution. Keep provider audio
outside the distributable skill unless its redistribution rights are established.

```sh
python3 /absolute/path/to/sound-tools/library.py import-sfx --root /absolute/path/to/user-sound-bank --source /absolute/path/to/acquisition-output
```

Import does not normalize every effect to full loudness. It preserves source
level, measures it and suggests an onset candidate. That candidate is not an
auditioned contact anchor. Listen to the dry sound, tail, noise, unintended voices
or music, material identity and intended use. Listen across ambience loop joins.
Reject unsuitable audio rather than compensating with volume or a new filename.

## Audition and actual-use review

All new music/effects start pending. A normal render rejects pending assets.
An explicit `--review-draft` allows auditions and lists every pending asset in
the report; it never marks the soundtrack approved. Record only an actually
performed listening review with meaningful observations and, for effects, the
auditioned onset/contact anchor. `record-review --help` exposes the CLI. Do not
mark approved from meters, hashes, generated prompts or positive feedback on an
unrelated film. Per-asset approval still does not certify a film mix.

## Arrange for the movie

Use a frame plan with `fps`, `duration_frames`, `cues` and optional `ducks`.
Each music cue names a mood, `at_frame`, `duration_frames`, selected `parts`
(`harmony`, `melody`, `rhythm`), gain, fade-in/out and explicit `repeat_body` when
needed. Each effect names its ID, actual contact `at_frame`, gain and pan. The
renderer aligns the reviewed contact anchor, reserving the full preroll and
tail. Ambience can repeat only when requested as a loop; its join needs review.
Keep rhythm and musical changes on useful phrase boundaries. A safety ramp at
repeated waveform boundaries prevents abrupt sample jumps but does not prove
that a musical/ambience join sounds natural. Check and prepare a better loop or
compose a longer phrase when necessary. Do not stretch dialogue or pad a film.

Select only the cues the story needs. During an intimate confession, remove
rhythm and simplify harmony; build a warning with a sparse motif; establish real
drum strokes before stopping; let a reveal breathe. Choose an ending suited to
the actual emotion. Avoid running all12 themes or continuous effects through
every story. These recipes are starting compositions, not fixed mandatory tunes.

Ducks use `start_frame`, `end_frame`, gain and attack/release, with optional
`stems` (`music`, `ambience`, `sfx`). Overlaps take the minimum envelope once and
recover to the original stem. Write independent music, ambience, SFX and combined
background WAVs, with shared headroom attenuation. Use the combined background
or components, never both. Mix narration separately in the existing film
pipeline. Author180-second-or-shorter sections for long films and explicitly
handle their joins. Exact source/cue tail overruns fail instead of being cut.

Measure loudness/true peak on the final encoded mix and listen to speech overlap,
opening, important contacts, drum stop, loop/section joins and ending. Record any
unperformed listening. No meters alone can choose the “best” sound.

Environmental motion: use [the shared living-environment plan](living-environments.md) before rendering. Select local story-led motion or deliberate stillness, retain this style’s palette/cadence, and bind effects/masks to each actual source.
