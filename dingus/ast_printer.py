from dingus.expr import ExprVisitor, Unary, Literal, Grouping, Binary
from dingus.stmt import StmtVisitor, Expression


class AstPrinter(ExprVisitor, StmtVisitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> object:
        left = expr.left.accept(self)
        right = expr.right.accept(self)
        return f'({left} {expr.operator.lexeme} {right})'

    def visit_grouping_expr(self, expr: Grouping) -> object:
        return f'({expr.expression.accept(self)})'

    def visit_literal_expr(self, expr: Literal) -> object:
        value = expr.value
        return f'{value}'

    def visit_unary_expr(self, expr: Unary) -> object:
        return f'({expr.operator.lexeme} {expr.right.accept(self)})'

    def visit_expression_stmt(self, stmt: Expression) -> object:
        return f'Expression[{stmt.expression.accept(self)}]'


