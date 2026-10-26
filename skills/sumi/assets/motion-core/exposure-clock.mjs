export function exposureClock(frame, outputFps = 24) {
  if (!Number.isInteger(frame) || frame < 0) throw new RangeError('frame must be a non-negative integer');
  if (!Number.isInteger(outputFps) || outputFps < 2 || outputFps % 2) throw new RangeError('outputFps must be a positive even integer');
  const exposure = Math.floor(frame / 2);
  return {frame, outputTime: frame / outputFps, exposure, characterFrame: exposure * 2, characterTime: exposure * 2 / outputFps};
}
