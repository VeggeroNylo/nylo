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
Contains the Lexer class definition.
"""

from abc import ABC as Abstract

from nylo.parser import Parser


class Token(Abstract):
    """This is the base class for every
    Nylo parser.
    """

    def __init__(self, *values):
        """Initialize the token object."""

    def can_parse(parser: Parser) -> bool:
        """Check if the Token can be parsed,
        by checking if the parser starts with
        the character that compose the token.
        Some tokens doesn't need this function.
        """

    def parse(self, parser: Parser):
        """Parse the object by reading parser characters;
        when done, adds the parsed object by calling
        parser.hasparsed; might call parser.parse for
        parsing more tokens.
        """

    def transpile(self, mesh: dict, path: tuple):
        """Traspile the value into the mesh; initialize
        mesh nodes and their values. Returns the token
        that should go to interpretation."""

    def interprete(self, mesh: dict, interpreting: list, interpreted: list):
        raise NotImplemented()  # TODO

    def evaluate(self, mesh: dict, interpreting: list, interpreted: list):
        """Evaluate the Token, adding things to interpreter or
        adding things that has been interpreted to the two lists.
        Values will go to interpreted, while tokens such as
        variables will add other tokens to the interpreting list
        to interpreter.
        """

    def chroot(self, oldroot: tuple, newroot: tuple):
        """Change the root location for absolute variable
        references.
        """

    def __hash__(self):
        return hash(tuple(tuple(x) if isinstance(x, list)
                          else x for key, x in self.__dict__.items()
                          if key != 'location'))

    def __eq__(self, other):
        return hash(self) == hash(other)
