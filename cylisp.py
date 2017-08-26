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
    
    return {
        '+' : lambda x, y: x +  y,
        '-' : lambda x, y: x -  y,
        '*' : lambda x, y: x *  y,
        '/' : lambda x, y: x /  y,
        '%' : lambda x, y: x %  y,
        '^' : lambda x, y: x ** y,
    }

def evaluate(tree, env):
    # symbols and constant literals
    if       isinstance(tree, str)  : return env[tree]
    elif not isinstance(tree, list) : return tree
    
    # special cases
    if tree[0] == 'quote': 
        
        return tree[1:][0]
    
    elif tree[0] == 'define':
        (symbol, expression) = tree[1:]
        env[symbol] = evaluate(expression, env)
        
        return symbol

    elif tree[0] == 'if':
        (predi, conseq, alter) = tree[1:]
        expression = (conseq if evaluate(predi, env) else alter)

        return evaluate(expression, env)

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

def repl():
    print("Welcome to CyLISP v0.1-alpha.")
    
    env = default_env()
    
    while True:
        try:
            program = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nDieu vous comant.")
            
            return
        
        if program:
            print(evaluate(parse(tokenize(program))[0], env))

    return

__name__ == "__main__" and repl()
