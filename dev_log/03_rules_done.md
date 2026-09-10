# Unit 03: rules - Completion Context

## What Was Implemented

`src/03/chatbot.py`: a rule-based chatbot with three hardcoded responses, matching on
lowercased substrings.

## Key Decisions

- `chat()` returns the string and `main` prints it — cleaner separation that pays off
  when responses are passed around in later units.
- Case-insensitive matching via `text.lower()`.
- `hello` is checked before `bye`, so a message containing both returns the hello
  response.

## Deviations from Plan

None.

## Files Modified

- `src/03/chatbot.py`

## Integration Notes

This is the "no magic" baseline: a chatbot that is purely `if/elif/else`. Units 05+
replace this logic with an LLM while keeping the same shape.

## Lessons Learned

Showing a fully deterministic chatbot first makes the later LLM version's
flexibility (and unpredictability) land clearly.
