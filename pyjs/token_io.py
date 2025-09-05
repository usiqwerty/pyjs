import io
from typing import Iterable

from pyjs.tokenizer import Token


class TokenIO:
    def __init__(self, tokens: Iterable[Token]):
        self.tokens = list(tokens)
        self.pos = 0

    @property
    def current(self):
        return self.tokens[self.pos]

    @property
    def open(self):
        return self.pos < len(self.tokens)

    def read(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def seek(self, offset, whence=0, /):
        if whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_END:
            self.pos = len(self.tokens) + offset
        else:
            raise ValueError

    def tell(self):
        return self.pos
