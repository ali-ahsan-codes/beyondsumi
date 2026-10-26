#!/usr/bin/env python3
"""Living Ink evidence gate. Checks records and freshness, never visual truth.

validate_shot_plan.validate automatically dispatches this method-specific gate.
The CLI also runs the combined gate. No model calls or review auto-completion.
"""
import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path

from plan_provenance import plan_digest

TRANSITIONS = {
    "ink-drop-birth", "brush-stroke-action", "water-wash", "object-ink-morph",
    "material-continuity",
}
LAYER_ROLES = {"paper", "environment", "subject", "foreground"}
REVIEW_AREAS = {
    "story", "japanese-sumi-identity", "living-ink-motion", "paper-continuity",
    "anatomy-contact", "transition-material", "caption-readability",
    "audio-narration",
}
EVIDENCE_KINDS = {
    "script", "character-master", "whole-pose", "source-reference",
    "rendered-frame", "clip", "audio",
}


def validate(data, root, stage="assets"):
    """Return additive errors; root is the plan's directory.

    This gate applies to living-ink shots. Proof stage additionally requires a
    completed external AI review, bound to this exact plan and actual files.
    Metadata can document an inspection, but cannot prove it happened or was right.
    """
    errors = []
    root = Path(root).resolve()

    def need(ok, message):
        if not ok:
            errors.append("Living Ink: " + message)
        return bool(ok)

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    def obj(value):
        return value if isinstance(value, dict) else {}

    def seq(value):
        return value if isinstance(value, list) else []

    def words(record, names, label):
        for name in names:
            need(text(obj(record).get(name)), label + ": missing " + name)

    def file_record(record, label):
        record = obj(record)
        if not need(text(record.get("path")), label + ": file record required"):
            return None
        path = (root / record["path"]).resolve()
        if not need(root in path.parents and path.is_file() and path.stat().st_size > 0,
                    label + ": missing, empty or outside-project file"):
            return None
        need(record.get("sha256") == hashlib.sha256(path.read_bytes()).hexdigest(),
             label + ": stale or missing SHA-256")
        return path

    def time_range(start, end, label):
        return need(number(start) and number(end) and number(duration)
                    and 0 <= start < end <= duration, label + ": invalid time range")

    def normalize(value):
        return " ".join(value.split()) if isinstance(value, str) else ""

    if not isinstance(data, dict):
        return ["Living Ink: plan must be an object"]
    if stage not in {"assets", "proof"}:
        return ["Living Ink: stage must be assets or proof"]
    shots = [s for s in seq(data.get("shots")) if isinstance(s, dict) and s.get("method") == "living-ink"]
    if not shots:
        return []
    duration = data.get("duration")
    config = obj(data.get("living_ink"))
    need(config.get("schema") in {1, 2}, "living_ink.schema must be 1 (historical) or 2 (new plans)")
    extended = config.get("schema") == 2
    story = obj(config.get("story"))
    script_path = file_record(story.get("script"), "reviewed story/script")
    words(story, ["analysis", "colour_reason"], "story")
    actions = seq(story.get("required_visual_actions"))
    need(bool(actions) and all(text(a) for a in actions), "required visual actions must be explicit")

    palette = obj(config.get("palette"))
    need(palette.get("base") == ["black", "charcoal", "off-white"],
         "declare the monochrome black/charcoal/off-white base")
    accent = obj(palette.get("accent"))
    words(accent, ["name", "story_meaning"], "single accent")
    need(isinstance(accent.get("hex"), str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", accent["hex"]),
         "one accent hex colour required")
    uses = seq(accent.get("permitted_uses"))
    need(bool(uses) and all(text(v) for v in uses), "accent needs story-linked permitted uses")
    # These are composition targets, not exact pixel quotas for every frame.
    for key, value in (("monochrome_target", .85), ("accent_target", .15)):
        need(number(palette.get(key)) and abs(palette[key] - value) < .001,
             "declare the approximate " + key)
    negative = palette.get("negative_space_target")
    need(negative == [.30, .40], "declare 30–40% negative-space composition target")
    need(palette.get("ratio_is_directional") is True, "ratios are directional, not pixel quotas")

    paper = obj(config.get("paper"))
    file_record(paper.get("image"), "persistent paper")
    paper_hash = obj(paper.get("image")).get("sha256")
    need(paper.get("coverage") == [0, duration], "paper must cover the complete film")
    need(paper.get("continuity") == "single-substrate", "paper must remain one substrate")
    need(paper.get("canvas_space") == "screen-fixed", "keep the paper substrate screen-fixed")
    words(paper, ["wash_behavior"], "paper")

    source_files = seq(config.get("source_files"))
    need(bool(source_files), "authored animation source files required")
    for item in source_files:
        file_record(item, "authored source")
    source_references = seq(config.get("source_references"))
    need(bool(source_references), "at least one studied source passage required")
    for ref in source_references:
        ref = obj(ref)
        file_record(ref.get("evidence"), "private source-study evidence")
        words(ref, ["source_name", "observed_motion", "coverage", "limits"], "source study")
    shot_ids = {s.get("id") for s in shots}
    pose_records = {
        (obj(c).get("id"), obj(p).get("id")): obj(p)
        for c in seq(data.get("characters")) for p in seq(obj(c).get("poses"))
    }
    exposure_records, camera_records = {}, {}
    if extended:
        words(config, ["transition_selection_rationale"], "material selection")
    for shot in shots:
        sid = str(shot.get("id"))
        settings = obj(shot.get("living_ink"))
        drawing_fps = settings.get("drawing_fps")
        need(number(drawing_fps) and 8 <= drawing_fps <= 12, sid + ": drawing exposure must be 8–12 fps")
        need(drawing_fps == shot.get("pose_fps"), sid + ": drawing exposure differs from pose_fps")
        need(settings.get("ink_simulation_fps") == shot.get("simulation_fps"),
             sid + ": ink simulation cadence must be declared separately")
        need(settings.get("output_fps") == data.get("output_fps"),
             sid + ": output cadence must be declared separately")
        words(settings, ["ink_mass_change", "whole_pose_strategy", "negative_space"], sid)
        if extended:
            start, end = shot.get("start"), shot.get("end")
            def in_shot(item, label):
                a, b = obj(item).get("start"), obj(item).get("end")
                return need(number(a) and number(b) and number(start) and number(end)
                            and start <= a < b <= end, label + ": timing outside shot")
            declared = {(obj(c).get("id"), p) for c in seq(shot.get("characters"))
                        for p in seq(obj(c).get("poses"))}
            used_characters = {c for c, _ in declared}
            signatures = set()
            for key in declared:
                pose = pose_records.get(key)
                if not need(pose is not None, sid + ": missing drawing source for " + str(key)):
                    continue
                file_record(pose.get("image"), sid + ": counted whole drawing")
                roi = pose.get("roi_xywh")
                if roi is not None:
                    dims = pose.get("board_dimensions")
                    valid_roi = (isinstance(roi, list) and len(roi) == 4
                                 and all(isinstance(v, int) and not isinstance(v, bool) for v in roi)
                                 and roi[0] >= 0 and roi[1] >= 0 and roi[2] > 0 and roi[3] > 0
                                 and isinstance(dims, list) and len(dims) == 2
                                 and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in dims)
                                 and roi[0] + roi[2] <= dims[0] and roi[1] + roi[3] <= dims[1])
                    if not need(valid_roi, sid + ": counted drawing needs a valid bounded ROI"):
                        continue
                canonical_region = "full-image"
                if roi is not None and roi != [0, 0, *pose["board_dimensions"]]:
                    canonical_region = tuple(roi)
                signatures.add((obj(pose.get("image")).get("sha256"), canonical_region))
            budget = obj(settings.get("drawing_budget"))
            words(budget, ["purpose", "risk", "reuse_rationale"], sid + ": drawing budget")
            count = budget.get("unique_source_drawings")
            need(isinstance(count, int) and not isinstance(count, bool) and count == len(signatures),
                 sid + ": unique_source_drawings must equal distinct source hash/ROI count")
            exposures = seq(settings.get("exposure_plan"))
            need(bool(exposures) or not declared, sid + ": timed exposure plan required")
            covered, intervals = set(), {}
            for entry in exposures:
                entry = obj(entry)
                eid, cid = entry.get("id"), entry.get("character_id")
                need(text(eid) and eid not in exposure_records, sid + ": unique exposure ID required")
                exposure_records[eid] = (sid, entry)
                valid_time = in_shot(entry, sid + "/" + str(eid))
                pids, ticks = seq(entry.get("pose_ids")), seq(entry.get("exposure_ticks"))
                need(bool(pids) and all((cid, pid) in declared for pid in pids),
                     sid + "/" + str(eid) + ": exposure must use declared whole poses")
                covered.update((cid, pid) for pid in pids)
                exposure = entry.get("exposure")
                need(exposure in {"hold", "one-shot", "cycle"}, sid + ": explicit exposure mode required")
                words(entry, ["action"], sid + "/" + str(eid))
                ticks_ok = (len(ticks) == len(pids) and bool(ticks)
                            and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in ticks))
                need(ticks_ok, sid + "/" + str(eid) + ": positive exposure_ticks must match pose_ids")
                if exposure == "hold":
                    need(len(pids) == 1, sid + ": a hold must identify one drawing")
                    words(entry, ["hold_reason"], sid + "/" + str(eid))
                elif exposure == "cycle":
                    need(len(pids) >= 2, sid + ": a cycle needs its ordered drawing sequence")
                if ticks_ok and valid_time and number(drawing_fps) and drawing_fps > 0:
                    ticks_duration = sum(ticks) / drawing_fps
                    span = entry["end"] - entry["start"]
                    need(ticks_duration <= span + 1 / drawing_fps + 1e-6,
                         sid + "/" + str(eid) + ": exposure sequence exceeds its interval")
                    if exposure != "cycle" and span - ticks_duration > 1 / drawing_fps + 1e-6:
                        words(entry, ["hold_reason"], sid + "/" + str(eid) + ": final drawing hold")
                if valid_time:
                    intervals.setdefault(cid, []).append((entry["start"], entry["end"]))
            need(covered == declared, sid + ": every declared used pose must appear in the exposure plan")
            for cid, ranges in intervals.items():
                ordered = sorted(ranges)
                need(all(a[1] <= b[0] + 1e-6 for a, b in zip(ordered, ordered[1:])),
                     sid + "/" + str(cid) + ": overlapping whole-pose exposure intervals")
            cues = seq(settings.get("camera_cues"))
            need(bool(cues), sid + ": camera subject cues required")
            for cue in cues:
                cue = obj(cue)
                cue_id = cue.get("id")
                need(text(cue_id) and cue_id not in camera_records, sid + ": unique camera cue ID required")
                camera_records[cue_id] = (sid, cue)
                in_shot(cue, sid + "/" + str(cue_id))
                need(cue.get("subject_id") in used_characters | {"world"},
                     sid + ": camera subject must be an onscreen character or world")
                words(cue, ["framing", "angle", "movement", "story_reason"], sid + ": camera cue")
                spoken = normalize(cue.get("spoken_cue"))
                if spoken:
                    approved = normalize(obj(config.get("narration")).get("approved_text"))
                    need(bool(approved) and spoken.casefold() in approved.casefold(),
                         sid + ": camera spoken cue must occur in approved narration")
                else:
                    words(cue, ["visual_cue", "silent_beat_reason"], sid + ": visual camera cue")
        layers = seq(settings.get("layers"))
        need(len(layers) == 4 and {obj(l).get("role") for l in layers} == LAYER_ROLES,
             sid + ": exactly four separated paper/environment/subject/foreground layers required")
        for layer in layers:
            layer = obj(layer)
            role = layer.get("role")
            files = seq(layer.get("files"))
            need(bool(files) or text(layer.get("empty_reason")), sid + "/" + str(role) + ": asset or explicit empty reason required")
            for asset in files:
                file_record(asset, sid + "/" + str(role))
            if role == "paper":
                need(len(files) == 1 and obj(files[0]).get("sha256") == paper_hash,
                     sid + ": paper layer must use the same persistent paper")
            words(layer, ["motion_rule"], sid + "/" + str(role))

    narration = obj(config.get("narration"))
    mode = narration.get("mode")
    need(mode in {"existing-approved-take", "new-approved-take", "none"}, "explicit narration mode required")
    narration_audio = None
    transcript = ""
    if mode != "none":
        narration_audio = file_record(narration.get("audio"), "narration take")
        transcript_path = file_record(narration.get("transcript"), "narration transcript")
        if transcript_path:
            try:
                transcript = transcript_path.read_text()
            except UnicodeError:
                need(False, "narration transcript must be UTF-8 text")
        need(text(narration.get("approved_text")) and normalize(transcript) == normalize(narration.get("approved_text")),
             "transcript must preserve approved spoken wording")
        need(narration.get("approved_take_sha256") == obj(narration.get("audio")).get("sha256"),
             "narration take must match the approved audio hash")
        need(narration.get("preserve_wording") is True, "narration wording preservation required")
        words(narration, ["approval_record", "delivery", "processing"], "narration")
    else:
        words(narration, ["reason"], "no narration")
    required_words = config.get("required_words")
    need(isinstance(required_words, list) and all(text(w) for w in required_words),
         "declare required words explicitly, including [] when none")

    sound = obj(config.get("sound"))
    need(sound.get("method") in {"local-python", "supplied", "explicit-silence"}, "sound method must be declared")
    words(sound, ["direction"], "sound")
    events = seq(sound.get("events"))
    event_ids = set()
    for event in events:
        event = obj(event)
        eid = event.get("id")
        need(text(eid) and eid not in event_ids, "unique sound event ID required")
        event_ids.add(eid)
        time_range(event.get("start"), event.get("end"), "sound " + str(eid))
        need(event.get("kind") in {"tactile", "world-foley", "score"}, "sound event kind must describe its purpose")
        words(event, ["trigger", "description"], "sound " + str(eid))
    if sound.get("method") != "explicit-silence":
        need(bool(events), "planned material/foley/score events required")

    captions = obj(config.get("captions"))
    need(captions.get("mode") in {"ink-phrases", "none"}, "caption mode required")
    words(captions, ["readability_plan"], "captions")
    caption_text = []
    for caption in seq(captions.get("items")):
        caption = obj(caption)
        words(caption, ["id", "text", "placement", "readability"], "caption")
        time_range(caption.get("start"), caption.get("end"), "caption")
        need(caption.get("reveal") == "brush-matte", "caption reveal must use a brush matte")
        need(caption.get("accent_hex") in {None, accent.get("hex")}, "caption introduces a second accent")
        caption_text.append(str(caption.get("text", "")))
    if captions.get("mode") == "ink-phrases":
        need(bool(seq(captions.get("items"))), "ink-phrases mode needs caption items")
    else:
        need(not seq(captions.get("items")), "caption mode none conflicts with caption items")
    available_words = normalize(transcript + " " + " ".join(caption_text))
    for required in seq(required_words):
        need(text(required) and normalize(required).casefold() in available_words.casefold(),
             "required words missing from narration/captions: " + str(required))

    transitions = seq(config.get("transitions"))
    need(bool(transitions), "material transitions required")
    transition_ids = set()
    for transition in transitions:
        transition = obj(transition)
        tid = transition.get("id")
        need(text(tid) and tid not in transition_ids, "unique transition ID required")
        transition_ids.add(tid)
        need(transition.get("kind") in TRANSITIONS, str(tid) + ": unsupported transition")
        if extended:
            need(transition.get("classification") in {"major", "local"},
                 str(tid) + ": classify material event as major or local")
            words(transition, ["story_reason"], str(tid))
            if transition.get("kind") == "material-continuity":
                need(transition.get("classification") == "local",
                     str(tid) + ": material continuity must remain local")
        time_range(transition.get("start"), transition.get("end"), str(tid))
        need(transition.get("from_shot") is None or transition.get("from_shot") in shot_ids,
             str(tid) + ": unknown source shot")
        need(transition.get("to_shot") is None or transition.get("to_shot") in shot_ids,
             str(tid) + ": unknown destination shot")
        need(transition.get("from_shot") is not None or transition.get("to_shot") is not None,
             str(tid) + ": transition must belong to a shot")
        words(transition, ["material_cause", "onset", "propagation", "resolution"], str(tid))
        need(transition.get("preserves_paper") is True, str(tid) + ": transition must preserve substrate")
        if sound.get("method") != "explicit-silence":
            quiet_local = (extended and transition.get("classification") == "local"
                           and transition.get("sound_event") is None and text(transition.get("sound_reason")))
            need(transition.get("sound_event") in event_ids or quiet_local,
                 str(tid) + ": material sound event or explicit quiet-local reason missing")
    ordered_shots = sorted(shots, key=lambda s: s.get("start", 0))
    for left, right in zip(ordered_shots, ordered_shots[1:]):
        if left.get("end") == right.get("start"):
            boundary = left.get("end")
            need(any(obj(t).get("from_shot") == left.get("id") and obj(t).get("to_shot") == right.get("id")
                     and number(obj(t).get("start")) and number(obj(t).get("end"))
                     and t["start"] <= boundary <= t["end"] for t in transitions),
                 "missing organic transition or local material continuity at " + str(boundary))

    if stage != "proof":
        return errors
    review_path = file_record(obj(data.get("proof")).get("living_ink_review"), "completed AI visual review")
    if not review_path:
        return errors
    try:
        review = json.loads(review_path.read_text())
    except (ValueError, UnicodeError):
        need(False, "visual review must be UTF-8 JSON")
        return errors
    if not need(isinstance(review, dict), "visual review must be an object"):
        return errors
    need(review.get("schema") == 1, "review schema must be 1")
    need(review.get("plan_sha256") == plan_digest(data), "visual review is stale for this plan")
    need(review.get("verdict") == "pass", "AI visual review has not passed")
    reviewer = obj(review.get("reviewer"))
    need(reviewer.get("kind") == "ai", "AI visual reviewer identity required")
    words(reviewer, ["name", "model", "completed_at"], "reviewer")
    need(reviewer.get("inspection") == "actual-files-and-normal-playback", "actual file/playback inspection required")
    try:
        stamp = datetime.fromisoformat(str(reviewer.get("completed_at", "")).replace("Z", "+00:00"))
        need(stamp.tzinfo is not None, "review completion time must include its timezone")
    except ValueError:
        need(False, "valid review completion timestamp required")
    evidence = {}
    planned_clip_hashes = {
        obj(obj(s.get("proof")).get("clip")).get("sha256") for s in shots
    } - {None}
    for item in seq(review.get("evidence")):
        item = obj(item)
        eid = item.get("id")
        need(text(eid) and eid not in evidence, "unique review evidence ID required")
        evidence[eid] = item
        kind = item.get("kind")
        need(kind in EVIDENCE_KINDS, "unknown review evidence kind")
        file_record(item.get("file"), "review evidence " + str(eid))
        if kind == "rendered-frame":
            need(number(item.get("time")) and number(duration) and 0 <= item["time"] <= duration,
                 "rendered-frame evidence needs an actual film time")
        if kind == "clip":
            time_range(item.get("start"), item.get("end"), "reviewed clip")
            need(item.get("playback_rate") == 1, "review must include normal-speed playback")
            need(item.get("watched_complete") is True, "reviewed clip playback must be completed")
            need(obj(item.get("file")).get("sha256") in planned_clip_hashes,
                 "reviewed clip differs from current shot proof")
    kinds = {e.get("kind") for e in evidence.values()}
    for kind in {"script", "source-reference", "rendered-frame", "clip"}:
        need(kind in kinds, "review did not inspect " + kind)
    need(any(e.get("kind") == "script" and obj(e.get("file")).get("sha256") == obj(story.get("script")).get("sha256")
             for e in evidence.values()), "review script differs from the approved plan script")
    studied_hashes = {obj(obj(r).get("evidence")).get("sha256") for r in source_references} - {None}
    for studied_hash in studied_hashes:
        need(any(e.get("kind") == "source-reference" and obj(e.get("file")).get("sha256") == studied_hash
                 for e in evidence.values()), "review must inspect every declared source-study evidence file")
    for item in evidence.values():
        if item.get("kind") == "rendered-frame":
            need(any(e.get("kind") == "clip"
                     and obj(e.get("file")).get("sha256") == item.get("clip_sha256")
                     and number(e.get("start")) and number(e.get("end")) and number(item.get("time"))
                     and e["start"] <= item["time"] <= e["end"] for e in evidence.values()),
                 "rendered-frame must identify its reviewed clip and valid capture time")
    for char in seq(data.get("characters")):
        char = obj(char)
        need(any(e.get("kind") == "character-master" and obj(e.get("file")).get("sha256") == obj(char.get("master")).get("sha256")
                 for e in evidence.values()), "review missing actual character master: " + str(char.get("id")))
        for pose in seq(char.get("poses")):
            need(any(e.get("kind") == "whole-pose" and obj(e.get("file")).get("sha256") == obj(obj(pose).get("image")).get("sha256")
                     for e in evidence.values()), "review missing actual whole pose: " + str(obj(pose).get("id")))
    if narration_audio:
        need(any(e.get("kind") == "audio" and obj(e.get("file")).get("sha256") == obj(narration.get("audio")).get("sha256")
                 for e in evidence.values()), "review missing the actual narration take")
    for shot in shots:
        start, end = shot.get("start"), shot.get("end")
        if number(start) and number(end):
            need(any(e.get("kind") == "clip" and number(e.get("start")) and number(e.get("end"))
                     and e["start"] <= start and e["end"] >= end for e in evidence.values()),
                 str(shot.get("id")) + ": no complete normal-speed clip review")
    observations = seq(review.get("observations"))
    areas = {obj(o).get("area") for o in observations}
    need(REVIEW_AREAS <= areas, "review must cover story, identity, ink motion, paper, anatomy/contact, transition, caption and audio")
    if extended:
        need({"performance-exposure", "camera-story-focus"} <= areas,
             "review must inspect performance exposures and story-linked camera focus")
    for observation in observations:
        observation = obj(observation)
        words(observation, ["finding"], "visual observation")
        refs = seq(observation.get("evidence_ids"))
        need(bool(refs) and all(r in evidence for r in refs), "observation must cite inspected evidence")
        result = observation.get("result")
        need(result in {"pass", "not-applicable"}, "each observation needs an explicit completed result")
        if result == "not-applicable":
            area = observation.get("area")
            allowed = (
                (area in {"anatomy-contact", "performance-exposure"} and data.get("character_free") is True)
                or (area == "caption-readability" and captions.get("mode") == "none")
                or (area == "audio-narration" and mode == "none" and sound.get("method") == "explicit-silence")
            )
            need(allowed, "required inspection cannot be marked not-applicable")
    # Temporal review must cite actual different frames, not an attractive single still.
    for area in {"living-ink-motion", "transition-material", "anatomy-contact"}:
        matching = [obj(o) for o in observations if obj(o).get("area") == area]
        refs = {r for o in matching for r in seq(o.get("evidence_ids"))}
        times = {evidence[r].get("time") for r in refs if r in evidence and evidence[r].get("kind") == "rendered-frame"}
        need(len(times) >= 2, area + ": at least two distinct rendered-frame times required")
        need(any(r in evidence and evidence[r].get("kind") == "clip" for r in refs),
             area + ": normal playback evidence required")
    for transition in transitions:
        transition = obj(transition)
        tid = transition.get("id")
        matching = [obj(o) for o in observations if obj(o).get("area") == "transition-material"
                    and tid in seq(obj(o).get("transition_ids"))]
        refs = {r for o in matching for r in seq(o.get("evidence_ids"))}
        start, end = transition.get("start"), transition.get("end")
        times = {
            evidence[r]["time"] for r in refs
            if r in evidence and evidence[r].get("kind") == "rendered-frame"
            and number(evidence[r].get("time")) and number(start) and number(end)
            and start <= evidence[r]["time"] <= end
        }
        need(len(times) >= 2, str(tid) + ": transition needs observed distinct onset/progression frames")
    if extended:
        # Binding IDs and actual intervals prevents a generic review paragraph
        # from silently standing in for inspection of all new acting/camera cues.
        for area, records, key in [
            ("performance-exposure", exposure_records, "exposure_ids"),
            ("camera-story-focus", camera_records, "camera_cue_ids"),
        ]:
            for rid, (sid, planned) in records.items():
                matching = [obj(o) for o in observations if obj(o).get("area") == area
                            and obj(o).get("shot_id") == sid and rid in seq(obj(o).get(key))]
                refs = {r for o in matching for r in seq(o.get("evidence_ids"))}
                a, b = planned.get("start"), planned.get("end")
                times = {evidence[r]["time"] for r in refs if r in evidence
                         and evidence[r].get("kind") == "rendered-frame"
                         and number(evidence[r].get("time")) and number(a) and number(b)
                         and a <= evidence[r]["time"] <= b}
                need(len(times) >= 2, str(rid) + ": needs two observed frames inside its interval")
                need(any(r in evidence and evidence[r].get("kind") == "clip"
                         and number(evidence[r].get("start")) and number(evidence[r].get("end"))
                         and number(a) and number(b)
                         and evidence[r]["start"] <= a and evidence[r]["end"] >= b for r in refs),
                     str(rid) + ": needs complete normal playback evidence")
    issues = review.get("issues")
    need(isinstance(issues, list), "review must explicitly record issues, including []")
    for issue in seq(issues):
        issue = obj(issue)
        words(issue, ["description"], "review issue")
        need(issue.get("severity") in {"blocking", "minor"}, "issue severity required")
        need(issue.get("status") in {"open", "resolved"}, "issue status required")
        need(not (issue.get("severity") == "blocking" and issue.get("status") != "resolved"),
             "unresolved blocking review issue: " + str(issue.get("description")))
        if issue.get("status") == "resolved":
            words(issue, ["resolution"], "resolved issue")
            refs = seq(issue.get("evidence_ids"))
            need(bool(refs) and all(r in evidence for r in refs), "resolved issue needs current evidence")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--stage", choices=["assets", "proof"], default="assets")
    parser.add_argument("--digest", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.plan.read_text())
        if args.digest:
            print(plan_digest(data))
            return
        from validate_shot_plan import validate as validate_all
        errors = validate_all(data, args.plan.resolve().parent, args.stage)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        parser.exit(2, "Invalid plan/review: " + str(exc) + "\n")
    print(json.dumps({
        "ok": not errors, "stage": args.stage, "errors": errors,
        "limit": "Checks evidence/provenance only. It cannot see, listen, approve or certify visual truth."
    }, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
