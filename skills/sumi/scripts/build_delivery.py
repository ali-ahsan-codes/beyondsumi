#!/usr/bin/env python3
"""Package existing MP4 exports in the Beyondsumi local delivery dashboard.

No rendering, transcoding, upload, dependency installation or review approval.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

from sumi_catalog import STYLES as STYLE_DATA

STYLES = {item['name'] for item in STYLE_DATA.values()}


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def probe(path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                             '-of', 'json', str(path)], check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    videos = [s for s in data['streams'] if s['codec_type'] == 'video' and not s.get('disposition', {}).get('attached_pic')]
    if not videos:
        raise ValueError('No video stream: ' + str(path))
    video = videos[0]
    audio = [s for s in data['streams'] if s['codec_type'] == 'audio']
    if path.suffix.lower() != '.mp4' or video['codec_name'] != 'h264' or video.get('pix_fmt') not in {'yuv420p', 'yuvj420p'}:
        raise ValueError('Delivery needs an existing H.264 / 8-bit 4:2:0 MP4: ' + str(path))
    if any(s['codec_name'] != 'aac' for s in audio):
        raise ValueError('Delivery MP4 audio must be AAC (or absent for intentional silence)')
    return {'width': video['width'], 'height': video['height'],
            'fps': float(Fraction(video['avg_frame_rate'])),
            'duration': float(video.get('duration') or data['format']['duration']),
            'container_duration': float(data['format']['duration']), 'bytes': path.stat().st_size,
            'audio': bool(audio), 'sha256': sha(path)}


def build(manifest, destination):
    manifest = manifest.resolve()
    config = json.loads(manifest.read_text())
    if destination.exists():
        raise ValueError('Destination already exists; choose a new revision')
    if not config.get('title') or not isinstance(config.get('films'), list) or not config['films']:
        raise ValueError('A title and at least one film are required')
    template = Path(__file__).resolve().parents[1] / 'assets/delivery-dashboard'
    if not shutil.which('ffprobe'):
        raise ValueError('ffprobe is required to inspect actual files. Detect/explain it before requesting installation.')
    films = []
    for i, item in enumerate(config['films']):
        style = item.get('style')
        if style not in STYLES:
            raise ValueError('Choose Sumi Original, Sumi Light or Sumi Dark')
        status = item.get('status', 'draft')
        if status not in {'draft', 'ready'} or not item.get('review_note'):
            raise ValueError('Each film needs draft/ready status and an honest review note')
        source = (manifest.parent / item['source']).resolve()
        metadata = probe(source)
        evidence = None
        if status == 'ready':
            if not item.get('review_file') or item.get('reviewed_sha256') != metadata['sha256']:
                raise ValueError('Ready delivery needs review_file and reviewed_sha256 matching this export')
            evidence = (manifest.parent / item['review_file']).resolve()
            if not evidence.is_file():
                raise ValueError('The recorded review file does not exist')
        poster = (manifest.parent / item['poster']).resolve() if item.get('poster') else None
        if poster and (not poster.is_file() or poster.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}):
            raise ValueError('Poster must be an existing JPG, PNG or WebP')
        if not poster and not shutil.which('ffmpeg'):
            raise ValueError('Provide a poster or use the existing ffmpeg installation to extract one')
        name = f'{i+1:02d}-' + re.sub('[^a-z0-9]+', '-', style.lower()).strip('-')
        film = dict(metadata, style=style, description=item.get('description', ''),
                    status=status, review_note=item['review_note'], file=f'media/{name}.mp4',
                    download_name=f'{name}.mp4', poster=f'media/{name}{poster.suffix.lower() if poster else ".jpg"}')
        films.append((film, source, poster, evidence))
    # Validate all inputs before making a destination. Existing exports remain untouched.
    shutil.copytree(template, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'proof.html', 'proof.css', 'proof-player.js'))
    (destination / 'media').mkdir()
    for film, source, poster, evidence in films:
        target = destination / film['file']
        shutil.copy2(source, target)
        assert sha(target) == film['sha256']
        if poster:
            shutil.copy2(poster, destination / film['poster'])
        else:
            subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(min(2, film['duration'] / 2)),
                            '-i', str(source), '-frames:v', '1', '-q:v', '3',
                            str(destination / film['poster'])], check=True)
        if evidence:
            film['review_evidence_sha256'] = sha(evidence)
    data = {'catalogue': [{'name': item['name'], 'description': item['short_description']} for item in STYLE_DATA.values()], 'brand': 'Beyondsumi', 'title': config['title'], 'subtitle': config.get('subtitle', ''),
            'recreation_context': config.get('recreation_context', ''),
            'films': [f[0] for f in films]}
    raw = json.dumps(data, ensure_ascii=True, indent=2)
    (destination / 'data.js').write_text('window.SUMI_DELIVERY = ' + raw.replace('<', '\\u003c') + ';\n')
    (destination / 'DELIVERY.json').write_text(raw + '\n')
    print(f'Beyondsumi delivery: {destination.resolve()}')
    print(f'Run: python3 "{destination.resolve() / "serve.py"}" --port 4260')
    print('Open http://127.0.0.1:4260/ on this computer. This is not a hosted/shareable URL.')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        build(args.manifest, args.destination)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')
