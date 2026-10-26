#!/usr/bin/env python3
"""Render an authored JSON score using Python stdlib. No API or network calls.
Synth primitives adapted from whaleyxbt/claude-motion, MIT; see LICENSE.
This original adapter writes aligned music, effects and background stems.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import wave
import synth
import material_sfx

SR = synth.SR
KINDS = {'pluck', 'bell', 'tone', 'click', 'impact', 'whoosh', 'riser', 'scratch'} | material_sfx.KINDS

def number(x, lo, hi, label):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or not lo <= x <= hi:
        raise ValueError(f'{label} must be a finite number in [{lo}, {hi}]')
    return x

def validate(p):
    duration = number(p.get('duration'), .1, 120, 'duration (render long films in sections)')
    seed = p.get('seed', 11)
    if isinstance(seed, bool) or not isinstance(seed, int): raise ValueError('seed must be an integer')
    number(p.get('ceiling_db', -6), -30, -1, 'sample peak ceiling')
    for key in ['fade_in', 'fade_out']: number(p.get(key, .12 if key=='fade_in' else .5), 0, duration, key)
    for bed in p.get('beds', []):
        at = number(bed.get('at', 0), 0, duration, 'bed.at')
        length = number(bed['duration'], .01, duration, 'bed.duration')
        if at+length > duration+1/SR: raise ValueError('bed extends beyond duration')
        number(bed.get('gain', .03), 0, 2, 'bed.gain')
        last = -1
        for start, freqs in bed['chords']:
            number(start, 0, length, 'chord time')
            if start <= last or start >= length: raise ValueError('chord times must increase inside bed')
            last = start
            if not freqs: raise ValueError('chord needs frequencies')
            for f in freqs: number(f, 20, 12000, 'frequency')
        if not bed['chords'] or bed['chords'][0][0] != 0: raise ValueError('first chord must start at 0')
    for e in p.get('events', []):
        if e['kind'] not in KINDS: raise ValueError('unknown sound kind')
        if e.get('stem','sfx') not in ('music','sfx'): raise ValueError('stem must be music or sfx')
        at=number(e['at'],0,duration,'event.at'); length=number(e['duration'],.005,duration,'event.duration')
        if at+length > duration+1/SR: raise ValueError('event tail extends beyond score; shorten it explicitly')
        number(e.get('gain',.1),0,2,'event.gain');number(e.get('pan',0),-1,1,'pan')
        for key in ['freq','f0','f1']:
            if key in e: number(e[key],20,12000,key)
    for d in p.get('ducks', []):
        start=number(d['start'],0,duration,'duck.start');end=number(d['end'],0,duration,'duck.end')
        if start>=end: raise ValueError('duck end must follow start')
        number(d.get('gain',.35),0,1,'duck.gain')
        number(d.get('attack',.08),.001,10,'duck.attack');number(d.get('release',.25),.001,10,'duck.release')
    return duration

def mono(e):
    k=e['kind'];d=e['duration'];f=e.get('freq',220)
    if k in material_sfx.KINDS: return material_sfx.render(k,d,e.get('freq'))
    if k=='pluck': return synth.blip(f,d,tau=max(.01,d/4))
    if k=='bell': return synth.chime([f,f*2],d,tau=max(.01,d/3))
    if k=='tone': return [math.sin(2*math.pi*f*i/SR) for i in range(round(d*SR))]
    if k=='click': return synth.click(f,d)
    if k=='impact': return synth.impact(d)
    if k=='whoosh': return synth.whoosh(d,e.get('f0',250),e.get('f1',2400))
    if k=='riser': return synth.riser(d,e.get('f0',250),e.get('f1',2400))
    return synth.scratch(d)

def write_pcm(path,left,right,gain):
    samples=array('h')
    for a,b in zip(left,right):
        # Attenuation is determined from ALL stems before PCM conversion.
        samples.extend((round(a*gain*32767),round(b*gain*32767)))
    if sys.byteorder!='little': samples.byteswap()
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(samples.tobytes())

def render(plan,out):
    duration=validate(plan)
    if out.exists(): raise ValueError('Output directory exists; use a new version directory')
    random.seed(plan.get('seed',11));n=round(duration*SR)
    music=[array('f',[0])*n,array('f',[0])*n];fx=[array('f',[0])*n,array('f',[0])*n]
    for bed in plan.get('beds',[]):
        length=bed['duration']; fade=min(.25,length/3)
        volume=synth.envelope([(0,0),(fade,1),(length-fade,1),(length,0)])
        left,right=synth.pad(length,bed['chords'],volume=volume)
        at=round(bed.get('at',0)*SR);g=bed.get('gain',.03)
        for j,(a,b) in enumerate(zip(left,right)):
            if at+j<n:music[0][at+j]+=a*g;music[1][at+j]+=b*g
    for e in plan.get('events',[]):
        samples=mono(e);at=round(e['at']*SR);g=e.get('gain',.1);pan=e.get('pan',0)
        dest=music if e.get('stem','sfx')=='music' else fx
        gl=g*math.cos((pan+1)*math.pi/4);gr=g*math.sin((pan+1)*math.pi/4)
        edge=max(1,min(round(.004*SR),len(samples)//3))
        for j,s in enumerate(samples):
            if at+j>=n:break
            env=min(1,j/edge,(len(samples)-1-j)/edge)
            dest[0][at+j]+=s*env*gl;dest[1][at+j]+=s*env*gr
    # Phrase-based music ducking; effects remain separately editable.
    envelope=array('f',[1])*n
    for d in plan.get('ducks',[]):
        start,end=d['start'],d['end'];attack=d.get('attack',.08);release=d.get('release',.25);g=d.get('gain',.35)
        for i in range(max(0,int((start-attack)*SR)),min(n,math.ceil((end+release)*SR))):
            t=i/SR
            weight=min(1,max(0,(t-start+attack)/attack),max(0,(end+release-t)/release))
            envelope[i]=min(envelope[i],1-(1-g)*weight)
    fi=plan.get('fade_in',.12)*SR;fo=plan.get('fade_out',.5)*SR
    for i in range(n):
        fade=min(1,i/fi if fi else 1,(n-1-i)/fo if fo else 1)
        for c in range(2):music[c][i]*=envelope[i]*fade;fx[c][i]*=fade
    background=[array('f',(a+b for a,b in zip(music[c],fx[c]))) for c in range(2)]
    peak=max((abs(v) for stem in (music,fx,background) for channel in stem for v in channel),default=0)
    ceiling=10**(plan.get('ceiling_db',-6)/20);gain=min(1,ceiling/peak) if peak else 1
    out.mkdir(parents=True)
    for name,stem in [('music',music),('sfx',fx),('background',background)]:write_pcm(out/f'{name}.wav',*stem,gain)
    (out/'score.json').write_text(json.dumps(plan,indent=2))
    report={'duration_seconds':n/SR,'sample_rate':SR,'channels':2,'seed':plan.get('seed',11),'shared_attenuation':gain,'sample_peak_dbfs':20*math.log10(peak*gain) if peak else None,'silent':peak==0,'true_peak_and_loudness_measured':False,'method':'local Python synthesis; no provider calls','score_sha256':hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()}
    (out/'report.json').write_text(json.dumps(report,indent=2))
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('score',type=Path);ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    try:report=render(json.loads(args.score.read_text()),args.out)
    except (ValueError,KeyError,TypeError) as e:ap.error(str(e))
    print(json.dumps(report))
if __name__=='__main__':main()
