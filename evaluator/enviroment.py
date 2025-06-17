# evaluator/environment.py

class Environment:
    def __init__(self):
        self.bindings = {}

    def define(self, name, expr):
        """Define um novo binding"""
        self.bindings[name] = expr

    def lookup(self, name):
        """Busca o valor associado a um nome"""
        if name in self.bindings:
            return self.bindings[name]
        else:
            raise NameError(f"Nome '{name}' não definido no ambiente.")
