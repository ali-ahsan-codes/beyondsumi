import {BY_ID} from "./catalog.mjs";
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const smooth=v=>{const x=clamp(v);return x*x*(3-2*x)};
const mix=(a,b,t)=>a+(b-a)*t;
const TAU=Math.PI*2;
const hash=(seed,n)=>{
  let h=(seed|0)^Math.imul(n+1,0x9e3779b1);
  h=Math.imul(h^(h>>>16),0x85ebca6b);h=Math.imul(h^(h>>>13),0xc2b2ae35);
  return ((h^(h>>>16))>>>0)/4294967296;
};
const grow=(t,delay=0,span=1)=>smooth((t-delay)/span);
const bez=(a,b,c,d,t)=>{const q=1-t;return q*q*q*a+3*q*q*t*b+3*q*t*t*c+t*t*t*d};
const rough=(x,y,seed)=>Math.sin(x*57+seed*.21)*.003+Math.sin(y*73-seed*.17)*.002+Math.sin((x+y)*117+seed)*.001;

/**
 * Deterministic authored density field, not a fluid simulation.
 * t is normalized local event progress [0,1]. Coordinates are actual pixels.
 * options.origin [0..1,0..1] and scale move/size the LOCAL material event.
 * Returned density is visible pigment, not an automatic image reveal command.
 */
export function prepare(mode,t,width,height,seed=1,options={}){
  if(!BY_ID[mode])throw new Error(`Unknown ink mechanism: ${mode}`);
  if(!Number.isFinite(t)||!Number.isFinite(width)||!Number.isFinite(height)||width<=0||height<=0)
    throw new Error("Finite progress and positive dimensions required");
  if(!Number.isInteger(seed))throw new Error("Use a finite integer seed");
  const p=clamp(t), primitives=[],cuts=[];
  const add=(fn)=>primitives.push(fn);
  const ellipse=(x,y,rx,ry,density=1,rotation=0,cut=false)=>{
    if(rx<=0||ry<=0||density<=0)return;
    const co=Math.cos(rotation),si=Math.sin(rotation);
    const fn=(u,v,j)=>{
      const a=(u-x)*co+(v-y)*si,b=-(u-x)*si+(v-y)*co;
      const dist=Math.sqrt((a/rx)**2+(b/ry)**2);
      return clamp((1.04-dist+j/Math.max(.04,Math.min(rx,ry)))/.11)*density;
    };
    (cut?cuts:primitives).push(fn);
  };
  const line=(ax,ay,bx,by,r,density=1,cut=false)=>{
    if(r<=0||density<=0)return;
    const dx=bx-ax,dy=by-ay,len=dx*dx+dy*dy;
    const fn=(u,v,j)=>{const k=clamp(((u-ax)*dx+(v-ay)*dy)/(len||1));
      const d=Math.hypot(u-ax-dx*k,v-ay-dy*k);
      return clamp((r-d+j)/Math.max(.005,r*.28))*density};
    (cut?cuts:primitives).push(fn);
  };
  const path=(points,progress,r,density=1,delay=0)=>{
    const n=points.length-1,amount=clamp(progress-delay)*n,start=primitives.length;
    for(let i=0;i<n;i++){const q=clamp(amount-i);if(q<=0)continue;
      line(...points[i],mix(points[i][0],points[i+1][0],q),mix(points[i][1],points[i+1][1],q),
        r*(1-.45*i/n),density)}
    // A curve is one brush deposit, so its tessellation joins must not darken
    // into repeated beads. Separate strokes can still accumulate pigment.
    const segments=primitives.splice(start);
    if(segments.length)add((u,v,j)=>{
      let value=0;for(const segment of segments)value=Math.max(value,segment(u,v,j));
      return value;
    });
  };
  const curve=(points,progress,r,density=1)=>{
    const result=[];for(let i=0;i<=14;i++){const k=i/14;
      result.push([bez(points[0][0],points[1][0],points[2][0],points[3][0],k),
        bez(points[0][1],points[1][1],points[2][1],points[3][1],k)])}
    path(result,progress,r,density);
  };
  const reservoir=(x,y,r,g,d=.9)=>{
    ellipse(x,y,r*g,r*g*.76,d*.15);
    ellipse(x,y,r*g*.88,r*g*.67,d*.28);
    ellipse(x,y,r*g*.73,r*g*.58,d);
  };
  switch(mode){
    case "drop-bloom":{
      const q=grow(p,0,.8);reservoir(.5,.5,.34,q);
      for(let i=0;i<11;i++){const a=i/11*TAU,r=.16*q;
        ellipse(.5+Math.cos(a)*r,.5+Math.sin(a)*r,.06*q*(.5+hash(seed,i)),.045*q,.5)}
      break;
    }
    case "twin-pools":{
      const q=grow(p,0,.95);reservoir(.32,.5,.26,q);reservoir(.68,.5,.26,grow(p,.12,.83));
      line(.34,.5,.66,.5,.07*grow(p,.5,.5),.74);break;
    }
    case "satellite-splatter":{
      reservoir(.49,.51,.25,grow(p,0,.5));
      for(let i=0;i<17;i++){const a=hash(seed,i)*TAU,r=.18+hash(seed,i+31)*.23;
        ellipse(.49+Math.cos(a)*r,.51+Math.sin(a)*r*.8,
          (.012+hash(seed,i+61)*.035)*grow(p,.08+hash(seed,i+97)*.35,.28),
          (.01+hash(seed,i+13)*.028)*grow(p,.08+hash(seed,i+97)*.35,.28),.6+hash(seed,i+7)*.35)}
      break;
    }
    case "capillary-fan":{
      reservoir(.5,.72,.16,grow(p,0,.5));
      for(let i=0;i<9;i++){const a=-Math.PI*.94+i/8*Math.PI*.88;
        const end=[.5+Math.cos(a)*.42,.72+Math.sin(a)*.55];
        curve([[.5,.72],[.46+hash(seed,i)*.08,.53],[end[0],.43],end],
          grow(p,i*.025,.75),.014+hash(seed,i+21)*.009,.8)}
      break;
    }
    case "river-confluence":{
      const ends=[[.15,.2],[.48,.12],[.86,.27]];
      ends.forEach((s,i)=>curve([s,[s[0],.4],[.56,.45],[.52,.7]],grow(p,i*.07,.72),.026,.65));
      reservoir(.52,.7,.2,grow(p,.35,.6));break;
    }
    case "porous-seep":{
      line(.25,.77,.75,.77,.032*grow(p,0,.2),.85);
      for(let i=0;i<13;i++){const x=.23+i*.043,endY=.25+hash(seed,i)*.23;
        curve([[x,.77],[x-.025,.6],[x+.025,.42],[x+.015,endY]],
          grow(p,hash(seed,i+40)*.18,.8),.012+hash(seed,i+30)*.009,.55+.3*hash(seed,i+4))}
      break;
    }
    case "root-branch":{
      path([[.5,.83],[.49,.61],[.52,.39],[.47,.15]],grow(p,0,.75),.045,.9);
      const branches=[[[.49,.61],[.31,.55],[.16,.35]],[[.51,.46],[.68,.37],[.79,.16]],
        [[.5,.7],[.68,.7],[.85,.82]],[[.49,.69],[.32,.75],[.16,.86]],
        [[.5,.32],[.35,.25],[.29,.12]]];
      const delays=[.30,.46,.22,.24,.55];
      branches.forEach((b,i)=>path(b,grow(p,delays[i],1-delays[i]),.023,.72));break;
    }
    case "vein-network":{
      const paths=[[[.19,.7],[.31,.4],[.52,.2],[.76,.37],[.82,.69],[.6,.8],[.35,.75],[.19,.7]],
        [[.31,.4],[.55,.51],[.76,.37]],[[.55,.51],[.6,.8]],[[.35,.75],[.55,.51],[.52,.2]]];
      const delays=[0,.34,.68,.72],spans=[.7,.5,.32,.28];
      paths.forEach((pts,i)=>path(pts,grow(p,delays[i],spans[i]),i? .018:.028,.65));break;
    }
    case "islands-gather":{
      for(let i=0;i<10;i++){const a=i/10*TAU,r=.21+.04*hash(seed,i);
        reservoir(.5+Math.cos(a)*r,.5+Math.sin(a)*r*.8,.12+.03*hash(seed,i+11),
          grow(p,hash(seed,i+20)*.25,.7),.8)}
      break;
    }
    case "fibre-weave":{
      for(let i=0;i<8;i++){
        const a=.24+i*.073;
        curve([[.2,a],[.4,a-.06],[.6,a+.06],[.8,a]],grow(p,i*.045,.62),.01,.74);
        curve([[a,.2],[a+.05,.4],[a-.05,.6],[a,.8]],grow(p,.18+i*.04,.55),.009,.56)}
      break;
    }
    case "pigment-migration":{
      reservoir(.23,.63,.16,1-.65*smooth(p),.85);
      reservoir(.76,.35,.2,grow(p,.3,.7),.92);
      for(let i=0;i<7;i++){const q=clamp(p*1.35-i*.06);
        const x=bez(.23,.37,.6,.76,q),y=bez(.63,.16,.82,.35,q);
        ellipse(x,y,.027*(1-i*.06),.024*(1-i*.06),.65)}
      curve([[.23,.63],[.37,.16],[.6,.82],[.76,.35]],smooth(p),.009,.18);break;
    }
    case "ripple-transfer":{
      const r=.05+.32*smooth(p),thickness=.025*(1-.45*p);
      add((u,v,j)=>clamp((thickness-Math.abs(Math.hypot(u-.5,(v-.5)*1.15)-r)+j)/.012)*(.85-.2*p));
      for(let i=0;i<12;i++){const a=i/12*TAU;
        ellipse(.5+Math.cos(a)*r,.5+Math.sin(a)*r/1.15,.017+.009*hash(seed,i),.014,.6*grow(p,.25,.6))}
      break;
    }
    case "dry-bristle":{
      for(let i=0;i<12;i++){const y=.35+i*.025,q=grow(p,hash(seed,i)*.1,.7);
        const end=.7+.1*hash(seed,i+14);
        line(.19,y,mix(.19,end,q),mix(y,y-.12,q),.005+.004*hash(seed,i+28),.55+.35*hash(seed,i+5))}
      for(let i=0;i<7;i++)line(.3+i*.06,.25,.31+i*.06,.7,.003,.8,true);
      break;
    }
    case "calligraphic-hook":{
      curve([[.21,.22],[.8,.12],[.81,.84],[.39,.74]],grow(p,0,.85),.065,.87);
      curve([[.39,.74],[.29,.7],[.34,.6],[.43,.57]],grow(p,.65,.35),.03,.9);break;
    }
    case "sheltering-arc":{
      curve([[.2,.79],[.18,.3],[.38,.16],[.51,.21]],grow(p,0,.84),.048,.9);
      curve([[.8,.79],[.82,.38],[.65,.22],[.51,.21]],grow(p,.17,.83),.031,.72);
      line(.24,.8,.76,.8,.012*grow(p,.45,.55),.6);break;
    }
    case "stipple-join":{
      for(let i=0;i<30;i++){const q=i/29,x=bez(.18,.36,.55,.84,q),y=bez(.75,.12,.89,.28,q);
        const g=grow(p,i/36,.16);
        ellipse(x+(hash(seed,i)-.5)*.025,y+(hash(seed,i+31)-.5)*.025,
          (.012+.013*hash(seed,i+80))*g,(.01+.012*hash(seed,i+90))*g,.85)}
      break;
    }
    case "neck-and-separate":{
      const q=smooth(p);reservoir(.42-.16*q,.5,.2,1,.9);reservoir(.58+.16*q,.5,.2,1,.9);
      line(.35-.09*q,.5,.65+.09*q,.5,.09*(1-grow(p,.2,.67)),.88);break;
    }
    case "petal-turn":{
      for(let i=0;i<6;i++){const a=i/6*TAU+.7*(1-smooth(p)),r=.07+.15*smooth(p);
        ellipse(.5+Math.cos(a)*r,.5+Math.sin(a)*r,.14*(.5+.5*grow(p,i*.03,.8)),
          .045+.012*hash(seed,i),.6+.3*hash(seed,i+7),a)}
      ellipse(.5,.5,.055,.055,.9*grow(p,.4,.6));break;
    }
    case "hollow-opens":{
      reservoir(.5,.52,.36,grow(p,0,.45),.95);
      ellipse(.5,.52,.19*grow(p,.3,.7),.23*grow(p,.3,.7),1,0,true);break;
    }
    case "paper-window":{
      const pts=[[.25,.25],[.75,.25],[.76,.75],[.24,.75]];
      pts.forEach((xy,i)=>reservoir(...xy,.15,grow(p,i*.1,.68),.8));
      pts.forEach((xy,i)=>line(...xy,...pts[(i+1)%4],.032*grow(p,.25+i*.08,.55),.6));
      break;
    }
    case "water-lift":{
      reservoir(.5,.5,.38,1,.9);
      ellipse(.43,.5,.46*grow(p,.05,.95),.39*grow(p,.05,.95),.96,0,true);break;
    }
    case "wick-away":{
      const remaining=1-.9*smooth(p);reservoir(.35,.53,.3,Math.sqrt(remaining),remaining);
      curve([[.35,.53],[.54,.4],[.62,.64],[.82,.49]],grow(p,0,.8),.022,.72);
      for(let i=0;i<5;i++)path([[.3,.3+i*.1],[.52,.47],[.64,.52]],grow(p,.12+i*.06,.7),.008,.45);
      reservoir(.82,.49,.085,grow(p,.35,.65),.9);break;
    }
    case "evaporation-islands":{
      reservoir(.5,.5,.37,1,.85);
      for(let i=0;i<18;i++){const x=.25+hash(seed,i)*.5,y=.29+hash(seed,i+31)*.42;
        ellipse(x,y,.11*grow(p,hash(seed,i+61)*.25,.75),.09*grow(p,hash(seed,i+61)*.25,.75),.95,0,true)}
      break;
    }
    case "settled-recede":{
      const q=smooth(p);ellipse(.5,.5,.36-.16*q,.27-.12*q,.22*(1-.6*q));
      ellipse(.5,.5,.28-.13*q,.21-.10*q,.45*(1-.45*q));
      ellipse(.5,.5,.12,.085,.88);break;
    }
  }
  const origin=options.origin??[.5,.5],scale=options.scale??1;
  if(!Array.isArray(origin)||origin.length!==2||!origin.every(Number.isFinite)||!Number.isFinite(scale)||scale<=0)
    throw new Error("origin must be two finite normalized values; scale must be positive");
  return Object.freeze({mode,progress:p,width,height,seed,
    density(x,y){
      if(!Number.isFinite(x)||!Number.isFinite(y))return 0;
      const u=(x/width-origin[0])/scale+.5,v=(y/height-origin[1])/scale+.5;
      if(u<0||u>1||v<0||v>1)return 0;
      const j=rough(u,v,seed);let inkRest=1,cutRest=1;
      for(const fn of primitives)inkRest*=1-clamp(fn(u,v,j));
      for(const fn of cuts)cutRest*=1-clamp(fn(u,v,j));
      return clamp((1-inkRest)*cutRest);
    }});
}

/** Convenience API. Prepare once per frame for high-resolution pixel loops. */
export const sample=(mode,t,x,y,width,height,seed=1,options={})=>
  prepare(mode,t,width,height,seed,options).density(x,y);

/** Renderer-neutral Canvas matte utility: white means ink density, black none. */
export function renderMatte(context,field,{invert=false}={}){
  const w=context.canvas.width,h=context.canvas.height,out=context.createImageData(w,h);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    let d=field.density((x+.5)*field.width/w,(y+.5)*field.height/h);
    if(invert)d=1-d;
    const i=(y*w+x)*4,v=Math.round(d*255);out.data[i]=out.data[i+1]=out.data[i+2]=v;out.data[i+3]=255;
  }
  context.putImageData(out,0,0);return out;
}
