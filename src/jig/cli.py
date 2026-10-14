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
            value = run(code, env)
            if value is not None:
                print(f"> {value}")
        except EOFError:
            break
        except Exception as err:  # noqa: BLE001
            print(f"error: {getattr(err, 'orig_exc', err)}")


def main():
    if len(argv) == 1:
        repl()
    if len(argv) > 1:
        if argv[1] == "-e":
            value = run(argv[2])
        else:
            with open(argv[1], "r") as f:
                value = run(f.read())
        if value is not None:
            print(value)


if __name__ == "__main__":
    main()
