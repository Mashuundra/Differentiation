""" Тесты для модуля упрощения выражений """

import pytest
from src.ast_nodes.nodes import (
    NumberNode, VariableNode, BinaryOpNode, UnaryOpNode, FunctionNode
)
from src.differentiation.simplifier import Simplifier


class TestSimplifier:
    def setup_method(self):
        self.simplifier = Simplifier()

    # сложение
    def test_simplify_zero_plus_expr(self):
        node = BinaryOpNode(NumberNode(0), '+', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_expr_plus_zero(self):
        node = BinaryOpNode(VariableNode('x'), '+', NumberNode(0))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_number_addition(self):
        node = BinaryOpNode(NumberNode(2), '+', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 5

    def test_simplify_negative_number_addition(self):
        node = BinaryOpNode(NumberNode(-2), '+', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 1

    def test_simplify_float_addition(self):
        node = BinaryOpNode(NumberNode(2.5), '+', NumberNode(3.7))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 6.2

    # вычитание
    def test_simplify_expr_minus_zero(self):
        node = BinaryOpNode(VariableNode('x'), '-', NumberNode(0))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_number_subtraction(self):
        node = BinaryOpNode(NumberNode(5), '-', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 2

    def test_simplify_negative_subtraction(self):
        node = BinaryOpNode(NumberNode(5), '-', UnaryOpNode('-', NumberNode(3)))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 8

    # умножение
    def test_simplify_one_times_expr(self):
        node = BinaryOpNode(NumberNode(1), '*', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_expr_times_one(self):
        node = BinaryOpNode(VariableNode('x'), '*', NumberNode(1))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_zero_times_expr(self):
        node = BinaryOpNode(NumberNode(0), '*', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_simplify_expr_times_zero(self):
        node = BinaryOpNode(VariableNode('x'), '*', NumberNode(0))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_simplify_number_multiplication(self):
        node = BinaryOpNode(NumberNode(2), '*', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 6

    def test_simplify_negative_multiplication(self):
        node = BinaryOpNode(NumberNode(-2), '*', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == -6

    def test_simplify_x_times_x(self):
        node = BinaryOpNode(VariableNode('x'), '*', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '^'
        assert isinstance(result.left, VariableNode)
        assert result.left.name == 'x'
        assert isinstance(result.right, NumberNode)
        assert result.right.value == 2

    # деление
    def test_simplify_expr_divided_by_one(self):
        node = BinaryOpNode(VariableNode('x'), '/', NumberNode(1))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_zero_divided_by_expr(self):
        node = BinaryOpNode(NumberNode(0), '/', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_simplify_number_division(self):
        node = BinaryOpNode(NumberNode(6), '/', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 2

    def test_simplify_float_division(self):
        node = BinaryOpNode(NumberNode(5), '/', NumberNode(2))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 2.5

    # степень
    def test_simplify_power_one(self):
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(1))
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_power_zero(self):
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(0))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 1

    def test_simplify_one_power_expr(self):
        node = BinaryOpNode(NumberNode(1), '^', VariableNode('x'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 1

    def test_simplify_zero_power_positive(self):
        node = BinaryOpNode(NumberNode(0), '^', NumberNode(2))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_simplify_number_power(self):
        node = BinaryOpNode(NumberNode(2), '^', NumberNode(3))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 8

    # унарные операции
    def test_simplify_negative_zero(self):
        node = UnaryOpNode('-', NumberNode(0))
        result = self.simplifier.simplify(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_simplify_double_negative(self):
        inner = UnaryOpNode('-', VariableNode('x'))
        node = UnaryOpNode('-', inner)
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    # комбинированные тесты
    def test_simplify_complex_expression_2(self):
        left = BinaryOpNode(VariableNode('x'), '^', NumberNode(1))
        right = BinaryOpNode(VariableNode('x'), '^', NumberNode(0))
        node = BinaryOpNode(left, '*', right)
        result = self.simplifier.simplify(node)

        assert isinstance(result, VariableNode)
        assert result.name == 'x'

    def test_simplify_with_function(self):
        inner = BinaryOpNode(NumberNode(0), '+', VariableNode('x'))
        node = FunctionNode('sin', inner)
        result = self.simplifier.simplify(node)

        assert isinstance(result, FunctionNode)
        assert result.name == 'sin'
        assert isinstance(result.argument, VariableNode)
        assert result.argument.name == 'x'

    # не упрощающиеся выражения
    def test_simplify_no_change_for_complex(self):
        node = BinaryOpNode(VariableNode('x'), '+', VariableNode('y'))
        result = self.simplifier.simplify(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '+'
        assert isinstance(result.left, VariableNode) and result.left.name == 'x'
        assert isinstance(result.right, VariableNode) and result.right.name == 'y'

    def test_simplify_no_change_for_power(self):
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(2))
        result = self.simplifier.simplify(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '^'
        assert isinstance(result.left, VariableNode)
        assert isinstance(result.right, NumberNode) and result.right.value == 2
