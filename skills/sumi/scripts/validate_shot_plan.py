#!/usr/bin/env python3
"""Check evidence/provenance. This cannot judge anatomy, motion or user approval."""
import argparse, hashlib, json, math, re
from pathlib import Path
from plan_provenance import plan_digest
from sumi_catalog import CATALOG_ID, STYLES, LEGACY_METHODS, uses_current_catalog
METHODS=LEGACY_METHODS  # Historical import compatibility, not the current style menu.

def validate_base(data,root,stage='assets'):
    errors=[];root=root.resolve()
    def need(ok,msg):
        if not ok:errors.append(msg)
    def words(x):return isinstance(x,str) and bool(x.strip())
    def num(x):return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
    def file(item,label):
        if not isinstance(item,dict) or not words(item.get('path')):errors.append(label+': file record required');return
        p=(root/item['path']).resolve()
        if root not in p.parents or not p.is_file() or not p.stat().st_size:errors.append(label+': missing/empty/outside-project file');return
        need(item.get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest(),label+': SHA-256 missing or stale')
    def text_fields(obj,keys,label):
        for k in keys:need(words(obj.get(k)),label+': missing '+k)
    if not isinstance(data,dict):return ['Plan must be an object']
    need(data.get('schema')==2,'Schema 2 required; legacy plans lack complete-character/method evidence')
    need(data.get('identity')=='japanese-sumi','Japanese Sumi identity required')
    current=uses_current_catalog(data)
    if current:
        need(data.get('catalog')==CATALOG_ID,'Current plans must declare the three-style catalogue')
        need(data.get('style') in STYLES,
             'Choose Sumi Original, Sumi Light or Sumi Dark')
    duration=data.get('duration');fps=data.get('output_fps')
    need(num(duration) and duration>0,'Positive duration required');need(num(fps) and 1<=fps<=120,'Output fps must be 1–120')
    text_fields(data.get('approval',{}),['script','direction','duration'],'Recorded user approval')
    chars=data.get('characters');need(isinstance(chars,list),'Declare characters or explicit character-free study')
    if not chars:need(data.get('character_free') is True and words(data.get('character_free_reason')),'Explicit character-free reason required')
    else:need(data.get('character_free') is not True,'Characters conflict with character-free declaration')
    poses={}
    for c in chars if isinstance(chars,list) else []:
        cid=c.get('id');need(words(cid) and cid not in poses,'Unique character ID required')
        if not words(cid):continue
        poses[cid]=set();file(c.get('master'),cid+' master');need(c.get('full_body') is True,cid+': complete body reference required')
        text_fields(c,['species','view','facing','limb_inventory'],cid)
        cp=c.get('poses',[]);need(isinstance(cp,list) and bool(cp),cid+': whole action poses required')
        for pose in cp if isinstance(cp,list) else []:
            pid=pose.get('id');need(words(pid) and pid not in poses[cid],cid+': unique pose ID required')
            if not words(pid):continue
            poses[cid].add(pid);label=cid+'/'+pid
            file(pose.get('image'),label+' whole pose');file(pose.get('review_overlay'),label+' annotated comparison')
            need(pose.get('full_body') is True,label+': whole pose required')
            need(words(pose.get('master_sha256')) and pose['master_sha256']==c.get('master',{}).get('sha256'),label+': master changed since review')
            text_fields(pose,['view','facing','near_far_order','joint_orientation','hand_paw_orientation','support_contact','observation'],label)
            for k in ['limb_count','proportions','joint_bends','facing','contact','identity']:need(pose.get('checks',{}).get(k) is True,label+': unchecked '+k)
            need(pose.get('unresolved')==[],label+': unresolved anatomy issues/missing issue list')
            if pose.get('mirrored') is True:need(pose.get('chirality_rechecked') is True,label+': mirrored side/palm/prop recheck required')
            parts=pose.get('parts',[]);need(isinstance(parts,list),label+': parts must be a list')
            for part in parts if isinstance(parts,list) else []:
                file(part,label+' derived piece');need(part.get('derived_from_sha256')==pose.get('image',{}).get('sha256'),label+': piece not derived from reviewed whole pose')
            if parts:file(pose.get('assembly_overlay'),label+' assembled overlay')
    shots=data.get('shots');need(isinstance(shots,list) and bool(shots),'At least one shot required')
    if not isinstance(shots,list):return errors
    intervals=[];ids=set();method_sources={}
    for s in shots:
        sid=s.get('id');need(words(sid) and sid not in ids,'Unique shot ID required');ids.add(str(sid))
        method=s.get('style') if current else s.get('method')
        mechanisms={key:value['mechanism'] for key,value in STYLES.items()} if current else LEGACY_METHODS
        need(method in mechanisms,f'{sid}: select a current style' if current else f'{sid}: unsupported historical method')
        if current:
            need(s.get('method') is None,f'{sid}: historical method IDs are not primary style labels')
            need(method==data.get('style'),
                 f'{sid}: shot style differs from the selected film style')
        m=s.get('mechanism',{});need(method in mechanisms and m.get('type')==mechanisms.get(method),f'{sid}: wrong animation mechanism')
        files=m.get('files',[]);need(isinstance(files,list) and bool(files),f'{sid}: mechanism source files required')
        for f in files if isinstance(files,list) else []:file(f,f'{sid} mechanism')
        signature=tuple(sorted(f.get('sha256','') for f in files if isinstance(f,dict)))
        if method in mechanisms:method_sources.setdefault(method,set()).add(signature)
        a,b=s.get('start'),s.get('end');valid=num(a) and num(b) and num(duration) and 0<=a<b<=duration
        need(valid,f'{sid}: invalid shot timing')
        if valid:intervals.append((a,b))
        text_fields(s,['performance','camera','transition','strict_identity','economy'],str(sid))
        if current and method=='sumi-original':
            cadence=s.get('style_profile',{}).get('cadence',{})
            version=tuple(map(int,re.findall(r'\d+',str(data.get('release_version','0.0.0')))))
            source_model=('scene-first-designed-states' if version >= (4,6,1) else 'scene-first-variable-exposure' if version >= (4,6,0) else 'requestAnimationFrame-elapsed-time' if data.get('release_version') == '4.0.0' else 'new-on-twos-adaptation')
            need(cadence.get('source_time_model')==source_model,
                 f'{sid}: preserve Original source time model separately from export fps')
            need(cadence.get('output_fps')==fps,f'{sid}: declare the new export clock separately')
        else:
            for k in ['pose_fps','simulation_fps']:need(num(s.get(k)) and 1<=s[k]<=240,f'{sid}: invalid '+k)
        assets=s.get('assets',[])
        procedural_only=(current and data.get('character_free') is True and not s.get('characters')
                         and words(s.get('style_profile',{}).get('procedural_only_reason')))
        need(isinstance(assets,list) and (bool(assets) or procedural_only),f'{sid}: image assets or explicit character-free procedural scene required')
        for f in assets if isinstance(assets,list) else []:file(f,f'{sid} asset')
        uses=s.get('characters');need(isinstance(uses,list),f'{sid}: explicit used characters required')
        for use in uses if isinstance(uses,list) else []:
            cid=use.get('id');need(cid in poses,f'{sid}: undeclared character');used=use.get('poses',[])
            need(isinstance(used,list) and bool(used),f'{sid}: declare whole poses used')
            for pid in used if isinstance(used,list) else []:need(pid in poses.get(cid,set()),f'{sid}: unreviewed/missing pose {pid}')
        for w in s.get('critical_windows',[]):
            need(valid and num(w.get('start')) and num(w.get('end')) and a<=w['start']<w['end']<=b,f'{sid}: critical window outside shot')
            need(num(w.get('fps')) and 1<=w['fps']<=240 and words(w.get('reason')),f'{sid}: critical cadence/reason required')
        if stage=='proof':
            p=s.get('proof',{})
            for k in ['clip','review','adjacent_frame_sheet','neutral_background_clip']:file(p.get(k),f'{sid} '+k)
            review_flags=['normal_speed','adjacent_frames','final_art','japanese_sumi_identity']
            review_flags.append('style_direction_reviewed' if current else 'method_visible_without_colour_camera')
            for k in review_flags:need(p.get(k) is True,f'{sid}: unverified '+k)
            need(p.get('unresolved')==[],f'{sid}: unresolved motion/missing issue list');need(words(p.get('observation')),f'{sid}: observations required')
    intervals.sort();cursor=0
    for a,b in intervals:need(abs(a-cursor)<.001,'Timeline gap/overlap');cursor=b
    need(num(duration) and abs(cursor-duration)<.001,'Shot coverage mismatch')
    if data.get('four_method_comparison') is True:
        need(not current,'The four-method comparison is historical compatibility only')
        need(set(method_sources)==set(LEGACY_METHODS),'Historical comparison must contain all four legacy methods');owners={}
        for method,signatures in method_sources.items():
            for sig in signatures:
                need(sig not in owners or owners[sig]==method,f'{method}: same mechanism sources reused as another method');owners[sig]=method
    if data.get('three_style_comparison') is True:
        need(False,'Use a separate authored plan per current style; compare their reviewed exports')
    if stage=='proof':need(data.get('proof',{}).get('plan_sha256')==plan_digest(data),'Proof missing/stale for this plan revision')
    return errors

def validate(data,root,stage='assets'):
    """Standard gate: base provenance plus any mandatory method-specific gate."""
    errors=validate_base(data,root,stage)
    shots=data.get('shots') if isinstance(data,dict) else None
    if uses_current_catalog(data):
        from motion_detail import validate as validate_choices
        errors.extend(validate_choices(data,root,stage))
        version=tuple(map(int,re.findall(r'\d+',str(data.get('release_version','0.0.0')))))
        if version >= (4,9,1):
            from validate_title_timing import validate as validate_titles
            errors.extend(validate_titles(data))
        try:
            from validate_style_profile import validate as validate_style_profile
        except ImportError:
            errors.append('Style profile: required validator is unavailable; restore the complete project scripts before rendering')
        else:
            errors.extend(validate_style_profile(data,root,stage))
        from validate_living_frames import validate as validate_living_frames
        errors.extend(validate_living_frames(data,root,stage))
        from validate_environment_plan import validate as validate_environment
        errors.extend(validate_environment(data,root,stage))
    elif isinstance(shots,list) and any(isinstance(shot,dict) and shot.get('method')=='living-ink' for shot in shots):
        try:
            from validate_living_ink import validate as validate_living_ink
        except ImportError:
            errors.append('Living Ink: required validator is unavailable; restore the complete project scripts before rendering')
        else:
            errors.extend(validate_living_ink(data,root,stage))
    if uses_current_catalog(data) and (data.get('release_version') not in {'4.0.0','4.1.0','4.1.1'} or data.get('physics_contract')):
        try:
            from validate_physics import validate as validate_physics
        except ImportError:
            errors.append('Physics: required validator unavailable; restore bundled scripts before final render')
        else:
            errors.extend(validate_physics(data,root,stage))
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--stage',choices=['assets','proof'],default='assets');p.add_argument('--digest',action='store_true',help='Print digest; does not approve or mark a review');a=p.parse_args()
    try:
        d=json.loads(a.plan.read_text())
        if a.digest:print(plan_digest(d));return
        errors=validate(d,a.plan.resolve().parent,a.stage)
    except (OSError,ValueError,TypeError,AttributeError,KeyError) as e:p.exit(2,f'Invalid plan: {e}\n')
    print(json.dumps({'ok':not errors,'stage':a.stage,'errors':errors,'limit':'Evidence/provenance checks only; inspect actual art, motion and approval.'},indent=2));raise SystemExit(bool(errors))
if __name__=='__main__':main()
