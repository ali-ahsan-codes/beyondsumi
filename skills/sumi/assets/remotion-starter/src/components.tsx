import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,useVideoConfig,delayRender,continueRender,cancelRender} from 'remotion';
export type CaptionCue={start:number;end:number;text:string};
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
export const smooth=(n:number)=>{const q=clamp(n);return q*q*(3-2*q)};
export const mix=(a:number,b:number,p:number)=>a+(b-a)*p;
export function CaptionTrack({cues,direction='auto',fontFamily='Arial,sans-serif',color='#fff',fontSize}:{cues:CaptionCue[];direction?:'auto'|'rtl'|'ltr';fontFamily?:string;color?:string;fontSize?:number}){
 const {fps,width,height}=useVideoConfig();const t=useCurrentFrame()/fps;const cue=cues.find(c=>t>=c.start&&t<c.end);if(!cue)return null;
 const fade=Math.min(.12,(cue.end-cue.start)/4);const opacity=Math.min(clamp((t-cue.start)/fade),clamp((cue.end-t)/fade));
 return <div dir={direction} style={{position:'absolute',left:'8%',right:'8%',bottom:'7%',textAlign:'center',fontFamily,fontSize:fontSize??width*(height>width?.038:.026),lineHeight:1.3,color,whiteSpace:'pre-line',opacity,textShadow:'0 2px 8px #0008'}}>{cue.text}</div>;
}
export type Pose={x:number;y:number;scale:number;rotation:number};
export function AssetLayer({src,width,height,start=0,duration,from,to,children,exposure='ones'}:{src?:string;width:number;height:number;start?:number;duration:number;from:Pose;to:Pose;children?:React.ReactNode;exposure?:'ones'|'twos'|'twenty'}){
 const frame=useCurrentFrame(),fps=useVideoConfig().fps;const t=exposure==='twenty'?Math.floor(frame*20/fps)/20:(exposure==='twos'?Math.floor(frame/2)*2:frame)/fps;const p=smooth((t-start)/duration);if(duration<=0)throw new Error('AssetLayer duration must be positive');
 return <div style={{position:'absolute',left:0,top:0,width,height,transformOrigin:'50% 50%',transform:`translate(${mix(from.x,to.x,p)}px,${mix(from.y,to.y,p)}px) rotate(${mix(from.rotation,to.rotation,p)}deg) scale(${mix(from.scale,to.scale,p)})`}}>{src?<Img src={staticFile(src)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>:null}{children}</div>;
}
export function FadeThrough({at,duration=.4,color='#111'}:{at:number;duration?:number;color?:string}){const {fps}=useVideoConfig();const time=useCurrentFrame()/fps;const distance=Math.abs(time-at);if(distance>=duration/2)return null;return <AbsoluteFill style={{background:color,opacity:1-distance/(duration/2),pointerEvents:'none'}}/>}
// Call at the top of a composition using a local, licensed font asset.
export function useLocalFont(family:string,src:string){const [handle]=useState(()=>delayRender(`Font: ${family}`));useEffect(()=>{let live=true;const face=new FontFace(family,`url(${staticFile(src)})`);face.load().then(()=>{document.fonts.add(face);if(live)continueRender(handle)}).catch(cancelRender);return()=>{live=false;continueRender(handle)}},[family,src,handle]);}
