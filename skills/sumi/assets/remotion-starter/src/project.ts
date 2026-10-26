import raw from '../project.json';
import type {CaptionCue} from './components';
export type AudioClip={src:string;startSeconds:number;durationSeconds:number;volume:number;trimBeforeSeconds?:number};
export type Project={style:string;catalog?:string;method?:string;variation?:string;title:string;width:number;height:number;fps:number;durationSeconds:number;audio:AudioClip[];captions:CaptionCue[]};
export const project:Project=raw;
for(const k of ['width','height','fps','durationSeconds'] as const){if(!Number.isFinite(project[k])||project[k]<=0)throw new Error(`Invalid project.${k}`);}
if(!Number.isInteger(project.width)||!Number.isInteger(project.height)||project.width%2||project.height%2)throw new Error('H.264 dimensions must be positive even integers');
export const secondsToFrames=(seconds:number)=>Math.round(seconds*project.fps);
export const durationInFrames=secondsToFrames(project.durationSeconds);
if(durationInFrames<1)throw new Error('Duration must contain at least one frame');
for(const clip of project.audio){if(!clip.src||/^(\/|https?:|[A-Z]:)/i.test(clip.src)||clip.src.split('/').includes('..'))throw new Error('Audio src must be a public-relative asset');if(![clip.startSeconds,clip.durationSeconds,clip.volume,clip.trimBeforeSeconds??0].every(Number.isFinite)||clip.startSeconds<0||clip.durationSeconds<=0||clip.volume<0||(clip.trimBeforeSeconds??0)<0||secondsToFrames(clip.startSeconds)+secondsToFrames(clip.durationSeconds)>durationInFrames)throw new Error(`Audio outside timeline: ${clip.src}`);}

for(const cue of project.captions){if(!Number.isFinite(cue.start)||!Number.isFinite(cue.end)||cue.start<0||cue.end<=cue.start||cue.end>durationInFrames/project.fps||!cue.text)throw new Error('Invalid caption timing/text');}
