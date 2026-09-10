# Unit 01: hello - Completion Context

## What Was Implemented

Two runnable samples: `src/00/hello.py` (prints `Hello, World!`) and `src/01/f.py`
(a function `f(x)` printing an argument taken from `sys.argv[1]`).

## Key Decisions

- Combined the two smallest samples into a single unit, per the agreed mapping
  (`src/00` + `src/01` = unit 01).
- Used `sys.argv` rather than `input()` at this stage — the interactive loop is
  introduced later (unit 04).

## Deviations from Plan

None.

## Files Modified

- `src/00/hello.py`
- `src/01/f.py`

## Integration Notes

`sys.argv[1]` returns a string. This is the setup for unit 02, where the string vs
number distinction becomes the teaching point.

## Lessons Learned

Starting from the absolute minimum (print, then one input) makes the later jump to
LLMs feel continuous rather than magical.
