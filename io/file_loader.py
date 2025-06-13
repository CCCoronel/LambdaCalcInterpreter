def load_definition(file_path):
    binds = []
    with open(file_path, 'r', encoding='utf-8') as file:
        print(f"Loading BNF definition from {file_path}")
        for i, line in enumerate(file, 1):
            line = line.strip()
            if line and not line.startswith("#"):  # Ignora linhas vazias e comentários
                binds.append(f"{i}: {line}")
    return binds

def main():
    binds = load_definition("./lambda.bnf")
    for bind in binds:
        print(bind)

if __name__ == "__main__":
    main()