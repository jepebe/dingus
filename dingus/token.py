from dingus.token_type import TokenType


class Token(object):
    def __init__(self, token_type: TokenType, lexeme: str, literal: object,
                 line: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f'{self.type} {self.lexeme} {self.literal}'

    def __repr__(self):
        return f'Token({self.type}, {self.lexeme}, {self.literal}, {self.line})'

    def __eq__(self, other):
        return (self.type == other.type and
                self.lexeme == other.lexeme and
                self.literal == other.literal and
                self.line == other.line
                )
