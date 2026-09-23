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
    # Happy answers (with lyrics) can run long; give headroom so a generation
    # is not cut off mid-answer.
    params={"max_tokens": 4096},
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


# --- The ranker: TypeSafe Nouls score candidates, code sorts them --------

N_CANDIDATES = 5

# TypeSafe's model label (shown on screen) and the yes/no question per mode.
# A Noul returns p(yes) in [0, 1]; we rank candidates by that probability.
JUDGE_LABEL = "jev"

JUDGE_QUESTIONS = {
    "cynical": "Is this answer cynical, pessimistic, or dismissive?",
    "happy": "Is this answer happy, cheerful, and positive?",
}

# Human-readable trait words for the ranking header, per mode.
TRAIT_NOUN = {"cynical": "cynicism", "happy": "happiness"}

# Judge/self-check output is printed dim so it stands out from the actual chat
# answers. ANSI codes degrade gracefully when the output is piped to a file.
_DIM = "\033[2m"          # dim gray — the judge being called
_RESET = "\033[0m"


def judge_note(message: str) -> None:
    """Print the Jev-activity status line, dimmed and set apart from the chat."""
    print(f"{_DIM}{message}{_RESET}")


def rank_candidates(mode: str, candidates: list[str]) -> list[tuple[str, float]]:
    """Score every candidate with one TypeSafe call and sort them, best first.

    Instead of a pass/fail gate (unit 14), we ask one Noul per candidate in a
    single batched call and use the calibrated probabilities to order them:
    the most cynical (or most happy) answer comes first.
    """
    judge_note(f"{JUDGE_LABEL} is ranking {len(candidates)} answers "
               f"by how {mode} they are\u2026")
    # One Noul per candidate, all in one call. Each question carries its own
    # candidate text via structured instructions, so it judges that answer.
    questions = {
        f"answer_{i}": Noul(instructions={
            "answer": candidate,
            "question": JUDGE_QUESTIONS[mode],
        })
        for i, candidate in enumerate(candidates)
    }
    response = judge_client.system_one(
        model="jev-latest",
        state={"note": "Score each answer independently."},
        questions=questions,
    )
    scored = [
        (candidates[i], response.answers[f"answer_{i}"].noul)
        for i in range(len(candidates))
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored


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

    # cynical / happy: generate several answers, then rank them by the trait.
    prompt = GENERATE_PROMPTS[mode] + text
    candidates = []
    for _ in range(N_CANDIDATES):
        try:
            candidates.append(strip_think(str(agent(prompt))))
        except Exception as error:
            # A single over-long or failed generation should not abort the
            # whole turn; skip it and rank whatever we did get.
            judge_note(f"(skipped one answer: {type(error).__name__})")

    if not candidates:
        print("Could not generate any answers. Try again.")
        print()
        continue

    ranked = rank_candidates(mode, candidates)

    print()  # blank line separating the Jev activity from the results
    print(f"Ranked by {TRAIT_NOUN[mode]} (most {mode} first):")
    print()
    for position, (candidate, probability) in enumerate(ranked, start=1):
        print(f"{position}. p({mode})={probability:.2f}  {candidate}")
        print()
