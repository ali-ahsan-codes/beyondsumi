# Expressions, emotional acting and connected action

Shared by Sumi Original, Light and Dark. Read with [Living Frames](living-frames.md) and [scene-first production](scene-first-workflow.md). This is a performance addition to the existing engine, not a new style. Preserve each style's art, camera, captions and transitions. Original remains30fps/20 designed character states/s; Light/Dark remain24fps/paired states. Output dimensions follow the selected aspect; FPS, state rate, source resolution and generated-image count are separate quantities.

## Plan the emotional change

Before new artwork, record what each important character knows, feels, conceals and visibly changes. Select a readable primary action: gaze shifts toward a sound, fingers tighten, eyelids lower, a hand hesitates before touching, or shoulders settle after bad news. Define anticipation, onset, peak, response and settle in actual narration-aligned frames. Small hair/cloth/breath motion supports the primary action. It cannot replace missing walking, grasping, lifting or resistance.

Use restrained timing appropriate to the emotion. Fear may interrupt breathing and tense fingers; grief may lower gaze and settle shoulders; anticipation may hold nearly still. Avoid running identical sinusoidal breathing, wind and blinks through every emotion. Author occasional blink/gaze changes, not synchronized metronome loops. A purposeful still hold is valid; document its story reason.

## Reuse supported art

Check approved whole masters, matching poses/expressions, safe local articulation and compatible existing rigs before new generation. A face derivative must preserve identity, neck alignment, lighting and body/set registration. Preserve complete sources and mask hashes; protect crown, hair roots, hands, grips, feet and rigid props unless the planned action explicitly moves them. A real head turn, hand release or changed silhouette may require a missing breakdown/clean plate; do not stretch a neutral face or dissolve incompatible poses to fake it. Generate only the needed expression/action states. Original has no animated splash treatment; Light/Dark retain their distinct brush construction.

## Primary movement and contact

Walking needs contact/down/passing/up phases, alternating legs, weight transfer and travel consistent with perspective. Track the planted foot in world space through its support interval. Grabbing/lifting/pushing needs approach, contact, force, response and follow-through; hand and prop share the same attachment until release. Use complete interacting drawings or parts derived from one checked whole composition. Review at normal speed and at pose boundaries. Add a missing breakdown or a motivated supported cut where safe articulation cannot carry the action. Do not increase a clock or add wobble to disguise a sparse action.

## Bind the plan to the actual renderer

Use the existing shot record and event ledger. Populate `acting` with actors/emotional arcs, primary/secondary details, required states, anchors/contact intervals, protected regions, source/master/mask hashes and runtime bindings. A binding names the consumed exposure/rig/target and frame interval. Label deliberate stillness and unresolved movement explicitly. Keep pending review until actual rendered evidence exists; writing a manifest does not implement its contents.

Audit coverage against every exposed source/view, including closing shots and alternate poses. A target attached to one filename/prefix does not cover another ending image. Re-author targets after source/crop/view changes. Inspect whether the actual exported face/hand/foot performs the planned action. Camera/light-only change and empty parameter ticks do not count as character acting. Separate source drawing count, generated calls, reused art, derived states and output frames.

## Sound and smallest repair

Use actual contact/release/reaction frames for sound. Keep speech, music, ambience and material effects independently editable. Measure duck attack/release and recovery against an unducked source where a mix concern exists; an overall loudness result alone cannot establish recovery. Do not assume repeated attenuation without inspecting code/audio. Preserve natural breaths; do not insert dead air to stretch duration.

Prove the hardest changed action, then review adjacent shots and the actual export. Repair the smallest affected asset/frame range and invalidate only its dependencies. Record missing evidence, source resolution and anatomy/registration limits. Tests of timing/hashes/anchors support review but do not automatically recognize anatomy, certify expression or replace listening. User praise of one performance is not universal certification.
