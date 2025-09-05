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
class ArrayExpression(Expression):
    array: list[Expression]


@dataclass
class CallExpression(Expression):
    name: str
    args: list[Expression]


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class NumberLiteral(Expression):
    value: float


@dataclass
class TemplateLiteral(Expression):
    value: str


@dataclass
class MathExpression(Expression):
    operation: Literal['+', '-', '*', '/']
    operands: list[Expression]


@dataclass
class FunctionExpression(Expression):
    name: str
    args: list[ReferenceExpression]
    body: list[Expression]
