"""Offline sound-bank safety/timing tests. No account calls or installations."""
from array import array
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS=Path(__file__).resolve().parents[1]/'assets/sound-library'
sys.path.insert(0,str(TOOLS))
import library
import music
import generate_sfx


class SoundLibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'bank';self.root.mkdir()
        self.out=Path(self.tmp.name)/'render'

    def tearDown(self):self.tmp.cleanup()

    def fixture(self,review='pending',anchor=.1):
        for name in ['music/test','sfx']:(self.root/name).mkdir(parents=True,exist_ok=True)
        n=48000
        for part in ['harmony','melody','rhythm']:
            sound=[array('f',[.1])*n,array('f',[.1])*n]
            library.write_wav(self.root/'music/test'/(part+'.wav'),sound)
        sound=[array('f',[0])*4800+array('f',[.1])*(n-4800) for _ in range(2)]
        library.write_wav(self.root/'sfx/test.wav',sound)
        files={str(p.relative_to(self.root)):library.sha(p) for p in (self.root/'music/test').glob('*.wav')}
        manifest={'music':{'test':{'review':review,'files':files,'body_seconds':.8}},
                  'sfx':{'test':{'review':review,'file':'sfx/test.wav','sha256':library.sha(self.root/'sfx/test.wav'),
                                 'category':'foley','duration':1,'contact_anchor_seconds':anchor,'contact_candidate_seconds':.1,
                                 'loop_requested':False}}}
        library.save(self.root/'library.json',manifest)

    def plan(self,**kw):
        p={'fps':30,'duration_frames':30,'cues':[{'type':'music','id':'test','at_frame':0,'duration_frames':30,'parts':['harmony'],'gain':.5,'fade_in':0,'fade_out':0}]}
        p.update(kw);return p

    def test_catalog_has_twelve_different_moods_and_bounded_batch(self):
        c=library.catalog();self.assertEqual(len(c['music']),12);self.assertEqual(len(c['sfx']),32)
        self.assertEqual(len({p['id'] for p in c['music']}),12)
        self.assertEqual(len({tuple(p['motif']) for p in c['music']}),12)
        self.assertAlmostEqual(sum(p['duration_seconds'] for p in c['sfx']),109.5)

    def test_composition_is_seeded_finite_and_keeps_editable_parts(self):
        p=dict(library.catalog()['music'][5]);p.update(bars=2,bpm=120)
        a,score=music.compose(p,seed=12);b,_=music.compose(p,seed=12)
        self.assertEqual(set(a),{'harmony','melody','rhythm'})
        self.assertEqual(score['provider_calls'],0);self.assertEqual(score['review'],'pending')
        self.assertEqual(len(a['harmony'][0]),round(score['duration']*48000))
        for part in a:
            self.assertEqual(a[part],b[part]);self.assertTrue(all(math.isfinite(v) for c in a[part] for v in c))
        self.assertNotEqual(a['melody'],a['harmony'])

    def test_pending_audition_cannot_render_as_approved(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError,'Audition pending'):library.render_plan(self.root,self.plan(),self.out)
        self.assertFalse(self.out.exists())

    def test_draft_is_exact_and_records_pending_sources(self):
        self.fixture();report=library.render_plan(self.root,self.plan(),self.out,True)
        self.assertEqual(report['sample_count'],48000);self.assertEqual(report['provider_calls'],0)
        self.assertEqual(report['unreviewed_assets'],['music:test'])
        self.assertFalse(report['listening_reviewed'])
        self.assertEqual(len(library.read_wav(self.out/'background.wav')[0]),48000)

    def test_24_and_30_frame_clocks(self):
        self.fixture()
        for fps,frames in [(24,13),(30,17)]:
            p=self.plan(fps=fps,duration_frames=frames)
            p['cues'][0]['duration_frames']=frames
            r=library.render_plan(self.root,p,self.out/str(fps),True)
            self.assertEqual(r['sample_count'],round(frames/fps*48000))

    def test_contact_anchor_uses_preroll_and_preserves_full_tail(self):
        self.fixture(review='approved')
        p=self.plan(duration_frames=60,cues=[{'type':'sfx','id':'test','at_frame':15,'gain':1,'fade_in':0,'fade_out':0}])
        r=library.render_plan(self.root,p,self.out)
        self.assertAlmostEqual(r['cues'][0]['source_start_seconds'],.4)
        s=library.read_wav(self.out/'sfx.wav')[0]
        self.assertTrue(all(v==0 for v in s[:24000]));self.assertGreater(s[24000],.09)

    def test_missing_contact_requires_audition(self):
        self.fixture(review='approved',anchor=None)
        with self.assertRaisesRegex(ValueError,'Contact anchor pending'):
            library.render_plan(self.root,self.plan(duration_frames=60,cues=[{'type':'sfx','id':'test','at_frame':15}]),self.out)

    def test_tail_and_negative_preroll_are_rejected(self):
        self.fixture(review='approved')
        for frame in [0,29]:
            with self.assertRaises(ValueError):library.render_plan(self.root,self.plan(cues=[{'type':'sfx','id':'test','at_frame':frame}]),self.out)
        self.assertFalse(self.out.exists())

    def test_overlap_ducks_do_not_compound_and_recover(self):
        a={'start_frame':6,'end_frame':15,'gain':.4,'attack':.02,'release':.1}
        b={'start_frame':9,'end_frame':18,'gain':.22,'attack':.02,'release':.1}
        e=library.envelope([a,b],48000,30,'music')
        self.assertAlmostEqual(e[16000],.22,places=6);self.assertEqual(e[40000],1)
        self.assertEqual(library.envelope([a,b],48000,30,'sfx')[16000],1)

    def test_duck_recovery_in_actual_render(self):
        self.fixture();p=self.plan(ducks=[{'start_frame':6,'end_frame':15,'gain':.4,'attack':.02,'release':.1}])
        library.render_plan(self.root,p,self.out,True);s=library.read_wav(self.out/'music.wav')[0]
        self.assertAlmostEqual(s[16000]/s[40000],.4,places=3)

    def test_hash_bound_files_and_safe_paths(self):
        self.fixture();p=self.root/'music/test/harmony.wav';p.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'Stale'):library.render_plan(self.root,self.plan(),self.out,True)
        with self.assertRaises(ValueError):library.asset(self.root,'../outside.wav')

    def test_frame_gain_parts_and_nan_validation(self):
        self.fixture()
        for field,value in [('at_frame',.2),('gain',float('nan')),('parts',['harmony','harmony']),('duration_frames',1.2)]:
            p=self.plan();p['cues'][0][field]=value
            with self.assertRaises(ValueError):library.render_plan(self.root,p,self.out,True)

    def test_does_not_overwrite_previous_render(self):
        self.fixture();library.render_plan(self.root,self.plan(),self.out,True)
        before=library.sha(self.out/'background.wav')
        with self.assertRaises(ValueError):library.render_plan(self.root,self.plan(),self.out,True)
        self.assertEqual(before,library.sha(self.out/'background.wav'))

    def test_shared_attenuation_retains_stem_balance(self):
        self.fixture();p=self.plan();p['cues'][0].update(parts=['harmony','melody','rhythm'],gain=2)
        r=library.render_plan(self.root,p,self.out,True)
        self.assertLess(r['shared_attenuation'],1)
        self.assertLessEqual(max(library.read_wav(self.out/'background.wav')[0]),10**(-6/20)+1/32768)

    def test_acquisition_requires_exact_approval_before_key_or_network(self):
        path=Path(self.tmp.name)/'approval.json';path.write_text('{}')
        with patch.object(generate_sfx,'read_key',side_effect=AssertionError('secret read')):
            with self.assertRaises(ValueError):generate_sfx.batch(TOOLS/'catalog.json',path,self.root)

    def test_uncertain_generation_is_never_repeated(self):
        c=library.catalog();raw=(TOOLS/'catalog.json').read_bytes()
        approval={'approved':True,'catalog_sha256':hashlib.sha256(raw).hexdigest(),'count':32,'total_seconds':109.5,'max_estimated_base_usd':1,'output_root':str(self.root)}
        path=Path(self.tmp.name)/'approval.json';path.write_text(json.dumps(approval))
        (self.root/'receipts').mkdir();(self.root/'receipts/ink-wet.json').write_text('{"status":"outcome_unknown"}')
        with patch.object(generate_sfx,'read_key',side_effect=AssertionError('secret read')):
            with self.assertRaisesRegex(ValueError,'no automatic retry'):
                generate_sfx.batch(TOOLS/'catalog.json',path,self.root,['ink-wet'])

    def test_paid_approval_cannot_be_reused_for_another_output_bank(self):
        raw=(TOOLS/'catalog.json').read_bytes()
        approval={'approved':True,'catalog_sha256':hashlib.sha256(raw).hexdigest(),'count':32,'total_seconds':109.5,'max_estimated_base_usd':1,'output_root':str(self.root/'different')}
        path=Path(self.tmp.name)/'approval.json';path.write_text(json.dumps(approval))
        with patch.object(generate_sfx,'read_key',side_effect=AssertionError('secret read')):
            with self.assertRaisesRegex(ValueError,'output directory'):generate_sfx.batch(TOOLS/'catalog.json',path,self.root)

    def test_review_needs_observations_and_binds_current_files(self):
        self.fixture()
        with self.assertRaises(ValueError):library.record_review(self.root,'music','test','','')
        result=library.record_review(self.root,'music','test','Test fixture','Synthetic fixture audition record for test only')
        self.assertEqual(result['review'],'approved')
        item=library.manifest(self.root)['music']['test']
        self.assertEqual(item['review_evidence']['source_hashes'],item['files'])
        path=self.root/'music/test/harmony.wav';path.write_bytes(b'changed')
        with self.assertRaises(ValueError):library.record_review(self.root,'music','test','Test fixture','Changed file must fail')

    def test_approved_effect_review_requires_an_interior_anchor(self):
        self.fixture()
        for anchor in [None,-.1,1, float('nan')]:
            with self.assertRaises(ValueError):library.record_review(self.root,'sfx','test','Test fixture','Fixture observation',anchor)
        self.assertEqual(library.record_review(self.root,'sfx','test','Test fixture','Fixture onset',.1)['review'],'approved')

if __name__=='__main__':unittest.main()
