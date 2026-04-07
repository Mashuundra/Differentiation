from src.parser import Parser
from src.differentiation import DifferentiationVisitor, Simplifier
from src.utils import to_string


def solve_derivative(expression: str, variable: str = 'x') -> str:
    # Парсинг строки
    parser = Parser(variable=variable)
    ast_nodes = parser.parse(expression)

    # Дифференцирование
    differentiator = DifferentiationVisitor(variable=variable)
    derivative_ast = differentiator.visit(ast_nodes)

    # Упрощение
    simplifier = Simplifier()
    simplified_ast = simplifier.simplify(derivative_ast)

    # Преобразование в строку
    result = to_string(simplified_ast)

    return result
