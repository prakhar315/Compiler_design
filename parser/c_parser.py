"""
C Language Parser
Generates Abstract Syntax Trees from C code using tokens from the lexer.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lexer.c_lexer import CLexer
from ast_nodes import *

class CParser:
    """
    Simple C parser that generates AST from tokens.
    """

    def __init__(self):
        self.lexer = CLexer()
        self.tokens = []
        self.current_token_index = 0
        self.current_token = None

    def parse(self, code):
        """
        Parse C code and return an AST.

        Args:
            code (str): C source code to parse

        Returns:
            Program: Root AST node
        """
        # Tokenize the code
        self.tokens = self.lexer.tokenize(code)
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None

        # Build AST
        return self.parse_program()

    def advance(self):
        """Move to the next token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def peek(self, offset=1):
        """Look ahead at the next token without advancing."""
        peek_index = self.current_token_index + offset
        if peek_index < len(self.tokens):
            return self.tokens[peek_index]
        return None

    def match(self, token_type):
        """Check if current token matches the given type."""
        return self.current_token and self.current_token['type'] == token_type

    def consume(self, token_type):
        """Consume a token of the given type."""
        if self.match(token_type):
            token = self.current_token
            self.advance()
            return token
        return None

    def parse_program(self):
        """Parse the entire program."""
        program = Program()

        while self.current_token:
            if self.match('HASH'):
                # Preprocessor directive
                directive = self.parse_preprocessor()
                if directive:
                    program.add_child(directive)
            elif self.is_function_definition():
                # Function definition
                func = self.parse_function()
                if func:
                    program.add_child(func)
            elif self.is_declaration():
                # Variable declaration
                decl = self.parse_declaration()
                if decl:
                    program.add_child(decl)
            else:
                # Skip unknown tokens
                self.advance()

        return program

    def parse_preprocessor(self):
        """Parse preprocessor directives."""
        if not self.consume('HASH'):
            return None

        if self.match('INCLUDE'):
            directive = self.current_token['value']
            self.advance()

            content = None
            if self.match('HEADER_FILE'):
                content = self.current_token['value']
                self.advance()

            return PreprocessorDirective(directive, content)

        return None

    def is_function_definition(self):
        """Check if current position is a function definition."""
        # Simple heuristic: type identifier ( ... ) {
        if not self.is_type():
            return False

        # Look ahead for identifier ( pattern
        i = 1
        while i < 3 and self.peek(i):
            token = self.peek(i)
            if token['type'] == 'IDENTIFIER':
                next_token = self.peek(i + 1)
                if next_token and next_token['type'] == 'LPAREN':
                    # Look for closing paren and opening brace
                    j = i + 2
                    paren_count = 1
                    while j < len(self.tokens) - self.current_token_index and paren_count > 0:
                        peek_token = self.peek(j)
                        if not peek_token:
                            break
                        if peek_token['type'] == 'LPAREN':
                            paren_count += 1
                        elif peek_token['type'] == 'RPAREN':
                            paren_count -= 1
                        j += 1

                    # Check for opening brace after closing paren
                    if paren_count == 0:
                        brace_token = self.peek(j)
                        if brace_token and brace_token['type'] == 'LBRACE':
                            return True
                break
            i += 1

        return False

    def is_declaration(self):
        """Check if current position is a variable declaration."""
        return self.is_type()

    def is_type(self):
        """Check if current token is a type."""
        type_tokens = ['INT', 'FLOAT', 'DOUBLE', 'CHAR', 'VOID']
        return self.current_token and self.current_token['type'] in type_tokens

    def parse_function(self):
        """Parse function definition."""
        # Parse return type
        if not self.is_type():
            return None

        return_type = self.current_token['value']
        self.advance()

        # Parse function name
        if not self.match('IDENTIFIER'):
            return None

        func_name = self.current_token['value']
        self.advance()

        # Parse parameters
        if not self.consume('LPAREN'):
            return None

        parameters = []
        while self.current_token and not self.match('RPAREN'):
            if self.is_type():
                param_type = self.current_token['value']
                self.advance()

                param_name = None
                if self.match('IDENTIFIER'):
                    param_name = self.current_token['value']
                    self.advance()

                parameters.append({'type': param_type, 'name': param_name})

            if self.match('COMMA'):
                self.advance()

        if not self.consume('RPAREN'):
            return None

        # Create function node
        func = Function(func_name, return_type, parameters)

        # Parse function body
        if self.match('LBRACE'):
            body = self.parse_block()
            if body:
                func.add_child(body)

        return func

    def parse_declaration(self):
        """Parse variable declaration."""
        if not self.is_type():
            return None

        data_type = self.current_token['value']
        self.advance()

        if not self.match('IDENTIFIER'):
            return None

        var_name = self.current_token['value']
        self.advance()

        # Skip initialization if present
        if self.match('ASSIGN'):
            self.advance()
            # Skip the value (simplified)
            while self.current_token and not self.match('SEMICOLON'):
                self.advance()

        if self.match('SEMICOLON'):
            self.advance()

        return Declaration('variable', var_name, data_type)

    def parse_block(self):
        """Parse code block."""
        if not self.consume('LBRACE'):
            return None

        statements = []
        while self.current_token and not self.match('RBRACE'):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                # Skip unknown tokens
                self.advance()

        if self.consume('RBRACE'):
            return Block(statements)

        return None

    def parse_statement(self):
        """Parse a statement."""
        if self.match('RETURN'):
            return self.parse_return_statement()
        elif self.match('IF'):
            return self.parse_if_statement()
        elif self.is_declaration():
            return self.parse_declaration()
        else:
            # Try to parse as expression statement
            return self.parse_expression_statement()

    def parse_return_statement(self):
        """Parse return statement."""
        if not self.consume('RETURN'):
            return None

        value = None
        if not self.match('SEMICOLON'):
            # Parse return value (simplified)
            value = self.parse_simple_expression()

        if self.consume('SEMICOLON'):
            return ReturnStatement(value)

        return None

    def parse_if_statement(self):
        """Parse if statement."""
        if not self.consume('IF'):
            return None

        if not self.consume('LPAREN'):
            return None

        condition = self.parse_simple_expression()

        if not self.consume('RPAREN'):
            return None

        then_stmt = self.parse_statement()

        else_stmt = None
        if self.match('ELSE'):
            self.advance()
            else_stmt = self.parse_statement()

        return IfStatement(condition, then_stmt, else_stmt)

    def parse_expression_statement(self):
        """Parse expression statement."""
        expr = self.parse_simple_expression()
        if self.consume('SEMICOLON'):
            return expr
        return None

    def parse_simple_expression(self):
        """Parse simple expressions (simplified)."""
        if self.match('IDENTIFIER'):
            name = self.current_token['value']
            self.advance()

            # Check for function call
            if self.match('LPAREN'):
                self.advance()
                args = []
                while self.current_token and not self.match('RPAREN'):
                    if self.match('COMMA'):
                        self.advance()
                    else:
                        # Skip argument parsing for simplicity
                        self.advance()

                if self.consume('RPAREN'):
                    return FunctionCall(name, args)

            return Identifier(name)

        elif self.match('INTEGER_LITERAL'):
            value = self.current_token['value']
            self.advance()
            return Literal(value, 'integer')

        elif self.match('STRING_LITERAL'):
            value = self.current_token['value']
            self.advance()
            return Literal(value, 'string')

        else:
            # Skip unknown tokens
            if self.current_token:
                self.advance()
            return None
