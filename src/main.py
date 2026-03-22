import re
from derivative_solver import solve_derivative


def main() -> None:
    print("Введите математическое выражение для дифференцирования")
    print("Введите 'help' для справки")
    print("Введите 'exit' или 'quit' для выхода")

    while True:
        try:
            user_input = input("\n>>> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("До свидания!")
                break

            elif user_input.lower() in ['help', 'h', '?']:
                show_help()
                continue

            is_valid, error_message = is_valid_expression(user_input)

            if is_valid:
                result = solve_derivative(user_input)
                print(f"  Производная вашей функции: {result}")
            else:
                print(f"  Ошибка: {error_message}")

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


def is_valid_expression(expression: str) -> tuple[bool, str]:
    expr = expression.replace(' ', '')

    if not expr:
        return False, "Выражение не может быть пустым"

    pattern = r'^[0-9+\-*/^()x.,sincostanlnexp]+$'
    if not re.match(pattern, expr):
        invalid_chars = set()
        for char in expr:
            if not re.match(r'[0-9+\-*/^()x.,]', char) and not char.isalpha():
                invalid_chars.add(char)
        return False, f"Недопустимые символы"

    balance = 0
    for char in expr:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance < 0:
            return False, "Лишняя закрывающая скобка"
    if balance != 0:
        return False, f"Незакрытых скобок: {balance}"

    if expr[0] in '*/^':
        return False, f"Выражение не может начинаться с оператора"
    if expr[-1] in '+-*/^':
        return False, f"Выражение не может заканчиваться оператором"

    if re.search(r'[\+\-\*/^]{2,}', expr):
        return False, "Два оператора подряд"

    if '()' in expr:
        return False, "Пустые скобки"

    return True, ""


if __name__ == '__main__':
    main()
