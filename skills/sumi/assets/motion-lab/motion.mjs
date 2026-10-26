export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const mix=(a,b,u)=>a+(b-a)*u;
export const ease=u=>{u=clamp(u);return u*u*u*(u*(u*6-15)+10);};
export function random(seed=1){let n=seed>>>0;return()=>{n=(1664525*n+1013904223)>>>0;return n/4294967296;};}
export function ik(root,target,a,b,side=1){
  const dx=target.x-root.x,dy=target.y-root.y;
  const d=clamp(Math.hypot(dx,dy),Math.abs(a-b)+1e-7,a+b-1e-7);
  const angle=Math.atan2(dy,dx),bend=Math.acos(clamp((a*a+d*d-b*b)/(2*a*d),-1,1))*side;
  return {x:root.x+a*Math.cos(angle+bend),y:root.y+a*Math.sin(angle+bend)};
}
export function branch(t){
  const a=-.5+.045*Math.sin(t*1.7),len=290;
  return {x:420+len*Math.cos(a),y:450+len*Math.sin(a),angle:a};
}
const release=2.5,anchor=branch(release),h=.00001;
const vel={x:(branch(release+h).x-branch(release-h).x)/(2*h),y:(branch(release+h).y-branch(release-h).y)/(2*h)};
function flight(dt){
  const k=.85,g=105,wind=24,e=Math.exp(-k*dt);
  return {x:anchor.x+wind*dt+(vel.x-wind)*(1-e)/k,
    y:anchor.y+g*dt/k+(vel.y-g/k)*(1-e)/k};
}
const contour=[];
function cubic(a,b,c,d,u){return (1-u)**3*a+3*(1-u)**2*u*b+3*(1-u)*u*u*c+u**3*d;}
for(let i=0;i<=80;i++){const u=i/80;contour.push({x:cubic(0,-16,15,31,u),y:cubic(0,-29,-42,-35,u)});contour.push({x:cubic(31,26,14,0,u),y:cubic(-35,-16,-3,0,u)});}
export function leafSupport(angle){return Math.max(...contour.map(p=>.75*(p.x*Math.sin(angle)+p.y*Math.cos(angle))));}
const supportAt=dt=>flight(dt).y+leafSupport(anchor.angle+dt*1.5);
let hi=.01;while(supportAt(hi)<475&&hi<20)hi+=.01;
let lo=hi-.01;for(let n=0;n<70;n++){let m=(lo+hi)/2;if(supportAt(m)<475)lo=m;else hi=m;}
const landDt=(lo+hi)/2,land=flight(landDt);
export function leaf(t){
  if(t<=release)return {...branch(t),state:'attached'};
  const dt=t-release;
  if(dt>=landDt){const a=anchor.angle+landDt*1.5,angle=mix(a,.18,ease((dt-landDt)/.65));return {...land,y:475-leafSupport(angle),angle,state:'landed'};}
  return {...flight(dt),angle:anchor.angle+dt*1.5,state:'airborne'};
}
export const events=Object.freeze({release,land:release+landDt});
export function revealPolyline(points,progress){
  if(points.length<2)return points.slice();
  const lengths=points.slice(1).map((p,i)=>Math.hypot(p.x-points[i].x,p.y-points[i].y));
  const target=lengths.reduce((a,b)=>a+b,0)*clamp(progress),out=[{...points[0]}];let travelled=0;
  for(let i=0;i<lengths.length;i++){
    if(travelled+lengths[i]<=target){out.push({...points[i+1]});travelled+=lengths[i];continue;}
    const u=lengths[i]?clamp((target-travelled)/lengths[i]):0,p={};
    for(const key of Object.keys(points[i]))p[key]=mix(points[i][key],points[i+1][key],u);
    out.push(p);break;
  }
  return out;
}
export function bird(t){return {x:180+t*73,y:245-75*Math.sin(Math.PI*clamp(t/8)),wing:Math.sin(t*5.4)*.65};}
export function split(t){const u=ease((t-2.8)/1.2);return {left:-50*u,right:80*u,rotation:.18*u,progress:u};}
