# Unit 09: happy - Completion Context

## What Was Implemented

`src/09/chatbot.py`: the unit 08 self-check loop re-skinned for an always-happy
persona, with an `is_happy` classifier and a generation prompt that permits quoting
happy song lyrics.

## Key Decisions

- Pulled the generation instruction into a `GENERATE_PROMPT` constant so the first
  attempt and every retry use identical wording.
- Reused the strict-classifier + tolerant-parse approach from unit 08 unchanged.

## Deviations from Plan

None.

## Files Modified

- `src/09/chatbot.py`

## Integration Notes

Demonstrates that the self-evaluation loop is a general pattern, not a one-off — only
the persona and the check change.

## Lessons Learned

Once the generate-judge-retry shape is right, swapping the persona is trivial, which
is a good point to make about agent design.
