import assert from 'node:assert/strict';
import {weights,parameters,ik,InkField,signedDistance,blueNoise,poseTime} from './core.mjs';
const w=weights([1,3,-1,Infinity,NaN]);assert.equal(w.reduce((a,b)=>a+b,0),1);assert.equal(w[1],.75);assert.equal(weights([],8)[8],1);assert.equal(weights([1e308,1e308])[0],.5);
assert.equal(parameters(weights([0,0,0,0,1]))[3],1);
for(const target of [[0,0],[5,1],[50,0]]){const r=ik([0,0],target,4,3,-1);assert.ok(Math.abs(Math.hypot(...r.joint)-4)<1e-6);assert.ok(Math.abs(Math.hypot(r.target[0]-r.joint[0],r.target[1]-r.joint[1])-3)<1e-6)}
assert.equal(ik([0,0],[50,0],4,3).reachable,false);
const mask=Uint8Array.from({length:32*20},(_,i)=>i%32>=10&&i%32<=21&&Math.floor(i/32)>=5&&Math.floor(i/32)<=14?255:0),sdf=signedDistance(mask,32,20);
assert.ok(sdf[10*32+15]<0);assert.ok(sdf[0]>.1,'outside image corners must not seed a spurious ink border');assert.ok(sdf[10*32+9]===0);assert.ok(sdf.every(Number.isFinite));
const a=new InkField(40,24),b=new InkField(40,24);a.seek(2);const expected=a.rgba();a.seek(.5);a.seek(2);assert.deepEqual(a.rgba(),expected,'backward seek must replay identical material state');b.seek(1);b.seek(2);assert.deepEqual(b.rgba(),expected,'seeking order cannot affect final state');assert.ok(a.density.every(v=>Number.isFinite(v)&&v>=0&&v<=1));
const f=new InkField(30,20);for(let i=0;i<f.u.length;i++){f.u[i]=Math.sin(i*.27);f.v[i]=Math.cos(i*.17)}const norm=v=>v.reduce((a,b)=>a+b*b,0),before=norm(f.divergence());f.project(60);assert.ok(norm(f.divergence())<before,'projection should reduce divergence');
const n=blueNoise(32);assert.deepEqual(n,blueNoise(32));const points=Array.from(n,(v,i)=>v<12?i:-1).filter(i=>i>=0);let close=0;for(let i=0;i<points.length;i++)for(let j=0;j<i;j++){const dx=Math.abs(points[i]%32-points[j]%32),dy=Math.abs(Math.floor(points[i]/32)-Math.floor(points[j]/32));if(Math.hypot(Math.min(dx,32-dx),Math.min(dy,32-dy))<2)close++}assert.equal(close,0,'early best-candidate ranks should avoid adjacent clumps');
assert.equal(poseTime(.08,6,true),0);assert.ok(poseTime(.08,6,true,true)>0);assert.equal(poseTime(2,6,true),2);
console.log('PASS: normalized material weights, IK reach, image SDF boundary, deterministic fluid seek, pressure projection, stipple spacing, independent pose cadence.');
