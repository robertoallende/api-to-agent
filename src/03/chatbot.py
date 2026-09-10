import sys


def chat(text) -> str:
    lowered = text.lower()
    if "hello" in lowered:
        return "hello, how are you?"
    if "bye" in lowered:
        return "bye!, have a nice day."
    return "Beautiful weather, nothing beats Wellington on a nice day!"


if __name__ == "__main__":
    print(chat(sys.argv[1]))
