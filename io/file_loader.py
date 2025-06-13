import os

def load_definition(file_name):
    # Caminho do diretório onde o script está
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, file_name)

    bindings = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ':' not in line:
                raise SyntaxError(f"Linha {line_num}: definição inválida: '{line}'")

            name, expr = line.split(':', 1)
            bindings.append((name.strip(), expr.strip()))

    return bindings


def main():
    binds = load_definition("lambda.txt")
    for name, expr in binds:
        print(f"{name} => {expr}")


if __name__ == "__main__":
    main()
