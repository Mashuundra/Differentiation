""" Преобразование AST обратно в строку """

from src.ast_nodes.nodes import (
    NumberNode, VariableNode, BinaryOpNode, FunctionNode, UnaryOpNode
)


def to_string(node) -> str:
    """Преобразует AST в строку"""
    if isinstance(node, NumberNode):
        # целые числа выводим без .0
        if node.value == int(node.value):
            return str(int(node.value))
        return str(node.value)

    elif isinstance(node, VariableNode):
        # переменная
        return node.name

    elif isinstance(node, BinaryOpNode):
        # бинарная операция
        left = to_string(node.left)
        right = to_string(node.right)

        # добавляем скобки
        if _needs_parentheses(node.left, node.operator, right=False):
            left = f"({left})"
        if _needs_parentheses(node.right, node.operator, right=True):
            right = f"({right})"

        if node.operator == '+':
            return f"{left} + {right}"
        elif node.operator == '-':
            return f"{left} - {right}"
        elif node.operator == '*':
            return f"{left}*{right}"
        elif node.operator == '/':
            return f"{left}/{right}"
        elif node.operator == '^':
            return f"{left}^{right}"

    elif isinstance(node, FunctionNode):
        # функция
        arg = to_string(node.argument)
        return f"{node.name}({arg})"

    elif isinstance(node, UnaryOpNode):
        # унарная операция
        operand = to_string(node.operand)
        # добавляем скобки
        if isinstance(node.operand, (BinaryOpNode, FunctionNode)):
            return f"-({operand})"
        return f"-{operand}"

    return str(node)


def to_infix_string(node) -> str:
    """Инфиксная строка с полными скобками (для тестов)"""
    if isinstance(node, NumberNode):
        if node.value == int(node.value):
            return str(int(node.value))
        return str(node.value)

    elif isinstance(node, VariableNode):
        return node.name

    elif isinstance(node, BinaryOpNode):
        left = to_infix_string(node.left)
        right = to_infix_string(node.right)
        return f"({left} {node.operator} {right})"

    elif isinstance(node, FunctionNode):
        arg = to_infix_string(node.argument)
        return f"{node.name}({arg})"

    elif isinstance(node, UnaryOpNode):
        operand = to_infix_string(node.operand)
        return f"{node.operator}{operand}"

    return str(node)


def _needs_parentheses(node, parent_op, right=False) -> bool:
    """Определяет, нужны ли скобки для операнда."""
    if not isinstance(node, BinaryOpNode):
        return False

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    node_prec = precedence.get(node.operator, 0)
    parent_prec = precedence.get(parent_op, 0)

    if node_prec < parent_prec:
        return True

    if node_prec == parent_prec:
        if right and parent_op in ('-', '/', '^'):
            return True
        if not right and parent_op == '^':
            return True

    return False
