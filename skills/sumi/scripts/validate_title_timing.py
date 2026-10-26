#!/usr/bin/env python3
"""Check declared title timing. Actual visibility/readability needs export review."""
import argparse
import json
import math
from pathlib import Path


def validate(plan):
    errors = []
    def num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    if not isinstance(plan, dict):
        return ['Titles: plan must be an object']
    timing = plan.get('title_timing')
    if not isinstance(timing, dict):
        return ['Titles: title_timing record required']
    cards = timing.get('cards')
    if timing.get('decision') != 'planned' or not isinstance(cards, list) or not cards:
        return ['Titles: plan the opening/closing title before production']
    duration = plan.get('duration')
    previous_end = -1
    for i, card in enumerate(cards):
        label = f'Titles[{i}]'
        if not isinstance(card, dict):
            errors.append(label+': object required'); continue
        start, end = card.get('start'), card.get('end')
        valid = (num(start) and num(end) and num(duration) and
                 0 <= start < end <= duration and end-start <= 3+1e-9)
        if not valid:
            errors.append(label+': first visible backing/word through fully gone must be inside film and at most3seconds')
        if num(start) and start < previous_end:
            errors.append(label+': title cards overlap or are out of order')
        if num(end): previous_end = end
        units = card.get('units')
        if not isinstance(units, list) or not units:
            errors.append(label+': ordered words or deliberate phrase groups required'); continue
        last_start = -1
        settled = []
        for j, unit in enumerate(units):
            if not isinstance(unit, dict):
                errors.append(label+f' unit{j}: object required'); continue
            a, b, text = unit.get('start'), unit.get('settled'), unit.get('text')
            if not (isinstance(text, str) and text.strip() and valid and
                    num(a) and num(b) and start <= a < b < end):
                errors.append(label+f' unit{j}: text and entrance/settled timing required')
            if num(a):
                if a <= last_start: errors.append(label+': words must enter individually in reading order')
                last_start = a
            if num(b): settled.append(b)
        if valid and settled and end-max(settled) < .5:
            errors.append(label+': completed title needs at least0.5second before fully gone; visually check stable hold and exit')
    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path)
    a = p.parse_args()
    try: errors = validate(json.loads(a.plan.read_text()))
    except (OSError, ValueError) as e: p.exit(2, f'Invalid plan: {e}\n')
    print(json.dumps({'ok': not errors, 'errors': errors,
                      'limit': 'Declared timing only; inspect actual title/backing visibility and readability.'}, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__': main()
