from dataclasses import dataclass

import pyjs
from pyjs.expressions import ReferenceExpression, NumberLiteral


@dataclass
class A:
    field: int


def test_attr():
    env = pyjs.Environment()
    env.objects['a'] = A(1)
    print(env.objects)
    print(env.resolve(ReferenceExpression('a')))
    print(env.resolve(ReferenceExpression('field', ReferenceExpression('a'))))


def test_write_global_object():
    env = pyjs.Environment()
    env.objects['a'] = A(1)
    env.run(pyjs.parse("a  = 2"))
    assert env.objects['a'] == NumberLiteral(2)


def test_read_object_fields():
    env = pyjs.Environment()
    env.objects['a'] = A(1)
    env.run(pyjs.parse("x = a.field + 10"))
    assert env.objects['x'] == NumberLiteral(11)
