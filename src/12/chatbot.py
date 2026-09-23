import random
import re
import string

from enum import Enum
from pathlib import Path
from typing import List

from openai import OpenAI
from pydantic import BaseModel, Field
from strands import Agent, tool
from strands.models.openai import OpenAIModel

# The qwen server, model, and API details, shared by the agent and the
# direct structured-extraction call below.
LLM_BASE_URL = "http://10.130.2.57:8080/v1"
LLM_API_KEY = "EMPTY"  # local server; the key is required but unused
LLM_MODEL_ID = "mlx-community/Qwen3-8B-4bit"

ROUTINE_FILE = "weekly-routine.md"
SCHEMA_FILE = Path(__file__).with_name("fancy-kanban-schema.md")
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"]

SYSTEM_PROMPT = (
    "You are an exercise-routine coach. You ONLY talk about weekly exercise "
    "routines: workouts, sports, rest days, and how to plan them across the "
    "week. If the user asks about anything else (news, code, food recipes, "
    "general chit-chat), politely refuse and steer the conversation back to "
    "their exercise routine. Keep replies short and practical.\n\n"
    "Always speak in terms of DAYS OF THE WEEK and ACTIVITIES (for example: "
    "'On Monday, do a 5km run'). NEVER mention cards, boards, columns, "
    "kanban, files, or any technical or storage detail — the user only thinks "
    "in days and exercises. Talk to them as a coach would, not as software.\n\n"
    "When the user asks to generate, save, or update their routine, you MUST "
    "call the save_weekly_routine tool.\n\n"
    # Qwen3 is a "thinking" model; /no_think keeps its <think> block empty so
    # replies stay short and parseable.
    "/no_think"
)

model = OpenAIModel(
    client_args={
        "api_key": LLM_API_KEY,
        "base_url": LLM_BASE_URL,
        # The local server is occasionally slow/flaky; allow a long wait and
        # let the SDK retry connection errors and timeouts automatically.
        "timeout": 120,
        "max_retries": 5,
    },
    model_id=LLM_MODEL_ID,
    params={"max_tokens": 2048},
)

# A direct client for structured extraction. Strands' structured_output cannot
# parse this thinking model's output (it prefixes a <think> block), so the save
# tool talks to the server directly and we clean/parse the JSON ourselves.
llm = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL,
             timeout=120, max_retries=5)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think(text: str) -> str:
    """Remove Qwen3 <think>...</think> reasoning blocks from model output."""
    return _THINK_RE.sub("", text).strip()


def extract_json(text: str) -> str:
    """Return the first balanced {...} JSON object in text (after stripping think)."""
    text = strip_think(text)
    start = text.find("{")
    if start < 0:
        raise ValueError(f"no JSON object found in model output: {text[:200]!r}")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise ValueError("unbalanced JSON braces in model output")


# --- Structured plan the model must produce ------------------------------

class Kind(str, Enum):
    exercise = "Exercise"
    rest = "Rest"
    match = "Match"


class DayPlan(BaseModel):
    day: str = Field(description="Day of week, one of Sunday..Saturday")
    kind: Kind = Field(description="Exercise, Rest, or Match")
    activity: str = Field(
        description="Short label, e.g. '5km run', 'Rest', 'Football match'")


class WeekPlan(BaseModel):
    days: List[DayPlan] = Field(description="Exactly seven days, Sunday..Saturday")


# --- Fancy Kanban rendering, driven by the schema-file template ----------

def load_template() -> str:
    """Read the board template from fancy-kanban-schema.md (between markers)."""
    text = SCHEMA_FILE.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- ROUTINE-TEMPLATE:BEGIN -->\n(.*?)\n<!-- ROUTINE-TEMPLATE:END -->",
        text, re.DOTALL)
    return match.group(1)


def _id() -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", "<br>")


def render_kanban(week: WeekPlan) -> str:
    by_day = {d.day: d for d in week.days}
    rows = []
    for day in DAYS:
        plan = by_day.get(day)
        kind = plan.kind.value if plan else "Rest"
        activity = (plan.activity.strip() if plan and plan.activity else "")
        if not activity:
            activity = kind  # never leave a day blank (e.g. Rest days)
        rows.append(f"| {_id()} | {_escape(activity)} | {day} | {kind} |")

    return (load_template()
            .replace("{{COLUMNS}}", "|".join(DAYS))
            .replace("{{ROWS}}", "\n".join(rows)))


# --- MCP persistence -----------------------------------------------------

# --- Filesystem persistence ----------------------------------------------
# The routine is stored as a plain file in output/. (The original sample wrote
# it through an MCP document server; this standalone version writes it directly
# so no extra server is required.)

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output"
ROUTINE_PATH = OUTPUT_DIR / ROUTINE_FILE


def load_routine() -> str:
    try:
        return ROUTINE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def save_routine(text: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ROUTINE_PATH.write_text(text, encoding="utf-8")


def summarize_routine(board: str) -> str:
    """Turn the saved kanban block into plain 'Day: activity' lines.

    The stored file is a kanban board, but the user only thinks in days and
    activities — so we hand the model a plain summary, never the raw block.
    """
    activity_by_day = {}
    for line in board.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| _id") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 4:
            _, activity, day, kind = cells
            if day in DAYS:
                activity_by_day[day] = activity or kind
    return "\n".join(f"{day}: {activity_by_day[day]}"
                     for day in DAYS if day in activity_by_day)


# --- The one tool the agent can call -------------------------------------

@tool
def save_weekly_routine(agent: Agent) -> str:
    """Generate and save the user's weekly exercise routine for the whole week.

    Reads the plan from the conversation so far and stores it as a Fancy Kanban
    board. Invoked when the user explicitly asks to generate or save the routine.
    """
    # Replay the conversation so far to the model and ask for a strict JSON plan.
    # (structured_output is bypassed because this thinking model prefixes a
    # <think> block that breaks Strands' JSON parsing.)
    history = "\n".join(
        f"{m['role']}: {c['text']}"
        for m in agent.messages
        for c in m.get("content", [])
        if isinstance(c, dict) and "text" in c
    )
    instruction = (
        "/no_think Based on the conversation below, output ONLY a JSON object "
        "(no prose, no markdown) with this exact shape: "
        '{"days":[{"day":"Sunday","kind":"Exercise|Rest|Match","activity":"short label"}]} '
        "containing exactly seven days, Sunday through Saturday, in order.\n\n"
        f"Conversation:\n{history}"
    )
    response = llm.chat.completions.create(
        model=LLM_MODEL_ID,
        messages=[{"role": "user", "content": instruction}],
        max_tokens=1024,
    )
    week = WeekPlan.model_validate_json(
        extract_json(response.choices[0].message.content))
    save_routine(render_kanban(week))
    return "The weekly routine has been saved."


# --- Make stray tool-call fragments human-readable -----------------------

def humanize_tool_call(text: str):
    """If the model leaks a raw tool-call fragment, return a readable line.

    Small local models sometimes print malformed JSON like
    {"name": "save_weekly_routine", "parameters": {...}} instead of prose.
    Returns None when the text is normal, so the caller prints it unchanged.
    """
    if '"name"' not in text or '"parameters"' not in text:
        return None
    match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
    if not match:
        return None
    tool_name = match.group(1).replace("_", " ")
    return f'\u2699\ufe0f  Running \u201c{tool_name}\u201d\u2026'


# --- Chat loop -----------------------------------------------------------

# Saving is gated on an explicit save *intent* rather than the small model's
# judgment, so it never fires while merely chatting — but it recognises natural
# phrasings like "save it on my weekly plan", not just one exact command.
SAVE_VERBS = ("save", "generate", "update", "create", "store")
SAVE_TARGETS = {"routine", "plan", "week", "weekly", "schedule", "it", "this"}


def wants_to_save(text: str) -> bool:
    lowered = text.lower()
    words = set(re.findall(r"[a-z]+", lowered))
    return any(verb in lowered for verb in SAVE_VERBS) and bool(words & SAVE_TARGETS)

system_prompt = SYSTEM_PROMPT
summary = summarize_routine(load_routine())
if summary:
    system_prompt += (
        "\n\nThe user's current weekly routine is:\n\n"
        + summary + "\n\nHelp them adjust it if they ask, "
        "always speaking in days and activities.")

# No tools attached: the agent only converses (and deflects off-topic).
# Saving is handled deterministically below, not by the model's judgment.
agent = Agent(model=model, system_prompt=system_prompt,
              callback_handler=None)

print("Exercise-routine coach. Chat about your week, and ask me to "
      "'generate routine' when you're ready. '/quit' to exit.\n")

while True:
    text = input("> ")

    if text.lower() == "/quit":
        break

    if wants_to_save(text):
        print(save_weekly_routine(agent))
        print()
        continue

    reply = strip_think(str(agent(text)))
    print(humanize_tool_call(reply) or reply)
    print()
