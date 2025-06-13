import os

def load_grammar(file_name):
    """
    Carrega uma gramática a partir de um arquivo BNF.
    Args:
        file_name (str): Nome do arquivo contendo a gramática BNF.
    Returns:
        list: Lista de tuplas contendo os nomes e expressões da gramática.
    Raises:
        SyntaxError: Se a sintaxe do arquivo BNF for inválida.
    
    Formato esperado:
        nome ::= expressão
    """

    # Caminho do diretório onde o script está
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, file_name)

    grammar = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if '::=' not in line:
                raise SyntaxError(f"Linha {line_num}: definição inválida: '{line}'")

            name, expr = line.split('::=', 1)
            grammar.append((name.strip(), expr.strip()))

    return grammar


def load_definition(file_name):
    """
    Carrega uma gramática a partir de um arquivo BNF.
    Args:
        file_name (str): Nome do arquivo contendo a gramática BNF.
    Returns:
        list: Lista de tuplas contendo os nomes e expressões da gramática.
    Raises:
        SyntaxError: Se a sintaxe do arquivo BNF for inválida.
    Formato Esperado:
        nome : expressão.
    """
    # Caminho do diretório onde o script está
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, file_name)

    definition = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ':' not in line:
                raise SyntaxError(f"Linha {line_num}: definição inválida: '{line}'")

            name, expr = line.split(':', 1)
            definition.append((name.strip(), expr.strip()))

    return definition


def main():
    binds = load_definition("lambda.bnf")
    for name, expr in binds:
        print(f"{name} : {expr}")


if __name__ == "__main__":
    main()
