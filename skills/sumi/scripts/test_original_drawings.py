"""Original density provenance checks; synthetic fixtures do not certify art."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from validate_style_profile import validate


class OriginalDrawingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        board = self.root / 'board.svg'
        board.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="100">'
                         + ''.join(f'<circle cx="{i*100+50}" cy="50" r="{10+i}"/>'
                                   for i in range(14)) + '</svg>')
        record = {'path': board.name, 'sha256': hashlib.sha256(board.read_bytes()).hexdigest()}
        self.drawing = {'minimum_distinct_drawings': 14, 'sequence_id': 'emotional-action',
                        'source_images': [{'id': f'pose-{i}', 'file': record,
                                           'board_dimensions': [1400, 100],
                                           'roi_xywh': [i*100, 0, 100, 100]} for i in range(14)],
                        'exposure_plan': [{'source_ids': [f'pose-{i}' for i in range(14)],
                                           'exposure_frames': [2]*14}],
                        'deliberate_stillness': False, 'stillness_reason': ''}
        self.plan = {'catalog': 'three-styles-v4', 'style': 'sumi-original',
                     'release_version': '4.5.0', 'style_profile': {},
                     'shots': [{'id': 'emotion', 'style': 'sumi-original',
                                'style_profile': {'original_drawings': self.drawing}}]}

    def tearDown(self): self.temp.cleanup()

    def density_errors(self):
        return [e for e in validate(self.plan, self.root) if 'Original drawing plan' in e]

    def test_one_sheet_fourteen_bounded_drawings(self):
        self.assertEqual(self.density_errors(), [])

    def test_relabelled_duplicate_not_fourteenth(self):
        self.drawing['source_images'][-1] = copy.deepcopy(self.drawing['source_images'][0])
        self.drawing['source_images'][-1]['id'] = 'different-name'
        self.assertTrue(any('fewer than 14' in e for e in self.density_errors()))

    def test_missing_or_unbounded_source_rejected(self):
        self.drawing['source_images'][-1]['roi_xywh'] = [1400, 0, 100, 100]
        self.assertTrue(self.density_errors())

    def test_changed_board_not_accepted(self):
        (self.root / 'board.svg').write_text('changed after review')
        self.assertTrue(any('stale hash' in e for e in self.density_errors()))

    def test_deliberate_stillness_needs_reason(self):
        self.drawing.update(deliberate_stillness=True, source_images=[])
        self.assertTrue(self.density_errors())
        self.drawing['stillness_reason'] = 'Intentionally unresponsive aftermath tableau; motion would contradict the scene.'
        self.assertEqual(self.density_errors(), [])

    def test_historical_release_preserved(self):
        self.plan['release_version'] = '4.4.8'
        self.drawing.clear()
        self.assertEqual(self.density_errors(), [])


class OriginalRateTests(unittest.TestCase):
    def setUp(self):
        OriginalDrawingTests.setUp(self)
        self.plan.update(release_version='4.5.1', output_fps=28)
        shot = self.plan['shots'][0]
        shot.update(start=0, end=1, pose_fps=14, simulation_fps=28)
        shot['style_profile']['cadence'] = {'output_fps': 28, 'character_update_fps': 14,
                                          'exposure_frames': 2}
        self.drawing.pop('minimum_distinct_drawings')
        self.drawing['minimum_drawings_per_second'] = 14
        self.drawing['exposure_plan'] = [{'source_id': f'pose-{i}',
                                          'start_frame': i*2, 'end_frame': i*2+2}
                                         for i in range(14)]

    def tearDown(self): OriginalDrawingTests.tearDown(self)

    def errors(self):
        return [e for e in validate(self.plan, self.root)
                if 'Original drawing rate' in e or 'requires 28fps' in e
                or 'Original cadence' in e]

    def test_fourteen_in_one_second(self):
        self.assertEqual(self.errors(), [])

    def test_repeated_fourteen_state_cycle_counted_as_exposures(self):
        self.plan['shots'][0]['end'] = 2
        self.drawing['exposure_plan'] += [{'source_id': f'pose-{i}',
                                           'start_frame': 28+i*2, 'end_frame': 30+i*2}
                                          for i in range(14)]
        self.assertEqual(self.errors(), [])

    def test_fourteen_per_scene_spread_across_two_seconds_fails(self):
        self.plan['shots'][0]['end'] = 2
        for i, entry in enumerate(self.drawing['exposure_plan']):
            entry.update(start_frame=i*4, end_frame=i*4+4)
        self.assertTrue(self.errors())

    def test_thirteen_state_cycle_does_not_count_as_fourteen(self):
        for i, entry in enumerate(self.drawing['exposure_plan']):
            entry['source_id'] = f'pose-{i % 13}'
        self.assertTrue(self.errors())

    def test_aliases_do_not_inflate_the_rate(self):
        self.drawing['source_images'][-1]['roi_xywh'] = [0, 0, 100, 100]
        self.assertTrue(self.errors())

    def test_24fps_does_not_fake_14_on_twos(self):
        self.plan.update(output_fps=24)
        self.plan['shots'][0].update(pose_fps=12, simulation_fps=24)
        self.assertTrue(self.errors())

    def test_gap_in_actual_exposure_coverage_fails(self):
        del self.drawing['exposure_plan'][5]
        self.assertTrue(self.errors())

    def test_short_shot_needs_proportionate_states(self):
        self.plan['shots'][0]['end'] = 8 / 28
        self.drawing['exposure_plan'] = self.drawing['exposure_plan'][:4]
        self.assertEqual(self.errors(), [])


class OriginalFifteenRateTests(unittest.TestCase):
    def setUp(self):
        OriginalRateTests.setUp(self)
        board = self.root / 'board.svg'
        board.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="100">'
                         + ''.join(f'<circle cx="{i*100+50}" cy="50" r="{10+i}"/>'
                                   for i in range(15)) + '</svg>')
        record = {'path': board.name, 'sha256': hashlib.sha256(board.read_bytes()).hexdigest()}
        self.drawing['source_images'] = [
            {'id': f'pose-{i}', 'file': record, 'board_dimensions': [1500, 100],
             'roi_xywh': [i*100, 0, 100, 100]} for i in range(15)]
        self.drawing['minimum_drawings_per_second'] = 15
        self.drawing['exposure_plan'] = [{'source_id': f'pose-{i}',
            'start_frame': i*2, 'end_frame': i*2+2} for i in range(15)]
        self.plan.update(release_version='4.5.3', output_fps=30)
        shot = self.plan['shots'][0]
        shot.update(pose_fps=15, simulation_fps=30)
        shot['style_profile']['cadence'].update(output_fps=30, character_update_fps=15)

    def tearDown(self): OriginalDrawingTests.tearDown(self)

    def errors(self):
        return [e for e in validate(self.plan, self.root)
                if 'Original drawing rate' in e or 'requires 30fps' in e
                or 'Original cadence' in e]

    def test_fifteen_drawings_one_second(self):
        self.assertEqual(self.errors(), [])

    def test_fourteen_state_cycle_is_insufficient(self):
        self.drawing['exposure_plan'][-1]['source_id'] = 'pose-0'
        self.assertTrue(self.errors())

    def test_aliases_are_not_fifteen(self):
        self.drawing['source_images'][-1]['roi_xywh'] = [0, 0, 100, 100]
        self.assertTrue(self.errors())

    def test_gapped_exposures_rejected(self):
        del self.drawing['exposure_plan'][6]
        self.assertTrue(self.errors())

    def test_old_28fps_rejected_for_new_film(self):
        self.plan['output_fps'] = 28
        self.plan['shots'][0].update(pose_fps=14, simulation_fps=28)
        self.assertTrue(self.errors())

    def test_two_seconds_checked_cycle(self):
        self.plan['shots'][0]['end'] = 2
        self.drawing['exposure_plan'] += [{'source_id': f'pose-{i}',
            'start_frame': 30+i*2, 'end_frame': 32+i*2} for i in range(15)]
        self.assertEqual(self.errors(), [])

    def test_fifteen_spread_over_two_seconds_rejected(self):
        self.plan['shots'][0]['end'] = 2
        for i, entry in enumerate(self.drawing['exposure_plan']):
            entry.update(start_frame=i*4, end_frame=i*4+4)
        self.assertTrue(self.errors())

    def test_short_shot_proportionate(self):
        self.plan['shots'][0]['end'] = 8/30
        self.drawing['exposure_plan'] = self.drawing['exposure_plan'][:4]
        self.assertEqual(self.errors(), [])

    def test_stillness_needs_documented_reason(self):
        self.drawing.update(deliberate_stillness=True, source_images=[], exposure_plan=[])
        self.assertTrue(self.errors())
        self.drawing['stillness_reason'] = 'Deliberately held response; no required physical action omitted.'
        self.assertEqual(self.errors(), [])

    def test_prior_452_contract_preserved(self):
        self.temp.cleanup()
        OriginalRateTests.setUp(self)
        self.plan['release_version'] = '4.5.2'
        self.assertEqual(OriginalRateTests.errors(self), [])


if __name__ == '__main__': unittest.main()
