"""Original authored mood scores rendered locally. No API, samples or model.

Three editable parts, deliberate note rhythms and chord voicings. Timbres are
synthetic felt/plucked/air/bowed impressions, not acoustic recordings.
"""
from array import array
import math
import random

SR = 48000


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def note(pitch, duration, instrument, rng):
    n = round(duration * SR); f = hz(pitch)
    result = array('f')
    if instrument in ('plucked', 'harp'):
        # Fractional delay compensates the smoothing filter's half-sample
        # phase delay. Rounding a string to whole samples detunes high notes.
        delay = SR / f - .5
        size = math.ceil(delay) + 2
        line = [rng.uniform(-1, 1) for _ in range(size)]
        # Remove DC before the feedback loop, then soften the excitation.
        mean = sum(line) / size
        line = [x - mean for x in line]
        for _ in range(3):
            line = [(line[i] + line[(i + 1) % size]) * .5 for i in range(size)]
        decay = .9965 if instrument == 'harp' else .993
        for i in range(n):
            pos = i % size
            read = (pos - delay) % size
            index = int(read); fraction = read - index
            a = line[index] * (1 - fraction) + line[(index + 1) % size] * fraction
            b = line[(index - 1) % size] * (1 - fraction) + line[index] * fraction
            x = .5 * (a + b)
            line[pos] = decay * x
            edge = min(1, i / (.004 * SR), (n - 1 - i) / (.05 * SR))
            result.append(x * edge * 1.9)
        return result
    partials = [(1, 1, 1.1), (2, .21, .42), (3, .08, .22)]
    if instrument == 'bell':
        partials = [(1, .8, .9), (2.76, .11, .35), (4.07, .035, .16)]
    for i in range(n):
        t = i / SR
        env = min(1, t / .014, (duration - t) / .08)
        x = sum(level * math.sin(2 * math.pi * f * ratio * t) * math.exp(-t / tau)
                for ratio, level, tau in partials)
        result.append(x * max(0, env) * .42)
    return result


def pad(pitches, duration, kind):
    n = round(duration * SR)
    out = array('f', [0]) * n
    for index, pitch in enumerate(pitches):
        f = hz(pitch)
        # Slight harmonic richness without wide beating or a noise riser.
        for i in range(n):
            t = i / SR
            env = min(1, t / .55, (duration - t) / .65)
            vibrato = .002 * math.sin(2 * math.pi * .31 * t + index)
            phase = 2 * math.pi * f * t + vibrato
            x = math.sin(phase) + .12 * math.sin(phase * 2) + .035 * math.sin(phase * 3)
            if kind == 'strings':
                x += .045 * math.sin(phase * 5)
            if kind == 'dark':
                x *= .78
            out[i] += x * max(0, env) / (len(pitches) * 1.3)
    return out


def drum(duration, frequency, strength, rng):
    n = round(duration * SR); out = array('f'); phase = low = 0.0
    for i in range(n):
        t = i / SR
        phase += 2 * math.pi * frequency * (1 + .28 * math.exp(-t / .022)) / SR
        low += .12 * (rng.uniform(-1, 1) - low)
        body = (math.sin(phase) + .15 * math.sin(phase * 1.61)) * math.exp(-t / .16)
        hit = low * math.exp(-t / .009) * .4
        env = min(1, i / 96, (n - 1 - i) / 480)
        out.append((body + hit) * max(0, env) * strength)
    return out


def put(stereo, samples, at, gain, pan=0):
    start = round(at * SR); angle = (pan + 1) * math.pi / 4
    left, right = gain * math.cos(angle), gain * math.sin(angle)
    for i, x in enumerate(samples):
        if start + i >= len(stereo[0]):
            break
        stereo[0][start + i] += x * left
        stereo[1][start + i] += x * right


def compose(profile, seed=20261024, intensity=.7):
    if not isinstance(intensity, (int, float)) or isinstance(intensity, bool) or not math.isfinite(intensity) or not 0 <= intensity <= 1:
        raise ValueError('Intensity must be 0..1')
    beat = 60 / profile['bpm']; bars = profile['bars']
    # A two-second natural ending is separate from the metrical body.
    body = bars * 4 * beat; duration = body + 2
    n = round(duration * SR)
    stems = {name:[array('f', [0]) * n, array('f', [0]) * n]
             for name in ('harmony','melody','rhythm')}
    rng = random.Random(seed)
    events = []
    root = profile['root_midi']
    for section in range(bars // 2):
        chord = profile['chords'][section % len(profile['chords'])]
        at = section * 8 * beat
        length = min(8 * beat + .55, duration - at)
        pitches = [root + interval - 12 for interval in chord]
        put(stems['harmony'], pad(pitches, length, profile['pad']), at, .095)
        events.append({'part':'harmony','at':at,'duration':length,'midi':pitches})
        rhythm = [0, 1.5, 3, 4, 5.5, 6.5]
        for index, offset in enumerate(rhythm):
            pitch = root + 12 + profile['motif'][(section * 2 + index) % len(profile['motif'])]
            at_note = at + offset * beat
            length_note = min(1.75 * beat, duration - at_note)
            level = .09 * (.7 + .3 * intensity) * (1 if index % 3 == 0 else .78)
            put(stems['melody'], note(pitch,length_note,profile['instrument'],rng), at_note, level,
                -.12 if index % 2 == 0 else .12)
            events.append({'part':'melody','at':at_note,'duration':length_note,'midi':pitch})
    for bar in range(bars):
        chord = profile['chords'][(bar // 2) % len(profile['chords'])]
        at = bar * 4 * beat
        bass = max(33, root + chord[0] - 24)
        put(stems['harmony'], note(bass, min(3.4 * beat,duration-at), 'felt',rng),at,.10)
        style = profile['rhythm']
        strikes = {'none':[], 'soft':[0], 'steady':[0,2], 'pulse':[0,2.5],
                   'heartbeat':[0,.65,2,2.65], 'march':[0,1,2,3]}[style]
        for offset in strikes:
            when = at + offset * beat
            gain = .045 if style in ('soft','pulse') else .075
            put(stems['rhythm'], drum(.65,65 if offset % 2 == 0 else 95,1,rng),when,gain*intensity)
            events.append({'part':'rhythm','at':when,'duration':.65,'kind':'drum'})
    # Resolve according to the theme; mysterious/dread scores keep their tension.
    final_pitch = root + (6 if profile['id']=='dread' else 7 if profile['id']=='suspense' else 12)
    put(stems['melody'], note(final_pitch,2.0,profile['instrument'],rng),body,.07)
    for stereo in stems.values():
        for c in range(2):
            for i in range(n):
                t = i / SR
                stereo[c][i] *= max(0,min(1,t/.12,(duration-t)/.7))
    return stems, {'id':profile['id'],'name':profile['name'],'duration':n/SR,'metrical_body_seconds':body,
                   'bpm':profile['bpm'],'bars':bars,'seed':seed,'intensity':intensity,
                   'source':'original Python composition','synthetic_instruments':True,
                   'provider_calls':0,'events':events,'review':'pending'}
