> Historical 3.1 compatibility record. The current styles are Sumi Original, Sumi Light and Sumi Dark, using the [current profile schema](style-profile-schema.md). This dedicated Living Ink gate remains for explicitly continued older projects and does not impose its palette/cadence rules on current styles.

# Historical Living Ink workflow and AI review records

`scripts/validate_living_ink.py` adds an evidence gate to schema-2 shot plans. It does **not** run an AI model, inspect pixels, listen, judge anatomy or create an approval. The assistant must inspect the actual supplied reference passages, whole-character art, rendered frames and normal-speed clips, then write truthful observations. A validator pass means the records are complete and current; it does not establish artistic quality.

Keep the completed review `null` until the inspection occurs. Never initialize observations or verdict to `pass`. Do not substitute a tool-success message, file metadata, storyboard descriptions or synthetic tests for visual review. If playback/listening is unavailable, disclose the missing check and leave a necessary review unresolved.

## Integration

For a historical plan with `method: "living-ink"`, the standard validator dispatches the additional Living Ink checks. The commands below run the combined gate:

```sh
python3 scripts/validate_shot_plan.py /absolute/project/shot-plan.json --stage assets
python3 scripts/validate_shot_plan.py /absolute/project/shot-plan.json --stage proof
python3 scripts/validate_living_ink.py /absolute/project/shot-plan.json --stage proof
```

The hidden compatibility alias `new_remotion_project.py --legacy-method living-ink` exists only for explicitly continued historical work. It receives the old incomplete configuration, validator dependencies and 24-mechanism library. Current projects use `--style sumi-original`, `--style sumi-light` or `--style sumi-dark` and the current profile schema. `npm run render` runs the combined proof preflight before Remotion. Initialization neither generates art nor completes approvals/reviews.

The outer shot plan stays at schema 2. **New Living Ink configurations use `living_ink.schema: 2`**, adding drawing budgets, timed exposure sequences, story-linked camera cues and local continuity. Historical Living Ink schema 1 remains readable without retroactively requiring those new fields. Do not downgrade a new plan to evade its missing direction/evidence. The external AI inspection record remains schema 1; its current plan hash binds the additional fields too.

For a render wrapper:

```python
from validate_shot_plan import validate
errors = validate(plan, project_root, stage)
# Abort full rendering if errors is nonempty. Do not rewrite review verdicts.
```

The functions return lists of errors. `validate_shot_plan.validate_base` remains available for focused base-only tests; production calls use `validate`. The additive `validate_living_ink.validate` remains available for focused method checks, and returns an empty list for projects without Living Ink shots. Missing method-validation code blocks Living Ink rendering instead of silently falling back to the base gate. `root` is the plan's directory. File records use `{"path": "relative/file", "sha256": "actual 64-character hash"}` and must stay inside that directory. Referencing private source screenshots here does not authorize packaging them in the portable skill.

`--digest` prints `plan_digest` without approving anything. Its unchanged algorithm now lives in the shared `plan_provenance.py` and remains importable from `validate_shot_plan`. This avoids circular imports. That digest excludes top-level and per-shot `proof`, but includes all Living Ink settings, source/art hashes and approved content. Completed AI review is an external JSON file under `proof.living_ink_review`; this avoids a recursive hash.

## Plan extension

Retain all ordinary schema-2 fields, complete character masters, checked whole poses, mechanism sources and shot proofs. Add the following `living_ink` object. This example is an incomplete structural guide; fill real files, timings and decisions before validation.

```json
{
  "living_ink": {
    "schema": 2,
    "story": {
      "script": {"path": "script.txt", "sha256": "..."},
      "analysis": "What changes emotionally and which actions must be visible.",
      "colour_reason": "Why this story needs the chosen single accent.",
      "required_visual_actions": ["Explicit action from the approved direction"]
    },
    "palette": {
      "base": ["black", "charcoal", "off-white"],
      "accent": {
        "name": "crimson",
        "hex": "#A62028",
        "story_meaning": "Define the story meaning; red need not mean violence.",
        "permitted_uses": ["Name the specific recurring motif or power word"]
      },
      "monochrome_target": 0.85,
      "accent_target": 0.15,
      "negative_space_target": [0.30, 0.40],
      "ratio_is_directional": true
    },
    "paper": {
      "image": {"path": "art/paper.png", "sha256": "..."},
      "coverage": [0, 30],
      "continuity": "single-substrate",
      "canvas_space": "screen-fixed",
      "wash_behavior": "Pigment washes away; the same paper grain remains."
    },
    "source_files": [{"path": "src/ink-animation.js", "sha256": "..."}],
    "source_references": [
      {
        "source_name": "Supplied reference title",
        "evidence": {"path": "private-research/passage-frames.jpg", "sha256": "..."},
        "observed_motion": "Specific observed density, edge and form change.",
        "coverage": "Actual source time interval and frame sampling.",
        "limits": "State what was not inspected; never imply all-frame study."
      }
    ],
    "narration": {
      "mode": "existing-approved-take",
      "audio": {"path": "audio/approved-voice.mp3", "sha256": "..."},
      "transcript": {"path": "audio/approved-words.txt", "sha256": "..."},
      "approved_text": "Exact approved spoken wording.",
      "approved_take_sha256": "...",
      "preserve_wording": true,
      "approval_record": "Where the user's approval was recorded.",
      "delivery": "Use the saved performance and retain its natural timing.",
      "processing": "State any planned mix processing; keep the source unchanged."
    },
    "required_words": [],
    "sound": {
      "method": "local-python",
      "direction": "Material sounds, sparse score and world foley chosen for the story.",
      "events": [
        {
          "id": "birth-drop", "kind": "tactile", "start": 0, "end": 0.5,
          "trigger": "scene-birth", "description": "Quiet wet drop on paper"
        }
      ]
    },
    "captions": {
      "mode": "ink-phrases",
      "readability_plan": "Hold readable phrases in deliberate negative space.",
      "items": [
        {
          "id": "caption-1", "text": "Approved words", "start": 1, "end": 3,
          "placement": "Left open paper", "readability": "Clear contrast and adequate hold",
          "reveal": "brush-matte", "accent_hex": null
        }
      ]
    },
    "transition_selection_rationale": "Choose a few material mechanisms that serve the story; retain local continuity elsewhere.",
    "transitions": [
      {
        "id": "scene-birth", "kind": "ink-drop-birth", "start": 0, "end": 1.5,
        "classification": "local", "story_reason": "Introduce the subject at the narrator's first mention.",
        "from_shot": null, "to_shot": "s1",
        "material_cause": "A wet drop makes the first pigment reservoir.",
        "onset": "Small dense bead",
        "propagation": "Irregular wet edge branches and fills subject masses.",
        "resolution": "Readable subject with evolving diluted edges",
        "preserves_paper": true, "sound_event": "birth-drop"
      }
    ]
  },
  "proof": {"living_ink_review": null}
}
```

Supply one accent, chosen from the story; diluted values of that pigment are allowed. The 85/15 and 30–40% values are composition targets, **not** strict per-frame pixel counts. Atmospheric washes can remain grey. They must not conceal a static slide behind a general distortion filter.

Allowed narration modes: `existing-approved-take`, `new-approved-take`, `none`. Both spoken modes require exact transcript/approved-text agreement and the approved audio hash. `none` requires `reason`, without fabricated audio. `required_words` declares essential spoken/displayed text; the gate checks presence in the transcript or captions, while the reviewer checks actual delivery/display.

Sound methods: `local-python`, `supplied`, `explicit-silence`. Explicit silence requires its direction to explain the user's choice; otherwise provide events. Event kinds are `tactile`, `world-foley`, `score`. Use synthetic instruments honestly; do not claim authentic recorded shakuhachi or taiko if the sound is synthesized. No narration or software installation is triggered by this validator.

Caption modes: `ink-phrases` or `none`. Keep `items: []` for no captions and explain the readability/absence decision. Required displayed text remains governed by the direction script. A caption may use the single accent or `null`; additional accent colours fail.

Material event types: `ink-drop-birth`, `brush-stroke-action`, `water-wash`, `object-ink-morph`, `material-continuity`. Every adjacent Living Ink shot boundary must have a material representation linking the shot IDs; **this does not require a major transition**. A retained stain, slight local wash, growing root or settled edge can continue the action without obscuring it. Schema 2 requires `classification: "major"` or `"local"` and `story_reason`; `material-continuity` must be local. Describe the actual cause, onset, propagation and resolution. The optional `mechanism_id` can identify a selected authored catalogue field, without replacing those descriptions.

A local event may have `sound_event: null` with an explicit `sound_reason`, such as “quiet settlement under the narration; no added accent.” Major events need their matching sound event unless the film's sound choice is explicitly silent. A typical 30-second film should begin with three major mechanisms, and use a fourth only when the story needs it. This is a direction default, not a validator quota or a universal limit on longer films. `transition_selection_rationale` explains the chosen variety and restraint. A label or filled record does not prove material behavior.

## Per-shot extension

Add `living_ink` to every Living Ink shot:

```json
{
  "drawing_fps": 10,
  "ink_simulation_fps": 30,
  "output_fps": 30,
  "ink_mass_change": "Explain what pigment does inside this shot, beyond revealing it.",
  "whole_pose_strategy": "Identify the checked complete drawings and their intentional action.",
  "negative_space": "Which open paper area supports the composition and captions.",
  "drawing_budget": {
    "unique_source_drawings": 1,
    "purpose": "The puppy is resting after finding shelter.",
    "risk": "Keep its whole-body support and expression readable.",
    "reuse_rationale": "This quiet hold does not need invented limb movement."
  },
  "exposure_plan": [
    {
      "id": "s1-puppy-rest", "character_id": "puppy", "pose_ids": ["rest"],
      "start": 0, "end": 4, "exposure": "hold", "exposure_ticks": [40],
      "action": "Hold the checked resting drawing.",
      "hold_reason": "A deliberate quiet pause after the narrated arrival."
    }
  ],
  "camera_cues": [
    {
      "id": "s1-puppy-focus", "start": 0, "end": 4, "subject_id": "puppy",
      "spoken_cue": "Exact phrase from the approved narration",
      "framing": "Whole body with visible ground support",
      "angle": "At the puppy's eye level", "movement": "Hold",
      "story_reason": "Give the viewer time to read its change from fear to rest."
    }
  ],
  "layers": [
    {"role": "paper", "files": [{"path": "art/paper.png", "sha256": "..."}], "motion_rule": "Fixed"},
    {"role": "environment", "files": [], "empty_reason": "Neutral mechanism study", "motion_rule": "None"},
    {"role": "subject", "files": [{"path": "art/whole-pose.png", "sha256": "..."}], "motion_rule": "Describe pigment and pose changes"},
    {"role": "foreground", "files": [], "empty_reason": "No foreground in this shot", "motion_rule": "None"}
  ]
}
```

There are exactly four separated layer roles. Empty layers need a reason. Paper must reuse the persistent paper hash. Whole-character drawings precede any derived parts; the base validator checks character/pose provenance.

Drawing exposure is 8–12 fps and must match `pose_fps`. Ink simulation and export cadence are distinct from drawing exposure; match the corresponding `simulation_fps` and `output_fps`. A 30/60 fps export is allowed. Fewer unique drawings or held exposures do not themselves establish token savings. Keep critical contact and emotional performance clear.

### Drawing count, exposures and camera cues in schema 2

`drawing_budget.unique_source_drawings` is derived from the shot's declared used character poses, using unique pairs of the actual source image SHA-256 and its canonical `roi_xywh` (or the whole image). Pose aliases, file paths, `crop_id` labels and scale/rotation transforms do not add drawings. Multiple checked whole poses on one board can count separately through distinct bounded regions. A region requires four nonnegative pixel coordinates/sizes with positive width/height and `board_dimensions: [width,height]`; its bounds must stay within that board. This is a provenance count of source regions, not a computer-vision judgment that two drawings look different. It cannot detect a duplicate drawing re-encoded into a different file. The source-art reviewer must compare them. Character-free studies use zero used character drawings and still need their budget rationale.

There is no universal minimum drawing count. Explain the shot's purpose, performance/contact risk and reuse choice. A still corpse or meaningful grief pause may use one held whole drawing; a difficult hand contact may need more reviewed drawings. Planning ranges in the direction guide are recommendations, not gates that force unnecessary motion.

Each `exposure_plan` entry declares a globally unique ID, used character ID, ordered `pose_ids`, absolute film `start`/`end`, `action`, and one of:

- `hold`: one drawing, with `hold_reason`.
- `one-shot`: play the declared sequence once, then hold its last drawing if needed.
- `cycle`: repeat the ordered sequence; at least two entries are required.

`exposure_ticks` has one positive integer for each pose entry. A tick is `1 / drawing_fps` seconds. For example, four poses with `[6, 6, 8, 16]` at 12 drawing fps occupy three seconds. The duration of one sequence must fit its interval within one drawing tick; a non-cycling sequence with a longer remainder needs `hold_reason`. The plan may repeat a source pose intentionally. Every pose declared as used in a shot must appear in an exposure entry; no unknown pose may be introduced. Exposure intervals for the same character may not overlap. Gaps are allowed when a character is offscreen; explain entrances, exits and the visible action in the direction. These timing records do not establish smooth or anatomically correct performance.

Each camera cue has a globally unique ID, interval inside the shot, `subject_id` (a used character or `"world"`), framing, angle, movement and story reason. A nonempty `spoken_cue` must be an actual phrase in the approved narration. A silent visual beat instead uses `visual_cue` and `silent_beat_reason`. Camera holds are valid; repeated automatic zooms are not required. The reviewer checks that the intended subject and world effect are actually visible at the narrated time. A substring check alone cannot establish audiovisual synchronization.

## Completed AI inspection record

After actual inspection, save a JSON record and set `proof.living_ink_review` to its file record. Changing the plan/source/art after review invalidates it. Review evidence files are also hashed.

```json
{
  "schema": 1,
  "plan_sha256": "digest of the current plan",
  "verdict": null,
  "reviewer": {
    "kind": "ai",
    "name": "Actual reviewing agent",
    "model": "Actual model identifier",
    "completed_at": null,
    "inspection": "actual-files-and-normal-playback"
  },
  "evidence": [],
  "observations": [],
  "issues": []
}
```

Only the reviewer changes `verdict` to `pass`, writes a timestamp with timezone and fills findings **after** the checks. Examples deliberately leave completion fields unset.

Each evidence item has `id`, `kind`, and `file`. Required kinds:

- `script`: same script hash as the plan.
- `source-reference`: every declared private source-study evidence file.
- `character-master` and `whole-pose`: every declared complete master and pose. Character-free studies cannot certify later characters.
- `rendered-frame`: real capture file plus film `time` and `clip_sha256`.
- `clip`: an actual current shot-proof clip, its film `start`/`end`, `playback_rate: 1`, and `watched_complete: true` only after complete playback. Clips must cover each shot.
- `audio`: the actual approved narration take when narration is used.

Each observation has `area`, `result`, `finding`, and `evidence_ids`. Areas required:
`story`, `japanese-sumi-identity`, `living-ink-motion`, `paper-continuity`, `anatomy-contact`, `transition-material`, `caption-readability`, `audio-narration`.

`result` is `pass` or `not-applicable`; applicability exceptions are limited to anatomy for explicitly character-free studies, captions when absent, or audio when both narration and sound are explicitly absent. Unperformed required checks cannot be called not applicable.

For ink motion, anatomy/contact and material transition, observations must cite normal-speed playback **and** at least two distinct rendered-frame times. Material-transition observations also declare `transition_ids`; each event requires two observed frames inside its interval. These minimums do not replace dense adjacent frames at contact, changes of view or difficult wet boundaries.

Issue records have `description`, `severity` (`blocking`/`minor`) and `status` (`open`/`resolved`). Open blocking issues fail. Resolved issues need `resolution` and current `evidence_ids`. Minor remaining limitations must be disclosed to the user.

For schema-2 Living Ink plans, also include `performance-exposure` and `camera-story-focus` observations. Each specifies `shot_id`, its `exposure_ids` or `camera_cue_ids`, a concrete finding and actual `evidence_ids`. Every planned exposure and camera cue needs at least two observed frame times inside its own interval and a cited completed normal-speed clip covering that interval. One observation may cite several IDs when it actually checks them, but broad labels cannot replace the interval evidence. Character-free performance may be not applicable; camera/story focus still needs review. Keep these fields absent or unresolved until the inspection happens.

```json
{
  "area": "camera-story-focus",
  "result": null,
  "shot_id": "s1",
  "camera_cue_ids": ["s1-puppy-focus"],
  "finding": "",
  "evidence_ids": []
}
```

The AI critic should compare reference motion, approved story, actual source art and proof together: identity and limb orientation, physical contact, evolving pigment, uninterrupted paper, single accent meaning, negative space, readable words, preserved narration and purposeful sound. It must report what it actually saw/heard. The deterministic gate cannot detect a dishonest review, identify malformed anatomy from pixels or infer audio quality.

## Regression verification

```sh
python3 -m unittest discover -s scripts -p test_living_ink.py -v
```

Tests use synthetic bytes and explicitly fictional review records in temporary directories. They test evidence validation only. They do not produce usable art, playable films or genuine AI review evidence.
