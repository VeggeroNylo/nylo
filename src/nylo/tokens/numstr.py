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
