# Unit 10: agent

## Objective

Make the leap from raw HTTP calls to a real agent framework: replace the hand-written
loop with a Strands `Agent` backed by the local Ollama model (`src/10`).

## Implementation

- `src/10/chatbot.py` — `OllamaModel(host="http://localhost:11434",
  model_id="llama3.2")` wrapped in a Strands `Agent` (`callback_handler=None`).
- The same `> ` / `/quit` loop now calls `agent(text)`.
- Conversation memory is automatic via `agent.messages` — no manual bookkeeping.

## AI Interactions

- Confirmed Strands ships a native Ollama provider and smoke-tested it against the
  local model.
- Recreated the project venv on Python 3.12 and installed `strands-agents[ollama]`
  (Strands requires 3.10+).
- Verified multi-turn memory works out of the box.

## Files Modified

- `src/10/chatbot.py`
- Project `.venv` recreated on Python 3.12.

## Status: Complete
