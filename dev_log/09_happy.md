# Unit 09: happy

## Objective

Show that the self-check pattern is reusable: the same generate-judge-retry loop with
a different persona — always happy, and allowed to quote happy song lyrics (`src/09`).

## Implementation

- `src/09/chatbot.py` — unit 08's structure with three changes:
  - `is_cynical` → `is_happy` (classifier now checks for happy/cheerful/positive).
  - A `GENERATE_PROMPT` asking for a very happy answer, permitting happy song lyrics,
    used identically on the first try and every retry.
  - Retry marker reads `<Not happy enough, calling chat again>`.
- `MAX_TRIES` and boolean parsing carry over from unit 08.

## AI Interactions

- Adapted the self-check loop to the happy persona and verified it produces happy
  answers (including quoting lyrics), exercising the retry path when early answers
  were not happy enough.

## Files Modified

- `src/09/chatbot.py`

## Status: Complete
