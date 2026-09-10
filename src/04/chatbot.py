while True:
    text = input("> ")
    lowered = text.lower()

    if lowered == "/quit":
        break
    elif "hello" in lowered:
        print("hello, how are you?")
    elif "bye" in lowered:
        print("bye!, have a nice day.")
    else:
        print("Beautiful weather, nothing beats Wellington on a nice day!")

    print()
