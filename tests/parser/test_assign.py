from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral, AssignmentExpression, MathExpression, ReferenceExpression
from tests.runner.test_eval import auto_literal


def test_parse_assign_literal():
    r = list(parse("a = 1"))
    assert r == [
        AssignmentExpression(None, "a", NumberLiteral(1))
    ]
    r = list(parse("const a = 1"))
    assert r == [
        AssignmentExpression("const", "a", NumberLiteral(1))
    ]


def test_parse_assign_call():
    r = list(parse("a = b()"))
    assert r == [
        AssignmentExpression(None, "a", CallExpression(ReferenceExpression('b'), []))
    ]
    r = list(parse("const a = b()"))
    assert r == [
        AssignmentExpression('const', "a", CallExpression(ReferenceExpression('b'), []))
    ]


def test_parse_assign_call_args():
    r = list(parse("a = b(1, 2)"))
    assert r == [
        AssignmentExpression(None, "a", CallExpression(ReferenceExpression('b'), [NumberLiteral(1), NumberLiteral(2)]))
    ]
    r = list(parse("const a = b(1, 2)"))
    assert r == [
        AssignmentExpression('const', "a", CallExpression(ReferenceExpression('b'), [NumberLiteral(1), NumberLiteral(2)]))
    ]


def test_ref_in_math():
    r = list(parse("a+b.c"))
    assert r == [
        MathExpression('+', [
            ReferenceExpression('a'),
            ReferenceExpression('c', ReferenceExpression('b')),
        ])
    ]


def test_multiple_lines():
    r = list(parse("a=3\nx = f(a)"))
    assert r == [
        AssignmentExpression(None, "a", auto_literal(3)),
        AssignmentExpression(None, "x", CallExpression(
            ReferenceExpression("f"), [
                ReferenceExpression("a")
            ]
        )),
    ]
