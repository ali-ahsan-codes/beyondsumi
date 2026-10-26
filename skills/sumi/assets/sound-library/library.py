#!/usr/bin/env python3
"""Model-free local music library, cached SFX preparation and frame-timed mixing.

All rendering is offline. ElevenLabs acquisition is a separate explicit tool.
No dependency installation, credential access or network code in this module.
"""
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import wave
import music

SR = 48000
HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(path)


def number(x, low, high, name):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not low <= x <= high:
        raise ValueError(name+' must be finite in '+str((low,high)))
    return x


def read_wav(path):
    with wave.open(str(path),'rb') as f:
        if (f.getframerate(),f.getsampwidth(),f.getnchannels(),f.getcomptype()) != (SR,2,2,'NONE'):
            raise ValueError('Library audio must be 48kHz/16bit/stereo PCM: '+str(path))
        n=f.getnframes();raw=f.readframes(n)
    samples=array('h',raw)
    if sys.byteorder!='little':samples.byteswap()
    if len(samples)!=2*n:raise ValueError('Truncated WAV')
    return [array('f',(v/32768 for v in samples[c::2])) for c in range(2)]


def metrics(stereo, gain=1):
    n=sum(len(c) for c in stereo)
    peak=max((abs(v) for c in stereo for v in c),default=0)*gain
    rms=math.sqrt(sum(v*v for c in stereo for v in c)/max(1,n))*gain
    return {'peak_dbfs':20*math.log10(peak) if peak else None,
            'rms_dbfs':20*math.log10(rms) if rms else None,'silent':peak==0}


def write_wav(path, stereo, gain=1):
    pcm=array('h')
    for a,b in zip(*stereo):
        for value in (a,b):
            scaled=round(value*gain*32767)
            if abs(scaled)>32767:raise ValueError('Unsafe sample peak; attenuate all stems first')
            pcm.append(scaled)
    if sys.byteorder!='little':pcm.byteswap()
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())


def catalog():
    return json.loads((HERE/'catalog.json').read_text())


def manifest(root):
    p=root/'library.json'
    return json.loads(p.read_text()) if p.exists() else {'schema':'sumi-local-sound-bank-v1','music':{},'sfx':{},'sensory_review':'pending'}


def asset(root, relative, expected=None):
    path=(root/relative).resolve()
    if root.resolve() not in path.parents or not path.is_file():raise ValueError('Missing or outside-library asset')
    if expected and sha(path)!=expected:raise ValueError('Stale/changed library asset')
    return path


def build_music(root, ids=None):
    data=manifest(root);root.mkdir(parents=True,exist_ok=True)
    profiles=catalog()['music'];known={p['id'] for p in profiles}
    if ids and not set(ids)<=known:raise ValueError('Unknown music mood')
    results=[]
    for index, profile in enumerate(profiles):
        id=profile['id']
        if ids and id not in ids:continue
        folder=root/'music'/id
        if folder.exists():
            prior=data['music'].get(id)
            if not prior:raise ValueError('Unregistered music output exists; do not overwrite')
            if prior.get('source_hash')!=sha(HERE/'music.py') or prior.get('catalog_sha256')!=sha(HERE/'catalog.json'):
                raise ValueError('Composition code/recipe changed; preserve the old music and use a new library revision')
            for rel, digest in prior['files'].items():asset(root,rel,digest)
            results.append({'id':id,'action':'reused'});continue
        stems, score=music.compose(profile,seed=20261024+index*101)
        mixed=[array('f',(a+b+c for a,b,c in zip(stems['harmony'][ch],stems['melody'][ch],stems['rhythm'][ch]))) for ch in range(2)]
        peak=max(abs(x) for c in mixed for x in c)
        gain=min(1,10**(-10/20)/peak) if peak else 1
        folder.mkdir(parents=True)
        for name, sound in [*stems.items(),('preview',mixed)]:write_wav(folder/(name+'.wav'),sound,gain)
        save(folder/'score.json',score)
        entry={'id':id,'name':profile['name'],'duration':score['duration'],'body_seconds':score['metrical_body_seconds'],
               'source':'original Python composition','review':'pending','source_hash':sha(HERE/'music.py'),
               'catalog_sha256':sha(HERE/'catalog.json'),'measurements':metrics(mixed,gain),
               'files':{str(p.relative_to(root)):sha(p) for p in sorted(folder.glob('*'))}}
        data['music'][id]=entry;save(root/'library.json',data)
        results.append({'id':id,'action':'created','duration':score['duration']})
        print(json.dumps(results[-1]),flush=True)
    return results


def import_effects(root, source, ffmpeg='ffmpeg'):
    data=manifest(root);results=[]
    for entry in catalog()['sfx']:
        id=entry['id'];receipt=source/'receipts'/(id+'.json');raw=source/'originals'/(id+'.mp3')
        if not receipt.exists():continue
        generation=json.loads(receipt.read_text())
        if generation.get('status')!='complete':raise ValueError('Uncertain or failed source: '+id)
        if not raw.is_file() or sha(raw)!=generation['audio_sha256']:raise ValueError('Raw source hash mismatch: '+id)
        relative='sfx/'+id+'.wav';dest=root/relative
        if dest.exists():
            old=data['sfx'].get(id,{})
            if old.get('source_sha256')!=sha(raw) or old.get('sha256')!=sha(dest):raise ValueError('Changed existing effect; create a revision')
            results.append({'id':id,'action':'reused'});continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        temp=dest.with_suffix('.preparing.wav')
        # Preserve the source level; do not normalize every effect to full loudness.
        subprocess.run([ffmpeg,'-v','error','-n','-i',str(raw),'-ar',str(SR),'-ac','2','-c:a','pcm_s16le',str(temp)],check=True)
        stereo=read_wav(temp);m=metrics(stereo)
        if m['silent']:raise ValueError('Silent provider output; preserve and review instead of retrying')
        peak=max(abs(v) for c in stereo for v in c)
        threshold=max(.002,peak*.08)
        candidate=next((i for i,(a,b) in enumerate(zip(*stereo)) if max(abs(a),abs(b))>=threshold),None)
        temp.replace(dest)
        data['sfx'][id]={'id':id,'category':entry['category'],'duration':len(stereo[0])/SR,'loop_requested':entry['loop'],
                         'file':relative,'sha256':sha(dest),'source_sha256':sha(raw),
                         'source':'ElevenLabs '+catalog()['provider']['model_id'],'receipt':str(receipt.resolve()),
                         'measurements':m,'contact_candidate_seconds':candidate/SR if candidate is not None else None,
                         'contact_anchor_seconds':None,'review':'pending','loop_review':'pending' if entry['loop'] else 'not_applicable'}
        save(root/'library.json',data);results.append({'id':id,'action':'prepared','duration':len(stereo[0])/SR})
    return results


def envelope(ducks,n,fps,stem):
    result=array('f',[1])*n
    for d in ducks:
        if stem not in d.get('stems',['music']):continue
        start=number(d['start_frame'],0,n/SR*fps,'duck start')/fps
        end=number(d['end_frame'],0,n/SR*fps,'duck end')/fps
        if end<=start:raise ValueError('Invalid duck interval')
        gain=number(d.get('gain',.35),0,1,'duck gain')
        attack=number(d.get('attack',.08),.001,5,'attack');release=number(d.get('release',.25),.001,5,'release')
        for i in range(max(0,int((start-attack)*SR)),min(n,math.ceil((end+release)*SR))):
            t=i/SR;w=min(1,max(0,(t-start+attack)/attack),max(0,(end+release-t)/release))
            result[i]=min(result[i],1-(1-gain)*w)
    return result


def render_plan(root, plan, out, review_draft=False):
    if out.exists():raise ValueError('Use a new output directory')
    fps=number(plan['fps'],1,120,'fps');total=number(plan['duration_frames'],1,21600,'duration_frames')
    if not isinstance(total,int):raise ValueError('Duration frames must be an integer')
    duration=number(total/fps,.1,180,'section duration');n=round(duration*SR)
    data=manifest(root);buses={name:[array('f',[0])*n,array('f',[0])*n] for name in ('music','sfx','ambience')}
    ledger=[];unreviewed=set()
    for cue in plan['cues']:
        kind=cue['type'];id=cue['id']
        if kind not in ('music','sfx'):raise ValueError('Unknown cue type')
        item=data[kind][id]
        if item['review']!='approved':
            unreviewed.add(kind+':'+id)
            if not review_draft:raise ValueError('Audition pending: '+id+'; explicit review draft required')
        at_frame=number(cue['at_frame'],0,total,'cue frame')
        if not isinstance(at_frame,int):raise ValueError('Cue frame must be an integer')
        at=round(at_frame/fps*SR)
        gain=number(cue.get('gain',.4 if kind=='music' else .5),0,2,'cue gain')
        pan=number(cue.get('pan',0),-1,1,'pan');gl=math.cos((pan+1)*math.pi/4)*math.sqrt(2);gr=math.sin((pan+1)*math.pi/4)*math.sqrt(2)
        if kind=='music':
            allowed={'harmony','melody','rhythm'};parts=cue.get('parts',sorted(allowed))
            if not parts or len(set(parts))!=len(parts) or not set(parts)<=allowed:raise ValueError('Invalid music parts')
            sounds=[]
            for part in parts:
                rel='music/'+id+'/'+part+'.wav';sounds.append(read_wav(asset(root,rel,item['files'][rel])))
            sound=[array('f',(sum(samples) for samples in zip(*(s[c] for s in sounds)))) for c in range(2)]
            frames=number(cue['duration_frames'],1,total,'music cue frames')
            if not isinstance(frames,int):raise ValueError('Music cue frames must be an integer')
            length=round(frames/fps*SR)
            source_start=0;body=round(item['body_seconds']*SR)
            repeat=cue.get('repeat_body',False)
            if not repeat and length>len(sound[0]):raise ValueError('Music cue exceeds source; choose repetition or another section explicitly')
            bus='music'
        else:
            sound=read_wav(asset(root,item['file'],item['sha256']))
            # Contact positions must be auditioned. A preview can use the clearly labelled candidate.
            anchor=item.get('contact_anchor_seconds')
            if anchor is None:
                if not review_draft:raise ValueError('Contact anchor pending: '+id)
                anchor=item['contact_candidate_seconds'] or 0
            source_start=0;repeat=cue.get('repeat_body',False);body=len(sound[0])
            if repeat and not item.get('loop_requested'):raise ValueError('Only ambience requested as loops can repeat')
            if repeat and item.get('loop_review')!='approved' and not review_draft:raise ValueError('Loop join review pending')
            if repeat:
                frames=number(cue['duration_frames'],1,total,'loop frames')
                if not isinstance(frames,int):raise ValueError('Loop cue frames must be an integer')
                length=round(frames/fps*SR)
            else:
                length=len(sound[0]);at-=round(anchor*SR)
                if at<0:raise ValueError('Contact anchor requires more preroll; move cue or prepare a reviewed trimmed derivative')
            bus='ambience' if item['category']=='ambience' else 'sfx'
        if at+length>n:raise ValueError('Cue tail exceeds film; budget it explicitly')
        fade_in=number(cue.get('fade_in',.25 if kind=='music' or repeat else .003),0,length/SR,'fade_in')*SR
        fade_out=number(cue.get('fade_out',.5 if kind=='music' or repeat else .015),0,length/SR,'fade_out')*SR
        for i in range(length):
            source_i=i%body if repeat else source_start+i
            edge=min(1,i/fade_in if fade_in else 1,(length-1-i)/fade_out if fade_out else 1)
            if repeat:
                # A 5 ms safety ramp avoids waveform discontinuities. Artistic loop review remains required.
                phase=i%body;edge*=min(1,phase/240,(body-1-phase)/240)
            buses[bus][0][at+i]+=sound[0][source_i]*gain*gl*edge
            buses[bus][1][at+i]+=sound[1][source_i]*gain*gr*edge
        ledger.append({'id':id,'type':kind,'stem':bus,'requested_frame':at_frame,'source_start_seconds':at/SR,'end_seconds':(at+length)/SR,'repeated':repeat,'review':item['review']})
    for name,stereo in buses.items():
        duck=envelope(plan.get('ducks',[]),n,fps,name)
        for c in range(2):
            for i in range(n):stereo[c][i]*=duck[i]
    mixed=[array('f',(a+b+c for a,b,c in zip(buses['music'][ch],buses['sfx'][ch],buses['ambience'][ch]))) for ch in range(2)]
    peak=max(abs(v) for sound in (*buses.values(),mixed) for c in sound for v in c)
    ceiling=10**(number(plan.get('ceiling_db',-6),-30,-1,'ceiling')/20);scale=min(1,ceiling/peak) if peak else 1
    out.mkdir(parents=True)
    for name,sound in [*buses.items(),('background',mixed)]:write_wav(out/(name+'.wav'),sound,scale)
    report={'duration_seconds':n/SR,'fps':fps,'duration_frames':total,'sample_rate':SR,'sample_count':n,'shared_attenuation':scale,
            'stems':{k:metrics(v,scale) for k,v in buses.items()},'cues':ledger,'unreviewed_assets':sorted(unreviewed),
            'review_draft':review_draft,'listening_reviewed':False,'provider_calls':0,'model_downloads':0,
            'loudness_true_peak_measured':False,'plan_sha256':hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()}
    save(out/'report.json',report);save(out/'plan.json',plan);return report


def record_review(root, kind, id, reviewer, notes, anchor=None, loop_reviewed=False):
    """Record an actually performed audition; callers must not invent evidence."""
    if not reviewer.strip() or not notes.strip():raise ValueError('Actual reviewer and listening observations required')
    data=manifest(root);item=data[kind][id]
    if kind=='music':
        for rel,digest in item['files'].items():asset(root,rel,digest)
    else:
        asset(root,item['file'],item['sha256'])
        if anchor is None:raise ValueError('An auditioned effect needs a meaningful contact/onset anchor')
        number(anchor,0,item['duration'],'contact anchor')
        if anchor>=item['duration']:raise ValueError('Contact anchor must be inside the effect')
        item['contact_anchor_seconds']=anchor
        if loop_reviewed and not item.get('loop_requested'):raise ValueError('This source is not a loop')
        if loop_reviewed:item['loop_review']='approved'
    from datetime import datetime,timezone
    item['review']='approved';item['review_evidence']={'reviewer':reviewer,'notes':notes,'at':datetime.now(timezone.utc).isoformat(),
                                                       'source_hashes':item.get('files') or {item['file']:item['sha256']}}
    save(root/'library.json',data);return {'kind':kind,'id':id,'review':'approved'}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build-music');b.add_argument('--root',type=Path,required=True);b.add_argument('--only',nargs='+')
    i=sub.add_parser('import-sfx');i.add_argument('--root',type=Path,required=True);i.add_argument('--source',type=Path,required=True)
    r=sub.add_parser('render');r.add_argument('--root',type=Path,required=True);r.add_argument('--plan',type=Path,required=True);r.add_argument('--out',type=Path,required=True);r.add_argument('--review-draft',action='store_true')
    l=sub.add_parser('list');l.add_argument('--root',type=Path,required=True)
    v=sub.add_parser('record-review');v.add_argument('--root',type=Path,required=True);v.add_argument('--type',choices=['music','sfx'],required=True)
    v.add_argument('--id',required=True);v.add_argument('--reviewer',required=True);v.add_argument('--notes',required=True)
    v.add_argument('--anchor',type=float);v.add_argument('--loop-reviewed',action='store_true')
    a=p.parse_args()
    try:
        if a.command=='build-music':result=build_music(a.root,a.only)
        elif a.command=='import-sfx':result=import_effects(a.root,a.source)
        elif a.command=='render':result=render_plan(a.root,json.loads(a.plan.read_text()),a.out,a.review_draft)
        elif a.command=='record-review':result=record_review(a.root,a.type,a.id,a.reviewer,a.notes,a.anchor,a.loop_reviewed)
        else:result=manifest(a.root)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as error:p.error(str(error))

if __name__=='__main__':main()
