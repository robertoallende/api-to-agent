# Project Plan and Dev Log

**From API Calls to Agents: Popping the Hood on AI**

This project is the talk *"From API Calls to Agents: Popping the Hood on AI"* — a
live-coded journey that starts from a plain function call and grows, step by step,
into a reasoning, tool-using AI agent. Each step is a small runnable Python program
in `src/`, and the accompanying Marp deck in `presentation/` narrates the story.
There is no magic — just the real mechanics of how agents work, shown through
simple running examples.

Development follows **MMDD** (Micromanaged Driven Development): granular units,
chronological documentation, and developer approval at each step.

## Structure

Work is organized into **units** in `dev_log/`. Each unit has a plan
(`<NN>_<name>.md`) and a completion context (`<NN>_<name>_done.md`).

Units map to the sample directories under `src/`. The first unit combines the two
smallest samples; from there each `src/NN` is its own unit:

| Unit | `src/` | Sample |
|------|--------|--------|
| 01 `hello`        | `00`, `01` | Hello World, then a function `f(x)` fed from the console |
| 02 `arithmetic`   | `02`       | `g(x) = x + x` — numeric vs string addition |
| 03 `rules`        | `03`       | Rule-based chatbot (three hardcoded cases) |
| 04 `loop`         | `04`       | Interactive input loop with `/quit` |
| 05 `llm`          | `05`       | First real LLM call (local Ollama), stateless |
| 06 `prompt`       | `06`       | A hardcoded system prompt prepended to every call |
| 07 `memory`       | `07`       | Conversation memory by feeding history back in |
| 08 `selfcheck`    | `08`       | The model judges and retries its own output |
| 09 `happy`        | `09`       | The same self-check loop, a different persona |
| 10 `agent`        | `10`       | A Strands agent replaces the raw HTTP loop |
| 11 `persistence`  | `11`       | Session memory saved/restored via an MCP tool |
| 12 `kanban`       | `12`       | A focused agent that writes a Fancy Kanban routine |

## About the Project

### What This Is

A teaching artifact for a conference talk. The samples are deliberately minimal and
build on each other so the audience can watch a bare function call become an agent.
The presentation shows each step; the code is the ground truth.

### Architecture

- **`src/NN/`** — one runnable sample per step, mostly a single `chatbot.py`.
- **`presentation/`** — a Marp deck (`presentation.md`) with a Shiki-highlighting
  build (`tooling/`) that renders code slides with line numbers.
- **`output/`** — working directory served by the MCP document server; where
  `sessions.md` (unit 11) and `weekly-routine.md` (unit 12) are written.
- **Local model** — `llama3.2` served by Ollama at `http://localhost:11434`.
- **MCP server** — `mcp_docs` (the "bash" MCP) over Streamable HTTP at
  `http://127.0.0.1:8766/mcp`, providing read/write document tools.

### Technical Stack

- Python 3.12 (`.venv`); early units use only the standard library.
- `strands-agents[ollama]` for the agent units (10–12).
- `mcp` client for the MCP-backed units (11–12).
- Ollama (`llama3.2`) as the local model provider.
- Marp CLI + `@marp-team/marp-core` v5 + Shiki for the presentation.

## Project Status

### Overall Completion

All twelve units are implemented and verified against the local Ollama model and,
for units 11–12, the running MCP document server. The presentation covers the full
progression.

### Completed Features

- Progression from a plain function call to a tool-using, self-persisting agent.
- Local, no-cloud LLM inference via Ollama.
- Self-evaluation loop (LLM as judge) with retry and observability.
- Framework-based agent (Strands) with automatic conversation memory.
- MCP tools for cross-session persistence and structured artifact generation.
- Marp deck with Shiki syntax highlighting and CSS line numbers.

## Units Implemented

### Completed Units

* **01** `hello` — Hello World and a first function `f(x)` taking a console argument (`src/00`, `src/01`).
* **02** `arithmetic` — `g(x) = x + x`; converting the argument to a number so addition is numeric, not string concatenation (`src/02`).
* **03** `rules` — A rule-based chatbot with three hardcoded responses (`src/03`).
* **04** `loop` — An interactive `input()` loop with a `/quit` exit condition (`src/04`).
* **05** `llm` — The first real LLM call to local Ollama; stateless, standard library only (`src/05`).
* **06** `prompt` — A hardcoded prompt prepended to every message (`src/06`).
* **07** `memory` — Conversation memory by concatenating history into each prompt (`src/07`).
* **08** `selfcheck` — The model evaluates its own answer and retries until it passes, with a visible marker (`src/08`).
* **09** `happy` — The same self-check loop with an always-happy persona (`src/09`).
* **10** `agent` — A Strands `Agent` on Ollama replaces the raw HTTP loop; memory is automatic (`src/10`).
* **11** `persistence` — Conversation saved to `sessions.md` and reloaded next run via MCP read/write tools (`src/11`).
* **12** `kanban` — An exercise-only agent that generates and updates a Fancy Kanban `weekly-routine.md` via MCP (`src/12`).
* **13** `modes` — A mode-switching chatbot (neutral/cynical/happy) reviving the 08/09 self-check loop on the qwen server, with a verbose judge and a separate `JUDGE_MODEL_ID` (`src/13`).
* **14** `typesafe` — Unit 13 with only the judge changed: a TypeSafe **Noul** returns a calibrated probability that the answer is cynical/happy, thresholded in code and shown on screen (`src/14`).
* **15** `ranking` — Unit 14 extended: generate five answers, score them all in one TypeSafe call, and print them ranked by cynicism/happiness, most first (`src/15`).

## Planned Units

None currently.

## Dev Log Index

| Unit | Plan | Completion |
|------|------|------------|
| 01 hello | [01_hello.md](01_hello.md) | [01_hello_done.md](01_hello_done.md) |
| 02 arithmetic | [02_arithmetic.md](02_arithmetic.md) | [02_arithmetic_done.md](02_arithmetic_done.md) |
| 03 rules | [03_rules.md](03_rules.md) | [03_rules_done.md](03_rules_done.md) |
| 04 loop | [04_loop.md](04_loop.md) | [04_loop_done.md](04_loop_done.md) |
| 05 llm | [05_llm.md](05_llm.md) | [05_llm_done.md](05_llm_done.md) |
| 06 prompt | [06_prompt.md](06_prompt.md) | [06_prompt_done.md](06_prompt_done.md) |
| 07 memory | [07_memory.md](07_memory.md) | [07_memory_done.md](07_memory_done.md) |
| 08 selfcheck | [08_selfcheck.md](08_selfcheck.md) | [08_selfcheck_done.md](08_selfcheck_done.md) |
| 09 happy | [09_happy.md](09_happy.md) | [09_happy_done.md](09_happy_done.md) |
| 10 agent | [10_agent.md](10_agent.md) | [10_agent_done.md](10_agent_done.md) |
| 11 persistence | [11_persistence.md](11_persistence.md) | [11_persistence_done.md](11_persistence_done.md) |
| 12 kanban | [12_kanban.md](12_kanban.md) | [12_kanban_done.md](12_kanban_done.md) |
| 13 modes | [13_modes.md](13_modes.md) | [13_modes_done.md](13_modes_done.md) |
| 14 typesafe | [14_typesafe.md](14_typesafe.md) | [14_typesafe_done.md](14_typesafe_done.md) |
| 15 ranking | [15_ranking.md](15_ranking.md) | [15_ranking_done.md](15_ranking_done.md) |
