# Sumi motion: physical credibility and shot review

Shared physics and motion-review guidance for **Sumi Original, Sumi Light and Sumi Dark**. Follow the selected current style profile when an older example conflicts with its source budget, cadence or palette. Light and Dark intentionally share the brush-and-ink workflow and may share geometry, animation mechanics and a suitable performance; they do not require unrelated motion engines. Every story still needs directed acting, staging, camera, editing, sound and credible physical consequences. Earlier treatment names are historical technique vocabulary.

## Scope

Read this when a shot needs physical contacts, locomotion, released objects, environmental dynamics or motion review. The [motion-core helpers](../assets/motion-core/motion-core.mjs) and [tests](../assets/motion-core/test-motion-core.mjs) cover bounded geometric behavior. Run `node assets/motion-core/test-motion-core.mjs` from the skill folder; project initialization copies these into `motion-tools/`. They are implementation building blocks, not finished animation or a physics engine. Reference observations and their limits are in [the motion recheck](motion-reference-recheck.md).

**Physical plausibility is part of direction.** We may deliberately hold a drawing, exaggerate a silhouette, hide a recovery in an honest cut, or turn a dead monster into ink. We must preserve the causal event underneath that choice: a supported stance, a hand on the handle, contact before reaction, and the monster remaining defeated. Numeric constraints do not establish natural acting or a beautiful film.

For portable execution in any supported local renderer, use the [physics gate](physics-gate.md). New projects must supply transformed geometry and action review; the standard final-render command blocks failures.

## Before producing assets or complete exports

First obtain approval of the proposed story, direction and estimated runtime under [the director workflow](director-workflow.md). The following proof work is part of that approved production.

1. Preserve the complete approved narration and story. Build a phrase-to-shot ledger. Every spoken causal step and every indispensable visual beat must have time. If their measured performance plus action pauses exceeds the brief, present the full estimate and a concrete shorter alternative for the user’s choice. Carry out a concrete approved choice without asking again; older broad permission does not override a newer ask-first instruction. Do not silently remove script sentences to keep a preset length. Follow [the script-duration contract](script-duration.md): when authorization is absent, ask the future user to choose full length or a concrete shorter edit before changing approved content.
2. Write the selected film's motion treatment: how bodies move, how material appears, how the camera sees it, how time is edited, and how sound supports its material. Light/Dark may share mechanics and a suitable performance; use their respective palette policies and shared source budget. Choose shot durations, poses, staging, edits and atmosphere from the story rather than manufacturing differences between styles.
3. Build the hardest **three-to-six-second shot** for that style before a complete film: walk-to-stop if locomotion is central; blade impact and aftermath for combat; falling flower for delicate nature; fog reveal for atmospheric depth. Include simple proxy art, actual hierarchy, final camera crop, collision geometry, and an event sound marker. A successful static frame does not pass this gate.
4. That first proof is not certification of every action. Apply [limb-motion review](limb-motion-review.md) to each distinct walk/start/stop, kneel/rise, turn, reach/grip or fall used by the film, including transitions between them. Review that shot at normal speed and inspect consecutive frames. Fix the rig, staging and contact before expensive art or whole-film renders. Review the finished art again because apparent anatomy, grip and occlusion can change after replacement.
5. Where useful, inspect a fixed-camera view with textures and colour temporarily neutralized to verify that internal action and contact remain readable. This diagnoses motion hidden by visual treatment. Identical mechanics in Light and Dark are allowed; this check does not require them to have distinct choreography.

## A shot contract the renderer can actually enforce

Keep world positions, rig-local positions and screen positions separate. Choose world scale once per shot. A camera moves the whole world; it must not move only the actor or silently alter its stride length. Name units in code (design pixels, seconds, radians), and apply scale/facing/rotation to attachments in the same order as rendering.

For every shot retain a compact record:

```js
{
  id: 'mentor-deflects', style: 'sumi-light', technique: 'wash',
  narrationIds: ['threat-reaches-the-gate'],
  startState: { swordOwner: 'mentor.right', monsterAlive: true },
  endState: { swordOwner: 'mentor.right', firstHeadRebounding: true },
  contacts: [{ id: 'deflect', time: 2.16, a: 'blade.edge', b: 'head.cheek' }],
  support: [{ from: 0, to: 2.6, anchors: ['leftFoot'] }],
  camera: { kind: 'side-dolly', focus: 'contact', cutAtEnd: true },
  review: { contactFrames: [-6,-3,-2,-1,0,1,2,3,6,12], fullSpeed: true }
}
```

Use actual contact/ownership events to drive reaction, impact SFX, particles and shake. Do not independently type similar timestamps into four systems and assume they remain synchronized after editing. Keep `defeated`, `broken`, `released` and `resting` as persistent outcomes derived from absolute time/events.

## Walk, stop, turn, kneel, rise

**Travel drives gait.** For a monotonic walk segment calculate traveled world distance, then derive stride phase from the character's world-scale stride. During stance, pin the foot to a world anchor. Convert that anchor back into rig space for IK; do not add a local sliding-foot function to a differently scaled moving body. Use a separate planted anchor for each foot and overlap contacts around transfer.

The supplied `gaitFoot()` does this for a level monotonic walk. It is a useful starting point, not a full gait system. Start/stop and reversal need authored transition poses: shorten the final step, plant, pass weight onto the foot, settle hips, then allow torso/cloth follow-through. A walk should not keep stepping when root travel becomes zero. Use a new segment/phase plan when turning rather than changing the sign of velocity under an unchanged foot cycle.

**Support belongs to the body, not just shoe coordinates.** At slow speed, project an approximate body centre of mass over the support foot or interval. At speed, purposeful forward lean is allowed, but the following step must catch that momentum. During a kneeling rise show hand/knee support, pelvis lift, foot plant, weight transfer and torso extension. Do not rotate an entire upright rig around its ankle to represent a complex fall or recovery.

Use fixed bone lengths. The helper `twoLink()` returns both the reachable end and an explicit failure flag. When the requested target is unreachable, move the pelvis/shoulder, change the pose, or add a foreshortened drawing. Never draw the original distant end after clamping only the elbow/knee calculation; that stretches the second segment. Check lower/upper reach bounds and bend direction.

Keep the shoe a rigid sub-object about its ankle/sole. Toe roll, heel lift and sole flattening are authored rotations/deformations; do not leave one vertex on the floor while moving the rest of the shoe vertically. Major body turns need appropriate alternate poses/drawings, not a mirrored face pasted onto an incompatible torso.

A useful close shot needs eyes, breath, head anticipation and fingers that agree with the body. Decorative cloth motion cannot compensate for a rigid torso or missing hand pose.

## Sword: grip, edge, sweep, release, consequence

1. **Define the object:** handle grip anchor, guard, blade spine, cutting edge, tip, length, thickness and approximate mass centre. Anchor the sword to the hand's full world transform. Draw fingers over the handle; neither guard nor blade should intersect the palm incorrectly. For two hands, solve the off-hand toward its grip point without stretching the arm.
2. **Pose the contact first:** target surface, blade edge at contact, wrist, elbow, shoulder, hips and support foot. Add anticipation and follow-through around that pose. Direction of force should pass through a coherent body chain. Do not make the slash drawing travel somewhere the weapon never goes.
3. **Distinguish cut and thrust:** a thrust advances the tip; a cut carries the cutting edge through a target along an arc. Use the action the story actually depicts. If the story requires severing a neck, show the edge crossing that neck, split/reveal the appropriate pieces at the crossing, and give both pieces an aftermath. A timed opacity fade after a tip approaches a glowing centre is a magical defeat, not demonstrated cutting geometry.
4. **Check a swept blade, not one still tip:** transform blade segments at subframes between adjacent delivery frames. Test against the moving target's collider/silhouette. Broad-phase bounding boxes may narrow the search. A sampled sweep needs a resolution bound: maximum motion per sample should be smaller than a fraction of the smallest relevant collision radius. Fast angular motion needs more samples. The included `sweepBlade()` is explicitly approximate; it does not certify arbitrary thin geometry.
5. **Drive the event once:** first valid directed contact triggers target reaction, material impact sound, deformation/splinter/ink response, and a limited camera impulse. An intentional hit-stop may freeze the pose for a few frames, but all affected layers and audio policy must agree. Show the recovery/settling after the impact.
6. **Detach cleanly:** evaluate world position, angle, linear velocity and angular velocity at the release instant. Inherit the hand motion, then add a documented impact impulse if the blow knocks the weapon away. Do not reset angle or move the sword onto an unrelated parabola. Exactly one owner is active: hand, flight or floor.
7. **Collide the whole prop:** test tip, guard and handle, including rotation. A sword can strike tip-first and pivot; clamping only its handle's `y` leaves the blade through the ground. Apply a purposeful bounce/rock/slide and friction, or deliberately land with a hard impact and a short visible settle. Keep it on the same floor position until pickup.
8. **Pickup:** fingers reach the handle, grip closes, weight transfers to the arm, then the prop leaves the ground. Bind ownership at the shared grip event, not on the first frame of a close-up. A cut is allowed to compress time; it must retain orientation, hand, blade direction and believable recovery state.

The helper `localToWorld()` matches the old Canvas hierarchy and handles facing. `anchorVelocity()` supplies a finite-difference derivative for smooth paths. At a cut use a one-sided/analytic derivative; differentiating across two shots invents an enormous velocity. `ballistic()` is exact only for constant gravity without drag and before collision.

## Petals, flowers, leaves and cloth

Choose what is moving. A detached petal is light and broad; a whole flower with stem has a different mass distribution; a falling sword should never share the same float curve.

For a petal use gravity, drag relative to a coherent wind field, slowly varying flutter torque, and a rotated silhouette with projected-area changes. Its upward flutter can be local while its long-term motion descends. At contact, use relevant extremities or a conservative radius, reduce angular/linear energy, allow a small slide, then settle. A leaf can lift again only if a sufficiently strong gust explains it. Do not loop an offscreen reset through a visible action shot, or make petals cross a floor forever with a sine-wave `y`.

`bakePetal()` provides a small deterministic approximation using fixed-step integration, drag, flutter and conservative floor contact. Bake from the same initial state and sample the cached trajectory. It is not aerodynamic simulation. For a hero flower or near-camera landing, replace its circle collider with oriented vertices and art-direct the final contact pose. Test that the geometry and shadow touch together.

Cloth/hair roots are pinned to the transformed body. Secondary points use length constraints, damping and the same world wind. Simulate/bake them or author coherent curves. A periodic wave may work for a distant sleeve; it should not pass through a hand or keep oscillating unchanged after a sudden turn. Strong directional acceleration first moves the body, then trailing fabric follows. Keep self-intersection and hidden-area coverage under review.

## Wind, fog and material-specific movement

Use one world wind field with low-frequency gusts, plus small seeded local variation. Distant mist, nearer leaves and clothing may respond differently because of mass/drag; they should not imply contradictory wind directions without a reason. Separate world motion from camera motion.

Fog needs layers: far thin haze behind silhouettes; middle banks that occasionally occlude lower body/world features; near wisps with larger apparent motion and lower detail. Each layer has depth, scale, density, drift, dissipation and a mask/coverage bound. Avoid one repeated Bézier stripe at several heights. Plan a readable interval for required action or consequence. Mist specifically retains substantial fog and soft focus; validate underlying anatomy/contact in a fog-disabled diagnostic pass, then restore the final dense atmosphere and test audience readability. Temporary concealment is deliberate, not permission for a missing attack.

Keep grain/texture registered to its object unless deliberate pigment movement is the subject. Ink spreading changes the edge, local opacity and wet/dry boundary over time. A static rough outline plus uniform translation does not demonstrate ink flow. Sketch line boil should update at an intentional drawing cadence with controlled registration; full-frame random noise creates flicker. Flow should reveal or transform brush mass along coherent stroke direction and preserve identity/continuity at intermediate frames.

These are implementation principles, not claims about a specific source video's original software. The individual reference-derived guides must decide how much atmospheric motion and material change is appropriate.

## Camera, speed and editing

Start with the focal action, then plan camera. Give each shot a subject, intended change of scale, start/end composition, duration and motivated cut. An establishing wide shot, a restrained push toward a reaction, a follow on a committed movement, a contact insert and a held aftermath serve different purposes. Avoid the same gentle push-in applied to every style.

Keep camera motion smooth within a shot using continuous velocity/acceleration unless a deliberate handheld impact calls for a discontinuity. Use distance and duration to choose speed. A dramatic acceleration is a directed curve, not a universal spring. Record zoom as actual image/world scale; ensure sufficient asset resolution and overscan at the largest crop. Camera and background perspective/parallax must agree.

For a lateral fight maintain screen direction and the line of action. If crossing it, establish the new geography first. Preserve entrances/exits, gaze, sword hand, light direction and prop state across cuts. A close-up should reveal useful information; do not use an extreme jump crop solely to hide a broken rig.

Use brief impact shake with decay and explicit amplitude. Check its frame edges and focal visibility. Shot holds and silence are cinematic tools; constant zoom, constant shake or constant particle motion is not a quality requirement. Add/extend duration to let emotion, preparation, contact and outcome register. Do not solve a dense story by accelerating every layer or cutting narration.

## Distinct motion treatments: shared constraints, separate direction

Use [animation-categories.md](animation-categories.md) and the selected individual guide as the authority for motion identity and its representative proof. The former generic per-style test table is superseded: a walk/strike test cannot establish Flow paint performance, Mist fog staging, Grain material behavior or Scenic dimensional acting. Choose mechanics required by the actual story, verify their real geometry, and separately prove the defining category behavior. Wash/Print/Noir may deliberately share physical mechanics while directing their performance, material and shots individually.

## Deterministic runtime and seeking

Use one master timebase for the film. Render `stateAt(frame)` or a pure function of seconds; cache seeded textures and baked dynamic trajectories. Repeatedly seeking to the same frame must produce the same state, even after visiting the ending first. Fixed-step simulation by itself is insufficient if preview starts from whatever state was last on screen.

Interpolate cached dynamics for display without reintegrating from playback state. Store event outcomes in deterministic time-derived state; after `deathTime`, no idle head motion or reappearance occurs. Audio schedules must be cancelled/rebuilt on seek/pause/replay. Captions follow the actual final narration take, not guessed text duration.

The review player should expose a frame step, timecode and optional debug overlay showing foot anchors, bones, grip, blade segment, colliders, contact id, wind vectors and camera bounds. Export without overlays. The debug geometry and visible geometry must use the same transforms.

## Review that detects actual defects

### A. Geometry and timing checks

Check real rendered transforms at final scale and facing, not only a helper in isolation. Recommended diagnostic tolerances are starting points: a planted foot drifting under roughly one delivery pixel across stance; near-zero grip error; invariant bone lengths within numerical tolerance; collisions within a frame at the chosen frame rate. Adapt only with an explicit stylization reason. A numeric pass is necessary for its narrow claim, not sufficient for perceived quality.

Test seeking at multiple orders including backward; compare selected frame states/pixels using deterministic assets. Assert all event consequences persist. Compare words/caption counts with the complete approved script. Verify final duration from the actual audio and export, not its player label.

### B. Consecutive frames, not only contact sheets

For each major contact/release/landing/pose change, extract at least frames `n-6, n-3, n-2, n-1, n, n+1, n+2, n+3, n+6, n+12` where `n` is the observed event frame. At24fps Light/Dark output, adjacent frames are about41.7ms apart and paired character states about83.3ms apart. At30fps Original output, adjacent frames are about33.3ms apart; inspect its actual variable drawing holds and derived motion. Inspect in order with frame numbers visible. Include both sides of cuts. A ten-image sheet sampled seconds apart will miss foot slip, duplicate props, premature reactions and one-frame popping.

For the most important action, also watch its 2–5-second crop at normal speed, then half speed. Frame checks answer where contact occurs; normal speed answers whether the action reads and has weight. Do both. Check the finished texture/lighting version and a clean silhouette/debug version.

Ask concrete questions: Does the hand close before the prop leaves? Does the cutting edge cross the intended target? Is a foot fixed while supporting weight? Does a petal descend then contact, or merely drift forever? Is fog in front of the correct layer? Can the viewer see the decisive change? If uncertain, revise staging rather than covering it with a flash.

### C. Whole-film and cross-style review

Watch each final export start-to-end in Chrome with its own mix and captions; do not infer seven passes from one shared renderer. Verify full script, complete causal story, animation style, edit rhythm, music/effect timing and ending hold. Watch once without captions and once with audio muted for visual comprehension where appropriate. Listen to the whole encoded mix for intelligibility and texture, then meter its loudness/peaks. Meters do not replace listening.

When producing a style comparison, compare the requested treatments on the same narrative beat. Record how each treatment differs in body animation, environment, camera, transition and sound—not just its colours. A failed style distinction requires direction changes before release, even if the underlying player/export tests pass.

After source, timing, rig, audio or camera changes, regenerate affected exports and evidence. Record hashes of the reviewed files. Do not reuse a previous revision's pass label.

### D. Honest release record

Keep `REVIEW.md` with performed checks, frames/clips reviewed, actual defects/fixes, source/export hashes and unresolved limits. Use `draft` while material motion/story defects or required review modalities remain. Never write “no errors,” “perfect physics,” or “fully reviewed audio” based on assertions/encoding alone. The target is to find and remove visible defects; an absolute guarantee is not a valid engineering claim.

## Included probes and what they prove

Run from the Sumi skill root:

```sh
node assets/motion-core/test-motion-core.mjs
```

For an initialized project, run `node motion-tools/test-motion-core.mjs` from that project root. The earlier-film audit is project-specific research and is not a bundled runtime dependency.

The tests exercise world-space stance at multiple character scales; full anchor transforms; two-link lengths and explicit reach failure; continuous release position/velocity before gravity diverges; a floor-time solve; a sampled fast blade crossing; and repeatable petal baking/settling. They do **not** test a finished body rig, production render, fabric collision, animation appeal, storytelling, source-reference fidelity, audio or camera composition. Integrating these helpers into a film still requires the full shot and playback reviews above.
