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
        bindings = load_definition("core.lambda")
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
        #Print de teste
        print(ast_list)
        #Confere cada um dos estados dos nós 
        for stmt in ast_list:
            if isinstance(stmt, Binding):
                # Impossível, pois no core só há expressões (não statements soltos) (calma que é possivel sim)
                env.define(stmt.name, stmt.expr)
            else:
                env.define(name, stmt)

    print("\n=== Ambiente carregado com sucesso! ===")
    print(f"Bindings definidos: {list(env.bindings.keys())}")

    # Agora vamos testar uma expressão simples (Aqui ta dando erro ainda)
    test_expr = "(and true false)"

    print(f"\n=== Testando a expressão: {test_expr} ===")
    tokens = tokenize_lambda_expression(test_expr)
    ast_list = parse_tokens(tokens)

    for stmt in ast_list:
        result = evaluate(stmt, env)
        print(f"Resultado da avaliação: {result}")

if __name__ == "__main__":
    main()
