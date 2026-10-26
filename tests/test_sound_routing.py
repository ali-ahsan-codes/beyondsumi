from pathlib import Path
import sys,tempfile,json,math,copy,unittest
from array import array
from unittest.mock import patch
P=Path(__file__).resolve().parents[1];TOOLS=P/'skills/sumi/assets/sound-library';sys.path.insert(0,str(TOOLS))
import library,route_sound

class RoutingTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.cache=self.root/'cache';self.cache.mkdir();(self.cache/'sfx').mkdir()
  sound=[array('f',(math.sin(i*.2)*.1 for i in range(2400)))]*2;f=self.cache/'sfx/cup-set.wav';library.write_wav(f,sound)
  self.record={'id':'cup-set','category':'foley','duration':.05,'file':'sfx/cup-set.wav','sha256':library.sha(f),'source':'fixture licensed source','review':'approved','contact_anchor_seconds':0,'contact_candidate_seconds':0,'loop_requested':False,'loop_review':'not_applicable'}
  library.save(self.cache/'library.json',{'music':{},'sfx':{'cup-set':self.record}})
  self.plan={'fps':24,'duration_frames':48,'cues':[{'type':'sfx','id':'cup-set','at_frame':1,'gain':.2}]}
 def tearDown(self):self.temp.cleanup()
 def test_library_first_reuses_exact_audio(self):
  out=self.root/'reuse';r=route_sound.prepare(self.plan,out,self.cache);self.assertEqual(r['cues'][0]['route'],'library');self.assertEqual(library.sha(out/'bank/sfx/cup-set.wav'),self.record['sha256'])
 def test_missing_effect_synthesized(self):
  p=copy.deepcopy(self.plan);p['cues'][0].update(id='bell-soft',python_duration=.2);r=route_sound.prepare(p,self.root/'missing',self.cache);self.assertEqual(r['cues'][0]['route'],'python-synthesis');self.assertEqual(r['provider_calls'],0)
 def test_pure_python_never_reads_provider_cache(self):
  with patch.object(library,'manifest',side_effect=AssertionError('Pure mode read a cached library')):
   r=route_sound.prepare(self.plan,self.root/'pure',self.cache,mode='python-only')
  self.assertEqual(r['cues'][0]['route'],'python-synthesis');self.assertFalse(r['private_library_inspected'])
 def test_available_api_requires_a_choice_without_spending(self):
  p=copy.deepcopy(self.plan);p['cues'][0]['id']='ink-drop';out=self.root/'paid';r=route_sound.prepare(p,out,self.cache,elevenlabs_available=True);self.assertEqual(r['status'],'needs_sound_choice');self.assertEqual(r['provider_calls'],0);self.assertFalse((out/'bank').exists());self.assertTrue((out/'NEXT-ACTIONS.json').exists())
 def test_explicit_python_declines_api(self):
  p=copy.deepcopy(self.plan);p['cues'][0].update(id='ink-drop',python_duration=.2);r=route_sound.prepare(p,self.root/'decline',self.cache,elevenlabs_available=True,missing_action='python');self.assertEqual(r['cues'][0]['route'],'python-synthesis')
 def test_corruption_is_not_hidden_by_fallback(self):
  (self.cache/'sfx/cup-set.wav').write_bytes(b'changed')
  with self.assertRaises(ValueError):route_sound.prepare(self.plan,self.root/'bad',self.cache)
 def test_unknown_design_does_not_fake_or_call_api(self):
  p=copy.deepcopy(self.plan);p['cues'][0]['id']='unknown-material'
  with self.assertRaisesRegex(ValueError,'No suitable saved effect'):route_sound.prepare(p,self.root/'unknown',self.cache)
 def test_pending_generated_audio_cannot_pass_normal_render(self):
  out=self.root/'pending';route_sound.prepare(self.plan,out,mode='python-only');p=json.loads((out/'resolved-plan.json').read_text())
  with self.assertRaisesRegex(ValueError,'Audition pending'):library.render_plan(out/'bank',p,out/'mix')
 def test_review_render_has_stems_and_exact_samples(self):
  out=self.root/'review';route_sound.prepare(self.plan,out,self.cache);p=json.loads((out/'resolved-plan.json').read_text());r=library.render_plan(out/'bank',p,out/'mix',True);self.assertEqual(r['sample_count'],96000);self.assertFalse(r['listening_reviewed']);self.assertTrue((out/'mix/background.wav').exists())
 def test_existing_selection_is_preserved(self):
  out=self.root/'old';out.mkdir()
  with self.assertRaises(ValueError):route_sound.prepare(self.plan,out,self.cache)
 def test_no_path_traversal(self):
  p=copy.deepcopy(self.plan);p['cues'][0]['id']='../private'
  with self.assertRaises(ValueError):route_sound.prepare(p,self.root/'unsafe',self.cache)

if __name__=='__main__':unittest.main()
