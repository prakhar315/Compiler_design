from ply import lex

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
    'INT',
    'RETURN',
    'LBRACE',
    'RBRACE'
)

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
t_INT = r'int'
t_RETURN = r'return'

reserved = {
    'int': 'INT',
    'return': 'RETURN'
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

data = '''
int main() {
    int a = 5;
    int b = 10;
    return a + b;
}
'''

lexer.input(data)
for tok in lexer:
    print(tok)