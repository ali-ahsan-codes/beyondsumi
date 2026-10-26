"""Versioned Original exposure provenance; no visual quality claims."""
import copy
import unittest
from test_original_drawings import OriginalRateTests
from validate_style_profile import validate

class VariableExposureTests(unittest.TestCase):
    # Reuse only fixture construction, not the legacy-rate test suite.
    def setUp(self):
        OriginalRateTests.setUp(self)
        self.plan.update(release_version='4.6.0',output_fps=30)
        shot=self.plan['shots'][0];shot.update(pose_fps=30,simulation_fps=30)
        shot['style_profile']['cadence']={'output_fps':30,'character_update_fps':30,'exposure_frames':1,'exposure_policy':'variable'}
        self.drawing.pop('minimum_drawings_per_second')
        self.drawing.update(budget_mode='action-driven',exposure_plan=[
            {'source_id':'pose-0','start_frame':0,'end_frame':7,'action':'anticipation','hold_reason':'read the concern'},
            {'source_id':'pose-1','start_frame':7,'end_frame':15,'action':'contact','hold_reason':'let contact register'},
            {'source_id':'pose-2','start_frame':15,'end_frame':30,'action':'settle','hold_reason':'deliberate emotional pause'}])
    def errors(self):
        return [e for e in validate(self.plan,self.root) if 'Original variable exposures' in e or 'new film requires' in e or 'evaluation clock' in e or 'exposure unit' in e]
    def tearDown(self):OriginalRateTests.tearDown(self)
    def test_variable_holds_accept_fewer_sources(self):self.assertEqual(self.errors(),[])
    def test_gap_rejected(self):
        self.drawing['exposure_plan'][1]['start_frame']=8;self.assertTrue(self.errors())
    def test_missing_source_rejected(self):
        self.drawing['exposure_plan'][1]['source_id']='missing';self.assertTrue(self.errors())
    def test_unknown_hold_reason_rejected(self):
        self.drawing['exposure_plan'][0]['hold_reason']='';self.assertTrue(self.errors())
    def test_old_density_policy_not_silently_used(self):
        self.plan['release_version']='4.5.4'
        errors=validate(self.plan,self.root)
        self.assertTrue(any('Original drawing rate' in e for e in errors))

if __name__=='__main__':unittest.main()
