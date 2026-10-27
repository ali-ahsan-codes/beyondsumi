# ALI Animation — install and use offline

For the standalone, illustrated HTML walkthrough, open [ALI-Animation-Guide.html](ALI-Animation-Guide.html).

**ALI Animation Studio** is a local browser-based animation/storyboard app. It has no AI, account, API key, npm package, Python package, or network dependency. Browser preview, project JSON and supported WebM recording happen on your own computer. The older `skills/` assistant workflow in this repository is a separate legacy toolkit; you do not need it for ALI Animation Studio.

## Quick install

1. Download/extract this repository, or copy the `studio` folder onto the computer you will use. After the files are on disk, disconnecting from the internet is fine.
2. Install Python 3.8+ if you do not already have it. Python is used only as a tiny local file server; the animation app itself has no Python packages.
3. Open a terminal/Command Prompt in the repository's `studio` folder and run:

   **Windows**
   ```powershell
   py -m http.server 8765 --bind 127.0.0.1
   ```

   **macOS / Linux**
   ```sh
   python3 -m http.server 8765 --bind 127.0.0.1
   ```

4. Open **http://127.0.0.1:8765** in a current Firefox, Chrome, or Edge browser. Keep the terminal open while using the app. Stop it with **Ctrl+C**.

If `py` is not recognised on Windows, try `python -m http.server 8765 --bind 127.0.0.1`. If port 8765 is occupied, use another number (for example 8766) in both the command and the URL. Do not expose this local server to a public network; the loopback binding keeps it on your computer.

## Roman Urdu — istemal ka tareeqa

- `studio` folder mein terminal khol kar upar wala command chalayein. Browser mein `http://127.0.0.1:8765` khol lein.
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
