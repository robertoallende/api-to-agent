# Unit 03: rules

## Objective

Build the first "chatbot" with no AI at all — a deterministic, rule-based responder
with three hardcoded cases (`src/03`).

## Implementation

- `src/03/chatbot.py` — `chat(text)` lowercases the input and returns:
  - contains `hello` → `hello, how are you?`
  - contains `bye` → `bye!, have a nice day.`
  - otherwise → `Beautiful weather, nothing beats Wellington on a nice day!`
- Input taken from `sys.argv[1]`.

## AI Interactions

- Implemented the three-case logic and verified each branch.

## Files Modified

- `src/03/chatbot.py`

## Status: Complete
