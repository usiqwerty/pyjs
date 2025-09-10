import pytest

from pyjs.environment import Environment
from pyjs.expressions import MathExpression, NumberLiteral, StringLiteral, FunctionExpression, CallExpression, \
    ReturnExpression


@pytest.mark.parametrize(
    ["a", 'b', 'res', 'op'],
    [
        (1, 2, 3, '+'),
        (1, 2, -1, '-'),
        (2, 3, 6, '*'),
        (1, 2, 0.5, '/'),
    ]
)
def test_eval_math(a, b, res, op):
    env = Environment()
    assert env.eval(MathExpression(op, [NumberLiteral(a), NumberLiteral(b)])) == NumberLiteral(res)


def auto_literal(val):
    if isinstance(val, str):
        return StringLiteral(val)
    elif isinstance(val, float):
        return NumberLiteral(val)
    elif isinstance(val, int):
        return NumberLiteral(val)
    raise TypeError


@pytest.mark.parametrize(
    ["a", 'res'],
    [
        (1, 1),
        ('1', '1')
    ]
)
def test_eval_literal(a, res):
    env = Environment()
    assert env.eval(auto_literal(a)) == auto_literal(res)


# TODO: add more js weird math...
@pytest.mark.parametrize(
    ["a", 'b', 'res', 'op'],
    [
        ('a', 'b', 'ab', '+'),
        ('a', 1, 'a1', '+'),
    ]
)
def test_eval_math_on_strings(a, b, res, op):
    env = Environment()
    assert env.eval(MathExpression(op, [auto_literal(a), auto_literal(b)])) == auto_literal(res)


def test_eval_func():
    env = Environment()
    f = FunctionExpression("func", [], [
        ReturnExpression(
            MathExpression('+', [auto_literal(1), auto_literal(1)])
        )
    ])
    env.run([f])
    assert env.objects == {f.name: f}
    assert env.eval(CallExpression("func", [])) == NumberLiteral(2)
