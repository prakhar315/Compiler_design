import ply.yacc as yacc

from lexer import tokens, lexer

start = 'program'

def make_node(type_, *children):
    return (type_,) + children

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'ISEQUALS', 'ISNOTEQUALS'),
    ('left', 'ISGREATERTHAN', 'ISLESSTHAN', 'ISGREATERTHANEQUAL', 'ISLESSTHANEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULUS'),
    ('right', 'NOT', 'UMINUS'),
)

def p_program(p):
    '''program : external_declaration
               | program external_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_external_declaration(p):
    '''external_declaration : function
                            | declaration SEMICOLON'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type IDENTIFIER
                   | type IDENTIFIER EQUALS expression'''
    if len(p) == 3:
        p[0] = make_node('Declaration', p[1], p[2])
    else:
        p[0] = make_node('DeclareAssign', p[1], p[2], p[4])

def p_function(p):
    '''function : type IDENTIFIER LPAREN parameter_list RPAREN LBRACE statements RBRACE'''
    p[0] = make_node('Function', p[1], p[2], p[4], p[7])

def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter_list COMMA parameter
                      | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : type IDENTIFIER'''
    p[0] = make_node('Parameter', p[1], p[2])

def p_type(p):
    '''type : INT
            | VOID
            | CHAR
            | FLOAT
            | DOUBLE'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration SEMICOLON
                 | expression SEMICOLON
                 | if_statement
                 | while_statement
                 | for_statement
                 | return_statement
                 | block'''
    p[0] = p[1]

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = make_node('Block', p[2])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = make_node('If', p[3], p[5])
    else:
        p[0] = make_node('IfElse', p[3], p[5], p[7])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = make_node('While', p[3], p[5])

def p_for_statement(p):
    '''for_statement : FOR LPAREN opt_expression SEMICOLON opt_expression SEMICOLON opt_expression RPAREN statement'''
    p[0] = make_node('For', p[3], p[5], p[7], p[9])

def p_opt_expression(p):
    '''opt_expression : expression
                      | empty'''
    p[0] = p[1]

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON
                        | RETURN SEMICOLON'''
    if len(p) == 4:
        p[0] = make_node('Return', p[2])
    else:
        p[0] = make_node('Return', None)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULUS expression
                  | expression ISGREATERTHAN expression
                  | expression ISLESSTHAN expression
                  | expression ISGREATERTHANEQUAL expression
                  | expression ISLESSTHANEQUAL expression
                  | expression ISEQUALS expression
                  | expression ISNOTEQUALS expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = make_node('BinOp', p[2], p[1], p[3])

def p_expression_unary(p):
    '''expression : NOT expression
                  | MINUS expression %prec UMINUS'''
    p[0] = make_node('UnaryOp', p[1], p[2])

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = make_node('Number', p[1])

def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    p[0] = make_node('Identifier', p[1])

def p_expression_assign(p):
    '''expression : IDENTIFIER EQUALS expression'''
    p[0] = make_node('Assign', p[1], p[3])

def p_expression_call(p):
    '''expression : IDENTIFIER LPAREN argument_list RPAREN'''
    p[0] = make_node('FunctionCall', p[1], p[3])

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression
                     | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno}, position {p.lexpos})")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()
