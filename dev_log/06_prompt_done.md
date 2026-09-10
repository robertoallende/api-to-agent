# Unit 06: prompt - Completion Context

## What Was Implemented

`src/06/chatbot.py`: unit 05 plus a hardcoded `MYAPP_PROMPT` prepended to every
message, so `chat(string)` effectively calls `llama(myapp_prompt + string)`.

## Key Decisions

- Kept the prompt as a plain string concatenation to show, with no framework, that a
  "system prompt" is just text placed before the user's input.
- Still stateless — the prompt is the only added context.

## Deviations from Plan

None.

## Files Modified

- `src/06/chatbot.py`

## Integration Notes

Sets up unit 07: if a fixed string can steer the model, a *growing* string
(conversation history) gives it memory.

## Lessons Learned

Demonstrating prompt-as-concatenation demystifies "system prompts" before any
framework hides the mechanism.
