from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral, AssignmentExpression, MathExpression, ReferenceExpression


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
        AssignmentExpression(None, "a", CallExpression('b', []))
    ]
    r = list(parse("const a = b()"))
    assert r == [
        AssignmentExpression('const', "a", CallExpression('b', []))
    ]


def test_parse_assign_call_args():
    r = list(parse("a = b(1, 2)"))
    assert r == [
        AssignmentExpression(None, "a", CallExpression('b', [NumberLiteral(1), NumberLiteral(2)]))
    ]
    r = list(parse("const a = b(1, 2)"))
    assert r == [
        AssignmentExpression('const', "a", CallExpression('b', [NumberLiteral(1), NumberLiteral(2)]))
    ]


def test_ref_in_math():
    r = list(parse("a+b.c"))
    assert r == [
        MathExpression('+', [
            ReferenceExpression('a'),
            ReferenceExpression('b.c'),
        ])
    ]

