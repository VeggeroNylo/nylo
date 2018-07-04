import argparse
import sys
from pprint import pprint as print

import nylo

sys.argv.pop(0)
if not sys.argv:
    sys.argv.append('-h')
parser = argparse.ArgumentParser("Nylo Programming Language")
parser.add_argument('-f', '--file',
                    help='the file you want to evaluate')
parser.add_argument('-v', '--version',
                    help='print current version',
                    action='version',
                    version='nylo 0.1.0')

args = parser.parse_args(sys.argv)

if args.file:
    with open(args.file, 'r') as codefile:
        code = codefile.read()
    struct = nylo.Parser.parsecode(code)
    # print(struct)
    mesh = nylo.builtins
    struct.transpile(mesh, ())
    # print(mesh)
    out = nylo.interprete(mesh)
    print(out)
