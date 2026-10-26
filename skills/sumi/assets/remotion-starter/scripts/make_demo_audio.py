#!/usr/bin/env python3
"""Generate a bounded smoke-test score; replace it with story-specific music for a film."""
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
p=json.loads((root/'project.json').read_text());duration=round(p['durationSeconds']*p['fps'])/p['fps']
if duration<.1 or duration>120:raise SystemExit('Demo synthesis supports 0.1–120 seconds; section longer films.')
folder=root/'public'/'demo-score'
if folder.exists():raise SystemExit('public/demo-score exists; preserve it or choose a fresh project.')
score={'duration':duration,'seed':21,'ceiling_db':-9,'fade_in':min(.1,duration/4),'fade_out':min(.5,duration/4),'beds':[{'at':0,'duration':duration,'gain':.045,'chords':[[0,[174.61,220,261.63]]]}],'events':[],'ducks':[]}
for i in range(int(duration)):
    length=min(.6,duration-i-.02)
    if length>.01:score['events'].append({'at':i+.02,'duration':length,'kind':'pluck','freq':[349.23,440,523.25][i%3],'gain':.09,'stem':'music'})
source=root/'demo-score.json';source.write_text(json.dumps(score,indent=2))
subprocess.run([sys.executable,str(root/'audio-tools'/'render_audio.py'),str(source),'--out',str(folder)],check=True)
p['audio'].append({'src':'demo-score/background.wav','startSeconds':0,'durationSeconds':duration,'volume':1})
(root/'project.json').write_text(json.dumps(p,indent=2)+'\n')
print('Attached one synthesized background track. Do not also attach its music/sfx stems.')
