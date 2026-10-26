#!/usr/bin/env python3
"""Deterministic motion parameters for authored masks/rigs. Does not locate anatomy.

Adapter contract: keep specified anchors/supports fixed; apply parameters only to
reviewed target regions. Camera/environment are separate and cannot count as
character animation. No third-party dependency is used here.
"""
import argparse
import json
import math


def character_clock(frame, output_fps=30, state_fps=20):
    if any(type(x) is not int or x < 1 for x in (output_fps,state_fps)) or state_fps > output_fps:
        raise ValueError('positive integer state rate must not exceed output rate')
    if type(frame) is not int or frame < 0:
        raise ValueError('non-negative integer frame required')
    state=frame*state_fps//output_fps
    start=(state*output_fps+state_fps-1)//state_fps
    return {'state':state,'start_frame':start,'time':state/state_fps}


def smooth(x):
    x=max(0,min(1,x));return x*x*(3-2*x)


def pulse(t,start,attack,hold,release):
    if t < start:return 0.0
    if attack > 0 and t < start+attack:return smooth((t-start)/attack)
    if t < start+attack+hold:return 1.0
    return 1-smooth((t-start-attack-hold)/release) if release > 0 else 0.0


def sample(motion,t):
    """Scalar displacement/closure, not a full image or a new drawing."""
    if not math.isfinite(t) or t < 0:raise ValueError('finite non-negative time required')
    kind=motion['behavior'];amp=float(motion.get('amplitude',1));phase=float(motion.get('phase',0))
    start=float(motion.get('start',0));end=float(motion.get('end',1e9))
    if not all(math.isfinite(v) for v in (amp,phase,start,end)) or end < start:raise ValueError('invalid motion bounds')
    if not start <= t < end:return 0.0
    q=t-start
    fade=min(smooth(q/.18),smooth((end-t)/.22))
    if kind in {'hair','cloth'}:
        hz=float(motion.get('hz',.45));v=.72*math.sin(2*math.pi*hz*q+phase)+.28*math.sin(2*math.pi*hz*.61*q+phase*1.7)
        for gust in motion.get('gusts',[]):v+=float(gust.get('strength',1))*pulse(t,float(gust['at']),.2,.12,.75)
        return amp*v*fade
    if kind=='breath':return amp*(1-math.cos(2*math.pi*float(motion.get('hz',.22))*q+phase))*.5*fade
    if kind=='tremble':return amp*(.6*math.sin(2*math.pi*6.7*q+phase)+.4*math.sin(2*math.pi*9.1*q+.4+phase))*fade
    if kind=='blink':return max([pulse(t,float(e['at']),float(e.get('close',.055)),float(e.get('hold',.025)),float(e.get('open',.11))) for e in motion.get('events',[])]+[0])
    if kind=='gaze':
        value=0.0
        for e in motion.get('events',[]):
            if t >= e['at']:value+=float(e['delta'])*smooth((t-e['at'])/float(e.get('settle',.16)))
        return amp*value*fade
    raise ValueError('unknown character behavior: '+kind)


def anchored_displacement(value,along,across=0):
    """Zero at attachment and lateral patch edges; along/across normalized0..1/-1..1."""
    if not 0 <= along <= 1 or not -1 <= across <= 1:raise ValueError('outside authored patch')
    return value*smooth(along)*max(0,1-across*across)**2


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan');p.add_argument('output');p.add_argument('--frames',type=int,required=True);p.add_argument('--fps',type=int,default=30);p.add_argument('--state-fps',type=int,default=20);a=p.parse_args()
    if a.frames < 1:p.error('positive frame count required')
    motions=json.load(open(a.plan))['motions'];rows=[]
    for frame in range(a.frames):
        c=character_clock(frame,a.fps,a.state_fps);rows.append({'frame':frame,**c,'values':{m['id']:sample(m,c['time']) for m in motions}})
    with open(a.output,'w') as f:json.dump({'status':'motion-parameters-not-rendered-art','frames':rows},f,indent=2);f.write('\n')

if __name__=='__main__':main()
