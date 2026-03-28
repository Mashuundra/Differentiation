from derivative_solver import solve_derivative


def main() -> None:
    print("Введите математическое выражение для дифференцирования")
    print("Введите 'help' для справки")
    print("Введите 'exit' или 'quit' для выхода")

    while True:
        try:
            user_input = input("\n>>> ").strip()

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("До свидания!")
                break

            elif user_input.lower() in ['help', 'h', '?']:
                show_help()
                continue

            result = solve_derivative(user_input)
            print(f"  diff({user_input}, x) -> {result}")

        except KeyboardInterrupt:
            print("\n\nДо свидания!")
            break

        except Exception as e:
            print(f"  Ошибка: {e}")


def show_help() -> None:
    help_message = (
        "Справка:\n"
        "Поддерживаемые операции:\n"
        "  +  - сложение\n"
        "  -  - вычитание\n"
        "  *  - умножение\n"
        "  /  - деление\n"
        "  ^  - возведение в степень\n"
        "  () - скобки\n\n"
        "Поддерживаемые функции:\n"
        "  sin(x) - синус\n"
        "  cos(x) - косинус\n"
        "  tan(x) - тангенс\n"
        "  ln(x)  - натуральный логарифм\n"
        "  exp(x) - экспонента\n\n"
        "Поддерживается неявное умножение:\n"
        "  2x → 2*x\n"
        "  x(x+1) → x*(x+1)\n\n"
        "Примеры выражений:\n"
        "  x^2\n"
        "  sin(x)^2\n"
        "  ln(x) * cos(x)\n\n"
        "Команды:\n"
        "  help, h, ?  - показать эту справку\n"
        "  exit, quit, q - выйти из программы")
    print(help_message)


if __name__ == '__main__':
    main()
