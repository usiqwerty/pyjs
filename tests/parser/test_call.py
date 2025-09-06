from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral


def test_parse_call():
    r = list(parse("a(1)"))
    assert r == [
        CallExpression("a", [NumberLiteral(1)])
    ]


def test_parse_call_multiple_args():
    r = list(parse("a(1, 2)"))
    assert r == [
        CallExpression("a", [NumberLiteral(1), NumberLiteral(2)])
    ]
