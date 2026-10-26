#!/usr/bin/env python3
"""Create a three-style Sumi project. Never overwrite, install or approve silently."""
import argparse
import json
import math
import re
import shutil
from pathlib import Path
from urllib.parse import unquote

from sumi_catalog import VERSION, PLAN_COMPATIBILITY_VERSION, CATALOG_ID, STYLES, LEGACY_METHODS
from validate_style_profile import LIGHT_PALETTE, DARK_PALETTE, DARK_RED


def copy_guides(skill, destination, entrypoints):
    """Preserve the relative tree for local Markdown dependencies; no downloads."""
    guide_root = destination / "sumi-guide"
    pending = [skill / name for name in entrypoints]
    copied = set()
    while pending:
        source = pending.pop().resolve()
        if source in copied:
            continue
        if skill not in source.parents or not source.exists():
            raise OSError(f"Missing or outside-bundle guide dependency: {source}")
        copied.add(source)
        target = guide_root / source.relative_to(skill)
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "node_modules", ".DS_Store"))
            if source.parent == skill / "assets" and source.name != "delivery-dashboard" and (source / "index.html").exists():
                pending.append(skill / "assets/delivery-dashboard")
            continue
        shutil.copy2(source, target)
        if source.suffix.lower() == ".md":
            for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                link = unquote(raw.strip("<>").split("#", 1)[0])
                if not link or re.match(r"[A-Za-z][\w+.-]*:", link):
                    continue
                dependency = (source.parent / link).resolve()
                # HTML examples need their adjacent scripts/styles/images as well.
                pending.append(dependency.parent if dependency.suffix.lower() == ".html" else dependency)
    return guide_root


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("destination", type=Path)
    p.add_argument("--style", choices=list(STYLES),
                   help="Current style: Sumi Original, Sumi Light or Sumi Dark.")
    p.add_argument("--legacy-method", "--method", "--variation", dest="legacy_method",
                   choices=list(LEGACY_METHODS),
                   help=argparse.SUPPRESS)
    p.add_argument("--aspect", choices=["16:9", "9:16", "1:1"], default="16:9")
    p.add_argument("--seconds", type=float, default=10)
    p.add_argument("--fps", type=int,
                   help="Original defaults to30fps/20 designed character states; Light/Dark to 24fps/12 paired states. Historical sources are preserved.")
    p.add_argument("--title", default="Production canvas")
    a = p.parse_args()
    if a.style and a.legacy_method:
        p.error("Choose a current style or explicit historical compatibility, not both.")
    chosen = a.style or ("sumi-original" if not a.legacy_method else None)
    if not math.isfinite(a.seconds) or not 0 < a.seconds <= 3600:
        p.error("seconds must be finite and between 0 and 3600")
    fps = a.fps if a.fps is not None else (STYLES[chosen]["default_output_fps"] if chosen else 30)
    if fps is None:
        p.error("Sumi Original has no fixed encoded-fps baseline. Supply --fps for this project's export and record the reason in its preservation plan.")
    if chosen and fps != STYLES[chosen]["default_output_fps"]:
        p.error("New Original uses30fps/20 designed character states; Light/Dark use 24fps with paired character states.")
    if not 1 <= fps <= 120 or round(a.seconds * fps) < 1:
        p.error("fps must be 1–120 and duration must contain a frame")
    skill = Path(__file__).resolve().parents[1]
    src = skill / "assets/remotion-starter"
    dest = a.destination.expanduser().absolute()
    if dest.exists() or dest.is_symlink():
        p.error("Destination already exists; choose a new folder.")
    helpers = ["validate_shot_plan.py", "validate_living_ink.py", "validate_style_profile.py",
               "plan_provenance.py", "sumi_catalog.py", "validate_physics.py", "build_delivery.py", "living_frames.py", "validate_living_frames.py", "environment_motion.py", "validate_environment_plan.py", "make_motion_preview.py", "validate_title_timing.py"]
    required = [src / "package-lock.json", src / "src/index.tsx",
                skill / "assets/procedural-audio/render_audio.py",
                skill / "assets/motion-core/motion-core.mjs",
                skill / "assets/templates/style-profile.json",
                skill / "assets/templates/shot-style-profile.json"]
    required += [skill / "scripts" / name for name in helpers]
    if chosen:
        required += [skill / f"references/styles/{chosen}.md", skill / "references/style-profile-schema.md"]
    if chosen in {"sumi-light", "sumi-dark"}:
        required += [skill / "references/brush-ink-workflow.md",
                     skill / "assets/templates/BRUSH-INK-SHOT.md"]
    for path in required:
        if not path.is_file():
            p.error(f"Incomplete bundle: missing {path}")
    try:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".DS_Store"))
        shutil.copytree(skill / "assets/procedural-audio", dest / "audio-tools",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(skill / "assets/sound-library", dest / "sound-tools",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "bundled-bank"))
        (dest / "sound-tools/library-location.json").write_text(json.dumps({
            "bundled_music_root": str(skill / "assets/sound-library/bundled-bank"),
            "effect_cache": "User-selected external library; do not copy or distribute it automatically."
        }, indent=2)+"\n")
        shutil.copytree(skill / "assets/motion-core", dest / "motion-tools")
        shutil.copytree(skill / "assets/delivery-dashboard", dest / "assets/delivery-dashboard",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        page=dest / "index.html"
        page.write_text(page.read_text().replace("../delivery-dashboard/", "assets/delivery-dashboard/"))
        shutil.copy2(skill / "assets/templates/VOICE-MAP.json", dest / "VOICE-MAP.json")
        for name in helpers:
            shutil.copy2(skill / "scripts" / name, dest / "scripts" / name)
        plan = json.loads((skill / "assets/templates/shot-plan.json").read_text())
        plan.update(title=a.title, duration=a.seconds, output_fps=fps)
        shot = plan["shots"][0]
        shot.update(end=a.seconds, performance="", camera="", transition="", strict_identity="", economy="")
        shot["critical_windows"], shot["assets"] = [], []
        shot.pop("method", None)
        if chosen:
            plan.update(catalog=CATALOG_ID, style=chosen, release_version=PLAN_COMPATIBILITY_VERSION, product_version=VERSION, physics_contract="sumi-physics-v1")
            shot["physics"] = {"actions": [], "character_free_reason": ""}
            shot["environment"] = {"decision": "pending", "reason": "", "plan": None, "review": None, "visibility": None}
            shot["acting"] = {"status": "pending", "actors": [], "runtime_bindings": [], "coverage": [], "review": None}
            shot["style"] = chosen
            plan["treatment"] = {"recommended_for": STYLES[chosen]["recommended_for"],
                                 "motion_direction": STYLES[chosen]["motion_direction"],
                                 "delivery_context": "YouTube storytelling/documentary; animated opening and ending; compact captions; Python material SFX"}
            shot["mechanism"]["type"] = STYLES[chosen]["mechanism"]
            profile = json.loads((skill / "assets/templates/style-profile.json").read_text())
            profile.update(style=chosen, profile=STYLES[chosen]["profile"])
            settings = json.loads((skill / "assets/templates/shot-style-profile.json").read_text())
            if chosen == "sumi-original":
                plan["treatment"]["presentation"] = {**STYLES[chosen]["presentation"], "aspect": a.aspect}
                profile.pop("brush_ink")
                settings["original_drawings"] = {"budget_mode": "action-driven",
                    "sequence_id": "", "source_images": [], "designed_states": [], "exposure_plan": [],
                    "deliberate_stillness": False, "stillness_reason": ""}
                settings["cadence"] = {"output_fps": fps, "character_update_fps": 20, "exposure_frames": 1, "exposure_policy": "20-in-30", "source_time_model": "scene-first-designed-states"}
                shot.update(pose_fps=20, simulation_fps=30)
            else:
                profile.pop("original_preservation")
                profile["brush_ink"]["palette"] = LIGHT_PALETTE if chosen == "sumi-light" else {**DARK_PALETTE, "dark_red": DARK_RED}
                settings["layers"] = [
                    {"role": role, "z": z, "source_ids": [], "motion_rule": "", "empty_reason": ""}
                    for role, z in zip(["far-background", "background", "subject", "foreground"],
                                       [-500, -150, 0, 150])
                ]
                shot.update(pose_fps=12, simulation_fps=24)
            plan["style_profile"], shot["style_profile"] = profile, settings
            guides = {
                "sumi-original": [("references/styles/sumi-original.md", "STYLE.md")],
                "sumi-light": [("references/styles/sumi-light.md", "STYLE.md"),
                               ("references/brush-ink-workflow.md", "BRUSH-INK-WORKFLOW.md")],
                "sumi-dark": [("references/styles/sumi-dark.md", "STYLE.md"),
                              ("references/brush-ink-workflow.md", "BRUSH-INK-WORKFLOW.md")],
            }
            entries = [source for source, _ in guides[chosen]]
            entries.append("references/style-profile-schema.md")
            entries.append("references/scene-first-workflow.md")
            entries.append("references/production-continuity.md")
            entries.append("references/review-playback.md")
            entries.append("references/living-frames.md")
            entries.append("references/living-environments.md")
            entries.append("assets/templates/ENVIRONMENT-SHOT.md")
            entries.append("references/expression-and-action-continuity.md")
            entries.append("references/original-pacing-and-voices.md")
            entries.append("assets/templates/SCENE-FIRST-SHOT.md")
            entries.append("references/physics-gate.md")
            entries.append("references/hooks-endings-sound.md")
            entries.append("references/sound-routing.md")
            entries.append("references/supplied-narration.md")
            entries.append("references/dialogue-and-lip-sync.md")
            entries.append("references/new-project-intake.md")
            entries.append("references/reuse-and-context.md")
            entries.append("references/interface-brand.md")
            entries.append("references/delivery-dashboard.md")
            if chosen in {"sumi-light", "sumi-dark"}:
                entries.extend(["references/brush-character-prompts.md", "references/ink-footage.md", "references/ink-transitions.md"])
                shutil.copytree(skill / "assets/ink-footage", dest / "public/ink-footage",
                                ignore=shutil.ignore_patterns("*.html", "serve.py", "__pycache__", "*.pyc"))
            if chosen in {"sumi-light", "sumi-dark"}:
                entries.append("assets/templates/BRUSH-INK-SHOT.md")
            copy_guides(skill, dest, entries)
            shutil.copy2(skill / "assets/templates/SCENE-FIRST-SHOT.md", dest / "SCENE-FIRST-SHOT.md")
            for source, name in guides[chosen] + [
                ("references/style-profile-schema.md", "STYLE-PROFILE-REVIEW.md")
            ]:
                (dest / name).write_text(
                    f"# Sumi project guide\n\nRead [{Path(source).stem}](sumi-guide/{source}).\n"
                    "\nThe linked guide tree retains its local reference links.\n"
                )
        else:
            # Historical imports stay explicit and retain their old evidence contract.
            plan.pop("physics_contract", None)
            plan.pop("release_version", None)
            shot.pop("physics", None)
            plan.pop("catalog", None)
            plan.pop("style", None)
            shot.pop("style", None)
            shot["method"] = a.legacy_method
            shot.update(pose_fps=12, simulation_fps=30)
            shot["mechanism"]["type"] = LEGACY_METHODS[a.legacy_method]
            plan["compatibility"] = {"catalog": "historical-four-methods", "new_style_selection": False}
            if a.legacy_method == "living-ink":
                template = json.loads((skill / "assets/templates/living-ink-config.json").read_text())
                plan["living_ink"] = template["living_ink"]
                plan["living_ink"]["paper"]["coverage"] = [0, a.seconds]
                config = template["shot_living_ink"]
                config.update(drawing_fps=shot["pose_fps"], ink_simulation_fps=shot["simulation_fps"],
                              output_fps=fps)
                shot["living_ink"] = config
                plan["proof"]["living_ink_review"] = None
                shutil.copy2(skill / "references/living-ink-review-schema.md", dest / "LIVING-INK-REVIEW.md")
        if chosen in {"sumi-light", "sumi-dark"} or a.legacy_method == "living-ink":
            shutil.copytree(skill / "assets/ink-transitions", dest / "ink-transitions")
            gallery = dest / "ink-transitions/index.html"
            gallery.write_text(gallery.read_text().replace("../delivery-dashboard/", "../assets/delivery-dashboard/"))
            if chosen:
                (dest / "INK-TRANSITIONS.md").write_text("# Ink transitions\n\nRead the [editable project guide](sumi-guide/references/ink-transitions.md).\n")
            else:
                shutil.copy2(skill / "references/ink-transitions.md", dest / "INK-TRANSITIONS.md")
        if chosen:
            ep=json.loads((skill/"assets/templates/environment-plan.json").read_text())
            ep.update(style=chosen,fps=fps,frames=round(a.seconds*fps),width={"16:9":1920,"9:16":1080,"1:1":1080}[a.aspect],height={"16:9":1080,"9:16":1920,"1:1":1080}[a.aspect])
            (dest/"environment-plan.json").write_text(json.dumps(ep,indent=2)+"\n")
        (dest / "shot-plan.json").write_text(json.dumps(plan, indent=2) + "\n")
        for memory in (skill / "assets/templates").glob("*.md"):
            if memory.name == "BRUSH-INK-SHOT.md":
                if chosen in {"sumi-light", "sumi-dark"}:
                    (dest / memory.name).write_text(
                        "# Brush-and-ink shot specification\n\n"
                        "Complete the [editable specification](sumi-guide/assets/templates/BRUSH-INK-SHOT.md).\n"
                    )
                continue
            text = memory.read_text()
            def project_link(match):
                raw = match.group(1)
                if not raw.startswith("../"):
                    return match.group(0)
                source = (memory.parent / unquote(raw)).resolve()
                if skill in source.parents:
                    local = Path("sumi-guide") / source.relative_to(skill)
                    if (dest / local).exists():
                        return "](" + local.as_posix() + ")"
                return match.group(0)
            text = re.sub(r"\]\(([^)]+)\)", project_link, text)
            (dest / memory.name).write_text(text)
        project = json.loads((dest / "project.json").read_text())
        project.update(style=chosen or "historical-sumi", identity="japanese-sumi",
                       catalog=CATALOG_ID if chosen else "historical-four-methods",
                       storyPlanStatus="not-authored", motionProofStatus="not-reviewed",
                       title=a.title, width={"16:9": 1920, "9:16": 1080, "1:1": 1080}[a.aspect],
                       height={"16:9": 1080, "9:16": 1920, "1:1": 1080}[a.aspect],
                       fps=fps, durationSeconds=a.seconds)
        if not chosen:
            project["method"] = a.legacy_method
        (dest / "project.json").write_text(json.dumps(project, indent=2) + "\n")
        (dest / "out").mkdir(exist_ok=True)
        (dest / "public").mkdir(exist_ok=True)
    except OSError as error:
        p.exit(1, f"Copy failed; partial destination may exist: {error}\n")
    print(f"Created {dest}\nStyle: {STYLES[chosen]['name'] if chosen else 'historical ' + a.legacy_method}"
          f"\nOutput: {fps} fps. This is an unauthored starter, not animation proof."
          "\nWrite the story and direction, prepare complete source art, and fill the project evidence."
          "\nThe standard full-render command remains gated by current evidence and actual review."
          "\nNo dependencies, paid media, tests or rendering were started by this initializer.")


if __name__ == "__main__":
    main()
