# ALI Animation — start here

## Model-free Studio (recommended)

ALI Animation Studio is the offline story-animation app. It does not need an AI model, account, API key, package install, or internet connection after the files are downloaded.

From the project root, run:

- **Windows:** `py -3 install.py` (or `python install.py` if your virtual environment is active)
- **macOS/Linux:** `python3 install.py`

The launcher starts a loopback-only local server and opens the Studio in your browser. Leave the terminal open while using it; press **Ctrl+C** to stop it. If needed, open the URL printed in the terminal. See [INSTALL.md](INSTALL.md) and the [standalone HTML guide](ALI-Animation-Guide.html) for UI instructions and file explanations.

## Optional legacy assistant skills

The separate `skills/` directory contains an older assistant-driven production toolkit. You do not need it for the offline Studio, and it is not a model-free workflow. Only install it if you use a compatible assistant host and specifically want those integrations. In that case, `install.py --skills-root PATH` installs the optional skills into that host's documented skills folder; choose the path for your host rather than guessing.
