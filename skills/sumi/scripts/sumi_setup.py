#!/usr/bin/env python3
"""Read-only dependency doctor; project installation is preview-only unless explicitly approved."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import urllib.request
from sumi_catalog import VERSION, CATALOG_ID, STYLES

def command_argv(argv, windows=None):
    """npm is a .cmd launcher on Windows; invoke it through the OS command interpreter."""
    windows = os.name == 'nt' if windows is None else windows
    if windows and str(argv[0]).lower().endswith(('.cmd','.bat')):
        return [os.environ.get('COMSPEC','cmd.exe'),'/d','/s','/c',subprocess.list2cmdline(argv)]
    return argv

def run(argv, cwd=None):
    try:
        r=subprocess.run(command_argv(argv),cwd=cwd,capture_output=True,text=True,timeout=15)
        return {'exit_code':r.returncode,'output':(r.stdout or r.stderr).strip()[:2500]}
    except (OSError,subprocess.TimeoutExpired) as e:
        return {'exit_code':None,'output':type(e).__name__}

def command(name,args=('--version',),minimum=None):
    path=shutil.which(name)
    if not path: return {'status':'not_found_on_PATH','path':None}
    result=run([path,*args]); out=result['output']
    status='available' if result['exit_code']==0 else 'needs_checking'
    match=re.search(r'(\d+)\.(\d+)',out)
    if status=='available' and minimum:
        if not match: status='needs_checking'
        elif tuple(map(int,match.groups()))<minimum: status='incompatible'
    return {'status':status,'path':path,'version':out.splitlines()[0] if out else None}

def app_paths():
    home=Path.home()
    chrome=[Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),home/'Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
    voicebox=[Path('/Applications/Voicebox.app'),home/'Applications/Voicebox.app']
    if os.name=='nt':
        for env in ['LOCALAPPDATA','PROGRAMFILES','PROGRAMFILES(X86)']:
            base=os.environ.get(env)
            if base:
                chrome.append(Path(base)/'Google/Chrome/Application/chrome.exe')
                voicebox += [Path(base)/'Voicebox/Voicebox.exe',Path(base)/'voicebox/voicebox.exe']
    for name in ['google-chrome','google-chrome-stable','chromium','chromium-browser']:
        found=shutil.which(name)
        if found: chrome.append(Path(found))
    found=shutil.which('voicebox')
    if found: voicebox.append(Path(found))
    return {'chrome':next((str(p) for p in chrome if p.is_file()),None),
            'voicebox':next((str(p) for p in voicebox if p.exists()),None)}

def memory_gib():
    try:
        if sys.platform=='darwin':
            return round(int(run(['/usr/sbin/sysctl','-n','hw.memsize'])['output'])/2**30,1)
        if sys.platform.startswith('linux'):
            return round(int(re.search(r'MemTotal:\s+(\d+)',Path('/proc/meminfo').read_text()).group(1))*1024/2**30,1)
        if os.name=='nt':
            import ctypes
            class Status(ctypes.Structure):
                _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(name,ctypes.c_ulonglong) for name in ['total','available','page_total','page_available','virtual_total','virtual_available','extended']]
            s=Status();s.length=ctypes.sizeof(s)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)): return round(s.total/2**30,1)
    except (OSError,ValueError,AttributeError): pass
    return None

def project_packages(project):
    manifest=project/'package.json'; lock=project/'package-lock.json'
    if not manifest.is_file() or not lock.is_file():
        return {'status':'missing_manifest_or_lockfile','ready':False}
    data=json.loads(manifest.read_text(encoding='utf-8'))
    required={**data.get('dependencies',{}),**data.get('devDependencies',{})}
    versions={}
    for name,wanted in required.items():
        installed=project/'node_modules'/name/'package.json'
        try: actual=json.loads(installed.read_text(encoding='utf-8')).get('version')
        except (OSError,ValueError): actual=None
        versions[name]={'wanted':wanted,'installed':actual,'matches':actual==wanted}
    direct_match=bool(versions) and all(v['matches'] for v in versions.values())
    health=run([shutil.which('npm'),'ls','--depth=0','--json'],cwd=project) if direct_match and shutil.which('npm') else None
    ready=direct_match and health is not None and health['exit_code']==0
    return {'status':'ready' if ready else 'missing_or_needs_checking','ready':ready,'packages':versions,
            'npm_dependency_check_passed':health is not None and health['exit_code']==0}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def voicebox_status(port=17493):
    # Only loopback, no proxy, no model downloads or generation. Do not return profile/audio data.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    result={'url':f'http://127.0.0.1:{port}','status':'not_reachable','models':[]}
    try:
        with opener.open(result['url']+'/models/status',timeout=2) as response:
            raw=response.read(1024*1024+1)
        if len(raw)>1024*1024: raise ValueError('Oversized local response')
        data=json.loads(raw)
        models=data.get('models') if isinstance(data,dict) else None
        if not isinstance(models,list): raise ValueError('Unknown model status schema')
        result['status']='responding'
        result['models']=[{k:m.get(k) for k in ['model_name','display_name','downloaded','loaded','size_mb']} for m in models if isinstance(m,dict)]
    except (OSError,ValueError): pass
    return result

def doctor(project=None,check_voicebox=False,port=17493):
    apps=app_paths()
    tools={n:command(n,minimum=m) for n,m in [('node',(20,0)),('npm',None)]}
    tools.update({n:command(n,args=('-version',)) for n in ['ffmpeg','ffprobe']})
    tools['python']={'status':'available' if sys.version_info>=(3,9) else 'incompatible','path':sys.executable,'version':platform.python_version()}
    for name,path in apps.items(): tools[name]={'status':'found_not_runtime_tested' if path else 'not_found_in_known_locations','path':path}
    result={'version':VERSION,'catalog':CATALOG_ID,'styles':[{'id':key,'name':value['name']} for key,value in STYLES.items()],
            'checked_at':datetime.now(timezone.utc).isoformat(),'system':platform.system(),'architecture':platform.machine(),
            'ram_gib':memory_gib(),'free_disk_gib':round(shutil.disk_usage(project or Path.cwd()).free/2**30,1),'tools':tools,
            'image_generation':{'status':'unknown','next_action':'Host agent must inspect callable image tools/MCP before selecting artwork route.'},
            'render_browser':'Not launched; use a compatible existing browser or approve a download.',
            'cost_notes':{'python_audio':'Free bundled standard-library synthesis','remotion':'Free only under applicable eligibility; see official license','voicebox':'Optional free local app; selected model download and hardware required','elevenlabs':'Optional account allowance/paid usage; no key is read by this doctor'}}
    if project: result['project']=project_packages(project)
    if check_voicebox: result['voicebox_server']=voicebox_status(port)
    return result

def install_project(project,approved=False):
    state=project_packages(project)
    if state['ready']: return {'action':'reused','project':str(project),'message':'Matching packages already available; nothing installed.'}
    if state['status']=='missing_manifest_or_lockfile': raise ValueError('A package manifest and lockfile are required; nothing installed.')
    node=command('node',minimum=(20,0));npm=shutil.which('npm')
    plan={'action':'approval_required','project':str(project),'command':['npm','ci'],'source':'Project package-lock.json registries',
          'effects':'Downloads third-party packages and may execute their installation scripts in this project.',
          'cost':'Remotion license eligibility applies; no subscription or media generation is started.'}
    if not approved: return plan
    if node['status']!='available' or not npm: raise ValueError('Compatible Node 20+ and npm are required. Resolve setup first.')
    subprocess.run(command_argv([npm,'ci']),cwd=project,check=True)
    checked=project_packages(project)
    if not checked['ready']: raise ValueError('Installation returned but package verification did not pass. Inspect the project; do not repeat blindly.')
    return {'action':'installed_and_verified','project':str(project),'packages':checked['packages']}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='action',required=True)
    d=sub.add_parser('doctor');d.add_argument('--project',type=Path);d.add_argument('--voicebox',action='store_true');d.add_argument('--voicebox-port',type=int,default=17493)
    i=sub.add_parser('install-project');i.add_argument('project',type=Path);i.add_argument('--approved',action='store_true',help='Use only after the user approved this concrete third-party installation.')
    a=p.parse_args()
    try:
        project=a.project.expanduser().resolve() if a.project else None
        if project and not project.is_dir(): raise ValueError('Project directory does not exist.')
        if a.action=='doctor':
            if not 1<=a.voicebox_port<=65535: raise ValueError('Invalid local port.')
            result=doctor(project,a.voicebox,a.voicebox_port)
        else: result=install_project(project,a.approved)
        print(json.dumps(result,indent=2,ensure_ascii=False))
    except (OSError,ValueError,subprocess.SubprocessError) as e:p.exit(1,f'Setup stopped: {e}\n')

if __name__=='__main__':main()
