# Unit 06: prompt

## Objective

Introduce the idea of a system/instruction prompt: a fixed piece of text prepended to
every user message, shaping the model's behavior (`src/06`).

## Implementation

- `src/06/chatbot.py` — identical to unit 05 plus a `MYAPP_PROMPT` constant.
- The call becomes `llama(MYAPP_PROMPT + astring)`.
- Demo prompt (the "cynic game"): *"Let's play the cynic game. For anything I write,
  you answer with Yes, whatever."*

## AI Interactions

- Added the hardcoded prompt and verified responses follow it (both test inputs
  returned `Yes, whatever.`).

## Files Modified

- `src/06/chatbot.py`

## Status: Complete
