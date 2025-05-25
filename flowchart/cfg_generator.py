"""
Control Flow Graph Generator
Generates CFG from C code using the lexer and parser.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lexer.c_lexer import CLexer
from parser.c_parser import CParser
from parser.ast_nodes import *
from .cfg_nodes import ControlFlowGraph

class CFGGenerator:
    """
    Generates Control Flow Graph from C code AST.
    """

    def __init__(self):
        self.lexer = CLexer()
        self.parser = CParser()
        self.cfg = None
        self.current_node = None

    def generate_cfg(self, code):
        """
        Generate CFG from C code.

        Args:
            code (str): C source code

        Returns:
            ControlFlowGraph: Generated CFG
        """
        try:
            # Parse the code to get AST
            ast = self.parser.parse(code)

            # Create new CFG
            self.cfg = ControlFlowGraph()

            # Generate CFG from AST
            self._process_ast_node(ast)

            return self.cfg

        except Exception as e:
            print(f"Error generating CFG: {e}")
            return None

    def _process_ast_node(self, node):
        """
        Process an AST node and generate corresponding CFG nodes.

        Args:
            node: AST node to process

        Returns:
            CFGNode: Last created CFG node
        """
        if node is None:
            return None

        if isinstance(node, Program):
            return self._process_program(node)
        elif isinstance(node, Function):
            return self._process_function(node)
        elif isinstance(node, Block):
            return self._process_block(node)
        elif isinstance(node, IfStatement):
            return self._process_if_statement(node)
        elif isinstance(node, ReturnStatement):
            return self._process_return_statement(node)
        elif isinstance(node, Declaration):
            return self._process_declaration(node)
        elif isinstance(node, AssignmentStatement):
            return self._process_assignment(node)
        elif isinstance(node, FunctionCall):
            return self._process_function_call(node)
        elif isinstance(node, PreprocessorDirective):
            return self._process_preprocessor(node)
        else:
            # Generic processing for other nodes
            return self._process_generic_statement(node)

    def _process_program(self, program):
        """Process the main program node."""
        start_node = self.cfg.create_node("START")
        self.current_node = start_node

        # Process all children
        for child in program.children:
            self.current_node = self._process_ast_node(child)

        # Create end node if we don't have one
        if not self.cfg.end_nodes:
            end_node = self.cfg.create_node("END")
            if self.current_node:
                self.cfg.connect_nodes(self.current_node.node_id, end_node.node_id)

        return self.current_node

    def _process_function(self, function):
        """Process function definition."""
        func_name = function.get_attribute('name')
        return_type = function.get_attribute('return_type')

        # Create function entry node
        func_node = self.cfg.create_node("FUNCTION", f"{return_type} {func_name}()", is_call=False)

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, func_node.node_id)

        self.current_node = func_node

        # Process function body
        for child in function.children:
            self.current_node = self._process_ast_node(child)

        return self.current_node

    def _process_block(self, block):
        """Process code block."""
        for child in block.children:
            self.current_node = self._process_ast_node(child)

        return self.current_node

    def _process_if_statement(self, if_stmt):
        """Process if statement."""
        # Create decision node
        decision_node = self.cfg.create_node("DECISION", "if condition")

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, decision_node.node_id)

        # Process then branch
        then_start = decision_node
        self.current_node = then_start

        if len(if_stmt.children) > 1:  # Has then statement
            then_node = self._process_ast_node(if_stmt.children[1])
        else:
            then_node = decision_node

        # Process else branch if exists
        else_node = decision_node
        if len(if_stmt.children) > 2:  # Has else statement
            self.current_node = decision_node
            else_node = self._process_ast_node(if_stmt.children[2])

        # Create merge node
        merge_node = self.cfg.create_node("PROCESS", "merge")

        # Connect branches to merge
        if then_node:
            self.cfg.connect_nodes(then_node.node_id, merge_node.node_id)
        if else_node and else_node != decision_node:
            self.cfg.connect_nodes(else_node.node_id, merge_node.node_id)
        else:
            self.cfg.connect_nodes(decision_node.node_id, merge_node.node_id)

        return merge_node

    def _process_return_statement(self, return_stmt):
        """Process return statement."""
        return_value = ""
        if return_stmt.children:
            # Simplified - just get the first child's content
            return_value = str(return_stmt.children[0])

        return_node = self.cfg.create_node("RETURN", return_value)

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, return_node.node_id)

        # Connect to end node
        end_node = self.cfg.create_node("END")
        self.cfg.connect_nodes(return_node.node_id, end_node.node_id)

        return return_node

    def _process_declaration(self, declaration):
        """Process variable declaration."""
        decl_type = declaration.get_attribute('data_type')
        name = declaration.get_attribute('name')

        decl_node = self.cfg.create_node("PROCESS", f"{decl_type} {name}")

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, decl_node.node_id)

        return decl_node

    def _process_assignment(self, assignment):
        """Process assignment statement."""
        operator = assignment.get_attribute('operator', '=')

        # Simplified assignment representation
        assign_node = self.cfg.create_node("ASSIGNMENT", f"assignment {operator}")

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, assign_node.node_id)

        return assign_node

    def _process_function_call(self, func_call):
        """Process function call."""
        func_name = func_call.get_attribute('function_name')

        call_node = self.cfg.create_node("FUNCTION", func_name, is_call=True)

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, call_node.node_id)

        return call_node

    def _process_preprocessor(self, preprocessor):
        """Process preprocessor directive."""
        directive = preprocessor.get_attribute('directive')
        content = preprocessor.get_attribute('content', '')

        prep_node = self.cfg.create_node("PROCESS", f"#{directive} {content}")

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, prep_node.node_id)

        return prep_node

    def _process_generic_statement(self, node):
        """Process generic statement."""
        content = f"{node.node_type}"
        if hasattr(node, 'attributes') and node.attributes:
            attrs = ', '.join(f"{k}={v}" for k, v in node.attributes.items())
            content += f"({attrs})"

        stmt_node = self.cfg.create_node("PROCESS", content)

        if self.current_node:
            self.cfg.connect_nodes(self.current_node.node_id, stmt_node.node_id)

        return stmt_node
