import assert from 'node:assert/strict';
import {random,ik,leaf,events,branch,split,revealPolyline,leafSupport} from './motion.mjs';
const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
for(const t of [0,1,2.49,events.release])assert.ok(dist(leaf(t),branch(t))<1e-10,'Attached leaf separates');
const eps=1e-4;
assert.ok(dist(leaf(events.release-eps),leaf(events.release+eps))<.01,'Position discontinuity');
const vl={x:(leaf(events.release).x-leaf(events.release-eps).x)/eps,y:(leaf(events.release).y-leaf(events.release-eps).y)/eps};
const vr={x:(leaf(events.release+eps).x-leaf(events.release).x)/eps,y:(leaf(events.release+eps).y-leaf(events.release).y)/eps};
assert.ok(dist(vl,vr)<.03,'Release velocity discontinuity');
for(let t=0;t<20;t+=.01){const p=leaf(t);assert.ok(p.y+leafSupport(p.angle)<=475+1e-9,'Leaf outline penetrates floor');}
assert.deepEqual(leaf(20),leaf(30),'Aftermath not persistent');
assert.ok(leaf(events.land-eps).state==='airborne');
assert.ok(leaf(events.land+eps).state==='landed');
const root={x:10,y:20};
for(const target of [{x:130,y:70},{x:40,y:150},{x:-90,y:40}]){
  for(const side of [-1,1]){let knee=ik(root,target,90,80,side);
    assert.ok(Math.abs(dist(root,knee)-90)<1e-8);assert.ok(Math.abs(dist(knee,target)-80)<1e-8);}
}
const rng=random(21),rng2=random(21);for(let i=0;i<1000;i++)assert.equal(rng(),rng2());
const times=[7,0,3.1,1,8,2.5];const expected=times.map(leaf);
for(let t=0;t<=8;t+=1/60)leaf(t);
assert.deepEqual(times.map(leaf),expected,'Seek order affects trajectory');
assert.equal(split(2).progress,0);assert.equal(split(8).progress,1);
const unequal=[{x:0,y:0},{x:3,y:0},{x:3,y:4}];
assert.deepEqual(revealPolyline(unequal,.5).at(-1),{x:3,y:.5},'Reveal is not distance based');
assert.deepEqual(revealPolyline(unequal,1),unequal);
console.log('PASS: attachment, release continuity, landing, persistent outcome, IK lengths, seed and seek order.');
