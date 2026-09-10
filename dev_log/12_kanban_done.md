# Unit 12: kanban - Completion Context

## What Was Implemented

`src/12/chatbot.py`: an exercise-only coaching agent that generates and updates a
weekly routine as a Fancy Kanban board (`weekly-routine.md`) via the MCP
`write_document` tool, reading any existing routine via `read_document`. Supported by
`src/12/README.md` and `src/12/fancy-kanban-schema.md` (schema + board template).

## Key Decisions

- **Structured output + Python rendering**: the model decides *what* the plan is
  (`structured_output(WeekPlan)` with a constrained `Exercise|Rest|Match` enum); a
  Python function fills a template to guarantee a valid board every time.
- **External template**: the board format lives in `fancy-kanban-schema.md` between
  `ROUTINE-TEMPLATE` markers, not in the code.
- **Domain restriction**: the system prompt keeps the agent on exercise and forbids
  mentioning cards/boards/kanban; the loaded routine is summarised to plain
  "Day: activity" lines so the storage vocabulary never leaks into chat.
- **Reliable saving**: tools are not attached to the agent (the small model
  hallucinated/misfired tool calls); saving is gated on explicit intent via
  `wants_to_save`, which then invokes the `@tool`. A `humanize_tool_call` filter
  catches any leaked tool-call JSON.
- Days (Sunday–Saturday) are the columns; one card per day with a colored `kind`.

## Deviations from Plan

Save triggering evolved from model-decided tool calls to explicit intent detection,
because `llama3.2` fired the tool on any day-mention and sometimes emitted raw
tool-call JSON as text. On a stronger model, autonomous tool calling could be
re-enabled.

## Files Modified

- `src/12/chatbot.py`
- `src/12/README.md`
- `src/12/fancy-kanban-schema.md`

## Integration Notes

Requires the 3.12 venv, Ollama, and the MCP server serving `output/`. Combines every
prior idea: conversation, structured output, an MCP tool, and a generated artifact.

## Lessons Learned

Split responsibilities to work around small-model limits: let the model decide
content, let code enforce format and control flow. Externalising the template keeps
the format editable without touching code.
