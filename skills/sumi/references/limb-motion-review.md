# Limb motion: review the drawing, not only the joints

Required for character animation in Sumi Original, Light and Dark. Apply during authorized production before full-film rendering, then inspect the relevant final export frames. Use the [portable physics gate](physics-gate.md) for numeric constraints and required evidence. Visual judgement remains an assistant/human review requirement, not an automated anatomy detector. Record unperformed checks as unverified. Never turn a completed checklist, source hash or paired-exposure timing pass into visual approval.

## Match the source to the action

Inventory each character/view and distinct action: idle, step/start/stop, turn, kneel/rise, reach/grip, strike/recoil, fall/land, as applicable. Include transitions between actions. A passed strike does not certify a walk; a good standing master does not certify a kneel. Shared mechanics can share evidence only when artwork, pose parameters, facing and support geometry match; check each final style's visibility/occlusion.

Use source-derived articulation only within the drawing's supported view and movement range. For an unsupported bend, foreshortening, torso rotation or grip, prepare a complete action pose and needed breakdowns. Do not force a standing cutout into every action. Count these drawings in the shot budget. Correct the pose or staging without deleting required story actions. No additional user approval is needed for technical corrections inside an approved direction.

## Inspect the whole movement

For each distinct action and entry/exit, retain an actual final-art full-body motion proof, a neutral fixed-camera diagnostic view and closely spaced frames. Include the supporting feet/knees and both hands even if the final shot is a close-up. The clean film may still use story-led close framing; the diagnostic view must reveal rather than hide defects.

At the selected output rate (Original 30fps, Light/Dark 24fps), inspect consecutive frames across the onset/transition/contact and successive two-frame exposures through the movement. Look especially at gait enabled/disabled, stride changes, knee-bend selection, pose replacement and prop attachment. Also play at normal speed; frame stepping alone cannot establish perceived motion. Record exact ranges and observations, not merely a playback-completed flag.

Check visible drawing and rendered transforms together:

- **Legs and weight:** anatomical side and near/far order; hip–knee–ankle bend; pelvis over a credible support; clear lift, swing, plant and transfer. Start/stop must blend through supported transition poses. Do not abruptly replace a wide stance with feet clustered at the root, reset gait from absolute x, or flip a knee's bend branch at a threshold. Fix the pose/view if the bend cannot be supported.
- **Feet:** inspect the actual boot/hoof/paw silhouette, heel, toe and sole. Author ankle/foot orientation and toe/heel roll where needed. A point labelled ankle+offset is not the shoe's contact surface. Do not leave the original boot orientation unchanged while the shin changes into an incompatible view. Use world-space stance anchors and check the actual transformed sole against the floor or object being stood on.
- **Reach and segments:** check upper and lower reach limits and both rendered segment endpoints. If IK clamps a target, the visible limb, hand/foot, prop and diagnostic geometry must use the same reachable result. Do not clamp the knee calculation but leave a distant ankle or rigid source segment elsewhere. Supply an appropriate pose if solving the target would produce an unnatural silhouette.
- **Hands and props:** inspect elbow–wrist–palm alignment, thumb side, finger closure and the handle inside the grip at anticipation, contact and recovery. Moving a wrist coordinate does not rotate or redraw its hand correctly. A rotating sword needs a compatible hand/wrist pose; a shield must remain plausibly strapped/held. Check overlaps and layer order, not just a grip distance.
- **Hierarchy and occlusion:** near/far limb order is pose/view-specific. Debug points must use the same complete transforms as visible pieces, including actor rotation, scale, camera and outer fall transforms. An untransformed rig return value is not screen-space evidence.

## Evidence and stop rule

In the project's review, include a row per distinct action/view with: character; action; frame range; source and mechanism hashes; full-body clip; consecutive-frame sheet; visible sole/grip overlay; observations; unresolved issues; correction and recheck status. Reuse the existing proof review file and adjacent-frame evidence fields where available. Do not duplicate approvals or invent completed checks.

Any visible wrong joint bend, folded/collapsed leg, unsupported weight transfer, sliding planted sole, disconnected hand, incompatible grip or unresolved silhouette overlap means that action is **not ready**. Repair and reprove it before the whole film. A user-requested unchanged historical film may be retained as a known-defective comparison, with its movement excluded from approved reusable examples.

If only a bounded comparison is authorized, label its defects and limits; do not use it as a certified motion baseline for later films. Automatic schema checks verify files, hashes and recorded observations, not whether the motion looks correct. This procedure reduces repeat failures; it cannot promise that future films will have zero errors.


Prefer the [whole-character action-sheet workflow](action-pose-sheets.md) when the drawing/rig does not support the requested action. Correct the source poses before motion, and retain all existing visual/contact review gates.
