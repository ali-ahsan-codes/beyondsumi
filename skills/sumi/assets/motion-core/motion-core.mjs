// Deterministic geometric helpers. These are tools for directed animation,
// not a human-body, cloth, fluid, or rigid-body physics engine.
export const clamp = (n, a = 0, b = 1) => Math.max(a, Math.min(b, n));
export const lerp = (a, b, u) => a + (b - a) * u;
export const ease = u => { u = clamp(u); return u * u * (3 - 2 * u); };
export const length = p => Math.hypot(p[0], p[1]);
export const distance = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1]);

// World-space feet. travel is signed, world-space root travel; reverse walking
// needs an authored direction change. Keep origin/stride fixed within a walk.
export function gaitFoot({travel, origin = 0, scale = 1, stride = 74,
  offset = 0, stance = .62, lift = 24, ground = 585}) {
  if (!(scale > 0 && stride > 0 && stance > 0 && stance < 1))
    throw new RangeError('Invalid gait dimensions');
  const worldStride = stride * scale;
  const q = travel / worldStride + offset;
  const cycle = Math.floor(q), phase = q - cycle;
  const plant = origin + worldStride * (cycle - offset + stance / 2);
  const inStance = phase < stance;
  const u = clamp((phase - stance) / (1 - stance));
  const x = inStance ? plant : lerp(plant, plant + worldStride, ease(u));
  const y = ground - (inStance ? 0 : lift * scale * Math.sin(Math.PI * u));
  return {world: [x, y], local: [(x - origin - travel) / scale,
    (y - ground) / scale], phase, inStance, cycle};
}

// Returns the actual end, never a joint aimed at an unreachable target with
// an overlong second bone. Callers must reposition the root or change the pose
// when reachable=false. Clamping is diagnostic, not an acceptable hidden fix.
export function twoLink(root, target, l1, l2, bend = 1) {
  if (!(l1 > 0 && l2 > 0)) throw new RangeError('Positive bone lengths required');
  let dx = target[0] - root[0], dy = target[1] - root[1];
  const requested = Math.hypot(dx, dy), epsilon = 1e-6;
  if (requested < epsilon) { dx = 1; dy = 0; }
  const norm = Math.hypot(dx, dy), ux = dx / norm, uy = dy / norm;
  const lo = Math.abs(l1 - l2) + epsilon, hi = l1 + l2 - epsilon;
  const reach = clamp(requested, lo, hi);
  const along = (l1 * l1 - l2 * l2 + reach * reach) / (2 * reach);
  const height = Math.sqrt(Math.max(0, l1 * l1 - along * along));
  return {
    joint: [root[0] + ux * along - uy * height * bend,
      root[1] + uy * along + ux * height * bend],
    end: [root[0] + ux * reach, root[1] + uy * reach],
    reachable: requested >= lo && requested <= hi,
    error: Math.abs(requested - reach)
  };
}

// Matches Canvas translate -> scale(facing * scale, scale) -> rotate(angle).
// Return anchors through the full hierarchy, including mirrored characters.
export function localToWorld(point, {x, y, angle = 0, scale = 1, facing = 1}) {
  const c = Math.cos(angle), s = Math.sin(angle);
  return [x + facing * scale * (point[0] * c - point[1] * s),
    y + scale * (point[0] * s + point[1] * c)];
}
export function anchorVelocity(positionAt, t, h = 1 / 600) {
  // Use a one-sided or analytic derivative at an intentional cut.
  const before = positionAt(t - h), after = positionAt(t + h);
  return [(after[0] - before[0]) / (2 * h), (after[1] - before[1]) / (2 * h)];
}
export function ballistic(p0, v0, age, gravity = 900) {
  age = Math.max(0, age);
  return {position: [p0[0] + v0[0] * age,
    p0[1] + v0[1] * age + .5 * gravity * age * age],
  velocity: [v0[0], v0[1] + gravity * age]};
}
export function floorTime(y0, vy, ground, gravity = 900) {
  if (!(gravity > 0 && ground >= y0)) throw new RangeError('Invalid floor solve');
  return (-vy + Math.sqrt(vy * vy + 2 * gravity * (ground - y0))) / gravity;
}

export function pointSegmentDistance(point, a, b) {
  const dx = b[0] - a[0], dy = b[1] - a[1], d = dx * dx + dy * dy;
  const u = d ? clamp(((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / d) : 0;
  return distance(point, [a[0] + u * dx, a[1] + u * dy]);
}
export function bladeSegment(pose, length, guard = 12) {
  const dir = [Math.cos(pose.angle), Math.sin(pose.angle)];
  return [[pose.x + dir[0] * guard, pose.y + dir[1] * guard],
    [pose.x + dir[0] * length, pose.y + dir[1] * length]];
}

// Author unwrapped angles for intentional spins. Target may move; both poses
// are evaluated at subframes. Bounded subdivision is an approximate sweep,
// not exact continuous collision detection. Choose samples from maximum
// blade/target displacement; require <= radius/4 per sample and inspect.
export function sweepBlade({poseAt, targetAt, from, to, length: bladeLength,
  radius, guard = 12, samples = 64}) {
  if (!(to >= from && samples >= 1 && radius > 0)) throw new RangeError('Invalid sweep');
  let closest = {distance: Infinity, time: from};
  for (let i = 0; i <= samples; i++) {
    const time = lerp(from, to, i / samples);
    const [a, b] = bladeSegment(poseAt(time), bladeLength, guard);
    const d = pointSegmentDistance(targetAt(time), a, b);
    if (d < closest.distance) closest = {distance: d, time};
    if (d <= radius) return {hit: true, time, distance: d};
  }
  return {hit: false, ...closest};
}

// A deliberately small petal model. Bake once from t=0; never integrate from
// the last requested preview frame. Units: design pixels, seconds, radians.
// Radius is a conservative collision proxy; replace with oriented extrema
// for hero flowers whose exact silhouette/landing is visible in close-up.
export function bakePetal({duration, hz = 120, position, velocity = [0, 0],
  angle = 0, spin = 1, radius = 3, ground = 585, gravity = 80, drag = 2,
  phase = 0, restitution = .08, friction = .65,
  wind = t => [22 + 8 * Math.sin(t * .8), 0]}) {
  const dt = 1 / hz, samples = [];
  let [x, y] = position, [vx, vy] = velocity, theta = angle, omega = spin;
  let resting = false;
  for (let frame = 0; frame <= Math.ceil(duration * hz); frame++) {
    const t = frame * dt;
    samples.push({t, x, y, vx, vy, theta, omega, resting});
    if (resting) continue;
    const [wx, wy] = wind(t);
    const flutter = Math.sin(theta * 2 + phase);
    vx += ((wx - vx) * drag + 8 * flutter) * dt;
    vy += (gravity + (wy - vy) * drag) * dt;
    omega += ((wx - vx) * .035 + Math.sin(t * 5 + phase) * .6 - omega * .8) * dt;
    x += vx * dt; y += vy * dt; theta += omega * dt;
    if (y + radius >= ground) {
      y = ground - radius;
      vy = -Math.max(0, vy) * restitution;
      vx *= 1 - friction; omega *= 1 - friction;
      if (Math.abs(vy) < 3 && Math.abs(vx) < 3 && Math.abs(omega) < .25) {
        vx = vy = omega = 0; resting = true;
      }
    }
  }
  return {hz, duration, samples};
}
export function sampleBake(bake, t) {
  const p = clamp(t, 0, bake.duration) * bake.hz;
  const i = Math.min(Math.floor(p), bake.samples.length - 1);
  const a = bake.samples[i], b = bake.samples[Math.min(i + 1, bake.samples.length - 1)];
  const u = p - i;
  return Object.fromEntries(Object.keys(a).map(k => [k,
    typeof a[k] === 'number' ? lerp(a[k], b[k], u) : a[k]]));
}
