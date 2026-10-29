# ALI Animation — install and use offline

For the standalone, illustrated HTML walkthrough, open [ALI-Animation-Guide.html](ALI-Animation-Guide.html).

**ALI Animation Studio** is a local browser-based animation/storyboard app. It has no AI, account, API key, npm package, Python package, or network dependency. Browser preview, project JSON and supported WebM recording happen on your own computer. The older `skills/` assistant workflow in this repository is a separate legacy toolkit; you do not need it for ALI Animation Studio.

## First run and launch — no AI model required

1. Download/extract the complete project folder. Once the files and Python are on your computer, the Studio can be used without internet.
2. Have Python 3.8+ installed. Python's standard library is all that is used; there are no packages or models to install.
3. **Windows:** double-click `install.bat` for a first-run Python/project check and to launch the Studio. For later sessions, double-click `start.bat`. If you prefer the terminal, open PowerShell in the project root (the folder containing `install.py`) and run `python install.py` or `py -3 install.py`.
4. **macOS / Linux:** from the project root run `python3 install.py`.
5. The local-only server opens the Studio in your browser. If it does not open automatically, visit the URL printed by the launcher (normally **http://127.0.0.1:8765**). Keep the launcher window open while using the app; press **Ctrl+C** there to stop it.

`install.bat` is a lightweight check-and-launch helper: it does not install software, download anything, or change Windows settings. `start.bat` starts the Studio directly. Both use only Python's standard library and talk to the loopback server on your own computer. If port 8765 is busy, the launcher chooses another available local port and prints its URL. `--skills-root` is separate optional legacy assistant tooling; it is not needed for the Studio.

## Roman Urdu — istemal ka tareeqa

- Windows par pehli dafa `install.bat` double-click karein; aglay martaba `start.bat` chalayein. macOS/Linux par project root mein terminal khol kar `python3 install.py` chalayein. Browser khul jayega; zaroorat par terminal mein diya gaya local URL khol lein.
- **Samples** se 4 example stories mein se koi chunain. **Story** tab mein title, kahani, kirdar aur duration badlein.
- **Direction** tab mein har scene ka action, narration, dialogue, sound notes aur seconds set karein; camera angle ke suggestions chunain ya apna angle khud type karein. **＋ Add scene** se shot barhayein.
- **Sound & voice** tab mein apni voice recording, music aur sound effects upload karein. **Assets** tab mein apni reference image dalein. Sirf apna ya ijazat wala media istemal karein.
- **Save frame** PNG tasveer banata hai. **Export project JSON** tamam story, shots aur upload kiye hue media ko aik editable project file mein pack karta hai. **Export video** browser support ke mutabiq WebM banata hai.
- Kaam ke darmiyan JSON export karke backup rakhein. Browser ki local autosave story text/settings ke liye hai; media ko backup karne ke liye JSON zaroor export karein.

## Make a new story

1. Choose one of the four sample projects, or click **New project** and confirm.
2. **Story** tab: set the title, genre, audience, target length, logline, complete story and character descriptions.
3. **Direction** tab: adjust each shot's location, seconds, action, exact narration/dialogue, transition, and camera angle. Choose a suggestion or type your own angle/framing text. Add, remove, or reorder shots with the up/down controls (scene cards run in story order).
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

- **Sample list doesn't load:** start with `install.bat`/`start.bat` on Windows or `python3 install.py` on macOS/Linux from the project root (the folder containing `install.py`). Do not open `studio/index.html` as a `file://` URL.
- **No voice in preview:** speech voices are provided by the operating system/browser. Upload a recording instead.
- **Video export unavailable:** update to a browser supporting Canvas `captureStream` and `MediaRecorder`. The editable JSON and PNG frame export remain available.
- **No place to import a previous story:** use the **Import project** control and select the exported `.ali-animation.json` file.
- **Need more frequent autosave:** click **Export project JSON** and keep backups outside the repository.
