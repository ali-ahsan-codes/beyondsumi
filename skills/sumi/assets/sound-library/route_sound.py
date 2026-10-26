#!/usr/bin/env python3
"""Library-first sound selection with local Python fallback; never calls a provider."""
import argparse,copy,hashlib,json,os,re,shutil,sys
from pathlib import Path
import library
import original_sfx

HERE=Path(__file__).resolve().parent

def checked_id(value):
    if not isinstance(value,str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',value):raise ValueError('Sound ID must be a short lowercase identifier')
    return value

def copy_record(root,record,target,kind):
    item=copy.deepcopy(record)
    files=item['files'] if kind=='music' else {item['file']:item['sha256']}
    for relative,digest in files.items():
        source=library.asset(root,relative,digest);dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            if library.sha(dest)!=digest:raise ValueError('Conflicting cached source')
        else:shutil.copy2(source,dest)
    return item

def prepare(plan,out,library_root=None,music_root=None,mode='library-first',elevenlabs_available=False,missing_action='ask'):
    if mode not in {'library-first','python-only'}:raise ValueError('Choose library-first or python-only')
    if out.exists():raise ValueError('Preserve previous selection; choose a new output directory')
    if not isinstance(plan,dict) or not isinstance(plan.get('cues'),list):raise ValueError('Sound cue plan required')
    cues=copy.deepcopy(plan['cues'])
    for cue in cues:
        checked_id(cue.get('id'))
        if cue.get('type') not in {'music','sfx'}:raise ValueError('Sound cue type must be music or sfx')
    if missing_action not in {'ask','python'}:raise ValueError('Choose ask or python for a missing effect')
    out.mkdir(parents=True);bank=out/'bank'
    prepared={'schema':'sumi-local-sound-bank-v1','music':{},'sfx':{},'sensory_review':'pending'}
    # Pure-Python does not even inspect the private/provider library.
    external=library.manifest(library_root) if mode=='library-first' and library_root else {'music':{},'sfx':{}}
    if music_root is None:
        music_root=HERE/'bundled-bank'
        location=HERE/'library-location.json'
        if not (music_root/'library.json').exists() and location.exists():
            music_root=Path(json.loads(location.read_text())['bundled_music_root'])
    builtin=library.manifest(music_root) if mode=='library-first' else {'music':{},'sfx':{}}
    definitions={x['id']:x for x in original_sfx.definitions(library.catalog())}
    # An available paid service is the second preference, not permission to bill it.
    # Resolve this choice before copying/synthesizing a dependent media batch.
    missing=[];prompts={x['id']:x for x in library.catalog()['sfx']}
    if mode=='library-first' and elevenlabs_available and missing_action=='ask':
        for cue in cues:
            if cue['type']!='sfx' or cue.get('source_policy')=='python':continue
            item=external.get('sfx',{}).get(cue['id'])
            if item and item.get('review')!='rejected':continue
            spec=prompts.get(cue['id'],{})
            missing.append({'id':cue['id'],'prompt':cue.get('description') or spec.get('prompt') or cue['id'].replace('-',' '),'duration_seconds':cue.get('python_duration',spec.get('duration_seconds',2))})
    if missing:
        report={'status':'needs_sound_choice','mode':mode,'priority':['sound-library','ElevenLabs if connected and explicitly approved','Python synthesis'],'missing_effects':missing,'provider_calls':0,'model_downloads':0,'next_step':'Show script-specific ElevenLabs SFX estimate and ask Generate with ElevenLabs or Use Python. Connection alone never authorizes charges. Reuse/import completed approved effects, or rerun with missing-action python.'}
        library.save(out/'NEXT-ACTIONS.json',report);return report
    bank.mkdir()
    ledger=[]
    for index,cue in enumerate(cues):
        kind,id=cue['type'],cue['id'];force=mode=='python-only' or cue.get('source_policy')=='python'
        selected=None;source_root=None
        if not force:
            for root,data in [(library_root,external),(music_root,builtin)]:
                item=data.get(kind,{}).get(id)
                if root and item and item.get('review')!='rejected':selected=item;source_root=root;break
        if selected:
            prepared[kind][id]=copy_record(source_root,selected,bank,kind)
            ledger.append({'cue':index,'requested_id':id,'selected_id':id,'route':'library','source':selected.get('source'),'review':selected.get('review','pending')})
        elif kind=='music':
            library.save(bank/'library.json',prepared);library.build_music(bank,[id]);prepared=library.manifest(bank)
            ledger.append({'cue':index,'requested_id':id,'selected_id':id,'route':'python-composition','review':'pending'})
        else:
            renderer=cue.get('python_kind',id);checked_id(renderer)
            if renderer not in definitions:raise ValueError('No suitable saved effect or Python design for '+id+'. Author an effect or supply licensed audio; no automatic API call.')
            spec=copy.deepcopy(definitions[renderer]);spec['duration_seconds']=cue.get('python_duration',spec['duration_seconds'])
            if isinstance(spec['duration_seconds'],bool) or not isinstance(spec['duration_seconds'],(int,float)) or not .05<=spec['duration_seconds']<=20:raise ValueError('Python effect duration must be0.05..20seconds')
            seed=cue.get('python_seed',20261026+index*113)
            if not isinstance(seed,int) or isinstance(seed,bool):raise ValueError('Python seed must be integer')
            key=id[:38]+'-py-'+hashlib.sha256(json.dumps([spec,seed],sort_keys=True).encode()).hexdigest()[:12]
            sound=original_sfx.render(spec,seed);relative='sfx/'+key+'.wav';dest=bank/relative;dest.parent.mkdir(exist_ok=True)
            library.write_wav(dest,sound)
            prepared['sfx'][key]={'id':key,'category':spec['category'],'duration':len(sound[0])/library.SR,'loop_requested':spec['loop'],'file':relative,'sha256':library.sha(dest),'source':'original Python synthesis','source_sha256':library.sha(HERE/'original_sfx.py'),'seed':seed,'review':'pending','contact_anchor_seconds':None,'contact_candidate_seconds':None,'loop_review':'pending' if spec['loop'] else 'not_applicable','measurements':library.metrics(sound)}
            cue['id']=key;ledger.append({'cue':index,'requested_id':id,'selected_id':key,'route':'python-synthesis','design':renderer,'review':'pending'})
    library.save(bank/'library.json',prepared)
    resolved=copy.deepcopy(plan);resolved['cues']=cues;library.save(out/'resolved-plan.json',resolved)
    report={'mode':mode,'cues':ledger,'provider_calls':0,'model_downloads':0,'new_dependency_installs':0,'private_library_inspected':mode=='library-first' and library_root is not None,'sound_library_separate_from_engine':True,'listening_certified':False,'notes':'Pending assets/anchors remain pending. Use explicit review drafts for audition; do not invent approvals.'}
    library.save(out/'ROUTING.json',report);return report

def configured_library():
    """Read only the user's non-secret selected cache path, never credentials."""
    if os.environ.get('SUMI_SOUND_LIBRARY'):return Path(os.environ['SUMI_SOUND_LIBRARY']).expanduser()
    if os.environ.get('SUMI_STATE_DIR'):state=Path(os.environ['SUMI_STATE_DIR']).expanduser()
    elif sys.platform=='darwin':state=Path.home()/'Library/Application Support/Sumi'
    elif os.name=='nt':state=Path(os.environ.get('APPDATA',str(Path.home()/'AppData/Roaming')))/'Sumi'
    else:state=Path(os.environ.get('XDG_CONFIG_HOME',str(Path.home()/'.config')))/'sumi'
    path=state/'user.json'
    if not path.exists():return None
    data=json.loads(path.read_text());value=data.get('preferences',{}).get('sound_library_path',{}).get('value')
    return Path(value).expanduser() if isinstance(value,str) and value.strip() else None

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['prepare','render']);p.add_argument('--plan',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--library-root',type=Path);p.add_argument('--music-root',type=Path);p.add_argument('--mode',choices=['library-first','python-only'],default='library-first');p.add_argument('--review-draft',action='store_true');p.add_argument('--elevenlabs-available',action='store_true',help='Use only after the host verifies the selected connection supports SFX; does not authorize generation.');p.add_argument('--missing-action',choices=['ask','python'],default='ask');a=p.parse_args()
    root=(a.library_root or configured_library()) if a.mode=='library-first' else None
    try:
        report=prepare(json.loads(a.plan.read_text()),a.out,root,a.music_root,a.mode,a.elevenlabs_available,a.missing_action)
        if report.get('status')=='needs_sound_choice':
            print(json.dumps(report,indent=2));raise SystemExit(3)
        if a.action=='render':report['render']=library.render_plan(a.out/'bank',json.loads((a.out/'resolved-plan.json').read_text()),a.out/'mix',a.review_draft)
        print(json.dumps(report,indent=2))
    except (OSError,ValueError,KeyError,TypeError) as e:p.exit(1,f'Sound selection stopped: {e}\n')
if __name__=='__main__':main()
