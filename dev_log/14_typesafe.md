# Unit 14: typesafe

## Objective

Swap **only the judging mechanism** of unit 13 from a prompt-and-parse LLM call to a
**TypeSafe Noul** — a typed yes/no judgment that returns a calibrated probability
(`src/14`). Everything else about unit 13 (modes, personas, generate prompts, retry
loop, commands, colored output) stays identical, so the diff is the lesson: an
LLM classifier hack becomes a single typed decision, and the probability is shown.

## Background (from src/14/SKILL.md and the saved docs)

- TypeSafe's **Jev** model returns typed judgments, not text. A **Noul** asks a yes/no
  question and returns `noul`, the calibrated probability of "yes" in [0, 1]. There is
  no separate confidence for a Noul — the one number is the answer.
- You do **not** train or fine-tune it. You "prepare" it by (a) the question wording
  (`instructions` / optional `criteria`) and (b) the **threshold** you pick in code.
- Verified live with the account key: cynical text → 0.98 cynical / 0.01 happy;
  happy text → 0.02 / 0.99; neutral → 0.04 / 0.08. A threshold near 0.6 separates them.
- Docs saved under `src/14/docs/` (`noul.md`, `python-sdk.md`, `ai-primer.md`).

## What changes vs unit 13

Only `judge()`:

- **Before (13):** call the qwen chat model with a strict "reply true/false" prompt,
  `/no_think`, `strip_think`, then `"true" in verdict.lower()`.
- **After (14):** call TypeSafe once with a `Noul` whose `instructions` ask whether the
  answer is cynical / happy; read `response.answers[mode].noul`; compare to a threshold.

Kept unchanged from 13: the three modes (`neutral` default, `cynical`, `happy`), the
08/09 generate prompts, `MAX_TRIES` and the retry loop, the `mode` / `set mode` /
`/quit` commands, the qwen `OpenAIModel` **for generation**, and the dim-gray call /
dim-red retry / blank-line-before-answer output styling.

## Credentials

- The API key lives in `src/14/.credentials` (2 lines: `name:` and `key:`), already
  added to `.gitignore` (`.credentials`, `**/.credentials`).
- `chatbot.py` reads the `key:` line at startup and sets `TYPESAFE_API_KEY` in the
  environment before constructing `TypeSafeClient` (the SDK reads that env var).
- The key value is never printed.

## Probability in the verbose output

The judge line now shows the model and the probability, in the same dim-gray style:

```
jev is deciding if this answer is cynical enough… p(cynical)=0.98
```

- `JUDGE_LABEL = "jev"` (TypeSafe's model), replacing the qwen model id in the line.
- Threshold constant `JUDGE_THRESHOLD = 0.6`; "enough" means `noul >= JUDGE_THRESHOLD`.
- The dim-red retry marker (`<Not cynical enough, calling chat again>`) and the blank
  line before the answer are unchanged.

## Implementation

- Copy `src/13/chatbot.py` → `src/14/chatbot.py`.
- Remove the qwen-based judge internals; keep the qwen `model`/`agent` for generation.
- Add credential loading: read `src/14/.credentials`, set `TYPESAFE_API_KEY`.
- Rewrite `judge(mode, answer)`:
  - Build a `Noul` for the mode (`cynical` / `happy`) with `instructions`.
  - `client.system_one(model="jev-latest", state=answer, questions={mode: Noul(...)})`.
  - Print the dim verbose line including `p(mode)=<value>`.
  - Return `noul >= JUDGE_THRESHOLD`.
  - Reuse one module-level `TypeSafeClient` (opened once).
- `src/14/README.md` — short guide (what changed vs 13, credentials, how to run).
- Add `typesafe-sdk` to `requirements.txt`.

## AI Interactions

- Read `SKILL.md`, fetched and saved the live Noul / Python SDK / AI-primer docs.
- Verified the SDK install and live Noul judgments (cynical/happy/neutral) with the key.
- (to be filled) Implement, then verify each mode drives the Noul judge and prints the
  probability, with the retry loop behaving as in 13.

## Files Modified

- `src/14/chatbot.py` (new)
- `src/14/README.md` (new)
- `src/14/docs/` (saved reference docs — already created)
- `requirements.txt` (add `typesafe-sdk`)
- `.gitignore` (already updated for `.credentials`)
- `dev_log/00_main.md` (index + status)

## Status: Complete
