# Ink art and choreography

Current routing: apply [animation-categories.md](animation-categories.md) and the selected style guide first. These mechanics are implementation options, not complete category proofs. Existing lab clips do not certify Bloom Flow, dense Mist, TV-like Grain, Wash-family Print/Noir or Scenic 2D/3D acting.


This is the preserved **Wash** foundation. A selected [variation](variations.md) may deliberately change palette, contour, texture and compositing. Apply its art direction while retaining the shared principles of clear action, stable materials, coherent contacts and visible consequences.

## Compose an ink world

Treat the paper as a persistent surface. Keep its fibers and grain stable as objects move; surface grain may stay in screen space while pigment texture follows painted forms. Use broad pale washes for distant depth, denser midground strokes, and sharply defined dark accents at the focal action. Preserve quiet areas. Do not apply the same contrast/noise everywhere.

Use expressive variable-width strokes and broken dry-brush edges. Build irregularity from seeded points or cached masks, not fresh frame noise. For ink bleed, use bounded layered dilation/soft edges with local opacity evolution. Preserve a legible solid silhouette inside the wash. Bleed should grow and settle; it must not make a face or weapon wobble randomly.

Use a stable palette with one accent only when it conveys meaning: a scarf, blossom, lantern or other recurring anchor. A scene need not contain red simply because the samurai example did. Do not use saturated UI gradients, glossy shading or generic particle showers to signal cinematic quality.

## Match method to shot

| Shot need | Useful implementation | Required inspection |
|---|---|---|
| Wide landscape and travel | Separate painted planes + articulated silhouette | Ground plane, gait, parallax and frame-edge coverage |
| Emotional close-up | Detailed portrait/pose with controlled eye/head/breath motion | Identity, anatomy, tiny motion rather than whole-head distortion |
| Gripping, fighting, planting | Separate props + arm/body rig or matched action poses | Grip, contact point, handoff and visible consequence |
| Flowing cloth/branches | Constrained chain or designed curve deformation | Fixed roots, length and world-space forces |
| Ink transformation/dissolve | Stable silhouette mask + seeded particles/washes | Opacity inherited by every child and no lingering duplicate |
| Fine repeatable graphic | SVG/Canvas path | Strokes/edges remain consistent through zoom/export |

A wide silhouette can tolerate fewer details than a close-up. Invest detail where the camera and emotion need it. Use cropped close-ups and motivated cuts to simplify difficult transitions, but never hide a missing decisive action behind a flash.

## Asset directions

Background: describe terrain, setting, period, ink density and reserved staging space. Request an empty action area, useful overscan and no character/prop duplicates. Foreground branches may be separate if they need parallax or occlusion.

Character: establish proportions, costume, motif and screen direction in one reference. Request distinct poses only when needed: walk contact/pass, anticipation, attack contact, recoil, grounded recovery, final gesture. Independently moving parts need overlap near pivots to prevent gaps. Keep transparent image bounds generous enough for weapons, fingers and cloth.

Props: isolate the sword, stake, lantern or other interactive item. Specify whether it is being held, airborne, grounded or attached in each shot. Use alternate empty-hand/costume assets when a prop is removed. Reject anatomy or identity errors before building motion around them.

Example asset direction, adapted to the actual story: “Isolated ink-wash figure in the attached reference's costume, kneeling with open empty hands near the ground, full silhouette in frame, expressive charcoal strokes and sparse grey wash, no sword or scarf, no text or environment, transparent background.” Set the tool's transparency option as well.

## Staging and action

Establish geography before the threat crosses it. Preserve screen direction across cuts unless a neutral view or visible camera move reorients the viewer. Keep the threatened object visible long enough to matter emotionally. A planted sword, repaired branch or returned object can resolve the story more strongly than a final slogan.

Build an action around these states, adapting timing to mood and narration:

1. Intention: gaze, body orientation or hand movement names the target.
2. Preparation: weight shifts against the coming movement.
3. Commitment: body accelerates and the weapon/prop follows its attachment.
4. Contact: the exact world-space positions coincide; the target reacts.
5. Follow-through: momentum continues, then dissipates through recovery or fall.
6. Consequence: the changed state persists and the next shot respects it.

Use the constraints in the production standard rather than relying on linear translation and a camera shake. For a jump, move the body's center on a ballistic arc and blend an airborne pose. On landing, compress then recover. For a tumble, rotate around a plausible pelvis/center of mass and evaluate silhouette-ground contact. Don't hinge the entire figure around a toe.

For an expressive tree, roots stay anchored while branch angles respond to wind. The blossom should move with its branch until it detaches; then it follows its own seeded wind/drag trajectory. For scarf tying, the cloth root changes ownership only at the shown handoff, and the ending tie stays at the trunk/stake contact.

## Camera and finish

Vary framing by purpose: establish location, follow an approach, isolate the moment of recognition, widen for consequence. Do not make every shot the same slow push. Keep foreground parallax proportional to depth and leave enough painted overscan. Use a cut when it communicates more clearly than a decorative transition.

Ink wipes and brief blooms should connect shots or actions, not obscure every change. Review their middle frames for doubled faces/weapons and accidental white gaps. Keep impact shake short and decaying, with a stable aftermath for the viewer to understand what changed.

Detailed backgrounds, purposeful weather, cloth and ink can enrich the world. They remain subordinate to the main gesture and readable captions. The final image should hold long enough to complete the emotional release.
