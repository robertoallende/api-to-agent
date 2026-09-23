import os
import re
from pathlib import Path

from strands import Agent
from strands.models.openai import OpenAIModel
from typesafe_sdk import Noul, TypeSafeClient

# --- Model / server wiring (from unit 12) --------------------------------

LLM_BASE_URL = "http://10.130.2.57:8080/v1"
LLM_API_KEY = "EMPTY"  # local server; the key is required but unused
LLM_MODEL_ID = "mlx-community/Qwen3-8B-4bit"

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

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_think(text: str) -> str:
    """Remove Qwen3 <think>...</think> reasoning blocks from model output."""
    return _THINK_RE.sub("", text).strip()


# --- TypeSafe judge credentials ------------------------------------------
# The API key lives in src/14/.credentials (git-ignored), a 2-line file:
#   name: <account>
#   key:  <api key>
# We load the key into TYPESAFE_API_KEY, which the SDK reads. The value is
# never printed.

def _load_typesafe_key() -> None:
    creds = Path(__file__).with_name(".credentials")
    for line in creds.read_text(encoding="utf-8").splitlines():
        if line.strip().lower().startswith("key:"):
            os.environ["TYPESAFE_API_KEY"] = line.split(":", 1)[1].strip()
            return
    raise RuntimeError(f"no 'key:' line found in {creds}")


_load_typesafe_key()
judge_client = TypeSafeClient()


# --- Personas: generate prompts (from units 08 and 09) -------------------

GENERATE_PROMPTS = {
    "cynical": "Give me a cynical answer for this: ",
    "happy": (
        "Give me a very happy, cheerful, and positive answer for this. "
        "You can even quote lyrics from happy songs. Here it is: "
    ),
}


# --- The judge: a TypeSafe Noul (typed yes/no with a calibrated probability) --

MAX_TRIES = 3

# TypeSafe's model and the threshold for "enough". A Noul returns p(yes) in
# [0, 1]; "enough" means the probability clears the threshold. Tune on real
# examples: raise for stricter, lower for looser.
JUDGE_LABEL = "jev"
JUDGE_THRESHOLD = 0.6

JUDGE_QUESTIONS = {
    "cynical": "Is this answer cynical, pessimistic, or dismissive?",
    "happy": "Is this answer happy, cheerful, and positive?",
}

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
    """Judge the answer with a TypeSafe Noul. Returns whether it is 'enough'.

    Instead of prompting an LLM to reply 'true'/'false' and parsing the text
    (units 08/09/13), we ask a typed yes/no Noul and get back a calibrated
    probability we threshold in code.
    """
    response = judge_client.system_one(
        model="jev-latest",
        state=answer,
        questions={mode: Noul(instructions=JUDGE_QUESTIONS[mode])},
    )
    probability = response.answers[mode].noul
    judge_note(f"{JUDGE_LABEL} is deciding if this answer is {mode} enough\u2026 "
               f"p({mode})={probability:.2f}")
    return probability >= JUDGE_THRESHOLD


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
