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


memory = ""

while True:
    text = input("> ")

    if text.lower() == "/quit":
        break

    prompt = memory + "User: " + text + "\nAssistant: "
    answer = chat(prompt)

    print(answer)
    print()

    memory = prompt + answer + "\n"
