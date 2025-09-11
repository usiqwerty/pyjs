import pyjs
from pyjs.expressions import ReferenceExpression, CallExpression, StringLiteral, AssignmentExpression
from tests.runner.test_eval import auto_literal


def test_unicode_reference():
    r = list(pyjs.parse("привет"))
    assert r == [ReferenceExpression("привет")]


def test_unicode_call():
    r = list(pyjs.parse("привет()"))
    assert r == [CallExpression(ReferenceExpression("привет"), [])]


def test_unicode_string():
    r = list(pyjs.parse("'привет'"))
    assert r == [StringLiteral("привет")]


def test_unicode_comment():
    r = list(pyjs.parse("// привет"))
    assert r == []


def test_comment():
    r = list(pyjs.parse("// hello\na=1;\nconst b=2 // hi"))
    assert r == [
        AssignmentExpression(None, "a", auto_literal(1)),
        AssignmentExpression('const', "b", auto_literal(2))
    ]
