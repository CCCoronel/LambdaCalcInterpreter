# ast_nodes/printer.py

from ast_nodes.nodes import Var, Lambda, App, Expr

def is_nil(expr):
    return isinstance(expr, Var) and expr.name == "nil"

def is_cons(expr):
    # Não usamos o cons literal aqui, detectamos estrutura de App(App(Var(cons), head), tail)
    return isinstance(expr, App) and isinstance(expr.func, App) and isinstance(expr.func.func, Var) and expr.func.func.name == "cons"

def extract_church_number(expr):
    """
    Tenta converter um numeral Church para um número Python inteiro.
    """
    if not isinstance(expr, Lambda):
        return None

    def count_applications(e):
        if isinstance(e, Var):
            return 0
        elif isinstance(e, App):
            return 1 + count_applications(e.arg)
        elif isinstance(e, Lambda):
            return count_applications(e.body)
        else:
            return None

    return count_applications(expr.body)

def to_python_list(expr):
    result = []

    while True:
        if is_nil(expr):
            break
        if is_cons(expr):
            head_expr = expr.func.arg
            tail_expr = expr.arg

            # Tenta extrair numeral de Church
            num_value = extract_church_number(head_expr)
            if num_value is not None:
                result.append(num_value)
            else:
                result.append(f"<{head_expr}>")  # Caso não seja número, só mostra a AST
            expr = tail_expr
        else:
            result.append(f"<{expr}>")  # Caso final não seja nil
            break

    return result

def pretty_print(expr):
    if is_nil(expr):
        print("[]")
    else:
        as_list = to_python_list(expr)
        print(as_list)