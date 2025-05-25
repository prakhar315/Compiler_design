"""
AST Formatter
Formats Abstract Syntax Trees into readable text representation.
"""

from ast_nodes import *

class ASTFormatter:
    """
    Formats AST nodes into a readable tree structure.
    """
    
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 2
    
    def format_ast(self, node):
        """
        Format an AST node and its children into a readable string.
        
        Args:
            node: AST node to format
            
        Returns:
            str: Formatted AST representation
        """
        if node is None:
            return "Empty AST"
        
        result = "Abstract Syntax Tree (AST):\n"
        result += "=" * 40 + "\n\n"
        result += self._format_node(node)
        return result
    
    def _format_node(self, node, prefix="", is_last=True):
        """
        Recursively format a node and its children.
        
        Args:
            node: Current AST node
            prefix: Current line prefix for tree structure
            is_last: Whether this is the last child of its parent
            
        Returns:
            str: Formatted node representation
        """
        if node is None:
            return ""
        
        # Create the current line
        connector = "└── " if is_last else "├── "
        line = prefix + connector + self._node_to_string(node) + "\n"
        
        # Format children
        if node.children:
            # Update prefix for children
            child_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                line += self._format_node(child, child_prefix, is_last_child)
        
        return line
    
    def _node_to_string(self, node):
        """
        Convert a single node to its string representation.
        
        Args:
            node: AST node
            
        Returns:
            str: String representation of the node
        """
        if isinstance(node, Program):
            return "Program"
        
        elif isinstance(node, Function):
            params = ", ".join([f"{p.get('type', '')} {p.get('name', '')}" for p in node.parameters])
            return f"Function: {node.get_attribute('return_type')} {node.get_attribute('name')}({params})"
        
        elif isinstance(node, Declaration):
            decl_type = node.get_attribute('decl_type')
            name = node.get_attribute('name')
            data_type = node.get_attribute('data_type')
            return f"Declaration: {data_type} {name} ({decl_type})"
        
        elif isinstance(node, Block):
            stmt_count = len(node.children)
            return f"Block ({stmt_count} statements)"
        
        elif isinstance(node, ReturnStatement):
            return "Return Statement"
        
        elif isinstance(node, IfStatement):
            return "If Statement"
        
        elif isinstance(node, FunctionCall):
            func_name = node.get_attribute('function_name')
            arg_count = len(node.arguments)
            return f"Function Call: {func_name}() ({arg_count} args)"
        
        elif isinstance(node, Identifier):
            name = node.get_attribute('name')
            return f"Identifier: {name}"
        
        elif isinstance(node, Literal):
            value = node.get_attribute('value')
            literal_type = node.get_attribute('literal_type')
            return f"Literal: {value} ({literal_type})"
        
        elif isinstance(node, BinaryOp):
            operator = node.get_attribute('operator')
            return f"Binary Operation: {operator}"
        
        elif isinstance(node, AssignmentStatement):
            operator = node.get_attribute('operator')
            return f"Assignment: {operator}"
        
        elif isinstance(node, PreprocessorDirective):
            directive = node.get_attribute('directive')
            content = node.get_attribute('content')
            if content:
                return f"Preprocessor: #{directive} {content}"
            else:
                return f"Preprocessor: #{directive}"
        
        else:
            # Generic node representation
            attrs = []
            for key, value in node.attributes.items():
                if key != 'line':  # Skip line numbers for cleaner output
                    attrs.append(f"{key}={value}")
            
            attr_str = f"({', '.join(attrs)})" if attrs else ""
            return f"{node.node_type}{attr_str}"

def format_ast_simple(node):
    """
    Simple function to format an AST.
    
    Args:
        node: AST root node
        
    Returns:
        str: Formatted AST string
    """
    formatter = ASTFormatter()
    return formatter.format_ast(node)
