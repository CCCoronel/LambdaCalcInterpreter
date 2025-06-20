# evaluator/evaluator.py

from ast_nodes.nodes import Var, Lambda, App, Binding, Expr
from evaluator.enviroment import Environment

def substitute(expr: Expr, var_name: str, replacement: Expr) -> Expr:
    """
    Substitui todas as ocorrências da variável var_name por replacement dentro de expr.
    """
    if isinstance(expr, Var):
        if expr.name == var_name:
            return replacement
        else:
            return expr

    elif isinstance(expr, Lambda):
        if expr.param == var_name:
            return expr  # Variável ligada, não substitui
        else:
            new_body = substitute(expr.body, var_name, replacement)
            return Lambda(expr.param, new_body)

    elif isinstance(expr, App):
        new_func = substitute(expr.func, var_name, replacement)
        new_arg = substitute(expr.arg, var_name, replacement)
        return App(new_func, new_arg)

    else:
        raise TypeError(f"Tipo de expressão desconhecida: {type(expr)}")

def evaluate(expr: Expr, env: Environment) -> Expr:
    """
    Faz a avaliação (redução beta) da expressão no ambiente dado.
    """
    if isinstance(expr, Var):
        # Se for uma variável, busca o valor dela no ambiente
        return evaluate(env.lookup(expr.name), env)

    elif isinstance(expr, Lambda):
        return expr  # Lambda é um valor final (não avalia corpo ainda)

    elif isinstance(expr, App):
        func = evaluate(expr.func, env)
        arg = evaluate(expr.arg, env)

        if isinstance(func, Lambda):
            # Aplicação beta: substitui param por arg no corpo da função
            result = substitute(func.body, func.param, arg)
            return evaluate(result, env)
        else:
            raise TypeError(f"Tentando aplicar uma expressão não-lambda: {func}")
    elif isinstance(expr, Binding):
        # Avalia a expressão ligada e define no ambiente
        evaluated_expr = evaluate(expr.expr, env)
        env.define(expr.name, evaluated_expr)
        return evaluated_expr

    else:
        raise TypeError(f"Tipo de expressão desconhecida: {type(expr)}")
