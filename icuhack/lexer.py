from sly import Lexer


class CircuitLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {ID, NUMBER, ASSIGN, LPAREN, RPAREN, GATE, COMMA}

    # String containing ignored characters between tokens
    ignore = " \t"

    # Regular expression rules for tokens
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = r"\d+"
    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"
    GATE = r".cnot|.h|.x|.z|.t"
    COMMA = ","


class TopDefLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {ID, DEF, LPAREN, RPAREN, COLON}

    # String containing ignored characters between tokens
    ignore = " \t"

    # Regular expression rules for tokens
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    DEF = "def"
    LPAREN = r"\("
    RPAREN = r"\)"
    COLON = ":"
