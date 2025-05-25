"""
Graphviz Renderer for Control Flow Graphs
Renders CFG using Graphviz for visualization.
"""

import graphviz
from .cfg_nodes import ControlFlowGraph, CFGNode

class GraphvizRenderer:
    """
    Renders Control Flow Graphs using Graphviz.
    """

    def __init__(self):
        self.graph = None
        self.node_styles = {
            'START': {
                'shape': 'ellipse',
                'style': 'filled',
                'fillcolor': 'lightgreen',
                'fontweight': 'bold'
            },
            'END': {
                'shape': 'ellipse',
                'style': 'filled',
                'fillcolor': 'lightcoral',
                'fontweight': 'bold'
            },
            'PROCESS': {
                'shape': 'box',
                'style': 'filled',
                'fillcolor': 'lightblue'
            },
            'DECISION': {
                'shape': 'diamond',
                'style': 'filled',
                'fillcolor': 'lightyellow'
            },
            'FUNCTION': {
                'shape': 'box',
                'style': 'filled,rounded',
                'fillcolor': 'lightpink'
            },
            'RETURN': {
                'shape': 'box',
                'style': 'filled',
                'fillcolor': 'orange'
            },
            'LOOP': {
                'shape': 'hexagon',
                'style': 'filled',
                'fillcolor': 'lightcyan'
            },
            'ASSIGNMENT': {
                'shape': 'parallelogram',
                'style': 'filled',
                'fillcolor': 'wheat'
            }
        }

    def render_cfg(self, cfg, format='svg', filename=None):
        """
        Render CFG using Graphviz.

        Args:
            cfg (ControlFlowGraph): CFG to render
            format (str): Output format ('svg', 'png', 'pdf', etc.)
            filename (str): Output filename (optional)

        Returns:
            str: Rendered graph content or filename
        """
        if not cfg or not cfg.nodes:
            return self._create_empty_graph(format)

        # Create Graphviz digraph
        self.graph = graphviz.Digraph(
            name='CFG',
            comment='Control Flow Graph',
            format=format
        )

        # Set graph attributes
        self.graph.attr(rankdir='TB')  # Top to bottom layout
        self.graph.attr('node', fontname='Arial', fontsize='10')
        self.graph.attr('edge', fontname='Arial', fontsize='8')

        # Add nodes
        self._add_nodes(cfg)

        # Add edges
        self._add_edges(cfg)

        # Render graph
        if filename:
            return self.graph.render(filename, cleanup=True)
        else:
            return self.graph.source

    def _add_nodes(self, cfg):
        """Add nodes to the Graphviz graph."""
        for node in cfg.get_all_nodes():
            # Get node style
            style = self.node_styles.get(node.node_type, {
                'shape': 'box',
                'style': 'filled',
                'fillcolor': 'white'
            })

            # Format node label
            label = self._format_node_label(node)

            # Add node to graph
            self.graph.node(
                node.node_id,
                label=label,
                **style
            )

    def _add_edges(self, cfg):
        """Add edges to the Graphviz graph."""
        for from_id, to_id in cfg.get_edges():
            from_node = cfg.get_node(from_id)

            # Add edge labels for decision nodes
            edge_attrs = {}
            if from_node and from_node.node_type == 'DECISION':
                # Simple labeling for decision branches
                if len(from_node.successors) == 2:
                    if to_id == from_node.successors[0].node_id:
                        edge_attrs['label'] = 'True'
                        edge_attrs['color'] = 'green'
                    else:
                        edge_attrs['label'] = 'False'
                        edge_attrs['color'] = 'red'

            self.graph.edge(from_id, to_id, **edge_attrs)

    def _format_node_label(self, node):
        """Format node label for display."""
        content = node.content

        # Truncate long content
        if len(content) > 30:
            content = content[:27] + "..."

        # Escape special characters for Graphviz
        content = content.replace('"', '\\"')
        content = content.replace('\n', '\\n')

        return content

    def _create_empty_graph(self, format='svg'):
        """Create an empty graph for error cases."""
        empty_graph = graphviz.Digraph(format=format)
        empty_graph.node('error', 'No flowchart data available',
                        shape='box', style='filled', fillcolor='lightgray')
        return empty_graph.source

    def render_to_text(self, cfg):
        """
        Render CFG as text representation.

        Args:
            cfg (ControlFlowGraph): CFG to render

        Returns:
            str: Text representation of the CFG
        """
        if not cfg or not cfg.nodes:
            return "No flowchart data available."

        output = "Control Flow Graph:\n"
        output += "=" * 40 + "\n\n"

        # List all nodes
        output += "Nodes:\n"
        output += "-" * 20 + "\n"
        for node in cfg.get_all_nodes():
            output += f"{node.node_id}: [{node.node_type}] {node.content}\n"

        output += "\nEdges:\n"
        output += "-" * 20 + "\n"
        for from_id, to_id in cfg.get_edges():
            from_node = cfg.get_node(from_id)
            to_node = cfg.get_node(to_id)
            output += f"{from_id} -> {to_id}\n"
            output += f"  ({from_node.content} -> {to_node.content})\n"

        return output

def render_cfg_graphviz(cfg, format='svg'):
    """
    Convenience function to render CFG with Graphviz.

    Args:
        cfg (ControlFlowGraph): CFG to render
        format (str): Output format

    Returns:
        str: Rendered graph content
    """
    renderer = GraphvizRenderer()
    return renderer.render_cfg(cfg, format)

def render_cfg_text(cfg):
    """
    Convenience function to render CFG as text.

    Args:
        cfg (ControlFlowGraph): CFG to render

    Returns:
        str: Text representation
    """
    renderer = GraphvizRenderer()
    return renderer.render_to_text(cfg)
