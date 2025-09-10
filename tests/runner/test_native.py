import pyjs
from pyjs.expressions import NumberLiteral


def native_func(arg):
    return arg * 2


def test_native_call():
    env = pyjs.Environment()
    env.objects['f'] = native_func

    env.run(pyjs.parse("x = f(3)"))
    assert env.objects['x'] == NumberLiteral(6)
