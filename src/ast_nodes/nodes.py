"""Классы узлов для абстрактного синтаксического дерева."""
# Определяет классы узлов дерева

from dataclasses import dataclass


class ASTNode:
    """Базовый класс для всех узлов AST.
    Позволяет писать функции, которые работают с любым узлом"""
    pass


@dataclass # автоматическое создание __init__, __eq__, __hash__
class NumberNode(ASTNode):
    """Узел для числовой константы.
     Представляет числа в выражении"""
    value: float

    def __repr__(self):
        return f"Number({self.value})"


@dataclass
class VariableNode(ASTNode):
    """Узел для переменной.
    Представляет переменную (по умолчанию 'x')"""
    name: str

    def __repr__(self):
        return f"Variable({self.name})"


@dataclass
class BinaryOpNode(ASTNode):
    """Узел для бинарной операции.
    Представляет операции с двумя операндами"""
    left: ASTNode
    operator: str  # '+', '-', '*', '/', '^'
    right: ASTNode

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


@dataclass
class UnaryOpNode(ASTNode):
    """Узел для унарной операции.
    Представляет операции с одним операндом"""
    operator: str  # '+', '-'
    operand: ASTNode

    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"


@dataclass
class FunctionNode(ASTNode):
    """Узел для вызова функции.
    Представляет математические функции"""
    name: str  # 'sin', 'cos', 'tan', 'ln', 'exp'
    argument: ASTNode

    def __repr__(self):
        return f"Function({self.name}, {self.argument})"