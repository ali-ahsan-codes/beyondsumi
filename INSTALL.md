# ALI Animation — install and use offline

For the standalone, illustrated HTML walkthrough, open [ALI-Animation-Guide.html](ALI-Animation-Guide.html).

**ALI Animation Studio** is a local browser-based animation/storyboard app. It has no AI, account, API key, npm package, Python package, or network dependency. Browser preview, project JSON and supported WebM recording happen on your own computer. The older `skills/` assistant workflow in this repository is a separate legacy toolkit; you do not need it for ALI Animation Studio.

## Quick install — no AI model required

1. Download/extract the repository. Once the files are on your computer, disconnecting from the internet is fine.
2. Install Python 3.8+ if needed. Python's standard library is all that is used; there are no packages or models to install.
3. Open PowerShell/Terminal in the **project root** (the folder containing `install.py`) and run:

   **Windows**
   ```powershell
   py -3 install.py
   ```
   If you already activated a virtual environment, `python install.py` works too.

   **macOS / Linux**
   ```sh
   python3 install.py
   ```

4. The script starts a local-only server and opens the Studio in your browser. If it does not open automatically, visit the URL printed in the terminal (normally **http://127.0.0.1:8765**). Keep the terminal open while using the app; press **Ctrl+C** to stop it.

This default launch path does not install or call an AI model. `--skills-root` is an optional, separate installer for legacy assistant integrations; you do not need it to use ALI Animation Studio. If the default port is busy, the launcher selects another available local port and prints its URL. The server listens only on your computer.

## Roman Urdu — istemal ka tareeqa

- Project root (jahan `install.py` hai) mein terminal khol kar upar diya gaya command chalayein. Launcher browser khol dega; zaroorat par terminal mein diya gaya local URL khol lein.
- **Samples** se 4 example stories mein se koi chunain. **Story** tab mein title, kahani, kirdar aur duration badlein.
- **Direction** tab mein har scene ka camera angle, action, narration, dialogue, sound notes aur seconds set karein. **＋ Add scene** se shot barhayein.
- **Sound & voice** tab mein apni voice recording, music aur sound effects upload karein. **Assets** tab mein apni reference image dalein. Sirf apna ya ijazat wala media istemal karein.
- **Save frame** PNG tasveer banata hai. **Export project JSON** tamam story, shots aur upload kiye hue media ko aik editable project file mein pack karta hai. **Export video** browser support ke mutabiq WebM banata hai.
- Kaam ke darmiyan JSON export karke backup rakhein. Browser ki local autosave story text/settings ke liye hai; media ko backup karne ke liye JSON zaroor export karein.

## Make a new story

1. Choose one of the four sample projects, or click **New project** and confirm.
2. **Story** tab: set the title, genre, audience, target length, logline, complete story and character descriptions.
3. **Direction** tab: adjust each shot's location, seconds, action, exact narration/dialogue, camera and transition. Add, remove, or reorder shots with the up/down controls in Direction (scene cards run in story order).
4. **Sound & voice** tab: upload your own narration, music, and sound effects. Select an SFX scene and start time. A local operating-system speech voice can be previewed if installed, but the preview is not a generated voice recording.
5. **Assets** tab: optionally add original/authorised reference artwork. In the direction preview, choose whether to show it in-scene.
6. Play or scrub the timeline, inspect each shot, and review the script, timing, camera continuity, rights and audio.
7. Export editable **project JSON** first. Export a **WebM video** and selected **PNG frames**. Open the WebM in a player/editor to review and make any final edits.

## What the app can and cannot do

- The preview draws an original procedural 2D storyboard animation locally and responds to story, camera, timing, palette and project settings. It is a lightweight offline story/animatic tool, not a full hand-drawn animation suite, image generator, voice cloning tool, or professional nonlinear editor.
- Four sample JSON stories include multi-shot story, camera, narration/dialogue, ambience/music/effects cues, characters and timing. Samples contain no licensed voice/music or stock footage; add your own recordings/artwork.
- Project JSON embeds uploads so the project is portable; use the provided 15 MB per-media and 35 MB per-project limits. Browser autosave does not store uploaded media.
- WebM and audio recording depend on browser support. Use a current desktop browser, allow audio playback, and test a short export first. The browser's installed speech voice is not guaranteed offline and is only a preview; upload a voice recording for predictable narration. SFX upload/start offsets are included in the video. Verify mix/sync and listen before release.
- The app deliberately makes no internet requests. Once files are installed, Python and the browser are the only runtime requirements. Browser documentation/installation downloads would of course require internet beforehand.

## Project and sample files

- [Studio interface layout preview (PNG)](docs/screenshots/ali-animation-interface-preview.png) — a static UI reference, not a captured browser screenshot; use the live local app for real controls and animations.
- Blank fill-in template: use **Download blank story template** in the Studio.
- Full schema guide: [`studio/story-format.md`](studio/story-format.md).
- Four sample projects: [`studio/samples/`](studio/samples/).
- Studio UI: [`studio/index.html`](studio/index.html).
- Run offline tests: from the repository root, run `node --test studio/test-*.mjs`.

## Troubleshooting

- **Sample list doesn't load:** use the local server command above (not a `file://` URL); confirm the server is running from the `studio` folder.
- **No voice in preview:** speech voices are provided by the operating system/browser. Upload a recording instead.
- **Video export unavailable:** update to a browser supporting Canvas `captureStream` and `MediaRecorder`. The editable JSON and PNG frame export remain available.
- **No place to import a previous story:** use the **Import project** control and select the exported `.ali-animation.json` file.
- **Need more frequent autosave:** click **Export project JSON** and keep backups outside the repository.
