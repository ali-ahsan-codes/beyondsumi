import {TRANSITIONS} from "./catalog.mjs";
import {prepare} from "./fields.mjs";
const grid=document.querySelector("#grid"),slider=document.querySelector("#progress");
const play=document.querySelector("#play"),position=document.querySelector("#position");
let progress=.58,playing=false,last=0,elapsed=0;
const cards=[];
for(let i=0;i<TRANSITIONS.length;i++){
  const mode=TRANSITIONS[i],article=document.createElement("article");
  article.className="card";article.dataset.family=mode.family;
  const canvas=document.createElement("canvas");canvas.className="drawing";canvas.width=192;canvas.height=120;
  canvas.setAttribute("role","img");canvas.setAttribute("aria-label",`${mode.name}: ${mode.massGeometry}`);
  const body=document.createElement("div");body.className="card-body";
  body.innerHTML=`<div class="meta"><span>${String(i+1).padStart(2,"0")} · ${mode.family}</span><span>${mode.durationSeconds[0]}–${mode.durationSeconds[1]} s</span></div>
    <h2>${mode.name}</h2><p>${mode.reveal}</p><p class="use">${mode.storyUse}</p>
    <details><summary>Direction &amp; sound</summary><dl><dt>Visible cause</dt><dd>${mode.cause}</dd><dt>Material geometry</dt><dd>${mode.massGeometry}</dd><dt>Sound</dt><dd>${mode.sound.description}. Relative intensity ${Math.round(mode.sound.intensity*100)}% before final mix judgment.</dd></dl></details>`;
  article.append(canvas,body);grid.append(article);
  cards.push({article,canvas,context:canvas.getContext("2d"),mode,visible:true});
}
function paint(card){
  if(card.article.hidden)return;
  const {canvas,context,mode}=card,w=canvas.width,h=canvas.height;
  const field=prepare(mode.id,progress,w,h,1827);
  const image=context.createImageData(w,h);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const d=field.density(x+.5,y+.5),i=(y*w+x)*4,v=Math.round(255-d*232);
    image.data[i]=image.data[i+1]=image.data[i+2]=v;image.data[i+3]=255;
  }
  context.putImageData(image,0,0);canvas.dataset.progress=progress.toFixed(3);
}
function render(all=false){
  slider.value=String(Math.round(progress*1000));position.textContent=`${Math.round(progress*100)}%`;
  for(const card of cards)if(all||card.visible)paint(card);
}
const observer=new IntersectionObserver(entries=>{
  for(const entry of entries){const card=cards.find(c=>c.article===entry.target);card.visible=entry.isIntersecting;if(card.visible)paint(card)}
},{rootMargin:"180px"});
cards.forEach(c=>observer.observe(c.article));
function pause(){playing=false;play.textContent="Play all"}
play.onclick=()=>{
  playing=!playing;play.textContent=playing?"Pause":"Play all";
  elapsed=progress*3000;last=0;if(playing)requestAnimationFrame(tick);
};
document.querySelector("#restart").onclick=()=>{pause();progress=0;render(true)};
slider.oninput=()=>{pause();progress=Number(slider.value)/1000;render(true)};
document.querySelector("#family").onchange=event=>{
  const family=event.target.value;
  cards.forEach(c=>c.article.hidden=family!=="all"&&c.mode.family!==family);render(true);
};
function tick(now){
  if(!playing)return;
  if(last===0)last=now;
  if(now-last>=1000/12){
    elapsed+=Math.min(200,now-last);last=now;
    const cycle=elapsed%3700;progress=Math.min(1,cycle/3000);
    render(false);
  }
  requestAnimationFrame(tick);
}
render(true);
