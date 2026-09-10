# 12 — Exercise-Routine Chatbot with Fancy Kanban Output

A focused agent that only talks about **weekly exercise routines**. You chat with it
to plan your week, and when you say **`generate routine`** it writes a
[Fancy Kanban](https://github.com/robertoallende/fancy-kanban) board to
`weekly-routine.md` — one column per day (Sunday → Saturday), one card per day
describing the exercise, a rest day, or a sports match.

It is the last step of the "From API Calls to Agents" progression: a
domain-restricted agent that combines conversation, **structured output**, and an
**MCP tool** to produce and maintain a real artifact.

## What it does

- **Stays on topic.** A system prompt restricts the agent to exercise routines; it
  politely deflects anything else (news, code, recipes, small talk).
- **Plans by chatting.** Describe your week in natural language ("run Monday and
  Wednesday, football Saturday, rest Sunday, gym otherwise").
- **Generates on command.** Typing `generate routine` extracts the plan as
  structured data and writes a valid Fancy Kanban board.
- **Modifies an existing routine.** On startup it loads the current
  `weekly-routine.md` (if any) so you can ask for changes ("make Friday a tennis
  match") and regenerate.

## How it works

```
chat  ──►  explicit "generate routine"  ──►  save_weekly_routine  (@tool)
                                                    │
                    ├─ structured_output(WeekPlan)   what the plan is
                    ├─ render_kanban() + template     how it is formatted
                    └─ MCP write_document             where it is stored
```

1. **Model** — local `llama3.2` via Ollama, driven by the Strands `Agent`.
2. **Conversation** — the agent discusses the week and answers questions, refusing
   off-topic requests. It speaks only in days and activities — never in "cards",
   "boards", or storage details. **No tools are attached to the agent**, so it can
   never spuriously trigger a save while chatting.
3. **A single tool, explicitly triggered** — `save_weekly_routine` is a Strands
   `@tool`. Saving is gated on an explicit command (`generate routine`,
   `save my routine`, …); on that command the program invokes the tool. This is a
   deliberate choice: a small local model is unreliable at deciding *when* to call
   a save tool (it fires on any day-mention), so the trigger is deterministic. On a
   stronger model you could let the agent call the tool autonomously.
4. **Structured extraction** — inside the tool, `structured_output()` turns the
   conversation into a `WeekPlan` (seven `DayPlan`s, each with a `kind` of
   `Exercise | Rest | Match` and a short activity label). A Pydantic schema keeps
   the *shape* reliable even though the model is small.
5. **Template-driven rendering** — `render_kanban()` fills the board **template**
   stored in `fancy-kanban-schema.md` (between the `ROUTINE-TEMPLATE` markers),
   substituting `{{COLUMNS}}` and `{{ROWS}}`. The format lives in the schema file,
   not in the Python source, and the LLM never hand-writes the markdown.
6. **Persistence via MCP** — the board is saved through the `mcp_docs`
   `write_document` tool; the existing routine is loaded through `read_document`
   and summarised into plain "Day: activity" lines for the conversation.

### Why a tool + structured output + a template?

- **Tool** — asking the agent to *call a function* is how real agents act; the
  program no longer hard-codes a `"generate routine"` string check.
- **Structured output + Python rendering** — a small model is not reliable at
  emitting a byte-perfect Fancy Kanban block, so the model decides *what* the plan
  is and Python decides *how* it is formatted. The board is valid every time.
- **External template** — the board format is data in `fancy-kanban-schema.md`, so
  you can change the layout without touching the code.

## Board format

- `status` — the **Day** field (`Sunday … Saturday`), which becomes the kanban
  columns.
- `title` — the **Activity** label shown on each card (e.g. "5km run", "Rest",
  "Football match").
- `kind` — a colored `Select` (`Exercise` green, `Rest` grey, `Match` orange),
  shown on the card face via `card_fields`.

Example output (`weekly-routine.md`):

````markdown
```fancy-kanban
---
title: Weekly Exercise Routine
fields:
  - name: title, type: Text, label: Activity
  - name: status, type: Select, options: Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday, label: Day
  - name: kind, type: Select, options: Exercise|Rest|Match, colors: Exercise=#27ae60|Rest=#95a5a6|Match=#e67e22, label: Kind
card_fields: kind
---

| _id | Activity | Day | Kind |
|-----|----------|-----|------|
| rmrw8paf | Light Walk | Sunday | Rest |
| gfwyhciv | Running | Monday | Exercise |
| 6ia5f3vx | Gym | Tuesday | Exercise |
| nlktnk0i | Running | Wednesday | Exercise |
| sh5xorq4 | Gym | Thursday | Exercise |
| raqfocp3 | Tennis | Friday | Match |
| 2tbqyaof | Football | Saturday | Match |
```
````

## Prerequisites

- **Ollama** running locally with the `llama3.2` model:
  ```bash
  ollama pull llama3.2
  ```
- The **mcp_docs** server (the "bash" MCP) running over HTTP, serving the `output/`
  directory where `weekly-routine.md` is written:
  ```bash
  python -m mcp_docs --dir ~/code/ai/output --http --port 8766
  ```
- The project virtualenv with `strands-agents[ollama]` installed (repo root
  `.venv`).

## Run

```bash
.venv/bin/python src/12/chatbot.py
```

Then, for example:

```
> I want to run Monday and Wednesday, play football Saturday, rest Sunday, gym the rest.
> generate my routine
The weekly routine has been saved.
> make Friday a tennis match instead of gym
> save it
The weekly routine has been saved.
> /quit
```

Open `output/weekly-routine.md` in Obsidian (with the Fancy Kanban plugin) to see
the rendered board, or read it as plain text — the block is human-readable either
way.

## Commands

| Input | Effect |
|-------|--------|
| *(any exercise question)* | Chat about your routine |
| *"generate / save / update my routine"* | The agent calls `save_weekly_routine`, which writes `weekly-routine.md` via MCP |
| `/quit` | Exit |
