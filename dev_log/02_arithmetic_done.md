# Unit 02: arithmetic - Completion Context

## What Was Implemented

`src/02/g.py`: `g(x) = x + x` with the command-line argument converted to an integer
so the addition is numeric.

## Key Decisions

- Used `int()` rather than `float()` to keep the example simple; `float()` is noted
  as the alternative if decimals are wanted.

## Deviations from Plan

None.

## Files Modified

- `src/02/g.py`

## Integration Notes

Reinforces the "input is a string" lesson from unit 01 and demonstrates
deterministic behavior — the contrast the talk later draws against the
non-determinism of LLMs.

## Lessons Learned

A one-line change (`int(...)`) makes a memorable teaching moment about types.
