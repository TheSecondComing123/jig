from sys import argv

from jig import run


def repl():
    print("jig repl")
    env = {}
    while True:
        try:
            code = input("$ ")
            if code.strip().lower() in ["", "exit", "quit", "e", "q"]:
                break
            print(f"> {run(code, env)}")
        except EOFError:
            break
        except Exception as err:
            print(f"error: {getattr(err, 'orig_exc', err)}")


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
