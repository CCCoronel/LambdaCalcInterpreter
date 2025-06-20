from evaluator.evaluator import substitute
from ast_nodes.nodes import Var, Lambda, App, Binding, Expr

def beta_reduce(term):
    if isinstance(term, App):
        if isinstance(term.func, Lambda):
            # Redução beta: ((λx. M) N) → M[x := N]
            return substitute(term.func.body, term.func.param, term.arg)
        else:
            # Tenta reduzir dentro da função ou dentro do argumento
            reduced_func = beta_reduce(term.func)
            if reduced_func != term.func:
                return App(reduced_func, term.arg)
            reduced_arg = beta_reduce(term.arg)
            if reduced_arg != term.arg:
                return App(term.func, reduced_arg)
            return term
    elif isinstance(term, Lambda):
        reduced_body = beta_reduce(term.body)
        if reduced_body != term.body:
            return Lambda(term.param, reduced_body)
        else:
            return term
    else:
        return term


def normalize(term):
    while True:
        reduced = beta_reduce(term)
        if reduced == term:
            break
        term = reduced
    return term
