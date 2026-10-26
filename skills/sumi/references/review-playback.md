# Visible playback and short-proof fallback

Use the supplied loopback range-capable delivery server. Confirm200full-file
responses,206partial responses/seeking and byte-matching downloads. A plain
temporary HTTP server that ignores Range can break playback even when the file
decodes. Do not stop an unrelated process to reuse its port.

Inspect the actual picture while it plays: opening, intermediate times, joins
and near the ending. Check pause/resume/seek/replay and fullscreen where
available. For a film, listen with sound on to speech, SFX/music balance and
timing. A poster, readyState, a moving progress bar or an ended timer does not
prove that the video stayed visible. Recheck the user's selected browser after
a reported blank/dark playback problem; do not insist that a file hash disproves
the user's observation. Keep the original MP4 and earlier versions.

If native playback fails for a **short silent technical proof**, the optional
[preview helper](../scripts/make_motion_preview.py) creates an image-animation
comparison page from the existing encoded frames. It does not create new art,
alter the film engine or add drawings. The preview can be smaller than full HD;
the page labels its actual size and retains a byte-identical MP4 download.

```sh
python3 /absolute/path/to/sumi/scripts/make_motion_preview.py /project/proof.mp4 /project/proof-review --title "Environment proof" --before /project/unchanged-master.png
python3 /project/proof-review/serve.py --port 4260
```

The helper accepts an entire silent constant-rate24/30fps clip of at most10s,
refuses existing output folders and records source/output hashes, real counts,
dimensions and duration. If `--before` is absent, the control says First frame,
not unanimated artwork. It uses existing FFmpeg/ffprobe and Pillow with animated
WebP support; detect them and ask before any missing third-party installation.
No model, provider or paid generation is involved. Keep this optional helper
separate from the standard no-Pillow full-film dashboard route.

Check actual intermediate image states in the browser; an animation timer is
still not a visual review. Inspect compression/detail and scene movement at the
intended display size. Preserve the existing style clock and do not count these
extracted frames as new source drawings. A silent proof cannot demonstrate SFX,
narration or complete film quality. Never replace a narrated film with silent
WebP or use this fallback to label an unreviewed film ready.
