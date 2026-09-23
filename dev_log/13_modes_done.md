# Unit 13: modes - Completion Context

## What Was Implemented

`src/13/chatbot.py`: a mode-switching chatbot with three runtime modes — `neutral`
(default), `cynical`, and `happy`. Neutral is a plain model call; cynical/happy revive
the generate-judge-retry self-check loop from units 08/09. `src/13/README.md`
documents it.

Commands: `mode` (show current mode), `set mode neutral|cynical|happy` (switch),
`/quit` (exit).

The judge announces itself before each check with a demo-friendly line naming the
judge model, e.g.
`mlx-community/Qwen3-8B-4bit is deciding if this answer is cynical enough…`,
and the 08/09 retry marker (`<Not cynical enough, calling chat again>`) is kept.

## Key Decisions

- **Reuse, not refactor.** Copied unit 12 as the base for its qwen `OpenAIModel`
  wiring (`LLM_*` constants, direct `OpenAI` client, `/no_think`, `strip_think`,
  timeout/retries) and ported the 08/09 judge and loop as plain functions.
- **Separate judge model id.** The judge calls through `JUDGE_MODEL_ID`, defaulting to
  `LLM_MODEL_ID`, so the next subunit can point the judge at a different model without
  touching the loop. This was the explicit setup requested for 13_01.
- **Judge on the direct client**, not the Strands agent — matches the plain classify
  call in 08/09 and is more reliable with this thinking model (we clean the `<think>`
  block ourselves).
- **Neutral = plain call**, no persona prompt and no judge (no verbose line, no retry).

## Deviations from Plan

None functionally. Wording of the verbose judge line was made funnier per developer
request (`… is deciding if this answer is … enough…` with a ).

## Files Modified

- `src/13/chatbot.py` (new)
- `src/13/README.md` (new)
- `dev_log/00_main.md` (index + status updated)

## Integration Notes

- Requires the qwen OpenAI-compatible server at `LLM_BASE_URL` and the project venv
  with `strands-agents[openai]`. No MCP server needed (unlike 12).
- Reuses the model wiring established in unit 12 and the self-check pattern from 08/09.

## Lessons Learned

- Conversation memory is shared across modes (one `Agent`), so switching to `neutral`
  after `happy` can still show the base model's carried-over style. Left as-is for
  this unit; a future tweak could clear `agent.messages` on mode change if a clean
  neutral is wanted.
- Threading the judge through its own `JUDGE_MODEL_ID` up front makes the planned
  "different model for the judge" subunit a one-line change.

## Status: Complete
