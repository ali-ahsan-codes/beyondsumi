#!/usr/bin/env python3
"""Create a local listening page from actual cached files. No API/network calls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import library


def build(root):
    data=library.manifest(root)
    def audition(entry):
        id=entry['id'];source=root/'music'/id/'preview.wav';dest=root/'music'/id/'audition.mp3'
        if not dest.exists():
            # Monitoring copy only. Source stems and film balance remain intact.
            subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-af',
                            'loudnorm=I=-20:TP=-2:LRA=9','-ar','48000','-c:a','libmp3lame','-b:a','160k',str(dest)],check=True)
        return {'id':id,'file':str(dest.relative_to(root)),'sha256':library.sha(dest),
                'source_sha256':library.sha(source),'purpose':'level-adjusted audition only; source stems unchanged'}
    with ThreadPoolExecutor(max_workers=4) as executor:
        copies=list(executor.map(audition,data['music'].values()))
    library.save(root/'AUDITION-COPIES.json',copies)
    cards=[]
    for entry in data['music'].values():
        cards.append({'type':'music','id':entry['id'],'title':entry['name'],'category':entry['id'],
                      'seconds':round(entry['duration'],2),'audio':'music/'+entry['id']+'/audition.mp3',
                      'download':'music/'+entry['id']+'/preview.wav','review':entry['review'],
                      'detail':'Python composition · harmony, melody and rhythm parts · audition level adjusted'})
    for entry in data['sfx'].values():
        cards.append({'type':'sfx','id':entry['id'],'title':entry['id'].replace('-',' ').title(),'category':entry['category'],
                      'seconds':round(entry['duration'],2),'audio':entry['file'],'download':entry['file'],
                      'review':entry['review'],'detail':'Cached ElevenLabs source · no API needed for playback or reuse'})
    library.save(root/'audition-data.json',cards)
    # Safe JSON embedding: replacing < prevents accidental script-end injection.
    encoded=json.dumps(cards,ensure_ascii=False).replace('<','\\u003c')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sumi Sound Library · Beyondsumi</title><style>
:root{color-scheme:light;--paper:#f4f1e9;--ink:#252321;--muted:#6d6a64;--red:#8d302d}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:36px 28px 64px}header{border-bottom:1px solid #cec8bd;padding-bottom:32px}nav{display:flex;justify-content:space-between;gap:20px;align-items:center}.brand{font-family:Georgia,serif;font-size:28px;letter-spacing:-1px}nav span:last-child,.eyebrow{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--red)}h1{font:clamp(42px,7vw,80px)/1.05 Georgia,serif;max-width:850px;letter-spacing:-2px;margin:38px 0 20px}p{max-width:750px;color:var(--muted)}.stats{font-size:14px;font-weight:600}.tools{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:30px 0 22px}button,input{font:inherit;border:1px solid #bdb6aa;border-radius:6px;padding:10px 15px;background:transparent;color:var(--ink)}button{cursor:pointer}button.active{background:var(--ink);border-color:var(--ink);color:var(--paper)}input{min-width:230px;flex:1}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:18px}.card{background:#fffdf7;border:1px solid #d9d3c8;border-radius:12px;padding:22px;display:flex;flex-direction:column;min-height:270px}.tag{font-size:10px;text-transform:uppercase;letter-spacing:1.6px;color:var(--red)}h2{font:26px/1.2 Georgia,serif;margin:10px 0}small{color:var(--muted);font-size:12px}.card p{font-size:13px;margin:14px 0;min-height:40px}.card audio{width:100%;height:42px;margin-top:auto}.bottom{display:flex;align-items:center;justify-content:space-between;margin-top:15px;font-size:12px;gap:10px}a{color:var(--red);text-underline-offset:4px}.pending{border:1px solid #ddd6c9;border-radius:20px;padding:4px 9px;color:var(--muted)}footer{border-top:1px solid #cec8bd;margin-top:40px;padding-top:20px;color:var(--muted);font-size:13px}.empty{padding:40px}audio:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #b36e60;outline-offset:3px}@media(max-width:600px){main{padding:24px 18px}nav span:last-child{display:none}h1{letter-spacing:-1px}}
</style><main><header><nav><span class="brand">Beyondsumi ／ Sound</span><span>A local listening room</span></nav><div class="eyebrow" style="margin-top:40px">The first collection</div><h1>A sound for the story.</h1><p>Original Python music and a reusable collection of custom effects. Listen, compare and tell your agent which sounds fit. New assets remain pending until auditioned; this page never spends credits.</p><div class="stats" id="stats"></div></header><div class="tools"><button class="active" data-filter="all">All sounds</button><button data-filter="music">12 mood themes</button><button data-filter="sfx">32 effects</button><input id="search" type="search" aria-label="Search sounds" placeholder="Search a mood, material or action"></div><section class="grid" id="grid" aria-label="Sound previews"></section><footer>Music previews are level-adjusted for listening. Original WAVs and editable parts keep their source levels. Effect WAVs preserve the generated source level. Film loudness, contact timing and loop joins need their own review. Local only · no models · no playback API calls.</footer></main><script>
const items=__DATA__;let filter='all';const grid=document.getElementById('grid');const search=document.getElementById('search');
document.getElementById('stats').textContent=`${items.filter(x=>x.type==='music').length} original mood themes · ${items.filter(x=>x.type==='sfx').length} cached effects · 48 kHz WAV library`;
function draw(){grid.querySelectorAll('audio').forEach(audio=>audio.pause());grid.replaceChildren();const query=search.value.toLowerCase();for(const item of items){if(filter!=='all'&&item.type!==filter)continue;if(![item.id,item.title,item.category].join(' ').toLowerCase().includes(query))continue;const card=document.createElement('article');card.className='card';const tag=document.createElement('div');tag.className='tag';tag.textContent=item.type==='music'?'Original music · '+item.category:'Sound effect · '+item.category;const title=document.createElement('h2');title.textContent=item.title;const meta=document.createElement('small');meta.textContent=item.seconds+' seconds';const detail=document.createElement('p');detail.textContent=item.detail;const audio=document.createElement('audio');audio.controls=true;audio.preload='none';audio.src=item.audio;audio.setAttribute('aria-label','Listen to '+item.title);const bottom=document.createElement('div');bottom.className='bottom';const status=document.createElement('span');status.className='pending';status.textContent=item.review==='approved'?'Audition approved':'Pending audition';const link=document.createElement('a');link.href=item.download;link.download='';link.textContent='Download WAV ↗';bottom.append(status,link);card.append(tag,title,meta,detail,audio,bottom);grid.append(card)}if(!grid.children.length){const empty=document.createElement('p');empty.className='empty';empty.textContent='No sounds match this search.';grid.append(empty)}}
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{filter=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.classList.toggle('active',b===button));draw()}));search.addEventListener('input',draw);document.addEventListener('play',event=>{document.querySelectorAll('audio').forEach(audio=>{if(audio!==event.target)audio.pause()})},true);draw();
</script></html>'''
    (root/'index.html').write_text(page.replace('__DATA__',encoded))
    return {'music':len(data['music']),'sfx':len(data['sfx']),'page':str((root/'index.html').resolve()),'automatic_approval':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True,type=Path);a=p.parse_args()
    print(json.dumps(build(a.root),indent=2))
