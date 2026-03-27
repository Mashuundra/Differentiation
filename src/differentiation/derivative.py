""" Модуль с правилами дифференцирования """

from src.ast_nodes.nodes import (
    ASTNode, NumberNode, VariableNode,
    BinaryOpNode, FunctionNode, UnaryOpNode
)
from src.ast_nodes.visitor import NodeVisitor


class DifferentiationVisitor(NodeVisitor):
    """Обходит AST и применяет правила дифференцирования"""

    def __init__(self, variable: str = 'x'):
        self.variable = variable

    def visit_NumberNode(self, node: NumberNode) -> ASTNode:
        return NumberNode(0)

    def visit_VariableNode(self, node: VariableNode) -> ASTNode:
        if node.name == self.variable:
            return NumberNode(1)
        return NumberNode(0)

    def visit_BinaryOpNode(self, node: BinaryOpNode) -> ASTNode:
        left_deriv = self.visit(node.left)
        right_deriv = self.visit(node.right)

        if node.operator == '+':
            return BinaryOpNode(left_deriv, '+', right_deriv)

        elif node.operator == '-':
            return BinaryOpNode(left_deriv, '-', right_deriv)

        elif node.operator == '*':
            left_part = BinaryOpNode(left_deriv, '*', node.right)
            right_part = BinaryOpNode(node.left, '*', right_deriv)
            return BinaryOpNode(left_part, '+', right_part)

        elif node.operator == '/':
            numerator_left = BinaryOpNode(left_deriv, '*', node.right)
            numerator_right = BinaryOpNode(node.left, '*', right_deriv)
            numerator = BinaryOpNode(numerator_left, '-', numerator_right)
            denominator = BinaryOpNode(node.right, '^', NumberNode(2))
            return BinaryOpNode(numerator, '/', denominator)

        elif node.operator == '^':
            if isinstance(node.right, NumberNode):
                n = node.right.value
                new_power = NumberNode(n - 1)
                power_node = BinaryOpNode(node.left, '^', new_power)
                result = BinaryOpNode(NumberNode(n), '*', power_node)
                result = BinaryOpNode(result, '*', left_deriv)
                return result

            elif isinstance(node.left, NumberNode):
                power_node = BinaryOpNode(node.left, '^', node.right)
                ln_a = FunctionNode('ln', node.left)
                result = BinaryOpNode(power_node, '*', ln_a)
                result = BinaryOpNode(result, '*', right_deriv)
                return result

            else:
                power_node = BinaryOpNode(node.left, '^', node.right)
                ln_f = FunctionNode('ln', node.left)
                term1 = BinaryOpNode(right_deriv, '*', ln_f)
                u_deriv_over_u = BinaryOpNode(left_deriv, '/', node.left)
                term2 = BinaryOpNode(node.right, '*', u_deriv_over_u)
                sum_term = BinaryOpNode(term1, '+', term2)
                result = BinaryOpNode(power_node, '*', sum_term)
                return result

            return NumberNode(0)

    def visit_FunctionNode(self, node: FunctionNode) -> ASTNode:
        arg_deriv = self.visit(node.argument)

        if node.name == 'sin':
            cos_node = FunctionNode('cos', node.argument)
            return BinaryOpNode(cos_node, '*', arg_deriv)

        elif node.name == 'cos':
            sin_node = FunctionNode('sin', node.argument)
            neg_sin = UnaryOpNode('-', sin_node)
            return BinaryOpNode(neg_sin, '*', arg_deriv)

        elif node.name == 'tan':
            cos_node = FunctionNode('cos', node.argument)
            cos_squared = BinaryOpNode(cos_node, '^', NumberNode(2))
            one = NumberNode(1)
            sec_squared = BinaryOpNode(one, '/', cos_squared)
            return BinaryOpNode(sec_squared, '*', arg_deriv)

        elif node.name == 'ln':
            one = NumberNode(1)
            fraction = BinaryOpNode(one, '/', node.argument)
            return BinaryOpNode(fraction, '*', arg_deriv)

        elif node.name == 'exp':
            return BinaryOpNode(node, '*', arg_deriv)

        else:
            raise Exception(f"Функция {node.name} не поддерживается")

    def visit_UnaryOpNode(self, node: UnaryOpNode) -> ASTNode:
        operand_deriv = self.visit(node.operand)

        if node.operator == '-':
            return UnaryOpNode('-', operand_deriv)

        return operand_deriv
