"""Original Sumi material-effect synthesizer. Python stdlib only, no samples/API.

Authored modal oscillators, filtered noise, transients and periodic ambience.
These are synthetic material impressions, not acoustic recordings or copies of
provider waveforms. A fixed seed recreates each effect; audition in the film.
"""
from array import array
import math
import random

SR=48000
EXTRA=[
 ('rain-window','ambience',10,True),('night-insects','ambience',10,True),
 ('river-soft','ambience',10,True),('distant-storm','ambience',10,True),
 ('leaf-rustle','nature',2,False),('bird-wing','nature',1.2,False),
 ('stone-roll','foley',2,False),('pebbles-fall','foley',2,False),
 ('sand-step','footstep',1.4,False),('mud-step','footstep',1.4,False),
 ('snow-step','footstep',1.4,False),('running-pair','footstep',2,False),
 ('heartbeat-soft','emotion',2,False),('heartbeat-fast','emotion',2,False),
 ('clock-tick','foley',1,False),('bell-soft','percussion',3,False),
 ('bell-warning','percussion',3,False),('wood-knock','foley',1.5,False),
 ('glass-touch','foley',2,False),('water-pour','foley',3,False),
 ('water-ripple','nature',3,False),('rope-tension','foley',2,False),
 ('flag-flap','foley',2.5,False),('horse-hoof','footstep',1.5,False),
 ('armor-shift','action',2,False),('bow-release','action',1.5,False),
 ('branch-snap','nature',1.5,False),('body-fall','action',2,False),
 ('brush-wide','ink',2,False),('ink-bloom-soft','ink',3,False),
 ('paper-fold','foley',1.5,False),('resolve-chime','emotion',4,False)]


def definitions(catalog):
    base=[{'id':x['id'],'category':x['category'],'duration_seconds':x['duration_seconds'],'loop':x['loop']} for x in catalog['sfx']]
    return base+[dict(id=i,category=c,duration_seconds=d,loop=l) for i,c,d,l in EXTRA]


def render(spec,seed):
    name=spec['id'];d=spec['duration_seconds'];n=round(d*SR)
    if not .05<=d<=20:raise ValueError('Effect duration outside supported range')
    rng=random.Random(seed);out=array('f',[0])*n
    def tone(at,length,f,amp=.3,tau=.2,ratios=(1,1.61,2.37),bend=0):
        start=round(at*SR);count=min(round(length*SR),n-start)
        phases=[0.0]*len(ratios)
        for k in range(max(0,count)):
            t=k/SR;env=min(1,k/96,max(0,(count-1-k)/192))*math.exp(-t/max(.005,tau));v=0
            for j,r in enumerate(ratios):
                phases[j]+=2*math.pi*f*r*(1+bend*math.exp(-t/.025))/SR
                v+=math.sin(phases[j])/(1+j*2.1)
            out[start+k]+=v*env*amp
    def noise(at,length,amp=.3,cutoff=2200,shape='decay',rough=0):
        start=round(at*SR);count=min(round(length*SR),n-start);low=slow=0.0
        alpha=1-math.exp(-2*math.pi*min(cutoff,16000)/SR)
        for k in range(max(0,count)):
            t=k/SR;u=k/max(1,count-1);white=rng.uniform(-1,1);low+=alpha*(white-low);slow+=.009*(white-slow)
            if shape=='swell':env=math.sin(math.pi*u)**2
            elif shape=='rise':env=u*u*min(1,(1-u)*60)
            elif shape=='steady':env=1
            else:env=math.exp(-t/max(.02,length/5))
            edge=min(1,k/96,(count-1-k)/192)
            grain=.4+.6*max(0,math.sin(t*(44+rough*43))) if rough else 1
            out[start+k]+=(low-.45*slow)*amp*env*max(0,edge)*grain
    def cracks(count,at=0,span=.5,metal=False):
        for k in range(count):
            pos=at+rng.random()*span;f=rng.uniform(700,2400) if metal else rng.uniform(130,480)
            tone(pos,.12,f,.1,.025,(1,2.3,4.7) if metal else (1,1.43,2.2))
            noise(pos,.035,.28,6000)
    if spec.get('loop'):
        # All components are periodic in exactly n samples, including cyclic pulses.
        # No fades-to-silence at the join and no copied external ambience.
        dark=name in ('quiet-room','distant-storm');wind=name in ('wind-trees','night-insects')
        if name=='night-insects':
            for j in range(9):
                cycles=rng.randint(round(2200*d),round(4200*d));phase=rng.random()*math.tau
                for k in range(n):
                    u=k/n;chirp=max(0,math.sin(math.tau*(17+j)*u+j))**8
                    out[k]+=.015*math.sin(math.tau*cycles*u+phase)*chirp
        else:
            # Overlap a generated extension into the head so noise crosses the
            # loop seam continuously instead of fading out or becoming a tone.
            cross=round(.3*SR);base=array('f');low=0.0
            alpha=.52 if name.startswith('rain') or name=='river-soft' else .05 if name=='fire-room' else .012
            for k in range(n+cross):
                low+=alpha*(rng.uniform(-1,1)-low);base.append(low)
            for k in range(n):
                u=k/n;value=base[k+cross]
                if k>=n-cross:
                    w=(k-n+cross)/cross;w=w*w*(3-2*w)
                    value=value*(1-w)+base[k-n+cross]*w
                level=.15 if dark else .25 if name.startswith('rain') else .32
                out[k]+=value*level*(1+.16*math.sin(math.tau*2*u))
            if name=='distant-storm':
                for j in range(6):
                    cycles=rng.randint(round(28*d),round(85*d));phase=rng.random()*math.tau
                    for k in range(n):
                        u=k/n;out[k]+=.025*math.sin(math.tau*cycles*u+phase)*(.5+.5*math.sin(math.tau*u))**2
        if name in ('rain-open','rain-window','fire-room','river-soft'):
            count=140 if name.startswith('rain') else 48
            for j in range(count):
                at=rng.randrange(n);length=rng.randint(250,1700);freq=rng.uniform(850,7000);amp=rng.uniform(.015,.07)
                for k in range(length):
                    t=k/SR;v=amp*math.sin(math.tau*freq*t)*math.exp(-k/(length/6))*min(1,k/15,(length-k)/40)
                    out[(at+k)%n]+=v
    elif name.startswith('step-') or name in ('sand-step','mud-step','snow-step','running-pair','horse-hoof'):
        freq={'step-stone':180,'step-gravel':220,'step-wood':105,'step-grass':100,'sand-step':130,'mud-step':75,'snow-step':200,'horse-hoof':210}.get(name,150)
        starts=[.02,.38,.77,1.14] if name=='running-pair' else [.025]
        for at in starts:
            tone(at,.38,freq,.3,.065,(1,1.72,2.3));tone(at+.13,.22,freq*.78,.12,.045)
            noise(at,.34,.65 if name in ('step-gravel','sand-step','snow-step') else .3,3400 if name!='mud-step' else 650,rough=1)
            if name=='step-gravel':cracks(8,at,.2)
            if name=='horse-hoof':tone(at+.085,.15,380,.26,.035,(1,2,3))
    elif name.startswith('ink-') or name in ('brush-wide','ink-bloom-soft'):
        if name=='ink-drop':
            tone(.025,.55,440,.42,.1,(1,1.8),-.55);noise(.035,.22,.6,1400);tone(.12,.5,175,.14,.15)
        else:
            wet=name in ('ink-wet','ink-splash','ink-bloom-soft');noise(.015,d-.03,.75,1100 if wet else 6500,'swell',.6 if not wet else .2)
            if name=='ink-splash':cracks(7,.015,.3);tone(.02,.55,110,.25,.15)
            if name=='ink-bloom-soft':tone(.08,1.3,135,.16,.45,(1,1.12))
    elif name in ('paper-turn','scroll-open','paper-fold','cloth-move','cloth-grip','flag-flap','rope-tension','leaf-rustle','bird-wing'):
        pulses=3 if name in ('flag-flap','bird-wing','leaf-rustle') else 1
        for j in range(pulses):
            at=.02+j*d/pulses;length=d/pulses-.04
            cutoff=5600 if name.startswith('paper') else 3100 if name=='scroll-open' else 1400
            noise(at,length,.6,cutoff,'swell',1)
        if name=='rope-tension':tone(.1,1.6,240,.12,.7,(1,1.006),.22)
        if name=='cloth-grip':noise(.05,.4,.3,900,'decay',2)
    elif name in ('cup-set','tray-set','glass-touch','bell-soft','bell-warning','resolve-chime'):
        freqs={'cup-set':(740,1490),'tray-set':(470,1260),'glass-touch':(1260,2850),'bell-soft':(660,990),'bell-warning':(440,466),'resolve-chime':(523.25,659.25,783.99)}[name]
        for j,f in enumerate(freqs):tone(.02+j*.12,d-.03-j*.12,f,.24,.5 if name in ('cup-set','tray-set') else .9,(1,2.71,4.13))
        if name in ('cup-set','tray-set'):noise(.02,.05,.25,6000)
    elif name in ('door-open','door-slam','wood-knock','wood-break','branch-snap','stone-roll','pebbles-fall','body-fall'):
        tone(.02,min(d-.03,.8),65 if name=='body-fall' else 135,.48,.18,(1,1.53,2.19));noise(.02,.28,.45,1800)
        if name in ('wood-break','branch-snap','pebbles-fall','stone-roll'):cracks(11 if name=='wood-break' else 5,.03,d*.65)
        if name=='door-open':tone(.22,d-.25,350,.15,.8,(1,1.01),.14);noise(.1,d-.15,.25,700,'swell',2)
    elif name in ('sword-draw','sword-clash','shield-hit','armor-shift','arrow-impact','bow-release'):
        if name=='sword-draw':noise(.01,1.1,.55,7000,'swell',.3);tone(.45,.9,1400,.1,.3,(1,2.4,4.7))
        elif name=='bow-release':tone(.02,.6,160,.42,.1,(1,2,3),-.35);noise(.025,.35,.32,4000)
        elif name=='arrow-impact':tone(.03,.45,160,.4,.08,(1,1.4,2.2));noise(.02,.07,.65,5600);tone(.06,.6,600,.1,.16)
        elif name=='shield-hit':tone(.02,.8,95,.5,.17,(1,1.65,2.8));noise(.02,.12,.5,3500)
        else:
            cracks(5 if name=='armor-shift' else 1,.02,.85 if name=='armor-shift' else .01,True)
            for j,f in enumerate((690,1070,1910,3310)):tone(.03+j*.006,1.5,f,.25/(j+1),.36,(1,1.41))
    elif name in ('drum-low','drum-heavy','heartbeat-soft','heartbeat-fast'):
        if name.startswith('heartbeat'):
            period=.55 if name.endswith('fast') else .9
            for j in range(math.ceil(d/period)):
                for offset,g in [(0,.46),(.13,.24)]:tone(.02+j*period+offset,.24,52,g,.07,(1,1.55),.35)
        else:
            tone(.015,d-.02,43 if name=='drum-heavy' else 68,.6,.5 if name=='drum-heavy' else .32,(1,1.59,2.14,2.64),.55);noise(.015,.055,.5,3600)
    elif name=='clock-tick':tone(.02,.12,1900,.4,.015,(1,1.9));noise(.02,.025,.4,9000)
    elif name in ('water-pour','water-ripple'):
        noise(.02,d-.04,.4,1800,'swell',.6)
        for j in range(22 if name=='water-pour' else 8):
            at=.03+rng.random()*(d-.3);tone(at,.25,rng.uniform(380,1300),.11,.055,(1,1.8),-.35)
    else:
        noise(.01,d-.02,.65,2400,'rise' if name=='tension-rise' else 'swell')
        if name=='dark-sting':tone(.01,3.5,42,.45,.75,(1,1.059,1.5));cracks(3,.04,.35,True)
        if name=='arrow-pass':noise(.08,.35,.5,6500,'swell')
    # Remove tiny synthesis DC; preserve purposeful level, not full-scale normalization.
    mean=sum(out)/n;peak=max(abs(x-mean) for x in out);scale=min(1,.67/max(.0001,peak))
    result=[array('f'),array('f')]
    for k,x in enumerate(out):
        pan=.65*math.sin(math.pi*(k/n-.5)) if name in ('arrow-pass','air-short','air-slow','bird-wing') else .08*math.sin(math.tau*k/n)
        value=(x-mean)*scale;result[0].append(value*math.cos((pan+1)*math.pi/4));result[1].append(value*math.sin((pan+1)*math.pi/4))
    return result
