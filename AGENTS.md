# Working in this repository

This repository publishes the reusable skill at `skills/podcast-animation/SKILL.md`. Read it before operating the workflow. Read `README.md` for install and release boundaries.

- Keep all generative media calls on the user's own fal account. Do not introduce author-hosted infrastructure or another generation provider as a silent fallback.
- Never ask for keys in chat or commit credentials, cookies, session exports, user media, signed upload URLs or job records. Examples must be synthetic and credential-free.
- Installation and tests must not make paid API calls. Generations require the operator's actual authorization and budget.
- Keep provider schemas and prices discoverable through current official sources. Distinguish documentation support, local test coverage and live model quality.
- Preserve existing skills when installing. This public skill does not modify a user's other workflows.
- Run the standard-library tests before publication. Media processing must preserve the video stream when only audio-tail cleanup was requested.
