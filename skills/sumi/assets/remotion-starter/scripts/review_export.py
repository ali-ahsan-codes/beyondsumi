#!/usr/bin/env python3
"""Inspect a rendered export, decode it and create a contact sheet; not an artistic review."""
import argparse,json,pathlib,shutil,subprocess,sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=pathlib.Path);a=p.parse_args()
    root=pathlib.Path(__file__).resolve().parents[1];cfg=json.loads((root/'project.json').read_text())
    for exe in ['ffmpeg','ffprobe']:
        if not shutil.which(exe):p.error(f'{exe} is required on PATH')
    video=a.video.resolve()
    if not video.is_file():p.error('Rendered video does not exist')
    reportdir=root/'out'/'review';reportdir.mkdir(parents=True,exist_ok=True)
    def run(cmd):return subprocess.run(cmd,capture_output=True,text=True)
    probe=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)])
    if probe.returncode:p.exit(1,probe.stderr)
    data=json.loads(probe.stdout);vs=[s for s in data['streams'] if s['codec_type']=='video'];aus=[s for s in data['streams'] if s['codec_type']=='audio'];errors=[]
    if len(vs)!=1:errors.append('Expected one video stream')
    else:
        v=vs[0];num,den=map(int,v['r_frame_rate'].split('/'));expected=round(cfg['durationSeconds']*cfg['fps'])/cfg['fps']
        if (v['width'],v['height'])!=(cfg['width'],cfg['height']):errors.append('Dimensions mismatch')
        if num/den!=cfg['fps']:errors.append('FPS mismatch')
        if abs(float(v.get('duration',data['format']['duration']))-expected)>1/cfg['fps']+.001:errors.append('Picture duration mismatch')
    if cfg['audio'] and not aus:errors.append('Configured audio absent')
    decode=run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'])
    if decode.returncode or decode.stderr.strip():errors.append('Decode reported errors: '+decode.stderr[-1500:])
    duration=float(data['format']['duration']);interval=max(duration/12,.01)
    sheet=run(['ffmpeg','-v','error','-y','-i',str(video),'-vf',f'fps=1/{interval},scale=320:320:force_original_aspect_ratio=decrease,pad=320:320:(ow-iw)/2:(oh-ih)/2:color=0x172630,tile=4x3','-frames:v','1',str(reportdir/'contact.jpg')])
    if sheet.returncode:errors.append('Contact-sheet generation failed')
    if aus:
        loud=run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-']);(reportdir/'audio-analysis.txt').write_text(loud.stderr)
        if loud.returncode:errors.append('Audio analysis failed')
    report={'video':str(video),'technical_pass':not errors,'errors':errors,'streams':data['streams'],'format':data['format'],'visual_review':'pending human/agent inspection','full_playback':'pending','listening':'pending; numerical audio analysis is not listening'}
    (reportdir/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'technical_pass':not errors,'errors':errors,'report':str(reportdir/'report.json')}));return int(bool(errors))
if __name__=='__main__':sys.exit(main())
