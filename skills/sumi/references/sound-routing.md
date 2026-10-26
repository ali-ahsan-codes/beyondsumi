# Choose sound separately from narration

At first use/new project when not already chosen, ask: **“Use the Sumi sound library, or create fresh sound with our Python engine?”** Recommend library-first; remember an explicit reusable choice when requested. A project-only choice does not overwrite a default. The library, Python engine and narration provider are separate components.

Library-first priority:

1. Reuse a suitable user-authorized saved music/effect, matching material, mood, contact, duration and quality. Verify hashes and audition status. A similarly named sound is not automatically suitable. Keep the cache outside source code/film exports.
2. If a needed effect is missing and a verified ElevenLabs connection supports Sound Effects, offer a concrete prompt/duration/count and cost limit. Ask before the paid call unless that exact request/budget is already approved. A key or narration setup is not permission to spend on SFX. Submit once, save receipt/source/metadata privately, reuse/import the completed result. Inspect uncertainty instead of automatic retakes. Never start a paid batch merely to fill a library.
3. If ElevenLabs is absent, unsupported, declined or a local result is preferred, create the missing cue with our model-free Python engine. No API, speech model or new audio dependency is needed. Unknown material designs may need authored synthesis; do not replace every request with a generic whoosh or promise exact realism.

**Python-only:** bypass cached provider effects and paid SFX even if connected. Compose requested music and synthesize effects/ambience locally from the cue plan, retaining separate stems and seeds. The user can request a new sound or a completely local soundtrack. Prefer meaningful material designs over unnecessary noise. Existing supplied sound may be used only if the user explicitly requests it instead.

Voicebox is a narration option, not an assumed foley/music generator. Someone using Voicebox can use the same sound library and Python engine. ElevenLabs SFX is available only if separately connected/authorized; do not secretly route a Voicebox project to a paid provider. A supplied human narration uses the same sound choices without TTS.

The [router](../assets/sound-library/route_sound.py) prepares a new, hash-bound working bank and cue ledger. `--mode library-first` is the renderer default **after the user makes this choice**; conversational intake still asks when unspecified. `--library-root` or `SUMI_SOUND_LIBRARY` points to the separate cache; `--music-root` defaults to the bundled12original music themes. `--elevenlabs-available` is a host-attested verified capability, not credential discovery or permission. When a missing cue could use that service, the router writes NEXT-ACTIONS.json and exits3 without media/provider work; ask Generate with ElevenLabs or Use Python. After approval/import rerun, or use `--missing-action python`. It never makes API calls.

```
python3 /path/to/sound-tools/route_sound.py prepare --plan audio-plan.json --out work/audio-choice-v1 --mode library-first --library-root /user/sound-bank
python3 /path/to/sound-tools/route_sound.py render --plan audio-plan.json --out work/audio-local-v1 --mode python-only --review-draft
```

Plans use the existing frame-clock cues/ducks. Optional per-effect `python_kind`, `python_duration`, `python_seed` and `source_policy:"python"` select an authored local design; derived cache IDs prevent conflicts. Render only explicit review drafts for pending auditions/contacts; no asset is automatically marked approved. Listen to source/tails/loops and the actual final mix, verify speech duck/recovery and measure encoded loudness/peaks. Preserve original files and older films.

Distribution: the ordinary user package contains our12Python music themes/source plus the synthesis/composition/mixing code. No provider WAVs or recordings/keys are in it. The owner's separate private effect pack contains the32previously generated ElevenLabs effects with provider terms; it is not a free redistribution license. Do not add duplicate pre-rendered Python replacements to that selected library. The Python engine creates a missing/local-only cue on demand. Generated sounds remain synthetic impressions, not guaranteed acoustic recordings.

New film projects copy engine code, not the full224MB music bank. Their local `sound-tools/library-location.json` points to the installed suite’s shared original music cache; a supplied `--music-root` overrides it. If moved to another machine, choose that machine’s bank or rebuild selected music locally. Effect cache stays separate. No user recordings or provider library are automatically copied into each film.
