import pytest

from dingus.scanner import Scanner
from dingus.token import Token
from dingus.token_type import TokenType


class ErrorHandler:
    def __init__(self) -> None:
        self.failed = -1

    def scanner_error(self, line, message):
        self.failed = line


def create_scanner(source):
    error_handler = ErrorHandler()
    scanner = Scanner(source, error_handler)
    tokens = scanner.scan_tokens()
    return tokens, error_handler


def test_scanner():
    source = 'a = 5 + x'
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.IDENTIFIER, 'a', None, 1)
    assert tokens[1] == Token(TokenType.EQUAL, '=', None, 1)
    assert tokens[2] == Token(TokenType.NUMBER, '5', 5, 1)
    assert tokens[3] == Token(TokenType.PLUS, '+', None, 1)
    assert tokens[4] == Token(TokenType.IDENTIFIER, 'x', None, 1)
    assert tokens[5] == Token(TokenType.EOF, '', None, 1)
    assert error_handler.failed == -1


def test_scanner_unexpected():
    source = 'a = § +'
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.IDENTIFIER, 'a', None, 1)
    assert tokens[1] == Token(TokenType.EQUAL, '=', None, 1)
    assert tokens[2] == Token(TokenType.PLUS, '+', None, 1)
    assert tokens[3] == Token(TokenType.EOF, '', None, 1)
    assert error_handler.failed == 1


def test_unterminated_string():
    source = 'a = "string...'
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.IDENTIFIER, 'a', None, 1)
    assert tokens[1] == Token(TokenType.EQUAL, '=', None, 1)
    assert tokens[2] == Token(TokenType.EOF, '', None, 1)
    assert error_handler.failed == 1


def test_escaped_string():
    source = "a = '...\\\'string\\\'...'"
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.IDENTIFIER, 'a', None, 1)
    assert tokens[1] == Token(TokenType.EQUAL, '=', None, 1)
    esc_str = "'...\\\'string\\\'...'"
    string = "...'string'..."
    assert tokens[2] == Token(TokenType.STRING, esc_str, string, 1)
    assert tokens[3] == Token(TokenType.EOF, '', None, 1)
    assert error_handler.failed == -1


def test_keywords():
    source = 'yield then\ngenerator end'
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.YIELD, 'yield', None, 1)
    assert tokens[1] == Token(TokenType.THEN, 'then', None, 1)
    assert tokens[2] == Token(TokenType.END_OF_LINE, '\n', None, 1)
    assert tokens[3] == Token(TokenType.GENERATOR, 'generator', None, 2)
    assert tokens[4] == Token(TokenType.END, 'end', None, 2)
    assert tokens[5] == Token(TokenType.EOF, '', None, 2)
    assert error_handler.failed == -1


def test_custom_operator():
    source = 'a@5 !'
    tokens, error_handler = create_scanner(source)
    assert tokens[0] == Token(TokenType.IDENTIFIER, 'a', None, 1)
    assert tokens[1] == Token(TokenType.CUSTOM_OPERATOR, '@', '@', 1)
    assert tokens[2] == Token(TokenType.NUMBER, '5', 5, 1)
    assert tokens[3] == Token(TokenType.CUSTOM_OPERATOR, '!', '!', 1)
    assert tokens[4] == Token(TokenType.EOF, '', None, 1)
    assert error_handler.failed == -1
