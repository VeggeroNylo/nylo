"""
This modules contains all the function related to interpreting.
"""

from .tokens.keyword import Keyword


def interprete(mesh):
    interpreting, interpreted = [], []
    mesh[(Keyword('self'),)].interprete(mesh, interpreting, interpreted)
    while interpreting:
        interpreting.pop().evaluate(mesh, interpreting, interpreted)
    return interpreted.pop()
