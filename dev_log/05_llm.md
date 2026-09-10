# Unit 05: llm

## Objective

Replace the hardcoded rules with a real call to a language model — the first "AI"
step — using local Ollama, stateless, and only the standard library (`src/05`).

## Implementation

- `src/05/chatbot.py` — `chat(astring)` POSTs to Ollama's `/api/generate`
  (`http://localhost:11434`) with model `llama3.2` and `stream: False`, using
  `urllib.request` and `json`.
- The same `> ` / `/quit` loop from unit 04 now calls `chat()`.
- Stateless: each call sends only the current message.

## AI Interactions

- Detected the running Ollama instance and the fastest small model (`llama3.2`).
- Implemented the call with the standard library (no `requests` dependency).
- Verified a prompt returns a model response.

## Files Modified

- `src/05/chatbot.py`

## Status: Complete
