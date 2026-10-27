#!/usr/bin/env python3
"""Launch the local, model-free ALI Animation Studio.

With no arguments this serves the Studio on loopback and opens it in a browser.
The optional --skills-root mode is only for installing the separate legacy
assistant skill suite; the Studio itself does not use an AI model.
"""
import argparse
import functools
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

NAMES = ['sumi', 'sumi-svg', 'sumi-voicebox', 'sumi-elevenlabs']


def install(source, root, replace=False, names=None):
    """Install selected optional legacy skills into an explicit host folder."""
    names = names or NAMES
    source = source.resolve()
    root = root.expanduser().absolute()
    if root.is_symlink():
        raise ValueError('Choose the intended real skills folder, not a symlink')
    root = root.resolve()
    if source == root or source in root.parents or root in source.parents:
        raise ValueError('Installation must be outside this source suite')
    for name in names:
        if name not in NAMES or not (source / 'skills' / name / 'SKILL.md').is_file():
            raise ValueError('Incomplete requested skill: ' + name)
        if (root / name).is_symlink():
            raise ValueError('Refuse symlink skill destination')
        if (root / name).exists() and not replace:
            raise ValueError('Existing skill preserved; use --replace for a backed-up update')

    root.mkdir(parents=True, exist_ok=True)
    backup = root.parent / 'sumi-suite-backups' / (
        datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    )
    staged = Path(tempfile.mkdtemp(prefix='.sumi-suite-', dir=root.parent))
    moved = []
    installed = []
    try:
        for name in names:
            shutil.copytree(
                source / 'skills' / name,
                staged / name,
                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'node_modules', '.DS_Store'),
            )
        for name in names:
            target = root / name
            if target.exists():
                backup.mkdir(parents=True, exist_ok=True)
                target.rename(backup / name)
                moved.append(name)
            (staged / name).rename(target)
            installed.append(name)
    except Exception:
        for name in reversed(installed):
            shutil.rmtree(root / name)
        for name in reversed(moved):
            (backup / name).rename(root / name)
        raise
    finally:
        shutil.rmtree(staged, ignore_errors=True)

    return {
        'installed': [str(root / name) for name in names],
        'backup': str(backup) if moved else None,
        'third_party_software_installed': False,
        'model_downloads': 0,
        'paid_calls': 0,
    }


def launch_studio(source, port=8765, open_browser=True):
    """Serve the Studio locally; no Python packages, AI model, or network access required."""
    studio_dir = (source / 'studio').resolve()
    if not (studio_dir / 'index.html').is_file():
        raise ValueError(f'Studio files were not found at {studio_dir}')

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(studio_dir))
    try:
        server = http.server.ThreadingHTTPServer(('127.0.0.1', port), handler)
    except OSError as exc:
        # If the usual port is taken, ask the OS for an available local port.
        if port != 8765:
            raise ValueError(f'Could not start the local server on port {port}: {exc}') from exc
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        print('Port 8765 was busy; using an available local port instead.')

    url = f'http://127.0.0.1:{server.server_port}/'
    print('ALI Animation Studio is ready — it runs locally and does not use an AI model.')
    print(f'Open {url} in your browser. Press Ctrl+C here to stop the local server.')
    if open_browser:
        try:
            webbrowser.open(url, new=2)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nALI Animation Studio server stopped.')
    finally:
        server.server_close()


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            'ALI Animation Studio is the default offline, model-free mode. '
            'Use --skills-root only to install the separate optional legacy assistant skills.'
        )
    )
    parser.add_argument(
        '--skills-root',
        type=Path,
        help='Optional host skills folder for legacy assistant integrations; not needed for the Studio.',
    )
    parser.add_argument('--replace', action='store_true', help='Back up and replace existing legacy skills.')
    parser.add_argument('--state-dir', type=Path, help='Optional state folder for the legacy skill first-run check.')
    parser.add_argument('--only', nargs='+', choices=NAMES, help='Install only selected legacy skills.')
    parser.add_argument('--port', type=int, default=8765, help='Local Studio server port (default: 8765).')
    parser.add_argument('--no-browser', action='store_true', help='Do not open a browser automatically in Studio mode.')
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    source = Path(__file__).resolve().parent

    if args.skills_root is None:
        if args.replace or args.state_dir or args.only:
            parser.error('--replace, --state-dir, and --only require --skills-root; none are needed for the Studio.')
        if not 0 <= args.port <= 65535:
            parser.error('--port must be between 0 and 65535.')
        try:
            launch_studio(source, args.port, open_browser=not args.no_browser)
        except (ValueError, OSError) as exc:
            parser.exit(1, f'Could not launch ALI Animation Studio: {exc}\n')
        return

    try:
        result = install(source, args.skills_root, args.replace, args.only)
    except (ValueError, OSError) as exc:
        parser.exit(1, f'Installation stopped: {exc}\n')

    print(json.dumps(result, indent=2))
    main_skill = args.skills_root.expanduser() / 'sumi'
    if main_skill.is_dir():
        print((main_skill / 'assets/WELCOME.txt').read_text())
        print('Read-only requirements check:')
        state_args = ['--state-dir', str(args.state_dir)] if args.state_dir else []
        marker = subprocess.run(
            [sys.executable, str(main_skill / 'scripts/sumi_memory.py'), *state_args, 'mark', 'installation'],
            capture_output=True,
            text=True,
        )
        if marker.returncode:
            print('Installed source; setup memory marker was not changed: ' + marker.stderr.strip(), file=sys.stderr)
        subprocess.run(
            [sys.executable, str(main_skill / 'scripts/first_run.py'), *state_args],
            check=True,
        )
    else:
        print('Companion installed. Ask your agent to read its SKILL.md; no app/model was installed.')
    print('Ask your agent to display the welcome in chat and check its image tools. A silent ZIP import cannot display chat by itself.')


if __name__ == '__main__':
    main()
