# Runtime dependencies

This source bundle is portable. It contains no node_modules symlinks, credentials, narration recordings, generated film assets or machine-specific browser paths.

- Node.js 20+ and npm; tested dependency versions are locked in package-lock.json. Run npm ci in the copied project. Network/package access is required on a fresh computer.
- Python 3.9+ for bundled setup, audio synthesis and review helpers. Synthesis uses only the standard library.
- Chrome for user playback. Remotion uses its compatible render browser, downloaded on first use when needed; `npx remotion browser ensure` prepares it. An existing compatible browser can be selected with the installed CLI's --browser-executable option. Avoid hardcoded paths.
- FFmpeg and ffprobe on PATH for the review helper. These are media tools, not Python packages.
- Narration is optional: use a supplied recording, Voicebox with an approved cached local model, or ElevenLabs. ElevenLabs credentials and model/voice access are needed only when that provider is chosen. Use the installed connector, or the bundled Python fallback. No credential is shipped.
- Image generation is supplied by the host's image tool, not a locally bundled model. Supplied images, SVG and Canvas remain supported when that tool is unavailable.

The original starter code is supplied with this skill. Installed npm packages, fonts, assets and services retain their own licenses. Remotion usage remains governed by its own terms: https://www.remotion.dev/license . Do not describe the dependency as unrestricted MIT code merely because an adjacent helper has an MIT license.

The pinned 4.0.516 version is the version used in the reviewed local films, not a claim that it is newest. Upgrade all @remotion packages and remotion together in a new project, regenerate the lockfile, and test preview/render before adopting new APIs.

Detect first and ask before installing missing third-party software/packages or downloading models/browser binaries. Compatible tools are reused. Refer to the installed Sumi setup/narration guides. Setup never authorizes paid test media.
