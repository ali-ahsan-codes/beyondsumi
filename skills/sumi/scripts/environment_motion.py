"""Deterministic environment parameters, not segmentation or physical-light simulation.

Local source-space effects are evaluated at output time, independent of character
pose clocks. Linked receivers share one driver. No image generation/network/deps.
"""
import argparse
import json
import math
from pathlib import Path

KINDS={'flame','light','shadow','reflection','haze','smoke','cloud','dust','embers','rain','snow','ripple','cloth','texture','parallax','painted_atmosphere'}
MODES={'subtle':.45,'natural':.7,'dramatic':1.0}
PASSES={'background','foreground','lighting'}

def smooth(x):
    x=max(0.0,min(1.0,x));return x*x*(3-2*x)

def rand(n,seed):
    x=(int(n)*374761393+int(seed)*668265263)&0xffffffff
    x=((x^(x>>13))*1274126177)&0xffffffff
    return ((x^(x>>16))&0xffffffff)/4294967295

def noise(t,seed):
    n=math.floor(t);u=smooth(t-n)
    return (2*rand(n,seed)-1)*(1-u)+(2*rand(n+1,seed)-1)*u

def driver(d,t):
    hz=d.get('hz',.35);q=t+d.get('offset',0);seed=d.get('seed',0)
    # Coherent, bounded, low-frequency variation; direct seeks match forward play.
    phase=rand(0,seed)*2*math.pi
    return .50*math.sin(2*math.pi*hz*q+phase)+.34*noise(q*hz*.71,seed+37)+.16*noise(q*hz*.37,seed+97)

def envelope(e,t,fps):
    start=e['start_frame']/fps;end=e['end_frame']/fps
    if t<start or t>=end:return 0.0
    a=e.get('fade_in',.4);b=e.get('fade_out',.4)
    return min(smooth((t-start)/a) if a else 1,smooth((end-t)/b) if b else 1)

def sample(plan,frame):
    if type(frame) is not int or not 0<=frame<plan['frames']:raise ValueError('frame outside plan')
    t=frame/plan['fps'];drivers={d['id']:driver(d,t) for d in plan['drivers']};rows=[]
    for e in plan['effects']:
        env=envelope(e,t,plan['fps'])
        if env<=0:continue
        value=drivers[e['driver']];strength=MODES[plan['mode']]*e.get('intensity',1);q=t-e['start_frame']/plan['fps']
        # Drift is in authored source pixels/s, not arbitrary full-image movement.
        depth=e.get('depth_scale',1);velocity=e.get('velocity',[0,0]);amp=e.get('amplitude',1)*strength
        dx=(velocity[0]*q*depth*strength+value*amp)*env;dy=(velocity[1]*q*depth*strength+value*amp*.25)*env
        opacity=e.get('opacity',.12)*(1+e.get('variation',.65)*value)*strength*env
        if e['kind'] in {'light','shadow','reflection'}:
            travel=e.get('light_travel',[24,6]);dx=travel[0]*value*strength*env;dy=travel[1]*value*strength*env
        if e['kind']=='texture':
            rate=e.get('texture_fps',6);value=driver(next(d for d in plan['drivers'] if d['id']==e['driver']),math.floor(t*rate)/rate)
            dx=value*amp*env;dy=value*amp*.25*env
        default_color=('#141414' if e['kind']=='shadow' else '#c8c8c8') if plan['style']=='sumi-dark' else ('#171321' if e['kind']=='shadow' else '#e4d5bb')
        rows.append({**e,'color':e.get('color',default_color),'seed':e.get('seed',next(d['seed'] for d in plan['drivers'] if d['id']==e['driver'])),'dx':dx,'dy':dy,'alpha':opacity,'signal':value,'envelope':env,'time':t,'strength':strength})
    return {'frame':frame,'style':plan['style'],'time':t,'drivers':drivers,'effects':rows}

def bake(plan):
    return {'schema':'sumi-environment-samples-v1','status':'parameters-not-reviewed-animation','width':plan['width'],'height':plan['height'],'fps':plan['fps'],'frames':[sample(plan,f) for f in range(plan['frames'])]}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    # Validation is imported from the installed/project helper tree by callers.
    plan=json.loads(a.plan.read_text())
    from validate_environment_plan import validate_plan
    errors=validate_plan(plan,a.plan.resolve().parent)
    if errors:p.error('; '.join(errors))
    if a.output.exists():p.error('Preserve earlier bake; choose a new output')
    a.output.write_text(json.dumps(bake(plan),separators=(',',':'))+'\n')

if __name__=='__main__':main()
