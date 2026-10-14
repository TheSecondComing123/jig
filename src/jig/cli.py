from sys import argv

from jig import run


def repl():
    print("jig repl")
    while True:
        try:
            code = input("$ ")
            if code.strip().lower() in ["", "exit", "quit", "e", "q"]:
                break
            print(f"> {run(code)}")
        except EOFError:
            break


def main():
    if len(argv) == 1:
        repl()
    if len(argv) > 1:
        if argv[1] == "-e":
            print(run(argv[2]))
        else:
            with open(argv[1], "r") as f:
                print(run(f.read()))


if __name__ == "__main__":
    main()
