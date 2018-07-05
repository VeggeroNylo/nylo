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
Contains the Keyword class definition.
"""

import string

from nylo.token import Token


class TypeDef(Token):

    def __init__(self, value=None):
        self.value = value

    @staticmethod
    def can_parse(parser):
        return parser.any_starts_with(string.ascii_letters + '_')

    def parse(self, parser):
        if self.value is None:
            self.value = []
            return parser.parse(self, Keyword())
        self.value.append(parser.getarg())
        if self.can_parse(parser):
            return parser.parse(self, Keyword())
        return parser.hasparsed(self if len(self.value) > 1
                                else self.value[0])

    def transpile(self, mesh, path):
        self.value[-1].transpile(mesh, path)
        mesh['types'][self.value[-1].value] = self

    def __repr__(self):
        return ' '.join(map(str, self.value)) if self.value else '*'


class Keyword(Token):

    def __init__(self, value='', ref=None):
        self.value, self.ref = value, ref

    def parse(self, parser):
        while parser.read() in string.ascii_letters + '_':
            self.value += parser.move()
        parser.hasparsed(self)

    def transpile(self, mesh, path):
        for i in reversed(range(len(path) + 1)):
            if path[:i] + (self,) in mesh:
                self.ref = path[:i] + (Keyword(self.value),)
                return
        raise NameError(f"Couldn't find variable {self.value}")

    def __repr__(self):
        return str(self.value) + ('@' + str(self.ref) if self.ref else '')

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.append(self)

    def evaluate(self, mesh, interpreting, interpreted):
        replaces = []
        while self.ref not in mesh:
            for classpath in sorted(mesh['classes'], key=len, reverse=True):
                subpath = self.ref[:len(classpath)]
                if classpath == subpath:
                    fclass = mesh['classes'][classpath]
                    replaces.append((subpath, fclass))
                    self.ref = fclass + self.ref[len(subpath):]
                    break
            else:
                raise NameError(self.ref)
        out = mesh[self.ref]
        for replace in reversed(replaces):
            mesh[self.ref] = out
            out = out.chroot(*replace)
            self.ref = self.chroot(*replace).ref
        out.location = self.ref
        out.interprete(mesh, interpreting, interpreted)

    def chroot(self, newroot, oldroot):
        if self.ref[:len(oldroot)] == oldroot:
            return Keyword(self.value, newroot + self.ref[len(oldroot):])
        return self

    def __hash__(self):
        return hash(self.value)
