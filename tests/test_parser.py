"""Тесты для парсера математических выражений."""

import pytest
from src.parser.parser import Parser, Tokenizer
from src.parser.exceptions import InvalidExpressionError, UnexpectedTokenError
from src.ast_nodes import (
    NumberNode, VariableNode, BinaryOpNode, UnaryOpNode, FunctionNode
)


class TestTokenizer:
    """Тесты для лексического анализатора."""

    def test_tokenize_numbers(self):
        """Тест токенизации чисел."""
        tokenizer = Tokenizer("123")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == 'NUMBER'
        assert tokens[0].value == '123'

    def test_tokenize_float(self):
        """Тест токенизации вещественных чисел."""
        tokenizer = Tokenizer("3.14")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == 'NUMBER'
        assert tokens[0].value == '3.14'

    def test_tokenize_variable(self):
        """Тест токенизации переменной."""
        tokenizer = Tokenizer("x")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == 'VARIABLE'
        assert tokens[0].value == 'x'

    def test_tokenize_operators(self):
        """Тест токенизации операторов."""
        tokenizer = Tokenizer("x+y-z")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 5
        assert tokens[0].type == 'VARIABLE'
        assert tokens[1].type == 'OPERATOR' and tokens[1].value == '+'
        assert tokens[2].type == 'VARIABLE'
        assert tokens[3].type == 'OPERATOR' and tokens[3].value == '-'
        assert tokens[4].type == 'VARIABLE'

    def test_tokenize_function(self):
        """Тест токенизации функций."""
        tokenizer = Tokenizer("sin(x)")
        tokens = tokenizer.tokenize()
        assert len(tokens) == 4
        assert tokens[0].type == 'FUNCTION' and tokens[0].value == 'sin'
        assert tokens[1].type == 'LPAREN'
        assert tokens[2].type == 'VARIABLE'
        assert tokens[3].type == 'RPAREN'


class TestParser:
    """Тесты для синтаксического анализатора."""

    def setup_method(self):
        self.parser = Parser()

    def test_parse_number(self):
        """Тест парсинга числа."""
        ast = self.parser.parse("42")
        assert isinstance(ast, NumberNode)
        assert ast.value == 42.0

    def test_parse_variable(self):
        """Тест парсинга переменной."""
        ast = self.parser.parse("x")
        assert isinstance(ast, VariableNode)
        assert ast.name == 'x'

    def test_parse_addition(self):
        """Тест парсинга сложения."""
        ast = self.parser.parse("x+5")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '+'
        assert isinstance(ast.left, VariableNode)
        assert isinstance(ast.right, NumberNode)
        assert ast.right.value == 5.0

    def test_parse_subtraction(self):
        """Тест парсинга вычитания."""
        ast = self.parser.parse("x-3")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '-'

    def test_parse_multiplication(self):
        """Тест парсинга умножения."""
        ast = self.parser.parse("x*4")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '*'

    def test_parse_division(self):
        """Тест парсинга деления."""
        ast = self.parser.parse("x/2")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '/'

    def test_parse_power(self):
        """Тест парсинга степени."""
        ast = self.parser.parse("x^2")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '^'

    def test_parse_expression_with_precedence(self):
        """Тест приоритета операций."""
        ast = self.parser.parse("2+3*4")
        # 2 + (3 * 4)
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '+'
        assert isinstance(ast.right, BinaryOpNode)
        assert ast.right.operator == '*'

    def test_parse_power_precedence(self):
        """Тест приоритета степени."""
        ast = self.parser.parse("2^3+4")
        # (2^3) + 4
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '+'
        assert isinstance(ast.left, BinaryOpNode)
        assert ast.left.operator == '^'

    def test_parse_parentheses(self):
        """Тест скобок."""
        ast = self.parser.parse("(2+3)*4")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '*'
        assert isinstance(ast.left, BinaryOpNode)
        assert ast.left.operator == '+'

    def test_parse_unary_minus(self):
        """Тест унарного минуса."""
        ast = self.parser.parse("-x")
        assert isinstance(ast, UnaryOpNode)
        assert ast.operator == '-'
        assert isinstance(ast.operand, VariableNode)

    def test_parse_unary_plus(self):
        """Тест унарного плюса."""
        ast = self.parser.parse("+x")
        assert isinstance(ast, VariableNode)  # унарный плюс игнорируется

    def test_parse_function_sin(self):
        """Тест функции синуса."""
        ast = self.parser.parse("sin(x)")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'sin'
        assert isinstance(ast.argument, VariableNode)

    def test_parse_function_cos(self):
        """Тест функции косинуса."""
        ast = self.parser.parse("cos(x)")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'cos'

    def test_parse_function_tan(self):
        """Тест функции тангенса."""
        ast = self.parser.parse("tan(x)")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'tan'

    def test_parse_function_ln(self):
        """Тест натурального логарифма."""
        ast = self.parser.parse("ln(x)")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'ln'

    def test_parse_function_exp(self):
        """Тест экспоненты."""
        ast = self.parser.parse("exp(x)")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'exp'

    def test_parse_nested_function(self):
        """Тест вложенной функции."""
        ast = self.parser.parse("sin(cos(x))")
        assert isinstance(ast, FunctionNode)
        assert ast.name == 'sin'
        assert isinstance(ast.argument, FunctionNode)
        assert ast.argument.name == 'cos'

    def test_parse_implicit_multiplication_number_variable(self):
        """Тест неявного умножения числа на переменную."""
        ast = self.parser.parse("2x")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '*'
        assert isinstance(ast.left, NumberNode)
        assert ast.left.value == 2.0
        assert isinstance(ast.right, VariableNode)

    def test_parse_implicit_multiplication_variable_parentheses(self):
        """Тест неявного умножения переменной на скобки."""
        ast = self.parser.parse("x(2+3)")
        assert isinstance(ast, BinaryOpNode)
        assert ast.operator == '*'
        assert isinstance(ast.left, VariableNode)
        assert isinstance(ast.right, BinaryOpNode)

    def test_parse_complex_expression(self):
        """Тест сложного выражения."""
        ast = self.parser.parse("x^2 + 2*x + 1")
        # Проверяем структуру, но не детально
        assert isinstance(ast, BinaryOpNode)

    def test_parse_empty_expression(self):
        """Тест пустого выражения."""
        with pytest.raises(InvalidExpressionError):
            self.parser.parse("")

    def test_parse_invalid_character(self):
        """Тест недопустимого символа."""
        with pytest.raises(InvalidExpressionError):
            self.parser.parse("x@2")

    def test_parse_missing_parentheses(self):
        """Тест незакрытой скобки."""
        with pytest.raises(UnexpectedTokenError):
            self.parser.parse("(x+2")

    def test_parse_extra_parentheses(self):
        """Тест лишней закрывающей скобки."""
        with pytest.raises(UnexpectedTokenError):
            self.parser.parse("(x+2))")
