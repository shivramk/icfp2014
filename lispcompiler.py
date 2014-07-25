from collections import namedtuple
from StringIO import StringIO
import sys

Symbol = namedtuple('Symbol', ['token', 'line', 'column'])

class SyntaxError(Exception):
    def __init__(self, message, line=None, column=None):
        if line is None:
            message = "Error: %s" % (message)
        else:
            message = "Error: Line %d, column %d: %s" % (line, column, message)
        Exception.__init__(self, message)

def tokenize(s):
    line, column = 1, 1
    current_token = None
    for ch in s:
        if ch in (' ', '\t', '\n', '(', ')'):
            if current_token:
                yield tuple(current_token)
                current_token = None
            if ch == '\n':
                line = line + 1
                column = 0
            elif ch == '(' or ch == ')':
                yield (ch, line, column)
        elif not current_token:
            current_token = [ch, line, column]
        else:
            current_token[0] += ch
        column += 1
    if current_token:
        yield tuple(current_token)

def read_expr(tokens):
    token, line, column = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0][0] != ')':
            L.append(read_expr(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )', line, column)
    else:
        return Symbol(atom(token), line, column)

def parse(s):
    tokens = list(tokenize(s))
    exprs = []
    while len(tokens) > 0:
        exprs.append(read_expr(tokens))
    return exprs

def atom(token):
    try: 
        return int(token)
    except ValueError:
        try: 
            return float(token)
        except ValueError:
            return token

def compile_add(self, args, stream):
    for expr in args:
        compile_expr(expr, stream)
    stream.write('ADD\n')

def compile_sub(self, args, stream):
    for expr in args:
        compile_expr(expr, stream)
    stream.write('SUB\n')

builtins = {
    '+': compile_add,
    '-': compile_sub
}

symtable = {}

def compile_atom(expr, stream):
    stream.write("LDC %d\n" % (expr.token))

def compile_lisp(exprlist):
    for idx, expr in enumerate(exprlist):
        if expr[0].token != 'define':
            raise SyntaxError("Expected 'define' at top level", expr[0].line,
                    expr[0].column)
        symtable[expr[1][0].token] = idx
    if 'main' not in symtable:
        raise SyntaxError("main function missing")

    # Move main to the top
    mainidx = symtable['main']
    exprlist.insert(0, exprlist.pop(mainidx))
    stream = StringIO()
    for expr in exprlist:
        compile_function(expr[1], expr[2:], stream)
    print stream.getvalue()

def compile_apply(self, args, stream):
    # Dispatch based on type
    if self.token in builtins:
        builtins[self.token](self, args, stream)
    elif self.token in symtable:
        # TODO: Function call
        pass
    elif isinstance(self.token, int):
        compile_atom(self, stream)
    else:
        raise SyntaxError("Undefined reference to '%s'" % self.token,
                self.line, self.column)

def compile_expr(expr, stream):
    if isinstance(expr, list):
        compile_apply(expr[0], expr[1:], stream)
    elif isinstance(expr.token, int):
        compile_atom(expr, stream)
    else:
        raise SyntaxError("Unknown type: %s" % str(type(expr)), 
                expr.line, expr.column)

def compile_function(definition, body, stream):
    name = definition[0].token
    args = definition[1:]
    if name != 'main':
        stream.write('%s: \n', name)
    for expr in body:
        compile_expr(expr, stream)

def main():
    if len(sys.argv) != 2:
        print "Usage: lispcompiler.py <source>"
        sys.exit(1)

    with open(sys.argv[1]) as f:
        try:
            compile_lisp(parse(f.read().strip()))
        except SyntaxError, e:
            print e

if __name__ == "__main__":
    main()
