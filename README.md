

Lexer using PLY
A simple lexical analyzer (lexer) for parsing tokens in the C programming language (or C-like syntaxes), built using the PLY (Python Lex-Yacc) library.

This lexer supports:

All standard C keywords.
Common operators and punctuation.
Preprocessor directives, identifiers, numbers, string literals, and character literals.
Features
Tokenizes input source code into meaningful units.
Handles reserved keywords like if, while, for, etc.
Supports arithmetic, bitwise, comparison, and assignment operators.
Recognizes literals: integers, strings ("..."), and characters ('...').
Basic preprocessor directive detection (e.g., #include, #define).
Tokens Recognized
Reserved Keywords
All C11 keywords are supported and mapped to uppercase token names. Examples include:
AUTO, BREAK, CASE, CHAR, CONST, CONTINUE... and many more (see reserved dictionary in source)

Operators & Symbols
PLUS     +
MINUS    -
TIMES    *
DIVIDE   /
MODULUS  %
BITAND   &
BITOR    `
BITXOR   ^
BITNOT   ~
EQUALS   = ...(See full list in tokens tuple)

Literals & Identifiers
NUMBER: Integer constants.
STRINGLITERAL: Double-quoted strings.
CHARLITERAL: Single-quoted characters.
IDENTIFIER: Variable/function names.
Preprocessor Directives
PREPROCESSOR: Anything starting with #, e.g., #include, #define.
Punctuation
SEMICOLON, COLON, COMMA, DOT, etc.


Usage
To use the lexer:
code:
⌄
from lexer import tokenize

code = '''
// desired c code
'''

tokens = tokenize(code)
for token in tokens:
    print(token)
^

Each token object has attributes:

type: The token type (e.g., 'INT', 'IDENTIFIER')
value: The actual value of the token (e.g., 'main', 42)
lineno: Line number where the token was found
lexpos: Position in the input stream
Note: lineno and lexpos are not shown by default. You can enable tracking if needed. 

Requirements :
Python 3.x
PLY library (pip install ply)
Installation
Install dependencies:
bash

installation :

pip install ply
Save the lexer code as lexer.py.

License
MIT License – see LICENSE for details.