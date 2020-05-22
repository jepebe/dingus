from dingus.token import Token
from typing import List


class Expr(object):
	def accept(self, visitor):
		print("[Expr.accept()] Not implemented!")


class Binary(Expr):
	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_binary_expr(self)


class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_grouping_expr(self)


class Literal(Expr):
	def __init__(self, value: object):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_literal_expr(self)


class Unary(Expr):
	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_unary_expr(self)


class ExprVisitor(object):
	def visit_binary_expr(self, expr: Binary) -> object:
		print("[visit_binary_expr] Not implemented!")
		return None

	def visit_grouping_expr(self, expr: Grouping) -> object:
		print("[visit_grouping_expr] Not implemented!")
		return None

	def visit_literal_expr(self, expr: Literal) -> object:
		print("[visit_literal_expr] Not implemented!")
		return None

	def visit_unary_expr(self, expr: Unary) -> object:
		print("[visit_unary_expr] Not implemented!")
		return None


