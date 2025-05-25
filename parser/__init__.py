"""
C Parser Package
A parser for generating Abstract Syntax Trees from C code.
"""

from .ast_nodes import *
from .c_parser import CParser
from .ast_formatter import format_ast_simple

__version__ = "1.0.0"
__author__ = "C Code Analyzer"

__all__ = ['CParser', 'format_ast_simple', 'ASTNode', 'Program', 'Function', 'Declaration']
