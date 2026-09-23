# TypeSafe Python SDK

Source: https://docs.typesafe.ai/sdk/python.md (fetched 2026-09-23)
SDK source: https://github.com/typesafe-ai/typesafe-sdk-python

## Install

```sh
pip install typesafe-sdk
# or: uv add typesafe-sdk
```

## Auth

Set `TYPESAFE_API_KEY` in the environment. Create a key at https://console.typesafe.ai/.
Keep the key server-side.

## Sync client (what unit 14 will use)

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state={"document": "I was charged twice. Please fix this ASAP."},
        questions={
            "billing": Noul(instructions="Is this ticket about billing?"),
            "tone": Choice(
                instructions="What is the customer's tone?",
                criteria={"calm": None, "frustrated": None, "angry": None},
            ),
            "urgency": Score(
                instructions="How urgent is this ticket?",
                criteria=["can wait", "this week", "today"],
            ),
        },
    )
    print(response.nouls["billing"].noul)     # or response.answers["billing"].noul
    print(response.choices["tone"].choice)
    print(response.scores["urgency"].score)
```

An `AsyncTypeSafeClient` exists with the same shape (`await client.system_one(...)`).

## Key facts

- Endpoint: `https://api.typesafe.ai/v1/systemone`; SDK method `client.system_one(...)`.
- `model` defaults to a current Jev; can pass `model="jev-latest"`.
- Response answers are keyed by the question ids you chose; a Noul answer's value is
  `.noul` (a float 0..1).
- The client reads `TYPESAFE_API_KEY` from the environment by default.
</content>
