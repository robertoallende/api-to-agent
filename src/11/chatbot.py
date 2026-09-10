import json

from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient

SESSIONS_FILE = "sessions.md"

model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")

# The bash MCP server (mcp_docs) exposes read_document / write_document, scoped
# to its served directory. We use them to persist the conversation across runs.
mcp = MCPClient(lambda: streamable_http_client("http://127.0.0.1:8766/mcp"))


def load_history() -> str:
    """Read the previous conversation from sessions.md via the MCP read tool."""
    result = mcp.call_tool_sync(
        tool_use_id="load-history",
        name="read_document",
        arguments={"name": SESSIONS_FILE},
    )
    # The tool returns its result as a JSON string in a text block:
    # {"name": ..., "text": ...} on success, or {"error": ...} if absent.
    payload = json.loads(result["content"][0]["text"])
    return payload.get("text", "")


def transcript(messages) -> str:
    """Render the agent's messages as a readable Markdown transcript."""
    lines = ["# Session\n"]
    for message in messages:
        role = message["role"].capitalize()
        for block in message.get("content", []):
            if "text" in block:
                lines.append(f"**{role}:** {block['text']}\n")
    return "\n".join(lines)


def save_history(messages) -> None:
    """Write the conversation to sessions.md via the MCP write tool."""
    mcp.call_tool_sync(
        tool_use_id="save-history",
        name="write_document",
        arguments={"name": SESSIONS_FILE, "text": transcript(messages)},
    )


with mcp:
    previous = load_history()
    system_prompt = "You are a helpful chatbot."
    if previous:
        system_prompt += (
            "\n\nHere is the conversation from our previous session; "
            "continue naturally and remember it:\n\n" + previous
        )

    agent = Agent(model=model,
                  system_prompt=system_prompt, callback_handler=None)

    while True:
        text = input("> ")

        if text.lower() == "/quit":
            save_history(agent.messages)
            print("<conversation saved to sessions.md>")
            break

        print(agent(text))
        print()
