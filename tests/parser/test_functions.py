from pyjs import parse
from pyjs.expressions import FunctionExpression, AssignmentExpression, NumberLiteral, ReferenceExpression


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


def test_parse_arrow_functions_no_args():
    r = list(parse("() => {x=b}"))
    assert r == [
        FunctionExpression(None, [],
                           [
                               AssignmentExpression(None, 'x', ReferenceExpression('b'))
                           ])
    ]


def test_parse_arrow_functions_arg_empty_body():
    r = list(parse("(a, b) => {}"))
    assert r == [
        FunctionExpression(None, [ReferenceExpression('a'), ReferenceExpression('b')], [])
    ]


def test_parse_arrow_functions_args():
    r = list(parse("(a, b) => {x=b}"))
    assert r == [
        FunctionExpression(None, [ReferenceExpression('a'), ReferenceExpression('b')],
                           [
                               AssignmentExpression(None, 'x', ReferenceExpression('b'))
                           ])
    ]


def test_parse_arrow_functions_arg_no_brackets():
    r = list(parse("a => {x=b}"))
    assert r == [
        FunctionExpression(None, [ReferenceExpression('a')],
                           [
                               AssignmentExpression(None, 'x', ReferenceExpression('b'))
                           ])
    ]


def test_parse_arrow_functions_no_arg_no_body_brackets():
    r = list(parse("() => expression"))
    assert r == [
        FunctionExpression(None, [],
                           [
                               ReferenceExpression('expression')
                           ])
    ]


def test_parse_arrow_functions_no_brackets():
    r = list(parse("param => expression"))
    assert r == [
        FunctionExpression(None, [ReferenceExpression('param')],
                           [
                               ReferenceExpression('expression')
                           ])
    ]
