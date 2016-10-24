def tokenize(prog):
    return prog.replace('(', ' ( ').replace(')', ' ) ').split()

# TODO: fix paren error checking 
def parse(tokens):
    def _parse_sexp(tokens, in_paren):
        result = list()
        while len(tokens) != 0:
            if tokens[0] == '(':
                # pop off '(' and append a list recursively
                tokens.pop(0) 
                result.append(_parse_sexp(tokens, True))
            elif tokens[0] == ')':
                return in_paren and result or None
            else:
                result.append(tokens[0])

            len(tokens) != 0 and tokens.pop(0)
     
        return not in_paren and result or None
    
    sexp = _parse_sexp(tokens, False)
    
    if sexp == None or None in sexp: 
        return None
    return sexp

# prototype
print("CyLisp Version 1.0")
tokens = input(">>> ")
parsed = parse(tokenize(tokens))
if parsed == None: print("Error: Unmatched paren(s)")
else: print(parsed)
