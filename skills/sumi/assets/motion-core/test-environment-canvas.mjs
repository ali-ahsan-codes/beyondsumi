import assert from 'node:assert/strict';
import {particlePositions,patchDisplacement,drawEnvironmentPass,textureWindow} from './environment-canvas.mjs';
const s={id:'test',kind:'flame',pass:'background',bounds:[20,20,80,80],dx:2,dy:.5,signal:.2,strength:.7,time:2,seed:7,alpha:.1};
assert.deepEqual(patchDisplacement(s,20,50),[0,0]);assert.deepEqual(patchDisplacement(s,50,80),[0,0]);assert.ok(patchDisplacement(s,50,50)[0]>0);
assert.deepEqual(particlePositions(s),particlePositions(s));assert.notDeepEqual(particlePositions(s),particlePositions({...s,time:2.1}));
for(const p of particlePositions(s)){assert.ok(p.x>=20&&p.x<=80&&p.y>=20&&p.y<=80);assert.ok(p.alpha>=0&&p.alpha<=1);}
let transforms=[];function ctx(){return {canvas:{},setTransform(){},clearRect(){},save(){},restore(){},translate(){},scale(){},drawImage(){},beginPath(){},moveTo(){},lineTo(){},closePath(){},clip(){},arc(){},fill(){},stroke(){},fillRect(){},transform(...v){transforms.push(v)},createRadialGradient(){return {addColorStop(){}}}};}
globalThis.OffscreenCanvas=class{constructor(w,h){this.width=w;this.height=h;this.c=ctx()}getContext(){return this.c}};
const c=ctx();drawEnvironmentPass(c,{}, {effects:[s]},'background',{width:100,height:100});assert.equal(transforms.length,72);assert.ok(transforms.every(a=>a.every(Number.isFinite)));assert.ok(transforms.every(([a,b,cc,d])=>a*d-b*cc>0));
const n=transforms.length;drawEnvironmentPass(c,{}, {effects:[s]},'lighting',{width:100,height:100});assert.equal(transforms.length,n);
assert.throws(()=>drawEnvironmentPass(c,{}, {effects:[{...s,mask:{path:'missing'}}]},'background',{width:100,height:100}),/mask/);
console.log('Environment Canvas data/mesh tests passed; actual pixels reviewed separately.');

assert.deepEqual(textureWindow({width:300,height:200},{dx:30,dy:5},100,100),[70,45,100,100]);
assert.notDeepEqual(textureWindow({width:300,height:200},{dx:30,dy:5},100,100),textureWindow({width:300,height:200},{dx:40,dy:5},100,100));
assert.throws(()=>textureWindow({width:100,height:100},{dx:4,dy:0},100,100),/overscan/);
