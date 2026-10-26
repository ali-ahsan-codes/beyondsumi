"""Meaningful data/clock/provenance regressions; no visual certification."""
import copy,hashlib,json,math,tempfile,unittest
from pathlib import Path
from environment_motion import sample,bake,driver
from validate_environment_plan import validate_plan,validate,digest
class EnvironmentTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'master.png').write_bytes(b'checked source fixture')
 def tearDown(self):self.tmp.cleanup()
 def file(self,n='master.png'):return {'path':n,'sha256':hashlib.sha256((self.root/n).read_bytes()).hexdigest()}
 def plan(self):
  return {'schema':'sumi-environment-v1','style':'sumi-original','fps':30,'frames':150,'width':200,'height':100,'mode':'natural','master':self.file(),'environment':'room','time_of_day':'night','weather':'sheltered, still air','motion_reason':'visible candle','protected_regions':[{'id':'caption','role':'text','bounds':[20,90,180,100]}],'static_regions':[{'id':'wall-trim','bounds':[100,0,110,50]}],'drivers':[{'id':'candle','seed':1440,'hz':.35}], 'effects':[{'id':'flame','kind':'flame','driver':'candle','pass':'background','bounds':[10,10,25,30],'start_frame':0,'end_frame':150,'amplitude':1,'purpose':'visible flame'}]}
 def receiver(self):return {'id':'wall-light','kind':'light','driver':'candle','source_effect':'flame','receiver':'stone beside candle','pass':'lighting','bounds':[30,10,70,70],'start_frame':0,'end_frame':150,'opacity':.06,'purpose':'same-source illumination'}
 def test_valid_local_plan(self):self.assertEqual(validate_plan(self.plan(),self.root),[])
 def test_seeded_seek_matches_forward(self):
  p=self.plan();rows=bake(p)['frames'];self.assertEqual(rows[79],sample(p,79));self.assertEqual(rows,bake(p)['frames'])
 def test_24fps_keeps_twos_separate(self):
  p=self.plan();p.update(style='sumi-light',fps=24,frames=120);p['effects'][0]['end_frame']=120
  self.assertEqual(validate_plan(p,self.root),[]);self.assertEqual(len(bake(p)['frames']),120);self.assertAlmostEqual(sample(p,24)['time'],1)
 def test_wrong_style_fps_rejected(self):
  p=self.plan();p['fps']=24;self.assertTrue(validate_plan(p,self.root))
 def test_linked_receivers_share_driver_signal(self):
  p=self.plan();p['effects'].append(self.receiver());rows=sample(p,77)['effects'];self.assertEqual(rows[0]['signal'],rows[1]['signal'])
 def test_wrong_light_source_driver_rejected(self):
  p=self.plan();p['drivers'].append({'id':'unrelated','seed':2,'hz':.3});r=self.receiver();r['driver']='unrelated';p['effects'].append(r);self.assertTrue(validate_plan(p,self.root))
 def test_outside_patch_rejected(self):
  p=self.plan();p['effects'][0]['bounds']=[-1,0,30,30];self.assertTrue(validate_plan(p,self.root))
 def test_global_colour_shift_rejected(self):
  p=self.plan();r=self.receiver();r['bounds']=[0,0,200,100];p['effects'].append(r);self.assertTrue(validate_plan(p,self.root))
 def test_rigid_structure_cannot_be_deformed(self):
  p=self.plan();p['effects'][0]['bounds']=[90,10,120,30];self.assertTrue(validate_plan(p,self.root))
 def test_protected_text_is_excluded(self):
  p=self.plan();p['effects'][0]['bounds']=[25,80,60,95];self.assertTrue(validate_plan(p,self.root))
 def test_shared_character_light_requires_reason(self):
  p=self.plan();r=self.receiver();p['protected_regions'].append({'id':'sleeve','role':'character','bounds':[40,20,60,40]});r['affects_character']=True;p['effects'].append(r)
  self.assertTrue(validate_plan(p,self.root));r['character_light_reason']='sleeve beside candle, masked';self.assertEqual(validate_plan(p,self.root),[])
 def test_master_hash_stale_rejected(self):
  p=self.plan();(self.root/'master.png').write_bytes(b'changed');self.assertTrue(validate_plan(p,self.root))
 def test_mask_provenance(self):
  p=self.plan();p['effects'][0]['mask']={'path':'../outside','sha256':'bad'};self.assertTrue(validate_plan(p,self.root))
 def test_original_texture_boil_not_automatic(self):
  p=self.plan();p['effects'][0]['kind']='texture';self.assertTrue(validate_plan(p,self.root))
 def test_dark_neutral_red_preserved(self):
  p=self.plan();p.update(style='sumi-dark',fps=24,frames=150);p['effects'][0]['color']='#7A1622';self.assertEqual(validate_plan(p,self.root),[])
  p['effects'][0]['color']='#f4c57e';self.assertTrue(validate_plan(p,self.root))
 def test_dark_default_effects_are_neutral(self):
  p=self.plan();p.update(style='sumi-dark',fps=24);a=sample(p,50)['effects'][0]['color'];self.assertEqual(a[1:3],a[3:5]);self.assertEqual(a[3:5],a[5:7])
 def test_zero_and_end_timing(self):
  p=self.plan();self.assertEqual(sample(p,0)['effects'],[]);self.assertLess(sample(p,149)['effects'][0]['envelope'],.05)
  with self.assertRaises(ValueError):sample(p,150)
 def test_independent_candles(self):
  d={'seed':1,'hz':.35};e={'seed':2,'hz':.35};self.assertNotEqual([driver(d,i/30) for i in range(150)],[driver(e,i/30) for i in range(150)])
 def test_finite_temporally_coherent_motion(self):
  p=self.plan();v=[sample(p,i)['drivers']['candle'] for i in range(150)];self.assertTrue(all(math.isfinite(x) and abs(x)<=1 for x in v));self.assertLess(max(abs(a-b) for a,b in zip(v,v[1:])),.1)
 def test_historical_plan_unchanged(self):self.assertEqual(validate({'release_version':'4.7.0','shots':[{}]},self.root),[])
 def test_new_pending_and_reasoned_stillness(self):
  p={'release_version':'4.8.0','shots':[{'id':'quiet','environment':{'decision':'pending'}}]};self.assertTrue(validate(p,self.root));p['shots'][0]['environment']={'decision':'still','reason':'deliberate suspended beat'};self.assertEqual(validate(p,self.root),[])
 def test_review_is_hash_bound_not_prefilled(self):
  env=self.plan();(self.root/'env.json').write_text(json.dumps(env));p={'release_version':'4.8.0','style':'sumi-original','output_fps':30,'shots':[{'id':'shot','start':0,'end':5,'environment':{'decision':'animate','plan':self.file('env.json'),'review':None}}]}
  self.assertEqual(validate(p,self.root),[]);self.assertTrue(validate(p,self.root,'proof'))
 def test_parallax_needs_hidden_pixel_plate(self):
  p=self.plan();p['effects'][0]['kind']='parallax';self.assertTrue(validate_plan(p,self.root))
 def test_particle_count_bounded(self):
  p=self.plan();p['effects'][0].update(kind='dust',count=10000);self.assertTrue(validate_plan(p,self.root))
 def test_local_patch_cannot_drift_or_fold(self):
  p=self.plan();p['effects'][0]['amplitude']=30;self.assertTrue(validate_plan(p,self.root));p=self.plan();p['effects'][0]['velocity']=[20,0];self.assertTrue(validate_plan(p,self.root))
 def test_local_light_has_active_temporal_travel_and_contrast(self):
  p=self.plan();p['effects'].append(self.receiver());rows=[sample(p,i)['effects'][-1] for i in range(15,130)];self.assertGreater(max(x['dx'] for x in rows)-min(x['dx'] for x in rows),8);self.assertGreater(max(x['alpha'] for x in rows)-min(x['alpha'] for x in rows),.01)
 def test_explicit_additive_holdout(self):
  p=self.plan();p['effects'][0].update(kind='dust',bounds=[25,80,60,95],holdouts=['caption']);self.assertEqual(validate_plan(p,self.root),[])
 def test_intensity_modes_have_effect(self):
  p=self.plan();a=sample(p,70)['effects'][0];p['mode']='dramatic';b=sample(p,70)['effects'][0];self.assertGreater(abs(b['dx']),abs(a['dx']));self.assertGreater(b['alpha'],a['alpha'])
if __name__=='__main__':unittest.main()
