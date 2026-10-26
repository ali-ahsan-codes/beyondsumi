import {clamp,mix,ease,random,branch,leaf,bird,split,revealPolyline} from './motion.mjs';
const canvas=document.querySelector('#film'),c=canvas.getContext('2d');
const select=document.querySelector('#style'),seek=document.querySelector('#seek'),out=document.querySelector('#time'),play=document.querySelector('#play');
const names=['wash','grain','print','noir','mist','sketch','flow','scenic'];
const notes={wash:'A branch releases one leaf. The leaf inherits its anchor velocity, meets the ground and stays there. The paper texture is stable.',grain:'A graphic bird crosses granular mountain planes. Stipple stays attached to the painted forms while the wings articulate.',print:'Outlined leaves and flowers move around fixed branch roots. Petals open in staggered stages; the drawn border stays rigid.',noir:'A directional stroke divides one graphic shape. Both pieces begin separating at the same event and settle into a lasting new composition.',mist:'A travelling wash reveals a landscape through a coherent soft mask. The central subject remains readable as peripheral mist changes.',sketch:'A scratch-drawn bird notices a falling seed. Its eye closes and opens locally; the body stays grounded while the head pivots.',flow:'A pressure-varying ribbon grows along a curved path. Fine bristle strands follow the same gesture and retain seeded variation.',scenic:'A layered painted landscape opens through a modest camera move. Depth planes move at different rates and a bird articulates independently.'};
const paper=document.createElement('canvas');paper.width=960;paper.height=540;
const pc=paper.getContext('2d'),pr=random(224);
for(let i=0;i<20000;i++){pc.fillStyle=`rgba(45,39,26,${pr()*.04})`;pc.fillRect(pr()*960,pr()*540,pr()*1.5+.3,pr()*1.2+.3);}
function path(points,fill,stroke=null,width=1){c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.closePath();if(fill){c.fillStyle=fill;c.fill();}if(stroke){c.strokeStyle=stroke;c.lineWidth=width;c.stroke();}}
function ellipse(x,y,rx,ry,col){c.fillStyle=col;c.beginPath();c.ellipse(x,y,Math.max(.01,rx),Math.max(.01,ry),0,0,Math.PI*2);c.fill();}
function stroke(points,color,width=2){c.beginPath();points.forEach((p,i)=>i?c.lineTo(...p):c.moveTo(...p));c.strokeStyle=color;c.lineWidth=width;c.lineCap='round';c.lineJoin='round';c.stroke();}
function base(col='#eeeadd'){c.clearRect(0,0,960,540);c.fillStyle=col;c.fillRect(0,0,960,540);}
function finish(){c.drawImage(paper,0,0);}
function hills(t,colored=false){
  const colors=colored?['#b5c2ba','#809c95','#4e716e']:['#d5d6cc','#bdc1b7','#8c9992'];
  colors.forEach((col,j)=>{c.save();c.translate(-30-ease(t/8)*(12+j*15),0);c.beginPath();c.moveTo(-50,550);c.lineTo(-50,440);const rr=random(20+j);for(let x=-50;x<=1100;x+=24){let y=360-110*Math.sin(x*.007+j*.4)**2+j*30+(rr()-.5)*14;c.lineTo(x,y);}c.lineTo(1100,550);c.closePath();c.fillStyle=col;c.fill();c.clip();const grain=random(80+j);for(let k=0;k<1800;k++){c.fillStyle=`rgba(28,49,39,${grain()*.045})`;c.fillRect(grain()*1100,260+grain()*290,1+grain()*5,.5+grain()*2);}c.restore();});
}
function paintBranch(t,mode='wash'){
  const b=branch(t);path([[396,477],[411,453],[420,446],[426,451],[413,478]],'#252e29');c.save();c.translate(420,450);c.rotate(b.angle);
  c.beginPath();c.moveTo(0,0);c.bezierCurveTo(80,-12,180,6,290,0);c.lineTo(289,4);c.bezierCurveTo(170,17,70,14,0,9);c.closePath();c.fillStyle=mode==='print'?'#535c49':'#252e29';c.fill();
  if(mode==='wash'){for(let j=0;j<8;j++)stroke([[0,j],[80,1+j*.9],[200,4+j*.7],[286,2+j*.4]],'#555b4b30',.5);}
  c.restore();
}
function leafShape(x,y,angle,scale=1,color='#a44735',outline=false){c.save();c.translate(x,y);c.rotate(angle);c.scale(scale,scale);c.beginPath();c.moveTo(0,0);c.bezierCurveTo(-16,-29,15,-42,31,-35);c.bezierCurveTo(26,-16,14,-3,0,0);c.fillStyle=color;c.fill();if(outline){c.strokeStyle='#3e473f';c.lineWidth=1.3;c.stroke();}stroke([[0,0],[13,-18],[29,-34]],outline?'#4b4a38':'#e8d5ae80',.8);c.restore();}
function wash(t){base();hills(t);c.fillStyle='#eeeaddcc';c.fillRect(0,350,960,190);stroke([[0,479],[200,473],[420,477],[740,479],[960,474]],'#62665c50',1.3);paintBranch(t);const p=leaf(t);leafShape(p.x,p.y,p.angle,.75);}
const gr=random(77),dots=Array.from({length:12000},()=>({x:gr()*1000,y:gr()*400,r:gr()*.8+.2,a:gr()}));
function grain(t){base('#e9e8d7');ellipse(700,175,105,105,'#faf9ed');
  for(let j=0;j<3;j++){c.save();c.translate(-80-t*(2+j*2),130+j*45);let pts=[[0,340],[145,180],[255,290],[395,5],[540,245],[700,80],[850,290],[1050,210],[1150,450],[0,450]];path(pts,['#b7c0af','#819589','#324e49'][j]);c.clip();for(const d of dots){c.fillStyle=`rgba(9,25,22,${d.a*.3*(d.y/400)})`;c.fillRect(d.x,d.y,d.r,d.r);}c.restore();}
  const b=bird(t);drawBird(b.x,b.y,.75,b.wing,'#182c29');}
function drawBird(x,y,s,wing,col){c.save();c.translate(x,y);c.scale(s,s);ellipse(0,0,23,8,col);ellipse(24,-7,8,7,col);path([[30,-8],[45,-5],[30,-4]],col);path([[-16,0],[-50,-10],[-36,8]],col);c.save();c.rotate(wing);path([[0,0],[-60,-68],[-28,-53],[17,0]],col);c.restore();c.save();c.rotate(-wing*.5);path([[2,1],[-32,40],[18,13]],col);c.restore();c.restore();}
function print(t){base('#dfd3b3');c.strokeStyle='#625e48';c.lineWidth=1.5;c.strokeRect(40,35,880,470);ellipse(710,165,86,86,'#abb9b0');
  for(let j=0;j<4;j++)stroke([[40,400+j*18],[210,400+j*18],[310,402+j*18],[600,400+j*18],[920,400+j*18]],'#a6a58a',1);
  paintBranch(t,'print');const a=branch(t).angle;
  for(let i=0;i<7;i++){let localX=60+i*32;let x=420+localX*Math.cos(a),y=450+localX*Math.sin(a);let ang=a-.4+(i%2?-.7:.7)+Math.sin(t*1.8+i)*.08;leafShape(x,y,ang,.85,i%2?'#a56941':'#6b8267',true);
    if(i%2===0){stroke([[x,y],[x,y-40]],'#5b664a',1.3);let o=ease((t-i*.2)/3);c.save();c.translate(x,y-40);for(let k=0;k<5;k++){c.save();c.rotate(k*Math.PI*2/5);c.translate(0,-11*o);c.scale(.4+.6*o,.7+.3*o);ellipse(0,-6,10,15,'#ece6cf');c.strokeStyle='#746a51';c.lineWidth=.8;c.stroke();c.restore();}ellipse(0,0,5,5,'#c5ac62');c.restore();}}
}
function noir(t){base('#101819');const q=split(t),r=2.8;ellipse(705,160,75,75,'#e8e4d7');
  c.save();c.translate(490,295);c.rotate(-.16);const shape=[[-145,-95],[115,-78],[146,101],[-117,118]];
  for(const side of [-1,1]){c.save();c.translate(side<0?q.left:q.right,side<0?28*q.progress:45*q.progress);c.rotate(side*q.rotation);c.beginPath();c.rect(side<0?-500:0,-500,500,1000);c.clip();path(shape,'#e8e4d7');for(let i=0;i<12;i++)stroke([[-120,-70+i*13],[110,-64+i*13]],'#101819',1.2);c.restore();}c.restore();
  const p=ease((t-r+.18)/.35);if(t>r-.18&&t<r+.6){c.globalAlpha=1-ease((t-r-.15)/.45);stroke([[518.7,472.7],[mix(518.7,461.3,p),mix(472.7,117.3,p)]],'#b54836',8);c.globalAlpha=1;}
}
const mistLayer=document.createElement('canvas');mistLayer.width=960;mistLayer.height=540;const mc=mistLayer.getContext('2d');const mask=document.createElement('canvas');mask.width=960;mask.height=540;const mk=mask.getContext('2d');
function mist(t){base('#edf0e9');mc.clearRect(0,0,960,540);mc.fillStyle='#526a66';mc.beginPath();mc.moveTo(0,400);for(let x=0;x<=960;x+=10)mc.lineTo(x,335+22*Math.sin(x*.011)+14*Math.cos(x*.023));mc.lineTo(960,500);mc.lineTo(0,500);mc.fill();
  mc.fillStyle='#172c2a';mc.beginPath();mc.ellipse(520,345,6,8,0,0,Math.PI*2);mc.fill();mc.fillRect(515,352,10,25);mc.fillRect(515,375,3,16);mc.fillRect(522,375,3,16);
  mk.clearRect(0,0,960,540);const rr=random(52);for(let i=0;i<65;i++){const x=100+rr()*760,y=345+rr()*115;const rad=(35+rr()*40)*ease((t-i*.025)/2);if(rad>.01){const g=mk.createRadialGradient(x,y,0,x,y,rad);g.addColorStop(0,'#000');g.addColorStop(1,'transparent');mk.fillStyle=g;mk.fillRect(x-rad,y-rad,rad*2,rad*2);}}mc.globalCompositeOperation='destination-in';mc.drawImage(mask,0,0);mc.globalCompositeOperation='source-over';c.drawImage(mistLayer,0,0);
  for(let i=0;i<4;i++){const g=c.createLinearGradient(0,280+i*40,0,345+i*40);g.addColorStop(0,'#edf0e900');g.addColorStop(.5,'#edf0e998');g.addColorStop(1,'#edf0e900');c.fillStyle=g;c.fillRect(Math.sin(t*.3+i)*35,280+i*40,960,65);}c.globalAlpha=ease((t-1)/2);ellipse(520,345,6,8,'#263c38');c.fillStyle='#263c38';c.fillRect(515,352,10,25);c.fillRect(515,375,3,16);c.fillRect(522,375,3,16);c.globalAlpha=1;}
function sketch(t){base('#f1ecdf');stroke([[170,453],[730,453]],'#bbb8a9',.8);const nod=.08*Math.sin(t*.9);c.save();c.translate(470,380);ellipse(0,0,94,55,'#30383b');path([[-55,15],[-180,-20],[-113,31]],'#30383b');stroke([[-15,40],[-15,72],[-30,74]],'#30383b',4);stroke([[20,40],[20,72],[6,74]],'#30383b',4);
  c.save();c.translate(60,-30);c.rotate(nod);ellipse(0,-25,48,51,'#30383b');path([[37,-28],[84,-13],[43,-5]],'#b57d47');const blink=1-ease((t-2.6)/.12)+ease((t-2.85)/.18);ellipse(15,-35,7,6*clamp(blink,.04,1),'#d7a451');ellipse(17,-36,2,3*clamp(blink,.04,1),'#161c1e');const rr=random(5);for(let i=0;i<55;i++){let x=rr()*65-35,y=rr()*65-65;stroke([[x,y],[x+9,y-6]],'#e5e4d225',.7);}c.restore();
  for(let i=0;i<26;i++)stroke([[-80+i*5,-15+Math.sin(i)*5],[-76+i*5,20+Math.sin(t*1.3+i)*2]],'#eceadd25',.7);c.restore();ellipse(600,Math.min(447,180+35*Math.max(0,t-.6)**2),3,6,'#b57d47');}
const ribbon=Array.from({length:401},(_,i)=>{const u=i/400,dy=825*Math.cos(u*7.5)-70,n=Math.hypot(710,dy);return {u,x:125+710*u,y:280+110*Math.sin(u*7.5)-70*u,nx:-dy/n,ny:710/n};});
function flow(t){base('#f6f3e9');const section=revealPolyline(ribbon,ease(t/6.5));for(let br=0;br<20;br++){let pts=section.map(p=>{const pressure=Math.pow(Math.max(0,Math.sin(Math.PI*p.u)),.65),offset=(br-9.5)*3.8*pressure;return [p.x+p.nx*offset,p.y+p.ny*offset];});if(pts.length>1)stroke(pts,br%5===0?'#555c4b80':'#1e2926',br%4===0?.8:1.8);}}
function scenic(t){base('#d4ddd5');const g=c.createLinearGradient(0,0,0,540);g.addColorStop(0,'#b9ced0');g.addColorStop(.55,'#e6dfc6');g.addColorStop(1,'#748f89');c.fillStyle=g;c.fillRect(0,0,960,540);ellipse(705,145,54,54,'#f0e9d1');hills(t,true);
  c.fillStyle='#a5bbb4';c.fillRect(0,430,960,110);for(let i=0;i<25;i++){let y=435+i*4;stroke([[80+Math.sin(t*.6+i)*12,y],[840+Math.sin(t*.6+i)*12,y]],`rgba(231,235,210,${.05+i*.005})`,.5);}
  c.save();c.translate(-30-ease(t/8)*75,0);stroke([[70,540],[95,250],[150,130],[310,80]],'#273f38',24);for(let i=0;i<16;i++)ellipse(100+i*19,100+35*Math.sin(i*.6),45,21,'#344e40');c.restore();const b=bird(t);drawBird(b.x,b.y,.48,b.wing,'#293e38');}
const renderers={wash,grain,print,noir,mist,sketch,flow,scenic};
let t=0,running=false,last=0;const params=new URLSearchParams(location.search);if(names.includes(params.get('style')))select.value=params.get('style');if(params.has('t'))t=clamp(Number(params.get('t'))||0,0,8);
function render(){c.setTransform(1,0,0,1,0,0);c.globalAlpha=1;c.globalCompositeOperation='source-over';renderers[select.value](t);finish();seek.value=t;out.textContent=`${t.toFixed(2)} / 8.00`;canvas.dataset.style=select.value;canvas.dataset.time=t.toFixed(4);canvas.dataset.playing=String(running);document.querySelector('#description').textContent=notes[select.value];play.textContent=running?'Pause':'Play';}
function tick(now){if(running){t=Math.min(8,t+(now-last)/1000);if(t>=8)running=false;render();}last=now;requestAnimationFrame(tick);}requestAnimationFrame(tick);
play.onclick=()=>{if(t>=8)t=0;running=!running;last=performance.now();render();};document.querySelector('#replay').onclick=()=>{t=0;running=true;last=performance.now();render();};
select.onchange=()=>{t=0;running=false;render();};seek.oninput=()=>{t=Number(seek.value);running=false;render();};document.querySelector('#full').onclick=()=>canvas.requestFullscreen?.();render();
