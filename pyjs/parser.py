from dataclasses import dataclass
from typing import Iterable, Generator

from pyjs.expressions import (AssignmentExpression, ReferenceExpression, StringLiteral, NumberLiteral,
                              CallExpression, Expression, MathExpression, TemplateLiteral, FunctionExpression,
                              ReturnExpression)
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
    is_ret = False
    for tok in tokens:
        # print(tok.type, tok.value)
        if tok.type == "SPACE":
            continue
        elif tok.type == "LBRACKET":
            # TODO: may be an anonymous function
            sub = combine(tokens)
            print(f"{sub=}")
            comb = CombinedTokens(sub)
            if groups and isinstance(groups[-1], ReferenceExpression|MathExpression):
                args = list(comb.as_args())
                if isinstance(groups[-1], ReferenceExpression):
                    call_expression = CallExpression(groups[-1], args)

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
                    last_operand = groups[-1].operands.pop()
                    call_expression = CallExpression(last_operand, args)
                    groups[-1].operands.append(call_expression)

            else:
                groups.append(comb)
        elif tok.type == "RBRACKET":
            return groups
        elif tok.type == "DOT":
            was_dot = True
        elif tok.type == "REF":
            if was_dot:
                was_dot = False
                for g in groups:
                    print(g)
                prev = groups.pop()
                if isinstance(prev, ReferenceExpression):
                    groups.append(ReferenceExpression(tok.value, parent=prev))
                elif isinstance(prev, CallExpression):
                    groups.append(ReferenceExpression(tok.value, parent=prev))
                elif isinstance(prev, MathExpression):
                    last_oper = prev.operands.pop()
                    if isinstance(last_oper, ReferenceExpression|CallExpression):
                        if isinstance(last_oper, ReferenceExpression):
                            # last_oper.name = last_oper.name + f".{tok.value}"
                            prev.operands.append(ReferenceExpression(tok.value, last_oper) )
                            groups.append(prev)
                        else:
                            last_oper = ReferenceExpression(tok.value, last_oper)
                            prev.operands.append(last_oper)

                            groups.append(prev)
                    else:
                        raise TypeError(last_oper)
                else:
                    raise TypeError(f"can't handle dot referece here {tok} {prev}")
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
            assert len(next) == 1
            groups.append(MathExpression(tok.value, [prev, next[0]]))
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
            else:
                groups.append(sub)
        elif tok.type == "RCBRACKET":
            return groups
        elif tok.type == 'KEYWORD':
            if tok.value == 'function':
                is_function_def = True
                groups.append(tok)
            elif tok.value == 'return':
                groups.append(ReturnExpression(None))
            else:
                groups.append(tok)
        elif tok.type == "ARROW":
            if isinstance(groups[-1], CombinedTokens):
                arrow_args_combined = groups.pop()
                sub = combine(tokens)
                if isinstance(sub[0], list): # curly brackets, explicit return
                    sub = join_assignments_values(sub[0])
                else:
                    # implicit return
                    last = sub.pop()
                    sub.append(ReturnExpression(last))
                print(f"arrow func sub {sub}")
                groups.append(
                    FunctionExpression(None, list(arrow_args_combined.as_args()), sub)
                )
            elif isinstance(groups[-1], ReferenceExpression):
                args = [groups.pop()]
                sub = combine(tokens)
                if isinstance(sub[0], list):  # curly brackets, explicit return
                    sub = join_assignments_values(sub[0])
                else:
                    # implicit return
                    last = sub.pop()
                    sub.append(ReturnExpression(last))
                print(f"arrow func sub {sub}")
                groups.append(
                    FunctionExpression(None, args, sub)
                )
            else:
                raise Expression


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
        if i > 0 and isinstance(groups[i - 1], AssignmentExpression|ReturnExpression) and groups[i - 1].value is None:
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
