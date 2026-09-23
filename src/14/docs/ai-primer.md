# AI primer — how TypeSafe's model works (and how you "prepare" it)

Source: https://docs.typesafe.ai/introduction/machine-learning-primer.md (fetched 2026-09-23)

## You do NOT train it

Jev is a pretrained "System One" model. You never train or fine-tune it. You "prepare"
it purely by **how you phrase the question** (`instructions` / `criteria`) and by the
**threshold you pick in code** for acting on its probability. No datasets, no labels,
no training loop.

## What makes it different (RLCD)

Post-training approaches:
- **RLHF** → chatbots; optimizes for responses people prefer (can reward sycophancy /
  confident hallucinations; causes "mode dropping").
- **RLVR** → reasoning models; strong at math but slower/pricier.
- **RLCD (TypeSafe)** → "Reinforcement learning for calibrated decisions." The model
  does NOT generate text; it returns **decisions + calibrated probabilities**.

## Calibration (why the probability is trustworthy)

Across many predictions from a well-calibrated model:
- outcomes assigned 0.2 occur ~20% of the time,
- outcomes assigned 0.8 occur ~80% of the time,
- outcomes assigned 1.0 occur ~100% of the time.

These are group-level rates, not a guarantee about any single answer. Calibration is
what makes the probability usable by software (thresholding, routing, escalation).

## Implication for our judge (cynical/happy "enough")

- "Enough" is a threshold decision, which is exactly what a calibrated probability is
  for: ask a Noul "Is this answer cynical?" → get p(yes) → compare to a threshold you
  choose (e.g. 0.6). Raise/lower the threshold to make "enough" stricter/looser.
- No prompt-and-parse, no `<think>` stripping, no "reply true/false" hack — the API
  returns the number directly.
</content>
