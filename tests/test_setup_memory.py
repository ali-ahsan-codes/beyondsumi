"""Offline contract tests. No installs, real account calls, model downloads or media generation."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/sumi'
sys.path.insert(0,str(SKILL/'scripts'))
import sumi_memory as memory
import sumi_setup as setup

def load_voice():
    spec=importlib.util.spec_from_file_location('sumi_test_voice',SKILL/'assets/remotion-starter/scripts/elevenlabs_voice.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class Contracts(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def project(self):
        p=self.root/'film';p.mkdir();(p/'package.json').write_text(json.dumps({'dependencies':{'remotion':'4.0.516'}}));(p/'package-lock.json').write_text('{}');return p
    def cli(self,script,*args,ok=True):
        r=subprocess.run([sys.executable,str(SKILL/'scripts'/script),*map(str,args)],capture_output=True,text=True)
        if ok:self.assertEqual(r.returncode,0,r.stderr)
        else:self.assertNotEqual(r.returncode,0)
        return r

    def test_memory_read_does_not_create_files(self):
        p=self.root/'new/user.json';self.assertEqual(memory.read(p)['preferences'],{});self.assertFalse(p.parent.exists())

    def test_explicit_preferences_persist_and_forget_only_target(self):
        state=self.root/'state'
        self.cli('sumi_memory.py','--state-dir',state,'set','narration_provider','none','--reason','User asked for no voice by default')
        self.cli('sumi_memory.py','--state-dir',state,'set','storage','local','--reason','User wants local work')
        self.cli('sumi_memory.py','--state-dir',state,'forget','narration_provider')
        data=memory.read(state/'user.json');self.assertNotIn('narration_provider',data['preferences']);self.assertEqual(data['preferences']['storage']['value'],'local')

    def test_credentials_and_unknown_fields_rejected_without_write(self):
        for key,value in [('api_key','private'),('narration_model','sk_abcdefghijklmnop123456')]:
            self.cli('sumi_memory.py','--state-dir',self.root/'state','set',key,value,'--reason','Test rejection',ok=False)
        self.assertFalse((self.root/'state/user.json').exists())

    def test_install_and_first_run_markers_are_independent(self):
        self.cli('sumi_memory.py','--state-dir',self.root,'mark','installation')
        data=memory.read(self.root/'user.json');self.assertIn('installation',data['onboarding']);self.assertNotIn('first_run',data['onboarding'])
        self.cli('sumi_memory.py','--state-dir',self.root,'mark','first_run')
        self.assertEqual(set(memory.read(self.root/'user.json')['onboarding']),{'installation','first_run'})

    def test_bad_memory_preserved(self):
        p=self.root/'user.json';p.write_text('{broken')
        self.cli('sumi_memory.py','--state-dir',self.root,'set','storage','local','--reason','Explicit choice',ok=False)
        self.assertEqual(p.read_text(),'{broken')

    def test_dependency_preview_never_invokes_installer(self):
        p=self.project()
        with patch.object(setup,'command',return_value={'status':'available'}),patch.object(setup.shutil,'which',return_value='/fake/npm'),patch.object(setup.subprocess,'run') as runner:
            result=setup.install_project(p,False)
        self.assertEqual(result['action'],'approval_required');runner.assert_not_called();self.assertFalse((p/'node_modules').exists())

    def test_existing_matching_dependencies_are_reused(self):
        p=self.project();installed=p/'node_modules/remotion';installed.mkdir(parents=True);(installed/'package.json').write_text('{"version":"4.0.516"}')
        with patch.object(setup.shutil,'which',return_value='/fake/npm'),patch.object(setup,'run',return_value={'exit_code':0,'output':'{}'}) as runner:
            result=setup.install_project(p,True)
        self.assertEqual(result['action'],'reused');self.assertEqual(runner.call_args.args[0][1],'ls')

    def test_wrong_dependency_version_is_not_ready(self):
        p=self.project();installed=p/'node_modules/remotion';installed.mkdir(parents=True);(installed/'package.json').write_text('{"version":"4.0.100"}')
        self.assertFalse(setup.project_packages(p)['ready'])

    def test_missing_and_old_node_are_distinct(self):
        with patch.object(setup.shutil,'which',return_value=None):self.assertEqual(setup.command('node',minimum=(20,0))['status'],'not_found_on_PATH')
        with patch.object(setup.shutil,'which',return_value='/fake/node'),patch.object(setup,'run',return_value={'exit_code':0,'output':'v18.20.0'}):self.assertEqual(setup.command('node',minimum=(20,0))['status'],'incompatible')

    def test_windows_npm_launcher_uses_command_interpreter(self):
        args=setup.command_argv(['C:\\Program Files\\nodejs\\npm.cmd','ci'],windows=True)
        self.assertEqual(args[1:4],['/d','/s','/c']);self.assertIn('"C:\\Program Files\\nodejs\\npm.cmd"',args[4])
        self.assertEqual(setup.command_argv(['/usr/bin/node','--version'],windows=False),['/usr/bin/node','--version'])

    def test_local_voicebox_detection_gets_only_status(self):
        calls=[]
        class Opener:
            def open(self,url,timeout):
                calls.append(url);return io.BytesIO(b'{"models":[{"model_name":"kokoro","downloaded":true,"loaded":false,"secret":"omit"}]}')
        with patch.object(setup.urllib.request,'build_opener',return_value=Opener()):result=setup.voicebox_status(17493)
        self.assertEqual(calls,['http://127.0.0.1:17493/models/status']);self.assertTrue(result['models'][0]['downloaded']);self.assertNotIn('secret',result['models'][0])

    def test_initializer_creates_memory_and_refuses_overwrite(self):
        dest=self.root/'film'
        self.cli('new_remotion_project.py',dest,'--method','drawn-acting','--title','A small kindness','--seconds','12')
        self.assertTrue((dest/'SUMI-PROJECT.md').is_file());self.assertTrue((dest/'DIRECTION-PLAN.md').is_file())
        self.assertEqual(json.loads((dest/'project.json').read_text())['storyPlanStatus'],'not-authored')
        self.cli('new_remotion_project.py',dest,ok=False)
        self.assertFalse((dest/'node_modules').exists())

    def test_skill_update_backs_up_old_files_preserves_user_preferences(self):
        dest=self.root/'skills/sumi';dest.mkdir(parents=True);(dest/'SKILL.md').write_text('old skill')
        state=self.root/'state';memory.write(state/'user.json',{'schema_version':1,'preferences':{'storage':{'value':'local','reason':'user'}},'onboarding':{'first_run':{'shown_at':'earlier'}}})
        self.cli('install_skill.py','--destination',dest,'--state-dir',state,ok=False)
        self.cli('install_skill.py','--destination',dest,'--state-dir',state,'--replace')
        backups=list((self.root/'sumi-skill-backups').glob('*/SKILL.md'));self.assertEqual(len(backups),1);self.assertEqual(backups[0].read_text(),'old skill')
        data=memory.read(state/'user.json');self.assertEqual(data['preferences']['storage']['value'],'local');self.assertEqual(data['onboarding']['first_run']['shown_at'],'earlier')
        self.assertEqual((dest/'SKILL.md').read_bytes(), (SKILL/'SKILL.md').read_bytes())

    def test_v4_route_stops_before_credentials_or_paid_request(self):
        voice=load_voice()
        with patch.object(voice,'get_preferences',return_value={}),patch.object(voice,'require_key') as key,patch.object(voice,'api_request') as api:
            with self.assertRaises(voice.PluginError) as error:voice.generate_narration('Hello',str(self.root),voice_id='example',model_id='eleven_v4')
        self.assertEqual(error.exception.code,'endpoint_not_supported');key.assert_not_called();api.assert_not_called();self.assertEqual(list(self.root.iterdir()),[])

if __name__=='__main__':unittest.main(verbosity=2)
