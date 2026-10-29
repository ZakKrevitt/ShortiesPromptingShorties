---
name: podcast-animation
description: Turn a podcast anecdote into a story-faithful animated short using fal, with clip discovery, character and speaker continuity, optional VEED translations, clean audio endings, and a folder containing the original plus all requested languages. Use for podcast animation and its translation/export workflow.
---

# Podcast Animation

Guide the user from an episode to an animated anecdote and a complete delivery folder. Use the user's own fal account for all image generation, animation and dubbing. Local editing and transcription do not require another generation provider. This skill includes no paid account or source footage.

## Start with the person and the source

Read [setup](references/setup.md) on first use or if a dependency is missing. Do independent preparation while waiting for essential inputs. Ask only for information not already supplied, in short groups:

- Podcast file or accessible episode link; a preferred timestamp, or permission to find candidates.
- Visual style in their own words, optional visual references, target length/framing, and captions or a clean export.
- Source language and desired target languages, including whether they want no translations. Clarify ambiguous language/dialect choices only when consequential.
- A generation budget or authorization for a quoted first pass. Setup does not authorize spend.

When a podcast has not been supplied, ask for it. Do not invent a source. A public link is not a guarantee that it can be downloaded: use available official downloads or the operator's local file; do not bypass access controls. Keep source URL/title and time range as provenance. Rights decisions remain with the operator; do not manufacture rights attestations.

## Find a clip worth animating

Read [clip selection and production](references/production.md). Use supplied timed transcripts or transcribe the source, including surrounding context. Offer about three candidates with exact start/end, the actual hook and payoff, visual beats, and any context dependency. Favor a coherent mini-story over an isolated provocative line. Do not call a candidate viral or promise growth. Let the user select unless they have delegated selection.

Keep a private project folder for source, transcript, cast references, shot plan, provider inputs, job IDs, costs and review notes. Record user choices so a resumed session does not ask them again. These project records do not belong in the public skill repo.

## Produce with fal

Read [fal routing](references/fal.md) before generation. Inspect current endpoint schemas and quote costs; use a connected fal integration or the official SDK with the user's key. Respect a model or budget already selected. Do not replace fal with another provider without a new user request.

Establish host likeness and the chosen material in reference images before animating. Separate the visible speaker from offscreen narration. Only the actual host articulates in a studio shot; story characters remain silent unless the user deliberately assigns them a quoted line. Match literal objects and actions to the surrounding conversation.

Build short shots around story beats. For continuous action, extract a boundary frame from the accepted video and carry its physical state into the next shot. Hard-cut between different locations. Preserve usable footage and repair only failed criteria. The [production guide](references/production.md) covers continuity, props and quote-only mouth edits.

Keep original source-language speech for assembly. Do not synthesize a replacement for an available original recording. Dubbing is a separate, explicitly requested translation operation. Use `scripts/assemble.py` with the [assembly manifest](references/assembly.md); captions are optional and follow the user's intended delivery.

## Review, translate and deliver

Inspect speaker ownership, host likeness, style, story action, physical continuity, timing and the full ending. Successful encoding or a completed provider job does not establish creative quality. Record approximate lip sync honestly.

Before dubbing, settle the source-language master and remove any unwanted next-sentence fragment from its audio. Preserve a complete payoff and the full video length. If the user requested an original preview before translation, show it and wait for their review; otherwise use the existing authorization without inventing an extra approval gate. A later edit invalidates older exports as the current master.

Read [dubbing and delivery](references/dubbing-delivery.md) for VEED on fal, translation checks, word-specific ending cleanup and packaging. Translate only the requested languages. Inspect each returned version again: a dub may retain or reintroduce an offscreen source-language fragment.

Use `scripts/finalize_versions.py` to place the source-language original and every requested dub in one named folder, optionally with a ZIP. Cutoffs are measured per clip/version, never copied from an example. Video-only timing and frames must remain unchanged during audio-tail cleanup. Preserve private source files and provider originals separately.

Present the folder and playable results. State which versions are included, what was checked, remaining quality limitations, and the actual models/route used. The original is the animated source-language version unless the user also asks for the raw podcast excerpt. Never publish or post the media merely because it was exported.
