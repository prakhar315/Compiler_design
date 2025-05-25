"""
C Language Lexer and Parser using PLY (Python Lex-Yacc)
This module implements a lexical analyzer and parser for the C programming language.
"""

import ply.lex as lex
import ply.yacc as yacc

class CLexer:
    """
    C Language Lexer class that tokenizes C source code.
    """

    # Reserved words (C keywords)
    reserved = {
        'auto': 'AUTO',
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
        'float': 'FLOAT',
        'for': 'FOR',
        'goto': 'GOTO',
        'if': 'IF',
        'int': 'INT',
        'long': 'LONG',
        'register': 'REGISTER',
        'return': 'RETURN',
        'short': 'SHORT',
        'signed': 'SIGNED',
        'sizeof': 'SIZEOF',
        'static': 'STATIC',
        'struct': 'STRUCT',
        'switch': 'SWITCH',
        'typedef': 'TYPEDEF',
        'union': 'UNION',
        'unsigned': 'UNSIGNED',
        'void': 'VOID',
        'volatile': 'VOLATILE',
        'while': 'WHILE',
        'include': 'INCLUDE',
        'define': 'DEFINE',
        'ifdef': 'IFDEF',
        'ifndef': 'IFNDEF',
        'endif': 'ENDIF',
        'printf': 'PRINTF',
        'scanf': 'SCANF',
    }

    # Token list
    tokens = [
        # Identifiers and literals
        'IDENTIFIER',
        'INTEGER_LITERAL',
        'FLOAT_LITERAL',
        'CHAR_LITERAL',
        'STRING_LITERAL',

        # Operators
        'PLUS',
        'MINUS',
        'MULTIPLY',
        'DIVIDE',
        'MODULO',
        'ASSIGN',
        'PLUS_ASSIGN',
        'MINUS_ASSIGN',
        'MULTIPLY_ASSIGN',
        'DIVIDE_ASSIGN',
        'MODULO_ASSIGN',
        'INCREMENT',
        'DECREMENT',

        # Comparison operators
        'EQ',
        'NE',
        'LT',
        'LE',
        'GT',
        'GE',

        # Logical operators
        'AND',
        'OR',
        'NOT',

        # Bitwise operators
        'BITWISE_AND',
        'BITWISE_OR',
        'BITWISE_XOR',
        'BITWISE_NOT',
        'LEFT_SHIFT',
        'RIGHT_SHIFT',

        # Delimiters
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'SEMICOLON',
        'COMMA',
        'DOT',
        'ARROW',
        'QUESTION',
        'COLON',

        # Preprocessor
        'HASH',
        'HEADER_FILE',

        # Comments
        'COMMENT',
        'MULTILINE_COMMENT',
    ] + list(reserved.values())

    # Token rules

    # Operators (order matters for multi-character operators)
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_MULTIPLY_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_MODULO_ASSIGN = r'%='
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'
    t_LEFT_SHIFT = r'<<'
    t_RIGHT_SHIFT = r'>>'
    t_EQ = r'=='
    t_NE = r'!='
    t_LE = r'<='
    t_GE = r'>='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_ARROW = r'->'

    # Single character operators
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_ASSIGN = r'='
    t_LT = r'<'
    t_GT = r'>'
    t_NOT = r'!'
    t_BITWISE_AND = r'&'
    t_BITWISE_OR = r'\|'
    t_BITWISE_XOR = r'\^'
    t_BITWISE_NOT = r'~'
    t_QUESTION = r'\?'
    t_COLON = r':'

    # Delimiters
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_DOT = r'\.'
    t_HASH = r'\#'

    def __init__(self):
        self.tokens_list = []
        self.lexer = None
        self.build()

    def t_HEADER_FILE(self, t):
        r'<[a-zA-Z_][a-zA-Z0-9_]*\.h>'
        return t

    def t_FLOAT_LITERAL(self, t):
        r'\d+\.\d+([eE][+-]?\d+)?[fF]?'
        t.value = float(t.value.rstrip('fF'))
        return t

    def t_INTEGER_LITERAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CHAR_LITERAL(self, t):
        r"'([^'\\]|\\.)*'"
        return t

    def t_STRING_LITERAL(self, t):
        r'"([^"\\]|\\.)*"'
        return t

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_MULTILINE_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_COMMENT(self, t):
        r'//.*'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        """Build the lexer"""
        self.lexer = lex.lex(module=self, **kwargs)

    def tokenize(self, code):
        """
        Tokenize the given C code and return a list of tokens.

        Args:
            code (str): C source code to tokenize

        Returns:
            list: List of token dictionaries with type, value, line, and position
        """
        self.tokens_list = []
        self.lexer.input(code)

        while True:
            tok = self.lexer.token()
            if not tok:
                break

            token_info = {
                'type': tok.type,
                'value': tok.value,
                'line': tok.lineno,
                'position': tok.lexpos
            }
            self.tokens_list.append(token_info)

        return self.tokens_list

    def get_formatted_output(self, code):
        """
        Get formatted lexical analysis output for display.

        Args:
            code (str): C source code to analyze

        Returns:
            str: Formatted string showing the lexical analysis results
        """
        tokens = self.tokenize(code)

        output = "Lexical Analysis Results:\n"
        output += "=" * 50 + "\n\n"

        if not tokens:
            output += "No tokens found.\n"
            return output

        # Group tokens by type for summary
        token_counts = {}
        for token in tokens:
            token_type = token['type']
            if token_type in token_counts:
                token_counts[token_type] += 1
            else:
                token_counts[token_type] = 1

        # Display token summary
        output += "Token Summary:\n"
        output += "-" * 20 + "\n"
        for token_type, count in sorted(token_counts.items()):
            output += f"{token_type}: {count}\n"

        output += "\nDetailed Token List:\n"
        output += "-" * 30 + "\n"
        output += f"{'Line':<6} {'Type':<20} {'Value':<20} {'Position':<10}\n"
        output += "-" * 60 + "\n"

        for token in tokens:
            value_str = str(token['value'])
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."

            output += f"{token['line']:<6} {token['type']:<20} {value_str:<20} {token['position']:<10}\n"

        return output
