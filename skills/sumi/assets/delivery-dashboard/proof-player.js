'use strict';
const proof=window.SUMI_PROOF;
document.title=proof.title+' · ALI Animation';
document.getElementById('title').textContent=proof.title;
document.getElementById('before').textContent=proof.before_label;
document.querySelector('progress').max=proof.duration;
const proofImage=document.querySelector('.stage img');
proofImage.width=proof.preview_size[0];proofImage.height=proof.preview_size[1];
document.getElementById('details').textContent='Preview '+proof.preview_size.join(' × ')+' · '+proof.fps+' fps · '+proof.duration.toFixed(3)+' seconds. Download '+proof.source_size.join(' × ')+' MP4.';

const cache=new Map(), states=new Map();
function state(section){if(!states.has(section))states.set(section,{token:0,timer:0,url:null});return states.get(section);}
function stop(section,before=false,message='Stopped. Choose Play motion to replay.'){
  const s=state(section),image=section.querySelector('img');s.token++;clearInterval(s.timer);
  image.onload=null;image.onerror=null;image.src=before?image.dataset.before:image.dataset.after;
  if(s.url){URL.revokeObjectURL(s.url);s.url=null;}
  section.dataset.state=before?'before':'stopped';section.querySelector('.status').textContent=message;
  section.querySelector('progress').value=0;section.querySelector('[data-play]').disabled=false;
}
async function play(button){
  const section=button.closest('section'),s=state(section),image=section.querySelector('img');
  document.querySelectorAll('section').forEach(other=>{if(other!==section&&['playing','loading'].includes(other.dataset.state))stop(other);});
  stop(section,false,'Loading preview…');const token=s.token;
  section.dataset.state='loading';button.disabled=true;
  try{
    let blob=cache.get(image.dataset.motion);
    if(!blob){const response=await fetch(image.dataset.motion);if(!response.ok)throw Error('Preview unavailable');blob=await response.blob();cache.set(image.dataset.motion,blob);}
    if(s.token!==token)return;
    s.url=URL.createObjectURL(blob);
    image.onload=()=>{
      if(s.token!==token)return;
      image.onload=null;button.disabled=false;section.dataset.state='playing';
      const start=performance.now(),progress=section.querySelector('progress');
      section.querySelector('.status').textContent='Playing motion · normal speed';
      s.timer=setInterval(()=>{
        const elapsed=Math.min(window.SUMI_PROOF.duration,(performance.now()-start)/1000);progress.value=elapsed;
        section.querySelector('.status').textContent='Playing motion · normal speed · '+elapsed.toFixed(1)+' / '+window.SUMI_PROOF.duration.toFixed(1)+' s';
        if(elapsed===window.SUMI_PROOF.duration){clearInterval(s.timer);section.dataset.state='ended';section.querySelector('.status').textContent='Proof complete. Play again to compare.';}
      },100);
    };
    image.onerror=()=>stop(section,false,'Preview could not load. Download the MP4 below.');
    image.src=s.url;
  }catch(error){if(s.token===token)stop(section,false,'Preview could not load. Download the MP4 below.');}
}
