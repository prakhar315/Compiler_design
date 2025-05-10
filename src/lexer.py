from ply import lex


# Lexer for C or C-like languages
def tokenize(data):
    # List of token names. This is always required
    tokens = (
        'IDENTIFIER',
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'EQUALS',
        'SEMICOLON',
        'COMMA',
        'LBRACE',
        'RBRACE'
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_EQUALS = r'='
    t_SEMICOLON = r';'
    t_COMMA = r','

    reserved = {
        'alignas': 'ALIGNAS',
        'alignof': 'ALIGNOF',
        'asm': 'ASM',
        'auto': 'AUTO',
        'bool': 'BOOL',
        'break': 'BREAK',
        'case': 'CASE',
        'char': 'CHAR',
        'const': 'CONST',
        'continue': 'CONTINUE',
        'default': 'DEFAULT',
        'do': 'DO',
        'double': 'DOUBLE',
        'else': 'ELSE',
        'enum': 'ENUM',
        'extern': 'EXTERN',
        'false': 'FALSE',
        'float': 'FLOAT',
        'for': 'FOR',
        'goto': 'GOTO',
        'if': 'IF',
        'inline': 'INLINE',
        'int': 'INT',
        'long': 'LONG',
        'nullptr': 'NULLPTR',
        'register': 'REGISTER',
        'restrict': 'RESTRICT',
        'return': 'RETURN',
        'short': 'SHORT',
        'signed': 'SIGNED',
        'sizeof': 'SIZEOF',
        'static': 'STATIC',
        'struct': 'STRUCT',
        'switch': 'SWITCH',
        'true': 'TRUE',
        'typedef': 'TYPEDEF',
        'typeof': 'TYPEOF',
        'union': 'UNION',
        'unsigned': 'UNSIGNED',
        'void': 'VOID',
        'volatile': 'VOLATILE',
        'while': 'WHILE'
    }

    def t_ID(t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
        return t

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)  # Convert to integer
        return t

    t_ignore = ' \t\n'  # Ignore spaces and tabs and newlines

    def t_error(t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    lexer = lex.lex()

    lexer.input(data)
    # for tok in lexer:
    #     print(tok)
    return lexer