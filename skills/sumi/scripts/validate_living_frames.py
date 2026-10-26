"""Evidence checks for authored living frames. No pixel/anatomy recognition."""
from pathlib import Path
import hashlib
import json
import math
import re
from living_frames import character_clock


def _file(row,root):
    if not isinstance(row,dict) or not isinstance(row.get('path'),str):return None
    p=(root/row['path']).resolve()
    if root not in p.parents or not p.is_file():return None
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    return digest if digest==row.get('sha256') else None


def validate_original_states(shot,root,state_fps=20,output_fps=30,source_key="original_drawings",whole_drawings_only=False):
    root=Path(root).resolve();errors=[];d=shot.get('style_profile',{}).get(source_key,{});label=str(shot.get('id'))+f': {state_fps} character states'
    def need(ok,msg):
        if not ok:errors.append(label+': '+msg)
    need(d.get('budget_mode')=='action-driven','new-source budget must remain action-driven')
    need(shot.get('style_profile',{}).get('cadence',{}).get('exposure_policy')==f'{state_fps}-in-{output_fps}',f'declare {state_fps}-in-{output_fps} exposure policy')
    if d.get('deliberate_stillness') is True:
        need(bool(str(d.get('stillness_reason','')).strip()),'stillness reason required');return errors
    sources={r.get('id'):_file(r.get('file',r.get('image')),root) for r in d.get('source_images',[]) if isinstance(r,dict)}
    states={};identities={}
    for row in d.get('designed_states',[]):
        sid=row.get('id');need(isinstance(sid,str) and sid not in states,'unique designed state IDs required')
        source=sources.get(row.get('source_id'));need(bool(source),'state source hash missing/stale')
        kind=row.get('kind');need(kind in {'whole-drawing','derived-character'},'state must be a drawing or supported derived character motion')
        if whole_drawings_only:
            need(kind=='whole-drawing','smooth24 requires actual distinct pose/in-between drawings; camera, grain and derived micro-motion are not extra pose art')
        roi=row.get('roi_xywh');roi=tuple(roi) if isinstance(roi,list) else None
        signature=(source,roi)
        if kind=='derived-character':
            need(bool(_file(row.get('rig'),root)),'derived state needs hashed renderer/rig')
            values=row.get('character_parameters')
            need(isinstance(values,dict) and bool(values) and all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in values.values()),'actual finite character parameters required; camera/light/weather excluded')
            need(bool(row.get('target_ids')),'derived state must name its checked character targets')
            need(isinstance(values,dict) and all(re.fullmatch(r'(hair|cloth|breath|eye|brow|mouth|tear|hand|body)_[A-Za-z0-9_]+',k) for k in values),'camera/environment-only parameters cannot count as character states')
            signature+=(json.dumps(values,sort_keys=True),json.dumps(row.get('target_ids'),sort_keys=True))
        identities[sid]=signature;states[sid]=row
    entries=d.get('exposure_plan',[]);first=round(shot.get('start',0)*output_fps);last=round(shot.get('end',0)*output_fps);cursor=first;used=[];k=0
    while cursor < last and k < len(entries):
        e=entries[k];offset=character_clock(cursor-first,output_fps,state_fps)['state'];end=min(last,first+math.ceil((offset+1)*output_fps/state_fps))
        need(e.get('start_frame')==cursor and e.get('end_frame')==end,'contiguous exposures at the selected character clock required')
        need(e.get('state_id') in states,'missing designed character state')
        used.append(identities.get(e.get('state_id')));cursor=end;k+=1
    need(cursor==last and k==len(entries) and bool(entries),'complete exposure coverage required')
    window=min(state_fps,len(used))
    if window:
        for i in range(len(used)-window+1):need(None not in used[i:i+window] and len(set(used[i:i+window]))==window,f'repeated/aliased states do not provide {state_fps} distinct character states per second')
    return errors


def validate(data,root,stage='assets'):
    match=re.fullmatch(r'(\d+)\.(\d+)\.(\d+)',str(data.get('release_version','')))
    if not match or tuple(map(int,match.groups())) < (4,6,1):return []
    root=Path(root).resolve();errors=[]
    for shot in data.get('shots',[]):
        cfg=shot.get('style_profile',{});strategy=cfg.get('animation_strategy');label=str(shot.get('id'))+': Living Frames'
        def need(ok,msg):
            if not ok:errors.append(label+': '+msg)
        need(strategy in {'whole_pose','living_frame','mixed'},'choose a shot strategy')
        if strategy not in {'living_frame','mixed'}:continue
        lf=cfg.get('living_frame') or {};need(bool(_file(lf.get('master'),root)),'complete master hash missing/stale')
        need(bool(str(lf.get('intent','')).strip()),'emotional/story intent required')
        need(1 <= len(lf.get('primary_focus',[])) <= 2,'choose one/two primary details')
        need(len(lf.get('secondary_motion',[])) <= 2,'at most two supporting motions')
        need(bool(lf.get('protected_regions')),'declare protected face/grip/support regions')
        need(bool(str(lf.get('camera','')).strip()),'declare motivated camera or stillness')
        for m in lf.get('motions',[]):
            need(m.get('behavior') in {'hair','cloth','breath','tremble','blink','gaze'},'unknown character behavior')
            need(bool(m.get('target')) and bool(m.get('anchor')),'target/anchor required')
            need(bool(_file(m.get('mask'),root)),'target mask missing/stale')
            need(bool(_file(m.get('rig'),root)),'renderer/rig missing/stale')
            if m.get('exposes_hidden_pixels') is not False:need(bool(_file(m.get('clean_plate'),root)),'moving patch needs clean plate or explicit no-hidden-pixels reasoning')
            else:need(bool(str(m.get('no_plate_reason','')).strip()),'explain why no hidden pixels are exposed')
        if stage=='proof':need(bool(_file(lf.get('comparison'),root)) and bool(str(lf.get('observation','')).strip()),'actual composed source/extrema comparison and observations required')
    return errors
