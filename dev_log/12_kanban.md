# Unit 12: kanban

## Objective

Build a focused, tool-using agent with a real job: an exercise-only coach that, on
request, generates and updates a weekly routine as a Fancy Kanban board in
`weekly-routine.md` (`src/12`).

## Implementation

- `src/12/chatbot.py` — Strands agent on Ollama with a domain-restricted system
  prompt (exercise routines only; deflects off-topic; speaks in days and activities,
  never "cards" or "boards").
- On an explicit save intent (`wants_to_save`), `save_weekly_routine` (a Strands
  `@tool`) runs `structured_output(WeekPlan)` to extract a 7-day plan, and
  `render_kanban()` fills a board template read from `fancy-kanban-schema.md`
  (`{{COLUMNS}}` / `{{ROWS}}`), written via the MCP `write_document` tool.
- On start, the existing routine is loaded via `read_document` and summarised into
  plain "Day: activity" lines for the conversation.
- Days (Sunday–Saturday) are the kanban columns; each day is one card with a colored
  `kind` (Exercise / Rest / Match).
- `src/12/README.md` documents the sample; `src/12/fancy-kanban-schema.md` holds the
  schema and the board template.

## AI Interactions

- Designed the day-as-column board mapping from the Fancy Kanban schema.
- Chose structured-output + Python rendering because a small model cannot reliably
  hand-write a valid board.
- Iterated on several real issues: stopped the agent leaking "card" vocabulary
  (summarise instead of injecting the raw block); moved the board format into the
  schema file; used `@tool`; stopped spurious/hallucinated tool calls by detaching
  tools and gating saves on explicit intent; broadened intent detection so natural
  phrasings ("save it on my weekly plan") trigger a save; added a humaniser for any
  leaked tool-call fragments.

## Files Modified

- `src/12/chatbot.py`
- `src/12/README.md`
- `src/12/fancy-kanban-schema.md`

## Status: Complete
