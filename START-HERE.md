# ALI Animation — start here

## Model-free, manual Studio

This is a manual story/animatic workflow: **you** provide the script, characters, scene actions, camera angles, timing, and any voice/music/art. The Studio does not ask an AI to create or complete these items. It runs locally without a model, account, API key, package install, or internet connection after download.

- **Windows, first run:** double-click `install.bat`. It checks that Python and the project files are present, then launches the Studio. Next time, double-click `start.bat`.
- **Windows terminal alternative:** from the project root run `python install.py` (or `py -3 install.py`).
- **macOS/Linux:** from the project root run `python3 install.py`.

The launcher opens the Studio in your browser and serves it only on your computer. Leave its window open while using the app; press **Ctrl+C** to stop it. If needed, visit the local URL printed in that window. See [INSTALL.md](INSTALL.md) and the [standalone HTML guide](ALI-Animation-Guide.html) for the steps to write a story, set shot angles, import your own media, preview, and export.

## Optional legacy assistant skills

The separate `skills/` directory contains an older assistant-driven production toolkit. You do not need it for the offline Studio, and it is not a model-free workflow. Only install it if you use a compatible assistant host and specifically want those integrations. In that case, `install.py --skills-root PATH` installs the optional skills into that host's documented skills folder; choose the path for your host rather than guessing.
