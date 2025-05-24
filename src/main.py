from lexer import lexer
from custom_parser import parser
from flowchart_mapping import generate_flowchart
import pprint

def generate_ast(code):
    """Generate an Abstract Syntax Tree from C code."""
    lexer.input(code)
    print("Tokens:")
    for tok in lexer:
        print(f"{tok.type}: {tok.value}")
    
    lexer.input(code)
    
    try:
        ast = parser.parse(code, lexer=lexer)
        return ast
    except Exception as e:
        print(f"Parser error: {e}")
        return None

def print_ast(ast, indent=0):
    """Pretty print the AST with proper indentation."""
    if isinstance(ast, tuple):
        print("  " * indent + ast[0])
        for child in ast[1:]:
            print_ast(child, indent + 1)
    elif isinstance(ast, list):
        for item in ast:
            print_ast(item, indent)
    else:
        print("  " * indent + str(ast))

def generate_control_flow(ast):
    """Generate a control flow representation from the AST."""
    flow = {'nodes': [], 'edges': []}
    node_id = 0
    
    def process_node(node, parent_id=None):
        nonlocal node_id
        current_id = node_id
        node_id += 1

        if not isinstance(node, (tuple, list)):
            return current_id
        
        if isinstance(node, list):
            # list_id = current_id
            # flow['nodes'].append({'id': list_id, 'type': 'Program'})
            # if parent_id is not None:
            #     flow['edges'].append({'from': parent_id, 'to': list_id})
            # for item in node:
            #     process_node(item, list_id)
            # return list_id
            prev_id = parent_id
            for item in node:
                stmt_id = process_node(item, prev_id)
                prev_id = stmt_id
            return prev_id
        
        node_type = node[0]
        node_info = {'id': current_id, 'type': node_type}
        flow['nodes'].append(node_info)
        
        if parent_id is not None:
            flow['edges'].append({'from': parent_id, 'to': current_id})
        
        if node_type == 'Function':
            node_info['return_type'] = node[1]  # Return type
            node_info['name'] = node[2]  # Function name
            node_info['params'] = process_node(node[3], current_id)  # Parameters
            node_info['body'] = process_node(node[4], current_id)  # Body
            
        elif node_type == 'DeclareAssign':
            node_info['var_type'] = node[1] # Variable type
            node_info['variable'] = node[2] # Variable name
            node_info['value'] = process_node(node[3], current_id)
            
        elif node_type in 'If':
            node_info['condition'] = process_node(node[1], current_id)  # Condition
            node_info['then'] = process_node(node[2], current_id)  # Then branch

        elif node_type == 'IfElse':
            node_info['condition'] = process_node(node[1], current_id) # Condition
            node_info['then'] = process_node(node[2], current_id) # Then branch
            if len(node) > 3:
                node_info['else'] = process_node(node[3], current_id) # Else branch
                
        elif node_type == 'While':
            cond_id = process_node(node[1], current_id)  # Condition
            body_id = process_node(node[2], current_id)  # Body
            node_info['condition'] = cond_id
            node_info['body'] = body_id
            flow['edges'].append({'from': body_id, 'to': cond_id})  # Loop back edge
            
        elif node_type == 'For':
            node_info['init'] = process_node(node[1], current_id) if node[1] else None
            node_info['condition'] = process_node(node[2], current_id) if node[2] else None
            node_info['update'] = process_node(node[3], body_id) if node[3] else None
            node_info['body'] = process_node(node[4], cond_id)
            # Back edge from update to condition
            if node_info['update'] and node_info['condition']:
                flow['edges'].append({'from': node_info['update'], 'to': node_info['condition']})
            
        elif node_type == 'BinOp':
            node_info['operator'] = node[1] # Operator
            node_info['left'] = process_node(node[2], current_id)  # Left
            node_info['right'] = process_node(node[3], current_id)  # Right
            
        elif node_type in ('Number', 'Identifier'):
            node_info['value'] = node[1]

        elif node_type == 'Return':
            if len(node) > 1:
                node_info['returns'] = process_node(node[1], current_id)
            
        return current_id
    
    if ast:
        process_node(ast)
    return flow

# Test cases
test_cases = [
    # Simple function with return
    # """
    # int main() {
    #     return 0;
    # }
    # """
    
    # # Function with variables and arithmetic
    """
    int sum() {
        int a = 5;
        int b = 10;
        return a + b;
    }
    """,
    
    # If-else statement
    """
    void check(int x) {
        if (x > 0) {
            return;
        } else {
            return;
        }
    }
    """
    
    # # While loop
    # """
    # void countdown(int n) {
    #     while (n > 0) {
    #         n = n - 1;
    #     }
    # }
    # """,
    
    # # For loop
    # """
    # void loop() {
    #     for (int i = 0; i < 10; i = i + 1) {
    #         // Do nothing
    #     }
    # }
    # """,
    
    # # Function with parameters
    # """
    # int add(int a, int b) {
    #     return a + b;
    # }
    # """
]

# Run all test cases
for i, test_code in enumerate(test_cases, 1):
    print(f"\n=== Test Case {i} ===")
    print("Input Code:")
    print(test_code.strip())
    
    ast = generate_ast(test_code)
    print("\nAbstract Syntax Tree:")
    if ast:
        print_ast(ast)
    else:
        print("Failed to generate AST")
    
    if ast:
        flow = generate_control_flow(ast)
        print("\nControl Flow Graph:")
        pprint.pprint(flow)
        flowchart = generate_flowchart(flow)
        with open(f"flowchart_{i}.html", "w") as f:
            f.write(flowchart.flowchart())
    