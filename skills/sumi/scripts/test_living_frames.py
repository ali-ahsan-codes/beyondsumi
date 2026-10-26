import copy
import hashlib
import tempfile
import unittest
from pathlib import Path
from living_frames import character_clock,sample,anchored_displacement
from validate_living_frames import validate_original_states,validate

class LivingFramesTests(unittest.TestCase):
    def test_original_clock(self):
        states=[character_clock(i)['state'] for i in range(30)]
        self.assertEqual(len(set(states)),20);self.assertEqual([states.count(i) for i in range(20)],[2,1]*10)
    def test_light_dark_clock_unchanged(self):
        self.assertEqual(len({character_clock(i,24,12)['state'] for i in range(24)}),12)
    def test_deterministic_seek(self):
        m={'behavior':'hair','phase':.5,'amplitude':3,'end':10}
        forward=[sample(m,character_clock(i)['time']) for i in range(100)]
        self.assertEqual(forward[71],sample(m,character_clock(71)['time']))
    def test_anchor_and_edges_fixed(self):
        self.assertEqual(anchored_displacement(5,0),0);self.assertEqual(anchored_displacement(5,1,1),0);self.assertEqual(anchored_displacement(5,1),5)
    def test_blink_not_metronome(self):
        m={'behavior':'blink','events':[{'at':.8},{'at':3.3}]}
        self.assertEqual(sample(m,2),0);self.assertGreater(sample(m,.87),.9)
    def test_settle_and_end(self):
        m={'behavior':'cloth','end':2,'amplitude':2}
        self.assertEqual(sample(m,2),0);self.assertAlmostEqual(sample(m,0),0)
    def fixture(self,root):
        (root/'master').write_bytes(b'approved source');(root/'rig').write_bytes(b'authored rig')
        def f(name):return {'path':name,'sha256':hashlib.sha256((root/name).read_bytes()).hexdigest()}
        rows=[{'id':str(i),'kind':'derived-character','source_id':'master','rig':f('rig'),'target_ids':['hair-tips'],'character_parameters':{'hair_tip_x':i/10}} for i in range(20)]
        entries=[]
        for frame in range(30):
            c=character_clock(frame)
            if c['start_frame']==frame:entries.append({'start_frame':frame,'end_frame':min(30,frame+(2 if c['state']%2==0 else 1)),'state_id':str(c['state'])})
        return {'id':'shot','start':0,'end':1,'style_profile':{'cadence':{'exposure_policy':'20-in-30'},'original_drawings':{'budget_mode':'action-driven','source_images':[{'id':'master','file':f('master')}],'designed_states':rows,'exposure_plan':entries}}}
    def test_checked_derived_states_not_twenty_new_images(self):
        with tempfile.TemporaryDirectory() as t:self.assertEqual(validate_original_states(self.fixture(Path(t)),Path(t)),[])
    def test_renamed_copies_fail(self):
        with tempfile.TemporaryDirectory() as t:
            shot=self.fixture(Path(t))
            for s in shot['style_profile']['original_drawings']['designed_states']:s['character_parameters']={'hair_tip_x':0}
            self.assertTrue(validate_original_states(shot,Path(t)))
    def test_clock_only_has_no_states(self):
        with tempfile.TemporaryDirectory() as t:
            shot=self.fixture(Path(t));shot['style_profile']['original_drawings']['designed_states']=[];self.assertTrue(validate_original_states(shot,Path(t)))
    def test_camera_only_not_character_state(self):
        with tempfile.TemporaryDirectory() as t:
            shot=self.fixture(Path(t))
            for i,s in enumerate(shot['style_profile']['original_drawings']['designed_states']):s['character_parameters']={'camera_zoom':i}
            self.assertTrue(validate_original_states(shot,Path(t)))
    def test_wrong_hold_fails(self):
        with tempfile.TemporaryDirectory() as t:
            shot=self.fixture(Path(t));shot['style_profile']['original_drawings']['exposure_plan'][0]['end_frame']=3;self.assertTrue(validate_original_states(shot,Path(t)))
    def test_missing_strategy_pending(self):self.assertTrue(validate({'release_version':'4.6.1','shots':[{'id':'pending'}]},Path('.')))
    def test_historical_plan_not_reinterpreted(self):self.assertEqual(validate({'release_version':'4.6.0','shots':[{}]},Path('.')),[])

if __name__=='__main__':unittest.main()
