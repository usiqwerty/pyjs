from abc import ABC
from dataclasses import dataclass
from typing import Literal


class Expression(ABC):
    """Abstract base class for JS expression"""


@dataclass
class ReferenceExpression(Expression):
    name: str


@dataclass
class AssignmentExpression(Expression):
    type: Literal["const", "let", "var", None]
    name: str
    value: Expression


@dataclass
class CallExpression(Expression):
    name: str
    args: list[Expression]


class LiteralValue(Expression, ABC):
    pass


@dataclass
class StringLiteral(LiteralValue):
    value: str

    def __add__(self, other):
        return StringLiteral(f"{self.value}{other.value}")

@dataclass
class NumberLiteral(LiteralValue):
    value: float

    def __add__(self, other):
        return NumberLiteral(self.value + other.value)

    def __sub__(self, other):
        return NumberLiteral(self.value - other.value)

    def __mul__(self, other):
        return NumberLiteral(self.value * other.value)

    def __truediv__(self, other):
        return NumberLiteral(self.value / other.value)


@dataclass
class TemplateLiteral(Expression):
    value: str


@dataclass
class MathExpression(Expression):
    operation: Literal['+', '-', '*', '/']
    operands: list[Expression]


@dataclass
class FunctionExpression(Expression):
    name: str | None
    args: list[ReferenceExpression]
    body: list[Expression]


@dataclass
class ReturnExpression(Expression):
    value: Expression
