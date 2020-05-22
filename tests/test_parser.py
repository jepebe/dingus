import dingus.expr as xpr
import dingus.stmt as mnt
from dingus.parser import Parser
from dingus.scanner import Scanner
from dingus.token_type import TokenType


class ErrorHandler:
    def __init__(self) -> None:
        self.failed = -1

    def parser_error(self, token, message):
        self.failed = token.line


def test_parser_expression():
    source = '5 + 7 / 2'
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    assert isinstance(ast, mnt.Expression)
    assert isinstance(ast.expression, xpr.Binary)
    ast = ast.expression
    assert isinstance(ast.left, xpr.Literal)
    assert ast.left.value == 5
    assert ast.operator.type == TokenType.PLUS
    assert isinstance(ast.right, xpr.Binary)
    assert isinstance(ast.right.left, xpr.Literal)
    assert ast.right.left.value == 7
    assert ast.right.operator.type == TokenType.SLASH
    assert isinstance(ast.right.right, xpr.Literal)
    assert ast.right.right.value == 2


def test_parser_expression_2():
    source = '5 * 7 - 2'
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens, error_handler)
    ast = parser.parse()

    assert isinstance(ast, mnt.Expression)
    assert isinstance(ast.expression, xpr.Binary)
    ast = ast.expression
    assert isinstance(ast.left, xpr.Binary)
    assert isinstance(ast.left.left, xpr.Literal)
    assert ast.left.left.value == 5
    assert ast.left.operator.type == TokenType.STAR
    assert isinstance(ast.left.right, xpr.Literal)
    assert ast.left.right.value == 7

    assert ast.operator.type == TokenType.MINUS
    assert isinstance(ast.right, xpr.Literal)
    assert ast.right.value == 2
