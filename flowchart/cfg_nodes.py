"""
Control Flow Graph Node Classes
Defines the structure of CFG nodes for flowchart generation.
"""

class CFGNode:
    """Base class for Control Flow Graph nodes."""
    
    def __init__(self, node_id, node_type, content="", **kwargs):
        self.node_id = node_id
        self.node_type = node_type
        self.content = content
        self.successors = []  # List of successor nodes
        self.predecessors = []  # List of predecessor nodes
        self.attributes = kwargs
    
    def add_successor(self, node):
        """Add a successor node."""
        if node not in self.successors:
            self.successors.append(node)
        if self not in node.predecessors:
            node.predecessors.append(self)
    
    def add_predecessor(self, node):
        """Add a predecessor node."""
        if node not in self.predecessors:
            self.predecessors.append(node)
        if self not in node.successors:
            node.successors.append(self)
    
    def __str__(self):
        return f"{self.node_type}({self.node_id}): {self.content}"

class StartNode(CFGNode):
    """Entry point of the control flow graph."""
    
    def __init__(self, node_id):
        super().__init__(node_id, "START", "Program Start")

class EndNode(CFGNode):
    """Exit point of the control flow graph."""
    
    def __init__(self, node_id):
        super().__init__(node_id, "END", "Program End")

class ProcessNode(CFGNode):
    """Node representing a process/statement."""
    
    def __init__(self, node_id, statement):
        super().__init__(node_id, "PROCESS", statement)

class DecisionNode(CFGNode):
    """Node representing a decision/condition."""
    
    def __init__(self, node_id, condition):
        super().__init__(node_id, "DECISION", condition)

class FunctionNode(CFGNode):
    """Node representing a function call or definition."""
    
    def __init__(self, node_id, function_name, is_call=True):
        content = f"Call {function_name}()" if is_call else f"Function {function_name}"
        super().__init__(node_id, "FUNCTION", content)

class ReturnNode(CFGNode):
    """Node representing a return statement."""
    
    def __init__(self, node_id, return_value=None):
        content = f"return {return_value}" if return_value else "return"
        super().__init__(node_id, "RETURN", content)

class LoopNode(CFGNode):
    """Node representing loop constructs."""
    
    def __init__(self, node_id, loop_type, condition=None):
        if condition:
            content = f"{loop_type} ({condition})"
        else:
            content = loop_type
        super().__init__(node_id, "LOOP", content)

class AssignmentNode(CFGNode):
    """Node representing assignment statements."""
    
    def __init__(self, node_id, assignment):
        super().__init__(node_id, "ASSIGNMENT", assignment)

class ControlFlowGraph:
    """Represents a complete control flow graph."""
    
    def __init__(self):
        self.nodes = {}  # Dictionary of node_id -> CFGNode
        self.start_node = None
        self.end_nodes = []  # Can have multiple end nodes
        self.node_counter = 0
    
    def add_node(self, node):
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
        return node
    
    def get_node(self, node_id):
        """Get a node by ID."""
        return self.nodes.get(node_id)
    
    def create_node(self, node_type, content="", **kwargs):
        """Create and add a new node."""
        self.node_counter += 1
        node_id = f"node_{self.node_counter}"
        
        if node_type == "START":
            node = StartNode(node_id)
            self.start_node = node
        elif node_type == "END":
            node = EndNode(node_id)
            self.end_nodes.append(node)
        elif node_type == "PROCESS":
            node = ProcessNode(node_id, content)
        elif node_type == "DECISION":
            node = DecisionNode(node_id, content)
        elif node_type == "FUNCTION":
            is_call = kwargs.get('is_call', True)
            node = FunctionNode(node_id, content, is_call)
        elif node_type == "RETURN":
            node = ReturnNode(node_id, content)
        elif node_type == "LOOP":
            loop_type = kwargs.get('loop_type', 'loop')
            node = LoopNode(node_id, loop_type, content)
        elif node_type == "ASSIGNMENT":
            node = AssignmentNode(node_id, content)
        else:
            node = CFGNode(node_id, node_type, content, **kwargs)
        
        return self.add_node(node)
    
    def connect_nodes(self, from_node_id, to_node_id):
        """Connect two nodes."""
        from_node = self.get_node(from_node_id)
        to_node = self.get_node(to_node_id)
        
        if from_node and to_node:
            from_node.add_successor(to_node)
    
    def get_all_nodes(self):
        """Get all nodes in the graph."""
        return list(self.nodes.values())
    
    def get_edges(self):
        """Get all edges in the graph."""
        edges = []
        for node in self.nodes.values():
            for successor in node.successors:
                edges.append((node.node_id, successor.node_id))
        return edges
