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
