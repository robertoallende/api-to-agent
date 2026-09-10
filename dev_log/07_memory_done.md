# Unit 07: memory - Completion Context

## What Was Implemented

`src/07/chatbot.py`: conversation memory by concatenating the full history into each
prompt, so the model can reference earlier turns.

## Key Decisions

- Kept `chat()` stateless and put the memory bookkeeping in the loop, making explicit
  that "memory" is just accumulated text, not a model feature.
- Used `User:` / `Assistant:` role labels in the concatenated history.

## Deviations from Plan

None.

## Files Modified

- `src/07/chatbot.py`

## Integration Notes

This hand-rolled memory is what the Strands framework later provides automatically
(unit 10) and what unit 11 persists to disk.

## Lessons Learned

Building memory by hand first makes the framework's automatic history feel like a
convenience, not a mystery.
