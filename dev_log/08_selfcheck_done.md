# Unit 08: selfcheck - Completion Context

## What Was Implemented

`src/08/chatbot.py`: a generate-judge-retry loop where the model classifies its own
answer (`is_cynical`) and the program regenerates until it passes or hits
`MAX_TRIES`, with a visible retry marker.

## Key Decisions

- `is_cynical` returns a real `bool`; reliability comes from (a) a strict one-word
  classifier prompt and (b) tolerant parsing (`"true" in verdict.strip().lower()`).
- Added observability: `<Not cynical enough, calling chat again>` prints on each
  retry so the self-correction is visible on stage.
- Capped retries with `MAX_TRIES = 3`.

## Deviations from Plan

The original judge prompt made `llama3.2` answer `False` even for clearly cynical
text, which would loop forever; a stricter classifier prompt fixed it.

## Files Modified

- `src/08/chatbot.py`

## Integration Notes

This is the "LLM as judge" beat — the program uses the model to evaluate and control
itself. Unit 09 reuses the exact loop with a different persona.

## Lessons Learned

Two things matter for reliable self-checking on a small model: a decisive classifier
prompt and forgiving output parsing.
