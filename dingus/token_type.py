from enum import Enum, unique


@unique
class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    LEFT_BRACKET = '['
    RIGHT_BRACKET = ']'

    COMMA = ','
    DOT = '.'

    MINUS = '-'
    PLUS = '+'
    SLASH = '/'
    STAR = '*'

    # One or two character tokens.
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literals.
    IDENTIFIER = '[identifier]'
    STRING = '[string]'
    NUMBER = '[number]'
    CUSTOM_OPERATOR = '[custom operator]'

    # Keywords.
    AND = 'and'
    BREAK = 'break'
    CLASS = 'class'
    ELSE = 'else'
    END = 'end'
    FALSE = 'False'
    FOR = 'for'
    FUNCTION = 'def'
    GENERATOR = 'generator'
    IF = 'if'
    IN = 'in'
    IS = 'is'
    NONE = 'None'
    NOT = 'not'
    OPERATOR = 'operator'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SELF = 'self'
    THEN = 'then'
    TRUE = 'True'
    UNDEFINED = 'Undefined'
    WHILE = 'while'
    YIELD = 'yield'

    END_OF_LINE = '\n'

    # End of file marker
    EOF = '[EOF]'
