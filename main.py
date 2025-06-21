import sys
from utils.pretty_printer import pretty_print
from utils.normalize import normalize
from lambda_io.file_loader import load_definition
from parser.tokenizer import tokenize_lambda_expression
from parser.parser import parse_tokens
from evaluator.enviroment import Environment
from evaluator.evaluator import evaluate
from ast_nodes.nodes import Binding

def main():
    #Aqui ele cria o ambiente
    env = Environment()
    # Carrega todas as definições do core.lambda
    try:
        #Cria uma lista de tublas com as definições. As tuplas são divididas em (name, expr) sendo name o nome da expressão (id, true, false, etc) e o expr a expressão lambda correspondente 
        bindings = load_definition("../core.lambda")
    except FileNotFoundError:
        print("Arquivo core.lambda não encontrado.")
        return
    except SyntaxError as e:
        print(f"Erro de sintaxe ao carregar definições: {e}")
        return

    
    # Parseia cada binding
    for name, expr_str in bindings:
        #Separa em tokens cada um dos elementos da expressão
        tokens = tokenize_lambda_expression(expr_str)
        #Usa esses tokens para fazer o pareamento e recebe uma lista de estado
        ast_list = parse_tokens(tokens)
        #Confere cada um dos estados dos nós 
        for stmt in ast_list:
            if isinstance(stmt, Binding):
                # Impossível, pois no core só há expressões (não statements soltos) (calma que é possivel sim)
                env.define(stmt.name, stmt.expr)
            else:
                env.define(name, stmt)



    # Agora vamos testar uma expressão simples (Aqui ta dando erro ainda)
    test_expr = "(plus 5 3)"

    print(f"\n=== Testando a expressão: {test_expr} ===")

    if len(sys.argv) > 1:
        test_expr = sys.argv[1]

    tokens = tokenize_lambda_expression(test_expr)
    ast_list = parse_tokens(tokens)
    for stmt in ast_list:
        expr = stmt.expr if isinstance(stmt, Binding) else stmt
        result = evaluate(expr, env)
        print("Resultado:", result)  # Mostra o termo cru
        normalized_result = normalize(result)
        print("Forma legível:")
        pretty_print(normalized_result)

if __name__ == "__main__":
    main()
