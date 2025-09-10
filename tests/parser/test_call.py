from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral, ReferenceExpression, MathExpression


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


def test_call_on_call_in_math():
    r = list(parse("1+a.b().c()"))

    assert r == [
        MathExpression('+', [
            NumberLiteral(1.0),
            CallExpression(
                ReferenceExpression("c", CallExpression(ReferenceExpression('b', ReferenceExpression('a')), []))
                , [])
        ])

    ]
