""" Тесты для модуля дифференцирования """

import pytest
from src.ast_nodes.nodes import (
    NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
)
from src.differentiation import DifferentiationVisitor, Simplifier


class TestDifferentiationVisitor:
    def setup_method(self):
        self.visitor = DifferentiationVisitor(variable='x')

    def test_constant_differentiation(self):
        node = NumberNode(5)
        result = self.visitor.visit(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_variable_differentiation(self):
        node = VariableNode('x')
        result = self.visitor.visit(node)

        assert isinstance(result, NumberNode)
        assert result.value == 1

    def test_different_variable_differentiation(self):
        node = VariableNode('t')
        result = self.visitor.visit(node)

        assert isinstance(result, NumberNode)
        assert result.value == 0

    def test_sum_differentiation(self):
        node = BinaryOpNode(VariableNode('x'), '+', NumberNode(5))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '+'
        assert isinstance(result.left, NumberNode) and result.left.value == 1
        assert isinstance(result.right, NumberNode) and result.right.value == 0

    def test_subtraction_differentiation(self):
        node = BinaryOpNode(VariableNode('x'), '-', NumberNode(5))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '-'
        assert isinstance(result.left, NumberNode) and result.left.value == 1
        assert isinstance(result.right, NumberNode) and result.right.value == 0

    def test_product_differentiation(self):
        node = BinaryOpNode(VariableNode('x'), '*', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '+'

        left_part = result.left
        right_part = result.right

        assert isinstance(left_part, BinaryOpNode) and left_part.operator == '*'
        assert isinstance(right_part, BinaryOpNode) and right_part.operator == '*'

    def test_division_differentiation(self):
        node = BinaryOpNode(VariableNode('x'), '/', NumberNode(2))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '/'

        numerator = result.left
        denominator = result.right

        assert isinstance(numerator, BinaryOpNode) and numerator.operator == '-'
        assert isinstance(denominator, BinaryOpNode) and denominator.operator == '^'

    def test_power_constant_differentiation(self):
        node = BinaryOpNode(VariableNode('x'), '^', NumberNode(3))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'

        first_part = result.left
        assert isinstance(first_part, BinaryOpNode) and first_part.operator == '*'
        assert isinstance(first_part.left, NumberNode) and first_part.left.value == 3

        second_part = result.right
        assert isinstance(second_part, NumberNode) and second_part.value == 1

    def test_power_variable_exponent_error(self):
        node = BinaryOpNode(VariableNode('x'), '^', VariableNode('x'))

        with pytest.raises(Exception, match="Степень с переменным показателем"):
            self.visitor.visit(node)

    def test_sin_differentiation(self):
        node = FunctionNode('sin', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'
        assert isinstance(result.left, FunctionNode) and result.left.name == 'cos'
        assert isinstance(result.right, NumberNode) and result.right.value == 1

    def test_cos_differentiation(self):
        node = FunctionNode('cos', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'
        assert isinstance(result.left, UnaryOpNode) and result.left.operator == '-'
        assert isinstance(result.left.operand, FunctionNode) and result.left.operand.name == 'sin'
        assert isinstance(result.right, NumberNode) and result.right.value == 1

    def test_ln_differentiation(self):
        node = FunctionNode('ln', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'
        assert isinstance(result.left, BinaryOpNode) and result.left.operator == '/'
        assert isinstance(result.right, NumberNode) and result.right.value == 1

    def test_exp_differentiation(self):
        node = FunctionNode('exp', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'
        assert isinstance(result.left, FunctionNode) and result.left.name == 'exp'
        assert isinstance(result.right, NumberNode) and result.right.value == 1

    def test_chain_rule(self):
        inner = BinaryOpNode(NumberNode(2), '*', VariableNode('x'))
        node = FunctionNode('sin', inner)
        result = self.visitor.visit(node)

        assert isinstance(result, BinaryOpNode)
        assert result.operator == '*'
        assert isinstance(result.left, FunctionNode) and result.left.name == 'cos'

        right_part = result.right

        def find_number(node, value):
            if isinstance(node, NumberNode) and node.value == value:
                return True
            if isinstance(node, BinaryOpNode):
                return find_number(node.left, value) or find_number(node.right, value)
            return False

        assert find_number(right_part, 2), "В производной должно быть число 2"

    def test_unary_minus(self):
        node = UnaryOpNode('-', VariableNode('x'))
        result = self.visitor.visit(node)

        assert isinstance(result, UnaryOpNode)
        assert result.operator == '-'
        assert isinstance(result.operand, NumberNode) and result.operand.value == 1
