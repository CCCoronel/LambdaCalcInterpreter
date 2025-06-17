# ast_nodes/nodes.py

from dataclasses import dataclass
from typing import Union

# ------------------------------
# Classe base para todas as expressões
# ------------------------------
class Expr:
    pass

# ------------------------------
# Variável (exemplo: x, true, id)
# ------------------------------
@dataclass
class Var(Expr):
    name: str

    def __repr__(self):
        return f"Var({self.name})"

# ------------------------------
# Abstração lambda (exemplo: λx. corpo)
# ------------------------------
@dataclass
class Lambda(Expr):
    param: str           
    body: Expr            

    def __repr__(self):
        return f"Lambda({self.param}, {self.body})"

# ------------------------------
# Aplicação (exemplo: (f x))
# ------------------------------
@dataclass
class App(Expr):
    func: Expr            
    arg: Expr            

    def __repr__(self):
        return f"App({self.func}, {self.arg})"

# ------------------------------
# Binding (exemplo: id: (λx. x))
# ------------------------------
@dataclass
class Binding:
    name: str
    expr: Expr

    def __repr__(self):
        return f"Binding({self.name}, {self.expr})"

if __name__ == "__main__":
    # Exemplo de AST manual
    example_ast = App(
        Lambda("x", Var("x")),
        Var("y")
    )
    print(example_ast)
