# Interview question bank

Prompts to draw from during the interview. Don't ask them all — pick the ones that matter for this feature and follow the threads that open up. Prefer AskUserQuestion with concrete options.

## Technical implementation
- Where should this live — which module/package/directory owns it?
- Which existing files or interfaces does it touch or extend?
- What are the exact inputs and outputs (types, shapes, formats)?
- Any new dependencies, services, or infrastructure?
- How does it integrate with what's already there — does it replace, wrap, or sit beside existing code?
- Sync or async? Any performance or scale constraints that shape the design?

## UI/UX
- Walk me through the user's flow, step by step.
- What are the loading, empty, and error states?
- What happens on the unhappy path — bad input, timeout, no permission?
- Any accessibility, responsiveness, or localization requirements?

## Edge cases
- Empty / null / missing input?
- Concurrency — two of these at once? Race conditions?
- Failure and retry — what's idempotent, what isn't?
- Limits — size, rate, pagination, timeouts?
- Auth / permission boundaries — who can and can't do this?
- Existing data — does anything need migrating or backfilling?

## Tradeoffs (spend the most time here)
- Where is there more than one reasonable way to do this?
- Simplicity now vs. flexibility later — which way do you lean, and why?
- Build vs. reuse an existing library/service?
- What are you willing to NOT handle in v1?
- If you had to cut this in half, what stays?

## Closing checks
- What would make you call this "done"?
- How should we verify it end to end?
- Anything I haven't asked that I should have?
