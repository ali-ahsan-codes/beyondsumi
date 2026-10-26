# Three-style project records

**24October2026 override for new4.6.1+ projects:** use [Living Frames](living-frames.md). Original30fps/20 designed character states per animated second (whole drawings or supported derived acting), alternating two/one-frame exposures; source generation remains action-driven and deliberate stillness is documented. Light/Dark retain24fps/on-twos. New shot plans record `animation_strategy` and hashed living-frame master/targets/anchors/masks/rig/clean-plate evidence where used. Older rate/exposure contracts below remain historical compatibility. Cadence checks do not inspect pixels.

The primary catalogue is **Sumi Original, Sumi Light, Sumi Dark**. The exposure profile introduced in 4.1.0 is retained. Version 4.2.0 adds the [portable physics contract](physics-gate.md) and requires it in final-render preflight. Earlier 4.1.1 added instruction-level limb review. Focused initializer/exposure checks are recorded in release validation; they do not certify visual output. A schema is evidence bookkeeping, not visual judgement or an implementation of the described animation.

Use the existing schema-2 character, source and shot-proof records. New plans add `catalog: "three-styles-v4"`, a single film `style`, the same `style` on every shot, and `style_profile` at film and shot level. A comparison uses a separate plan for each style. Do not label a current shot with a retired `method` ID.

| Style ID | Profile | Mechanism label | Output clock |
|---|---|---|---|
| `sumi-original` | `original-preservation-v1` | `preserved-original-sumi` | 30fps with action-driven sources and variable exposures new adaptation; historical source unchanged |
| `sumi-light` | `brush-ink-on-twos-v2` | `layered-brush-ink` | 24fps / character on twos |
| `sumi-dark` | `brush-ink-on-twos-v2` | `layered-brush-ink` | 24fps / character on twos |

These labels route records. They do not implement a renderer or prove that an animation matches its style.

## Initialize without approving anything

```sh
python3 scripts/new_remotion_project.py /path/to/new-project --style sumi-light --seconds 30
python3 scripts/new_remotion_project.py /path/to/new-project --style sumi-dark --seconds 30
```

Original4.6.1 defaults to30fps/20 designed character states/s with action-driven source counts and supported derived acting for new adaptations. Record that choice separately from the preserved requestAnimationFrame source; do not retime the historical films.

The initializer copies incomplete templates, source helpers and guides. It does not install dependencies, generate artwork, run tests, render, or write a passing review. Keep unknown evidence empty until work is actually done. Standard full rendering still routes through `validate_shot_plan.py --stage proof`; `--stage assets` checks only the available asset/planning records.

## Shared authored plan

The top-level `style_profile` uses `schema: 1`, `status: "authored_spec_only"`, the selected `style` and `profile`. `status` describes the specification, while review status is a separate record.

- `story`: hashed approved script, exact `approved_text`, analysis and required visual actions.
- `source_files`: current authored animation code with project-relative path and SHA-256.
- `narration`: `mode` of `existing-approved-take`, `new-approved-take` or `none`; for narration, the approved and used source take must hash-match, with the real approval record. A mixed soundtrack is separate from the untouched narration source.
- `review`: starts `null`; never silently initialize a pass.

Original adds `original_preservation`: `baseline_name`, actual `baseline_revision`, hashed `baseline_sources`, source observation, preserved features, deliberate changes, source simulation notes, and export choice reason. The source name is **The Last Blossom**, not The Last Light. Distinguish the 56-second and revised 60-second sources. Do not replace the original source mechanism with the Light/Dark profile. For historical4.6.0 plans, per-shot cadence records `source_time_model:"scene-first-variable-exposure"`, output30fps and frame-evaluated character state; authored exposure rows choose the actual drawing holds. Baseline preservation retains the original elapsed-time source model separately.

## Light and Dark sources, clocks and direction

The `brush_ink` policy declares output 24fps, character update 12fps, exposure_frames 2 and character edge updates 12fps. Budget mode is `shot-specific`; each shot records planned and actual source/complete-pose counts. Four depth planes remain. Read the full [workflow](brush-ink-workflow.md) for acting and clock implementation.

Light records its eight permitted mineral swatches; each shot uses only the story-relevant colours. Dark records white `#FFFFFF`, carbon `#111111`, diluted ink `#5C5C5C`, optional equal-channel neutral greys, and optional `dark_red` (recommended `#7A1622`). Only that named accent may contain hue; record its story purpose, authored regions/mask and continuity. The palette checker accepts muted dark red, not arbitrary colour. Selective red preservation is permitted for those regions. Neutral-only Dark remains valid when the story needs no red. The historical Living Ink one-accent/85–15 rule does not apply to these styles.

Per-shot `style_profile` contains:

- `source_images`: `{id,file:{path,sha256},kind,roi_xywh?,board_dimensions?}` for every static source consumed. A complete board is one source only when used as one intact drawing; each separately used pose/atlas region is distinct. Renaming or transforming a source does not create a new drawing. File hashes and regions cannot detect falsely labelled or re-encoded copies; actual inspection still has to compare them.
- `budget`: `planned_source_images`, `planned_character_extremes`, then actual `unique_source_images`, `unique_character_extremes`, reuse rationale and action plan. Every used character-pose source must be in the source inventory. Relabelling a pose as scenery does not remove it from the character count. An intact complete-pair interaction region may be shared by both character records and counted once.
- `layers`: four records with `role`, Z, known `source_ids` or an explicit empty/procedural reason, and motion rule. Derivative passes and procedural masks refer back to their source; independently drawn stages count as sources.
- `exposure_plan`: each entry names `source_id`, `start`/`end` in absolute film seconds, driver (`hold`, `articulated`, `warp`, `replacement`), visible action and support/contact. A hold has a reason. A procedural event instead uses driver `procedural` and hashed `recipe_sources` from the authored source inventory. Put the detailed 12 Hz ticks and protected masks in the shot specification.
- `camera_cues`: start/end, onscreen `subject_id` or `world`, framing, angle, movement, story reason, and an exact `spoken_cue` from approved wording. Silent beats instead have `visual_cue` and `silent_beat_reason`.
- `effects`: `smear`, `impact`, `whip`, each `used` or `omitted` with a story reason. An omission is valid for a quiet beat.
- `profile_observation`: what was actually authored/implemented and what remains missing.
- `review`: `null` until performed.

Use [the shot specification](../assets/templates/BRUSH-INK-SHOT.md) for shader parameters, opacity/holdouts, internal movement, effects, captions, soundtrack and transition direction. Merely filling numerical settings is not implementation.

An entirely procedural character-free scene may use zero static sources when it records `procedural_only_reason` and the actual hashed recipes, camera and material direction. There is no fixed four-source ceiling in the new profile. Characters still require complete masters, pose evidence and honest source-region accounting; relabelling a character stage as a procedural container is not a budget exemption.

## Actual review

Only after inspection, per-shot `review` may record `status: "passed"`, reviewer ID/kind, current `plan_sha256`, inspected source/art/master file records, the hashed `normal_speed_clip`, `normal_speed: true`, and at least two actual adjacent-frame records. Frame records contain path/hash, film time, and the reviewed `clip_sha256`. Include concrete overall, budget, palette, acting/contact and camera observations, and `unresolved: []` only if there are no remaining issues.

The review clip must match that shot's base proof clip. All current authored sources, rendered artwork and used complete masters need recorded inspection. Normal-speed playback, adjacent-frame observation and audio listening remain distinct actions; these metadata checks do not perform any of them. Do not claim listening from waveform or hash checks.

Plan hashing excludes only review containers, so adding an honest review does not create a circular hash. Changing the authored plan or any bound file invalidates its prior evidence.

## Historical compatibility

Older schema-2 plans with `method` IDs remain readable through a dedicated compatibility branch. The hidden legacy initializer aliases exist only for explicitly continuing old projects; they are not current style selectors. A historical Living Ink plan keeps its original dedicated gate. Current Light/Dark plans use the new shared profile and their actual palettes. Saved retired style preferences are surfaced as history rather than silently converted into a current choice. The archived teaching labs retain labelled historical controls and do not become current style menus.

Historical `brush-ink-v1` records are checked with their 60/12/8 cadence and four/two limits only when release_version is 4.0.0. New plans use brush-ink-on-twos-v2; changing the version does not certify or migrate old rendered media.

## Historical Original exposure evidence —4.6.0 plans

Original retains30fps output. `pose_fps` and cadence `character_update_fps` are30 (the available evaluation clock, not new drawings/s); `exposure_frames:1` permits whole-frame variable holds, with `exposure_policy:"variable"`. `original_drawings` declares `budget_mode:"action-driven"`, `sequence_id`, hashed/region-bounded `source_images`, and contiguous `exposure_plan` rows naming `source_id`, inclusive `start_frame`, exclusive `end_frame`, `action`, and `hold_reason` for unchanged holds. Source counts are independent of output frames. No fixed minimum source rate is imposed. These checks cannot judge whether enough acting exists.

Versioned compatibility remains:4.5.0 per-scene14,4.5.1/4.5.2 at28fps/14,4.5.3/4.5.4 at30fps/15. Historical validators retain those rules; do not downgrade new plans to bypass current checks. Light/Dark remain24fps/on-twos. All three apply [the shared workflow](scene-first-workflow.md) and the same existing physics/review requirements.

## Current Original evidence —4.6.1

Use `pose_fps:20`, `simulation_fps:30`, cadence `{output_fps:30, character_update_fps:20, exposure_frames:1, exposure_policy:"20-in-30", source_time_model:"scene-first-designed-states"}`. Preserve the historical baseline record. `original_drawings` keeps action-driven sources, `designed_states` and the actual contiguous `exposure_plan`. Each state names `id`, `source_id`, and `kind:"whole-drawing"` or `"derived-character"`. Derived states also name a hashed `rig`, checked `target_ids` and finite meaningful `character_parameters` (hair/cloth/breath/eye/brow/mouth/tear/hand/body only). Camera/environment values do not count. Exposure rows name `state_id` and absolute `[start_frame,end_frame)` boundaries, alternating two/one frames from the shot's start. Checked cycles can repeat after20 distinct states; duplicate aliases cannot fill a state window. Deliberate stillness requires its reason and is not counted as animation.

Shared `animation_strategy` selects `whole_pose`, `living_frame` or `mixed`. Living-frame records include master/hash, intent, primary/supporting details, protected regions, motivated camera/stillness and each motion's target/anchor/mask/rig with a clean plate or explicit supported no-hidden-pixels explanation. At proof stage record the actual comparison file/hash and observations. These checks validate authored evidence, not actual pixel/anatomy quality; inspect the real render.
