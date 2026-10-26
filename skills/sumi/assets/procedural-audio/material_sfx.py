"""Original local material-inspired sound design; Python stdlib, not recordings.

Return mono floats at 48 kHz. Use the seeded process random state, as synth.py
does, so the score renderer remains reproducible. Listen before delivery:
these are controllable synthetic impressions, not authentic field recordings.
"""
import math
import random

SR = 48000
KINDS = {'brush', 'ink_drop', 'splash', 'footstep', 'cloth',
         'wood_crack', 'blade', 'drum', 'rain', 'wind'}


def render(kind, duration, frequency=None):
    if kind not in KINDS:
        raise ValueError('Unknown material sound')
    if (isinstance(duration, bool) or not isinstance(duration, (int, float))
            or not math.isfinite(duration) or not .005 <= duration <= 120):
        raise ValueError('Material duration must be finite, .005–120 seconds')
    if frequency is not None and (isinstance(frequency, bool)
            or not isinstance(frequency, (int, float))
            or not math.isfinite(frequency) or not 20 <= frequency <= 12000):
        raise ValueError('Material frequency must be finite, 20–12000 Hz')
    defaults = {'drum': 78, 'blade': 1350, 'footstep': 115,
                'wood_crack': 185, 'ink_drop': 480}
    f = frequency if frequency is not None else defaults.get(kind, 220)
    n = round(duration * SR)
    low = mid = phase = droplets = 0.0
    out = []
    for i in range(n):
        t, u = i / SR, i / n
        noise = random.uniform(-1, 1)
        low += .055 * (noise - low)
        mid += .38 * (noise - mid)
        high = noise - mid
        body = math.sin(2 * math.pi * f * t)
        if kind == 'drum':
            # Falling membrane pitch, inharmonic skin modes, short beater.
            phase += 2 * math.pi * f * (1 + .42 * math.exp(-t / .025)) / SR
            x = (.72 * math.sin(phase) + .20 * math.sin(phase * 1.59)
                 + .08 * math.sin(phase * 2.14)) * math.exp(-t / .24)
            x += .42 * mid * math.exp(-t / .012)
        elif kind == 'blade':
            x = sum(g * math.sin(2 * math.pi * f * ratio * t)
                    * math.exp(-t / tau) for ratio, g, tau in
                    [(1, .35, .20), (1.43, .25, .12), (2.17, .17, .08)])
            x += high * .5 * math.exp(-t / .009)
        elif kind == 'wood_crack':
            crack = sum(math.exp(-max(0, t - at) / .006)
                        if t >= at else 0 for at in [0, .018, .047])
            x = .72 * high * crack + .3 * (low + body) * math.exp(-t / .11)
        elif kind == 'footstep':
            heel = math.exp(-t / .025)
            toe = math.exp(-max(0, t - duration * .32) / .018) if u >= .32 else 0
            x = (.42 * body + .8 * low) * heel + .28 * mid * toe
        elif kind == 'ink_drop':
            phase += 2 * math.pi * f * (1 + 1.8 * math.exp(-t / .025)) / SR
            x = .55 * math.sin(phase) * math.exp(-t / .075)
            x += .5 * mid * math.exp(-t / .04)
        elif kind == 'splash':
            bubbles = .5 + .5 * math.sin(70 * t + math.sin(103 * t))
            x = (1.35 * mid + .6 * low) * math.exp(-t / max(.02, duration / 3)) * bubbles
        elif kind == 'brush':
            x = (.7 * mid + .18 * high) * math.sin(math.pi * u) ** .7
            x *= .7 + .3 * math.sin(t * 130 + math.sin(t * 37)) ** 2
        elif kind == 'cloth':
            folds = (.5 + .5 * math.sin(t * 39 + math.sin(t * 17))) ** 2
            x = (.85 * low + .22 * mid) * folds * math.sin(math.pi * u)
        elif kind == 'rain':
            if random.random() < 150 / SR:
                droplets += random.uniform(.15, .65)
            droplets *= .94
            x = .18 * mid + droplets * high
        else:  # wind
            gust = .55 + .3 * math.sin(t * 1.9) + .15 * math.sin(t * 4.3)
            x = 1.7 * low * gust
        # Very short edge fade prevents section-boundary clicks.
        edge = min(1, i / max(1, .0015 * SR), (n - 1 - i) / max(1, .006 * SR))
        out.append(x * edge)
    return out
