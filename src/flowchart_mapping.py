from pyflowchart import Flowchart, StartNode, OperationNode, ConditionNode, EndNode

def generate_flowchart(flowgraph):
    node_map = {}

    for node in flowgraph['nodes']:
        if node['type'] == 'Function':
            node_map[node['id']] = StartNode(f"Function {node['name']}")
        elif node['type'] in ['If', 'IfElse']:
            node_map[node['id']] = ConditionNode(f"Condition {node['id']}")
        elif node['type'] == 'While':
            node_map[node['id']] = ConditionNode(f"While {node['id']}")
        elif node['type'] == 'Return':
            node_map[node['id']] = EndNode(f"Return {node['id']}")
        else:
            node_map[node['id']] = OperationNode(f"Operation {node['id']}")


    for edge in flowgraph['edges']:
        from_node = node_map[edge['from']]
        to_node = node_map[edge['to']]
        
        if isinstance(from_node, ConditionNode):
            if not from_node.connections:
                from_node.connect_yes(to_node)
            else:
                from_node.connect_no(to_node)
        else:
            from_node.connect(to_node)

    root = next(n for n in flowgraph['nodes'] if n['type'] == 'Function')
    return Flowchart(node_map[root['id']])