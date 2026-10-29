# Translate, clean endings and deliver

## Settle the original first

Use the latest reviewed source-language animation. Preserve its actual audio, framing and length. Remove an unwanted next-sentence fragment before uploading for dubbing so it cannot become translated speech. An edit requested after translation means checking which exports now use an outdated master; do not silently mix versions in the delivery folder.

When the user has asked to see the original before dubbing, show a playable file and wait for that review. Otherwise honor their existing authorization. Translate only the requested languages; adding another language is an additional paid job.

## VEED on fal

Inspect the current `veed/dubbing` schema and price. It currently accepts `video_url`, `source_language`, `target_language` and `keyterms`, returning `video.url`. It translates speech and adjusts visible lips where supported. It is not a script editor, and clay faces may retain approximate original mouth motion.

Set the known source language explicitly. Common target codes include `es`, `pt`, `zh`, `fr`, `de`, `hi`; these are examples, not a default batch. Explain Mandarin versus Cantonese when relevant (`zh` versus `yue`). The documented model does not provide regional dialect control; do not promise Brazilian Portuguese or a specific regional accent from a base language code.

Use keyterms for names and specialized terms, not hidden translation instructions. The 29 October 2026 schema allowed videos with speech up to 10 minutes long. Read the live limits and pricing rather than assuming that date's values are current.

Upload the master once where possible. Keep one durable job record per target language, with source hash, endpoint, request ID, price estimate and output. Resume polling accepted requests after a network error; do not pay for a duplicate. Retain raw provider output for comparison.

## Check every version

- Decode the full file; confirm picture, audio, dimensions, intended duration and caption treatment.
- Check the correct host still speaks and listeners have not acquired speech motion. Compare the same frames and action beats with the master.
- Listen to the voice and especially the ending. Use multilingual ASR to check language and story coverage when available. Transcripts and English back-translations can be wrong, so do not “repair” meaning solely from a dubious automatic translation.
- Check character names, ambiguous objects, the quote and the payoff in context. Note whether a native-language review was actually performed.
- Do not promise phoneme-perfect translated mouth animation, especially on stylized characters.

## Remove a dangling fragment without shortening the video

Inspect the last few seconds of the original and each dub separately. Find the end of the last intended complete phrase and the start of the unwanted next utterance. ASR word boundaries are only a starting point: confirm with the waveform and audio, including the end of a trailing vowel or consonant.

Choose a quiet gap after the complete phrase. A short fade (around 20 ms) ending at that cutoff avoids a click; audio after it becomes silent. Keep the video duration and every video packet unchanged. Do not trim the video, freeze its last frame, remove the punchline, or blindly mute a fixed number of milliseconds from every clip.

A provider can leave a source-language fragment in the background even when the translated sentence is complete. Recheck after dubbing even if the original was already clean. A version without a fragment needs no additional mute. Never reuse a prior clip's cutoff timestamp as a preset.

## Package the original and every language

Create a new named delivery folder in the user's requested location. Include the cleaned animated source-language original and every requested dub with clear language filenames. Include the unanimated horizontal source excerpt too when requested, clearly labeled as raw/source footage. Do not confuse it with the animated original. Keep drafts and provider originals elsewhere.

The portable helper takes a JSON manifest; paths are relative to the manifest. `original` is required. `versions` may be empty. `extras` can hold an explicitly requested raw source excerpt. Each `mute_from` is a measured time in that particular input file, or `null` to copy it unchanged. Inputs must already be final MP4s of the intended length.

```json
{
  "original": {
    "source": "animation-original.mp4",
    "filename": "01-English-original.mp4",
    "language": "en",
    "mute_from": null
  },
  "versions": [
    {
      "source": "dub-hindi.mp4",
      "filename": "02-Hindi.mp4",
      "language": "hi",
      "mute_from": null
    }
  ],
  "extras": []
}
```

Set a numeric `mute_from` only after finding the real cutoff. Then run:

```sh
python3 scripts/finalize_versions.py delivery.json /path/to/new-delivery-folder
```

Use `--ffmpeg /path/to/ffmpeg` if needed. Add `--zip` only if a ZIP is wanted. The helper refuses existing output destinations, preserves inputs, copies video streams, checks video hashes/durations, decodes the results and verifies the muted tail. It writes a verification manifest beside the folder, outside any optional ZIP. It cannot decide where a sentence ends; that editorial choice remains with the operator and agent.

Present the folder and playable files, count the included languages, describe ending cleanup and state remaining quality limitations. No upload to a social platform is implied by delivery.
