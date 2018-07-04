"""
Contains Number and String classes definitions.
"""

import string

from nylo.token import Token


class Number(Token):

    def __init__(self, value=''):
        self.value = value

    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(string.digits)

    def parse(self, parser):
        while parser.any_starts_with(string.digits + '_.'):
            if parser.starts_with('.') and '.' in self.value:
                break
            self.value += parser.move()
        parser.hasparsed(Number(float(self.value))
                         if '.' in self.value else Number(int(self.value)))

    def transpile(self, mesh, path):
        pass

    def __repr__(self):
        return repr(self.value)

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)

    def evaluate(self, mesh, interpreting, interpreted):
        interpreted.append(self)

    def chroot(self, oldroot, newroot):
        return self


class String(Token):
    start_to_ends = {'"': '"', "'": "'", '«': '»'}

    def __init__(self, value=''):
        self.value = value

    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(String.start_to_ends)

    def parse(self, parser):
        start = parser.move()
        while parser.read() != self.start_to_ends[start]:
            self.value += parser.move()
        parser.move()
        parser.hasparsed(self)

    def transpile(self, mesh, path):
        pass

    def __repr__(self):
        return "'%s'" % self.value

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)

    def evaluate(self, mesh, interpreting, interpreted):
        interpreted.append(self)

    def chroot(self, oldroot, newroot):
        return self
