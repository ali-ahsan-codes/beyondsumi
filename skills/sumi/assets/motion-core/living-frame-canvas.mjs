/** Local source-derived Canvas adapter. No segmentation/anatomy recognition.
 * Targets are authored per source: {id,behavior,bounds:[cx,cy,rx,ry],amplitude,phase,hz,dx,dy}.
 * Whole patch coverage and fixed borders expose no hidden pixels. Use a proper
 * clean plate/layer method instead when actual independent extraction is needed.
 */
export function characterClock(frame, outputFps=30, stateFps=20){
 if(!Number.isInteger(frame)||frame<0||!Number.isInteger(outputFps)||!Number.isInteger(stateFps)||stateFps<1||stateFps>outputFps)throw new RangeError('Invalid character clock');
 const state=Math.floor(frame*stateFps/outputFps);return {state,time:state/stateFps,startFrame:Math.ceil(state*outputFps/stateFps)};
}
export function motionValue(m,t){
 if(!Number.isFinite(t)||t<0)throw new RangeError('Invalid time');const amp=m.amplitude??1,phase=m.phase??0,hz=m.hz??(m.behavior==='breath'?.25:.48),tau=2*Math.PI;
 if(m.behavior==='breath')return amp*(1-Math.cos(tau*hz*t+phase))*.5;
 if(m.behavior==='hair'||m.behavior==='cloth')return amp*(.72*Math.sin(tau*hz*t+phase)+.28*Math.sin(tau*hz*.61*t+phase*1.7));
 throw new RangeError('This adapter supports authored hair/cloth/breath patches; use checked expression drawings/rigs for faces.');
}
export function displacement(m,x,y,t){
 const [cx,cy,rx,ry]=m.bounds,u=(x-cx+rx)/(2*rx),v=(y-cy+ry)/(2*ry);
 if(u<=0||u>=1||v<=0||v>=1)return [0,0];
 const w=Math.sin(Math.PI*u)**2*Math.sin(Math.PI*v)**2,a=motionValue(m,t);
 return [a*(m.dx??1)*w,a*(m.dy??0)*w];
}
export function validateTargets(targets,width,height,protectedRegions=[]){
 const errors=[];
 for(const m of targets){
  const b=m.bounds;
  if(!Array.isArray(b)||b.length!==4||!b.every(Number.isFinite)){errors.push(`${m.id}: invalid bounds`);continue;}
  const [cx,cy,rx,ry]=b;
  if(rx<=0||ry<=0||cx-rx<0||cy-ry<0||cx+rx>width||cy+ry>height)errors.push(`${m.id}: patch outside source`);
  if(!Number.isFinite(m.amplitude)||Math.abs(m.amplitude)>.10*Math.min(rx,ry))errors.push(`${m.id}: displacement too large for this micro-motion adapter`);
  for(const r of protectedRegions){const [x0,y0,x1,y1]=r.bounds;if(cx+rx>x0&&cx-rx<x1&&cy+ry>y0&&cy-ry<y1)errors.push(`${m.id}: overlaps protected ${r.id}`);}
 }
 return errors;
}
function triangle(c,im,s,d,width,height){
 const [p0,p1,p2]=s,[q0,q1,q2]=d,den=(p1[0]-p0[0])*(p2[1]-p0[1])-(p2[0]-p0[0])*(p1[1]-p0[1]);
 const a=((q1[0]-q0[0])*(p2[1]-p0[1])-(q2[0]-q0[0])*(p1[1]-p0[1]))/den;
 const b=((q1[1]-q0[1])*(p2[1]-p0[1])-(q2[1]-q0[1])*(p1[1]-p0[1]))/den;
 const cc=((p1[0]-p0[0])*(q2[0]-q0[0])-(p2[0]-p0[0])*(q1[0]-q0[0]))/den;
 const dd=((p1[0]-p0[0])*(q2[1]-q0[1])-(p2[0]-p0[0])*(q1[1]-q0[1]))/den;
 c.save();c.beginPath();const cx=(q0[0]+q1[0]+q2[0])/3,cy=(q0[1]+q1[1]+q2[1])/3;
 d.forEach((p,i)=>{const dx=p[0]-cx,dy=p[1]-cy,n=Math.hypot(dx,dy),x=p[0]+dx/n*.35,y=p[1]+dy/n*.35;i?c.lineTo(x,y):c.moveTo(x,y);});c.closePath();c.clip();c.transform(a,b,cc,dd,q0[0]-a*p0[0]-cc*p0[1],q0[1]-b*p0[0]-dd*p0[1]);c.drawImage(im,0,0,width,height);c.restore();
}
export function drawLivingFrame(c,im,targets,time,{width=1920,height=1080,grid=6}={}){
 if(!Number.isInteger(grid)||grid<2||grid>16)throw new RangeError('Grid must be2..16');
 c.drawImage(im,0,0,width,height);
 for(const m of targets)drawBoundedPatch(c,im,m.bounds,(x,y)=>displacement(m,x,y,time),{width,height,grid});
}
/** Reusable fixed-border local resampling. Caller supplies bounded displacement. */
export function drawBoundedPatch(c,im,bounds,move,{width=1920,height=1080,grid=6}={}){
 if(!Number.isInteger(grid)||grid<2||grid>16)throw new RangeError('Grid must be2..16');
 const [cx,cy,rx,ry]=bounds,src=[],dst=[];
 for(let j=0;j<=grid;j++){src[j]=[];dst[j]=[];for(let i=0;i<=grid;i++){
  const x=cx-rx+2*rx*i/grid,y=cy-ry+2*ry*j/grid,[dx,dy]=move(x,y);
  if(![dx,dy].every(Number.isFinite))throw new RangeError('Non-finite local displacement');
  src[j][i]=[x,y];dst[j][i]=[x+dx,y+dy];
 }}
 for(let j=0;j<grid;j++)for(let i=0;i<grid;i++){
  triangle(c,im,[src[j][i],src[j][i+1],src[j+1][i+1]],[dst[j][i],dst[j][i+1],dst[j+1][i+1]],width,height);
  triangle(c,im,[src[j][i],src[j+1][i+1],src[j+1][i]],[dst[j][i],dst[j+1][i+1],dst[j+1][i]],width,height);
 }
}
