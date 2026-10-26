// Capture already-transformed geometry from the renderer. Does not invent joints,
// read pixels, solve physics, approve a review, or alter animation.
export function createPhysicsTrace({fps = 24, planSha256}) {
  if (!Number.isFinite(fps) || fps <= 0 || !/^[a-f0-9]{64}$/.test(planSha256))
    throw new TypeError('Positive fps and current plan SHA-256 required');
  const actions = new Map();
  return {
    record({action, character, frame, points, unresolved = []}) {
      if (typeof action !== 'string' || !action.trim() || typeof character !== 'string' ||
          !character.trim() || !Number.isInteger(frame) || frame < 0 ||
          !points || typeof points !== 'object' || Array.isArray(points) ||
          !Array.isArray(unresolved) || unresolved.some(x => typeof x !== 'string'))
        throw new TypeError('Invalid physics sample');
      const copy = {};
      for (const [name, p] of Object.entries(points)) {
        if (!name.trim() || !Array.isArray(p) || p.length !== 2 || !p.every(Number.isFinite))
          throw new TypeError('Finite transformed 2D points required');
        copy[name] = [...p];
      }
      if (!actions.has(action)) actions.set(action, new Map());
      const samples = actions.get(action);
      if (samples.has(frame)) throw new Error('Duplicate action/frame');
      samples.set(frame, {frame, character, points: copy, unresolved: [...unresolved]});
    },
    toJSON() {
      return JSON.parse(JSON.stringify({schema: 1, fps, coordinates: 'world-design-pixels',
        plan_sha256: planSha256,
        actions: Object.fromEntries([...actions].map(([id, rows]) =>
          [id, [...rows.values()].sort((a, b) => a.frame - b.frame)]))}));
    }
  };
}
