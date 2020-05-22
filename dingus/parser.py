import dingus.expr as xpr
import dingus.stmt as mnt
from dingus.errors import ParserError
from dingus.token_type import TokenType


class Parser(object):
    def __init__(self, tokens, error_handler) -> None:
        self.tokens = tokens
        self.error = error_handler
        self.current = 0

    def parse(self):
        return self._declaration()

    def _declaration(self):
        try:
            return self._statement()
        except ParserError as e:
            self._synchronize()

        return None

    def _statement(self):
        #if self._match(TT.PRINT):
        #    return self._print_statement()
        return self._expression_statement()

    def _expression_statement(self):
        value = self._expression()
        if not self._is_at_end_of_expression():
            self._consume(self._peek(), "Expected end of line after expression.")
        return mnt.Expression(value)

    def _expression(self):
        return self._addition()

    def _binary_rule(self, next_rule, tokens):
        expr = next_rule()

        while self._match(*tokens):
            operator = self._previous()
            right = next_rule()
            expr = xpr.Binary(expr, operator, right)
        return expr

    def _addition(self):
        return self._binary_rule(self._multiplication, [TokenType.PLUS,
                                                        TokenType.MINUS])

    def _multiplication(self):
        return self._binary_rule(self._unary, [TokenType.STAR,
                                               TokenType.SLASH])

    def _unary(self):
        if self._match(TokenType.MINUS, TokenType.NOT):
            operator = self._previous()
            right = self._unary()
            return xpr.Unary(operator, right)

        return self._primary()

    def _primary(self):
        if self._match(TokenType.FALSE):
            return xpr.Literal(False)
        if self._match(TokenType.TRUE):
            return xpr.Literal(True)
        if self._match(TokenType.NONE):
            return xpr.Literal(None)
        if self._match(TokenType.UNDEFINED):
            return xpr.Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return xpr.Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return xpr.Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _check(self, token_type):
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self):
        if not self._is_at_end():
            self.current += 1

        return self._previous()

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

    def _is_at_end_of_expression(self):
        return self._peek().type in (TokenType.END_OF_LINE, TokenType.EOF)

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _consume(self, token_type, message):
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token, message):
        self.error.parser_error(token, message)
        return ParserError(token, message)

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.END_OF_LINE:
                return

            #if self._peek().type in KEYWORD_TOKENS:
            #    return

            self._advance()
