# Portable physics and anatomy gate

Sumi 4.2.0 includes a local, service-independent check. It works from saved project files with standard Python 3; it does not require ChatGPT, this conversation, an API key or a new model. Any assistant or editor that follows the skill can produce the evidence. It is not an autonomous vision system and cannot stop someone deliberately bypassing the supplied render command.

## Run it

New projects copy `validate_physics.py` and its standard-library dependency `plan_provenance.py` into `scripts/`. From the project:

```sh
python3 scripts/validate_physics.py shot-plan.json --stage assets
python3 scripts/validate_physics.py shot-plan.json --stage proof
```

The first validates the planned action inventory/constraints; the second requires sampled geometry and actual visual-review evidence. Both return nonzero on failure. `npm run physics` runs the proof check, and `npm run render` invokes the standard preflight, which also invokes physics for 4.2.0/new plans. A missing physics script, missing trace, stale source, missing visual review or failed constraint blocks that final command. `npm run draft`, stills and preview remain available to build and repair proofs; they do not certify a deliverable. Direct use of a renderer outside these commands can bypass the gate.

For Canvas, SVG or another renderer, use the same JSON contract and run the Python command before the final export. Export actual geometry from that renderer. The bundled JavaScript [trace recorder](../assets/motion-core/physics-trace.mjs) can capture points; it does not discover anatomy or manufacture evidence. A Python or other application may write the same JSON without JavaScript. No automatic installation or third-party service is required.

## Plan each action

At plan root set `physics_contract: "sumi-physics-v1"`. Each shot has `physics.actions`; an action names a character already listed by the shot, its kind/view and an **end-exclusive** absolute output frame range. For each character, action ranges must cover the whole shot, including holds and transitions. The same character may have overlapping action records when useful. A character-free shot must have an empty inventory and a specific `physics.character_free_reason`.

An illustrative action (adapt its values and add the other required checks):

```json
{
  "id": "captain-step",
  "character": "captain",
  "kind": "start-walk",
  "view": "checked right three-quarter",
  "start_frame": 0,
  "end_frame": 48,
  "checks": [
    {"id":"right-shin","kind":"length","points":["rightKnee","rightAnkle"],"min":99,"max":101,"reason":"100-unit checked segment at this view/scale"},
    {"id":"right-knee","kind":"bend","points":["rightHip","rightKnee","rightAnkle"],"sign":1,"epsilon":0.01,"reason":"bend side from complete reference drawing"},
    {"id":"right-plant","kind":"pin","points":["rightSoleContact"],"anchor":[400,900],"max_error":1,"start_frame":0,"end_frame":12,"reason":"stance contact patch until heel lift"},
    {"id":"pelvis-step","kind":"step","points":["pelvis"],"max_error":12,"reason":"planned maximum displacement per output frame, including held-pose jumps"}
  ],
  "not_applicable": {"grip":"No object held in this action"}
}
```

Declare every relevant limb, joint and planted contact, not just the one shown in the example. Split contact windows for stance, heel/toe roll, flight and landing. Keep planned geometry/thresholds stable; never loosen them solely to make a failing trace pass. Document changes in direction and re-review. Every action requires `limbs`, `joints`, `support`, `grip` and `motion` check families or an explicit applicable reason in `not_applicable`. The visual reviewer must evaluate every exemption. Do not exempt a hidden body part merely because the final camera crops it.

Supported checks:

| Kind | Inputs | What is measured |
|---|---|---|
| `length` | two points, positive `min`, `max` | rendered segment length |
| `bend` | root/joint/end, `sign` ±1, `epsilon` | signed 2D cross product `(end-root) × (joint-root)`; epsilon has squared-distance units |
| `pin` | one visible contact point, fixed `anchor`, `max_error` | world-space stance drift |
| `surface` | one sole/contact point, `min`, `max` | permitted world y interval, e.g. floor contact/penetration |
| `grip` | visible hand grip and prop grip points, `max_error` | attachment separation |
| `step` | one point, `max_error` | displacement between consecutive output frames, including action entry when a preceding frame exists in that action |
| `support` | approximate mass projection, left/right support endpoints, `max_error` | x projection within the support interval, for deliberately slow supported movement |

Each check has unique `id`, nonempty `reason` and optional `start_frame`/`end_frame` inside its action. Scale/view-specific tolerances are necessary: projected segment lengths vary with deliberate foreshortening. The support check is a limited 2D balance diagnostic, not full dynamic balance or a 3D physical simulation. Fast motion needs appropriate authored catching steps and visual review. For an entry discontinuity, include frames before and after that entry in the action proof; a check cannot compare a sample that was never exported.

## Export real geometry

Use `world-design-pixels`: apply all actor scale/facing/rotation and outer group transforms, but exclude the camera. Fixed world anchors must not move when the camera moves. Export visible sole contacts, hand/prop grips and joints from the **same transforms used to draw them**, not a separate ideal skeleton. Supply an overlay in the final camera so a reviewer can confirm this correspondence. For whole drawings, annotate the corresponding real landmarks in each pose. Any unresolved reach clamp, collider penetration or renderer constraint failure belongs in that frame's `unresolved` list and fails the gate.

Every output frame in each action is required, including both repeated frames of an on-twos exposure. No selected-frame-only trace. Use the current digest from `python3 scripts/validate_shot_plan.py shot-plan.json --digest`. Trace schema:

```json
{
  "schema":1,
  "fps":24,
  "coordinates":"world-design-pixels",
  "plan_sha256":"CURRENT_PLAN_DIGEST",
  "actions": {
    "captain-step":[
      {"frame":0,"character":"captain","points":{"rightSoleContact":[400,900]},"unresolved":[]}
    ]
  }
}
```

This fragment is incomplete and must fail until all required points/frames are present. Hash the completed trace and put its `{path, sha256}` record in `shot.proof.physics_trace`. Source files declared in the plan are checked against real bytes; changing sources invalidates evidence. Do not fabricate points or prefill passes.

## Visual review remains required

Follow [limb-motion review](limb-motion-review.md), then save a JSON file bound to the same plan digest:

```json
{
  "schema":1,
  "plan_sha256":"CURRENT_PLAN_DIGEST",
  "actions": {
    "captain-step": {
      "start_frame":0,"end_frame":48,"reviewer":"ACTUAL_REVIEWER",
      "status":"unreviewed","normal_speed":false,"consecutive_frames":false,"final_art":false,
      "orientation":"","soles":"","hands":"","weight_transfer":"","entry_exit":"",
      "trace_matches_visible_geometry":"",
      "not_applicable_reviewed":{},
      "unresolved":["Review not performed"],
      "full_body_clip":{},"neutral_clip":{},"adjacent_frame_sheet":{},"sole_grip_overlay":{}
    }
  }
}
```

After actual inspection, replace blanks with specific observations and hash-bound evidence files, assess exemptions exactly as declared, and set pass/true/empty unresolved only when earned. Put this file's `{path, sha256}` record in `shot.proof.limb_review`. `reviewer` may name the actual capable local/other assistant or a human; it is not an identity/security attestation. If the environment cannot inspect images or playback, keep the relevant fields unreviewed and explain the blocker. Do not silently approve.

Automatic numeric checks operate only on declared, supplied data. The gate validates evidence presence, source binding and recorded outcomes; it cannot know whether a person/model's observation is true or whether the exporter omitted an undeclared body part. This portable combination improves failure detection without claiming perfect anatomy. Historical 4.0.0–4.1.1 plans retain explicit compatibility; new 4.2.0 plans must not downgrade their version to bypass the gate.
