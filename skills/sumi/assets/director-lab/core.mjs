// Original Sumi mechanism helpers. No external packages. World/grid units are explicit.
export const names=['Sumo','Wash','Grain','Print','Noir','Mist','Sketch','Flow','Scenic'];
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const mix=(a,b,t)=>a+(b-a)*t;
export const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
export const hash=(x,y=0)=>{const n=Math.sin(x*127.1+y*311.7)*43758.5453123;return n-Math.floor(n)};
export function noise(x,y){let a=Math.floor(x),b=Math.floor(y),u=smooth(x-a),v=smooth(y-b);return mix(mix(hash(a,b),hash(a+1,b),u),mix(hash(a,b+1),hash(a+1,b+1),u),v)}
export function fbm(x,y,n=4){let a=.5,s=0;for(let i=0;i<n;i++){s+=a*noise(x,y);x=x*2.03+11;y=y*2.01+7;a*=.5}return s}
export function curl(x,y,t=0){const e=.02,f=(a,b)=>fbm(a+t*.09,b-t*.04);return[(f(x,y+e)-f(x,y-e))/(2*e),-(f(x+e,y)-f(x-e,y))/(2*e)]}
export function weights(values,fallback=0){const a=names.map((_,i)=>Number.isFinite(Number(values[i]))?Math.max(0,Number(values[i])):0),m=Math.max(...a);const scaled=a.map(v=>m?v/m:0),s=scaled.reduce((x,y)=>x+y,0);return s?scaled.map(x=>x/s):a.map((_,i)=>+(i===clamp(Math.floor(fallback),0,8)))}
export const profiles=[
 // bleed, grain, print, noir, fog, sketch, bloom, scenic, bristle
 [.48,.14,0,0,.12,.05,0,0,0], [.94,.07,0,0,.14,0,0,0,0],
 [.12,1,0,0,.04,0,0,0,0], [.1,.1,1,0,0,.06,0,0,0],
 [.3,.08,0,1,.08,.07,0,0,0], [.2,.04,0,0,1,0,0,.1,0],
 [.05,.06,0,0,0,1,0,0,0], [.62,.06,0,0,.06,0,1,0,1],
 [.08,.06,0,0,.15,0,0,1,0]
];
export function parameters(w){return profiles[0].map((_,i)=>w.reduce((s,v,j)=>s+v*profiles[j][i],0))}
export function ik(a,b,l1,l2,bend=1){let dx=b[0]-a[0],dy=b[1]-a[1],raw=Math.hypot(dx,dy),d=clamp(raw,Math.abs(l1-l2)+1e-4,l1+l2-1e-4),base=Math.atan2(dy,dx),angle=base+bend*Math.acos(clamp((l1*l1+d*d-l2*l2)/(2*l1*d),-1,1));return{joint:[a[0]+l1*Math.cos(angle),a[1]+l1*Math.sin(angle)],reachable:raw<=l1+l2&&raw>=Math.abs(l1-l2),target:[a[0]+Math.cos(base)*d,a[1]+Math.sin(base)*d]}}

// Output fps, pose exposure and simulation cadence are separate decisions.
// These are lab defaults, not measurements of reference films.
export const cadences=[12,15,12,12,15,12,10,12,12];
export function poseTime(t,style,economy=true,critical=false){const fps=critical?30:(economy?cadences[style]:30);return Math.floor((t+1e-8)*fps)/fps}
export function estimateFrames(seconds,fps,poseFps){return {output:Math.ceil(seconds*fps),poseSamples:Math.ceil(seconds*poseFps),note:'Pose samples are code updates, not AI-generated images or measured tokens.'}}

// CPU jump flooding: approximate Euclidean distance to the image boundary, signed by mask.
// This is a genuine image-derived field, not a guessed analytic silhouette.
export function signedDistance(mask,w,h){let ax=new Int32Array(w*h).fill(-1),ay=new Int32Array(w*h).fill(-1);
 for(let y=0;y<h;y++)for(let x=0;x<w;x++){let k=y*w+x,s=mask[k]>127; if((s&&(x===0||y===0||x===w-1||y===h-1))||(x>0&&s!==(mask[k-1]>127))||(x<w-1&&s!==(mask[k+1]>127))||(y>0&&s!==(mask[k-w]>127))||(y<h-1&&s!==(mask[k+w]>127))){ax[k]=x;ay[k]=y}}
 for(let step=2**Math.ceil(Math.log2(Math.max(w,h)));step>=1;step=Math.floor(step/2)){const bx=ax.slice(),by=ay.slice();for(let y=0;y<h;y++)for(let x=0;x<w;x++){let k=y*w+x,best=ax[k]<0?Infinity:(x-ax[k])**2+(y-ay[k])**2;for(let j=-1;j<=1;j++)for(let i=-1;i<=1;i++){let xx=x+i*step,yy=y+j*step;if(xx<0||yy<0||xx>=w||yy>=h)continue;let q=yy*w+xx;if(ax[q]<0)continue;let d=(x-ax[q])**2+(y-ay[q])**2;if(d<best){best=d;bx[k]=ax[q];by[k]=ay[q]}}}ax=bx;ay=by}
 return Float32Array.from(ax,(v,k)=>(mask[k]>127?-1:1)*Math.hypot(k%w-v,Math.floor(k/w)-ay[k])/w)
}

// Progressive best-candidate ranks on a torus. A generated blue-noise approximation,
// not a named studio's stock texture. Minimum-distance distribution is tested.
export function blueNoise(size=64){const n=size*size,rank=new Uint8Array(n),used=new Uint8Array(n),dist=new Float32Array(n).fill(Infinity);let seed=23;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 for(let k=0;k<n;k++){let best=-1,bestD=-1;for(let c=0;c<32;c++){let i=Math.floor(rnd()*n);if(!used[i]&&dist[i]>bestD){bestD=dist[i];best=i}}if(best<0){best=used.findIndex(x=>!x)}used[best]=1;rank[best]=Math.floor(k*255/(n-1));let x=best%size,y=Math.floor(best/size);for(let i=0;i<n;i++){let dx=Math.abs(i%size-x),dy=Math.abs(Math.floor(i/size)-y);dx=Math.min(dx,size-dx);dy=Math.min(dy,size-dy);dist[i]=Math.min(dist[i],dx*dx+dy*dy)}}return rank}

export class InkField{
 constructor(w=80,h=45){this.w=w;this.h=h;this.reset()}
 reset(){for(const n of ['u','v','density','pressure','curl','wake'])this[n]=new Float32Array(this.w*this.h);this.frame=0}
 sample(a,x,y){const {w,h}=this;x=clamp(x,0,w-1.001);y=clamp(y,0,h-1.001);const i=Math.floor(x),j=Math.floor(y),u=x-i,v=y-j,k=j*w+i;return mix(mix(a[k],a[k+1],u),mix(a[k+w],a[k+w+1],u),v)}
 divergence(){let a=new Float32Array(this.w*this.h),{w,h,u,v}=this;for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x;a[k]=.5*(u[k+1]-u[k-1]+v[k+w]-v[k-w])}return a}
 project(iterations=24){const {w,h}=this,d=this.divergence();let p=new Float32Array(w*h),q=p.slice();for(let a=0;a<iterations;a++){for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x;q[k]=(p[k-1]+p[k+1]+p[k-w]+p[k+w]-d[k])*.25}[p,q]=[q,p]}for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x;this.u[k]-=.5*(p[k+1]-p[k-1]);this.v[k]-=.5*(p[k+w]-p[k-w])}this.pressure=p;return d}
 step(){let {w,h}=this,t=this.frame/30,dt=1/30,n=w*h,u=this.u.slice(),v=this.v.slice(),d=this.density.slice(),wk=this.wake.slice();
  for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x;u[k]=this.sample(this.u,x-dt*this.u[k],y-dt*this.v[k])*.995;v[k]=this.sample(this.v,x-dt*this.u[k],y-dt*this.v[k])*.995;this.curl[k]=.5*(this.v[k+1]-this.v[k-1]-this.u[k+w]+this.u[k-w])}
  for(let y=2;y<h-2;y++)for(let x=2;x<w-2;x++){let k=y*w+x,gx=Math.abs(this.curl[k+1])-Math.abs(this.curl[k-1]),gy=Math.abs(this.curl[k+w])-Math.abs(this.curl[k-w]),m=Math.hypot(gx,gy)+1e-5;u[k]+=dt*.8*gy/m*this.curl[k];v[k]-=dt*.8*gx/m*this.curl[k]}
  const sx=w*(.18+.62*smooth((t-.4)/6)),sy=h*(.52+.18*Math.sin(t*1.4));
  for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x,r=Math.hypot(x-sx,y-sy),source=Math.exp(-r*r/8)*(t<7?1:0);u[k]+=source*1.3;v[k]+=source*Math.cos(t*1.4)*1.2;d[k]=Math.min(1,d[k]+source*.16);wk[k]=Math.max(wk[k]*.982,Math.exp(-r*r/13)*(t<7?1:0))}
  this.u=u;this.v=v;this.project();u=this.u;v=this.v;
  for(let y=1;y<h-1;y++)for(let x=1;x<w-1;x++){let k=y*w+x,a=this.sample(d,x-dt*u[k],y-dt*v[k]);const angle=noise(x*.13,y*.11)*Math.PI,c=Math.cos(angle),s=Math.sin(angle),xx=.08*c*c+.012*s*s,yy=.08*s*s+.012*c*c,xy=(.08-.012)*c*s; // positive diffusion tensor
   const lap=xx*(d[k-1]+d[k+1]-2*d[k])+yy*(d[k-w]+d[k+w]-2*d[k])+xy*.5*(d[k+w+1]-d[k+w-1]-d[k-w+1]+d[k-w-1]);this.density[k]=clamp(a*.998+lap);this.wake[k]=this.sample(wk,x-dt*u[k],y-dt*v[k])}
  this.frame++
 }
 seek(seconds){const target=Math.round(clamp(seconds,0,12)*30);if(target<this.frame)this.reset();while(this.frame<target)this.step();return this}
 rgba(){const a=new Uint8Array(this.w*this.h*4);for(let i=0;i<this.density.length;i++){a[i*4]=this.density[i]*255;a[i*4+1]=clamp(this.pressure[i]*.5+.5)*255;a[i*4+2]=this.wake[i]*255;a[i*4+3]=255}return a}
}
