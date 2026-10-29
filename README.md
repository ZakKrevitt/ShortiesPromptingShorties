# Podcast Animation

Turn a podcast story into an animated short, then dub it into the languages you choose. A reusable Codex skill by ShortiesPromptingShorties, built around fal.

Give Codex a podcast file or an accessible episode link. It helps find a self-contained anecdote, asks about visual style and languages, preserves the real speakers and source audio, generates the animation, and delivers the original plus translated versions in one folder.

## Give this to Codex

Copy this message into Codex:

```text
Install the Podcast Animation skill from
https://github.com/ZakKrevitt/ShortiesPromptingShorties
using the skill at skills/podcast-animation.
Read its setup instructions, help me configure my own fal account without
putting my key in chat, then ask for my podcast, visual style and languages.
Show me clip candidates and a cost estimate before generating anything.
```

Codex can use its skill installer with `skills/podcast-animation`, or clone this repository and run:

```sh
python3 install.py
```

The installer copies only the skill into `~/.codex/skills/podcast-animation` (or `$CODEX_HOME/skills/podcast-animation`). It does not overwrite an existing skill, read keys, install packages or generate media. The skill is available on your next Codex turn. Start with:

```text
Use $podcast-animation to help me animate a podcast anecdote.
```

## What happens

1. Set up your own fal access and local editing tools.
2. Provide a podcast file or accessible link, or select a timestamp yourself.
3. Review a small shortlist of story-driven clips with start/end times and context.
4. Describe the look: claymation, paper cutout, illustrated, cinematic, or your own reference. Choose languages, framing, length and caption preference.
5. Review the storyboard, styled characters and estimated spend. Codex generates within your approved scope and budget.
6. Review the source-language animation before translation when requested. Characters, speaker ownership, story action and joins are checked separately.
7. Dub through VEED on fal. Check the end of every version and mute any stray next-sentence fragment while keeping the whole video.
8. Receive a folder containing the source-language original and every requested dub, plus an optional ZIP.

## One generation account

All paid image, animation and dubbing requests use **your fal account**. Candidate models include GPT Image 2 on fal for reference editing, Seedance 2.5 on fal for animation, and VEED on fal for translation. Endpoint availability, parameters and prices are checked at runtime. Optional BYOK fields for other providers are not needed by this workflow.

Codex handles planning and review. FFmpeg handles local editing, and optional local Whisper handles transcription. A fal-only generation route does not mean every local editing operation is a fal call. No OpenShorts account or author-hosted service is required.

## Setup and your key

You need Codex with local file/terminal tools, Python 3.10+, FFmpeg and ffprobe, and a funded fal account. Optional dependencies are documented in the [setup guide](skills/podcast-animation/references/setup.md).

**Do not paste an API key into chat, a prompt, a source file or a GitHub issue.** Use a connected fal integration belonging to you, a secret manager that supplies `FAL_KEY`, or the local hidden-input configurator:

```sh
python3 skills/podcast-animation/scripts/configure.py
python3 skills/podcast-animation/scripts/doctor.py
```

The configurator stores your key outside the repository in a private local configuration file. The doctor reports only whether credentials exist. No API keys, user footage, cookies, completed jobs or paid example renders are included here.

## What is implemented and what is not promised

This is an agent-operated production skill, not a one-click rendering service. It includes install/setup checks, a local transcript helper, an assembly helper, and a tested final-delivery helper. The skill uses connected fal tools or the official fal SDK for generation; it discovers current model schemas instead of maintaining a second provider SDK.

The public package has local fixture tests. The complete fal-only creative workflow has not been live-rendered as a release test. Model output still needs review; lip sync, character likeness and translations can require iterations. There is no promise of identical results across models or clips. Credentials and sufficient provider balance remain the user's responsibility.

[Workflow instructions](skills/podcast-animation/SKILL.md) · [fal routing](skills/podcast-animation/references/fal.md) · [Dubbing and delivery](skills/podcast-animation/references/dubbing-delivery.md)

## Development

```sh
python3 -m unittest discover -s tests -v
```

Media tests use synthetic footage and require FFmpeg/ffprobe. Tests never submit a paid generation or need an API key. MIT licensed.
