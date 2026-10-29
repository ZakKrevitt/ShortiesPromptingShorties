# fal-only generation

All generative images, animated shots and dubs use the operator’s own fal account. There is no author account, proxy, OpenShorts backend or other generation-provider dependency. Prefer the connected fal integration when available; otherwise use the official `fal-client` Python SDK or `@fal-ai/client` JavaScript SDK. This package deliberately does not fork those SDKs.

## Discover before calling

Search the current catalog, inspect the exact endpoint schema and price, and confirm account access. Model names and endpoint variants can change. Do not copy a connector-specific mode or parameter from a different provider.

These were documented candidates on 29 October 2026, not permanent defaults:

| Step | Candidate on fal | Inspect before use |
|---|---|---|
| Styled references / targeted still correction | `openai/gpt-image-2/edit` | Reference-image fields, output size and token/image pricing |
| New reference image | `openai/gpt-image-2` | Current schema and requested style |
| Animation / video repair / extension | `bytedance/seedance-2.5/us/reference-to-video` | `task`, images/video/audio inputs, duration, resolution and access |
| First/last-frame animation | `bytedance/seedance-2.5/us/image-to-video` | `image_url`, optional end frame and audio support |
| Translated voice and lip sync | `veed/dubbing` | Source/target languages, duration limit, current per-second rate |

The reference-to-video schema currently documents `reference`, `editing`, `extension` and `auto` tasks. Do not assume all variants accept the same fields. Select a different fal model only with a clear task-specific reason, and disclose any limitation that affects the approved shot.

## Credentials and uploads

Use the user’s connected fal account or `FAL_KEY`. The setup helper’s `settings.load_key()` can supply the key to a short-lived server-side Python process; never print it. Do not use optional provider-specific BYOK fields.

Use `fal_client.upload_file(...)`, `fal.storage.upload(...)` or the connected upload tool to upload a local source/reference. Save the returned media URL privately with the asset record. Do not publish signed URLs or upload private inputs merely to make documentation examples work. Model inputs are JSON data, not shell commands.

## Submit once and resume

Quote costs before a paid pass and honor authorization already given. Record the endpoint, input hash, purpose, estimated cost and authorization in a private job record before submission. Persist the returned request ID and queue URLs immediately. Generation billing and output quality remain provider-controlled; a local estimate is not a provider spending cap.

For long jobs, use the asynchronous queue rather than holding an interactive request. fal REST submissions use `POST https://queue.fal.run/<endpoint>` with `Authorization: Key <user credential>`. Use the status and response URLs returned by that submission. Nested endpoint suffixes do not necessarily belong in result URLs.

Poll with backoff and preserve the same request ID across reconnects. After a timeout or lost submit response, mark the outcome unknown and reconcile request history before another paid POST. Do not create a new job merely because polling failed. Distinguish a known terminal failure from an uncertain submission and do not assume a failure was refunded.

Download completed outputs into the project workspace and verify their media streams. Keep raw provider outputs separately from final edits. Stop paid retries when the approved budget is exhausted or a failure needs user input. Continue transcript, storyboard and local editing work that remains possible.

## Official sources

- [fal authentication](https://fal.ai/docs/documentation/model-apis/authentication/key-based)
- [Queue lifecycle and returned URLs](https://fal.ai/docs/documentation/model-apis/inference/queue)
- [GPT Image 2 edit](https://fal.ai/models/openai/gpt-image-2/edit)
- [Seedance 2.5 reference-to-video schema](https://fal.ai/models/bytedance/seedance-2.5/us/reference-to-video/api)
- [VEED dubbing schema](https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=veed/dubbing)
- [VEED model page](https://fal.ai/models/veed/dubbing)

These sources establish documented capability. The public skill’s tests exercise local helpers with synthetic media, not a paid end-to-end generation. Do not describe this package as a live-verified fal reproduction of any earlier clip.
