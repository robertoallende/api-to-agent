# From API Calls to Agents: Popping the Hood on AI

A live-coded journey that starts from a plain function call and grows, step by step,
into a reasoning, tool-using AI agent — with **no magic**, just the real mechanics.

Each step is a small, runnable Python program under [`src/`](src), and the companion
[Marp deck](presentation/) narrates the story. The talk abstract lives in
[`dev_log/00_description.md`](dev_log/00_description.md).

> **From API Calls to Agents: Popping the Hood on AI**
> This talk pulls back the curtain. Starting from a plain function call, we trace the
> journey to a working AI agent — step by step, concept by concept. What is a tool,
> and how does an agent discover it? How does an LLM decide what to call and when?
> What turns a raw response into a natural conversation?

## The progression

Each sample builds on the previous one, changing as little as possible so the diff is
the lesson.

| Step | Directory | What it adds |
|------|-----------|--------------|
| 1 | [`src/00`](src/00), [`src/01`](src/01) | Hello World, then a function `f(x)` fed from the console |
| 2 | [`src/02`](src/02) | `g(x) = x + x` — numeric vs string addition |
| 3 | [`src/03`](src/03) | A rule-based chatbot (three hardcoded cases) |
| 4 | [`src/04`](src/04) | An interactive `> ` input loop with `/quit` |
| 5 | [`src/05`](src/05) | The first real LLM call (local Ollama), stateless |
| 6 | [`src/06`](src/06) | A hardcoded prompt prepended to every message |
| 7 | [`src/07`](src/07) | Conversation **memory** by feeding history back in |
| 8 | [`src/08`](src/08) | The model **judges and retries** its own output |
| 9 | [`src/09`](src/09) | The same self-check loop, a different persona |
| 10 | [`src/10`](src/10) | A **Strands agent** replaces the raw HTTP loop |
| 11 | [`src/11`](src/11) | Session memory **saved/restored via an MCP tool** |
| 12 | [`src/12`](src/12) | A focused **tool-using agent** that writes a Fancy Kanban routine |

The story arc: deterministic code → a first LLM call → prompts → memory →
self-evaluation → a framework agent → tools, persistence, and a real artifact.

## Layout

```
src/            One runnable sample per step (00–12)
presentation/   Marp deck + Shiki build tooling
output/         Working dir served by the MCP server (sessions.md, weekly-routine.md)
dev_log/        MMDD dev log: project index (00_main.md) + one unit per step
```

## Requirements

- **Python 3.12** (repo `.venv`). Steps 1–9 use only the standard library.
- **[Ollama](https://ollama.com)** running locally with the `llama3.2` model
  (steps 5+):
  ```bash
  ollama pull llama3.2
  ```
- **Strands Agents** for the agent steps (10–12):
  ```bash
  python3.12 -m venv .venv
  .venv/bin/pip install "strands-agents[ollama]" mcp
  ```
- **An MCP document server** for steps 11–12 (the "bash" MCP, `mcp_docs`), serving the
  `output/` directory over HTTP:
  ```bash
  python -m mcp_docs --dir ~/code/ai/output --http --port 8766
  ```

## Running the samples

Steps 1–4 (standard library, any Python 3):

```bash
python3 src/00/hello.py
python3 src/01/f.py 10
python3 src/02/g.py 10
python3 src/03/chatbot.py "hello there"
python3 src/04/chatbot.py          # interactive; type /quit to exit
```

Steps 5–9 (need Ollama running):

```bash
python3 src/05/chatbot.py
python3 src/08/chatbot.py
```

Steps 10–12 (need the 3.12 venv; 11–12 also need the MCP server):

```bash
.venv/bin/python src/10/chatbot.py
.venv/bin/python src/11/chatbot.py    # persists to output/sessions.md
.venv/bin/python src/12/chatbot.py    # writes output/weekly-routine.md
```

Step 12 has its own detailed guide in [`src/12/README.md`](src/12/README.md).

## Presentation

The deck is a Marp file at [`presentation/presentation.md`](presentation/presentation.md),
built with a custom engine that adds Shiki syntax highlighting and CSS line numbers.

Build once and serve it locally:

```bash
cd presentation
./serve.sh            # builds, then serves at http://localhost:8000/presentation.html
```

Or rebuild on save while editing:

```bash
cd presentation/tooling
npm install           # first time only
npm run watch         # rebuilds ../presentation.html on change
```

## How it was built

This project was developed with **MMDD** (Micromanaged Driven Development): granular
units, chronological documentation, and approval at each step. The full dev log —
including the real design decisions and course-corrections — is in
[`dev_log/`](dev_log), indexed by [`dev_log/00_main.md`](dev_log/00_main.md).

## Author

Roberto Allende — [allende.nz](https://allende.nz/)
