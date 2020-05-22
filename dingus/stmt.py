from dingus.expr import Expr
from dingus.token import Token
from typing import List


class Stmt(object):
	def accept(self, visitor):
		print("[Stmt.accept()] Not implemented!")


class Expression(Stmt):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_expression_stmt(self)


class StmtVisitor(object):
	def visit_expression_stmt(self, stmt: Expression) -> object:
		print("[visit_expression_stmt] Not implemented!")
		return None


