from ply import lex


# Lexer for C or C-like languages
def tokenize(data):
    
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


    # List of token names. This is always required
    tokens = (
        'IDENTIFIER',
        'NUMBER',
        'STRINGLITERAL',
        'CHARLITERAL',
        'PREPROCESSOR',
        'EQUALS',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULUS',
        'INCREMENT',
        'DECREMENT',
        'PLUSEQUALS',
        'MINUSEQUALS',
        'TIMESEQUALS',
        'DIVIDEEQUALS',
        'MODULUSEQUALS',
        'ANDEQUALS',
        'OREQUALS',
        'XOREQUALS',
        'LEFTSHIFTEQUALS',
        'RIGHTSHIFTEQUALS',
        'ISEQUALS',
        'ISNOTEQUALS',
        'ISLESSTHAN',
        'ISGREATERTHAN',
        'ISLESSTHANEQUAL',
        'ISGREATERTHANEQUAL',
        'AND',
        'OR',
        'NOT',
        'BITAND',
        'BITOR',
        'BITXOR',
        'BITNOT',
        'BITSHIFTLEFT',
        'BITSHIFTRIGHT',
        'CONDITIONAL',
        'ADDRESSOF',
        'DEREFERNCETO',
        'ARROW',
        'SEMICOLON',
        'COLON',
        'COMMA',
        'DOT',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LSQUARE',
        'RSQUARE'
    ) + tuple(reserved.values())  # Add reserved words to tokens

    # Regular expression rules for simple tokens
    t_PREPROCESSOR = r'\#\s*[a-zA-Z_][a-zA-Z0-9_]*'
    t_STRINGLITERAL = r'"([^\\\"]|\\.)*"'
    t_CHARLITERAL = r"'([^\\']|\\.)*'"
    t_EQUALS = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULUS = r'%'
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'
    t_PLUSEQUALS = r'\+='
    t_MINUSEQUALS = r'-='
    t_TIMESEQUALS = r'\*='
    t_DIVIDEEQUALS = r'/='
    t_MODULUSEQUALS = r'%='
    t_ANDEQUALS = r'&='
    t_OREQUALS = r'\|='
    t_XOREQUALS = r'\^='
    t_LEFTSHIFTEQUALS = r'<<='
    t_RIGHTSHIFTEQUALS = r'>>='
    t_ISEQUALS = r'=='
    t_ISNOTEQUALS = r'!='
    t_ISLESSTHAN = r'<'
    t_ISGREATERTHAN = r'>'
    t_ISLESSTHANEQUAL = r'<='
    t_ISGREATERTHANEQUAL = r'>='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_BITAND = r'&'
    t_BITOR = r'\|'
    t_BITXOR = r'\^'
    t_BITNOT = r'~'
    t_BITSHIFTLEFT = r'<<'
    t_BITSHIFTRIGHT = r'>>'
    t_CONDITIONAL = r'\?'
    t_ADDRESSOF = r'&'
    t_DEREFERNCETO = r'\*'
    t_ARROW = r'->'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_DOT = r'\.'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'

    def t_IDENTIFIER(t):
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