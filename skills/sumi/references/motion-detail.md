# Per-video motion detail, image calls and lip-sync

Ask for these choices on **every new video**, including a story/prompt, supplied recording or dialogue-driven request. An answer already explicit in the current brief counts; a saved preference from an older film does not silently answer for this one. Keep the question human and short. Confirm missing duration first, then narration/dialogue/both/none. Recommend a style and identify the actual artwork route before describing its default.

## Image-based motion choice

For Sumi Original, Light and Dark, offer **Default** or **Smoother, up to 24 distinct pose/in-between drawings per animated second** before generating artwork. Default Original is 30 output fps/20 designed character states per animated second; Light/Dark are 24 output fps/up to 12 paired states. Smoother Original retains 30 output fps with a 24-state exposure clock; smoother Light/Dark retain 24 output fps with one-frame character exposures. Their art, material, camera and sound identities remain distinct.

Suggested question for every new story, prompt or supplied-audio film: “This style’s default is [30 / 24] output frames per second with [20 / up to 12] character motion states per animated second. Would you like the default, or smoother movement with up to 24 pose/in-between drawings per animated second? The smoother option may need extra image calls, tokens, cost and processing. I’ll show the artwork/call budget before generation.”

**This is actual character artwork and performance, not an FPS-only switch.** In active smoother passages prepare distinct connected whole-character poses/in-between drawings, including anticipation, weight transfer, contact, follow-through and settling. Generate additional matching pose artwork when required. Several drawings may share one checked sheet; crop only observed valid cells. Reuse exact compatible drawings/cycles. Camera movement, new grain, repeated stills, renaming files and hair-only rig changes do not count as additional full-action pose drawings. Secondary eyes/hair/cloth/breath still help but cannot replace the required action. Quiet holds remain deliberate and explained.

Both choices must receive professional animation care. The default is not permission for frozen posters or rough movement. Plan connected poses and in-betweens, spacing/easing, believable weight and foot/grip contact, overlapping hair/cloth/breath and emotional faces; keep the selected style’s material and camera vocabulary. Time each movement to its story cause and the final speech/sound. More pose images must improve the action’s continuity, not just its count.

Before a full batch, prove a difficult representative movement and any visible speaking passage at the selected detail. Review the actual animation at normal speed for popping, abrupt pose jumps, unwanted slides, unstable faces and mouth sync. If it is still awkward, repair the pose/timing/registration within the approved budget or ask for a bounded increase. A higher number or successful metadata check is not proof of professional smoothness.

Record source drawings/regions, actual generation calls, derived states, reused exposures and output frames separately. Twenty-four drawings do not imply twenty-four API calls. Preserve final timing, identity, support, hand/leg mechanics and actual normal-speed proof. Density metadata does not certify smoothness.

## Before each separate image call or batch

Show the purpose, needed new pose/in-between/mouth drawings, sheet/panel resolution, planned number of calls, maximum approved calls, expected token/credit/cost/time impact where knowable, and exact compatible reuse. Get approval of that scope before new generation. One approval may cover a clearly bounded batch; do not repeat it for every call inside that batch. Stop before an extra call/retake exceeds it and ask for the increase. Motion-choice approval does not itself authorize paid images, voices, installations or unbounded retries. For a standalone animation sheet/image-generation request, confirm the same motion/detail scope and call budget; an isolated still image has no FPS of its own.

Use `motion_detail.image_batches`: unique `id`, `purpose`, `new_pose_drawings`, `image_calls_max`, `actual_image_calls`, and the actual `approval_record`. Exact reuse instead of calls needs `reuse_only_reason`. Never invent receipts or claim measured token use from drawings/FPS alone.

## SVG exception

Keep SVG’s current style defaults. Do not ask the extra motion-detail question or automatically offer the 24-drawing increase on SVG. Record the route as SVG/default/not-applicable. If the user explicitly requests a different SVG treatment, plan that request separately; switching to generated images requires the image-route choice and budget above.

## Lip-sync on every video’s brief

Lip-sync needs actual speech and a visible speaker. Narrated/spoken videos use it on visible speaking roles, matched to their final lines; music/SFX-only videos have no lip-sync. Offscreen narrator prose never makes unrelated story characters speak. Include speaking views and matching mouth/expression art in the approved direction when the story calls for them.

Ask whether the story should use narrator only, character dialogue or both, and offer **lip-sync on/off for visible speaking characters**, recommending on for dialogue. A current explicit choice needs no repeat. For narration-only or no speech, explain that visible character lip-sync is not applicable; never move unrelated mouths to the narrator. This dialogue choice applies to SVG too; only the motion-detail prompt is exempt there.

With lip-sync on, use [the dialogue guide](dialogue-and-lip-sync.md): exact lines, role→final audio map, identity/angle-matched mouth and expression drawings, real phrase/phoneme timing, rest at pauses and emotional acting. Include added mouth/expression artwork in the separate image-call budget. Preserve supplied recordings. A back-facing or offscreen speaker needs no visible mouth flapping. A request for dialogue or lip-sync is not permission to rewrite approved narration or buy a new take.

Record `dialogue_animation.speech_mode`, `lip_sync` (on/off/not-applicable), `approval_record` and the `voice_map` location. Review actual line starts, pauses, ends and adjacent cuts. Record approximate timing or unavailable checks honestly.

## Records and gates

New initializers leave choices pending; SVG bypasses only the motion question. The standard gate blocks missing per-film choices and overspent image batches. Smooth24 requires hashed whole-drawing state/exposure evidence (`original_drawings` for Original, `motion_drawings` plus the normal source inventory for Light/Dark). Deliberate stillness needs a story reason. Existing historical plans/films retain their approved contracts; these changes start no film or paid call.
