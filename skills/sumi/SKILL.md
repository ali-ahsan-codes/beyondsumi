---
name: sumi
description: "Create and revise Japanese Sumi animated films in Sumi Original, Sumi Light or Sumi Dark. Guide setup, story, direction, original artwork, animation, narration, local sound and review."
---

# Beyondsumi · Sumi

Version 1.0.0. A guided local film studio with exactly **Sumi Original, Sumi Light and Sumi Dark**. Use the user's current brief, external preferences and current project record. Preserve prior films and paused work; changing the skill does not resume a film. Keep credentials/recordings outside the portable package.

## Load only what the task needs

- **First use / setup:** [first-run flow](references/first-run-flow.md). Use the separate SVG, ElevenLabs or Voicebox companion only when that route is selected.
- **New film:** ask missing duration, then narrator/dialogue/both. Offer [story-writing help](references/story-writing.md) before [director workflow](references/director-workflow.md), then [scene-first production](references/scene-first-workflow.md) and the chosen style below. Ask only missing questions; retain earlier authorization for the same scope.
- **Revision:** read the project's latest direction/review and inspect the affected sources before editing. Reuse compatible art, takes, code and sound. [Reuse and context](references/reuse-and-context.md) covers cache/provenance and selective reads.
- **Implementation:** [Remotion/local engine](references/remotion-workflow.md). Preserve a suitable existing renderer. No external AI video generation unless explicitly requested.
- **Review/delivery:** [production review](references/production-standard.md), the [portable physics gate](references/physics-gate.md) for new character actions, and [delivery](references/delivery-dashboard.md). Do not infer approval from a helper or packaging step.

## Three styles; images first

- **[Original](references/styles/sumi-original.md):** painted Japanese Sumi-e/Sumi Anime stories, richer character acting and emotional depth; no animated brush/splash reveals. Default full-frame 16:9. New films use 30 fps/20 designed character states per animated second.
- **[Light](references/styles/sumi-light.md):** colourful brush-and-ink romance, children's/general stories and documentaries; readable action and explanation, story-selected washes.24 fps, paired character states up to 12 changes/s.
- **[Dark](references/styles/sumi-dark.md):** horror, mystery and dark stories; large splash-built forms, neutral ink with selective dark red, stronger motivated camera/face/detail reveals.24 fps, paired character states up to 12 changes/s.

These are recommendations, not genre restrictions. All three need cinematic direction and complete storytelling. Preserve each identity; Dark is not a recoloured Light. Older style names are internal historical mechanisms, not extra menu choices. Consult [catalogue history](references/animation-categories.md) only when recovering a technique or resolving an old project.

Default to the selected callable image tool, connected image provider or supplied art. SVG is the user's explicit choice or a disclosed fallback when image generation is unavailable; follow [image capability](references/image-capabilities.md). Do not silently downgrade a painted film. A comparison sample is optional: one image of the same scene in all three styles, after the user asks for it. Do not generate all three films by default.

## Story and approval

Concept/story → script review → direction and duration/cost approval → actual narration alignment → storyboard/rough animatic/layout → contextual artwork/action poses → animation → synchronized sound → export review. Technical preparation may continue while a dependent choice is pending.

Preserve supplied/approved words and required actions. If the full story exceeds 30 seconds or another requested target, show its estimate and a concrete shorter alternative, then wait for the user's selection. Never independently omit beats, rush speech, extend or add dead-air padding. See [duration contract](references/script-duration.md).

The agent directs scenes, expressions, focal subjects, camera, transitions and sound; a beginner need not choose technical settings. Show script first, then the concrete direction plan. Proceed within existing approval without asking about every aesthetic choice. A new paid take/download needs its own authorized scope; a connected key is not spending permission.

## Artwork and animation invariants

Compose complete integrated shots with camera/view, floor, light, scale, occlusion and props planned **before** finished artwork. Derive layers from that coordinated master. Prepare complete sequential action poses/sheets for major movement, inspect cells before cropping, and preserve identity, handedness, support, grip and screen direction. Never assemble unrelated generated limbs or turn a crop into a claimed new camera angle.

Use [whole action preparation](references/action-pose-sheets.md) for movement, [connected expressions](references/expression-and-action-continuity.md) for acting, [Living Frames](references/living-frames.md) for supported face/hair/cloth/breath details, and [visible environments](references/living-environments.md) for scene-linked rain/cloud/fire/light/shadow/reflection. Read only the relevant detailed section. Weather/camera cannot substitute for missing character action. Count actual drawings, derived states, reused cycles and exposures separately;20/12 state targets are not new AI drawings each second. Declare meaningful stillness.

Keep one deterministic output-frame event ledger. Carry [prop, knowledge, route and consequence continuity](references/production-continuity.md) across shots. In Light/Dark, build subjects from wet brush masses matching the background; use action-linked ink and sparse material transitions. Consult [brush construction](references/brush-character-prompts.md), [Light/Dark mechanics](references/brush-ink-workflow.md) or [ink mechanisms](references/ink-transitions.md) only as required. Do not use a fast sideways card slide as a generic ink effect.

## Voice, captions and sound

Follow [narration routing](references/narration.md): ElevenLabs, Voicebox, the user's recording, or none. Read only the selected provider setup. Supplied audio uses [its real recording workflow](references/supplied-narration.md); preserve originals and actual performance. [Character dialogue and lip-sync](references/dialogue-and-lip-sync.md) apply to all three styles, including identified supplied dialogue. Keep narrator prose off character mouths and respect provider-specific casting controls.

[Sound routing](references/sound-routing.md) is independent of voice/artwork: ask library-first versus Python-only unless already chosen. Cache → optional connected/explicitly approved ElevenLabs SFX → Python fallback; Python-only bypasses provider effects. Reuse separate editable music/voice/ambience/effect stems, synchronize contacts and duck/recover around actual speech. Voicebox is speech, not an assumed foley generator.

[Titles, captions and sound hierarchy](references/hooks-endings-sound.md) are the shared authority. Music, ambience and important SFX need explicit scene coverage, including an audible lead-in before a named sound stop; missing sound is unfinished production. These rules apply to all three styles: all styles/art routes retain compact readable story captions even without narration unless explicitly text-free. Without speech, an audible story-shaped score and effects lead; with dialogue, preserve intelligibility. Opening and standalone closing titles last ≤ 3 seconds total, with individually entering words and style-specific treatment. No extra watermarks, sample signatures or technical text in the film.

## Finish honestly

Prove the hardest representative shot before a full batch; inspect actual final artwork, adjacent poses and normal-speed output for crop, anatomy/support/grip, camera, material, captions and consequence. Run checks appropriate to changed areas, retaining valid evidence for unchanged sources. Do not invent visual/listening approval or claim zero errors; record missing modalities and limitations in REVIEW.md.

Deliver HD H.264/AAC MP4 plus the branded Beyondsumi watch/download dashboard and editable source. [Interface branding](references/interface-brand.md) governs pages, not the film's story palette. Show all three editions, with available-file downloads and agent-neutral recreation requests for unmade editions. Verify actual moving pictures and downloads; a poster/timer alone is insufficient. Local URLs require the server; publishing/cloud/GitHub require a separate request. Personal preferences live in [external memory](references/memory.md), project decisions in its concise current record.
