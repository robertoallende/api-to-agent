# Unit 04: loop

## Objective

Turn the one-shot chatbot into an interactive session: read repeatedly from the
console until the user quits (`src/04`).

## Implementation

- `src/04/chatbot.py` — a `while True` loop reading `input("> ")`.
- `/quit` exits the loop (checked before the response logic).
- The three-case response logic is inlined into the loop (no function, no
  `__main__` guard) to keep the reading top-to-bottom for the talk.
- A blank line is printed after each answer for readability.

## AI Interactions

- Converted `sys.argv` input to an `input()` loop with a `/quit` exit.
- Inlined the logic and removed the `__main__` guard at the developer's request.
- Changed the prompt to `> ` and added a trailing blank line.

## Files Modified

- `src/04/chatbot.py`

## Status: Complete
