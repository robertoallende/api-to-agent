# Unit 11: persistence - Completion Context

## What Was Implemented

`src/11/chatbot.py`: the Strands agent with cross-session memory. The conversation is
saved to `sessions.md` via the MCP `write_document` tool on `/quit` and reloaded via
`read_document` on start, then injected into the system prompt.

## Key Decisions

- Persistence goes through the `mcp_docs` MCP server over Streamable HTTP — the talk's
  MCP demonstration — rather than a plain local file write.
- The MCP tools are NOT attached to the agent. When they were, `llama3.2` tried to
  call `write_document` conversationally and derailed; the program drives save/load
  instead.
- The transcript is human-readable (`User:` / `Assistant:` markdown) so it can be
  shown on stage; it is re-injected via the system prompt to restore context.

## Deviations from Plan

Reload is done by injecting the transcript into the system prompt rather than using a
Strands `FileSessionManager`, because the developer wanted a human-readable
`sessions.md` produced through the MCP tool.

## Files Modified

- `src/11/chatbot.py`

## Integration Notes

Requires the MCP server running and serving `output/`, plus the 3.12 venv. Depends on
the `write_document` tool added to the MCP server (its Unit 06).

## Lessons Learned

Small models over-eagerly call tools; making persistence program-driven (with the
tool as the I/O mechanism) is more reliable for a live demo.
