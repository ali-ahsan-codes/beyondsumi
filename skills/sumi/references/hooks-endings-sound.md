# Opening hook, ending and dramatic sound

Use story-led emphasis for all three styles. This updates the earlier blanket small-text instruction: **opening/topic typography may be prominent; continuing narration captions remain compact**. Preserve the fonts the user likes and adapt treatment to the style and actual framing. No new unapproved spoken words or runtime changes.

## YouTube storytelling and documentary context

All three styles make directed YouTube films: establish the subject/promise promptly, connect story beats clearly, vary framing with a reason and resolve the promise/consequence at the end. Original emphasizes richer painted character animation; Light suits romance, children’s/general stories and documentaries; Dark suits horror/mystery/dark stories. These guide recommendations, not permission to override a user's selection or factual brief. Documentary reconstruction, time/place cards and factual claims must be clear. Do not stretch the intro, invent clickbait claims or add an unrequested subscription/outro message.

## Opening

Give the first beat a clear subject, tension/question and visible action. A brief opening topic/title can be much larger than subtitles, typically 2–6 words inside a **maximum 3-second total visibility window**. Count from the first visible word or title backing through the fully cleared title, including entrance, readable hold and exit; do not add a separate 3-second hold. At 1080p, roughly 64–96px is a starting range for a short hook, not a universal fixed size. Avoid faces, hands and the action centre; shorten or reflow text rather than clipping it. Bring words in **individually**, in reading order, using small deliberate offsets; keep earlier words settled while later words enter. Hold the completed title steadily for reading, then clear it before the three-second limit. A long approved title may use short readable phrase groups rather than rushed tiny words; record the grouping and retain the exact approved wording. Do not add a silent bumper, speed up speech or lengthen the film. Do not animate every narration word as a large headline.

For Light/Dark, reveal the hook with a motivated brush deposition or a restrained recorded splash/ink backing. For Original, use its distinct Sumi Anime-inspired opening: a meaningful character/scene hook, elegant prominent title with clean masks/spacing/scale, layered paper/mist depth and story-led music, without animated brush handwriting or splash reveals. Follow the [Original presentation guide](styles/sumi-original.md) for full-frame16:9 and compact stylish captions raised above their usual bottom position. Align the key sound with the visible reveal/impact. Prefer the actual title or an approved story phrase; a surprising new factual claim requires verification and script approval as appropriate.

Plan the topic reveal as a coherent opening mini-scene: story-appropriate imagery/camera, attractive title entrance, a short musical build or intentional quiet, and synchronized material sound. An intense siege may use a low musical accent; a tender story may need a gentle resolving note. Dramatic means emotionally apt, not automatically loud, violent or drum-heavy. Protect the first narration line, retain approved words/runtime, and let the title hold long enough to read.

## Ending

Show the consequence before the title/end card. Give the final image or line room to register within the approved runtime; let sound decay into the final hold. A considered title, brush mark or neutral seal may finish the composition. A standalone closing title also has at most 3 seconds total visibility, with individually entering words when it has several words. A final spoken moral or ordinary narration caption keeps its required reading time; it is not a title card. Light can use an established pigment accent; Dark keeps its neutral base with purposeful approved dark-red accents; Original retains its own treatment. Do not end by abruptly stopping every layer or add an unrelated call to action.

The end must receive an explicit animation and sound plan, not a static afterthought: let the consequence register, reveal an elegant final phrase/title with the style's material, hold for reading and let the score/ambience resolve. Original can use a tender painted resolve; Light a clear documentary conclusion; Dark a final camera settle, pigment dispersal and restrained red motif. These are options; avoid covering the last narration line with a large title or abrupt loud sting.

## Sound hierarchy

Plan a cue ledger with film output frame, visible cause, material, narrative purpose, stem, relative gain, attack, decay and voice overlap. After narration retiming, rebind cues to the **actual visible event**. Recheck cause → impact → reaction and retained silence. Do not schedule from similarly named but different story/output clocks.

Separate narration, score, ambience and effects. Keep narration intelligible, while allowing the story's important physical events to be heard. Duck the music bed around voice rather than automatically weakening every impact. An isolated hero effect in an appropriate speech gap may start around 3–6dB above quieter effects; this is a relative mixing suggestion, not a fixed final gain. Use source quality, layering, timing and contrast before adding loudness. Preserve headroom and measure final peaks/loudness; do not raise the whole mix or clip it for drama.

Examples of directed contrast:

- Drums gather tension while shown/heard in the world; when the story says **the drums stopped**, actually stop them. Let that silence make the command meaningful. Do not increase drums over the word “stopped.”
- An arrow volley has a directional onset, passing air and selected impacts. Avoid one generic whoosh for the entire action.
- A gate strike has a low body hit, a short wood crack and falling debris. Align the first hit to contact; do not cover the dialogue with continuous rumble.
- A blade clash can briefly rise above the preceding bed, then decay; the reaction and recovery need their own audible space.
- A final grief/aftermath beat can reduce density rather than escalate. Let the last voice line land cleanly and retain a deliberate tail.

These are options, not mandatory additions to gentle stories. Use the approved local Python synthesis method and its material-specific generators by default; describe its synthetic character honestly. Listening and visual sync must be checked on the actual final mix when a capable modality is available. Meters, cue lists and playback completion do not prove emotional impact or listening quality; disclose unperformed listening.

## Title timing record and check

For each opening/closing title, record first-visible start, fully-gone end, the ordered words/phrase units and each unit’s start/settled times in `title_timing.cards`. New projects initialize this as pending. Run `python3 scripts/validate_title_timing.py shot-plan.json`; the current production validator also invokes it for releases from4.9.1. It checks declared timing, not pixels or artistic readability. Inspect entrance, completed-title hold and first title-free frame in the actual export; include the backing in the same visibility window. Existing historical films are preserved unless their revision is requested.


## Story captions and audible non-narrated sound · 26 October 2026

Owner clarification applies to **Sumi Original, Sumi Light and Sumi Dark**, including SVG artwork: retain compact readable story captions even when there is no narration or dialogue, unless the user explicitly asks for a text-free film. Write concise scene-linked captions from the approved story so the viewer understands cause, action and consequence. Spoken films still use approved speech-aligned captions. Keep faces/hands/feet and important action clear, use the style's appropriate backing, and preserve the separate three-second title rule. No sample signatures, scene labels, technical notes or other unapproved text belongs in the film.

Without narration/dialogue, music and environmental sound carry the film. Keep an attractive, clearly audible, story-shaped background score; do not leave narration ducking active across a speechless film. Layer distinct contact-aligned material effects and ambience, with purposeful build, brief contrast, impact and a resolved ending. Rich sound is not continuous maximum volume or a generic whoosh over every frame. Preserve deliberate dramatic quiet, recover the score, avoid clipping, measure the encoded mix and audition when the modality is available. Meters and unmuted browser playback do not constitute independent listening approval. Use the selected library/Python route and ask before any new paid acquisition.

## Sound coverage is required

Sound is a core story requirement for all three styles and both image/SVG art routes. Before production, give **every scene** a score state (active/reduced/intentional silence with reason), ambience or a justified quiet setting, and the important action SFX with their cause/contact. Do not leave this until after the images or assume that narration alone completes the soundtrack. The assistant reads the story and authors this sound plan; our Python engine composes, synthesizes and mixes the planned cues. Use the selected library/Python route and actual supported designs.

For each story-important sound record its asset/design, start/build, event or stop frame, voice overlap, gain/duck recovery, decay and a review time. If narration says drums play and stop, the rendered mix must contain clearly audible drum strokes before that stop, then the intended contrast. A silent source, a cue hidden beneath speech, an empty stem or a label saying “drums” does not fulfil the beat. Do not add drums to every story; use the material and feeling the story needs.

Before delivery compare the final script/visible event list with the actual stems and encoded mix. Review the opening, each hero contact, named sound entrance/stop, major mood change and ending; check that score and setting do not disappear through accidental ducking, missing files or wrong clocks. Record each cue as heard/needs repair/unverified with its time and real observation. Repair confirmed omissions before calling the soundtrack complete. If sensory listening is unavailable, keep that status unverified; cue metadata, meters and unmuted playback do not prove audibility. Preserve deliberate quiet with an explicit reason rather than filling it with noise.
