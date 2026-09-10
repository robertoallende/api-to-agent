# Unit 04: loop - Completion Context

## What Was Implemented

`src/04/chatbot.py`: an interactive read-eval-print loop over the rule-based logic,
with a `/quit` exit and a `> ` prompt.

## Key Decisions

- Inlined the response logic and dropped both the function and the `__main__` guard,
  so the whole program reads as a single top-to-bottom loop — chosen deliberately for
  live explanation.
- `/quit` is checked before the response branches so it never gets a chatbot reply.

## Deviations from Plan

The logic was moved fully into the loop (rather than kept as a `chat()` function) at
the developer's request, to avoid explaining function calls during the talk.

## Files Modified

- `src/04/chatbot.py`

## Integration Notes

Establishes the `> ` / `/quit` loop shape reused by every later chatbot unit (05–12),
so the diffs between units stay focused on the response mechanism.

## Lessons Learned

Locking in a stable loop shape early keeps subsequent units to a minimal, teachable
diff.
