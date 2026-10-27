# ALI Animation story JSON (schema version 1)

The **Download blank story template** button gives a ready-to-fill `.json` file. You can also write a JSON file following this minimal format and use **Import project**. Import is validated before any project is replaced.

```json
{
  "schema_version": 1,
  "title": "The Lantern Keeper",
  "genre": "Adventure",
  "aspect_ratio": "16:9",
  "audience": "Family, ages 8+",
  "target_seconds": 32,
  "logline": "A keeper takes her last lantern to guide a stranger home.",
  "story": "Write the complete beginning, middle and ending here.",
  "characters": "Mira — age, appearance, clothes, personality, voice.",
  "visual_style": "Ink & wash",
  "palette": "Midnight blue, warm amber, paper ivory",
  "fps": 24,
  "voice_plan": "Narrator voice, language, pace, tone; note character voices.",
  "music_notes": "Mood, instruments, intensity, where music starts and stops.",
  "rights_note": "Who made the supplied media or what permission applies.",
  "assets": {},
  "scenes": [
    {
      "id": "shot-01",
      "title": "The fading beacon",
      "slug": "EXT. LIGHTHOUSE · NIGHT",
      "duration": 9,
      "camera": "Wide establishing shot",
      "action": "What the audience sees; character movement and important props.",
      "narration": "Exact voiceover words for this shot.",
      "dialogue": "Character name and exact spoken line, or empty string.",
      "sound": "Ambience, sound effects, music cue, and silence/transition notes.",
      "transition": "Cut, dissolve, fade, or match cut."
    }
  ]
}
```

## Fields and production checklist

- **Story:** original premise/logline, full script with beginning–middle–ending, audience, target duration and ending beat.
- **Characters:** name, age range, silhouette, face/hair, clothing/colours, personality, consistent details, voice/language/pronunciation.
- **Each scene/shot:** location/time, duration in seconds (1–120), action, exact narration/dialogue, camera shot/angle/movement, transition, ambience, effects and music cue. Duration is the sum of scene durations.
- **Camera menu:** wide establishing, medium, tracking, close-up/insert, over-the-shoulder, low angle, high angle, point of view, push-in, pull-back, crane up or locked frame. Include explicit intent in the action if you need a special move.
- **Media:** optional image reference, voiceover, music and sound-effect files in the Assets/Sound tabs. Use your own work or confirm permissions. Each upload is limited to 15 MB; a project file is limited to 35 MB. Media is embedded into exported project JSON as a data URL so it can travel with the story.
- **Voice:** upload a human voice recording for dependable offline narration. “Try installed system voice” is only available if the operating system/browser already has a local speech voice; it does not synthesize a downloadable narration track.
- **Final sound:** voiceover and music are mixed into the WebM recording; assigned SFX are played at their scene/time offsets. Review loudness and sync before publishing. Imported project JSON is the editable master; WebM is a review/export copy.

SFX array format: `"sfx": [{"name":"bell.wav","type":"audio/wav","data":"data:audio/wav;base64,...","start":12,"scene":1}]`. Uploaded image/voice/music use `{ "name": "...", "type": "...", "data": "data:..." }` in `assets.image`, `assets.voice` and `assets.music` respectively. Keep media small; remove the `data` fields to create a lightweight text-only project.
