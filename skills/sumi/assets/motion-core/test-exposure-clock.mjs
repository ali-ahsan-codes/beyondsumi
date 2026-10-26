import assert from 'node:assert/strict';
import {exposureClock} from './exposure-clock.mjs';
for(let frame=0; frame<1440; frame+=2){const a=exposureClock(frame),b=exposureClock(frame+1);assert.equal(a.characterTime,b.characterTime);assert.ok(Math.abs(b.outputTime-a.outputTime-1/24)<1e-12)}
assert.equal(new Set(Array.from({length:24},(_,f)=>exposureClock(f).exposure)).size,12);
assert.equal(exposureClock(1439).exposure,719);
assert.throws(()=>exposureClock(-1));assert.throws(()=>exposureClock(.5));
for(let frame=0;frame<1680;frame+=2){const a=exposureClock(frame,28),b=exposureClock(frame+1,28);assert.equal(a.characterTime,b.characterTime);assert.ok(Math.abs(b.outputTime-a.outputTime-1/28)<1e-12)}
assert.equal(new Set(Array.from({length:28},(_,f)=>exposureClock(f,28).exposure)).size,14);
assert.equal(exposureClock(56,28).characterTime,2);
assert.throws(()=>exposureClock(1,27));assert.throws(()=>exposureClock(1,0));
console.log('1440 frames: paired character time, independent output time, 720 exposures; invalid input rejected.');
console.log('Original 28fps: 1680 frames, 14 paired states/second; Light/Dark default unchanged.');

for(let f=0;f<1800;f+=2){assert.equal(exposureClock(f,30).characterTime,exposureClock(f+1,30).characterTime);}
assert.equal(new Set(Array.from({length:30},(_,f)=>exposureClock(f,30).exposure)).size,15);
assert.equal(exposureClock(60,30).characterTime,2);
console.log('Current Original30fps:15 paired states/second; historical28fps and Light/Dark24fps retained.');
