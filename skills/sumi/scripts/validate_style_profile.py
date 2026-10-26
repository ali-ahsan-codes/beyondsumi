#!/usr/bin/env python3
"""Evidence checks for three-style plans. Current on-twos and explicit historical profile evidence checks.

This records source budgets and reviews; it does not inspect pixels, generate an
AI review, certify animation or grant production approval.
"""
import hashlib
import math
import re
from pathlib import Path

from plan_provenance import plan_digest
from motion_detail import smooth_24
from sumi_catalog import STYLES, uses_current_catalog

LIGHT_PALETTE = {
    "paper": "#F3EFE6", "carbon": "#111114", "diluted": "#5A5D64",
    "cinnabar": "#D3381C", "indigo": "#1D3B58", "gold": "#C89B3C",
    "jade": "#2E6F5E", "peony": "#C94A6A",
}
DARK_PALETTE = {"paper": "#FFFFFF", "carbon": "#111111", "diluted": "#5C5C5C"}
DARK_RED = "#7A1622"
DEPTH_Z = [-500, -150, 0, 150]


def is_dark_red(value):
    if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return False
    red, green, blue = (int(value[i:i+2], 16) for i in (1, 3, 5))
    return 64 <= red <= 180 and red >= 1.6 * green and red >= 1.6 * blue


def valid_dark_palette(palette):
    if not isinstance(palette, dict) or not all(palette.get(k) == v for k, v in DARK_PALETTE.items()):
        return False
    for key, value in palette.items():
        if key == "dark_red":
            if not is_dark_red(value): return False
        elif not (isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", value)
                  and value[1:3].lower() == value[3:5].lower() == value[5:7].lower()):
            return False
    return True


def validate(data, root, stage="assets"):
    if not uses_current_catalog(data):
        return []
    root, errors = Path(root).resolve(), []

    def need(ok, message):
        if not ok:
            errors.append("Style profile: " + message)
        return bool(ok)

    def obj(value):
        return value if isinstance(value, dict) else {}

    def seq(value):
        return value if isinstance(value, list) else []

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def num(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    def words(record, fields, label):
        for key in fields:
            need(text(obj(record).get(key)), label + ": missing " + key)

    def file(record, label):
        record = obj(record)
        if not need(text(record.get("path")), label + ": file record required"):
            return None
        path = (root / record["path"]).resolve()
        if not need(root in path.parents and path.is_file() and path.stat().st_size > 0,
                    label + ": missing, empty or outside-project file"):
            return None
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        need(record.get("sha256") == digest, label + ": missing or stale hash")
        return digest

    def region(record, label):
        record = obj(record)
        digest = file(record.get("file", record.get("image")), label)
        roi, dims = record.get("roi_xywh"), record.get("board_dimensions")
        if roi is None:
            return (digest, "full-image") if digest else None
        valid = (isinstance(roi, list) and len(roi) == 4
                 and all(isinstance(v, int) and not isinstance(v, bool) for v in roi)
                 and roi[0] >= 0 and roi[1] >= 0 and roi[2] > 0 and roi[3] > 0
                 and isinstance(dims, list) and len(dims) == 2
                 and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in dims)
                 and roi[0] + roi[2] <= dims[0] and roi[1] + roi[3] <= dims[1])
        if not need(valid, label + ": invalid source region"):
            return None
        return (digest, "full-image" if roi == [0, 0, *dims] else tuple(roi)) if digest else None

    smooth = smooth_24(data)
    config = obj(data.get("style_profile"))
    need(config.get("schema") == 1, "style_profile.schema must be 1")
    need(config.get("status") == "authored_spec_only",
         "configuration status describes an authored specification, not a generated approval")
    story = obj(config.get("story"))
    script_hash = file(story.get("script"), "approved script")
    words(story, ["analysis"], "story")
    need(bool(seq(story.get("required_visual_actions"))), "declare required visual actions")
    approved_text = story.get("approved_text", "")
    sources = seq(config.get("source_files"))
    need(bool(sources), "authored source files required")
    source_hashes = {file(source, "authored source") for source in sources}
    source_hashes.add(script_hash)
    source_hashes.discard(None)
    narration = obj(config.get("narration"))
    need(narration.get("mode") in {"existing-approved-take", "new-approved-take", "none"},
         "declare narration mode")
    if narration.get("mode") != "none":
        words(narration, ["approval_record"], "narration")
        need(text(approved_text), "preserve the exact approved narration wording")
        approved_hash = file(narration.get("approved_take"), "approved narration")
        used_hash = file(narration.get("used_take"), "used narration source")
        need(approved_hash is not None and used_hash == approved_hash,
             "used narration source must match the approved take")
        need(narration.get("preserve_wording") is True, "approved wording must be preserved")
        if script_hash:
            try:
                script_text = (root / story["script"]["path"]).read_text(encoding="utf-8")
                need(" ".join(script_text.split()) == " ".join(approved_text.split()),
                     "approved narration text must match the hashed script")
            except (OSError, UnicodeError):
                need(False, "approved script must be readable UTF-8 text")
    poses = {(obj(c).get("id"), obj(p).get("id")): obj(p)
             for c in seq(data.get("characters")) for p in seq(obj(c).get("poses"))}
    for shot in seq(data.get("shots")):
        shot = obj(shot)
        style, sid = shot.get("style"), str(shot.get("id"))
        if style not in STYLES:
            continue
        settings = obj(shot.get("style_profile"))
        legacy_brush = config.get("profile") == "brush-ink-v1" and data.get("release_version") == "4.0.0"
        expected = "brush-ink-v1" if legacy_brush else STYLES[style]["profile"]
        need(config.get("profile") == expected,
             sid + ": wrong technical profile")
        need(config.get("style") == style,
             sid + ": profile style differs from shot")
        words(settings, ["profile_observation"], sid)
        release_match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(data.get("release_version", "")))
        rate_original = (style == "sumi-original" and release_match is not None
                         and tuple(map(int, release_match.groups())) >= (4, 5, 1))
        living_original = (rate_original and tuple(map(int, release_match.groups())) >= (4, 6, 1))
        adaptive_original = (rate_original and tuple(map(int, release_match.groups())) >= (4, 6, 0))
        if data.get("release_version") != "4.0.0":
            current_original = (rate_original and tuple(map(int, release_match.groups())) >= (4, 5, 3))
            target_fps, target_pose = ((30, 15) if current_original else (28, 14)) if rate_original else (24, 12)
            if adaptive_original:
                target_fps, target_pose = 30, (20 if living_original else 30)
            if smooth:
                target_pose = 24
            need(data.get("output_fps") == target_fps and shot.get("pose_fps") == target_pose and shot.get("simulation_fps") == target_fps,
                 sid + f": new film requires {target_fps}fps output with {target_pose}fps character poses")
            need(obj(settings.get("cadence")).get("exposure_frames") == (1 if adaptive_original or smooth else 2),
                 sid + ": exposure unit differs from the selected version/style")
            if rate_original:
                need(obj(settings.get("cadence")).get("character_update_fps") == target_pose
                     and obj(settings.get("cadence")).get("output_fps") == target_fps,
                     sid + f": Original character evaluation clock must be {target_pose}Hz at {target_fps}fps; this is not a new-drawing rate")
        if style == "sumi-original":
            release = str(data.get("release_version", ""))
            match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", release)
            if living_original:
                from validate_living_frames import validate_original_states
                errors.extend(validate_original_states(shot, root, state_fps=24 if smooth else 20, whole_drawings_only=smooth))
            elif adaptive_original:
                drawing = obj(settings.get("original_drawings"))
                label = sid + ": Original variable exposures"
                need(drawing.get("budget_mode") == "action-driven", label + " requires action-driven source budget")
                need(obj(settings.get("cadence")).get("exposure_policy") == "variable", label + " requires variable exposure policy")
                need(text(drawing.get("sequence_id")), label + " needs an action sequence ID")
                sources = {}
                for row in seq(drawing.get("source_images")):
                    row = obj(row); source_id = row.get("id")
                    need(text(source_id) and source_id not in sources, label + " needs unique source IDs")
                    identity = region(row, label)
                    if text(source_id): sources[source_id] = identity
                a, b = shot.get("start"), shot.get("end")
                valid_span = num(a) and num(b) and 0 <= a < b
                need(valid_span, label + " needs actual shot timing")
                if valid_span:
                    first, last = round(a * 30), round(b * 30); cursor = first
                    entries = seq(drawing.get("exposure_plan"))
                    for entry in entries:
                        entry = obj(entry); start, end = entry.get("start_frame"), entry.get("end_frame")
                        correct = (isinstance(start, int) and not isinstance(start, bool)
                                   and isinstance(end, int) and not isinstance(end, bool)
                                   and start == cursor and first <= start < end <= last)
                        need(correct, label + " needs contiguous bounded whole-frame exposures")
                        need(sources.get(entry.get("source_id")) is not None, label + " exposure uses missing/unusable source")
                        need(text(entry.get("action")), label + " needs the actual action/derived-motion description")
                        if entry.get("driver", "hold") == "hold":
                            need(text(entry.get("hold_reason")), label + " held drawing needs its reason")
                        if isinstance(end, int) and not isinstance(end, bool): cursor = end
                    need(bool(entries) and cursor == last, label + " exposure coverage is incomplete")
            elif rate_original:
                drawing = obj(settings.get("original_drawings"))
                label = sid + ": Original drawing rate"
                need(drawing.get("minimum_drawings_per_second") == target_pose,
                     label + f" requires {target_pose} drawings per second, not per scene")
                if drawing.get("deliberate_stillness") is True:
                    need(text(drawing.get("stillness_reason")), label + " needs a deliberate-stillness reason")
                else:
                    need(text(drawing.get("sequence_id")), label + " needs an action sequence ID")
                    rows = seq(drawing.get("source_images"))
                    sources = {}
                    for row in rows:
                        row = obj(row)
                        source_id = row.get("id")
                        need(text(source_id) and source_id not in sources, label + " needs unique source IDs")
                        identity = region(row, label)
                        if text(source_id): sources[source_id] = identity
                    entries = seq(drawing.get("exposure_plan"))
                    a, b = shot.get("start"), shot.get("end")
                    valid_span = num(a) and num(b) and 0 <= a < b
                    need(valid_span, label + " needs actual shot timing")
                    if valid_span:
                        first, last = round(a * target_fps), round(b * target_fps)
                        cursor, identities = first, []
                        for entry in entries:
                            entry = obj(entry)
                            start, end = entry.get("start_frame"), entry.get("end_frame")
                            correct = (isinstance(start, int) and not isinstance(start, bool)
                                       and isinstance(end, int) and not isinstance(end, bool)
                                       and start == cursor and end == min(start + 2, last) and start < last)
                            need(correct, label + " needs contiguous two-frame drawings through the shot")
                            identity = sources.get(entry.get("source_id"))
                            need(identity is not None, label + " exposure uses missing/unusable drawing")
                            identities.append(identity)
                            if isinstance(end, int): cursor = end
                        need(bool(entries) and cursor == last, label + " exposure coverage is incomplete")
                        # Each rate-specific sliding state window is one animated second on twos.
                        # Checked complete cycles may repeat; a held/aliased pose is not a new drawing.
                        window = min(target_pose, max(1, math.ceil((last - first) / 2)))
                        for i in range(max(0, len(identities) - window + 1)):
                            group = identities[i:i + window]
                            need(None not in group and len(set(group)) == window,
                                 label + f" needs {target_pose} distinct drawings in each animated second (scaled for a short shot)")
            elif match and tuple(map(int, match.groups())) >= (4, 5, 0):
                drawing = obj(settings.get("original_drawings"))
                label = sid + ": Original drawing plan"
                need(drawing.get("minimum_distinct_drawings") == 14,
                     label + " requires minimum 14 distinct drawings per animated scene/connected action")
                if drawing.get("deliberate_stillness") is True:
                    need(text(drawing.get("stillness_reason")),
                         label + " needs a meaningful deliberate-stillness reason")
                else:
                    need(text(drawing.get("sequence_id")), label + " needs a connected-action sequence ID")
                    rows = seq(drawing.get("source_images"))
                    identities = {region(row, label) for row in rows}
                    identities.discard(None)
                    need(len(identities) >= 14, label + " has fewer than 14 distinct source hash/regions")
                    need(bool(seq(drawing.get("exposure_plan"))), label + " needs its actual sequence exposure plan")
            preservation = obj(config.get("original_preservation"))
            need(preservation.get("baseline_name") == "The Last Blossom",
                 sid + ": name the preserved Original source")
            need(preservation.get("baseline_revision") == "earlier-56-second-recovered-source",
                 sid + ": preserve the earlier Original baseline; the later 60-second revision is separate")
            baseline = seq(preservation.get("baseline_sources"))
            need(bool(baseline), sid + ": actual Original baseline sources required")
            for item in baseline:
                file(item, sid + ": Original baseline")
            words(preservation, ["baseline_revision", "baseline_observation",
                                 "source_simulation_notes", "export_choice_reason"], sid + ": preservation")
            need(bool(seq(preservation.get("preserved_features"))), sid + ": record preserved features")
            need(isinstance(preservation.get("intentional_changes"), list),
                 sid + ": record intentional changes, including an empty list if none")
            need(preservation.get("source_cadence") == "requestAnimationFrame with elapsed wall-clock time",
                 sid + ": preserve the source time model; it has no encoded fps baseline")
            need(preservation.get("export_fps_is_new_choice") is True,
                 sid + ": an encoded export fps is a new project choice")
        else:
            profile = obj(config.get("brush_ink"))
            cadence = ({"output_fps":60,"character_update_fps":12,"edge_boil_fps":8} if legacy_brush else
                       {"output_fps":24,"character_update_fps":12,"edge_boil_fps":12,"exposure_frames":2})
            if smooth and not legacy_brush:
                cadence.update(character_update_fps=24, exposure_frames=1, exposure_policy="24-in-24")
                from validate_living_frames import validate_original_states
                errors.extend(validate_original_states(shot, root, state_fps=24, output_fps=24,
                    source_key="motion_drawings", whole_drawings_only=True))
            need(data.get("output_fps") == cadence["output_fps"], sid + ": output clock differs from selected profile")
            need(obj(profile.get("cadence")) == cadence, sid + ": declared cadence differs from selected profile")
            need(obj(settings.get("cadence")) == cadence, sid + ": shot cadence differs from profile")
            need(shot.get("pose_fps") == (24 if smooth else 12) and shot.get("simulation_fps") == cadence["output_fps"],
                 sid + ": character and material clocks differ from profile")
            need(profile.get("depth_z") == DEPTH_Z, sid + ": declare four stage depth planes")
            policy = obj(profile.get("budget"))
            if legacy_brush:
                need(policy.get("max_source_images_per_shot") == 4 and policy.get("max_character_extreme_poses") == 2,
                     sid + ": historical v1 budget differs")
            else:
                need(policy.get("mode") == "shot-specific", sid + ": plan a shot-specific drawing allowance")
            need(policy.get("count_by") == "distinct-source-hash-and-pose-region",
                 sid + ": count source drawings/regions rather than atlas files")
            palette = obj(profile.get("palette"))
            if style == "sumi-light":
                need(palette == LIGHT_PALETTE, sid + ": Light must declare its mineral palette")
            else:
                need(all(palette.get(k) == v for k, v in DARK_PALETTE.items()),
                     sid + ": Dark paper/carbon/diluted palette mismatch")
                need(valid_dark_palette(palette),
                     sid + ": Dark requires a neutral base; only named dark_red may contain muted red")
            source_images = seq(settings.get("source_images"))
            source_ids = [obj(image).get("id") for image in source_images]
            need(all(text(sid) for sid in source_ids) and len(source_ids) == len(set(source_ids)),
                 sid + ": source image IDs must be unique")
            identities = {region(image, sid + ": visual source") for image in source_images}
            identities.discard(None)
            if smooth:
                drawn = {region(row, sid + ": smoother pose source")
                         for row in seq(obj(settings.get("motion_drawings")).get("source_images"))}
                need(None not in drawn and drawn.issubset(identities),
                     sid + ": smoother pose art must be included in the normal hashed source inventory and image budget")
            if legacy_brush:
                need(len(identities) <= 4, sid + ": historical source image budget exceeded")
            if not identities:
                words(settings, ["procedural_only_reason"], sid + ": no static source artwork")
            used = {(obj(c).get("id"), pid) for c in seq(shot.get("characters"))
                    for pid in seq(obj(c).get("poses"))}
            extremes = {region(poses[key], sid + ": character extreme")
                        for key in used if key in poses}
            extremes.discard(None)
            need(extremes.issubset(identities), sid + ": every used character drawing must count as a source")
            if legacy_brush:
                need(len(extremes) <= 2, sid + ": historical extreme-pose budget exceeded")
            budget = obj(settings.get("budget"))
            if not legacy_brush:
                for key, count in [("planned_source_images",len(identities)),("planned_character_extremes",len(extremes))]:
                    allowed=budget.get(key)
                    need(isinstance(allowed,int) and not isinstance(allowed,bool) and allowed >= count,
                         sid + ": actual sources exceed or lack the declared " + key)
            need(budget.get("unique_source_images") == len(identities)
                 and budget.get("unique_character_extremes") == len(extremes),
                 sid + ": declared source/character counts differ from actual hash/region identities")
            words(budget, ["reuse_rationale", "action_plan"], sid + ": budget")
            layers = seq(settings.get("layers"))
            need(len(layers) == 4 and {obj(layer).get("z") for layer in layers} == set(DEPTH_Z),
                 sid + ": map the four separated layers to their depth planes")
            for layer in layers:
                words(layer, ["role", "motion_rule"], sid + ": layer")
                need(bool(seq(obj(layer).get("source_ids"))) or text(obj(layer).get("empty_reason")),
                     sid + ": each layer needs source IDs or an explicit empty reason")
                need(all(value in source_ids for value in seq(obj(layer).get("source_ids"))),
                     sid + ": layer uses an undeclared source image")
            def within_shot(entry, label):
                a, b = obj(entry).get("start"), obj(entry).get("end")
                start, end = shot.get("start"), shot.get("end")
                return need(num(a) and num(b) and num(start) and num(end) and start <= a < b <= end,
                            sid + ": " + label + " is outside the shot")
            exposures = seq(settings.get("exposure_plan"))
            need(bool(exposures), sid + ": source images need an authored exposure/movement plan")
            for entry in exposures:
                entry = obj(entry)
                within_shot(entry, "exposure")
                need(entry.get("driver") in {"hold", "articulated", "warp", "replacement", "procedural"},
                     sid + ": name the actual source-animation driver")
                if entry.get("driver") == "procedural":
                    recipes = seq(entry.get("recipe_sources"))
                    need(bool(recipes), sid + ": procedural exposure needs actual hashed recipe sources")
                    for recipe in recipes:
                        digest = file(recipe, sid + ": procedural exposure recipe")
                        need(digest is not None and digest in source_hashes,
                             sid + ": procedural recipe must occur in the authored source inventory")
                else:
                    need(entry.get("source_id") in source_ids, sid + ": exposure uses an undeclared source")
                words(entry, ["action", "support_contact"], sid + ": exposure")
                if entry.get("driver") == "hold":
                    words(entry, ["hold_reason"], sid + ": exposure hold")
            cues = seq(settings.get("camera_cues"))
            need(bool(cues), sid + ": narration-linked camera direction is required")
            character_ids = {obj(c).get("id") for c in seq(shot.get("characters"))}
            for cue in cues:
                cue = obj(cue)
                within_shot(cue, "camera cue")
                need(cue.get("subject_id") in character_ids | {"world"},
                     sid + ": camera subject must be an onscreen character or world")
                words(cue, ["framing", "angle", "movement", "story_reason"], sid + ": camera cue")
                spoken = " ".join(str(cue.get("spoken_cue", "")).split())
                if spoken:
                    need(spoken.casefold() in " ".join(approved_text.split()).casefold(),
                         sid + ": camera spoken cue differs from approved wording")
                else:
                    words(cue, ["visual_cue", "silent_beat_reason"], sid + ": camera cue")
            for effect in ["smear", "impact", "whip"]:
                choice = obj(obj(settings.get("effects")).get(effect))
                need(choice.get("status") in {"used", "omitted"}, sid + ": choose or omit " + effect)
                words(choice, ["story_reason"], sid + ": " + effect)
        if stage == "proof":
            review = obj(settings.get("review"))
            need(review.get("status") == "passed", sid + ": actual review is pending")
            words(obj(review.get("reviewer")), ["id", "kind"], sid + ": reviewer")
            need(review.get("plan_sha256") == plan_digest(data), sid + ": review plan hash is missing/stale")
            inspected = seq(review.get("inspected_sources"))
            inspected_hashes = {file(item, sid + ": inspected source") for item in inspected}
            required_hashes = source_hashes | {
                obj(asset).get("sha256") for asset in seq(shot.get("assets"))
            }
            required_hashes |= {
                obj(obj(image).get("file")).get("sha256")
                for image in seq(settings.get("source_images"))
            }
            required_hashes |= {
                obj(poses.get((obj(c).get("id"), pid), {}).get("image")).get("sha256")
                for c in seq(shot.get("characters")) for pid in seq(obj(c).get("poses"))
            }
            used_character_ids = {obj(c).get("id") for c in seq(shot.get("characters"))}
            required_hashes |= {
                obj(obj(c).get("master")).get("sha256")
                for c in seq(data.get("characters")) if obj(c).get("id") in used_character_ids
            }
            required_hashes.discard(None)
            need(required_hashes.issubset(inspected_hashes),
                 sid + ": reviewer must inspect current source files, artwork and used character masters")
            clip_hash = file(review.get("normal_speed_clip"), sid + ": reviewed normal-speed clip")
            need(clip_hash is not None and clip_hash == obj(obj(shot.get("proof")).get("clip")).get("sha256"),
                 sid + ": review must bind to the shot proof clip")
            need(review.get("normal_speed") is True, sid + ": normal-speed review not performed")
            frames = seq(review.get("adjacent_frames"))
            need(len(frames) >= 2, sid + ": actual adjacent-frame evidence required")
            for frame in frames:
                file(frame, sid + ": adjacent frame")
                need(obj(frame).get("clip_sha256") == clip_hash, sid + ": frame must bind to the reviewed clip")
            if len(frames) >= 2:
                times = [obj(frame).get("time") for frame in frames]
                need(all(num(t) for t in times), sid + ": adjacent-frame times required")
                if all(num(t) for t in times) and num(data.get("output_fps")) and data["output_fps"] > 0:
                    need(any(abs(b - a - 1 / data["output_fps"]) < 1e-6
                             for a, b in zip(times, times[1:])),
                         sid + ": review needs actual consecutive output frames")
            words(review, ["observation", "budget_observation", "palette_observation",
                           "acting_contact_observation", "camera_observation"], sid + ": actual review")
            need(review.get("unresolved") == [], sid + ": unresolved issues or missing issue list")
    return errors
