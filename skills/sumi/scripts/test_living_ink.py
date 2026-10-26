#!/usr/bin/env python3
"""Synthetic metadata regression tests, not visual proof or real media fixtures."""
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_living_ink import REVIEW_AREAS, validate
from validate_shot_plan import plan_digest, validate_base, validate as validate_all

SCRIPTS = Path(__file__).resolve().parent


class LivingInkGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan, self.review = self.fixture()

    def asset(self, name, content=None):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((content if content is not None else "synthetic test asset " + name).encode())
        return {"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def fixture(self):
        paper = self.asset("paper.png")
        source = self.asset("ink.js")
        study = self.asset("private-source-sheet.png")
        script = self.asset("script.txt", "A puppy found a home.")
        audio = self.asset("approved-narration.wav")
        master = self.asset("puppy-master.png")
        pose_image = self.asset("puppy-pose.png")
        overlay = self.asset("puppy-overlay.png")
        clip = self.asset("proof.mp4")
        a = self.asset("frame-a.png")
        b = self.asset("frame-b.png")
        pose = {
            "id": "rest", "image": pose_image, "review_overlay": overlay, "full_body": True,
            "master_sha256": master["sha256"], "view": "side", "facing": "right",
            "near_far_order": "left legs near", "joint_orientation": "species appropriate",
            "hand_paw_orientation": "pads on support", "support_contact": "grounded",
            "observation": "Synthetic metadata fixture only.",
            "checks": {k: True for k in ["limb_count", "proportions", "joint_bends", "facing", "contact", "identity"]},
            "unresolved": [], "parts": [],
        }
        shot_proof = {
            "clip": clip, "review": self.asset("shot-review.txt"),
            "adjacent_frame_sheet": self.asset("adjacent.png"),
            "neutral_background_clip": clip,
            "normal_speed": True, "adjacent_frames": True, "final_art": True,
            "method_visible_without_colour_camera": True, "japanese_sumi_identity": True,
            "unresolved": [], "observation": "Synthetic metadata fixture only.",
        }
        shot = {
            "id": "s1", "method": "living-ink", "start": 0, "end": 4,
            "mechanism": {"type": "evolving-ink-mass", "files": [source]},
            "performance": "Ink gathers into the resting puppy", "camera": "fixed",
            "transition": "ink drop birth", "strict_identity": "Japanese ink",
            "economy": "one whole pose", "pose_fps": 10, "simulation_fps": 30,
            "assets": [pose_image], "characters": [{"id": "puppy", "poses": ["rest"]}],
            "critical_windows": [], "proof": shot_proof,
            "living_ink": {
                "drawing_fps": 10, "ink_simulation_fps": 30, "output_fps": 30,
                "ink_mass_change": "density gathers and splits before resolving",
                "whole_pose_strategy": "resting drawing matches master", "negative_space": "left third open",
                "drawing_budget": {"unique_source_drawings": 1, "purpose": "A quiet resting moment",
                                   "risk": "Keep support and identity readable", "reuse_rationale": "Deliberate rest holds one pose"},
                "exposure_plan": [{"id": "rest-hold", "character_id": "puppy", "pose_ids": ["rest"],
                                   "start": 0, "end": 4, "exposure": "hold", "exposure_ticks": [40],
                                   "action": "Resting puppy", "hold_reason": "Quiet rest needs no fabricated limb movement"}],
                "camera_cues": [{"id": "home-focus", "start": 0, "end": 4, "subject_id": "puppy",
                                 "spoken_cue": "A puppy found a home", "framing": "whole body",
                                 "angle": "eye level", "movement": "hold", "story_reason": "Let resting support be seen"}],
                "layers": [
                    {"role": "paper", "files": [paper], "motion_rule": "fixed substrate"},
                    {"role": "environment", "files": [], "empty_reason": "neutral diagnostic", "motion_rule": "none"},
                    {"role": "subject", "files": [pose_image], "motion_rule": "local ink mass evolves"},
                    {"role": "foreground", "files": [], "empty_reason": "neutral diagnostic", "motion_rule": "none"},
                ],
            },
        }
        config = {
            "schema": 2,
            "transition_selection_rationale": "One local birth is enough for this short study.",
            "story": {"script": script, "analysis": "Shelter follows isolation.",
                      "colour_reason": "One red mark means home.", "required_visual_actions": ["puppy settles"]},
            "palette": {
                "base": ["black", "charcoal", "off-white"],
                "accent": {"name": "crimson", "hex": "#A62028", "story_meaning": "home", "permitted_uses": ["home caption"]},
                "monochrome_target": .85, "accent_target": .15,
                "negative_space_target": [.30, .40], "ratio_is_directional": True,
            },
            "paper": {"image": paper, "coverage": [0, 4], "continuity": "single-substrate",
                      "canvas_space": "screen-fixed", "wash_behavior": "ink clears, paper remains"},
            "source_files": [source],
            "source_references": [{"source_name": "private reference", "evidence": study,
                                   "observed_motion": "wet edge grows", "coverage": "one passage",
                                   "limits": "does not claim all-frame study"}],
            "narration": {"mode": "existing-approved-take", "audio": audio, "transcript": script,
                          "approved_text": "A puppy found a home.", "approved_take_sha256": audio["sha256"],
                          "preserve_wording": True, "approval_record": "fixture approval",
                          "delivery": "saved calm take", "processing": "unchanged source"},
            "required_words": ["HOME"],
            "sound": {"method": "local-python", "direction": "quiet tactile sound",
                      "events": [{"id": "drop", "kind": "tactile", "start": 0, "end": .4,
                                  "trigger": "birth", "description": "wet drop"}]},
            "captions": {"mode": "ink-phrases", "readability_plan": "open area with high contrast",
                         "items": [{"id": "home", "text": "HOME", "start": 2, "end": 4,
                                    "placement": "left blank paper", "readability": "two-second hold",
                                    "reveal": "brush-matte", "accent_hex": "#A62028"}]},
            "transitions": [{"id": "birth", "kind": "ink-drop-birth", "start": 0, "end": 1.8,
                             "classification": "local", "story_reason": "Introduce the resting subject",
                             "from_shot": None, "to_shot": "s1", "material_cause": "drop on paper",
                             "onset": "one bead", "propagation": "wet boundary branches",
                             "resolution": "puppy density resolves", "preserves_paper": True,
                             "sound_event": "drop"}],
        }
        plan = {
            "schema": 2, "identity": "japanese-sumi", "duration": 4, "output_fps": 30,
            "approval": {"script": "fixture", "direction": "fixture", "duration": "fixture"},
            "characters": [{"id": "puppy", "master": master, "full_body": True, "species": "dog",
                            "view": "side", "facing": "right", "limb_inventory": "four paws", "poses": [pose]}],
            "shots": [shot], "living_ink": config, "proof": {},
        }
        evidence = [
            {"id": "script", "kind": "script", "file": script},
            {"id": "master", "kind": "character-master", "file": master},
            {"id": "pose", "kind": "whole-pose", "file": pose_image},
            {"id": "reference", "kind": "source-reference", "file": study},
            {"id": "a", "kind": "rendered-frame", "file": a, "time": .2, "clip_sha256": clip["sha256"]},
            {"id": "b", "kind": "rendered-frame", "file": b, "time": 1.2, "clip_sha256": clip["sha256"]},
            {"id": "clip", "kind": "clip", "file": clip, "start": 0, "end": 4,
             "playback_rate": 1, "watched_complete": True},
            {"id": "audio", "kind": "audio", "file": audio},
        ]
        review = {
            "schema": 1, "plan_sha256": plan_digest(plan), "verdict": "pass",
            "reviewer": {"kind": "ai", "name": "synthetic test reviewer", "model": "fixture",
                         "completed_at": "2026-10-20T12:00:00+05:00",
                         "inspection": "actual-files-and-normal-playback"},
            "evidence": evidence,
            "observations": [{"area": area, "result": "pass", "finding": "Synthetic metadata fixture, not a real observation.",
                              "evidence_ids": ["a", "b", "clip", "script", "reference", "master", "pose", "audio"],
                              "transition_ids": ["birth"] if area == "transition-material" else []}
                             for area in sorted(REVIEW_AREAS)],
            "issues": [],
        }
        for area, key, value in [("performance-exposure", "exposure_ids", "rest-hold"),
                                 ("camera-story-focus", "camera_cue_ids", "home-focus")]:
            review["observations"].append({
                "area": area, "result": "pass", "shot_id": "s1", key: [value],
                "finding": "Synthetic metadata fixture only, not genuine film review.",
                "evidence_ids": ["a", "b", "clip"]
            })
        plan["proof"]["plan_sha256"] = plan_digest(plan)
        self.save_review(plan, review)
        return plan, review

    def save_review(self, plan=None, review=None):
        plan = self.plan if plan is None else plan
        review = self.review if review is None else review
        plan["proof"]["living_ink_review"] = self.asset("ai-review.json", json.dumps(review))

    def check_fails(self, fragment, stage="proof"):
        errors = validate(self.plan, self.root, stage)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_complete_records_pass_both_gates(self):
        self.assertEqual(validate_base(self.plan, self.root, "proof"), [])
        self.assertEqual(validate(self.plan, self.root, "proof"), [])
        self.assertEqual(validate_all(self.plan, self.root, "proof"), [])

    def test_standard_gate_dispatches_living_ink_checks(self):
        del self.plan["living_ink"]
        self.plan["proof"]["plan_sha256"] = plan_digest(self.plan)
        self.assertEqual(validate_base(self.plan, self.root, "proof"), [])
        errors = validate_all(self.plan, self.root, "proof")
        self.assertTrue(any("living_ink.schema" in error for error in errors), errors)

    def test_standard_cli_dispatches_living_ink_checks(self):
        del self.plan["living_ink"]
        self.plan["proof"]["plan_sha256"] = plan_digest(self.plan)
        path = self.root / "shot-plan.json"
        path.write_text(json.dumps(self.plan))
        result = subprocess.run([sys.executable, str(SCRIPTS / "validate_shot_plan.py"), str(path),
                                 "--stage", "proof"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertTrue(any("living_ink.schema" in error for error in json.loads(result.stdout)["errors"]))

    def test_missing_method_gate_fails_closed_without_affecting_other_methods(self):
        isolated = self.root / "isolated-scripts"
        isolated.mkdir()
        for name in ["validate_shot_plan.py", "plan_provenance.py", "sumi_catalog.py"]:
            shutil.copy2(SCRIPTS / name, isolated / name)
        path = self.root / "shot-plan.json"
        path.write_text(json.dumps(self.plan))
        command = [sys.executable, str(isolated / "validate_shot_plan.py"), str(path), "--stage", "proof"]
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertTrue(any("required validator is unavailable" in error for error in json.loads(failed.stdout)["errors"]))
        self.plan["shots"][0]["method"] = "drawn-acting"
        self.plan["shots"][0]["mechanism"]["type"] = "whole-pose-replacement"
        self.plan["proof"]["plan_sha256"] = plan_digest(self.plan)
        path.write_text(json.dumps(self.plan))
        passed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_unconducted_review_blocks_proof_but_assets_can_proceed(self):
        self.plan["proof"]["living_ink_review"] = None
        self.assertEqual(validate(self.plan, self.root, "assets"), [])
        self.check_fails("completed AI visual review")

    def test_changed_source_invalidates_hash(self):
        (self.root / "ink.js").write_text("changed mechanism")
        self.check_fails("stale or missing SHA-256")

    def test_changed_plan_invalidates_review_even_after_asset_hash_updated(self):
        self.plan["living_ink"]["source_files"][0] = self.asset("ink.js", "new authored mechanism")
        self.check_fails("visual review is stale")

    def test_second_accent_rejected(self):
        self.plan["living_ink"]["captions"]["items"][0]["accent_hex"] = "#00FF00"
        self.check_fails("second accent", "assets")

    def test_paper_swap_rejected(self):
        self.plan["shots"][0]["living_ink"]["layers"][0]["files"] = [self.asset("other-paper.png")]
        self.check_fails("same persistent paper", "assets")

    def test_incomplete_four_layer_stage_rejected(self):
        self.plan["shots"][0]["living_ink"]["layers"].pop()
        self.check_fails("exactly four", "assets")

    def test_60fps_export_is_allowed_with_10fps_drawings(self):
        self.plan["output_fps"] = 60
        self.plan["shots"][0]["living_ink"]["output_fps"] = 60
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_drawing_and_output_cadence_are_not_confused(self):
        self.plan["shots"][0]["living_ink"]["drawing_fps"] = 30
        self.check_fails("drawing exposure must be 8–12", "assets")

    def test_changed_narration_take_rejected(self):
        self.plan["living_ink"]["narration"]["audio"] = self.asset("replacement.wav")
        self.check_fails("approved audio hash", "assets")

    def test_missing_required_words_rejected(self):
        self.plan["living_ink"]["required_words"].append("THREE MONTHS")
        self.check_fails("required words missing", "assets")

    def test_hard_cut_and_missing_boundary_rejected(self):
        first = self.plan["shots"][0]
        first["end"] = 2
        second = copy.deepcopy(first)
        second.update(id="s2", start=2, end=4)
        self.plan["shots"].append(second)
        self.check_fails("missing organic transition", "assets")
        self.plan["living_ink"]["transitions"][0]["kind"] = "cross-dissolve"
        self.check_fails("unsupported transition", "assets")

    def test_single_still_cannot_certify_motion(self):
        self.review["evidence"] = [e for e in self.review["evidence"] if e["id"] != "b"]
        for observation in self.review["observations"]:
            observation["evidence_ids"].remove("b")
        self.save_review()
        self.check_fails("at least two distinct")

    def test_slow_playback_only_rejected(self):
        next(e for e in self.review["evidence"] if e["id"] == "clip")["playback_rate"] = .25
        self.save_review()
        self.check_fails("normal-speed playback")

    def test_unrelated_review_clip_rejected(self):
        next(e for e in self.review["evidence"] if e["id"] == "clip")["file"] = self.asset("other.mp4")
        self.save_review()
        self.check_fails("differs from current shot proof")

    def test_frame_must_bind_to_reviewed_clip(self):
        next(e for e in self.review["evidence"] if e["id"] == "a")["clip_sha256"] = "0" * 64
        self.save_review()
        self.check_fails("identify its reviewed clip")

    def test_actual_character_master_must_be_inspected(self):
        next(e for e in self.review["evidence"] if e["id"] == "master")["file"] = self.asset("wrong-master.png")
        self.save_review()
        self.check_fails("missing actual character master")

    def test_transition_needs_temporal_inspection_at_its_own_times(self):
        next(e for e in self.review["evidence"] if e["id"] == "b")["time"] = 3
        self.save_review()
        self.check_fails("transition needs observed")

    def test_open_blocking_issue_cannot_pass(self):
        self.review["issues"] = [{"description": "Backwards paw", "severity": "blocking", "status": "open"}]
        self.save_review()
        self.check_fails("unresolved blocking")

    def test_review_does_not_auto_approve(self):
        self.review["verdict"] = None
        self.save_review()
        self.check_fails("has not passed")

    def test_missing_inspection_result_rejected(self):
        self.review["observations"][0]["result"] = None
        self.save_review()
        self.check_fails("explicit completed result")

    def test_required_anatomy_cannot_be_skipped(self):
        next(o for o in self.review["observations"] if o["area"] == "anatomy-contact")["result"] = "not-applicable"
        self.save_review()
        self.check_fails("cannot be marked not-applicable")

    def test_escaped_file_rejected(self):
        self.plan["living_ink"]["paper"]["image"]["path"] = "../outside.png"
        self.check_fails("outside-project", "assets")

    def test_historical_extension_one_still_valid_without_new_records(self):
        self.plan["living_ink"]["schema"] = 1
        settings = self.plan["shots"][0]["living_ink"]
        for key in ["drawing_budget", "exposure_plan", "camera_cues"]:
            settings.pop(key)
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_new_extension_requires_drawing_budget_and_camera(self):
        settings = self.plan["shots"][0]["living_ink"]
        settings.pop("drawing_budget")
        settings.pop("camera_cues")
        self.check_fails("unique_source_drawings", "assets")
        self.check_fails("camera subject cues", "assets")

    def add_pose_alias(self, roi=None):
        pose = copy.deepcopy(self.plan["characters"][0]["poses"][0])
        pose["id"] = "alias"
        if roi is not None:
            pose.update(roi_xywh=roi, board_dimensions=[100, 100])
        self.plan["characters"][0]["poses"].append(pose)
        self.plan["shots"][0]["characters"][0]["poses"].append("alias")
        entry = self.plan["shots"][0]["living_ink"]["exposure_plan"][0]
        entry.update(pose_ids=["rest", "alias"], exposure="one-shot", exposure_ticks=[20, 20])
        return pose

    def test_pose_aliases_and_transforms_do_not_inflate_count(self):
        alias = self.add_pose_alias()
        alias.update(crop_id="renamed", transform={"scale": 2, "rotate": 90})
        self.assertEqual(validate(self.plan, self.root, "assets"), [])
        self.plan["shots"][0]["living_ink"]["drawing_budget"]["unique_source_drawings"] = 2
        self.check_fails("distinct source hash/ROI count", "assets")

    def test_distinct_bounded_board_regions_count_separately(self):
        original = self.plan["characters"][0]["poses"][0]
        original.update(roi_xywh=[0, 0, 50, 100], board_dimensions=[100, 100])
        self.add_pose_alias([50, 0, 50, 100])
        self.plan["shots"][0]["living_ink"]["drawing_budget"]["unique_source_drawings"] = 2
        self.assertEqual(validate(self.plan, self.root, "assets"), [])
        self.plan["characters"][0]["poses"][1]["roi_xywh"] = [51, 0, 50, 100]
        self.check_fails("valid bounded ROI", "assets")

    def test_same_region_with_new_crop_label_is_one_drawing(self):
        self.plan["characters"][0]["poses"][0].update(roi_xywh=[0, 0, 50, 100], board_dimensions=[100, 100])
        alias = self.add_pose_alias([0, 0, 50, 100])
        alias["crop_id"] = "different-label"
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_full_board_roi_alias_does_not_create_second_drawing(self):
        self.add_pose_alias([0, 0, 100, 100])
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_missing_exposure_and_unknown_pose_rejected(self):
        self.plan["shots"][0]["living_ink"]["exposure_plan"][0]["pose_ids"] = ["unknown"]
        self.check_fails("declared whole poses", "assets")
        self.check_fails("every declared used pose", "assets")

    def test_exposure_duration_ticks_and_overlap_rejected(self):
        settings = self.plan["shots"][0]["living_ink"]
        settings["exposure_plan"][0]["exposure_ticks"] = [60]
        self.check_fails("sequence exceeds", "assets")
        settings["exposure_plan"][0]["exposure_ticks"] = [40]
        duplicate = copy.deepcopy(settings["exposure_plan"][0])
        duplicate["id"] = "overlap"
        settings["exposure_plan"].append(duplicate)
        self.check_fails("overlapping whole-pose", "assets")

    def test_deliberate_hold_allowed_but_must_explain_it(self):
        self.assertEqual(validate(self.plan, self.root, "assets"), [])
        del self.plan["shots"][0]["living_ink"]["exposure_plan"][0]["hold_reason"]
        self.check_fails("hold_reason", "assets")

    def test_camera_requires_real_narration_phrase_and_subject(self):
        cue = self.plan["shots"][0]["living_ink"]["camera_cues"][0]
        cue["spoken_cue"] = "Not in the approved words"
        self.check_fails("occur in approved narration", "assets")
        cue["subject_id"] = "unknown-character"
        self.check_fails("camera subject must", "assets")

    def test_silent_visual_camera_beat_can_be_explained(self):
        cue = self.plan["shots"][0]["living_ink"]["camera_cues"][0]
        cue.pop("spoken_cue")
        cue.update(visual_cue="The puppy rests after the line", silent_beat_reason="Intentional visual pause")
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_local_material_continuity_covers_boundary_without_major_transition(self):
        first = self.plan["shots"][0]
        first["end"] = 2
        settings = first["living_ink"]
        settings["exposure_plan"][0].update(end=2, exposure_ticks=[20])
        settings["camera_cues"][0]["end"] = 2
        second = copy.deepcopy(first)
        second.update(id="s2", start=2, end=4)
        second["living_ink"]["exposure_plan"][0].update(id="rest-2", start=2, end=4)
        second["living_ink"]["camera_cues"][0].update(id="focus-2", start=2, end=4)
        self.plan["shots"].append(second)
        self.plan["living_ink"]["transitions"].append({
            "id": "quiet-boundary", "kind": "material-continuity", "classification": "local",
            "start": 1.8, "end": 2.2, "from_shot": "s1", "to_shot": "s2",
            "material_cause": "The existing wet shoulder settles", "onset": "Retained stain",
            "propagation": "Small edge recedes", "resolution": "Rest remains visible",
            "story_reason": "Continue the quiet rest without a showcase transition",
            "preserves_paper": True, "sound_event": None, "sound_reason": "Quiet local settlement"
        })
        self.assertEqual(validate(self.plan, self.root, "assets"), [])

    def test_local_sound_omission_needs_explicit_reason(self):
        self.plan["living_ink"]["transitions"][0]["sound_event"] = None
        self.check_fails("quiet-local reason", "assets")

    def test_exposure_and_camera_review_must_bind_to_current_ids(self):
        for observation in self.review["observations"]:
            if observation["area"] == "performance-exposure":
                observation["exposure_ids"] = ["unrelated"]
            if observation["area"] == "camera-story-focus":
                observation["camera_cue_ids"] = ["unrelated"]
        self.save_review()
        self.check_fails("rest-hold: needs two observed")
        self.check_fails("home-focus: needs two observed")


class InitializerGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def initialize(self, method):
        destination = self.root / method
        result = subprocess.run([
            sys.executable, str(SCRIPTS / "new_remotion_project.py"), str(destination),
            "--method", method, "--seconds", "30", "--fps", "60"
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return destination, json.loads((destination / "shot-plan.json").read_text())

    def test_living_ink_initializer_is_incomplete_and_guarded(self):
        destination, plan = self.initialize("living-ink")
        self.assertEqual(plan["living_ink"]["paper"]["coverage"], [0, 30])
        self.assertEqual(plan["shots"][0]["living_ink"]["output_fps"], 60)
        self.assertEqual(plan["shots"][0]["living_ink"]["drawing_fps"], 12)
        self.assertEqual(plan["living_ink"]["schema"], 2)
        self.assertIsNone(plan["shots"][0]["living_ink"]["drawing_budget"]["unique_source_drawings"])
        self.assertEqual(plan["shots"][0]["living_ink"]["exposure_plan"], [])
        self.assertEqual(plan["shots"][0]["living_ink"]["camera_cues"], [])
        self.assertIsNone(plan["proof"]["living_ink_review"])
        self.assertEqual(plan["approval"], {"script": "", "direction": "", "duration": ""})
        self.assertFalse((destination / "node_modules").exists())
        self.assertFalse((destination / "out" / "film.mp4").exists())
        for name in ["validate_shot_plan.py", "validate_living_ink.py", "plan_provenance.py"]:
            self.assertTrue((destination / "scripts" / name).is_file())
        self.assertTrue((destination / "LIVING-INK-REVIEW.md").is_file())
        self.assertTrue((destination / "ink-transitions" / "fields.mjs").is_file())
        self.assertTrue((destination / "ink-transitions" / "test-fields.mjs").is_file())
        result = subprocess.run([
            sys.executable, str(destination / "scripts" / "validate_shot_plan.py"),
            str(destination / "shot-plan.json"), "--stage", "proof"
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        errors = json.loads(result.stdout)["errors"]
        self.assertTrue(any("completed AI visual review" in error for error in errors), errors)

    def test_other_methods_do_not_receive_living_ink_requirements(self):
        destination, plan = self.initialize("drawn-acting")
        self.assertNotIn("living_ink", plan)
        self.assertNotIn("living_ink", plan["shots"][0])
        self.assertNotIn("living_ink_review", plan["proof"])
        self.assertFalse((destination / "LIVING-INK-REVIEW.md").exists())
        self.assertFalse((destination / "ink-transitions").exists())
        errors = validate_all(plan, destination, "proof")
        self.assertFalse(any(error.startswith("Living Ink:") for error in errors), errors)

    @unittest.skipUnless(shutil.which("npm"), "npm not installed; Python dispatch tests still run")
    def test_standard_npm_render_stops_at_unreviewed_workflow(self):
        destination, _ = self.initialize("living-ink")
        result = subprocess.run(["npm", "run", "render"], cwd=destination,
                                capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("completed AI visual review", result.stdout)
        self.assertNotIn("remotion: command not found", result.stdout + result.stderr)
        self.assertFalse((destination / "out" / "film.mp4").exists())


if __name__ == "__main__":
    unittest.main()
