import json
import urllib.request

MYAPP_PROMPT = (
    "Let's play the cynic game. "
    "For anything I write, you answer with Yes, whatever.\n\n"
)


def chat(astring) -> str:
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps({
            "model": "llama3.2",
            "prompt": MYAPP_PROMPT + astring,
            "stream": False,
        }).encode(),
        headers={"Content-Type": "application/json"},
    )
    response = urllib.request.urlopen(request)
    return json.load(response)["response"]


while True:
    text = input("> ")

    if text.lower() == "/quit":
        break

    print(chat(text))
    print()
