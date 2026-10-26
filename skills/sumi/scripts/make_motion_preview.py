#!/usr/bin/env python3
"""Package an existing short silent proof as image animation plus original MP4."""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path


def inspect_clip(source):
    data=json.loads(subprocess.check_output([
        'ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(source)]))
    streams=data.get('streams',[])
    videos=[s for s in streams if s.get('codec_type')=='video']
    if len(videos)!=1 or any(s.get('codec_type')=='audio' for s in streams):
        raise ValueError('Use one short silent technical proof. Keep a full film and its sound in the standard MP4 dashboard.')
    video=videos[0]
    fps=Fraction(video['avg_frame_rate'])
    if fps not in (24,30) or Fraction(video['r_frame_rate'])!=fps:
        raise ValueError('Use a constant-rate24/30fps proof; do not retime it for this preview.')
    count=int(video['nb_read_frames'])
    duration=float(video['duration'])
    if count<2 or not 0<duration<=10 or abs(count/float(fps)-duration)>0.002:
        raise ValueError('Use an entire proof of at most10seconds with complete constant-rate timing.')
    timestamps=json.loads(subprocess.check_output([
        'ffprobe','-v','error','-select_streams','v:0','-show_frames',
        '-show_entries','frame=best_effort_timestamp_time','-of','json',str(source)]))['frames']
    times=[float(frame['best_effort_timestamp_time']) for frame in timestamps]
    if len(times)!=count or any(abs((t-times[0])-n/float(fps))>0.001 for n,t in enumerate(times)):
        raise ValueError('Variable or incomplete frame timestamps require a separately prepared proof.')
    return {'fps':int(fps),'frames':count,'duration':duration,
            'width':int(video['width']),'height':int(video['height'])}


def preview_geometry(width,height,limit,count):
    scale=min(1,limit/width,720/height)
    w=max(2,int(width*scale)//2*2)
    h=max(2,int(height*scale)//2*2)
    if w*h*count>180_000_000:
        raise ValueError('This preview exceeds the local memory budget. Choose a smaller --width or a shorter proof.')
    return w,h


def frame_durations(count,fps):
    return [round((n+1)*1000/fps)-round(n*1000/fps) for n in range(count)]


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def make(source,dest,title,before=None,width=960):
    from PIL import Image,features
    if not features.check('webp_anim'):
        raise ValueError('Animated WebP support is unavailable. Detect setup and ask before installing anything.')
    source=source.expanduser().resolve()
    dest=dest.expanduser().absolute()
    if dest.exists() or dest.is_symlink():raise ValueError('Output already exists; use a new revision folder.')
    info=inspect_clip(source)
    w,h=preview_geometry(info['width'],info['height'],width,info['frames'])
    if before:
        before=before.expanduser().resolve()
        with Image.open(before) as image:
            if not math.isclose(image.width/image.height,info['width']/info['height'],rel_tol=0.01):
                raise ValueError('Before artwork needs the same composition/aspect; do not stretch it to match.')
    skill=Path(__file__).resolve().parents[1]
    assets=skill/'assets/delivery-dashboard'
    for name in ['proof.html','proof-player.js','serve.py','logo.png','brand.css','proof.css','brand.html','brand-page.css','wordmark.svg']:
        if not (assets/name).is_file():raise ValueError(f'Incomplete preview bundle: {name}')
    process=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-map','0:v:0',
        '-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
    frames=[]
    try:
        size=w*h*3
        while True:
            block=process.stdout.read(size)
            if not block:break
            if len(block)!=size:raise ValueError('Incomplete decoded image frame.')
            frames.append(Image.frombytes('RGB',(w,h),block))
        if process.wait()!=0 or len(frames)!=info['frames']:
            raise ValueError('Decoded frame count does not match the inspected proof.')
        dest.mkdir(parents=True)
        times=frame_durations(len(frames),info['fps'])
        frames[0].save(dest/'motion.webp','WEBP',save_all=True,append_images=frames[1:],
            duration=times,loop=1,quality=85,method=3,kmin=9,kmax=17)
        frames[len(frames)//2].save(dest/'poster.png')
        if before:
            with Image.open(before) as image:image.convert('RGB').save(dest/'before.png')
        else:frames[0].save(dest/'before.png')
        with Image.open(dest/'motion.webp') as image:
            actual_count=image.n_frames
            duration=0
            for n in range(actual_count):
                image.seek(n);image.load();duration+=image.info.get('duration',0)
        if actual_count<2 or duration!=sum(times):
            raise ValueError('The image preview has no distinct animation or incomplete duration; preserve this partial folder for diagnosis.')
        shutil.copy2(source,dest/'proof.mp4')
        for src,target in [('proof.html','index.html'),('proof-player.js','proof-player.js'),('serve.py','serve.py'),('logo.png','logo.png'),('brand.css','brand.css'),('proof.css','proof.css'),('brand.html','brand.html'),('brand-page.css','brand-page.css'),('wordmark.svg','wordmark.svg')]:
            shutil.copy2(assets/src,dest/target)
        metadata={'title':title,'duration':sum(times)/1000,'fps':info['fps'],
            'source_frames':info['frames'],'encoded_image_frames':actual_count,
            'preview_size':[w,h],'source_size':[info['width'],info['height']],
            'before_label':'Before · still artwork' if before else 'First frame',
            'source_sha256':digest(source),'mp4_sha256':digest(dest/'proof.mp4'),
            'preview_sha256':digest(dest/'motion.webp'),'before_source_sha256':digest(before) if before else None,
            'visual_review':'pending','audio':'silent technical proof; not a soundtrack review'}
        assert metadata['source_sha256']==metadata['mp4_sha256']
        (dest/'preview.json').write_text(json.dumps(metadata,indent=2)+'\n')
        (dest/'data.js').write_text('window.SUMI_PROOF='+json.dumps(metadata,ensure_ascii=True).replace('<','\\u003c')+';\n')
        return metadata
    finally:
        if process.poll() is None:process.kill();process.wait()
        process.stdout.close()
        for image in frames:image.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path);parser.add_argument('destination',type=Path)
    parser.add_argument('--title',default='Motion proof');parser.add_argument('--before',type=Path)
    parser.add_argument('--width',type=int,default=960)
    args=parser.parse_args()
    if not 160<=args.width<=1280:parser.error('Preview width must be160–1280; full-HD MP4 stays unchanged.')
    try:result=make(args.source,args.destination,args.title,args.before,args.width)
    except ImportError:parser.exit(1,'Pillow is missing. Detect setup and ask before a third-party install; the normal MP4 dashboard remains available.\n')
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as error:parser.exit(1,f'Preview not completed: {error}\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
