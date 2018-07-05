# This file is a part of nylo
#
# Copyright (c) 2018 The nylo Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Contains the Symbol class definition.
"""

import operator as op

from nylo.token import Token
from nylo.tokens.value import Value


class Symbol(Token):
    map_to_py = {
        '+': op.add, '-': op.sub, '=': op.eq,
        'and ': op.and_, '>': op.gt, '<': op.lt,
        '!=': op.ne, 'xor ': op.xor, '>=': op.ge,
        '<=': op.le, '*': op.mul, '/': op.truediv,
        '^': op.pow, '%': op.mod, '&': op.add,
        'or ': op.or_, '..': NotImplemented,
        'in ': NotImplemented, '+-': NotImplemented,
        '|': NotImplemented, '.': NotImplemented,
        'not ': op.not_}

    symbols, to_avoid = [*map_to_py], ('->',)

    symbols_priority = (
        ('|',), ('and ', 'or ', 'xor '),
        ('=', '!=', '>=', '<=', 'in ', '>', '<'),
        ('..', '%'), ('+', '-', '&'),
        ('*', '/'), ('^', '+-'), ('.',))

    def __init__(self, op=None, args=None):
        self.op, self.args = op, args if args else []

    def parse(self, parser):
        if not self.op:
            self.op = parser.any_starts_with(self.symbols) or None
            if self.op and not parser.any_starts_with(self.to_avoid):
                parser.move(len(self.op))
                self.args.append(parser.getarg())
                parser.parse(self, Value())
        else:
            self.args.append(parser.getarg())
            if (isinstance(self.args[1], Symbol) and
                    self.priority() > self.args[1].priority()):
                otherobj = self.args[1]
                otherobj.args[0], self.args[1] = self, otherobj.args[0]
                parser.hasparsed(otherobj)
            else:
                parser.hasparsed(self)

    def priority(self):
        "Get the priority of the symbol"
        return [self.op in value for value in self.symbols_priority].index(True)

    def transpile(self, mesh, path):
        for i, arg in enumerate(self.args):
            arg.transpile(mesh, path + (i,))

    def __repr__(self):
        return str(self.op) + ' ' + ' '.join(map(repr, self.args))

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)
        for arg in self.args:
            arg.interprete(mesh, interpreting, interpreted)

    def evaluate(self, mesh, interpreting, interpreted):
        interpreting.append(Value(self.map_to_py[self.op](
            interpreted.pop().value, interpreted.pop().value)))
        if hasattr(self, 'location'):
            mesh[self.location] = interpreting[-1]

    def chroot(self, oldroot, newroot):
        return Symbol(self.op,
                      [arg.chroot(oldroot, newroot) for arg in self.args])
