# Unit 15: ranking - Completion Context

## What Was Implemented

`src/15/chatbot.py`: unit 14 with the cynical/happy branch changed from
"generate one, judge, retry" to "generate several, rank all". In cynical/happy mode it
generates `N_CANDIDATES = 5` answers with Qwen, scores them in a **single** TypeSafe
call (one Noul per candidate, each embedding its own text via structured instructions),
and prints them ranked by probability — most cynical/happy first. Neutral mode is
unchanged. `src/15/README.md` documents it with a diagram.

## Key Decisions

- **Batched scoring, one call.** All five candidates are scored in a single
  `system_one` call using structured `instructions` (`{"answer": <text>,
  "question": <mode question>}`) so each Noul judges its own candidate. Verified live
  before building (five distinct answers ranked correctly).
- **Ranking, not gating.** `rank_candidates` sorts `(candidate, noul)` by probability
  descending. No threshold, no retry, no `MAX_TRIES` — every candidate is shown, ordered.
- **On-screen Jev activity kept.** A dim-gray `judge_note` line ("jev is ranking 5
  answers by how cynical they are…") plus per-line `p(mode)=..`, matching the earlier
  units' style.
- **Resilient generation.** Each generation is wrapped in try/except; a single failed or
  over-long candidate is skipped (with a dim note) rather than aborting the turn.
- **max_tokens raised to 4096.** Five happy generations frequently hit the old 2048 cap
  (Strands raises `MaxTokensReachedException` on truncation); 4096 gives headroom.

## Deviations from Plan

- Added try/except skipping and raised `max_tokens` (4096) after a happy-mode run hit
  `MaxTokensReachedException` — not in the original plan but necessary for reliability
  with five generations.

## Files Modified

- `src/15/chatbot.py` (new)
- `src/15/README.md` (new)
- `src/15/.credentials` (copied from unit 14; git-ignored, NOT committed)
- `dev_log/00_main.md` (index + status)

## Integration Notes

- Requires the Qwen server (generation), `typesafe-sdk`, and a key in
  `src/15/.credentials` (ranking). No MCP server.
- Reuses unit 14's credential loading, `judge_client`, `Noul`, `GENERATE_PROMPTS`,
  modes, commands, and dim styling; only the cynical/happy branch and the judge→ranker
  swap are new.

## Lessons Learned

- The same calibrated Noul that gave a pass/fail in unit 14 becomes a **ranking signal**
  just by sorting on the probability instead of thresholding it — a small change that
  reframes the judge as a comparator.
- Generating N answers multiplies exposure to per-generation failures (token limits,
  server blips); isolating each generation keeps one bad candidate from killing the turn.

## Status: Complete
