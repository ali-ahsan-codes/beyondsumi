#!/usr/bin/env python3
"""Explicit, one-time ElevenLabs acquisition. The offline renderer never calls this.

Credentials remain in environment/Keychain. Every attempt has an exclusive
receipt before the request, so interruptions cannot silently repeat a charge.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.request


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    temp.replace(path)


def read_key():
    key = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    if not key and sys.platform == 'darwin':
        r = subprocess.run(['/usr/bin/security', 'find-generic-password', '-s',
                            'com.codex.personal.elevenlabs-voice', '-a',
                            'elevenlabs-api-key', '-w'], capture_output=True, text=True, timeout=30)
        key = r.stdout.strip() if r.returncode == 0 else ''
    if not key:
        raise ValueError('No existing ElevenLabs credential. Use secure setup; never paste keys in chat.')
    return key


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def batch(catalog_path, approval_path, out, only=None):
    catalog = json.loads(catalog_path.read_text())
    approval = json.loads(approval_path.read_text())
    if approval.get('approved') is not True or approval.get('catalog_sha256') != sha(catalog_path):
        raise ValueError('An explicit approval bound to this exact catalog is required.')
    if not approval.get('output_root') or Path(approval['output_root']).resolve() != out.resolve():
        raise ValueError('Approval must bind the acquisition output directory; do not duplicate a paid batch into a new folder.')
    entries = catalog['sfx']
    if approval.get('count') != len(entries) or approval.get('total_seconds') != sum(e['duration_seconds'] for e in entries):
        raise ValueError('Approval count/duration does not match.')
    estimate = sum(e['duration_seconds'] for e in entries) * catalog['provider']['price_usd_per_minute'] / 60
    if not 0 < estimate <= approval['max_estimated_base_usd']:
        raise ValueError('Published-price estimate exceeds the approved limit.')
    if len({e['id'] for e in entries}) != len(entries):
        raise ValueError('Duplicate effect ID.')
    for e in entries:
        if not re.fullmatch(r'[a-z0-9-]{1,64}', e['id']) or not .5 <= e['duration_seconds'] <= 30:
            raise ValueError('Invalid effect ID/duration.')
    if only:
        if not set(only) <= {e['id'] for e in entries}:
            raise ValueError('Unknown selected effect.')
        entries = [e for e in entries if e['id'] in only]
    out.mkdir(parents=True, exist_ok=True)
    receipts = out / 'receipts'; receipts.mkdir(exist_ok=True)
    raw_dir = out / 'originals'; raw_dir.mkdir(exist_ok=True)
    key = None
    done = []
    for entry in entries:
        receipt = receipts / (entry['id'] + '.json')
        raw = raw_dir / (entry['id'] + '.mp3')
        payload = {'text': entry['prompt'], 'duration_seconds': entry['duration_seconds'],
                   'loop': entry['loop'], 'model_id': catalog['provider']['model_id'],
                   'prompt_influence': catalog['provider']['prompt_influence']}
        payload_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if receipt.exists():
            prior = json.loads(receipt.read_text())
            if prior.get('status') == 'complete' and prior.get('payload_sha256') == payload_hash and raw.is_file() and sha(raw) == prior.get('audio_sha256'):
                done.append({'id':entry['id'],'status':'reused'}); continue
            raise ValueError('Existing failed, uncertain or changed attempt for ' + entry['id'] + '. Inspect the receipt; no automatic retry.')
        if raw.exists():
            raise ValueError('Unreceipted audio exists; preserve and inspect it before generation.')
        key = key or read_key()
        record = {'id':entry['id'],'status':'outcome_unknown', 'started_at':datetime.now(timezone.utc).isoformat(),
                  'payload':payload, 'payload_sha256':payload_hash, 'catalog_sha256':sha(catalog_path),
                  'estimated_base_usd':entry['duration_seconds'] * catalog['provider']['price_usd_per_minute'] / 60,
                  'review':'pending', 'automatic_retry':False}
        with receipt.open('x') as f:
            json.dump(record, f, indent=2)
        url = 'https://api.elevenlabs.io/v1/sound-generation?output_format=' + catalog['provider']['output_format']
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST',
                                     headers={'xi-api-key':key,'Content-Type':'application/json','Accept':'audio/mpeg',
                                              'User-Agent':'Sumi-Sound-Library/4.7.0'})
        try:
            with urllib.request.build_opener(NoRedirect()).open(req, timeout=180) as response:
                audio = response.read(16 * 1024 * 1024 + 1)
                record['request_id'] = response.headers.get('request-id') or response.headers.get('x-request-id')
                record['provider_billed_credits'] = response.headers.get('character-cost')
                if len(audio) > 16 * 1024 * 1024 or not audio:
                    raise ValueError('Empty or oversized provider response; inspect receipt, do not repeat.')
            with raw.open('xb') as f:
                f.write(audio)
            record.update(status='complete', audio_sha256=sha(raw), bytes=len(audio), audio_path=str(raw.resolve()))
            save(receipt, record)
            done.append({'id':entry['id'],'status':'complete','bytes':len(audio),'provider_billed_credits':record['provider_billed_credits']})
            print(json.dumps(done[-1]), flush=True)
        except urllib.error.HTTPError as error:
            record.update(status='rejected' if error.code < 500 else 'outcome_unknown', http_status=error.code)
            # No raw server body: it could include private account data.
            save(receipt, record)
            raise ValueError('Provider HTTP ' + str(error.code) + '; stopped without retry. Inspect account scopes/receipt.') from None
        except (urllib.error.URLError, TimeoutError, socket.timeout, OSError, ValueError):
            save(receipt, record)
            raise ValueError('Generation outcome may be unknown. Inspect saved files and receipt; no automatic retry.') from None
    return {'selected':len(entries),'results':done,'published_price_batch_estimate_usd':estimate,
            'actual_dollar_invoice_verified':False,'music_provider_calls':0}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalog',type=Path,default=Path(__file__).with_name('catalog.json'))
    p.add_argument('--approval',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--only',nargs='+')
    a=p.parse_args()
    try:
        print(json.dumps(batch(a.catalog,a.approval,a.out,a.only),indent=2))
    except (ValueError,KeyError,OSError) as e:
        p.error(str(e))

if __name__ == '__main__':
    main()
