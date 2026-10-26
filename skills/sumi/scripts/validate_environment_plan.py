#!/usr/bin/env python3
"""Check authored environment bounds/provenance/timing. Cannot certify visual realism."""
import argparse,hashlib,json,math,re
from pathlib import Path
KINDS={'flame','light','shadow','reflection','haze','smoke','cloud','dust','embers','rain','snow','ripple','cloth','texture','parallax','painted_atmosphere'}
GEOMETRY={'flame','cloth','ripple','texture','parallax'}
def finite(n):return type(n) in (int,float) and math.isfinite(n)
def digest(data):return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def record_file(r,root):
    if not isinstance(r,dict) or not isinstance(r.get('path'),str):return False
    p=(root/r['path']).resolve()
    return root.resolve() in p.parents and p.is_file() and p.stat().st_size>0 and r.get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest()
def overlaps(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
def bounds(b,w,h):return isinstance(b,list) and len(b)==4 and all(finite(v) for v in b) and 0<=b[0]<b[2]<=w and 0<=b[1]<b[3]<=h
def validate_plan(p,root):
    root=Path(root).resolve();errors=[]
    def need(ok,msg):
        if not ok:errors.append(msg)
    if not isinstance(p,dict):return ['environment plan must be an object']
    need(p.get('schema')=='sumi-environment-v1','environment schema required')
    need(p.get('style') in {'sumi-original','sumi-light','sumi-dark'},'choose one of three styles')
    fps=p.get('fps');n=p.get('frames');w=p.get('width');h=p.get('height')
    need(type(fps) is int and fps==(30 if p.get('style')=='sumi-original' else 24),'preserve style output clock')
    need(type(n) is int and n>0,'positive frame count required');need(all(type(x) is int and x>0 for x in (w,h)),'positive dimensions required')
    if errors:return errors
    need(p.get('mode') in {'subtle','natural','dramatic'},'choose environment intensity')
    need(record_file(p.get('master'),root),'master file missing/stale/outside project')
    for key in ['environment','time_of_day','weather','motion_reason']:need(isinstance(p.get(key),str) and bool(p[key].strip()),'declare '+key)
    ds=p.get('drivers',[]);es=p.get('effects',[]);regions=p.get('protected_regions',[]);static=p.get('static_regions',[])
    if not all(isinstance(a,list) for a in (ds,es,regions,static)):return errors+['drivers/effects/regions must be lists']
    ids=set()
    for d in ds:
        if not isinstance(d,dict):errors.append('driver must be an object');continue
        need(isinstance(d.get('id'),str) and d['id'] and d['id'] not in ids,'unique driver ID required');
        if isinstance(d.get('id'),str):ids.add(d['id'])
        need(type(d.get('seed')) is int and 0<=d['seed']<=2147483647,'non-negative bounded seed required')
        need(finite(d.get('hz')) and 0<d['hz']<=2,'coherent driver hz must be0..2')
        need(finite(d.get('offset',0)),'invalid driver offset')
    for r in regions+static:
        need(isinstance(r,dict) and bounds(r.get('bounds'),w,h),'invalid protected/static bounds')
    eids=set()
    for e in es:
        if not isinstance(e,dict):errors.append('effect must be an object');continue
        eid=e.get('id');need(isinstance(eid,str) and eid and eid not in eids,'unique effect ID required');
        if isinstance(eid,str):eids.add(eid)
        k=e.get('kind');need(k in KINDS,f'{eid}: unknown kind');need(e.get('driver') in ids,f'{eid}: missing driver')
        need(e.get('pass') in {'background','foreground','lighting'},f'{eid}: invalid compositor pass')
        b=e.get('bounds');good=bounds(b,w,h);need(good,f'{eid}: local bounds outside source')
        a,z=e.get('start_frame'),e.get('end_frame');need(type(a) is int and type(z) is int and 0<=a<z<=n,f'{eid}: invalid frame window')
        for key,default,lo,hi in [('intensity',1,0,1),('opacity',.06,0,.45),('amplitude',1,0,30),('depth_scale',1,.01,4),('fade_in',.4,0,10),('fade_out',.4,0,10)]:
            v=e.get(key,default);need(finite(v) and lo<=v<=hi,f'{eid}: invalid '+key)
        v=e.get('velocity',[0,0]);need(isinstance(v,list) and len(v)==2 and all(finite(x) and abs(x)<=500 for x in v),f'{eid}: invalid velocity')
        need(isinstance(e.get('purpose'),str) and bool(e['purpose'].strip()),f'{eid}: story/material purpose required')
        if k in {'light','shadow','reflection'}:
            need(e.get('pass')=='lighting',f'{eid}: lighting pass required')
            need(isinstance(e.get('receiver'),str) and bool(e['receiver'].strip()),f'{eid}: source-related receiver required')
            light=e.get('source_effect');linked=next((x for x in es if isinstance(x,dict) and x.get('id')==light),None)
            need(linked is not None and linked.get('kind') in {'flame','cloud'} and linked.get('driver')==e.get('driver'),f'{eid}: receiver must share its flame/cloud driver')
            if e.get('affects_character'):need(bool(e.get('character_light_reason')),f'{eid}: explain shared character lighting')
        if k=='texture':
            need(p['style']!='sumi-original',f'{eid}: automatic Original texture boil is disabled')
            need(type(e.get('texture_fps',6)) is int and 1<=e.get('texture_fps',6)<=12,f'{eid}: texture exposure rate1..12 required')
        if k in {'parallax','cloud'}:need(record_file(e.get('layer'),root) and record_file(e.get('clean_plate'),root),f'{eid}: moving layer requires matching cutout and clean plate')
        if k in {'dust','embers','rain','snow'}:
            need(type(e.get('count',18)) is int and 1<=e.get('count',18)<=250,f'{eid}: bounded particle count required')
            need(finite(e.get('radius',1.2)) and .2<=e.get('radius',1.2)<=10,f'{eid}: invalid particle radius')
        if e.get('color') is not None:need(isinstance(e['color'],str) and re.fullmatch(r'#[0-9A-Fa-f]{6}',e['color']) is not None,f'{eid}: six-digit colour required')
        if p['style']=='sumi-dark' and isinstance(e.get('color'),str):
            color=e['color'].lower();channels=[int(color[i:i+2],16) for i in (1,3,5)] if re.fullmatch(r'#[0-9a-f]{6}',color) else []
            need(channels and (channels[0]==channels[1]==channels[2] or (channels[0]>channels[1] and channels[0]>channels[2] and channels[0]<=160 and max(channels[1:])<=65)),f'{eid}: Dark needs neutral or selective dark-red pigment')
        if k=='painted_atmosphere':need(record_file(e.get('layer'),root),f'{eid}: painted atmosphere needs a matching texture layer')
        for key,default,lo,hi in [('variation',.65,0,.9),('layer_opacity',1,0,1)]:
            v=e.get(key,default);need(finite(v) and lo<=v<=hi,f'{eid}: invalid '+key)
        travel=e.get('light_travel',[24,6]);need(isinstance(travel,list) and len(travel)==2 and all(finite(x) and abs(x)<=120 for x in travel),f'{eid}: invalid local light travel')
        if e.get('mask') is not None:need(record_file(e['mask'],root),f'{eid}: mask missing/stale')
        if e.get('layer') is not None:need(record_file(e['layer'],root),f'{eid}: layer missing/stale')
        if good:
            if k in GEOMETRY-{'parallax','painted_atmosphere'}:
                mode={'subtle':.45,'natural':.7,'dramatic':1}.get(p.get('mode'),1)
                effective=e.get('amplitude',1)*e.get('intensity',1)*mode if finite(e.get('amplitude',1)) and finite(e.get('intensity',1)) else float('inf')
                need(effective<=.1*min(b[2]-b[0],b[3]-b[1]),f'{eid}: deformation too large for bounded micro-motion')
                need(e.get('velocity',[0,0])==[0,0],f'{eid}: local patch drift requires extracted layer/clean plate instead')
            if b==[0,0,w,h] and k in {'light','shadow','reflection','texture'}:errors.append(f'{eid}: global colour/texture effect forbidden')
            for r in regions:
                if isinstance(r,dict) and bounds(r.get('bounds'),w,h) and overlaps(b,r['bounds']):
                    allow=(k in {'light','shadow','reflection'} and e.get('affects_character') and r.get('role')=='character') or (k not in GEOMETRY and r.get('id') in e.get('holdouts',[]))
                    need(allow,f'{eid}: overlaps protected '+str(r.get('id')))
            if k in GEOMETRY:
                for r in static:
                    if isinstance(r,dict) and bounds(r.get('bounds'),w,h):need(not overlaps(b,r['bounds']),f'{eid}: would move rigid '+str(r.get('id')))
    need(bool(es),'animate decision requires an effect; use still with a reason otherwise')
    return errors

def validate(data,root,stage='assets'):
    version=tuple(int(v) for v in re.findall(r'\d+',str(data.get('release_version','0.0.0'))))
    if version<(4,8,0):return []
    errors=[]
    for shot in data.get('shots',[]):
        e=shot.get('environment',{});label=str(shot.get('id'))+': environment '
        if e.get('decision')=='still':
            if not isinstance(e.get('reason'),str) or not e['reason'].strip():errors.append(label+'stillness reason required')
            continue
        if e.get('decision')!='animate':errors.append(label+'decision remains pending');continue
        if not record_file(e.get('plan'),Path(root).resolve()):errors.append(label+'plan missing/stale');continue
        path=Path(root)/e['plan']['path'];plan=json.loads(path.read_text());errors += [label+x for x in validate_plan(plan,Path(root))]
        if plan.get('style')!=data.get('style') or plan.get('fps')!=data.get('output_fps'):errors.append(label+'style/output clock mismatch')
        expected=round((shot.get('end',0)-shot.get('start',0))*data.get('output_fps',0))
        if plan.get('frames')!=expected:errors.append(label+'shot runtime mismatch')
        if stage=='proof':
            review=e.get('review') or {}
            if review.get('plan_sha256')!=digest(plan):errors.append(label+'review missing/stale')
            for key in ['clip','adjacent_frames']:
                if not record_file(review.get(key),Path(root).resolve()):errors.append(label+key+' evidence required')
            if review.get('normal_speed') is not True or review.get('unresolved')!=[] or not review.get('observation'):errors.append(label+'actual sequence review incomplete')
            if version>=(4,8,1):
                v=review.get('visibility') or {}
                if v.get('normal_speed_visible') is not True or not all(v.get(k) for k in ['display_size','mechanism','time_window','observation']):errors.append(label+'normal-speed visibility review missing')
    return errors

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('plan',type=Path);x=a.parse_args()
    try:errors=validate_plan(json.loads(x.plan.read_text()),x.plan.resolve().parent)
    except (OSError,ValueError,TypeError) as e:a.exit(2,str(e)+'\n')
    print(json.dumps({'ok':not errors,'errors':errors,'visual_certification':False},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
