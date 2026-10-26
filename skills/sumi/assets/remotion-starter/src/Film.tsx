import React from 'react';
import {AbsoluteFill,Audio,Sequence,staticFile,useCurrentFrame,useVideoConfig,interpolate,spring} from 'remotion';
import {project,secondsToFrames} from './project';
import {CaptionTrack} from './components';
// A runnable engine check. Replace this visual with the current story's authored shots.
// Keep distinct shots and independently editable clips as separate JSX components/nodes.
export const Film=()=>{const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const portrait=height>width;const enter=spring({frame,fps,config:{damping:24,stiffness:140}});const line=interpolate(frame,[0,fps*1.4],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <AbsoluteFill style={{background:'#122b38',color:'#f7ebd6',justifyContent:'center',alignItems:'center',fontFamily:'Arial,sans-serif',overflow:'hidden'}}>
  <div style={{position:'absolute',inset:'8%',border:'1px solid #55747b'}}/>
  <div style={{textAlign:'center',width:'82%',transform:`translateY(${(1-enter)*80}px)`,opacity:Math.min(1,enter)}}>
    <div style={{fontSize:width*.023,letterSpacing:width*.005,textTransform:'uppercase',color:'#a4c5bf'}}>{project.style}</div>
    <h1 style={{fontSize:width*(portrait?.10:.065),lineHeight:1.05,letterSpacing:'-.05em',margin:'35px 0'}}>{project.title}</h1>
    <div style={{height:8,width:'60%',background:'#ee8a64',margin:'auto',transform:`scaleX(${line})`,transformOrigin:'left'}}/>
    <p style={{fontSize:width*.024,color:'#a4c5bf'}}>The production canvas is ready.</p>
  </div>
  <CaptionTrack cues={project.captions}/>
  {project.audio.map((clip,i)=><Sequence key={`${i}-${clip.src}`} name={clip.src} from={secondsToFrames(clip.startSeconds)} durationInFrames={secondsToFrames(clip.durationSeconds)} layout="none"><Audio src={staticFile(clip.src)} volume={clip.volume} startFrom={secondsToFrames(clip.trimBeforeSeconds??0)}/></Sequence>)}
</AbsoluteFill>};
