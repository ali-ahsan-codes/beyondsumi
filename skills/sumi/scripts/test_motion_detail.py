"""Per-film approval, budget and real source-pose cadence regression checks."""
import copy,hashlib,json,math,subprocess,sys,tempfile,unittest
from pathlib import Path
from motion_detail import initial_choice,smooth_24,validate
from living_frames import character_clock
from validate_living_frames import validate_original_states
from validate_style_profile import validate as validate_profile

class MotionChoiceTests(unittest.TestCase):
 def plan(self,style='sumi-original',route='images'):
  return {'release_version':'5.1.3','style':style,'motion_detail':initial_choice(style,route),
          'dialogue_animation':{'speech_mode':'narration-only','lip_sync':'not-applicable','approval_record':'current user requested narrator only'}}
 def approve(self,p,mode='default'):
  c=p['motion_detail'];c.update(mode=mode,status='approved',approval_record='current user selected '+mode,
    target_states_per_second=24 if mode=='smooth24' else c['default_states_per_second'],
    image_batches=[{'id':'walk-poses','purpose':'connected stance/lift/swing/contact and mouth poses',
    'new_pose_drawings':24,'image_calls_max':4,'actual_image_calls':3,'approval_record':'current user approved this four-call sheet batch'}]);return p
 def test_pending_blocks_production(self):self.assertTrue(validate(self.plan()))
 def test_default_answer_and_batch_pass(self):self.assertEqual(validate(self.approve(self.plan())),[])
 def test_smoother_answer_and_batch_pass(self):
  p=self.approve(self.plan(),'smooth24');self.assertEqual(validate(p),[]);self.assertTrue(smooth_24(p))
 def test_missing_receipt_does_not_enable_smoother(self):
  p=self.approve(self.plan(),'smooth24');p['motion_detail']['approval_record']='';self.assertFalse(smooth_24(p));self.assertTrue(validate(p))
 def test_call_overrun_requires_new_approval(self):
  p=self.approve(self.plan());p['motion_detail']['image_batches'][0]['actual_image_calls']=5;self.assertTrue(validate(p))
 def test_pose_count_is_separate_from_call_count(self):
  p=self.approve(self.plan());self.assertEqual(validate(p),[]);self.assertNotEqual(p['motion_detail']['image_batches'][0]['new_pose_drawings'],p['motion_detail']['image_batches'][0]['image_calls_max'])
 def test_empty_batch_or_reuse_explanation_required(self):
  p=self.approve(self.plan());p['motion_detail']['image_batches']=[];self.assertTrue(validate(p));p['motion_detail']['reuse_only_reason']='exact approved 24-pose action cycle exists';self.assertEqual(validate(p),[])
 def test_svg_default_bypasses_motion_question(self):self.assertEqual(validate(self.plan(route='svg')),[])
 def test_svg_cannot_silently_raise_detail(self):
  p=self.plan(route='svg');p['motion_detail']['mode']='smooth24';self.assertTrue(validate(p));self.assertFalse(smooth_24(p))
 def test_dialogue_needs_lipsync_choice(self):
  p=self.approve(self.plan());p['dialogue_animation'].update(speech_mode='dialogue',lip_sync='pending');self.assertTrue(validate(p))
 def test_dialogue_lipsync_on_uses_voice_map(self):
  p=self.approve(self.plan());p['dialogue_animation'].update(speech_mode='both',lip_sync='on');self.assertTrue(validate(p));p['dialogue_animation']['voice_map']='VOICE-MAP.json';self.assertEqual(validate(p),[])
 def test_narrator_does_not_move_unrelated_mouths(self):
  p=self.approve(self.plan());p['dialogue_animation']['lip_sync']='on';self.assertTrue(validate(p))
 def test_old_projects_not_reinterpreted(self):self.assertEqual(validate({'release_version':'5.1.2'}),[])
 def test_new_project_cannot_drop_choice_record(self):self.assertTrue(validate({'release_version':'5.1.3'}))

class SmootherDrawingsTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def shot(self,fps=30):
  # Generic metadata fixtures; these do not claim a generated animation/art review.
  board=self.root/'board';board.write_bytes(b'test action-sheet bytes');file={'path':'board','sha256':hashlib.sha256(board.read_bytes()).hexdigest()}
  rows=[{'id':str(i),'source_id':'sheet','kind':'whole-drawing','roi_xywh':[i*10,0,10,10]} for i in range(24)]
  exposures=[]
  for frame in range(fps):
   clock=character_clock(frame,fps,24)
   if clock['start_frame']==frame:
    exposures.append({'state_id':str(clock['state']),'start_frame':frame,'end_frame':min(fps,math.ceil((clock['state']+1)*fps/24))})
  return {'id':'walk','start':0,'end':1,'style_profile':{'cadence':{'exposure_policy':f'24-in-{fps}'},
     'original_drawings':{'budget_mode':'action-driven','source_images':[{'id':'sheet','file':file}],
      'designed_states':rows,'exposure_plan':exposures}}}
 def errors(self,s,fps=30):return validate_original_states(s,self.root,24,fps,whole_drawings_only=True)
 def test_24_actual_pose_regions_in_30_frames(self):self.assertEqual(self.errors(self.shot()),[])
 def test_24_actual_pose_regions_in_24_frames(self):self.assertEqual(self.errors(self.shot(24),24),[])
 def test_fps_change_without_new_drawings_fails(self):
  s=self.shot();s['style_profile']['original_drawings']['designed_states']=s['style_profile']['original_drawings']['designed_states'][:20];self.assertTrue(self.errors(s))
 def test_renaming_repeated_pose_does_not_add_art(self):
  s=self.shot();s['style_profile']['original_drawings']['designed_states'][-1]['roi_xywh']=[0,0,10,10];self.assertTrue(self.errors(s))
 def test_derived_micro_motion_does_not_replace_smoother_pose_art(self):
  s=self.shot();s['style_profile']['original_drawings']['designed_states'][0]['kind']='derived-character';self.assertTrue(self.errors(s))
 def test_wrong_exposure_clock_fails(self):
  s=self.shot();s['style_profile']['original_drawings']['exposure_plan'][0]['end_frame']=3;self.assertTrue(self.errors(s))

class InitializerChoiceTests(unittest.TestCase):
 def test_new_projects_show_choices_and_use_approved_cadence(self):
  script=Path(__file__).with_name('new_remotion_project.py')
  with tempfile.TemporaryDirectory() as d:
   scenarios=[('sumi-original','images',None,20),('sumi-original','images','smooth24',24),
     ('sumi-light','images','smooth24',24),('sumi-dark','images','smooth24',24),('sumi-dark','svg',None,12)]
   for i,(style,route,mode,rate) in enumerate(scenarios):
    dest=Path(d)/str(i);args=[sys.executable,'-B',str(script),str(dest),'--style',style,'--art-route',route,'--seconds','1']
    if mode:args+=['--motion-detail',mode,'--motion-approval','current user explicitly selected smoother motion']
    result=subprocess.run(args,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
    plan=json.loads((dest/'shot-plan.json').read_text());shot=plan['shots'][0]
    self.assertEqual(shot['pose_fps'],rate);self.assertEqual(plan['dialogue_animation']['lip_sync'],'pending')
    if route=='svg':self.assertEqual(plan['motion_detail']['status'],'not-applicable')
    elif not mode:self.assertEqual(plan['motion_detail']['status'],'pending')
    else:self.assertTrue(smooth_24(plan))
    # The cadence option must not be rejected by the legacy fixed-rate checks.
    errs=validate_profile(plan,dest)
    self.assertFalse([e for e in errs if any(t in e for t in ['new film requires','exposure unit differs','evaluation clock','cadence differs','clocks differ'])],errs)
    self.assertTrue((dest/'scripts/motion_detail.py').is_file());self.assertTrue((dest/'sumi-guide/references/motion-detail.md').is_file())
 def test_initializer_refuses_unapproved_smoother_selection(self):
  with tempfile.TemporaryDirectory() as d:
   p=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('new_remotion_project.py')),str(Path(d)/'x'),'--style','sumi-light','--motion-detail','smooth24'],capture_output=True,text=True)
   self.assertNotEqual(p.returncode,0);self.assertFalse((Path(d)/'x').exists())

if __name__=='__main__':unittest.main()
