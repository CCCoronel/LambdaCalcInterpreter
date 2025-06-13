import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Iterator


class TokenType(Enum):
    # Symbols
    LPAR = "LPAR"           # (
    RPAR = "RPAR"           # )
    DOT = "DOT"             # .
    COLON = "COLON"         # :
    
    # Lambda variants
    LAMBDA_CHR = "LAMBDA_CHR"     # λ
    LAMBDA_STR = "LAMBDA_STR"     # lambda
    BACKSLASH = "BACKSLASH"       # \
    
    # Identifiers and literals
    NAME = "NAME"           # [a-zA-Z0-9_]+
    
    # Control
    NEWLINE = "NEWLINE"     # \n or \r\n
    EOF = "EOF"             # End of file
    
    # Error
    UNKNOWN = "UNKNOWN"     # Unknown character


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class LambdaTokenizer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Token patterns (order matters for matching)
        self.token_patterns = [
            # Whitespace (except newlines) - skip
            (r'[ \t]+', None),
            
            # Comments (if you want to support them) - skip
            (r'#[^\r\n]*', None),
            
            # Newlines (Windows and Unix style)
            (r'\r\n|\r|\n', TokenType.NEWLINE),
            
            # Lambda variants
            (r'λ', TokenType.LAMBDA_CHR),
            (r'lambda\b', TokenType.LAMBDA_STR),  # \b ensures word boundary
            (r'\\', TokenType.BACKSLASH),
            
            # Symbols
            (r'\(', TokenType.LPAR),
            (r'\)', TokenType.RPAR),
            (r'\.', TokenType.DOT),
            (r':', TokenType.COLON),
            
            # Names (identifiers)
            (r'[a-zA-Z0-9_]+', TokenType.NAME),
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                  for pattern, token_type in self.token_patterns]
    
    def current_char(self) -> Optional[str]:
        """Get current character or None if at end"""
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Peek at character at current position + offset"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self, count: int = 1) -> None:
        """Advance position and update line/column tracking"""
        for _ in range(count):
            if self.pos < len(self.text):
                if self.text[self.pos] == '\n':
                    self.line += 1
                    self.column = 1
                elif self.text[self.pos] == '\r':
                    # Handle \r\n as single newline
                    if self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '\n':
                        self.pos += 1  # Skip the \n part
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
    
    def match_pattern(self) -> Optional[Token]:
        """Try to match current position against token patterns"""
        if self.pos >= len(self.text):
            return Token(TokenType.EOF, "", self.line, self.column)
        
        for pattern, token_type in self.compiled_patterns:
            match = pattern.match(self.text, self.pos)
            if match:
                value = match.group(0)
                token_line = self.line
                token_column = self.column
                
                # Advance position
                self.advance(len(value))
                
                # Skip whitespace and comments (token_type is None)
                if token_type is None:
                    return self.match_pattern()  # Recursively try next token
                
                return Token(token_type, value, token_line, token_column)
        
        # No pattern matched - unknown character
        char = self.current_char()
        token = Token(TokenType.UNKNOWN, char, self.line, self.column)
        self.advance()
        return token
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire input text"""
        tokens = []
        
        while self.pos < len(self.text):
            token = self.match_pattern()
            if token:
                tokens.append(token)
                if token.type == TokenType.EOF:
                    break
        
        # Ensure we have an EOF token
        if not tokens or tokens[-1].type != TokenType.EOF:
            tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        
        return tokens
    
    def tokenize_generator(self) -> Iterator[Token]:
        """Generator version of tokenize for memory efficiency"""
        while self.pos < len(self.text):
            token = self.match_pattern()
            if token:
                yield token
                if token.type == TokenType.EOF:
                    break
        
        # Ensure we have an EOF token
        if self.pos >= len(self.text):
            yield Token(TokenType.EOF, "", self.line, self.column)


def tokenize_lambda_expression(text: str) -> List[Token]:
    """Convenience function to tokenize lambda calculus expressions"""
    tokenizer = LambdaTokenizer(text)
    return tokenizer.tokenize()


def print_tokens(tokens: List[Token]) -> None:
    """Helper function to pretty print tokens"""
    for token in tokens:
        if token.type == TokenType.NEWLINE:
            print(f"{token.type.name:12} {'<newline>':15} at {token.line}:{token.column}")
        else:
            print(f"{token.type.name:12} {repr(token.value):15} at {token.line}:{token.column}")


if __name__ == "__main__":
    # Test the tokenizer
    test_cases = [
        # Basic lambda expression
        "(λx. x)",
        
        # Lambda with different syntaxes
        "(\\x. x)",
        "(lambda x. x)",
        
        # Binding
        "id: (λx. x)",
        
        # Function application
        "((λx. x) y)",
        
        # Complex expression
        """true:(λt. (λf. t))
false:(λt. (λf. f))
and:(λa. (λb. ((a b) a)))""",
        
        # Expression with numbers and underscores
        "test_123: (λf. (λx. (f x)))"
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Input: {repr(test)}")
        print("Tokens:")
        
        tokens = tokenize_lambda_expression(test)
        print_tokens(tokens)