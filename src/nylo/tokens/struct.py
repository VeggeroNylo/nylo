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
Contains the Struct class definition.
"""

from collections import defaultdict

from nylo.token import Token
from nylo.tokens.keyword import Keyword, TypeDef
from nylo.tokens.value import Value


class Struct(Token):

    def __init__(self, value=None):
        self.value = value if value else defaultdict(list)
        self.key = Keyword('atoms')

    @staticmethod
    def can_parse(parser):
        return parser.starts_with('(')

    def parse(self, parser):
        if parser.starts_with(':'):
            self.key = parser.getarg()
        elif not parser.starts_with('('):
            self.value[self.key].append(parser.getarg())
            if self.value[self.key][-1] is None:
                self.value[self.key].pop()
            self.key = Keyword('atoms')
        if parser.any_starts_with(('(', ':', ',')):
            parser.move()
            parser.parse(self, Value())
        elif parser.starts_with(')'):
            parser.move()
            if (len(self.value) == 1 and
                    len(self.value[Keyword('atoms')]) == 1):
                return parser.hasparsed(self.value[Keyword('atoms')][0])
            parser.hasparsed(self)
        elif parser.starts_with('->'):
            parser.move(2)
            parser.parse(self, Value())
            self.key = Keyword('self')
        else:
            parser.parse(self, Value())

    def __repr__(self):
        return '(%s)' % ', '.join(f'{key}: {value}' for key, value in self.value.items()
                                  if value)

    def transpile(self, mesh, path):
        self.path = path
        mesh[path + (Keyword('self'),)] = Value(repr(self))
        for key, value in self.value.items():
            if key == Keyword('atoms'):
                for i, el in enumerate(value):
                    if isinstance(el, TypeDef):
                        el = el.value[-1]
                    if isinstance(el, Keyword):
                        arg = path + (el.value,)
                        mesh[arg] = Keyword('placeholder')
                        mesh['arguments'][path].append(arg)
                    else:
                        mesh[path + (Value(i),)] = el
            if isinstance(key, TypeDef):
                key = key.value[-1]
            if isinstance(key, Keyword):
                mesh[path + (key.value,)] = Keyword('placeholder')
        for key, value in self.value.items():
            if isinstance(key, TypeDef):
                key = key.value[-1]
            newpath = path + (key,)
            if len(value) == 1:
                value[0].transpile(mesh, newpath)
                mesh[newpath] = value[0]
            else:
                for i, vl in enumerate(value):
                    vl.transpile(mesh, newpath)
                    mesh[newpath] = vl

    def transpile_call(self, mesh, path, called):
        for key, value in ([*self.value.items()] +
                           [*zip(mesh['arguments'][called],
                                 self.value[Keyword('atoms')])]):
            if isinstance(key, TypeDef):
                key = key.value[-1]
            if key == Keyword('atoms'):
                continue
            if isinstance(key, Keyword):
                if key == Keyword('self'):
                    continue
                key.transpile(mesh, called)
                key = key.ref
                value = value[0]
            key = path + key[len(called):]
            value.transpile(mesh, path)
            mesh[key] = value
        mesh['arguments'][path] = \
            mesh['arguments'][called][len(self.value[Keyword('atoms')]):]

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(Keyword('self', self.path + (Keyword('self'),)))

    def evaluate(self, mesh, interpreting, interpreted):
        interpreted.append(self)

    def chroot(self, oldroot, newroot):
        return self
