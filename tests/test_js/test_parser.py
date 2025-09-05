from pyjs import parse
from pyjs.expressions import CallExpression, NumberLiteral, AssignmentExpression, FunctionExpression, ReferenceExpression


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


def test_parse_functions():
    r = list(parse("function a(){x=1}"))
    assert r == [
        FunctionExpression("a", [],
                           [
                               AssignmentExpression(None, 'x', NumberLiteral(1))
                           ])
    ]


def test_parse_functions_with_arg():
    r = list(parse("function a(b){x=b}"))
    assert r == [
        FunctionExpression("a", [ReferenceExpression('b')],
                           [
                               AssignmentExpression(None, 'x', ReferenceExpression('b'))
                           ])
    ]


def test_parse_functions_with_args():
    r = list(parse("function a(b, c){x=b}"))
    assert r == [
        FunctionExpression("a", [ReferenceExpression('b'), ReferenceExpression('c')],
                           [
                               AssignmentExpression(None, 'x', ReferenceExpression('b'))
                           ])
    ]
