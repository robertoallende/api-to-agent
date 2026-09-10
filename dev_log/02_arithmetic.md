# Unit 02: arithmetic

## Objective

Show a function that does numeric work — `g(x) = x + x` — and expose the classic
string-vs-number pitfall with command-line input (`src/02`).

## Implementation

- `src/02/g.py` — reads `sys.argv[1]`, converts it with `int()`, and prints `x + x`.
- Without the conversion, `10` would concatenate to `1010`; with `int()`, it adds to
  `20`.

## AI Interactions

- Fixed the original string-addition behavior by wrapping the argument in `int()`.
- Verified `g.py 10` → `20`.

## Files Modified

- `src/02/g.py`

## Status: Complete
