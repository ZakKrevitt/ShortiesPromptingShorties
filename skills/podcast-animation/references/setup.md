# First-run setup

Work from a local checkout or an installed skill. Do not require the author’s development environment. No OpenShorts deployment, login, database, private plugin, or separate image-provider key is necessary.

## Discover what already works

Run `python3 scripts/doctor.py` from the skill folder. It checks Python, FFmpeg/ffprobe, optional packages and key presence without reading the key aloud or contacting a paid endpoint. A connected fal integration can be used without a local key; the doctor cannot verify a chat connector. Inspect its model-discovery tools separately.

Install missing local tools only within the user’s authorized setup scope. Prefer an isolated Python environment for optional dependencies:

```sh
python3 -m venv .venv
```

Use that environment’s Python (`.venv/bin/python` on macOS/Linux or `.venv/Scripts/python.exe` on Windows) to install `fal-client` for direct API/media uploads. Install `faster-whisper` only if local transcription is needed. It downloads model weights on first use; explain that before a large download. FFmpeg and ffprobe are separate executables installed with the operating system’s normal package manager. Do not silently run privileged installers.

For an already provided transcript, local Whisper is unnecessary. For a remote episode, prefer an accessible official download or ask for a file if retrieval is blocked. `yt-dlp` is optional for supported accessible sources; it does not grant permission to bypass login, DRM, CAPTCHA or platform restrictions.

## Configure the user's own account

Guide the user to [fal keys](https://fal.ai/dashboard/keys). They need their own account and sufficient balance. Do not create keys or purchase credit on their behalf unless separately authorized.

Use a connected fal integration, an existing `FAL_KEY` supplied by their secret manager, or let the user run this in their own interactive terminal:

```sh
python3 scripts/configure.py
```

The hidden prompt writes `~/.config/podcast-animation/fal.json` with restrictive permissions, outside the checkout and installed skill. It is a plaintext local secret, not an encrypted vault; a secret manager is preferable on a shared machine. `FAL_KEY` in the process environment takes precedence. Windows ACLs determine access beyond the basic file mode.

Never request the value through chat, display it, include it in a shell command, add it to examples, or load someone else’s deployment environment to obtain a key. Do not copy credentials from another project. Provider payloads must not contain API keys; optional model-specific BYOK fields are unnecessary here.

The configure and doctor commands are local-only. A successful presence check does not establish key validity, model access or provider balance. Use the user’s connected account and current provider tools/docs to establish those before paid work. Keep validation errors sanitized.

## Create a project workspace

Choose a new folder outside this skill repo, for example `~/Videos/PodcastAnimation/<clip-name>/`, or use the user’s requested location. Keep input files, private transcripts, shot plans, generated media and job records there. The final delivery folder is separate from private working files.

Ask for the episode, desired style, target length/framing, caption preference, languages and budget only when missing. Default to source-language-only output until translations are requested. Do not assume the languages or timestamps from a previous project apply to this one.
