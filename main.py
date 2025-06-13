from lambda_io.file_loader import load_definition
from parser.tokenizer import tokenize_lambda_expression, print_tokens

def main():
    # Carregar definições de um arquivo
    try:
        bindings = load_definition("./lambda.bnf")  # Ou ajuste o caminho conforme necessário
    except FileNotFoundError:
        print("Arquivo lambda.bnf não encontrado.")
        return
    except SyntaxError as e:
        print(f"Erro de sintaxe no arquivo: {e}")
        return

    print("\n==== Tokens de cada definição carregada ====\n")

    for name, expr in bindings:
        print(f"\n--- Tokenizando a definição: {name} ---")
        print(f"Expressão: {expr}")

        tokens = tokenize_lambda_expression(expr)
        print_tokens(tokens)

    print (f"--------- TESTE BASEADO EM UM CODIGO ---------")

    code = "(λx. x)"
    tokens = tokenize_lambda_expression(code)
    print(f"Codigo: {code}\n")
    for t in tokens:
        print(t)


if __name__ == "__main__":
    main()
