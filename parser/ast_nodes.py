"""
AST Node Classes for C Language
Defines the structure of Abstract Syntax Tree nodes.
"""

class ASTNode:
    """Base class for all AST nodes."""
    
    def __init__(self, node_type, **kwargs):
        self.node_type = node_type
        self.children = []
        self.attributes = kwargs
        self.line = kwargs.get('line', 0)
    
    def add_child(self, child):
        """Add a child node."""
        if child is not None:
            self.children.append(child)
    
    def get_attribute(self, name):
        """Get an attribute value."""
        return self.attributes.get(name)
    
    def set_attribute(self, name, value):
        """Set an attribute value."""
        self.attributes[name] = value
    
    def __str__(self):
        return f"{self.node_type}({', '.join(f'{k}={v}' for k, v in self.attributes.items())})"

class Program(ASTNode):
    """Root node representing the entire program."""
    
    def __init__(self):
        super().__init__('Program')

class Declaration(ASTNode):
    """Node representing variable or function declarations."""
    
    def __init__(self, decl_type, name, data_type=None, **kwargs):
        super().__init__('Declaration', decl_type=decl_type, name=name, data_type=data_type, **kwargs)

class Function(ASTNode):
    """Node representing function definitions."""
    
    def __init__(self, name, return_type, parameters=None, **kwargs):
        super().__init__('Function', name=name, return_type=return_type, **kwargs)
        self.parameters = parameters or []

class Statement(ASTNode):
    """Base class for statement nodes."""
    
    def __init__(self, stmt_type, **kwargs):
        super().__init__('Statement', stmt_type=stmt_type, **kwargs)

class Expression(ASTNode):
    """Base class for expression nodes."""
    
    def __init__(self, expr_type, **kwargs):
        super().__init__('Expression', expr_type=expr_type, **kwargs)

class BinaryOp(Expression):
    """Node representing binary operations."""
    
    def __init__(self, operator, left, right, **kwargs):
        super().__init__('BinaryOp', operator=operator, **kwargs)
        self.add_child(left)
        self.add_child(right)

class Identifier(Expression):
    """Node representing identifiers."""
    
    def __init__(self, name, **kwargs):
        super().__init__('Identifier', name=name, **kwargs)

class Literal(Expression):
    """Node representing literals (numbers, strings, etc.)."""
    
    def __init__(self, value, literal_type, **kwargs):
        super().__init__('Literal', value=value, literal_type=literal_type, **kwargs)

class FunctionCall(Expression):
    """Node representing function calls."""
    
    def __init__(self, function_name, arguments=None, **kwargs):
        super().__init__('FunctionCall', function_name=function_name, **kwargs)
        self.arguments = arguments or []
        for arg in self.arguments:
            self.add_child(arg)

class IfStatement(Statement):
    """Node representing if statements."""
    
    def __init__(self, condition, then_stmt, else_stmt=None, **kwargs):
        super().__init__('IfStatement', **kwargs)
        self.add_child(condition)
        self.add_child(then_stmt)
        if else_stmt:
            self.add_child(else_stmt)

class ReturnStatement(Statement):
    """Node representing return statements."""
    
    def __init__(self, value=None, **kwargs):
        super().__init__('ReturnStatement', **kwargs)
        if value:
            self.add_child(value)

class AssignmentStatement(Statement):
    """Node representing assignment statements."""
    
    def __init__(self, target, value, operator='=', **kwargs):
        super().__init__('AssignmentStatement', operator=operator, **kwargs)
        self.add_child(target)
        self.add_child(value)

class Block(Statement):
    """Node representing code blocks."""
    
    def __init__(self, statements=None, **kwargs):
        super().__init__('Block', **kwargs)
        if statements:
            for stmt in statements:
                self.add_child(stmt)

class PreprocessorDirective(ASTNode):
    """Node representing preprocessor directives."""
    
    def __init__(self, directive, content=None, **kwargs):
        super().__init__('PreprocessorDirective', directive=directive, content=content, **kwargs)
