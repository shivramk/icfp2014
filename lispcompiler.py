from collections import namedtuple
from StringIO import StringIO
import sys

Symbol = namedtuple('Symbol', ['token', 'line', 'column'])

class CompileError(Exception): pass

def sym_error_lc(message, line, column):
    return CompileError("Error: Line %d, column %d: %s" % (line,
        column, message))

def sym_error(message, symbol):
    return sym_error_lc(message, symbol.line, symbol.column)

def semantic_error(message):
    return CompileError("Error: %s" % message)

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
        sym_error_lc('unexpected )', line, column)
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

def compile_binop(op):
    def compile_op(self, args, stream):
        if len(args) != 2:
            raise sym_error('Expected 2 arguments, got %d' % len(args), self)
    return compile_op

builtins = {
    '+': compile_binop('ADD'),
    '-': compile_binop('SUB')
}

symtable = {}

def compile_atom(expr, stream):
    stream.write("LDC %d\n" % (expr.token))

def compile_lisp(exprlist):
    for idx, expr in enumerate(exprlist):
        if expr[0].token != 'define':
            raise sym_error("Expected 'define' at top level", expr[0])
        symtable[expr[1][0].token] = idx
    if 'main' not in symtable:
        raise semantic_error("main function missing")

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
        raise sym_error("Undefined reference to '%s'" % self.token, self)

def compile_expr(expr, stream):
    if isinstance(expr, list):
        compile_apply(expr[0], expr[1:], stream)
    elif isinstance(expr.token, int):
        compile_atom(expr, stream)
    else:
        raise sym_error("Unknown type: %s" % str(type(expr)), expr)

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
        except CompileError, e:
            sys.stderr.write(str(e) + '\n')

if __name__ == "__main__":
    main()
