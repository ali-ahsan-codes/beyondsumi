#!/usr/bin/env python3
"""Install only the authored Sumi skill, preserving previous versions. No third-party installs."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid
from sumi_memory import default_dir, read, write, now, VERSION

WELCOME = (Path(__file__).resolve().parents[1]/'assets/WELCOME.txt').read_text()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    base=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills'/'sumi'
    p.add_argument('--destination',type=Path,default=base)
    p.add_argument('--replace',action='store_true',help='Replace an existing Sumi installation after backing it up.')
    p.add_argument('--state-dir',type=Path,default=default_dir())
    a=p.parse_args();source=Path(__file__).resolve().parents[1];target=a.destination.expanduser().absolute()
    if not (source/'SKILL.md').is_file():p.error('Incomplete Sumi source.')
    if target.is_symlink():p.error('Destination is a symlink; choose its actual intended skill location.')
    if source==target or source in target.parents or target in source.parents:p.error('Source and destination must be separate folders.')
    if target.exists() and not a.replace:p.error('Sumi already exists. Use --replace to retain a backup and update it.')
    target.parent.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.sumi-install-',dir=target.parent));backup=None
    try:
        shutil.copytree(source,stage/'sumi',ignore=shutil.ignore_patterns('__pycache__','*.pyc','node_modules','.DS_Store'))
        if target.exists():
            # Backups stay outside the discovered skills directory to avoid duplicate skills.
            backups=target.parent.parent/'sumi-skill-backups';backups.mkdir(exist_ok=True)
            backup=backups/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8])
            target.rename(backup)
        try: (stage/'sumi').rename(target)
        except OSError:
            if backup and not target.exists():backup.rename(target)
            raise
    finally:shutil.rmtree(stage,ignore_errors=True)
    print(WELCOME)
    print(f'![Three Japanese Sumi styles]({target / "assets/style-atlas-three.svg"})')
    print(f'Installed: {target}\nPrevious version: {backup or "none"}')
    print(f'Next: ask your assistant to use $sumi; it will show first-use guidance and run {target / "scripts/sumi_setup.py"} doctor.')
    path=a.state_dir.expanduser().resolve()/'user.json'
    try:
        data=read(path);data['onboarding']['installation']={'shown_at':now(),'version':VERSION};write(path,data)
    except (OSError,ValueError) as e:print(f'Skill installed, but setup memory was not updated: {e}',file=sys.stderr)
    from sumi_setup import doctor
    print(json.dumps({'requirements':doctor(),'image_check':'Host agent must inspect image/MCP tools; no image test or installation ran.'},indent=2))
    print('No third-party packages, voice models or paid media were installed/generated.')

if __name__=='__main__':main()
