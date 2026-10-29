# Assembly manifest

Use `scripts/assemble.py manifest.json output.mp4 --ffmpeg /path/to/ffmpeg`. The helper assembles local animated shots over a single original source-audio span; it makes no generation calls and refuses to overwrite an output.

Paths are relative to the manifest. Each shot selects `start` through `end` from generated footage and fits it to `duration` in the edit. Use retiming only after inspecting motion and speech. Durations must sum to the intended source range. The `source` is normally the already extracted podcast excerpt; `audio_start` is seconds within it.

```json
{
  "source": "podcast-excerpt.mp4",
  "audio_start": 0,
  "width": 720,
  "height": 1280,
  "fps": 24,
  "shots": [
    {"path": "host.mp4", "start": 0, "end": 4, "duration": 4},
    {"path": "story.mp4", "start": 0, "end": 6, "duration": 6}
  ]
}
```

Optional `captions` points to an ASS subtitle file. Omit it for a clean export; do not add captions against the user's delivery choice. If using captions, check the FFmpeg build supports the ASS filter and review the rendered text.

The helper outputs H.264/AAC and a `.probe.json`. It preserves original speech content, but re-encodes audio; encoded audio bytes will change. Inspect the speaker, likeness, continuity and full ending before considering the result ready for dubbing. Use the finalizer for optional tail muting and language-folder delivery.
