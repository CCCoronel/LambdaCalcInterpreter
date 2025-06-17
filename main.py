from lambda_io.file_loader import load_definition
from parser.tokenizer import tokenize_lambda_expression
from parser.parser import parse_tokens
from evaluator.enviroment import Environment
from evaluator.evaluator import evaluate
from ast_nodes.nodes import Binding

def main():
    env = Environment()
    # Carrega todas as definições do core.lambda
    try:
        bindings = load_definition("core.lambda")
    except FileNotFoundError:
        print("Arquivo core.lambda não encontrado.")
        return
    except SyntaxError as e:
        print(f"Erro de sintaxe ao carregar definições: {e}")
        return

    # Parseia cada binding
    for name, expr_str in bindings:
        tokens = tokenize_lambda_expression(expr_str)
        ast_list = parse_tokens(tokens)
        print(ast_list)
        for stmt in ast_list:
            if isinstance(stmt, Binding):
                # Impossível, pois no core só há expressões (não statements soltos)
                env.define(stmt.name, stmt.expr)
            else:
                env.define(name, stmt)

    print("\n=== Ambiente carregado com sucesso! ===")
    print(f"Bindings definidos: {list(env.bindings.keys())}")

    # Agora vamos testar uma expressão simples
    test_expr = "(and true false)"

    print(f"\n=== Testando a expressão: {test_expr} ===")
    tokens = tokenize_lambda_expression(test_expr)
    ast_list = parse_tokens(tokens)

    for stmt in ast_list:
        result = evaluate(stmt, env)
        print(f"Resultado da avaliação: {result}")

if __name__ == "__main__":
    main()
