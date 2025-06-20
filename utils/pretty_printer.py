# ast_nodes/printer.py

from ast_nodes.nodes import Var, Lambda, App, Expr
from evaluator.enviroment import Environment

def term_to_string(term):
    if isinstance(term, Var):
        return term.name
    elif isinstance(term, Lambda):
        return f"(λ{term.param}. {term_to_string(term.body)})"
    elif isinstance(term, App):
        return f"({term_to_string(term.func)} {term_to_string(term.arg)})"
    else:
        return str(term)



def church_to_int(term):
    if not isinstance(term, Lambda):
        return None

    param_f = term.param
    body = term.body

    if not isinstance(body, Lambda):
        return None

    param_x = body.param
    inner = body.body

    count = 0
    current = inner

    while isinstance(current, App):
        if isinstance(current.func, Var) and current.func.name == param_f:
            count += 1
            current = current.arg
        else:
            return None
    if isinstance(current, Var) and current.name == param_x:
        return count
    else:
        return None



def pretty_print(term):
    num = church_to_int(term)
    if num is not None:
        print(num)
    else:
        print(term_to_string(term))  # Ou print(term) se não tiver term_to_string

