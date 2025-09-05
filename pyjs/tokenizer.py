import re
from typing import NamedTuple, Generator

"""
Many thanks to python docs!
https://docs.python.org/3/library/re.html#writing-a-tokenizer
"""


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


assignation_keywords = {"const", "let", "var"}
keywords = {
               "function"
           } | assignation_keywords
brackets = [
    ('LBRACKET', r'\('),
    ('RBRACKET', r'\)'),

    ('LCBRACKET', r'{'),
    ('RCBRACKET', r'}'),

    ('LSBRACKET', r'['),
    ('RSBRACKET', r']'),
]
comparison = [
    ('EQUALS', r'=='),
    ('EEQUALS', r'==='),
    ('LT', r'<'),
    ('LE', r'<='),
    ('LEE', r'<=='),
    ('GT', r'>'),
    ('GE', r'>='),
    ('GEE', r'>=='),
]
types = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('STRING', r'\'[\w\W]+?\'|\"[\w\W]+?\"'),
    ('TEMPLATE', r'`[\w\W]+?`')
]
general = [
    ('ASSIGN', r'='),
    ('REF', r'[A-Za-z]+[A-Za-z0-9]*'),

    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+'),
    ('DOT', r'\.'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('COLON', r':'),
    ('QMARK', r'\?'),
    ('EMARK', r'!'),

    ('ARROW', r'=>'),

    ('COMMENT', r'//'),
    ('BCOMMSTART', r'/\s*\*'),
    ('BCOMMEND', r'\*\s*/'),
    ('MATH', r'[+\-*/]'),
]
token_specification = types + general + comparison + brackets + [('MISMATCH', r'.')]


def tokenize(code) -> Generator[Token, None, None]:
    tok_regex = '|'.join(f'(?P<{token}>{expr})' for token, expr in token_specification)
    line_num = 0
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'REF' and value in keywords:
            kind = "KEYWORD"
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)
