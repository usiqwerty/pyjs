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
