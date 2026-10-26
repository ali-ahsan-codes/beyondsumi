import copy,hashlib,tempfile,unittest
from pathlib import Path
from validate_shot_plan import validate,plan_digest,METHODS
class Plans(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
  def file(name):
   content=('fixture '+name).encode();(self.root/name).write_bytes(content);return {'path':name,'sha256':hashlib.sha256(content).hexdigest()}
  self.file=file;master=file('master.svg');pose=file('pose.svg')
  c={'id':'girl','master':master,'full_body':True,'species':'human','view':'side','facing':'right','limb_inventory':'two arms, two legs','poses':[{'id':'offer','image':pose,'master_sha256':master['sha256'],'review_overlay':file('overlay.svg'),'full_body':True,'view':'side','facing':'right','near_far_order':'right near','joint_orientation':'elbow down','hand_paw_orientation':'palm up','support_contact':'planted feet','observation':'test fixture, not visual certification','checks':dict.fromkeys(['limb_count','proportions','joint_bends','facing','contact','identity'],True),'unresolved':[]}]}
  s={'id':'offer','method':'drawn-acting','mechanism':{'type':'whole-pose-replacement','files':[file('acting.mjs')]},'start':0,'end':6,'performance':'offer','camera':'locked','transition':'hold','strict_identity':'ink drawing','economy':'three poses','pose_fps':12,'simulation_fps':30,'assets':[pose],'characters':[{'id':'girl','poses':['offer']}],'proof':{'clip':file('proof.mp4'),'review':file('review.md'),'adjacent_frame_sheet':file('frames.svg'),'neutral_background_clip':file('neutral.mp4'),'normal_speed':True,'adjacent_frames':True,'final_art':True,'method_visible_without_colour_camera':True,'japanese_sumi_identity':True,'observation':'fixture','unresolved':[]}}
  self.plan={'schema':2,'identity':'japanese-sumi','duration':6,'output_fps':30,'approval':dict.fromkeys(['script','direction','duration'],'fixture approval'),'characters':[c],'shots':[s]};self.plan['proof']={'plan_sha256':plan_digest(self.plan)}
 def tearDown(self):self.temp.cleanup()
 def fails(self):self.assertTrue(validate(self.plan,self.root,'proof'))
 def test_valid_structure(self):self.assertEqual(validate(self.plan,self.root,'proof'),[])
 def test_missing_whole_body(self):self.plan['characters'][0]['full_body']=False;self.fails()
 def test_stale_master(self):(self.root/'master.svg').write_text('new');self.fails()
 def test_stale_pose(self):(self.root/'pose.svg').write_text('new');self.fails()
 def test_stale_code(self):(self.root/'acting.mjs').write_text('new');self.fails()
 def test_unchecked_joints(self):self.plan['characters'][0]['poses'][0]['checks']['joint_bends']=False;self.fails()
 def test_missing_pose(self):self.plan['shots'][0]['characters'][0]['poses']=['gone'];self.fails()
 def test_mirror(self):self.plan['characters'][0]['poses'][0]['mirrored']=True;self.fails()
 def test_unrelated_limb(self):self.plan['characters'][0]['poses'][0]['parts']=[self.file('unrelated.svg')];self.fails()
 def test_wrong_mechanism(self):self.plan['shots'][0]['method']='living-ink';self.fails()
 def test_legacy_style(self):self.plan['shots'][0]['method']='mist';self.fails()
 def test_no_neutral_proof(self):del self.plan['shots'][0]['proof']['neutral_background_clip'];self.fails()
 def test_stale_timing(self):self.plan['shots'][0]['pose_fps']=6;self.fails()
 def test_missing_approval(self):self.plan['approval']['direction']='';self.fails()
 def test_path_escape(self):self.plan['shots'][0]['assets'][0]['path']='../master.svg';self.fails()
 def test_unresolved(self):self.plan['shots'][0]['proof']['unresolved']=['foot slide'];self.fails()
 def test_missing_character(self):self.plan['characters']=[];self.fails()
 def test_shared_mechanism(self):
  self.plan['four_method_comparison']=True;shots=[]
  for i,(m,kind) in enumerate(METHODS.items()):
   s=copy.deepcopy(self.plan['shots'][0]);s.update(id=m,method=m,start=i*1.5,end=(i+1)*1.5);s['mechanism']['type']=kind;shots.append(s)
  self.plan['shots']=shots;self.plan['proof']['plan_sha256']=plan_digest(self.plan);self.fails()
if __name__=='__main__':unittest.main()
