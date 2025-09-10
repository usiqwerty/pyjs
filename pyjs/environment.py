from typing import Any

from pyjs.expressions import Expression, AssignmentExpression, ReferenceExpression, CallExpression, \
    LiteralValue, MathExpression, FunctionExpression, ReturnExpression, NumberLiteral, StringLiteral


class Environment:
    objects: dict[str, Any]

    def __init__(self):
        self.objects = {}

    def run_function(self, call: CallExpression):
        func: FunctionExpression = self.resolve(call.name)
        for expr in func.body:
            if isinstance(expr, ReturnExpression):
                return self.eval(expr.value)
            self.eval(expr)

    def eval(self, expression: Expression) -> LiteralValue | FunctionExpression:
        if isinstance(expression, LiteralValue):
            return expression
        elif isinstance(expression, CallExpression):
            return self.run_function(expression)
        elif isinstance(expression, MathExpression):
            # Well, in fact, there are only 2 operands...
            a, b = [self.eval(operand) for operand in expression.operands]
            if expression.operation == '+':
                return a + b
            elif expression.operation == '-':
                return a - b
            elif expression.operation == '*':
                return a * b
            elif expression.operation == '/':
                return a / b
        elif isinstance(expression, ReferenceExpression):
            return self.resolve(expression)
        elif isinstance(expression, FunctionExpression):
            # function definition is not a function call!
            return expression
        else:
            raise TypeError(f"Can't evaluate {expression}")

    def run(self, expressions: list[Expression]):
        for expression in expressions:
            if isinstance(expression, AssignmentExpression):
                # TODO: var types may be different
                self.objects[expression.name] = self.eval(expression.value)
            elif isinstance(expression, CallExpression):
                self.run_function(expression)
            elif isinstance(expression, FunctionExpression):
                self.objects[expression.name] = expression
            else:
                self.eval(expression)

    def resolve(self, reference: ReferenceExpression):
        if reference.parent is None:
            return self.objects[reference.name]
        obj = self.eval(reference.parent)
        # can read python objects
        value = getattr(obj, reference.name)
        if isinstance(value, int | float):
            return NumberLiteral(value)
        if isinstance(value, str):
            return StringLiteral(value)
        return value
