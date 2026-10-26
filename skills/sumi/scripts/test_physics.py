"""Synthetic geometry/evidence regressions; no film/artistic certification."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from plan_provenance import plan_digest
from validate_physics import validate, CONTRACT

class PhysicsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.source = self.file('rig.txt', 'synthetic fixture, not real artwork')
        self.action = {'id':'stand','character':'actor','kind':'stand','view':'side',
            'start_frame':0,'end_frame':4,'not_applicable':{},'checks':[
            {'id':'shin','kind':'length','points':['knee','ankle'],'min':4.99,'max':5.01,'reason':'fixed five-unit segment'},
            {'id':'knee','kind':'bend','points':['hip','knee','ankle'],'sign':1,'epsilon':0.01,'reason':'checked side view'},
            {'id':'sole','kind':'pin','points':['sole'],'anchor':[0,10],'max_error':0.1,'reason':'planted contact patch'},
            {'id':'floor','kind':'surface','points':['sole'],'min':9.9,'max':10.1,'reason':'visible sole at floor'},
            {'id':'grip','kind':'grip','points':['hand','handle'],'max_error':0.1,'reason':'closed grip'},
            {'id':'root','kind':'step','points':['hip'],'max_error':1,'reason':'quiet hold'},
            {'id':'weight','kind':'support','points':['mass','left','right'],'max_error':0.1,'reason':'slow supported hold'}]}
        self.plan={'schema':2,'identity':'japanese-sumi','catalog':'three-styles-v4','style':'sumi-light',
            'release_version':'4.2.0','physics_contract':CONTRACT,'output_fps':24,'duration':4/24,
            'shots':[{'id':'shot','start':0,'end':4/24,'characters':[{'id':'actor'}],
                      'mechanism':{'files':[self.source]},'physics':{'actions':[self.action]},'proof':{}}]}
        pts={'hip':[0,0],'knee':[-3,4],'ankle':[0,8],'sole':[0,10],
             'hand':[2,2],'handle':[2,2],'mass':[0,3],'left':[-2,10],'right':[2,10]}
        self.trace={'schema':1,'fps':24,'coordinates':'world-design-pixels',
            'actions':{'stand':[{'frame':i,'character':'actor','points':copy.deepcopy(pts),'unresolved':[]} for i in range(4)]}}
        self.review={'schema':1,'actions':{'stand':{'start_frame':0,'end_frame':4,'status':'pass',
            'reviewer':'synthetic test only','orientation':'fixture','soles':'fixture','hands':'fixture',
            'weight_transfer':'fixture','entry_exit':'fixture','trace_matches_visible_geometry':'fixture',
            'not_applicable_reviewed':{},'unresolved':[],'normal_speed':True,'consecutive_frames':True,'final_art':True,
            **{k:self.file(k+'.txt','synthetic evidence; not a visual review') for k in ['full_body_clip','neutral_clip','adjacent_frame_sheet','sole_grip_overlay']}}}}
        self.save()
    def tearDown(self): self.temp.cleanup()
    def file(self, name, data):
        p=self.root/name;p.write_text(data)
        return {'path':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    def save(self):
        self.trace['plan_sha256']=self.review['plan_sha256']=plan_digest(self.plan)
        self.plan['shots'][0]['proof']['physics_trace']=self.file('trace.json',json.dumps(self.trace))
        self.plan['shots'][0]['proof']['limb_review']=self.file('review.json',json.dumps(self.review))
    def result(self): return validate(self.plan,self.root)
    def fails(self, phrase):
        self.save();self.assertTrue(any(phrase in s for s in self.result()),self.result())
    def test_valid_fixture(self): self.assertEqual(self.result(),[])
    def test_foot_drift(self): self.trace['actions']['stand'][2]['points']['sole'][0]=3;self.fails('pin failed')
    def test_floor_penetration(self): self.trace['actions']['stand'][2]['points']['sole'][1]=13;self.fails('surface failed')
    def test_stretched_limb(self): self.trace['actions']['stand'][1]['points']['ankle'][1]=30;self.fails('length failed')
    def test_reversed_knee(self): self.trace['actions']['stand'][1]['points']['knee'][0]=3;self.fails('bend failed')
    def test_disconnected_grip(self): self.trace['actions']['stand'][3]['points']['handle'][0]=10;self.fails('grip failed')
    def test_abrupt_root_jump(self): self.trace['actions']['stand'][2]['points']['hip'][0]=50;self.fails('step failed')
    def test_unsupported_weight(self): self.trace['actions']['stand'][2]['points']['mass'][0]=30;self.fails('support failed')
    def test_clamp_rejected(self): self.trace['actions']['stand'][2]['unresolved']=['IK clamp'];self.fails('unresolved renderer')
    def test_missing_frame(self): self.trace['actions']['stand'].pop();self.fails('every output frame')
    def test_duplicate_frame(self): self.trace['actions']['stand'][3]['frame']=2;self.fails('duplicate')
    def test_missing_point(self): del self.trace['actions']['stand'][1]['points']['sole'];self.fails('missing point')
    def test_nonfinite(self): self.trace['actions']['stand'][0]['points']['sole'][0]=float('nan');self.fails('nonfinite')
    def test_wrong_character(self): self.trace['actions']['stand'][0]['character']='other';self.fails('character mismatch')
    def test_screen_coordinates_rejected(self): self.trace['coordinates']='screen';self.fails('world-design-pixels')
    def test_wrong_fps(self): self.trace['fps']=60;self.fails('output fps')
    def test_missing_review(self): del self.review['actions']['stand'];self.fails('visual review required')
    def test_visual_failure(self): self.review['actions']['stand']['unresolved']=['wrong boot'];self.fails('unresolved/unapproved')
    def test_unperformed_playback(self): self.review['actions']['stand']['normal_speed']=False;self.fails('unperformed normal_speed')
    def test_missing_observation(self): self.review['actions']['stand']['hands']='';self.fails('missing observation hands')
    def test_missing_evidence(self): (self.root/'sole_grip_overlay.txt').unlink();self.assertTrue(any('missing/outside' in x for x in self.result()))
    def test_stale_source(self): (self.root/'rig.txt').write_text('changed');self.assertTrue(any('stale file' in x for x in self.result()))
    def test_stale_trace(self): (self.root/'trace.json').write_text('{}');self.assertTrue(any('stale file' in x for x in self.result()))
    def test_stale_plan(self): self.plan['shots'][0]['physics']['note']='changed';self.assertTrue(any('stale plan binding' in x for x in self.result()))
    def test_action_gap(self): self.action['end_frame']=3;self.fails('entire shot')
    def test_missing_constraint_family(self): self.action['checks']=[c for c in self.action['checks'] if c['kind']!='grip'];self.fails('missing grip')
    def test_reviewed_exemption(self):
        self.action['checks']=[c for c in self.action['checks'] if c['kind']!='grip']
        self.action['not_applicable']={'grip':'No object is held'}
        self.review['actions']['stand']['not_applicable_reviewed']=self.action['not_applicable'].copy()
        self.save();self.assertEqual(self.result(),[])
    def test_unreviewed_exemption(self): self.action['not_applicable']={'grip':'none'};self.fails('contradictory')
    def test_outside_path(self): self.plan['shots'][0]['proof']['physics_trace']['path']='../escape.json';self.assertTrue(any('outside-project' in x for x in self.result()))
    def test_assets_stage_no_review_required(self): self.plan['shots'][0]['proof']={};self.assertEqual(validate(self.plan,self.root,'assets'),[])
    def test_character_free_explicit(self):
        s=self.plan['shots'][0];s['characters']=[];s['physics']={'actions':[],'character_free_reason':'Empty scenery'}
        self.assertEqual(self.result(),[])
    def test_character_free_requires_reason(self): self.plan['shots'][0]['characters']=[];self.fails('character-free')
    def test_standard_gate_calls_physics(self):
        import validate_shot_plan
        with patch.object(validate_shot_plan,'validate_base',return_value=[]),patch('validate_style_profile.validate',return_value=[]):
            del self.plan['physics_contract']
            self.assertTrue(any('physics_contract' in e for e in validate_shot_plan.validate(self.plan,self.root,'proof')))
    def test_standard_gate_rejects_actual_defect(self):
        import validate_shot_plan
        self.trace['actions']['stand'][1]['points']['sole'][0]=3;self.save()
        with patch.object(validate_shot_plan,'validate_base',return_value=[]),patch('validate_style_profile.validate',return_value=[]):
            self.assertTrue(any('pin failed' in e for e in validate_shot_plan.validate(self.plan,self.root,'proof')))
    def test_missing_helper_blocks_standard_gate(self):
        import validate_shot_plan
        with patch.object(validate_shot_plan,'validate_base',return_value=[]),patch('validate_style_profile.validate',return_value=[]),patch.dict('sys.modules',{'validate_physics':None}):
            self.assertTrue(any('required validator unavailable' in e for e in validate_shot_plan.validate(self.plan,self.root,'proof')))

if __name__=='__main__': unittest.main()
