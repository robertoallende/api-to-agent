# Unit 10: agent - Completion Context

## What Was Implemented

`src/10/chatbot.py`: a Strands `Agent` on the local Ollama model, keeping the
familiar `> ` / `/quit` loop but delegating the model loop and conversation memory to
the framework.

## Key Decisions

- Used Strands' native `OllamaModel` provider (no Bedrock/AWS, no OpenAI shim).
- Set `callback_handler=None` so the agent doesn't stream its own console output; the
  final answer is printed by our loop, keeping the interface identical to earlier
  units.
- Recreated `.venv` on Python 3.12 because Strands requires ≥3.10 (the prior venv was
  3.9).

## Deviations from Plan

Required a Python upgrade (3.9 → 3.12) that the earlier standard-library units did not
need.

## Files Modified

- `src/10/chatbot.py`
- Project `.venv` (recreated on 3.12, `strands-agents[ollama]` installed).

## Integration Notes

The framework now provides automatically what unit 07 built by hand (memory). Must be
run with the 3.12 venv (`.venv/bin/python`). Sets up tool use in units 11–12.

## Lessons Learned

Introducing the framework only after hand-rolling the loop and memory lets the
audience see exactly what the framework is doing for them.
