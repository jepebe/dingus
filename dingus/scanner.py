from dingus.error_handler import ErrorHandler
from dingus.token import Token
from dingus.token_type import TokenType

ord_a = ord('a')
ord_z = ord('z')
ord_A = ord('A')
ord_Z = ord('Z')
ord__ = ord('_')
ord_0 = ord('0')
ord_9 = ord('9')


def is_digit(c):
    return ord_0 <= ord(c) <= ord_9


def is_alpha(c):
    c = ord(c)
    return ord_a <= c <= ord_z or ord_A <= c <= ord_Z or c == ord__


def is_alpha_numeric(c):
    return is_digit(c) or is_alpha(c)


class Scanner(object):
    def __init__(self, source, error: ErrorHandler):
        self.tokens = []
        self.source = source
        self.error = error
        self.start = 0
        self.current = 0
        self.line = 1
        self.token_set = {item.value for item in TokenType}

    def scan_tokens(self):
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def _is_at_end(self):
        return self.current >= len(self.source)

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _match(self, expected):
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self):
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _identifier(self):
        while is_alpha_numeric(self._peek()):
            self._advance()

        text = self.source[self.start:self.current]

        if text in self.token_set:
            token_type = TokenType(text)
        else:
            token_type = TokenType.IDENTIFIER
        self._add_token(token_type)

    def _number(self):
        formatter = int
        while is_digit(self._peek()):
            self._advance()

        if self._peek() == '.' and is_digit(self._peek_next()):
            formatter = float
            self._advance()

            while is_digit(self._peek()):
                self._advance()

        value = self.source[self.start:self.current]
        self._add_token(TokenType.NUMBER, formatter(value))

    def _string(self, quote):
        has_escaped_quotes = False
        while self._peek() != quote and not self._is_at_end():
            if self._peek() == '\n':
                self.line += 1
            if self._peek() == '\\' and self._peek_next() == quote:
                self._advance()  # skip the escaped quote
                has_escaped_quotes = True
            self._advance()

        if self._is_at_end():
            self.error.scanner_error(self.line, "Unterminated string.")
            return

        self._advance()  # the ending quote

        value = self.source[self.start + 1: self.current - 1]
        if has_escaped_quotes:
            value = value.replace("\\'", "'")
        self._add_token(TokenType.STRING, value)

    def _add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def _consume_line(self):
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()

    def _scan_token(self):
        c = self._advance()

        if c in ('(', ')', '[', ']', '{', '}', ',', '.', '-', '+', '*', '/'):
            self._add_token(TokenType(c))
        elif c in ('=', '<', '>'):
            if self._match('='):
                c = f'{c}='
            self._add_token(TokenType(c))
        elif c == '!' and self._peek() == '=':
            self._advance()
            self._add_token(TokenType('!='))
        elif c == '#':
            self._consume_line()
        elif c in (' ', '\r', '\t'):
            pass
        elif c == '\n':
            self.line += 1
        elif c in ('"', '\''):
            self._string(c)
        elif is_digit(c):
            self._number()
        elif is_alpha(c):
            self._identifier()
        elif c in ('%', '$', '@', '|', '?', '~', '^', ':', '!'):
            self._add_token(TokenType.CUSTOM_OPERATOR, c)
        else:
            msg = f'Unexpected character: \'{c}\''
            self.error.scanner_error(self.line, msg)
