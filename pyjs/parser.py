from dataclasses import dataclass
from typing import Iterable, Generator

from pyjs.expressions import (AssignmentExpression, ReferenceExpression, StringLiteral, NumberLiteral,
                              CallExpression, Expression, MathExpression, TemplateLiteral, FunctionExpression)
from pyjs.tokenizer import tokenize, assignation_keywords, Token


@dataclass
class CombinedTokens:
    expressions: list[Expression]

    def as_args(self):
        for expr_tok in self.expressions:
            if isinstance(expr_tok, Token):
                if expr_tok.type == 'COMMA':
                    continue
                else:
                    raise ValueError(f"Token {expr_tok} should not be here")
            else:
                yield expr_tok


def combine(tokens: Generator[Token, None, None], stop_on_first=False):
    groups = []

    was_dot = False
    is_function_def = False
    for tok in tokens:
        # print(tok.type, tok.value)
        if tok.type == "SPACE":
            continue
        elif tok.type == "LBRACKET":
            # TODO: may be an anonymous function
            sub = combine(tokens)
            print(f"{sub=}")
            comb = CombinedTokens(sub)
            if groups and isinstance(groups[-1], ReferenceExpression):
                args = list(comb.as_args())
                call_expression = CallExpression(groups[-1].name, args)

                if (len(groups) >= 2
                        and isinstance(groups[-2], Token)
                        and groups[-2].type == "KEYWORD"
                        and groups[-2].value == "function"):
                    ref = groups.pop()
                    fun_kw = groups.pop()
                    groups.append(FunctionExpression(ref.name, args, None))
                else:
                    groups[-1] = call_expression
            else:
                groups.append(comb)
        elif tok.type == "RBRACKET":
            return groups
        elif tok.type == "DOT":
            was_dot = True
        elif tok.type == "REF":
            if was_dot:
                was_dot = False
                prev = groups.pop()
                groups.append(ReferenceExpression(prev.name + f".{tok.value}"))
            else:
                groups.append(ReferenceExpression(tok.value))
        elif tok.type == 'ASSIGN':
            var_name = groups[-1].name
            var_type = None
            if len(groups) > 1:
                if groups[-2].type == "KEYWORD" and groups[-2].value in assignation_keywords:
                    var_type = groups[-2].value
                    groups.pop(-2)
            groups.pop()
            groups.append(AssignmentExpression(var_type, var_name, None))
        elif tok.type == "MATH":
            prev = groups.pop()
            next = combine(tokens, True)
            groups.append(MathExpression(tok.value, [prev, next]))
        elif tok.type == "STRING":
            groups.append(StringLiteral(tok.value[1:-1]))
        elif tok.type == "NUMBER":
            groups.append(NumberLiteral(float(tok.value)))
        elif tok.type == "TEMPLATE":
            groups.append(TemplateLiteral(tok.value[1:-1]))
        elif tok.type == "LCBRACKET":
            # here may be everything: if-else block, loop or function
            sub = combine(tokens)
            print(f"func sub {sub}")

            if is_function_def:
                prev = groups[-1]
                print(f"{prev=}")
                assert isinstance(prev, FunctionExpression)
                prev.body = join_assignments_values(sub)
                is_function_def = False

        elif tok.type == "RCBRACKET":
            return groups
        elif tok.type == 'KEYWORD':
            if tok.value == 'function':
                is_function_def = True
            groups.append(tok)
        else:
            print(f"Unhadled token: {tok}")
            groups.append(tok)
        if stop_on_first and groups:
            return groups
    print(f"ret end {groups}")
    return groups


# TODO: remove this shame
def join_assignments_values(groups: list[Expression]):
    result = []

    for i in range(len(groups)):
        if i > 0 and isinstance(groups[i - 1], AssignmentExpression) and groups[i - 1].value is None:
            result[-1].value = groups[i]
        else:
            result.append(groups[i])

    return result


def parse(code: str) -> Iterable[Expression]:
    """Parse code into tree"""
    tokens_generator = tokenize(code)
    for x in join_assignments_values(combine(tokens_generator)):
        if isinstance(x, Token) and x.type == 'SEMICOLON':
            continue
        yield x
