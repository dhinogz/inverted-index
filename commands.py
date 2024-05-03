import pickle
from quotes import get_all_quotes

QUOTES_PICKLE_FILENAME = "quotes.pkl"


def handle_command(command: str, args: list[str]) -> None:
    match command:
        case "build":
            if len(args) > 0:
                print("build does not take arguments")
                return
            build()
        case "load":
            if len(args) > 0:
                print("load does not take arguments")
                return
            load()
        case "print":
            if len(args) != 1:
                print("print must receive an argument")
                return
            print_command(args[0])
        case "find":
            if len(args) <= 0:
                print("find must receive an argument")
                return
            find(args)
        case _:
            print("no command given")


def build():
    quotes: dict[str, int] = get_all_quotes()
    with open(QUOTES_PICKLE_FILENAME, "wb") as writer:
        pickle.dump(quotes, writer)


def load():
    try:
        with open(QUOTES_PICKLE_FILENAME, "rb") as reader:
            quotes: dict[str, int] = pickle.load(reader)
            _ = quotes
    except FileNotFoundError:
        print("reverse index has not been build yet")
        return

    print("loaded")


def print_command(word: str):
    try:
        with open(QUOTES_PICKLE_FILENAME, "rb") as reader:
            quotes: dict[str, int] = pickle.load(reader)
    except FileNotFoundError:
        print("reverse index has not been build yet")
        return

    try:
        print(quotes[word])
    except KeyError:
        print(f"word {word} not in index")


def find(words: list[str]):
    try:
        with open(QUOTES_PICKLE_FILENAME, "rb") as reader:
            quotes: dict[str, int] = pickle.load(reader)
    except FileNotFoundError:
        print("reverse index has not been build yet")
        return

    try:
        res = []
        for w in words:
            res.append(quotes[w])
        if len(res) > 1:
            pages = list(set(res[0]).intersection(*res[1:]))
        else:
            pages = res[0]
        print(pages)

    except KeyError:
        print("word not in index")
