#!/usr/bin/env python3
# Author: Rahul Gopinath <rahul.gopinath@cispa.saarland>
# License: GPLv3

import sys
from textwrap import dedent
import ast
import astunparse
from astmonkey import transformers

def slurp(src):
    with open(src) as x: return x.read()

class ForkingTransformer(ast.NodeTransformer):
    def visit_If(self, node):
        muid = (node.test.lineno, node.test.col_offset)
        node = ast.If(ast.Call(ast.Name('mu.mutate', None),
            [ast.Str(muid), node.test, ast.Name('f', None)],
            []), node.body, node.orelse)
        return self.generic_visit(node)

    def visit_Assert(self, node):
        node = ast.Expr(ast.Call(ast.Name('mu.verify', None), [node.test, ast.Name('f', None), ast.Num(node.test.lineno)], []))
        return self.generic_visit(node)

def forking_transform(src):
    return astunparse.unparse(ForkingTransformer().visit(ast.parse(src)))

def main(args):
    tmpl = """
    import mu
    f = mu.Forker()

    %s

    f.waitfor()
    """
    t = ast.parse(slurp(args[1]))
    print(dedent(tmpl) % forking_transform(t))

if __name__ == '__main__': main(sys.argv)
