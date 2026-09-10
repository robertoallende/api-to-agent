# Unit 05: llm - Completion Context

## What Was Implemented

`src/05/chatbot.py`: the first real LLM-backed chatbot, calling local Ollama's
`/api/generate` with `llama3.2`, stateless, standard library only.

## Key Decisions

- Used `urllib.request` + `json` instead of `requests` to avoid a dependency at this
  stage.
- Used `/api/generate` (single prompt) rather than `/api/chat`, keeping the call as
  plainly "text in, text out" as possible.
- Picked `llama3.2` (the smallest installed model) for speed during a live demo.

## Deviations from Plan

None.

## Files Modified

- `src/05/chatbot.py`

## Integration Notes

Same loop shape as unit 04; only the body of `chat()` changed. This is the pivot from
deterministic rules to a probabilistic model. Requires Ollama running locally.

## Lessons Learned

Keeping the loop identical and swapping only the response function makes the
"rules → LLM" moment a clean, single-idea diff.
