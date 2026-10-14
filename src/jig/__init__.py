def main():
    print("hi")


from .eval import evaluate


def run(src):
    return evaluate(src)


if __name__ == "__main__":
    main()
