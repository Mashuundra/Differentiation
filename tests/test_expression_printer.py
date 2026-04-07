""" Тесты для преобразования AST в строку """

from src.ast_nodes.nodes import (
    NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
)
from src.utils.expression_printer import to_string, to_infix_string


class TestToString:

    def test_number_to_string(self):
        # число
        node = NumberNode(42)
        assert to_string(node) == "42"

        node = NumberNode(3.14)
        assert to_string(node) == "3.14"

        node = NumberNode(5.0)
        assert to_string(node) == "5"

        node = NumberNode(-10)
        assert to_string(node) == "-10"

    def test_variable_to_string(self):
        # переменная
        node = VariableNode('x')
        assert to_string(node) == "x"

        node = VariableNode('t')
        assert to_string(node) == "t"

        node = VariableNode('y')
        assert to_string(node) == "y"

    def test_addition_to_string(self):
        # сложение
        node = BinaryOpNode(VariableNode('x'), '+', NumberNode(5))
        assert to_string(node) == "x + 5"

        node = BinaryOpNode(NumberNode(2), '+', NumberNode(3))
        assert to_string(node) == "2 + 3"

    def test_subtraction_to_string(self):
        # вычитание
        node = BinaryOpNode(VariableNode('x'), '-', NumberNode(3))
        assert to_string(node) == "x - 3"

        node = BinaryOpNode(NumberNode(5), '-', NumberNode(2))
        assert to_string(node) == "5 - 2"

    def test_multiplication_to_string(self):
        # умножение
        node = BinaryOpNode(VariableNode('x'), '*', NumberNode(2))
        assert to_string(node) == "x*2"

        node = BinaryOpNode(NumberNode(3), '*', VariableNode('x'))
        assert to_string(node) == "3*x"

    def test_division_to_string(self):
        # деление
        node = BinaryOpNode(VariableNode('x'), '/', NumberNode(2))
        assert to_string(node) == "x/2"

        node = BinaryOpNode(NumberNode(5), '/', NumberNode(2))
        assert to_string(node) == "5/2"

    def test_power_to_string(self):
        # степень
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(2))
        assert to_string(node) == "x^2"

        node = BinaryOpNode(NumberNode(2), '^', NumberNode(3))
        assert to_string(node) == "2^3"

    # скобки
    def test_parentheses_for_addition_in_multiplication(self):
        inner = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        node = BinaryOpNode(inner, '*', NumberNode(2))
        assert to_string(node) == "(x + 1)*2"

    def test_parentheses_for_subtraction_in_multiplication(self):
        inner = BinaryOpNode(VariableNode('x'), '-', NumberNode(1))
        node = BinaryOpNode(inner, '*', NumberNode(2))
        assert to_string(node) == "(x - 1)*2"

    def test_parentheses_for_multiplication_in_power(self):
        inner = BinaryOpNode(NumberNode(2), '*', VariableNode('x'))
        node = BinaryOpNode(inner, '^', NumberNode(3))
        assert to_string(node) == "(2*x)^3"

    def test_no_parentheses_for_multiplication_in_addition(self):
        left = BinaryOpNode(NumberNode(2), '*', VariableNode('x'))
        node = BinaryOpNode(left, '+', NumberNode(1))
        assert to_string(node) == "2*x + 1"

    def test_parentheses_for_addition_in_division(self):
        inner = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        node = BinaryOpNode(inner, '/', NumberNode(2))
        assert to_string(node) == "(x + 1)/2"

    def test_parentheses_for_division_in_power(self):
        inner = BinaryOpNode(VariableNode('x'), '/', NumberNode(2))
        node = BinaryOpNode(inner, '^', NumberNode(3))
        assert to_string(node) == "(x/2)^3"

    def test_complex_parentheses(self):
        left = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        right = BinaryOpNode(VariableNode('x'), '-', NumberNode(1))
        node = BinaryOpNode(left, '*', right)
        assert to_string(node) == "(x + 1)*(x - 1)"

    # функции
    def test_function_to_string(self):
        node = FunctionNode('sin', VariableNode('x'))
        assert to_string(node) == "sin(x)"

        node = FunctionNode('cos', VariableNode('x'))
        assert to_string(node) == "cos(x)"

        node = FunctionNode('tan', VariableNode('x'))
        assert to_string(node) == "tan(x)"

        node = FunctionNode('ln', VariableNode('x'))
        assert to_string(node) == "ln(x)"

        node = FunctionNode('exp', VariableNode('x'))
        assert to_string(node) == "exp(x)"

    def test_nested_function_to_string(self):
        inner = FunctionNode('cos', VariableNode('x'))
        node = FunctionNode('sin', inner)
        assert to_string(node) == "sin(cos(x))"

        inner2 = FunctionNode('sin', VariableNode('x'))
        inner1 = FunctionNode('cos', inner2)
        node = FunctionNode('tan', inner1)
        assert to_string(node) == "tan(cos(sin(x)))"

    def test_function_with_complex_argument(self):
        arg = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        node = FunctionNode('sin', arg)
        assert to_string(node) == "sin(x + 1)"

    # унарные операции
    def test_unary_minus_to_string(self):
        node = UnaryOpNode('-', VariableNode('x'))
        assert to_string(node) == "-x"

        node = UnaryOpNode('-', NumberNode(5))
        assert to_string(node) == "-5"

    def test_unary_minus_with_parentheses(self):
        inner = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        node = UnaryOpNode('-', inner)
        assert to_string(node) == "-(x + 1)"

    def test_double_unary_minus(self):
        inner = UnaryOpNode('-', VariableNode('x'))
        node = UnaryOpNode('-', inner)
        assert to_string(node) == "--x"

    # сложные выражения
    def test_complex_expression_1(self):
        # 2*x^2 + 3*x + 1
        power = BinaryOpNode(VariableNode('x'), '^', NumberNode(2))
        term1 = BinaryOpNode(NumberNode(2), '*', power)
        term2 = BinaryOpNode(NumberNode(3), '*', VariableNode('x'))
        sum1 = BinaryOpNode(term1, '+', term2)
        node = BinaryOpNode(sum1, '+', NumberNode(1))

        result = to_string(node)
        assert "2*x^2" in result
        assert "3*x" in result
        assert "+ 1" in result or "+1" in result

    def test_complex_expression_2(self):
        # sin(x)^2 + cos(x)^2
        sin_power = BinaryOpNode(
            FunctionNode('sin', VariableNode('x')),
            '^',
            NumberNode(2)
        )
        cos_power = BinaryOpNode(
            FunctionNode('cos', VariableNode('x')),
            '^',
            NumberNode(2)
        )
        node = BinaryOpNode(sin_power, '+', cos_power)

        result = to_string(node)
        assert "sin(x)^2" in result
        assert "cos(x)^2" in result
        assert "+" in result

    def test_expression_with_negative_number(self):
        node = BinaryOpNode(VariableNode('x'), '+', NumberNode(-5))
        assert to_string(node) == "x + -5"

    def test_expression_with_negative_in_multiplication(self):
        node = BinaryOpNode(VariableNode('x'), '*', NumberNode(-5))
        assert to_string(node) == "x*-5"


class TestToInfixString:
    # тесты со скобками

    def test_addition_infix(self):
        node = BinaryOpNode(VariableNode('x'), '+', NumberNode(5))
        assert to_infix_string(node) == "(x + 5)"

    def test_complex_infix(self):
        left = BinaryOpNode(NumberNode(2), '*', VariableNode('x'))
        node = BinaryOpNode(left, '+', NumberNode(1))
        assert to_infix_string(node) == "((2 * x) + 1)"

    def test_power_infix(self):
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(2))
        assert to_infix_string(node) == "(x ^ 2)"

    def test_nested_infix(self):
        inner = BinaryOpNode(VariableNode('x'), '+', NumberNode(1))
        node = FunctionNode('sin', inner)
        assert to_infix_string(node) == "sin((x + 1))"
