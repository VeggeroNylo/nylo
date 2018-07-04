"""
This module contains builtin objects in nylo.
"""

from collections import defaultdict

from .token import Token
from .tokens.keyword import Keyword
from .tokens.value import Value


class If(Token):

    def __init__(self, cond=Keyword('cond', (Keyword('if'), Keyword('cond'))),
                 then=Keyword('then', (Keyword('if'), Keyword('then'))),
                 else_=Keyword('else', (Keyword('if'), Keyword('else')))):
        self.cond, self.then, self.else_ = cond, then, else_

    def interprete(self, mesh, interpreting, interpreted):
        interpreting.extend([self, self.cond])

    def evaluate(self, mesh: dict, interpreting: list, interpreted: list):
        interpreting.append(self.then if interpreted.pop().value else self.else_)

    def chroot(self, oldroot: tuple, newroot: tuple):
        return If(self.cond.chroot(oldroot, newroot),
                  self.then.chroot(oldroot, newroot),
                  self.else_.chroot(oldroot, newroot))

    def __repr__(self):
        return "IF"


builtins = {
    'classes': defaultdict(list),
    'types': {},
    'arguments': defaultdict(list, {
        (Keyword('if'),): [(Keyword('if'), Keyword('cond')),
                           (Keyword('if'), Keyword('then')),
                           (Keyword('if'), Keyword('else'))]
    }),
    (Keyword('if'),): (Keyword('placeholder'),),
    (Keyword('if'), Keyword('self')): If(),
    (Keyword('placeholder'),): Value(None)
}
