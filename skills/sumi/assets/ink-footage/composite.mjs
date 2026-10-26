// Render-neutral Canvas adapter. Supply a decoded frame from the film's clock.
// No scene timing, media playback, style selection or review is inferred here.
export function sourceFrame(outputFrame, {startFrame, durationFrames, sourceFrames}) {
  if (![outputFrame,startFrame,durationFrames,sourceFrames].every(Number.isInteger) ||
      durationFrames < 2 || sourceFrames < 2) throw new RangeError('Integer frames and durations >= 2 required');
  if (outputFrame < startFrame) return null;
  return Math.round(Math.min(1,(outputFrame-startFrame)/(durationFrames-1))*(sourceFrames-1));
}
export function isDarkRed(color) {
  if (!/^#[0-9a-f]{6}$/i.test(color)) return false;
  const [r,g,b]=[1,3,5].map(i=>parseInt(color.slice(i,i+2),16));
  return r>=64 && r<=180 && r>=1.6*g && r>=1.6*b;
}
export function checkedColor(color, style='light') {
  if (!/^#[0-9a-f]{6}$/i.test(color)) throw new TypeError('Use a six-digit hex color');
  if (!['light','dark'].includes(style)) throw new Error('This splash library is for Light/Dark; preserve Original');
  const rgb=[1,3,5].map(i=>parseInt(color.slice(i,i+2),16));
  if(style==='dark' && !(rgb[0]===rgb[1]&&rgb[1]===rgb[2]) && !isDarkRed(color)) throw new Error('Dark ink requires neutral pigment or selective dark red');
  return color;
}
export function createInkPainter(width, height, makeCanvas=()=>document.createElement('canvas')) {
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1)throw new RangeError('Positive raster dimensions required');
  const mask=makeCanvas();mask.width=width;mask.height=height;
  const m=mask.getContext('2d',{willReadFrequently:true});
  const layer=makeCanvas();layer.width=width;layer.height=height;
  const l=layer.getContext('2d');
  function decode(source,kind){
    m.globalCompositeOperation='source-over';m.clearRect(0,0,width,height);m.drawImage(source,0,0,width,height);
    if(kind==='matte'){
      const im=m.getImageData(0,0,width,height);
      for(let i=0;i<im.data.length;i+=4){const a=im.data[i];im.data[i]=im.data[i+1]=im.data[i+2]=0;im.data[i+3]=a;}
      m.putImageData(im,0,0);
    }else if(kind!=='alpha')throw new Error('kind must be alpha or matte');
  }
  return {
    overlay(ctx, source, {color='#111111',style='light',kind='alpha',x=0,y=0,w=width,h=height,opacity=1}={}){
      checkedColor(color,style);decode(source,kind);
      m.globalCompositeOperation='source-in';m.fillStyle=color;m.fillRect(0,0,width,height);m.globalCompositeOperation='source-over';
      ctx.save();ctx.globalAlpha*=Math.max(0,Math.min(1,opacity));ctx.drawImage(mask,x,y,w,h);ctx.restore();
    },
    reveal(ctx, incoming, source, {kind='alpha',x=0,y=0,w=width,h=height}={}){
      decode(source,kind);l.globalCompositeOperation='source-over';l.clearRect(0,0,width,height);l.drawImage(incoming,0,0,width,height);
      l.globalCompositeOperation='destination-in';l.drawImage(mask,0,0);l.globalCompositeOperation='source-over';ctx.drawImage(layer,x,y,w,h);
    }
  };
}
