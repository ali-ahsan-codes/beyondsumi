import assert from 'node:assert/strict';
import {gaitFoot,twoLink,distance,localToWorld,anchorVelocity,ballistic,
  floorTime,sweepBlade,bakePetal,sampleBake} from './motion-core.mjs';
const checks = [];
const near = (a,b,tolerance=1e-6) => assert.ok(Math.abs(a-b)<tolerance,`${a} != ${b}`);

for (const scale of [.83,1,1.22]) {
  for (const offset of [0,.5]) {
    let last = null;
    for (let travel=0; travel<500; travel+=.3) {
      const f=gaitFoot({travel,scale,offset});
      if(last && f.inStance && last.inStance && f.cycle===last.cycle) near(f.world[0],last.world[0]);
      if(f.inStance) near(f.world[1],585);
      near(travel+f.local[0]*scale,f.world[0]);
      last=f;
    }
  }
}
checks.push('World-space stance is invariant at three rig scales and both feet.');
for(const target of [[40,20],[10,70],[200,0],[0,0]]) {
  const k=twoLink([0,0],target,40,43);
  near(distance([0,0],k.joint),40);
  near(distance(k.joint,k.end),43);
  if(k.reachable) near(distance(k.end,target),0);
}
assert.equal(twoLink([0,0],[200,0],40,43).reachable,false);
assert.equal(twoLink([0,0],[0,0],40,43).reachable,false);
checks.push('IK preserves both bone lengths and explicitly reports unreachable targets.');
const mirrored=localToWorld([10,0],{x:50,y:100,scale:2,facing:-1,angle:Math.PI/2});
near(mirrored[0],50); near(mirrored[1],120);
const positionAt=t=>localToWorld([10,0],{x:t*20,y:100,angle:t,scale:1.22});
const t=1.1,p=positionAt(t),v=anchorVelocity(positionAt,t);
const epsilon=1e-5,free=ballistic(p,v,epsilon);
near(free.position[0],positionAt(t+epsilon)[0],1e-6);
near(free.position[1],positionAt(t+epsilon)[1],1e-6);
const impact=floorTime(100,-50,585);
near(ballistic([10,100],[20,-50],impact).position[1],585);
checks.push('Full anchor transform, release position/velocity, and free-flight floor solve agree.');

// Fast rotating blade whose endpoints miss at the two outer frames. A sweep
// finds the intermediate crossing, unlike a final-tip-only assertion.
const hit=sweepBlade({poseAt:u=>({x:0,y:0,angle:-.5+u}),
  targetAt:()=>[80,0],from:0,to:1,length:100,radius:3,samples:200});
assert.equal(hit.hit,true); assert.ok(hit.time>.4&&hit.time<.6);
const miss=sweepBlade({poseAt:u=>({x:0,y:0,angle:-.5+u}),
  targetAt:()=>[140,0],from:0,to:1,length:100,radius:3,samples:200});
assert.equal(miss.hit,false);
checks.push('Subframe blade sweep detects a fast intermediate hit and rejects a distant target.');
const options={duration:20,position:[200,400],velocity:[20,-15],phase:.7};
const bake=bakePetal(options),again=bakePetal(options);
assert.deepEqual(bake,again);
for(const s of bake.samples) assert.ok(s.y+3<=585+1e-8);
const last=bake.samples.at(-1);
assert.equal(last.resting,true);
for(const t of [10,1,18,2,20,0,18]) assert.deepEqual(sampleBake(bake,t),sampleBake(again,t));
near(sampleBake(bake,19.8).x,sampleBake(bake,20).x);
checks.push('Baked petal has repeatable seeking, bounded floor contact, and persistent settling.');
console.log(JSON.stringify({status:'pass',checks,limitations:[
  'No rendered shot or normal-speed perceptual review is covered by these tests.',
  'Gait is for a monotonic walk segment; support shifts and turns still require authored poses.',
  'Sword sweep uses bounded samples; choose resolution for the actual motion and target.',
  'Petal is a stylized particle approximation, not aerodynamic simulation.'
]},null,2));
