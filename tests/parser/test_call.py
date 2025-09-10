from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral, ReferenceExpression


def test_parse_call():
    r = list(parse("a(1)"))
    assert r == [
        CallExpression(ReferenceExpression("a"), [NumberLiteral(1)])
    ]


def test_parse_call_multiple_args():
    r = list(parse("a(1, 2)"))
    assert r == [
        CallExpression(ReferenceExpression("a"), [NumberLiteral(1), NumberLiteral(2)])
    ]


def test_parse_call_on_call():
    r = list(parse("a().b()"))
    last_ref = ReferenceExpression(
        "b",
        CallExpression(ReferenceExpression("a"), [])
    )
    assert r == [
        CallExpression(last_ref, [])
    ]
