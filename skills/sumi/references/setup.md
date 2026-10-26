# Setup without surprises

Run `python3 /absolute/path/to/sumi/scripts/sumi_setup.py doctor` before installing. It reports OS/architecture, RAM where detectable, free disk space, Python, Node/npm, FFmpeg/ffprobe, Chrome, Voicebox and optional project dependencies. It does not install, launch apps, read API keys, generate media or contact external services. `--voicebox` additionally checks only the local Voicebox server. `--project /path/to/film` checks that project's packages. If the host has a bundled runtime, inspect its documented dependency tool before assuming a missing PATH command means the tool is unavailable.

Show a short table with tool, purpose, detected status, cost and action. Even when a tool exists, explain once what it does and whether it is free. Do not install a second copy merely because it is outside PATH; add an explicit command path for this project or use the working environment. A version/path check establishes availability, not successful rendering.

| Component | Purpose and cost | Install only if needed |
|---|---|---|
| Python 3.9+ | Runs Sumi setup, review and bundled background synthesis. Free; sound generator uses only the standard library. | Official [Python](https://www.python.org/downloads/) for the OS, or an existing trusted package manager. No pip audio stack needed. |
| Node.js 20+ and npm | Runs the bundled animation editor/render engine. Free. Prefer a currently supported LTS satisfying the lockfile. | [Node.js](https://nodejs.org/en/download); reuse compatible existing runtime. |
| Remotion, React, TypeScript | Assistant-authored animation, local Studio preview and export. Packages are locked in the starter. Remotion is free for eligible individuals, nonprofits and small companies; company licensing can apply. | Project-local `npm ci` after approval. Do not install globally or call Remotion unrestricted MIT. Check [the license](https://www.remotion.dev/license) for the actual use. |
| Chrome / render browser | Chrome is free for preview/playback. Remotion uses a compatible browser to export frames. | Reuse installed Chrome where compatible; otherwise disclose and approve a render-browser download. Test a still before claiming compatibility. |
| FFmpeg and ffprobe | Media conversion, audio mixing, duration/stream and loudness checks. Free software; build/codec licenses apply. | [Official FFmpeg download guidance](https://ffmpeg.org/download.html), or an existing trusted package manager. |
| Voicebox | Optional free local narration app. Model weights have their own terms; hardware and electricity still cost resources. | Only after the user selects it and approves the app/selected model. See [narration.md](narration.md). |
| ElevenLabs | Optional hosted narration with account allowance/usage charges; no local speech model download. | Reuse the connector or bundled helper. Secure API setup only if selected and not already connected. |
| Host image tool / supplied art | Still artwork. Host generation may use paid credits. Original SVG/Canvas or supplied artwork can avoid that charge. | No image model is silently installed. Choose and disclose the route in the film plan. |

Remotion Studio is a local preview, frame-navigation and rendering editor whose scene code the assistant edits. It is not a full drag-and-drop video editor. A beginner can request changes in ordinary language. Preserve a requested existing editor. For manual waveform work, a free editor such as Audacity is optional, not required for Python sound; detect it and ask before installing. Do not install unrelated creative apps “just in case.”

The [sound-library composer/mixer](sound-library.md) also uses Python standard library; FFmpeg prepares imported audio. Acquired effects are cached outside the skill. No sounddevice, PortAudio, AudioCraft or model is required for this route. Ordinary library reuse never triggers another paid generation or package installation.

## Concrete approval and installation

Example: “Python and Chrome are ready. This film still needs Node/npm, FFmpeg, and its locked animation packages. The first two are free; Remotion is free for eligible individual use. I will install these from the listed official sources and put project packages in this film folder. May I install those missing components?” For an organization, resolve applicable Remotion eligibility before presenting it as free.

After consent, use the platform's official installer or an existing package manager. Examples to adapt after checking the actual machine: Homebrew `brew install node ffmpeg` on macOS; winget official Node/Python/FFmpeg package entries on Windows; supported distribution packages on Linux (verify Node version). Do not install a package manager itself, add repositories, use sudo or run downloaded shell scripts without explaining that additional change and obtaining the required approval. Don't disable Gatekeeper, antivirus or browser security to install Voicebox. Let the user complete OS authentication where needed.

For the film's pinned packages, preview and then execute the bundled installer:

```sh
python3 /absolute/path/to/sumi/scripts/sumi_setup.py install-project /absolute/path/to/film
# Only after the user approves the displayed package installation:
python3 /absolute/path/to/sumi/scripts/sumi_setup.py install-project /absolute/path/to/film --approved
```

It reuses an already matching installation; otherwise runs `npm ci` from that project's lockfile. npm installs third-party code and can run package lifecycle scripts, so the preview is not consent. For a compatible render browser download, disclose the network/storage change first, then use the installed project's Remotion CLI (`npx --no-install remotion browser ensure`). Do not allow npx to fetch a different Remotion version. An explicit compatible existing Chrome path may avoid a download; record it locally rather than baking the machine path into the reusable skill.

Re-run doctor, typecheck and a small technical still/preview after approved setup. No full film or paid narration is needed to prove installation. Report exactly what was verified. Network errors, locked files or an incompatible version are recoverable setup states; keep the story and source work intact, explain the next fix and do not loop installers.

## Offline and upgrade behavior

Planning, memory and Python synthesis work offline once Python and the skill are present. Rendering needs installed packages/browser. Voicebox needs the selected cached model and a running local backend. ElevenLabs and host image generation need their services. Do not promise that an installed skill makes cloud narration work offline.

Keep existing lockfiles; update all Remotion packages together only when needed and approved. Do not bulk-upgrade the user's machine. Changing Sumi's authored instructions is separate from installing third-party packages. Check dependency download size from the actual installer/package manager when available; label unknown sizes instead of inventing a universal bundle size.
