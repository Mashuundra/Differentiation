"""Тесты для AST узлов и Visitor паттерна."""

import pytest
from src.ast_nodes import (
    NumberNode, VariableNode, BinaryOpNode, UnaryOpNode, FunctionNode
)
from src.ast_nodes.visitor import NodeVisitor


class TestASTNodes:
    """Тесты для узлов AST."""

    def test_number_node(self):
        node = NumberNode(42.0)
        assert node.value == 42.0
        assert repr(node) == "Number(42.0)"

    def test_variable_node(self):
        node = VariableNode('x')
        assert node.name == 'x'
        assert repr(node) == "Variable(x)"

    def test_binary_op_node(self):
        left = NumberNode(2.0)
        right = NumberNode(3.0)
        node = BinaryOpNode(left, '+', right)
        assert node.operator == '+'
        assert node.left == left
        assert node.right == right
        assert repr(node) == "BinaryOp(Number(2.0), +, Number(3.0))"

    def test_unary_op_node(self):
        operand = VariableNode('x')
        node = UnaryOpNode('-', operand)
        assert node.operator == '-'
        assert node.operand == operand
        assert repr(node) == "UnaryOp(-, Variable(x))"

    def test_function_node(self):
        arg = VariableNode('x')
        node = FunctionNode('sin', arg)
        assert node.name == 'sin'
        assert node.argument == arg
        assert repr(node) == "Function(sin, Variable(x))"


class TestNodeVisitor:
    """Тесты для Visitor паттерна."""

    def test_basic_visitor(self):
        class TestVisitor(NodeVisitor):
            def __init__(self):
                self.visited = []

            def visit_NumberNode(self, node):
                self.visited.append(('Number', node.value))

            def visit_VariableNode(self, node):
                self.visited.append(('Variable', node.name))

            def visit_BinaryOpNode(self, node):
                self.visited.append(('BinaryOp', node.operator))
                self.visit(node.left)
                self.visit(node.right)

        ast = BinaryOpNode(
            NumberNode(2.0),
            '+',
            VariableNode('x')
        )

        visitor = TestVisitor()
        visitor.visit(ast)

        assert len(visitor.visited) == 3
        assert visitor.visited[0] == ('BinaryOp', '+')
        assert visitor.visited[1] == ('Number', 2.0)
        assert visitor.visited[2] == ('Variable', 'x')

    def test_visitor_with_function(self):
        class FunctionVisitor(NodeVisitor):
            def __init__(self):
                self.functions = []

            def visit_FunctionNode(self, node):
                self.functions.append(node.name)
                self.visit(node.argument)

            def generic_visit(self, node):
                pass

        ast = FunctionNode(
            'sin',
            FunctionNode('cos', VariableNode('x'))
        )

        visitor = FunctionVisitor()
        visitor.visit(ast)

        assert visitor.functions == ['sin', 'cos']