import assert from "node:assert/strict";
import {TRANSITIONS,SELECTION_GUIDE} from "./catalog.mjs";
import {prepare,sample} from "./fields.mjs";
assert.equal(TRANSITIONS.length,24);
assert.equal(new Set(TRANSITIONS.map(x=>x.id)).size,24);
const snapshots=new Map();
for(const mode of TRANSITIONS){
  const data=[];
  for(const time of [0,.25,.6,1]){
    const f=prepare(mode.id,time,200,130,71);
    for(let y=4;y<130;y+=8)for(let x=4;x<200;x+=8){
      const d=f.density(x,y);assert(Number.isFinite(d)&&d>=0&&d<=1,mode.id);data.push(d);
    }
  }
  assert(data.some(v=>v>.2),`${mode.id} must deposit visible pigment`);
  const a=prepare(mode.id,.43,200,130,71),b=prepare(mode.id,.43,200,130,71);
  assert.equal(a.density(73,51),b.density(73,51),"Direct seeking must repeat");
  prepare(mode.id,.99,200,130,71);
  assert.equal(a.density(73,51),prepare(mode.id,.43,200,130,71).density(73,51),"Out-of-order sampling must repeat");
  assert.equal(sample(mode.id,.43,73,51,200,130,71),a.density(73,51));
  assert.equal(a.density(-200,-300),0,"Local field must not cover distant pixels");
  snapshots.set(mode.id,data);
}
const ids=[...snapshots.keys()];
let closest={distance:Infinity,a:"",b:""};
for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){
  const a=snapshots.get(ids[i]),b=snapshots.get(ids[j]);
  const diff=a.reduce((sum,v,k)=>sum+Math.abs(v-b[k]),0)/a.length;
  assert(diff>.008,`${ids[i]} and ${ids[j]} are effectively duplicated fields`);
  if(diff<closest.distance)closest={distance:diff,a:ids[i],b:ids[j]};
}
const area=(id,t)=>{const f=prepare(id,t,100,100,9);let sum=0;for(let y=0;y<100;y+=4)for(let x=0;x<100;x+=4)sum+=f.density(x,y);return sum};
assert(area("drop-bloom",1)>area("drop-bloom",0),"Birth grows");
assert(area("water-lift",1)<area("water-lift",0)*.25,"Water lifting removes most local pigment");
assert(area("settled-recede",1)<area("settled-recede",0),"Wet shoulder recedes");
assert(area("settled-recede",1)>0,"Settled core remains");
assert(prepare("hollow-opens",1,100,100,5).density(50,52)<.05,"Hollow protects its paper centre");
const moved=prepare("drop-bloom",1,100,100,9,{origin:[.2,.2],scale:.3});
assert(moved.density(20,20)>.5&&moved.density(75,75)===0,"Local origin and scale respected");
assert.throws(()=>prepare("unknown",.5,100,100));
assert.throws(()=>prepare("drop-bloom",NaN,100,100));
assert.throws(()=>prepare("drop-bloom",.5,0,100));
assert.throws(()=>prepare("drop-bloom",.5,100,100,NaN));
assert.throws(()=>prepare("drop-bloom",.5,100,100,1.5));
assert.equal(SELECTION_GUIDE.thirtySecondFilm.upperDefault,4);
console.log(JSON.stringify({ok:true,mechanisms:24,pairwiseDistinctChecks:276,
  closestPair:closest,checks:"finite density, deterministic seek, local placement, distinct temporal fields, birth/lift/core/hollow behavior",
  limit:"Numerical mechanism checks only; actual artwork, motion and sound still need review."},null,2));
