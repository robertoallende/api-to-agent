# Unit 08: selfcheck

## Objective

Have the model evaluate its own output and retry until it meets a criterion — the
first agentic behavior, where the program uses the model's judgment to control its own
flow (`src/08`).

## Implementation

- `src/08/chatbot.py` — two functions:
  - `chat(astring)` — the Ollama call from unit 05.
  - `is_cynical(question, answer)` — asks the model a strict true/false classifier
    question and parses the reply into a real `bool`.
- The loop generates a cynical answer, then retries (up to `MAX_TRIES`) while
  `is_cynical` is false, printing `<Not cynical enough, calling chat again>` each
  retry for observability.

## AI Interactions

- Implemented the generate/judge/retry loop with a boolean-parsing check.
- Found the first judge prompt unreliable (returned `False` even for cynical text);
  switched to a strict classifier prompt and `"true" in verdict` parsing.
- Added `MAX_TRIES` to bound retries. Verified the retry marker fires and the check
  distinguishes cynical from cheerful answers.

## Files Modified

- `src/08/chatbot.py`

## Status: Complete
