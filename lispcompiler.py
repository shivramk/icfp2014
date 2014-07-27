from collections import namedtuple
from cStringIO import StringIO
import sys

Symbol = namedtuple('Symbol', ['token', 'line', 'column'])

class CompileError(Exception): pass

def sym(token, s):
    return Symbol(token, s.line, s.column)

def sym_error_lc(message, line, column):
    return CompileError("Error: Line %d, column %d: %s" % (line,
        column, message))

def sym_error(message, symbol):
    return sym_error_lc(message, symbol.line, symbol.column)

def semantic_error(message):
    return CompileError("Error: %s" % message)

# TODO: STOP, TSEL, TAP, TRAP, DEBUG, BRK

class Assembler(object):
    def __init__(self):
        self.counter = 1
        self.instrs = []
        self.markers = {}

    def get_marker(self, name=None):
        if name is None:
            name = "loc" + str(self.counter)
            self.counter += 1
        if name in self.markers:
            semantic_error("Redefinition of symbol: '%s'" % (name))
        return name

    def insert_marker(self, name):
        # print 'inserting', name, len(self.instrs)
        self.markers[name] = len(self.instrs)

    def fix_ref_(self, instr):
        for idx, arg in enumerate(instr):
            if idx == 0:
                continue
            if isinstance(arg, str):
                instr[idx] = self.markers[arg]

    def add_instr(self, instr):
        # print instr
        self.instrs.append(instr)

    def find_loc(self, loc):
        for key, value in self.markers.iteritems():
            if value == loc:
                return key
        return None

    def get_program(self):
        # First fix all references
        for instr in self.instrs:
            self.fix_ref_(instr)
        s = StringIO()
        for idx, instr in enumerate(self.instrs):
            name = self.find_loc(idx)
            if name is not None:
                s.write("; " + name + "\n")
            s.write(" ".join(str(v) for v in instr) + "\n")
        return s.getvalue()

class Scope(object):
    assembler = Assembler()
    def __init__(self, parent=None):
        self.parent = parent
        self.instrs = []
        self.references = {}
        self.args = {}
        self.funcs = {}
        self.blocks = []

    def lookup(self, var):
        if var in self.funcs:
            return (0, 0) # Dummy
        if var in self.references:
            return (0, self.references[var])
        elif self.parent is not None:
            level, ref = self.parent.lookup(var)
            if ref is None:
                return None, None
            return (level + 1, ref)
        else:
            return None, None

    def add_var(self, var):
        self.references[var] = len(self.references)

    def set_var(self, var, gen_instr=True):
        level, ref = self.lookup(var)
        if ref is None:
            self.add_var(var)
            level, ref = 0, len(self.references) - 1
        # if level != 0:
        #     raise semantic_error("Cant mutate variables from parent scope")
        if gen_instr:
            self.add_instr("ST", level, ref)
        return level, ref

    def get_marker(self, name=None):
        return self.assembler.get_marker(name)

    def insert_marker(self, marker):
        self.instrs.append(marker)

    def load_var(self, var):
        if var in self.funcs:
            self.add_instr("LDF", self.funcs[var])
            return
        level, ref = self.lookup(var)
        if ref is None:
            raise semantic_error("Undefined reference to '%s'" % (var))
        self.add_instr("LD", level, ref)

    def add_instr(self, op, *args):
        instr = [op] + list(args)
        self.instrs.append(instr)

    def insert_code(self):
        code = CodeBlock(self)
        self.blocks.append(code)
        return code

    def insert_function(self, name):
        scope = Function(name, self)
        self.funcs[name] = scope.marker
        self.blocks.append(scope)
        return scope

    def has_references(self):
        return len(self.references) > 0

    def compile(self):
        for instr in self.instrs:
            if isinstance(instr, Scope):
                instr.compile()
            elif isinstance(instr, list):
                self.assembler.add_instr(instr)
            elif isinstance(instr, str):
                # A marker
                self.assembler.insert_marker(instr)
            else:
                assert False
        self.assembler.add_instr(["RTN"])
        for block in self.blocks:
            block.compile()
        
class Function(Scope):
    def __init__(self, name, parent=None):
        Scope.__init__(self, parent)
        self.name = name
        if parent:
            self.marker = parent.get_marker()

    def insert_scope(self):
        scope = Scope(self)
        self.instrs.append(scope)
        return scope

    def compile(self):
        if self.parent:
            self.assembler.insert_marker(self.marker)
        assert len(self.instrs) == 1 and isinstance(self.instrs[0], Scope)
        scope = self.instrs[0]
        marker = self.assembler.get_marker()
        if scope.has_references():
            self.assembler.add_instr(["DUM", len(scope.references)])
            for i in scope.references:
                self.assembler.add_instr(["LDC", 0])
            self.assembler.add_instr(["LDF", marker])
            self.assembler.add_instr(["RAP", len(scope.references)])
        else:
            self.assembler.add_instr(["LDF", marker])
            self.assembler.add_instr(["AP", 0])
        self.assembler.add_instr(["RTN"])
        self.assembler.insert_marker(marker)
        scope.compile()

class CodeBlock(Scope):
    def __init__(self, parent=None):
        Scope.__init__(self, parent)
        self.marker = self.get_marker()

    def lookup(self, var):
        return self.parent.lookup(var)

    def set_var(self, var, gen_instr=True):
        level, ref = self.parent.set_var(var, False)
        if gen_instr:
            self.add_instr("ST", level, ref)
        return level, ref

    def compile(self):
        self.assembler.insert_marker(self.marker)
        for instr in self.instrs:
            if isinstance(instr, list):
                self.assembler.add_instr(instr)
            elif isinstance(instr, str):
                # A marker
                self.assembler.insert_marker(instr)
            else:
                assert False
        self.assembler.add_instr(["JOIN"])
        for block in self.blocks:
            block.compile()

def tokenize(s):
    line, column = 1, 1
    current_token = None
    comment = False
    for ch in s:
        if comment:
            if ch == '\n':
                line = line + 1
                column = 0
                comment = False
        elif ch in (' ', '\t', '\n', '(', ')'):
            if current_token:
                yield tuple(current_token)
                current_token = None
            if ch == '\n':
                line = line + 1
                column = 0
            elif ch == '(' or ch == ')':
                yield (ch, line, column)
        elif ch == ';':
            # Consume input till '\n'
            comment = True
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
        while True:
            if len(tokens) == 0:
                raise sym_error_lc('mismatched (', line, column)
            elif tokens[0][0] == ')':
                break
            L.append(read_expr(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise sym_error_lc('unexpected )', line, column)
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

def compile_if(self, args, stream):
    if not (len(args) == 2 or len(args) == 3):
        raise sym_error('Expected 2/3 arguments, got %d' % len(args), self)
    compile_expr(args[0], stream)
    code1 = stream.insert_code()
    code2 = stream.insert_code()
    stream.add_instr("SEL", code1.marker, code2.marker)

    compile_expr(args[1], code1)
    # Optional else part
    if len(args) == 3:
        compile_expr(args[2], code2)

def compile_define(self, args, parent):
    body = args[1:]
    name = args[0][0].token
    args = args[0][1:]
    stream = parent.insert_function(name)
    local_scope = stream.insert_scope()
    for arg in args:
        stream.add_var(arg.token)
    for expr in body:
        compile_expr(expr, local_scope)
    return stream

def compile_cond(self, args, stream):
    if len(args) < 2:
        raise sym_error('Cond must have at least 2 arguments, got %d' % len(args), self)
    for idx, arg in enumerate(args):
        if not isinstance(arg, list):
            raise sym_error('Cond expects expressions', arg)
        if len(arg) != 2:
            raise sym_error('Each cond expression must have 2 parts', arg)
        if arg[0][0] == 'else':
            if idx != len(args) - 1:
                raise sym_error('else must be the last expression in a cond', arg)
            compile_expr(arg[1], stream)
        else:
            compile_expr(arg[0], stream)
            code1 = stream.insert_code()
            code2 = stream.insert_code()
            stream.add_instr("SEL", code1.marker, code2.marker)
            compile_expr(arg[1], code1)
            stream = code2

def compile_binop(op):
    def compile_op(self, args, stream):
        if len(args) != 2:
            raise sym_error('Expected 2 arguments, got %d' % len(args), self)
        for expr in args:
            compile_expr(expr, stream)
        stream.add_instr(op)
    return compile_op

def compile_uniop(op):
    def compile_op(self, args, stream):
        if len(args) != 1:
            raise sym_error('%s Expected 1 argument, got %d' % (op, len(args)), self)
        compile_expr(args[0], stream)
        stream.add_instr(op)
    return compile_op

def compile_set(self, args, stream):
    if len(args) != 2:
        raise sym_error('%s Expected 2 arguments, got %d' % (self.token, len(args)), self)
    compile_expr(args[1], stream)
    stream.set_var(args[0].token)

def compile_sub(self, args, stream):
    if len(args) == 1:
        compile_binop('SUB')(self, [sym(0, self)] + args, stream)
    elif len(args) == 2:
        compile_binop('SUB')(self, args, stream)
    else:
        raise sym_error('Expected 1 or 2 arguments, got %d' % len(args), self)

def compile_lte(self, args, stream):
    return compile_if(sym('if', self),
            [[sym('>', self)] + args, sym(0, self), sym(1, self)], stream)

def compile_lt(self, args, stream):
    return compile_if(sym('if', self),
            [[sym('>=', self)] + args, sym(0, self), sym(1, self)], stream)

def compile_do(self, args, stream):
    for expr in args:
        compile_expr(expr, stream)

def compile_ne(self, args, stream):
    return compile_if(sym('if', self),
            [[sym('=', self)] + args, sym(0, self), sym(1, self)], stream)

def compile_not(self, args, stream):
    return compile_if(sym('if', self),
            [args[0], sym(0, self), sym(1, self)], stream)

def compile_and(self, args, stream):
    if len(args) != 2:
        raise sym_error('Expected 2 arguments, got %d' % len(args), self)
    return compile_if(sym('if', self), [args[0], 
                [sym('if', self), args[1], sym(1, self), sym(0, self)], 
                sym(0, self)], stream)

def compile_or(self, args, stream):
    if len(args) != 2:
        raise sym_error('Expected 2 arguments, got %d' % len(args), self)
    return compile_if(sym('if', self), [args[0], sym(1, self), args[1]], stream)

def compile_debug(self, args, stream):
    if len(args) != 1:
        raise sym_error('debug Expected 1 argument, got %d' % len(args), self)
    compile_expr(args[0], stream)
    stream.add_instr("DBUG")

builtins = {
    '+': compile_binop('ADD'),
    '-': compile_sub,
    '*': compile_binop('MUL'),
    '/': compile_binop('DIV'),
    '=': compile_binop('CEQ'),
    '>': compile_binop('CGT'),
    '>=': compile_binop('CGTE'),
    'cons': compile_binop('CONS'),
    'atom?': compile_uniop('ATOM'),
    'car': compile_uniop('CAR'),
    'cdr': compile_uniop('CDR'),
    'define': compile_define,
    'cond': compile_cond,
    'do': compile_do,
    'set!': compile_set,
    'if': compile_if,
    '<': compile_lt,
    '<=': compile_lte,
    '!=': compile_ne,
    'debug': compile_debug,
    'not': compile_not,
    'and': compile_and,
    'or': compile_or,
}

symtable = {}

def compile_atom(expr, stream):
    stream.add_instr("LDC", expr.token)

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
    for key in symtable:
        symtable[key] = Scope.assembler.get_marker(key)
    for expr in exprlist:
        scope = compile_function(expr[1], expr[2:])
        scope.compile()
    return Scope.assembler.get_program()

def compile_function_call(self, args, stream):
    for arg in args:
        compile_expr(arg, stream)
    stream.add_instr("LDF", symtable[self.token])
    stream.add_instr("AP", len(args))

def compile_apply(self, args, stream):
    # Dispatch based on type
    if isinstance(self, list):
        for arg in args:
            compile_expr(arg, stream)
        compile_expr(self, stream)
        stream.add_instr("AP", len(args))
    elif self.token in builtins:
        builtins[self.token](self, args, stream)
    elif self.token in symtable:
        compile_function_call(self, args, stream)
    elif isinstance(self.token, int):
        compile_atom(self, stream)
    else:
        level, ref = stream.lookup(self.token)
        if ref is not None:
            for arg in args:
                compile_expr(arg, stream)
            stream.load_var(self.token)
            stream.add_instr("AP", len(args))
        else:
            raise sym_error("Undefined reference to '%s'" % self.token, self)

def compile_var(self, stream):
    # Check if this is a local
    level, ref = stream.lookup(self.token)
    if ref is not None:
        stream.load_var(self.token)
    elif self.token in symtable:
        stream.add_instr("LDF", symtable[self.token])
    else:
        raise sym_error("Undefined reference to '%s'" % self.token, self)

def compile_expr(expr, stream):
    if isinstance(expr, list):
        compile_apply(expr[0], expr[1:], stream)
    elif isinstance(expr.token, int):
        compile_atom(expr, stream)
    elif isinstance(expr.token, str):
        compile_var(expr, stream)
    else:
        raise sym_error("Unknown type: %s" % str(type(expr)), expr)

def compile_function(definition, body):
    name = definition[0].token
    args = definition[1:]
    stream = Function(name)
    stream.assembler.insert_marker(name)
    local_scope = stream.insert_scope()
    for arg in args:
        stream.add_var(arg.token)
    if name != 'main':
        #stream.write('%s: \n' % name)
        #TODO
        pass
    for expr in body:
        compile_expr(expr, local_scope)
    return stream

def main():
    if len(sys.argv) != 2:
        print "Usage: lispcompiler.py <source>"
        sys.exit(1)

    with open(sys.argv[1]) as f:
        try:
            # Read in the stdlib
            stdlib = open("stdlib.lisp").read()
            code = compile_lisp(parse(stdlib + f.read().strip()))
            sys.stdout.write(code)
        except CompileError, e:
            sys.stderr.write(str(e) + '\n')

if __name__ == "__main__":
    main()
