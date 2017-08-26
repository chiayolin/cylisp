def tokenize(prog):
    return prog.replace('(', " ( ").replace(')', " ) ").split()

def atomic(token):
    # TODO: too ungly, re-write required

    try               : return int(token)
    except ValueError :
        try               : return float(token)
        except ValueError : return str(token)

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
    # TODO: more elegant re-implementation required
    
    if       isinstance(tree, str)  : return env[tree]
    elif not isinstance(tree, list) : return tree

    if tree[0] == 'define':
        (symbol, expression) = tree[1:]
        env[symbol] = evaluate(expression, env)
        
        return symbol
    
    else:
        operands = []
        operator = evaluate(tree[0], env)

        for operand in tree[1:]:
            operands += [evaluate(operand, env)]
    
        return operator(*operands)

def repl():
    print("Welcome to CyLISP v0.1-alpha.")
    
    env = default_env()
    
    while True:
        program = input("> ")
        if program:
            print(evaluate(parse(tokenize(program))[0], env))

__name__ == "__main__" and repl()
