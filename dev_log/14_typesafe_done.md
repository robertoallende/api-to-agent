# Unit 14: typesafe - Completion Context

## What Was Implemented

`src/14/chatbot.py`: unit 13 with **only the judge changed**. Generation still uses the
local qwen `OpenAIModel`; the cynical/happy self-check now uses a **TypeSafe Noul** —
a typed yes/no question to TypeSafe's Jev model that returns a calibrated probability,
which the code thresholds (`JUDGE_THRESHOLD = 0.6`). The verbose judge line shows the
probability, e.g. `jev is deciding if this answer is cynical enough… p(cynical)=0.95`.

Everything else is identical to unit 13: modes (`neutral` default, `cynical`, `happy`),
the 08/09 generate prompts, `MAX_TRIES` retry loop, `mode` / `set mode` / `/quit`
commands, and the dim-gray call / dim-red retry / blank-line output styling.

Supporting files: `src/14/README.md`, saved reference docs in `src/14/docs/`
(`noul.md`, `python-sdk.md`, `ai-primer.md`), `typesafe-sdk` added to `requirements.txt`.

## Key Decisions

- **Noul, not a classifier prompt.** The judge sends `Noul(instructions="Is this answer
  cynical/happy?")` and reads `response.answers[mode].noul`. No prompt engineering for
  "reply true/false", no `<think>` stripping, no substring parsing on the judge path.
- **Threshold owned by code.** `JUDGE_THRESHOLD = 0.6` defines "enough"; raise/lower to
  tune. This is the "preparation" — the model itself is not trained or fine-tuned.
- **Credentials from a git-ignored file.** `src/14/.credentials` (`name:` / `key:`) is
  read at startup into `TYPESAFE_API_KEY`; the value is never printed. `.gitignore`
  updated (`.credentials`, `**/.credentials`).
- **Kept qwen for generation** so the only conceptual change on stage is the judge.

## Deviations from Plan

None. Unit 13's `JUDGE_MODEL_ID` (the hook for a different judge *LLM*) is gone,
superseded by TypeSafe; the "different judge" idea is now realised via a different kind
of model entirely.

## Files Modified

- `src/14/chatbot.py` (new)
- `src/14/README.md` (new)
- `src/14/docs/{noul,python-sdk,ai-primer}.md` (new, saved references)
- `requirements.txt` (added `typesafe-sdk`)
- `.gitignore` (ignore `.credentials`)
- `dev_log/00_main.md` (index + status)

## Integration Notes

- Requires the qwen server (generation), `typesafe-sdk`, and a valid key in
  `src/14/.credentials` (judging). No MCP server.
- Verified live: SDK installed (0.7.1); Noul judgments cynical=0.98/happy=0.01 on
  cynical text, 0.02/0.99 on happy text, 0.04/0.08 on neutral text; full loop run
  across all three modes prints the probability and behaves as in unit 13; no key
  value appears in output.

## Lessons Learned

- A calibrated typed judgment replaces the entire "prompt a classifier and parse its
  words" dance from 08/09/13, and it hands back a number the UI can display — a strong
  closing beat for the talk (prompt-and-parse → typed decision).
- "Preparing" a System One model is question wording plus a code-side threshold, not
  training. Worth stating explicitly on stage since it's a common misconception.

## Status: Complete
