#!/usr/bin/env python

import sys
import compiler
import compiler.ast as AST
import operator
from lispcompiler import compile_lisp, CompileError, Symbol, parse

# There ought to be a better way of doing this
node_type = lambda node: node.__class__.__name__

def const_handler(node):
    return node.getChildren()[0]

def module_handler(node):
    assert len(node.getChildNodes()) == 1
    return convert(node.getChildNodes()[0])

def stmt_handler(node):
    children = node.getChildNodes()
    if len(children) == 1:
        return convert(children[0])
    return map(convert, children)

def discard_handler(node):
    return convert(node.getChildren()[0])

def bin_op(operator):
    def bin_op_handler(node):
        return [operator] +  map(convert, node.getChildNodes())
    
    return bin_op_handler

def return_handler(node):
    return convert(node.getChildNodes()[0])

def function_handler(node):
    return ['define', [node.name] + list(node.argnames), convert(node.code)]

def call_func_handler(node):
    return [node.node.name] + map(convert, node.args)

def name_handler(node):
    return node.name

def if_handler(node):
    children = node.getChildren()
    ret = ['if', convert(children[0]), convert(children[1])]

    # If there is an else block
    if len(children) > 2:
        ret.append(convert(children[2]))
    
    return ret

def compare_handler(node):
    return [node.ops[0][0], convert(node.expr), convert(node.ops[0][1])]

def format_expr(expr):
    if isinstance(expr, list):
        return '(' + " ".join(map(format_expr, expr)) + ')'
    return str(expr)

def cons_children_handler(children):
    assert len(children) > 0
    
    if len(children) == 1:
        return convert(children[0])
        
    if len(children) == 2:
        return ['cons'] + map(convert, children)
    
    return ['cons', convert(children[0]), cons_children_handler(children[1:])]

def tuple_handler(node):
    children = node.getChildren()
    assert len(children) > 1
    return cons_children_handler(children)
    
def list_handler(node):
    return cons_children_handler(node.getChildren() + (AST.Const(0),))

def subscript_handler(node):
    subs = node.subs
    assert len(subs) == 1
    exprType = node_type(node.expr)
    
    # ASSUMPTION is everything embedded in a collection is a List.
    # Tuples embedded in Tuples/Lists will be assumed to be lists!
    if exprType == 'Subscript':
        return ['getlistelem'] + subscript_handler(node.expr) + [convert(subs[0])]
    
    # HACK for handling subscripts on variables.
    # All tuple variables need to start with t_ :D
    # Everything else is assumed to be a list
    if exprType == 'Name':
        if node.expr.name.startswith('t_'):
            exprType = 'Tuple'
        else:
            exprType = 'List'
    
    if exprType != 'List' and exprType != 'Tuple':
        raise CompileError('Subscript on ' + exprType + ' not supported: ' + str(node.expr))
        
    return ['get' + exprType.lower() + 'elem'] + [convert(node.expr), convert(subs[0])]
    
def assign_handler(node):
    assert len(node.nodes) == 1
    
    return ['set!', node.nodes[0].name, convert(node.expr)]
    
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
    'UnarySub': bin_op('-'),
    'Not': bin_op('not'),
    'And': bin_op('and'),
    'Compare': compare_handler,
    'If': if_handler,
    'Name': name_handler,
    'Tuple': tuple_handler,
    'List': list_handler,
    'Subscript': subscript_handler,
    'Assign': assign_handler,
    'NoneType': lambda x: 0
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
        if len(expr) == 1:
            return [tree2sym(expr[0])]
        return [tree2sym(e) for e in expr]
    else:
        return Symbol(expr, 1, 1)

def compile(fin):
    ast = compiler.parseFile(fin)
    exprs = convert(ast)
    exprstr = ''
    for expr in exprs:
        exprstr += format_expr(expr) + '\n'
    print >>sys.stderr, exprstr
    try:
        with open('stdlib.lisp') as f:
            code = compile_lisp(parse(f.read()) + tree2sym(exprs))
            # sys.stdout.write(code)
    except CompileError, e:
        sys.stderr.write(str(e) + '\n')

def main():
    if len(sys.argv) != 2:
        print "usage: pycompiler.py <infile.py>"
        sys.exit(1)

    compile(sys.argv[1])

if __name__ == "__main__":
    main()
