# 13 — Mode-Switching Chatbot (neutral / cynical / happy)

A chatbot with a **persona you switch at runtime**. It brings back the self-check idea
from units 08 (cynical) and 09 (happy) and lets you turn it on or off while chatting.

## The basics

- Starts in **neutral**: you get a plain answer, nothing special.
- Switch to **cynical** or **happy** and the bot does two things per message:
  1. **Generate** an answer in that persona.
  2. **Judge** its own answer with a second model call: "is this cynical/happy enough?"
     If not, it throws the answer away and tries again (up to `MAX_TRIES`).

The generation and the judging both use the same LLM (a local Qwen model), reached
through the `LLM_BASE_URL` set at the top of `chatbot.py` — no URL is hardcoded in this
document. The judge is a plain classifier prompt whose reply ("true"/"false") is parsed
into a yes/no.

## Flow

```
        you type a message
               │
      ┌────────┴─────────┐
      │  current mode?   │
      └───┬─────────┬────┘
   neutral│         │ cynical / happy
          │         │
   plain  │   ┌─────▼───────────────┐
   answer │   │ generate in persona │◄──────┐
          │   └─────────┬───────────┘       │
          │             │                   │ not "enough"
          │        ┌────▼─────┐   retry     │
          │        │  judge   │─────────────┘
          │        │ enough?  │
          │        └────┬─────┘
          │             │ yes
          ▼             ▼
        print the answer
```

## Commands

| Input | Effect |
|-------|--------|
| *(any message)* | Answer using the current mode |
| `mode` | Show the current mode |
| `set mode neutral\|cynical\|happy` | Switch mode |
| `/quit` | Exit |

The judge's activity is printed dimmed: the "is deciding…" line in gray, the
"not X enough, trying again" line in red, so it reads as background noise, separate
from the actual answer.

## Run

```bash
.venv/bin/python src/13/chatbot.py
```

## Requirements

- A local Qwen (OpenAI-compatible) server, set via `LLM_BASE_URL` in `chatbot.py`.
- The project venv with `strands-agents[openai]` (repo `requirements.txt`).
- No MCP server needed.
