import re

from openai import OpenAI
from strands import Agent
from strands.models.openai import OpenAIModel

# --- Model / server wiring (from unit 12) --------------------------------

LLM_BASE_URL = "http://10.130.2.57:8080/v1"
LLM_API_KEY = "EMPTY"  # local server; the key is required but unused
LLM_MODEL_ID = "mlx-community/Qwen3-8B-4bit"

# The judge uses its own model id so a later subunit can point it at a
# different model without touching the loop. For now it is the same model.
JUDGE_MODEL_ID = LLM_MODEL_ID

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

# A direct client for the judge, so we can call any model id and clean its
# output ourselves (Qwen3 prefixes a <think> block).
llm = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL,
             timeout=120, max_retries=5)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think(text: str) -> str:
    """Remove Qwen3 <think>...</think> reasoning blocks from model output."""
    return _THINK_RE.sub("", text).strip()


# --- Personas: generate prompts (from units 08 and 09) -------------------

GENERATE_PROMPTS = {
    "cynical": "Give me a cynical answer for this: ",
    "happy": (
        "Give me a very happy, cheerful, and positive answer for this. "
        "You can even quote lyrics from happy songs. Here it is: "
    ),
}


# --- The judge (from units 08 and 09), on the direct client --------------

MAX_TRIES = 3

# Judge/self-check output is printed dim so it stands out from the actual chat
# answers: the judge "call" line is dim gray, the retry outcome is dim red.
# ANSI codes degrade gracefully when the output is piped to a file.
_DIM = "\033[2m"          # dim gray — the judge being called
_DIM_RED = "\033[2;31m"   # dim red  — the "not X enough" retry outcome
_RESET = "\033[0m"


def judge_note(message: str) -> None:
    """Print the judge-call status line, dimmed and set apart from the chat."""
    print(f"{_DIM}{message}{_RESET}")


def judge(mode: str, answer: str) -> bool:
    """Ask the judge model whether the answer fits the mode. Returns a bool.

    Reuses the strict-classifier + tolerant-parse approach from units 08/09,
    but calls the qwen server directly and strips Qwen3's <think> block.
    """
    trait = ("cynical, pessimistic, or dismissive" if mode == "cynical"
             else "happy, cheerful, and positive")
    judge_note(f"{JUDGE_MODEL_ID} is deciding if this answer is {mode} enough\u2026")
    response = llm.chat.completions.create(
        model=JUDGE_MODEL_ID,
        messages=[{"role": "user", "content": (
            "/no_think You are a strict classifier. "
            "Reply with ONLY the word true or false, nothing else.\n"
            f"Is the answer below {trait}?\n"
            "Answer: " + answer
        )}],
        max_tokens=64,
    )
    verdict = strip_think(response.choices[0].message.content)
    # The model replies with free text (e.g. "True.", "false, because...").
    # Normalise it into a real boolean so the flow is reliable.
    return "true" in verdict.strip().lower()


# --- Mode commands -------------------------------------------------------

MODES = ("neutral", "cynical", "happy")


# --- Chat loop -----------------------------------------------------------

agent = Agent(model=model, callback_handler=None)
mode = "neutral"

print("Mode chatbot. Modes: neutral (default), cynical, happy.\n"
      "Commands: 'mode' shows the current mode, "
      "'set mode neutral|cynical|happy' switches it, '/quit' exits.\n")

while True:
    text = input("> ")
    lowered = text.strip().lower()

    if lowered == "/quit":
        break

    if lowered == "mode":
        print(f"Current mode: {mode}")
        print()
        continue

    if lowered.startswith("set mode"):
        requested = lowered[len("set mode"):].strip()
        if requested in MODES:
            mode = requested
            print(f"Mode set to: {mode}")
        else:
            print("Usage: set mode neutral|cynical|happy")
        print()
        continue

    if mode == "neutral":
        # Plain answer, no persona, no self-check.
        print(strip_think(str(agent(text))))
        print()
        continue

    # cynical / happy: generate with the persona prompt, then judge and retry.
    prompt = GENERATE_PROMPTS[mode] + text
    answer = strip_think(str(agent(prompt)))

    tries = 1
    while not judge(mode, answer) and tries < MAX_TRIES:
        print(f"{_DIM_RED}<Not {mode} enough, calling chat again>{_RESET}")
        answer = strip_think(str(agent(prompt)))
        tries += 1

    print()  # blank line separating the judge activity from the answer
    print(answer)
    print()
