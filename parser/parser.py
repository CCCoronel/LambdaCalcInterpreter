# parser/parser.py

from parser.tokenizer import TokenType, Token, LambdaTokenizer
from ast_nodes.nodes import Var, Lambda, App, Binding, Expr

class ParserError(Exception):
    """Exceção para erros de parsing."""
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return Token(TokenType.EOF, '', -1, -1)
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def expect(self, expected_type: TokenType):
        token = self.current_token()
        if token.type != expected_type:
            raise ParserError(f"Esperado {expected_type}, mas encontrado {token.type} na linha {token.line}, coluna {token.column}")
        self.advance()
        return token

    # --------------------------
    # Entrada principal do parser
    # --------------------------
    def parse(self):
        statements = []
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            statements.append(stmt)
            # Esperar NEWLINE entre statements
            if self.current_token().type == TokenType.NEWLINE:
                self.advance()
            else:
                break  # Se não for newline nem EOF, sai (só pra segurança inicial)
        return statements

    def parse_statement(self):
        """Um statement pode ser uma expressão ou um binding"""
        # Se depois de NAME vier COLON, é binding
        token = self.current_token()
        if token.type == TokenType.NAME:
            next_token = self.tokens[self.pos + 1] if (self.pos + 1) < len(self.tokens) else None
            if next_token and next_token.type == TokenType.COLON:
                return self.parse_binding()
        return self.parse_expression()

    def parse_binding(self):
        name_token = self.expect(TokenType.NAME)
        self.expect(TokenType.COLON)
        expr = self.parse_expression()
        return Binding(name_token.value, expr)

    def parse_expression(self):
        token = self.current_token()

        if token.type == TokenType.NAME:
            self.advance()
            return Var(token.value)

        elif token.type == TokenType.LPAR:
            self.advance()
            next_token = self.current_token()

            if next_token.type in (TokenType.LAMBDA_CHR, TokenType.LAMBDA_STR, TokenType.BACKSLASH):
                return self.parse_lambda()

            # Application com n argumentos: (f x y z)
            exprs = []
            while self.current_token().type != TokenType.RPAR:
                exprs.append(self.parse_expression())
            self.expect(TokenType.RPAR)

            # Encadeia as aplicações: (((f x) y) z)
            expr = exprs[0]
            for arg in exprs[1:]:
                expr = App(expr, arg)
            return expr

        else:
            raise ParserError(f"Token inesperado: {token.type} na linha {token.line}, coluna {token.column}")

    def parse_lambda(self):
        self.advance()  # Consumir lambda token
        param_token = self.expect(TokenType.NAME)
        self.expect(TokenType.DOT)
        body_expr = self.parse_expression()
        self.expect(TokenType.RPAR)
        return Lambda(param_token.value, body_expr)


def parse_tokens(tokens):
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    # Exemplo de teste rápido
    from parser.tokenizer import tokenize_lambda_expression, print_tokens

    code = "(λx. (x x))"
    tokens = tokenize_lambda_expression(code)
    print_tokens(tokens)

    print("\n=== AST ===")
    ast = parse_tokens(tokens)
    for stmt in ast:
        print(stmt)
