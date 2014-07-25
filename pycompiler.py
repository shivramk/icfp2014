#!/usr/bin/env python

import sys
import compiler
import compiler.ast as AST
import operator
from lispcompiler import compile_lisp, CompileError, Symbol

# There ought to be a better way of doing this
node_type = lambda node: node.__class__.__name__

def const_handler(node):
    return node.getChildren()[0]

def module_handler(node):
    assert len(node.getChildNodes()) == 1
    return convert(node.getChildNodes()[0])

def stmt_handler(node):
    return map(convert, node.getChildNodes())

def discard_handler(node):
    return convert(node.getChildren()[0])

def bin_op(operator):
    def bin_op_handler(node):
        return [operator] +  map(convert, node.getChildNodes())
    
    return bin_op_handler

def return_handler(node):
    return convert(node.getChildNodes()[0])

def function_handler(node):
    return ['define', [node.name] + list(node.argnames)] + convert(node.code)

def call_func_handler(node):
    return [node.node.name] + map(convert, node.args)

def name_handler(node):
    return node.name

def if_handler(node):
    children = node.getChildren()
    ret = ['if', convert(children[0])] + convert(children[1])

    # If there is an else block
    if len(children) > 2:
        ret.extend(convert(children[2]))
    
    return ret

def compare_handler(node):
    return [node.ops[0][0], convert(node.expr), convert(node.ops[0][1])]

def format_expr(expr):
    if isinstance(expr, list):
        return '(' + " ".join(map(format_expr, expr)) + ')'
    return str(expr)

synmap = {
    'Module': module_handler,
    'Stmt': stmt_handler,
    'Function': function_handler,
    'Return': return_handler,
    'Const': const_handler,
    'CallFunc': call_func_handler,
    'Discard': discard_handler,
    'Add': bin_op('+'),
    'Sub': bin_op('-'),
    'Div': bin_op('/'),
    'Mul': bin_op('*'),
    'FloorDiv': bin_op('/'), # Wonder if this is correct
    'LeftShift': bin_op('ash'),
    'RightShift': bin_op('ash'), # FIXME
    'Compare': compare_handler,
    'If': if_handler,
    'Name': name_handler
}

def convert(node):
    try:
        func = synmap[node_type(node)]
    except KeyError, e:
        # We don't know how to handle this, so just log a message
        print "Unable to handle %s %s" % (node_type(node), node)
    else:
        return func(node)

def tree2sym(expr):
    if isinstance(expr, list):
        return [tree2sym(e) for e in expr]
    else:
        return Symbol(expr, 1, 1)

def compile(fin):
    ast = compiler.parseFile(fin)
    exprs = convert(ast)
    for expr in exprs:
        print format_expr(expr)
    try:
        code = compile_lisp(tree2sym(exprs))
        sys.stdout.write(code)
    except CompileError, e:
        sys.stderr.write(str(e) + '\n')

def main():
    if len(sys.argv) != 2:
        print "usage: pycompiler.py <infile.py>"
        sys.exit(1)

    compile(sys.argv[1])

if __name__ == "__main__":
    main()
