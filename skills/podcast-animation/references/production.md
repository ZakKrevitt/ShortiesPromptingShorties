# Clip selection, direction and animation

## Select an anecdote

Read the timed transcript around each candidate, not just its punchline. A useful clip has a setup, an action that can be shown, and an ending that lands without the next sentence. Identify pronouns, people, locations and ambiguous nouns from context: for example, “bills” may mean legislation rather than restaurant receipts.

With a local file and no transcript, `scripts/transcribe.py input.mp4 transcript.json --language en` produces timed segments and words using optional local faster-whisper. Omit the language for detection. Review source frames and audio; ASR is evidence, not ground truth. It may mishear names, translate idioms literally, or place a final word before the sound actually ends.

Offer roughly three candidates, each with start/end, duration, a short faithful transcript excerpt, visual beats and why it stands alone. Keep natural speech pace. Do not stretch narration to hit an arbitrary duration. If the user delegates selection, choose and state the selection rather than asking again.

## Establish a cast and visual language

Inspect clear source frames for each speaker and capture reference crops. Determine the speaking host from footage/audio; screen position, famous appearance and transcript order are not reliable substitutes. Record names or stable labels, wardrobe, hair, glasses, facial hair, microphones and left/right position. Distinguish storyteller from characters inside the anecdote.

Ask for a style description or references before picking one for the user. Generate the style reference through a fal image endpoint. For claymation, make skin, eyes, hair, fabric and props read as sculpted plasticine with handmade surface detail. Reject photographic faces pasted into clay bodies. A public performer may be out of costume in the episode; the actual footage anchors likeness.

## Plan before generating shots

Save a shot table with output times, source-audio times, place, visible characters, speaker, initial state, action, required ending state and reference paths. Include a concise reason for each shot. Do not request or store private chain-of-thought.

Use hard cuts when location changes. Keep story characters silent during offscreen narration. If a user wants a story character to act out a quoted line, isolate that exact quote and animate the mouth only during it; preserve the surrounding body action and close the mouth outside the quote.

The first reference frame shows the setup, not the completed payoff: intact wall before a collision, object before it falls, doorway before a character enters. Specify direction and blocking explicitly: which side a character starts on, where they move and who stops them. Describe physical prop contact and hand orientation when the joke depends on them.

A useful prompt names who acts, who listens, what changes and the deadline for the action. Example: “The glasses-wearing host on the left speaks; the bald host on the right listens with closed lips. Keep the accepted clay material and wardrobe. Finish this gesture by the end of the supplied quote.”

## Generate and join

Read `fal.md` for discovery, schema checks and durable requests. Send only the original audio span belonging to that shot, padded with silence if required by the chosen endpoint. Keep padding out of the finished film. Use approved keyframes and accepted videos as identity references where supported.

To continue action, extract the frame at the actual accepted edit boundary. Carry it into the next shot with an explicit state description: character pose, position, clothes, held objects, damage/debris, lighting and camera. The next chunk must not repeat the same setup or reset a broken prop. A boundary frame may hide the face, so also include a clear identity reference.

Trim to usable action before smoothing a join. Prefer matching poses and motion to a long dissolve. Short motion interpolation can help, but inspect for doubled limbs, ghosting and prop deformation. A camera zoom on a still does not meet a request for character animation.

Use one continuous original recording for the source-language assembly, discarding generation audio. Preserve valid existing shots and repair only a failed criterion within the approved budget. For a model refusal, report the actual status without inventing the reason or disguising a prohibited request; offer a materially different creative option where appropriate.

## Review independently

Check correct speaker, host likeness, style, literal story action, prop physics, hands, direction of travel, camera continuity, timing and the entire ending. Review both sides of each join at normal speed and in frame sequences. A completed job is not a quality verdict. Keep approximate lip sync explicit.

Follow the requested caption treatment. Clean social-media exports can omit burned-in captions; captions added later by the user are a delivery choice. If subtitles are requested, derive them from the real speech, correct ASR errors, and apply them once after assembly.
