"""Синтаксический анализатор математических выражений."""

from typing import List, Optional
from src.ast_nodes import (
    ASTNode, NumberNode, VariableNode, BinaryOpNode,
    UnaryOpNode, FunctionNode
)
from src.parser.exceptions import (
    InvalidExpressionError, UnexpectedTokenError
)

class Token:
    """Токен лексического анализатора."""

    def __init__(self, type_: str, value: str, position: int):
        self.type = type_  # 'NUMBER', 'VARIABLE', 'OPERATOR', 'FUNCTION', 'LPAREN', 'RPAREN'
        self.value = value  # значение токена
        self.position = position  # позиция в строке

    def __repr__(self):
        return f"Token({self.type}, {self.value}, pos={self.position})"


class Tokenizer:
    """Лексический анализатор.
    Преобразование строки в список токенов"""

    def __init__(self, expression: str, variable: str = 'x'):
        self.expression = expression
        self.variable = variable
        self.position = 0
        self.tokens = []

        # Функции, которые поддерживаются, можно расширить
        self.functions = {'sin', 'cos', 'tan', 'ln', 'exp'}

        # Операторы
        self.operators = {'+', '-', '*', '/', '^'}

    def tokenize(self) -> List[Token]:
        """Разбивает выражение на токены."""
        self.position = 0
        self.tokens = []

        while self.position < len(self.expression):
            char = self.expression[self.position]

            # Пропускаем пробелы
            if char.isspace():
                self.position += 1
                continue

            # Числа
            if char.isdigit() or (char == '.' and self._is_number_start()):
                token = self._read_number()
                self.tokens.append(token)
                continue

            # Буквы (функции или переменные)
            if char.isalpha():
                token = self._read_identifier()
                if token.type == 'FUNCTION':
                    self.tokens.append(token)
                elif token.type == 'VARIABLE':
                    self.tokens.append(token)
                else:
                    raise InvalidExpressionError(
                        f"Неизвестный идентификатор '{token.value}' на позиции {token.position}"
                    )
                continue

            # Операторы
            if char in self.operators:
                self.tokens.append(Token('OPERATOR', char, self.position))
                self.position += 1
                continue

            # Скобки
            if char == '(':
                self.tokens.append(Token('LPAREN', '(', self.position))
                self.position += 1
                continue

            if char == ')':
                self.tokens.append(Token('RPAREN', ')', self.position))
                self.position += 1
                continue

            # Запятая (пока не используется)
            if char == ',':
                self.tokens.append(Token('COMMA', ',', self.position))
                self.position += 1
                continue

            # Недопустимый символ
            raise InvalidExpressionError(f"Недопустимый символ '{char}' на позиции {self.position}")

        return self.tokens

    def _is_number_start(self) -> bool:
        """Проверяет, может ли текущий символ начать число."""
        if self.position + 1 >= len(self.expression):
            return False
        next_char = self.expression[self.position + 1]
        return next_char.isdigit()

    def _read_number(self) -> Token:
        """Считывает число (целое или вещественное)."""
        start_pos = self.position
        number = ""
        has_dot = False

        while self.position < len(self.expression):
            char = self.expression[self.position]
            if char.isdigit():
                number += char
            elif char == '.' and not has_dot:
                number += char
                has_dot = True
            else:
                break
            self.position += 1

        # Проверяем, что число не заканчивается на точку
        if number.endswith('.'):
            raise InvalidExpressionError(f"Некорректное число '{number}' на позиции {start_pos}")

        return Token('NUMBER', number, start_pos)

    def _read_identifier(self) -> Token:
        """Считывает идентификатор (функцию или переменную)."""
        start_pos = self.position
        identifier = ""

        while self.position < len(self.expression) and self.expression[self.position].isalpha():
            identifier += self.expression[self.position]
            self.position += 1

        # Проверяем, является ли идентификатор функцией
        if identifier in self.functions:
            return Token('FUNCTION', identifier, start_pos)
        # Иначе считаем его переменной
        else:
            return Token('VARIABLE', identifier, start_pos)

class Parser:
    """Синтаксический анализатор."""

    def __init__(self, variable: str = 'x'):
        self.variable = variable
        self.tokens: List[Token] = []
        self.position = 0

    def parse(self, expression: str) -> ASTNode:
        """Разбирает выражение и возвращает AST."""
        # Токенизация
        tokenizer = Tokenizer(expression, self.variable)
        self.tokens = tokenizer.tokenize()
        self.position = 0

        if not self.tokens:
            raise InvalidExpressionError("Выражение не может быть пустым")

        # Парсинг выражения
        result = self._parse_expression()

        # Проверяем, что все токены обработаны
        if self.position < len(self.tokens):
            raise UnexpectedTokenError(
                f"Неожиданный токен '{self.current_token().value}' на позиции {self.current_token().position}"
            )

        return result

    def current_token(self) -> Optional[Token]:
        """Возвращает текущий токен."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, expected_type: str) -> Token:
        """Потребляет токен ожидаемого типа."""
        token = self.current_token()
        if token is None:
            raise UnexpectedTokenError("Неожиданный конец выражения")

        if token.type != expected_type:
            raise UnexpectedTokenError(
                f"Ожидался токен типа {expected_type}, получен {token.type} "
                f"со значением '{token.value}' на позиции {token.position}"
            )

        self.position += 1
        return token

    def peek(self) -> Optional[Token]:
        """Просматривает следующий токен."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def _parse_expression(self) -> ASTNode:
        """Разбирает выражение (самый низкий приоритет: +, -)."""
        node = self._parse_term()

        while True:
            token = self.current_token()
            if token and token.type == 'OPERATOR' and token.value in ('+', '-'):
                operator = token.value
                self.position += 1
                right = self._parse_term()
                node = BinaryOpNode(node, operator, right)
            else:
                break

        return node

    def _parse_term(self) -> ASTNode:
        """Разбирает терм (приоритет: *, /)."""
        node = self._parse_factor()

        while True:
            token = self.current_token()
            if token and token.type == 'OPERATOR' and token.value in ('*', '/'):
                operator = token.value
                self.position += 1
                right = self._parse_factor()
                node = BinaryOpNode(node, operator, right)
            else:
                break

        return node

    def _parse_factor(self) -> ASTNode:
        """Разбирает фактор (приоритет: ^)."""
        node = self._parse_power()

        # Обработка неявного умножения (например, 2x, x(x+1))
        while True:
            next_token = self.current_token()
            if next_token and (next_token.type in ('NUMBER', 'VARIABLE', 'LPAREN', 'FUNCTION')):
                # Неявное умножение: a b → a * b
                right = self._parse_power()
                node = BinaryOpNode(node, '*', right)
            else:
                break

        return node

    def _parse_power(self) -> ASTNode:
        """Разбирает степень (правый ассоциативный)."""
        node = self._parse_unary()

        token = self.current_token()
        if token and token.type == 'OPERATOR' and token.value == '^':
            self.position += 1
            right = self._parse_power()  # правый ассоциативный
            node = BinaryOpNode(node, '^', right)

        return node

    def _parse_unary(self) -> ASTNode:
        """Разбирает унарные операторы (+ и -)."""
        token = self.current_token()

        if token and token.type == 'OPERATOR' and token.value in ('+', '-'):
            operator = token.value
            self.position += 1
            operand = self._parse_unary()
            if operator == '+':
                return operand  # унарный плюс ничего не меняет
            else:
                return UnaryOpNode('-', operand)

        return self._parse_primary()

    def _parse_primary(self) -> ASTNode:
        """Разбирает первичные выражения (числа, переменные, скобки, функции)."""
        token = self.current_token()

        if token is None:
            raise UnexpectedTokenError("Неожиданный конец выражения")

        # Число
        if token.type == 'NUMBER':
            self.position += 1
            return NumberNode(float(token.value))

        # Переменная
        if token.type == 'VARIABLE':
            self.position += 1
            return VariableNode(token.value)

        # Функция
        if token.type == 'FUNCTION':
            func_name = token.value
            self.position += 1
            # Должна быть открывающая скобка
            self.eat('LPAREN')
            argument = self._parse_expression()
            self.eat('RPAREN')
            return FunctionNode(func_name, argument)

        # Выражение в скобках
        if token.type == 'LPAREN':
            self.position += 1
            node = self._parse_expression()
            self.eat('RPAREN')
            return node

        raise UnexpectedTokenError(f"Неожиданный токен '{token.value}' на позиции {token.position}")