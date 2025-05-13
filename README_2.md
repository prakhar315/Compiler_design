# C-like Language Parser

This project implements a parser for a C-like programming language using PLY (Python Lex-Yacc). The parser reads source code in this C-like language and builds an Abstract Syntax Tree (AST) representing the program structure.

## Overview

This parser works alongside a lexer (referred to in the import statement but not included in this file) to parse a C-like language that supports:

- Variable declarations and assignments
- Function definitions with parameters
- Control structures (if-else, while, for)
- Arithmetic and logical operations
- Function calls

## Requirements

- Python 3.x
- PLY (Python Lex-Yacc)

Install PLY using pip:
```
pip install ply
```

## Project Structure

The project consists of at least two files:
- `lexer.py` - The lexical analyzer (not shown in the provided code)
- `parser.py` - The syntax analyzer (the provided code)

## Language Features

### Data Types
- `int` - Integer type
- `void` - Void type (typically for functions)
- `char` - Character type
- `float` - Floating-point type
- `double` - Double-precision floating-point type

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Logical: `&&` (AND), `||` (OR), `!` (NOT)
- Assignment: `=`

### Control Structures
- `if-else` statements
- `while` loops
- `for` loops
- Function calls
- Return statements

## Parser Components Explanation

### Node Creation
The parser builds an Abstract Syntax Tree (AST) using tuples. Each node in the tree is created with the `make_node` function:

```python
def make_node(type_, *children):
    return (type_,) + children
```

### Operator Precedence
The parser defines operator precedence to ensure expressions are evaluated correctly:

```python
precedence = (
    ('left', 'OR'),                 # lowest precedence
    ('left', 'AND'),
    ('left', 'ISEQUALS', 'ISNOTEQUALS'),
    ('left', 'ISGREATERTHAN', 'ISLESSTHAN', 'ISGREATERTHANEQUAL', 'ISLESSTHANEQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULUS'),
    ('right', 'NOT', 'UMINUS'),     # highest precedence
)
```

### Grammar Rules

#### Program Structure
- A program consists of one or more external declarations
- External declarations can be functions or variable declarations

#### Declarations
- Simple declarations: `type identifier;`
- Declarations with initialization: `type identifier = expression;`

#### Functions
- Function definitions include return type, name, parameters, and a body
- Example: `int main(int argc, char argv[]) { /* statements */ }`

#### Statements
- Declarations
- Expressions
- Control structures (if, while, for)
- Return statements
- Blocks (groups of statements enclosed in braces)

#### Expressions
- Binary operations (arithmetic, comparison, logical)
- Unary operations (negation, logical NOT)
- Function calls
- Variable assignments
- Constants (numbers)
- Variable references

## Key Functions

### Program Structure
- `p_program`: Builds a list of top-level declarations
- `p_external_declaration`: Handles functions and global variable declarations

### Functions and Declarations
- `p_function`: Processes function definitions
- `p_declaration`: Handles variable declarations
- `p_parameter_list`: Processes function parameters

### Statements
- `p_statements`: Builds a list of statements
- `p_statement`: Handles different types of statements
- `p_block`: Processes blocks of statements

### Control Structures
- `p_if_statement`: Handles if and if-else statements
- `p_while_statement`: Processes while loops
- `p_for_statement`: Handles for loops
- `p_return_statement`: Processes return statements

### Expressions
- `p_expression_binop`: Handles binary operations
- `p_expression_unary`: Processes unary operations
- `p_expression_group`: Handles parenthesized expressions
- `p_expression_number`: Processes number literals
- `p_expression_identifier`: Handles variable references
- `p_expression_assign`: Processes assignment operations
- `p_expression_call`: Handles function calls

### Error Handling
- `p_error`: Reports syntax errors with line and position information

## Usage Example

```python
from parser import parser

# Sample code in the C-like language
code = """
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int main() {
    int result;
    result = factorial(5);
    return 0;
}
"""

# Parse the code
ast = parser.parse(code, lexer=lexer)

# Process or print the AST
print(ast)
```

## AST Structure

The Abstract Syntax Tree (AST) is represented as nested tuples with the following pattern:
- First element: Node type (string)
- Remaining elements: Children nodes

Example AST for `int x = 5;`:
```
('DeclareAssign', 'int', 'x', ('Number', 5))
```

## Extending the Parser

To add new language features:
1. Add new token definitions to the lexer
2. Create new grammar rules in the parser
3. Define how to build AST nodes for the new constructs

## Common Issues

- Make sure the lexer (`lexer.py`) is correctly implemented and imports properly
- Syntax errors will show line and position information to help with debugging
- The parser may need adjustments for complex language features
