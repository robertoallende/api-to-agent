# 15 — Ranking answers by cynicism / happiness

Unit 15 builds on unit **14**. In cynical or happy mode it no longer generates one
answer and gates it. Instead it **generates several answers and ranks them** with
TypeSafe, showing the strongest one first.

## The basics

- **Neutral** mode is unchanged: one plain answer.
- **Cynical / happy** mode:
  1. **Generate** `N_CANDIDATES` (5) answers with the local Qwen model, all using the
     persona prompt.
  2. **Score** every answer in a **single** TypeSafe call — one Noul per answer, each
     asking "Is this answer cynical/happy?" — getting a calibrated probability for each.
  3. **Rank** the answers in code by that probability and print them, most
     cynical/happy first.

There is no pass/fail threshold and no retry here (that was unit 14). Every candidate is
scored and shown, ordered.

## Flow

```
   generate 5 answers (Qwen, via LLM_BASE_URL)
                    │
                    ▼
     ┌──────────────────────────────┐
     │  TypeSafe: one Noul / answer  │   one batched call
     │  → a probability per answer   │
     └───────────────┬──────────────┘
                     │
          sort by probability (desc)
                     │
                     ▼
   print ranked list — most cynical/happy first
```

The TypeSafe activity is shown on screen (dim gray), e.g.:

```
jev is ranking 5 answers by how cynical they are…

Ranked by cynicism (most cynical first):

1. p(cynical)=0.98  "..."
2. p(cynical)=0.95  "..."
...
```

## Why one batched call

TypeSafe evaluates all the Noul questions in a request in parallel, so scoring five
answers is one round trip, not five. Each question carries its own answer text (via a
structured `instructions` object) so it judges that specific candidate.

## Credentials

The API key lives in `src/15/.credentials` (git-ignored), same 2-line format as unit 14:

```
name: <your account>
key:  <your api key>
```

Loaded at startup into `TYPESAFE_API_KEY`; never printed.

## Commands

Same as units 13/14: `mode`, `set mode neutral|cynical|happy`, `/quit`.

## Run

```bash
.venv/bin/python src/15/chatbot.py
```

## Requirements

- The local Qwen server (for generating), set via `LLM_BASE_URL` in `chatbot.py`.
- `typesafe-sdk` and a valid key in `.credentials` (for ranking).
- The project venv (`requirements.txt`). No MCP server needed.
