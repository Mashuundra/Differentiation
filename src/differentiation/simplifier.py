""" Модуль упрощения математических выражений """

from src.ast_nodes.nodes import (
    ASTNode, NumberNode, VariableNode,
    BinaryOpNode, UnaryOpNode, FunctionNode
)


def _is_number(node, value=None):
    if not isinstance(node, NumberNode):
        return False
    if value is not None:
        return node.value == value
    return True


def _is_variable(node, name=None):
    if not isinstance(node, VariableNode):
        return False
    if name is not None:
        return node.name == name
    return True


def _is_unary_minus(node):
    return isinstance(node, UnaryOpNode) and node.operator == '-'


class Simplifier:

    def simplify(self, node: ASTNode) -> ASTNode:
        prev = None
        current = node
        while str(prev) != str(current):
            prev = current
            current = self._simplify_once(current)
        return current

    def _simplify_once(self, node: ASTNode) -> ASTNode:
        if isinstance(node, BinaryOpNode):
            return self._simplify_binary(node)
        elif isinstance(node, UnaryOpNode):
            return self._simplify_unary(node)
        elif isinstance(node, FunctionNode):
            simplified_arg = self._simplify_once(node.argument)
            return self._simplify_function(FunctionNode(node.name, simplified_arg))
        return node

    def _simplify_function(self, node: FunctionNode) -> ASTNode:
        if node.name == 'ln':
            if isinstance(node.argument, VariableNode) and node.argument.name == 'e':
                return NumberNode(1)

            if isinstance(node.argument, BinaryOpNode) and node.argument.operator == '^':
                if isinstance(node.argument.left, VariableNode) and node.argument.left.name == 'e':
                    return self._simplify_once(node.argument.right)

            if _is_number(node.argument, 1):
                return NumberNode(0)


        elif node.name == 'exp':
            if _is_number(node.argument, 0):
                return NumberNode(1)

            if _is_number(node.argument, 1):
                return VariableNode('e')

        elif node.name == 'sin':
            if _is_number(node.argument, 0):
                return NumberNode(0)

        elif node.name == 'cos':
            if _is_number(node.argument, 0):
                return NumberNode(1)

        if node.argument != node.argument:
            return FunctionNode(node.name, node.argument)

        return node

    def _collect_factors(self, node, factors):
        """Собирает все множители из цепочки умножения"""
        if isinstance(node, BinaryOpNode) and node.operator == '*':
            self._collect_factors(node.left, factors)
            self._collect_factors(node.right, factors)
        else:
            factors.append(node)

    def _simplify_binary(self, node: BinaryOpNode) -> ASTNode:
        left = self._simplify_once(node.left)
        right = self._simplify_once(node.right)

        if node.operator == '+':
            if _is_number(left, 0):
                return right
            if _is_number(right, 0):
                return left
            if _is_unary_minus(right):
                return BinaryOpNode(left, '-', right.operand)
            if _is_number(left) and _is_number(right):
                return NumberNode(left.value + right.value)

        elif node.operator == '-':
            if _is_number(right, 0):
                return left
            if _is_unary_minus(right):
                return BinaryOpNode(left, '+', right.operand)
            if _is_number(left) and _is_number(right):
                return NumberNode(left.value - right.value)

        elif node.operator == '*':
            if _is_unary_minus(right):
                return UnaryOpNode('-', BinaryOpNode(left, '*', right.operand))
            if _is_unary_minus(left):
                return UnaryOpNode('-', BinaryOpNode(left.operand, '*', right))
            if _is_number(left, 1):
                return right
            if _is_number(right, 1):
                return left
            if _is_number(left, 0) or _is_number(right, 0):
                return NumberNode(0)
            if _is_number(left) and _is_number(right):
                return NumberNode(left.value * right.value)

            # Перегруппировка умножения
            factors = []
            self._collect_factors(left, factors)
            self._collect_factors(right, factors)

            number = 1
            vars_dict = {}
            other_factors = []

            for f in factors:
                if _is_number(f):
                    number *= f.value
                elif _is_variable(f):
                    vars_dict[f.name] = vars_dict.get(f.name, 0) + 1
                elif isinstance(f, BinaryOpNode) and f.operator == '^' and _is_variable(f.left) and _is_number(f.right):
                    vars_dict[f.left.name] = vars_dict.get(f.left.name, 0) + f.right.value
                else:
                    other_factors.append(f)

            # Строим результат
            result = None

            if number != 1:
                result = NumberNode(number)

            for name, power in vars_dict.items():
                var_node = VariableNode(name)
                if power == 1:
                    node_to_add = var_node
                else:
                    node_to_add = BinaryOpNode(var_node, '^', NumberNode(power))

                if result is None:
                    result = node_to_add
                else:
                    result = BinaryOpNode(result, '*', node_to_add)

            for f in other_factors:
                if result is None:
                    result = f
                else:
                    result = BinaryOpNode(result, '*', f)

            if result is not None:
                return result

            # число в начало
            if _is_number(right) and not _is_number(left):
                return BinaryOpNode(right, '*', left)

        elif node.operator == '/':
            if _is_number(right, 1):
                return left
            if _is_number(left, 0):
                return NumberNode(0)
            if _is_number(left) and _is_number(right) and right.value != 0:
                return NumberNode(left.value / right.value)

        elif node.operator == '^':
            if _is_number(right, 1):
                return left
            if _is_number(right, 0):
                return NumberNode(1)
            if _is_number(left, 1):
                return NumberNode(1)
            if _is_number(left) and _is_number(right):
                return NumberNode(left.value ** right.value)

        return BinaryOpNode(left, node.operator, right)

    def _simplify_unary(self, node: UnaryOpNode) -> ASTNode:
        operand = self._simplify_once(node.operand)

        if node.operator == '-':
            if _is_number(operand, 0):
                return NumberNode(0)
            if _is_unary_minus(operand):
                return self._simplify_once(operand.operand)

        return UnaryOpNode(node.operator, operand)
