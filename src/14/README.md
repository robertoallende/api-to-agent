# 14 — TypeSafe Judge (typed decision instead of prompt-and-parse)

Unit 14 is unit **13** with **only the judge changed**. Same modes, same personas, same
retry loop. The difference is *how the bot decides* whether an answer is cynical or
happy "enough".

## The basics

- **Generating** the answer still uses the local Qwen model (set via `LLM_BASE_URL` in
  `chatbot.py`; no URL is hardcoded in this document).
- **Judging** now uses **TypeSafe**. Instead of asking an LLM to reply "true"/"false"
  and parsing the text, we ask a **Noul** — a typed yes/no question — and get back a
  **calibrated probability** (0 to 1). Code compares it to a threshold.

You don't train TypeSafe. You "prepare" it in two ways, both plain code:
1. the **question** — "Is this answer cynical?"
2. the **threshold** — `JUDGE_THRESHOLD` (raise it for stricter, lower for looser).

## What changed vs unit 13

| | Unit 13 | Unit 14 |
|---|---|---|
| Ask the judge | LLM: "reply true/false…" | `Noul("Is this answer cynical?")` |
| Get back | text to clean and parse | a probability, e.g. `0.95` |
| Decide "enough" | `"true" in reply` | `probability >= JUDGE_THRESHOLD` |

The judge line now shows the number:

```
jev is deciding if this answer is cynical enough… p(cynical)=0.95
```

## Flow

```
      generate answer (Qwen, via LLM_BASE_URL)
                   │
                   ▼
        ┌──────────────────────┐
        │  TypeSafe Noul        │   "Is this answer cynical/happy?"
        │  → probability 0..1   │
        └──────────┬───────────┘
                   │
          probability >= threshold ?
             │                  │
          no │ retry            │ yes
             └──────────────►  print the answer
```

## Credentials

The API key lives in `src/14/.credentials` (git-ignored):

```
name: <your account>
key:  <your api key>
```

`chatbot.py` reads the `key:` line at startup into `TYPESAFE_API_KEY` (the SDK reads
that). The key is never printed. Create a key at https://console.typesafe.ai/.

## Commands

Same as unit 13: `mode`, `set mode neutral|cynical|happy`, `/quit`.

## Run

```bash
.venv/bin/python src/14/chatbot.py
```

## Requirements

- The local Qwen server (for generating), set via `LLM_BASE_URL` in `chatbot.py`.
- `typesafe-sdk` and a valid key in `.credentials` (for judging).
- The project venv (`requirements.txt`). No MCP server needed.

See `docs/` for the saved TypeSafe references (Noul, Python SDK, and how the model
works).
