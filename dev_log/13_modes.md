# Unit 13: modes

## Objective

A mode-switching chatbot that revives the self-check personas from units 08
(`cynical`) and 09 (`happy`) as *runtime-selectable modes*, on top of the qwen /
OpenAI-compatible server wiring introduced in unit 12 (`src/13`).

The bot starts in `neutral` mode (a plain answer, no persona, no self-check). The
user can inspect and switch modes at runtime; in `cynical` / `happy` mode the
generate prompt and the judge/retry self-check loop from 08/09 are applied. When the
judge runs, the program prints a verbose line naming the model doing the judging, so
the tool invocation is visible on stage.

## Scope and reuse

- **From unit 12 (copy the base):** the whole `src/12/chatbot.py` is copied to
  `src/13/chatbot.py` as the starting point, purely to inherit the model wiring —
  `OpenAIModel` on the qwen server, `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL_ID`,
  the direct `OpenAI` client (`llm`), `/no_think`, `strip_think()`, and the
  timeout/retry client args. The coach-specific parts (Fancy Kanban, structured
  output, `WeekPlan`, `render_kanban`, template loading, filesystem persistence,
  `save_weekly_routine`, `wants_to_save`, `humanize_tool_call`) are removed.
- **From units 08 / 09 (reuse the logic, not a refactor):** the judge functions
  `is_cynical` / `is_happy` and the generate-judge-retry loop shape (`MAX_TRIES`, the
  `<Not ... enough, calling chat again>` retry marker). These are kept as plain
  functions calling the model directly (not Strands `@tool`s), matching 08/09.

## Model

- The chat model and the judge both use **`mlx-community/Qwen3-8B-4bit`** (the unit-12
  `LLM_MODEL_ID`) on the qwen server. This is the single model from unit 12 onward.
- To prepare for the next subunit (a *separate judge model*), the judge's model id is
  referenced through its own constant `JUDGE_MODEL_ID`, defaulting to `LLM_MODEL_ID`.
  Subunit 13_01 will point it at a different model without touching the loop.

## Behaviour

### Modes

- `neutral` (startup default) — one plain `agent(text)` call. No persona prompt, no
  judge, no retry.
- `cynical` — generate with the cynical prompt (from unit 08), then run the
  `is_cynical` judge and retry up to `MAX_TRIES` while it fails.
- `happy` — generate with the happy prompt (from unit 09, including the
  "quote happy song lyrics" permission), then run `is_happy` with the same retry loop.

### Commands (checked before normal input, alongside `/quit`)

- `/quit` — exit (unchanged from every prior unit).
- `mode` — print the current mode: `neutral`, `cynical`, or `happy`.
- `set mode neutral|cynical|happy` — switch the active mode; from then on the
  generate prompt and judge follow that mode. An unknown value prints a usage hint and
  leaves the mode unchanged.

### Verbose judge output

Each time the judge is called (per attempt, in cynical/happy mode), print, before the
check:

```
mlx-community/Qwen3-8B-4bit is deciding if this answer is cynical enough…
mlx-community/Qwen3-8B-4bit is deciding if this answer is happy enough…
```

The existing retry marker is kept as well:

```
<Not cynical enough, calling chat again>
<Not happy enough, calling chat again>
```

So a retry shows: a "called to check" line for the failed attempt, then the retry
marker, then a "called to check" line for the next attempt.

## Implementation

- `src/13/chatbot.py`:
  - Keep unit 12's imports/model/`llm`/`strip_think` and the `> ` / `/quit` loop shell.
  - Remove all coach/kanban/persistence code.
  - Add `MODE` state (`"neutral"` default) and the `mode` / `set mode ...` commands.
  - Add `GENERATE_PROMPTS = {"cynical": ..., "happy": ...}` reusing the 08/09 wording.
  - Add `is_cynical(answer)` / `is_happy(answer)` judges that call the model via the
    direct `llm` client with `JUDGE_MODEL_ID`, `/no_think`, `strip_think`, and the
    tolerant `"true" in verdict.lower()` parse from 08/09.
  - Add a verbose print naming `JUDGE_MODEL_ID` before each judge call, in the form
    `<JUDGE_MODEL_ID> is deciding if this answer is cynical/happy enough…`.
  - In `neutral`, a single agent call; in `cynical`/`happy`, the generate-judge-retry
    loop with `MAX_TRIES` and the retry marker.
- `src/13/README.md` — short guide (modes, commands, how to run).

## AI Interactions

- (to be filled during implementation) Copy 12 → 13, strip coach code, port 08/09
  judges to the qwen `llm` client, wire modes/commands, verify each mode and the
  verbose judge output.

## Files Modified

- `src/13/chatbot.py` (new)
- `src/13/README.md` (new)
- `dev_log/00_main.md` (add unit 13 to the index / kanban board)

## Status: Complete
