# Unit 07: memory

## Objective

Give the chatbot memory across turns by feeding the accumulated conversation back
into each call — implementing `chat(string) = 🎲(m_n + string) = m_{n+1}` (`src/07`).

## Implementation

- `src/07/chatbot.py` — `chat()` is unchanged (still a stateless single call);
  memory lives outside it.
- A `memory` string starts empty. Each turn builds
  `prompt = memory + "User: " + text + "\nAssistant: "`, calls the model, then sets
  `memory = prompt + answer`.
- `User:` / `Assistant:` labels give the model the turn structure.

## AI Interactions

- Implemented the growing-history approach.
- Verified memory: stated a name and city in turn 1, and the model recalled both in
  turn 2.

## Files Modified

- `src/07/chatbot.py`

## Status: Complete
