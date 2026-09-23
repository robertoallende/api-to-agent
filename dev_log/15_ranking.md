# Unit 15: ranking

## Objective

In cynical/happy mode, generate **several** candidate answers with Qwen, score them all
with a single TypeSafe call, and print them **ranked** by the mode's trait — most
cynical (or most happy) first (`src/15`). This turns unit 14's "generate one, judge,
retry" into "generate many, judge all, rank", showing Jev used for ordering rather than
a pass/fail gate.

## Reuse (copy unit 14)

Copy `src/14/chatbot.py` → `src/15/chatbot.py`. Keep unchanged: Qwen `OpenAIModel` +
`agent` (generation), `strip_think`, the TypeSafe credential loading and
`judge_client`, `Noul`, `GENERATE_PROMPTS`, the modes and `mode` / `set mode` / `/quit`
commands, the neutral branch, and the dim-gray Jev status styling (`judge_note`).

Only the cynical/happy branch changes.

## Behaviour

### neutral (unchanged)
One plain `agent(text)` call, no generation of candidates, no Jev.

### cynical / happy (new)
1. Generate `N_CANDIDATES = 5` answers by calling `agent(GENERATE_PROMPTS[mode] + text)`
   five times (a simple loop; five separate generations rather than asking the model for
   "5 answers", which is fragile with the thinking model). Each is `strip_think`-ed.
2. Score all five in **one** TypeSafe `system_one` call: one Noul per candidate, all with
   the mode's question (`JUDGE_QUESTIONS[mode]`), keyed `answer_0 … answer_4`. Batching
   is parallel and is one round trip.
3. Read each `response.answers[key].noul`, pair with its candidate, sort **descending**
   by probability.
4. Print the ranked list, highest first (top = most cynical/happy).

No retry loop and no threshold in this unit: we always generate five and rank them.
`MAX_TRIES` is removed; the dim-red retry marker is removed (nothing retries).

### Showing the Jev calls on screen
Keep the current on-screen style. Before scoring, print a dim-gray line via `judge_note`,
e.g.:

```
jev is ranking 5 answers by how cynical they are…
```

After scoring, print each ranked line with its probability, e.g.:

```
Ranked by cynicism (most cynical first):

1. p(cynical)=0.97  "Oh sure, that'll work out great…"
2. p(cynical)=0.82  "Probably not, but who knows."
...
```

(Header trait word: "cynicism"/"cynical" or "happiness"/"happy" by mode. The per-line
`p(mode)=..` reuses the unit-14 wording. Candidate text may be truncated for display if
long; full text kept in memory.)

## Implementation

- `src/15/chatbot.py`:
  - Add `N_CANDIDATES = 5`.
  - Replace the cynical/happy branch:
    - loop to collect five `strip_think(str(agent(prompt)))` candidates;
    - build `questions = {f"answer_{i}": Noul(instructions=JUDGE_QUESTIONS[mode]) ...}`;
    - one `judge_client.system_one(model="jev-latest", state=..., questions=...)`;
    - NOTE on `state`: each Noul must judge its *own* candidate. Since one call shares a
      single `state`, use **structured instructions** — put the candidate text in the
      Noul `instructions` object alongside the question (per the Noul docs' structured
      form) so each question carries the text it judges. (Confirmed approach; see
      Deviations if it needs adjusting during build.)
    - collect `(candidate, prob)`, sort desc, print header + ranked lines with
      `judge_note` for the Jev activity.
  - Remove `MAX_TRIES` and the retry marker.
- `src/15/README.md` — short guide + a small diagram (generate 5 → Jev ranks → print).
- `dev_log/00_main.md` — add unit 15.

## Open implementation detail (resolved)

Batched scoring pairs each candidate with its own question via **Approach A**: one
`system_one` call, each Noul's `instructions` a structured object embedding that
candidate's text plus the mode question. Verified live before building — five distinct
answers were scored and ranked correctly in a single call, so the fallback (one call
per candidate) was not needed.

## AI Interactions

- (to be filled) Copy 14 → 15, implement generate-many + batched Noul ranking, verify
  ranking is correct and the Jev activity shows on screen.

## Files Modified

- `src/15/chatbot.py` (new)
- `src/15/README.md` (new)
- `dev_log/00_main.md`

## Status: Complete
