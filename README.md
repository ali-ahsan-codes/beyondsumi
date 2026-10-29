<p align="center"><img src="docs/screenshots/ali-animation-interface-preview.png" alt="ALI Animation offline story studio interface preview" width="100%"></p>

<h1 align="center">ALI Animation</h1>
<p align="center"><strong>Offline Story Studio — direct a story, animate a preview, export a video.</strong><br>Local-first. No AI, account, API key, or internet connection required at runtime.</p>

**[Open the Studio](studio/index.html)** · **[Standalone HTML installation & user guide](ALI-Animation-Guide.html)** · **[Install notes](INSTALL.md)** · **[Story JSON format](studio/story-format.md)** · **[4 sample projects](studio/samples/)** · **[UI preview](docs/screenshots/ali-animation-interface-preview.png)**

ALI Animation is a self-contained browser app for story-first animation. Write the story and characters, direct scene-by-scene camera angles, add voice/music/effects and reference art, preview the animation, and export a portable JSON project, PNG frames, and WebM video. Projects and media remain on your device.

## Start in minutes — no AI model

ALI Animation Studio is for a fully manual workflow: you write the script, choose each shot's camera angle and duration, and supply any voice/music/art yourself. It does not generate a script, angle, image, or voice with AI.

1. Download/extract the project and have Python 3.8+ installed. No Python packages are needed.
2. **Windows:** double-click `install.bat` for the first-run check and launch; later, double-click `start.bat`. You can also run `python install.py` (or `py -3 install.py`) from the project root.
3. **macOS/Linux:** from the project root run `python3 install.py`.
4. The local Studio opens in your browser. If it does not, visit the URL printed by the launcher (normally `http://127.0.0.1:8765`). Keep the launcher window open while using the app; press **Ctrl+C** there to stop it.

The launchers only check for Python and start the local app; they do not download models, install packages, or contact a cloud service. `--skills-root` is separate optional legacy tooling and is not needed for Studio. See [INSTALL.md](INSTALL.md) or the [standalone HTML guide](ALI-Animation-Guide.html).

## What is included

- **Four complete story samples:** The Lantern Keeper, The Last Seed, The Moon Ferry and The Brave Little Cloud. Each has three shots, a story, characters, camera directions, narration/dialogue, sound cues, transitions and timing.
- **All-UI project editing:** story, logline, characters, genre, target length, visual style, palette, freely typed camera angles (with suggestions), shot timing, narration, dialogue, transitions, sound cues and reference art.
- **Import/export:** fill the UI or import a versioned JSON file; export the editable project with uploaded media embedded. A blank project template and field-by-field format guide are included.
- **Local preview + exports:** procedural 2D animation in Canvas, timeline playback, PNG stills, and browser-generated WebM video. Uploaded narration/music and timed SFX can accompany the video.
- **No app dependencies:** Python's standard library serves the files. No packages, AI, service, key, or online API are used by the Studio.

The Canvas output is an offline story animatic, not a full hand-drawn production package or a professional video editor. Speech playback depends on voices already installed on the user's computer; for dependable narration, upload a recording you own. WebM export depends on browser support. Read the scope and caveats in [INSTALL.md](INSTALL.md).

## Test

```sh
node --test studio/test-*.mjs
python -m unittest discover -s tests
```

## Existing repository material

The existing `skills/` directories contain the earlier ALI Animation/Sumi assistant plugin, studies, examples and production recipes. They are retained as legacy source; ALI Animation Studio does not call or require that assistant workflow. Only rename/update those integrations separately if they are still needed.
