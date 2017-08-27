def tokenize(prog):

    return prog.replace('(', " ( ").replace(')', " ) ").split()

def atomic(token):
    # TODO: too ungly, re-write required

    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError: return str(token)

def parse(tokens):
    tree = []
    while tokens:
        token = tokens.pop(0)
        if   token == ')' : break
        elif token == '(' : tree += [parse(tokens)]
        else              : tree += [atomic(token)]

    return tree

def default_env():

    import sys
    import operator as op

    def _atom(x):

        return type(x) != list or x == []

    return {
        # boolean values
        '#t' : True, '#f' : False,

        # control charecters
        '#\\0' : '\0', '#\\a' : '\a', '#\\b' : '\b',
        '#\\t' : '\t', '#\\n' : '\n', '#\\r' : '\r',

        # arithmetic operators
        '+'  : op.add     , '-'  : op.sub, '*' : op.mul,
        '/'  : op.truediv , '>'  : op.gt , '<' : op.lt ,
        '>=' : op.ge      , '<=' : op.le , '=' : op.eq ,
        '//' : op.floordiv,

        # LISP primitive operators
        'eq?'     : lambda x, y: x == y or [],
        'car'     : lambda x: not _atom(x) and x[0]  or [],
        'cdr'     : lambda x: not _atom(x) and x[1:] or [],
        'cons'    : lambda x, y: [x] + list(y),
        'atom?'   : lambda x: _atom(x) or [],

        # other primitives
        'begin'   : lambda *x: x[-1],
        'display' : lambda  s: print(prettify(s), end = '') or '',
        'newline' : lambda   : sys.stdout.write('\n')
    }

def evaluate(tree, env):

    # symbols and constant literals
    if       isinstance(tree, str)  : return env[tree]
    elif not isinstance(tree, list) : return tree

    # special cases
    if tree[0] in ("quote", '"', "'"):

        if   not tree[1:][0]    : return []
        elif len(tree[1:]) == 1 : return tree[1:][0]
        else                    : return tree[1:]

    elif tree[0] == 'define':
        (symbol, expression) = tree[1:]
        env[symbol] = evaluate(expression, env)

        return symbol

    elif tree[0] == 'if':
        (predi, conseq, alter) = tree[1:]
        expression = (conseq if evaluate(predi, env) else alter)

        return evaluate(expression, env)

    elif tree[0] == 'cond':
        clauses = tree[1:]
        for clause in clauses:
            if evaluate(clause[0], env):

                return evaluate(clause[1], env)

        return

    elif tree[0] == 'lambda':
        (formal_param, body) = tree[1:]

        def _procedure(*_args):
            _env = dict(env)
            _env.update(zip(formal_param, _args))

            return evaluate(body, _env)

        return _procedure

    # general applicative-order evaluation
    operands = []
    operator = evaluate(tree[0], env)
    for operand in tree[1:]:
        operands += [evaluate(operand, env)]

    return operator(*operands)

def prettify(expression):
    if isinstance(expression, list):
        tokens = []
        for token in expression:
            tokens += [prettify(token)]

        return '(' + ' '.join(tokens) + ')'

    elif isinstance(expression, bool):

        return '#t' if expression else '#f'

    return str(expression)

def repl():
    print("Welcome to CyLISP v0.1-alpha.")

    env = default_env()

    # load library
    with open("lib.scm", 'r') as f:
         content = f.readlines()
    library = ''.join([x.strip() for x in content])
    evaluate(parse(tokenize(library))[0], env)

    while True:
        try:
            program = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nDieu vous comant.")

            return

        if program:
            print(prettify(evaluate(parse(tokenize(program))[0], env)))

    return

__name__ == "__main__" and repl()
