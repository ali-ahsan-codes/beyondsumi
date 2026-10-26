#!/usr/bin/env python3
"""Portable geometry/evidence gate; checks supplied rendered points, not video pixels.

No service, model, ChatGPT connection, or third-party Python package is required.
Run against a project shot-plan.json. Exit 1 blocks final production on failure.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
from plan_provenance import plan_digest

CONTRACT = 'sumi-physics-v1'
KINDS = {'length', 'bend', 'pin', 'grip', 'surface', 'step', 'support'}
FAMILIES = {'length': 'limbs', 'bend': 'joints', 'pin': 'support',
            'surface': 'support', 'support': 'support', 'grip': 'grip', 'step': 'motion'}

def finite(x):
    return isinstance(x, (float, int)) and not isinstance(x, bool) and math.isfinite(x)

def integer(x):
    return isinstance(x, int) and not isinstance(x, bool)

def point(x):
    return isinstance(x, list) and len(x) == 2 and all(finite(v) for v in x)

def text(x):
    return isinstance(x, str) and bool(x.strip())

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def validate(data, root, stage='proof'):
    errors = []
    root = Path(root).resolve()
    def need(ok, msg):
        if not ok: errors.append('Physics: ' + msg)
        return bool(ok)
    def record_file(record, label, as_json=False):
        if not need(isinstance(record, dict) and text(record.get('path')), label + ': file record required'):
            return None
        p = (root / record['path']).resolve()
        if not need(root in p.parents and p.is_file(), label + ': missing/outside-project file'):
            return None
        raw = p.read_bytes()
        if not need(bool(raw) and record.get('sha256') == hashlib.sha256(raw).hexdigest(), label + ': empty/stale file'):
            return None
        if as_json:
            try: return json.loads(raw)
            except (ValueError, UnicodeError): need(False, label + ': invalid JSON'); return None
        return True
    if not isinstance(data, dict): return ['Physics: plan must be an object']
    if not need(data.get('physics_contract') == CONTRACT, 'missing supported physics_contract'):
        return errors
    fps = data.get('output_fps')
    if not need(finite(fps) and fps > 0, 'positive output_fps required'): return errors
    if not need(isinstance(data.get('shots'), list) and data['shots'], 'shots required'): return errors
    digest = plan_digest(data)
    # The digest binds declared hashes; this separate traversal checks real bytes.
    def verify_sources(value):
        if isinstance(value, dict):
            if 'path' in value and 'sha256' in value: record_file(value, str(value.get('path')))
            else:
                for key, item in value.items():
                    if key != 'proof': verify_sources(item)
        elif isinstance(value, list):
            for item in value: verify_sources(item)
    verify_sources(data)
    for shot in data['shots']:
        if not need(isinstance(shot, dict), 'shot must be an object'): continue
        sid = str(shot.get('id', '?'))
        if not need(finite(shot.get('start')) and finite(shot.get('end')) and shot['end'] > shot['start'], sid + ': invalid interval'): continue
        start, end = math.ceil(shot['start'] * fps - 1e-8), math.ceil(shot['end'] * fps - 1e-8)
        uses = shot.get('characters')
        if not need(isinstance(uses, list), sid + ': characters list required'): continue
        ids = {x.get('id') for x in uses if isinstance(x, dict) and text(x.get('id'))}
        if not need(len(ids) == len(uses), sid + ': unique character IDs required'): continue
        spec = shot.get('physics', {})
        if not need(isinstance(spec, dict), sid + ': physics object required'): continue
        actions = spec.get('actions')
        if not need(isinstance(actions, list), sid + ': action inventory required'): continue
        if not ids:
            need(not actions and text(spec.get('character_free_reason')), sid + ': explain character-free shot')
            continue
        coverage = {cid: set() for cid in ids}; seen = set()
        proof = shot.get('proof', {})
        proof = proof if isinstance(proof, dict) else {}
        traces = reviews = None
        if stage == 'proof':
            traces = record_file(proof.get('physics_trace'), sid + ' trace', True)
            reviews = record_file(proof.get('limb_review'), sid + ' visual review', True)
            for label, item in [('trace', traces), ('visual review', reviews)]:
                need(isinstance(item, dict) and item.get('schema') == 1 and item.get('plan_sha256') == digest,
                     sid + ': ' + label + ' missing/stale plan binding')
            if isinstance(traces, dict):
                need(traces.get('coordinates') == 'world-design-pixels' and traces.get('fps') == fps,
                     sid + ': trace must use world-design-pixels and output fps')
        for action in actions:
            if not need(isinstance(action, dict), sid + ': action object required'): continue
            aid, cid = action.get('id'), action.get('character')
            label = sid + '/' + str(aid)
            if not need(text(aid) and aid not in seen and cid in ids, label + ': unique action ID and used character required'): continue
            seen.add(aid)
            a, b = action.get('start_frame'), action.get('end_frame')
            if not need(integer(a) and integer(b) and start <= a < b <= end, label + ': invalid end-exclusive frame interval'): continue
            coverage[cid].update(range(a, b))
            need(text(action.get('kind')) and text(action.get('view')), label + ': action kind/view required')
            checks = action.get('checks'); exemptions = action.get('not_applicable', {})
            if not need(isinstance(checks, list) and isinstance(exemptions, dict), label + ': checks and not_applicable required'): continue
            families = set(); check_ids = set(); valid_checks = []
            for check in checks:
                if not need(isinstance(check, dict), label + ': check object required'): continue
                name, kind = check.get('id'), check.get('kind')
                if not need(text(name) and name not in check_ids and kind in KINDS, label + ': unique check ID/known kind required'): continue
                check_ids.add(name);families.add(FAMILIES[kind])
                lo, hi = check.get('start_frame', a), check.get('end_frame', b)
                count = 3 if kind in {'bend', 'support'} else 1 if kind in {'pin', 'surface', 'step'} else 2
                names = check.get('points')
                ok = need(integer(lo) and integer(hi) and a <= lo < hi <= b, label + '/' + name + ': check interval invalid')
                ok &= need(isinstance(names, list) and len(names) == count and all(text(n) for n in names), label + '/' + name + ': point names invalid')
                need(text(check.get('reason')), label + '/' + name + ': threshold/geometry reason required')
                if kind in {'length', 'surface'}:
                    ok &= need(finite(check.get('min')) and finite(check.get('max')) and check['min'] <= check['max'], label + '/' + name + ': finite min/max required')
                    if kind == 'length': ok &= need(check.get('min', -1) > 0, label + '/' + name + ': positive length required')
                elif kind == 'bend':
                    ok &= need(check.get('sign') in {-1, 1} and not isinstance(check.get('sign'), bool), label + '/' + name + ': bend sign required')
                    ok &= need(finite(check.get('epsilon')) and check['epsilon'] >= 0, label + '/' + name + ': nonnegative cross-product epsilon required')
                else:
                    ok &= need(finite(check.get('max_error')) and check['max_error'] >= 0, label + '/' + name + ': nonnegative max_error required')
                if kind == 'pin': ok &= need(point(check.get('anchor')), label + '/' + name + ': fixed world anchor required')
                if ok: valid_checks.append((check, lo, hi))
            for family in {'limbs', 'joints', 'support', 'grip', 'motion'}:
                need(family in families or text(exemptions.get(family)), label + ': missing ' + family + ' checks or justified exemption')
                need(not (family in families and family in exemptions), label + ': contradictory ' + family + ' exemption')
            need(not (set(exemptions) - {'limbs', 'joints', 'support', 'grip', 'motion'}), label + ': unknown exemption')
            if stage != 'proof': continue
            samples = traces.get('actions', {}).get(aid) if isinstance(traces, dict) and isinstance(traces.get('actions'), dict) else None
            if not need(isinstance(samples, list), label + ': trace samples required'): continue
            frames = {}
            for sample in samples:
                if not need(isinstance(sample, dict) and integer(sample.get('frame')), label + ': bad trace frame'): continue
                f = sample['frame']
                if not need(a <= f < b and f not in frames and isinstance(sample.get('points'), dict), label + ': duplicate/outside/malformed frame'): continue
                if not need(sample.get('character') == cid, label + ': trace character mismatch'): continue
                if not need(sample.get('unresolved') == [], label + ': unresolved renderer constraint (clamp/contact/etc.)'): continue
                if not need(all(point(p) for p in sample['points'].values()), label + ': nonfinite/malformed point'): continue
                frames[f] = sample['points']
            need(set(frames) == set(range(a, b)), label + ': every output frame required; sparse samples are insufficient')
            for check, lo, hi in valid_checks:
                kind, names = check['kind'], check['points']
                for f in range(lo, hi):
                    pts = frames.get(f, {})
                    if not need(all(n in pts for n in names), label + '/' + check['id'] + ': missing point at frame ' + str(f)): break
                    p = [pts[n] for n in names]; ok = True; measured = None
                    if kind in {'length', 'grip'}:
                        measured = distance(*p)
                        ok = check['min'] <= measured <= check['max'] if kind == 'length' else measured <= check['max_error']
                    elif kind == 'bend':
                        measured = (p[2][0]-p[0][0])*(p[1][1]-p[0][1])-(p[2][1]-p[0][1])*(p[1][0]-p[0][0])
                        ok = measured * check['sign'] >= -check['epsilon']
                    elif kind == 'pin': measured = distance(p[0], check['anchor']); ok = measured <= check['max_error']
                    elif kind == 'surface': measured = p[0][1]; ok = check['min'] <= measured <= check['max']
                    elif kind == 'support':
                        measured = p[0][0]; ok = min(p[1][0], p[2][0])-check['max_error'] <= measured <= max(p[1][0], p[2][0])+check['max_error']
                    elif kind == 'step' and f > a:
                        previous = frames.get(f-1, {}).get(names[0])
                        ok = previous is not None
                        if ok: measured = distance(p[0], previous); ok = measured <= check['max_error']
                    if not ok:
                        need(False, f'{label}/{check["id"]}: {kind} failed at frame {f} (measured {measured})')
                        break
            review = reviews.get('actions', {}).get(aid) if isinstance(reviews, dict) and isinstance(reviews.get('actions'), dict) else None
            if not need(isinstance(review, dict), label + ': visual review required'): continue
            need(review.get('start_frame') == a and review.get('end_frame') == b, label + ': visual review interval mismatch')
            for key in ['reviewer', 'orientation', 'soles', 'hands', 'weight_transfer', 'entry_exit', 'trace_matches_visible_geometry']:
                need(text(review.get(key)), label + ': missing observation ' + key)
            need(review.get('not_applicable_reviewed') == exemptions, label + ': visual reviewer must assess every exemption')
            need(review.get('unresolved') == [] and review.get('status') == 'pass', label + ': unresolved/unapproved visual motion')
            for key in ['normal_speed', 'consecutive_frames', 'final_art']:
                need(review.get(key) is True, label + ': unperformed ' + key)
            for key in ['full_body_clip', 'neutral_clip', 'adjacent_frame_sheet', 'sole_grip_overlay']:
                record_file(review.get(key), label + '/' + key)
        for cid, frames in coverage.items():
            need(frames == set(range(start, end)), sid + '/' + cid + ': action inventory must cover entire shot, including holds and entry/exit')
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--stage', choices=['assets', 'proof'], default='proof')
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text())
        errors = validate(data, args.plan.resolve().parent, args.stage)
    except (OSError, ValueError, TypeError, KeyError) as e:
        errors = ['Physics: invalid/unreadable input: ' + str(e)]
    print(json.dumps({'passed': not errors, 'errors': errors,
                     'scope': 'Supplied geometry and review evidence only; not autonomous visual anatomy certification'}, indent=2))
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__': main()
