"""
Flowchart Package
Control Flow Graph generation and visualization for C code.
"""

from .cfg_nodes import ControlFlowGraph, CFGNode
from .cfg_generator import CFGGenerator
from .graphviz_renderer import GraphvizRenderer, render_cfg_graphviz, render_cfg_text

__version__ = "1.0.0"
__author__ = "C Code Analyzer"

__all__ = ['ControlFlowGraph', 'CFGNode', 'CFGGenerator', 'GraphvizRenderer', 'render_cfg_graphviz', 'render_cfg_text']
