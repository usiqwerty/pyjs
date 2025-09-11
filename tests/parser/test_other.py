import pyjs
from pyjs.expressions import ReferenceExpression, CallExpression, StringLiteral


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
