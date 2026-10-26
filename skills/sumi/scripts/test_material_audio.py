"""Offline checks for real sound outputs, timing and existing score compatibility."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest
import wave

AUDIO = Path(__file__).resolve().parents[1] / 'assets/procedural-audio'
spec = importlib.util.spec_from_file_location('sumi_material_test', AUDIO / 'material_sfx.py')
material = importlib.util.module_from_spec(spec)
spec.loader.exec_module(material)


class MaterialAudioTests(unittest.TestCase):
    def test_all_materials_finite_distinct_and_sized(self):
        signatures = set()
        for kind in sorted(material.KINDS):
            random.seed(13)
            samples = material.render(kind, .137)
            self.assertEqual(len(samples), round(.137 * 48000))
            self.assertTrue(all(math.isfinite(x) for x in samples))
            self.assertGreater(max(abs(x) for x in samples), .001)
            signatures.add(hashlib.sha256(repr(samples).encode()).hexdigest())
        self.assertEqual(len(signatures), len(material.KINDS))

    def test_membrane_has_decay(self):
        random.seed(4)
        samples = material.render('drum', .8)
        first = sum(x*x for x in samples[240:4800])
        last = sum(x*x for x in samples[-4800:-240])
        self.assertGreater(first, 10 * last)

    def test_bad_parameters_rejected(self):
        for duration in [float('nan'), float('inf'), True, -.1, 0, 121]:
            with self.assertRaises(ValueError): material.render('brush', duration)
        with self.assertRaises(ValueError): material.render('unknown', .1)
        with self.assertRaises(ValueError): material.render('blade', .1, 24001)

    def test_score_reproducible_pan_duration_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            score = {'duration': .7, 'seed': 21, 'fade_in': 0, 'fade_out': .02,
                     'events': [{'at': .1, 'duration': .3, 'kind': 'drum',
                                 'gain': .5, 'pan': -1, 'stem': 'sfx'}]}
            path = root / 'score.json'; path.write_text(json.dumps(score))
            def run(dest):
                return subprocess.run([sys.executable, str(AUDIO / 'render_audio.py'),
                                       str(path), '--out', str(dest)], capture_output=True)
            self.assertEqual(run(root / 'a').returncode, 0)
            self.assertEqual(run(root / 'b').returncode, 0)
            a = root / 'a/sfx.wav'
            self.assertEqual(a.read_bytes(), (root / 'b/sfx.wav').read_bytes())
            with wave.open(str(a)) as f:
                self.assertEqual((f.getframerate(), f.getnchannels(), f.getnframes()),
                                 (48000, 2, 33600))
                from array import array
                data = array('h', f.readframes(f.getnframes()))
                if sys.byteorder != 'little': data.byteswap()
                self.assertEqual(max(abs(x) for x in data[1::2]), 0)
                self.assertGreater(max(abs(x) for x in data[::2]), 100)
                self.assertEqual(max(abs(x) for x in data[:9600]), 0)
            before = a.read_bytes()
            self.assertNotEqual(run(root / 'a').returncode, 0)
            self.assertEqual(a.read_bytes(), before)

    def test_existing_demo_still_renders(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(AUDIO / 'render_audio.py'),
                                     str(AUDIO / 'example-score.json'), '--out',
                                     str(Path(tmp) / 'render')], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())


if __name__ == '__main__': unittest.main()
