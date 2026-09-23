# Noul (TypeSafe primitive)

Source: https://docs.typesafe.ai/primitives/noul.md (fetched 2026-09-23)

A **Noul** asks the model a yes/no question and returns the **probability that the
answer is yes** — a single number in [0, 1]. There is no separate `confidence` value
for a Noul (unlike Choice/Score): the one `noul` number describes the whole
two-outcome distribution.

- Near 1 = strong yes. Near 0 = strong no. Near 0.5 = model splits evenly.
- The value is *probability of yes*, NOT a degree/intensity scale. For "degree", use a
  Score instead.

## Request

Top-level fields: `state` (content to evaluate), `model`, `questions` (map of id -> question).

Each Noul question:
- `type`: always `"noul"`.
- `instructions`: the yes/no question or a statement to judge.
- `criteria` (optional): object with `true` and `false` descriptions clarifying what a
  yes vs a no means. Add it only when the boundary is subtle; try with and without.

Question ids (e.g. `is_human_escalation`) are chosen by you, are NOT sent to the model,
and key the answers in the response.

## Python SDK example

```python
from typesafe_sdk import Noul, NoulCriteria, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        model="jev-latest",
        state="I have asked three times now. Can I please just talk to a real person?",
        questions={
            "is_human_escalation": Noul(
                instructions="Is the customer asking for a human agent?",
            ),
            "is_repeat_contact": Noul(
                instructions="Has the customer contacted support about this before?",
                criteria=NoulCriteria(
                    true="Mentions a prior attempt, ticket, or that they have asked before",
                    false="No sign of any previous contact",
                ),
            ),
        },
    )
    print(response.answers["is_human_escalation"].noul)  # e.g. 0.99
    print(response.answers["is_repeat_contact"].noul)    # e.g. 0.93
```

Response shape:

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_human_escalation": { "type": "noul", "noul": 0.99 },
    "is_repeat_contact":   { "type": "noul", "noul": 0.93 }
  },
  "usage": { "input_tokens": 360, "output_tokens": 39 }
}
```

## Thresholding (the "preparation" you do in code)

You turn the probability into a boolean with a threshold you own:

```python
wants_human = response.answers["is_human_escalation"].noul > 0.9
```

- Use 0.5 when yes/no are equally easy to act on.
- Raise it when a false yes is expensive; lower it when missing a true yes is expensive.
- Middle values can be routed to a human / a different path.

## Writing good Noul questions

- One yes/no proposition per Noul. Don't combine ("angry AND asking for refund") — split
  into two Nouls and combine in code.
- Phrase so a HIGH value means yes. Avoid inverted phrasing ("Is it free of X?").
- Make the yes/no boundary unambiguous; add `criteria` when it's subtle.
- Ask many Nouls in one call (parallel, barely changes latency).
- `instructions` may be a string, object, or array; start with a string, use an object
  when you need to attach data.
</content>
