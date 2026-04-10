"""Базовый класс Visitor для обхода AST."""

from .nodes import ASTNode  # относительный импорт вместо абсолютного


class NodeVisitor:
    """Базовый класс для обхода AST."""

    def visit(self, node: ASTNode):
        """Посещает узел и вызывает соответствующий метод."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)  # вызов найденного метода у узла

    def generic_visit(self, node: ASTNode):
        """Общий метод посещения для неподдерживаемых узлов."""
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_NumberNode(self, node):
        return self.generic_visit(node)

    def visit_VariableNode(self, node):
        return self.generic_visit(node)

    def visit_BinaryOpNode(self, node):
        return self.generic_visit(node)

    def visit_UnaryOpNode(self, node):
        return self.generic_visit(node)

    def visit_FunctionNode(self, node):
        return self.generic_visit(node)
