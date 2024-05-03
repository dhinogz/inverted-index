from commands import handle_command


def main() -> None:
    try:
        while True:
            expression = input(">>> ").lower()
            if expression == "exit":
                print("Goodbye!")
                break
            else:
                parts = expression.split()
                if len(parts) < 1:
                    continue

                command = parts[0]
                args = parts[1:]

                handle_command(command, args)
    except KeyboardInterrupt:
        print("Goodbye!")


if __name__ == "__main__":
    main()
