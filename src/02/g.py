import sys

def f(x) -> None:
    print(x+x)

if __name__ == "__main__":
    f(int(sys.argv[1]))
