import json
import urllib.request


def chat(astring) -> str:
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps({
            "model": "llama3.2",
            "prompt": astring,
            "stream": False,
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    response = urllib.request.urlopen(request)
    return json.load(response)["response"]


def is_happy(question, answer) -> bool:
    verdict = chat(
        "You are a strict classifier. "
        "Reply with ONLY the word true or false, nothing else.\n"
        "Is the answer below happy, cheerful, and positive?\n"
        "Answer: " + answer
    )
    # The model replies with free text (e.g. "True.", "false, because...").
    # Normalise it into a real boolean so the flow is reliable.
    return "true" in verdict.strip().lower()


GENERATE_PROMPT = (
    "Give me a very happy, cheerful, and positive answer for this. "
    "You can even quote lyrics from happy songs. Here it is: "
)

MAX_TRIES = 3

while True:
    text = input("> ")

    if text.lower() == "/quit":
        break

    answer = chat(GENERATE_PROMPT + text)

    tries = 1
    while not is_happy(text, answer) and tries < MAX_TRIES:
        print("<Not happy enough, calling chat again>")
        answer = chat(GENERATE_PROMPT + text)
        tries += 1

    print(answer)
    print()
