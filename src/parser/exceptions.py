"""Исключения для парсера."""


class ParserError(Exception):
    """Базовый класс для ошибок парсинга."""
    pass


class InvalidExpressionError(ParserError):
    """Выражение некорректно."""
    pass


class UnexpectedTokenError(ParserError):
    """Неожиданный токен."""
    pass


class MissingOperandError(ParserError):
    """Отсутствует операнд."""
    pass


class MissingOperatorError(ParserError):
    """Отсутствует оператор."""
    pass


class MismatchedParenthesesError(ParserError):
    """Несогласованные скобки."""
    pass
