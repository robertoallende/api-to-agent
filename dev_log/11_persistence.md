# Unit 11: persistence

## Objective

Give the agent memory that survives process restarts: save the conversation to
`sessions.md` on exit and reload it on start — using an MCP tool for the file I/O
(`src/11`).

## Implementation

- `src/11/chatbot.py` — the unit 10 agent plus an `MCPClient` connected over
  Streamable HTTP to the `mcp_docs` server (`http://127.0.0.1:8766/mcp`).
- `load_history()` calls the MCP `read_document` tool for `sessions.md`, parsing the
  JSON result; `save_history()` calls `write_document` with a readable
  `User:`/`Assistant:` transcript rendered from `agent.messages`.
- On start, any prior transcript is injected into the `system_prompt`; on `/quit`,
  the conversation is saved.

## AI Interactions

- Gate check: confirmed `write_document` exists in the MCP server and live-listed all
  tools before building.
- Verified across two separate processes: session 1 stated a fact and quit; session 2
  recalled it from `sessions.md`.
- Fixed a design issue: attaching the MCP tools to the agent made the small model
  misuse them mid-chat, so persistence is driven by the program, not the agent.

## Files Modified

- `src/11/chatbot.py`

## Status: Complete
