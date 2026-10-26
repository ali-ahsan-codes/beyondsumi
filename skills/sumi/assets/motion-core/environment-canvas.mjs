/** Local environment pass for baked environment_motion.py states.
 * Draw under the same scene/world transform as the artwork, before titles.
 * Raster masks/layers are passed in assets by path. No automatic segmentation.
 */
import {drawBoundedPatch} from './living-frame-canvas.mjs';
const cache=new WeakMap();
const make=(w,h)=>{const a=typeof OffscreenCanvas==='function'?new OffscreenCanvas(w,h):document.createElement('canvas');a.width=w;a.height=h;return a;};
const localRandom=(n,seed)=>{let x=(Math.imul(n,374761393)+Math.imul(seed,668265263))>>>0;x=Math.imul(x^(x>>>13),1274126177)>>>0;return ((x^(x>>>16))>>>0)/4294967295;};
export function particlePositions(s){
 const [x0,y0,x1,y1]=s.bounds,w=x1-x0,h=y1-y0,count=s.count??18,seed=s.seed??7,velocity=s.velocity??[3,-2],depth=s.depth_scale??1,t=s.time;
 return Array.from({length:count},(_,i)=>{
  const life=3+localRandom(i+80,seed)*5,clock=t+localRandom(i+90,seed)*life,cycle=Math.floor(clock/life),age=clock-cycle*life,fade=Math.sin(Math.PI*age/life)**2;
  const tx=Math.max(-w*.7,Math.min(w*.7,velocity[0]*life*depth)),ty=Math.max(-h*.7,Math.min(h*.7,velocity[1]*life*depth));
  const x=Math.max(1,Math.min(w-1,localRandom(i*2+cycle*7919,seed)*(w-Math.abs(tx))+Math.max(0,-tx)+tx*age/life));
  const y=Math.max(1,Math.min(h-1,localRandom(i*2+1+cycle*7919,seed)*(h-Math.abs(ty))+Math.max(0,-ty)+ty*age/life));
  return {x:x0+x,y:y0+y,alpha:fade,radius:(s.radius??1.2)*(.6+localRandom(i+60,seed)*.8)};
 });
}
export function patchDisplacement(s,x,y){
 const [x0,y0,x1,y1]=s.bounds,u=(x-x0)/(x1-x0),v=(y-y0)/(y1-y0);
 if(u<=0||u>=1||v<=0||v>=1)return [0,0];
 const edge=Math.sin(Math.PI*u)**2*Math.sin(Math.PI*v)**2;
 // The flame base stays fixed; ripple/cloth/texture also have fixed borders.
 const taper=s.kind==='flame'?(1-v):1;
 return [s.dx*edge*taper,s.dy*edge*taper];
}
function surface(c,w,h){
 let a=cache.get(c);if(!a){a=make(w,h);cache.set(c,a);}if(a.width!==w)a.width=w;if(a.height!==h)a.height=h;return a;
}
export function textureWindow(im,s,w,h){
 const sx=(im.width-w)/2-s.dx,sy=(im.height-h)/2-s.dy;
 if(sx<0||sy<0||sx+w>im.width||sy+h>im.height)throw Error('Environment layer needs more overscan');
 return [sx,sy,w,h];
}
export function drawEnvironmentPass(c,source,state,pass,{width=1920,height=1080,assets=new Map(),protectedRegions=[]}={}){
 for(const s of state.effects){
  if(s.pass!==pass)continue;
  const [x0,y0,x1,y1]=s.bounds,w=Math.ceil(x1-x0),h=Math.ceil(y1-y0),layer=surface(c,w,h),lc=layer.getContext('2d');
  lc.setTransform(1,0,0,1,0,0);lc.clearRect(0,0,w,h);lc.save();lc.translate(-x0,-y0);
  if(['flame','cloth','ripple','texture'].includes(s.kind)){
   const bounds=[(x0+x1)/2,(y0+y1)/2,w/2,h/2];
   drawBoundedPatch(lc,source,bounds,(x,y)=>patchDisplacement(s,x,y),{width,height});
  }else if(['parallax','cloud','painted_atmosphere'].includes(s.kind)){
   const im=assets.get(s.layer.path);if(!im)throw Error('Missing environment layer');
   if(s.kind!=='painted_atmosphere'){const plate=assets.get(s.clean_plate.path);if(!plate)throw Error('Missing clean plate');lc.drawImage(plate,0,0,width,height);}
   const [sx,sy]=textureWindow(im,s,w,h);
   lc.globalAlpha=s.kind==='painted_atmosphere'?1:(s.layer_opacity??1)*s.envelope;lc.drawImage(im,sx,sy,w,h,x0,y0,w,h);lc.globalAlpha=1;
  }else if(['light','shadow','reflection'].includes(s.kind)){
   const cx=(x0+x1)/2+s.dx,cy=(y0+y1)/2+s.dy;
   lc.save();lc.translate(cx,cy);lc.scale(w/2,h/2);const g=lc.createRadialGradient(0,0,0,0,0,1);
   g.addColorStop(0,s.color??(s.kind==='shadow'?'#13121b':'#f4c57e'));g.addColorStop(1,(s.color??(s.kind==='shadow'?'#13121b':'#f4c57e'))+'00');lc.fillStyle=g;lc.fillRect(-1,-1,2,2);lc.restore();
  }else if(['haze','smoke','cloud'].includes(s.kind)){
   for(let i=0;i<4;i++){
    const cx=x0+w*(.18+i*.21)+s.dx,cy=y0+h*(.35+.17*Math.sin(i*2.3))+s.dy;
    lc.save();lc.translate(cx,cy);lc.scale(w*.34,h*.48);const g=lc.createRadialGradient(0,0,0,0,0,1);const color=s.color??'#c1c1ce';g.addColorStop(0,color);g.addColorStop(1,color+'00');lc.fillStyle=g;lc.fillRect(-1,-1,2,2);lc.restore();
   }
  }else{
   lc.fillStyle=s.color??'#e8dfcd';lc.strokeStyle=s.color??'#c1c5cf';lc.lineWidth=s.kind==='rain'?.7:1;
   for(const p of particlePositions(s)){
    lc.globalAlpha=p.alpha;
    if(s.kind==='rain'){lc.beginPath();lc.moveTo(p.x,p.y);lc.lineTo(p.x+s.dx*.02,p.y+8*(s.depth_scale??1));lc.stroke();}
    else{lc.beginPath();lc.arc(p.x,p.y,p.radius,0,Math.PI*2);lc.fill();}
   }
  }
  lc.restore();lc.globalAlpha=1;
  if(s.mask){const mask=assets.get(s.mask.path);if(!mask)throw Error('Missing environment mask');lc.globalCompositeOperation='destination-in';lc.drawImage(mask,0,0,w,h);lc.globalCompositeOperation='source-over';}
  for(const r of protectedRegions){
   if(r.role==='character'&&s.affects_character&&['light','shadow','reflection'].includes(s.kind))continue;
   const b=r.bounds;lc.clearRect(b[0]-x0,b[1]-y0,b[2]-b[0],b[3]-b[1]);
  }
  c.save();c.globalAlpha=['flame','cloth','ripple','texture','parallax','cloud'].includes(s.kind)?1:Math.min(.45,s.alpha);c.globalCompositeOperation=s.kind==='shadow'?'multiply':s.kind==='light'||s.kind==='reflection'?'screen':'source-over';if(s.kind==='flame')c.filter=`brightness(${1+s.signal*.22*s.strength})`;c.drawImage(layer,x0,y0);c.restore();
 }
}
