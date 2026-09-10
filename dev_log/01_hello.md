# Unit 01: hello

## Objective

Establish the very first step of the talk: a program that runs and prints, then a
first function that takes input. Two samples: Hello World (`src/00`) and a function
`f(x)` fed from the console (`src/01`).

## Implementation

- `src/00/hello.py` — a `main()` that prints `Hello, World!`, guarded by
  `if __name__ == "__main__"`.
- `src/01/f.py` — a function `f(x)` that prints its argument, with `x` supplied on
  the command line via `sys.argv[1]` (`python f.py 10` prints `10`).

The point of the unit is the leap from "code that runs" to "code that takes input":
`sys.argv[1]` is always a string, which sets up the next unit.

## AI Interactions

- Generated Hello World and verified it prints `Hello, World!`.
- Turned `f(x)` into a console-argument program and confirmed `f.py 10` → `10`.

## Files Modified

- `src/00/hello.py`
- `src/01/f.py`

## Status: Complete
