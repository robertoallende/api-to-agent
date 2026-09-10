from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(host="http://localhost:11434", model_id="llama3.2")
agent = Agent(model=model, callback_handler=None)

while True:
    text = input("> ")

    if text.lower() == "/quit":
        break

    answer = agent(text)

    print(answer)
    print()
