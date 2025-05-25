"""
Simple AST Server
Standalone server for generating AST from C code.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Simple AST generation without complex imports
def simple_ast_analysis(code):
    """Generate a simple AST-like analysis."""
    lines = code.strip().split('\n')

    ast_output = "Abstract Syntax Tree (AST):\n"
    ast_output += "=" * 40 + "\n\n"

    # Simple parsing
    has_include = any('#include' in line for line in lines)
    has_main = any('main' in line for line in lines)
    has_variables = any(any(dtype in line for dtype in ['int ', 'float ', 'char ', 'double ']) for line in lines)
    has_if = any('if' in line for line in lines)
    has_return = any('return' in line for line in lines)
    has_printf = any('printf' in line for line in lines)

    # Build tree structure
    ast_output += "└── Program\n"

    if has_include:
        ast_output += "    ├── Preprocessor Directive\n"
        ast_output += "    │   └── #include <stdio.h>\n"

    if has_main:
        ast_output += "    └── Function Declaration\n"
        ast_output += "        ├── Return Type: int\n"
        ast_output += "        ├── Name: main\n"
        ast_output += "        ├── Parameters: ()\n"
        ast_output += "        └── Function Body\n"

        if has_variables:
            ast_output += "            ├── Variable Declarations\n"
            # Find variable declarations
            for line in lines:
                line = line.strip()
                if any(dtype in line for dtype in ['int ', 'float ', 'char ', 'double ']) and '=' in line:
                    var_name = line.split()[1].split('=')[0].strip()
                    var_type = line.split()[0]
                    ast_output += f"            │   └── {var_type} {var_name}\n"

        if has_if:
            ast_output += "            ├── Conditional Statement\n"
            ast_output += "            │   ├── Condition Expression\n"
            ast_output += "            │   ├── True Branch\n"
            ast_output += "            │   └── False Branch (optional)\n"

        if has_printf:
            ast_output += "            ├── Function Call\n"
            ast_output += "            │   └── printf()\n"

        if has_return:
            ast_output += "            └── Return Statement\n"
            # Try to find return value
            for line in lines:
                if 'return' in line:
                    return_val = line.split('return')[1].strip().rstrip(';').strip()
                    if return_val:
                        ast_output += f"                └── Value: {return_val}\n"
                    break

    # Add analysis summary
    ast_output += "\nAST Analysis Summary:\n"
    ast_output += "=" * 30 + "\n"
    ast_output += f"• Program structure: {'✓' if has_main else '✗'}\n"
    ast_output += f"• Preprocessor directives: {'✓' if has_include else '✗'}\n"
    ast_output += f"• Variable declarations: {'✓' if has_variables else '✗'}\n"
    ast_output += f"• Control structures: {'✓' if has_if else '✗'}\n"
    ast_output += f"• Function calls: {'✓' if has_printf else '✗'}\n"
    ast_output += f"• Return statements: {'✓' if has_return else '✗'}\n"

    return ast_output

class ASTHandler(BaseHTTPRequestHandler):
    """HTTP request handler for AST API."""

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/parse':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')

                if code:
                    result = self.parse_code(code)
                    self.send_json_response(result)
                else:
                    self.send_error_response("No code provided")

            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON data")
            except Exception as e:
                self.send_error_response(f"Server error: {str(e)}")
        else:
            self.send_404()

    def parse_code(self, code):
        """Parse C code and return AST results."""
        try:
            print(f"Parsing code: {code[:50]}...")  # Debug output

            # Use simple AST analysis
            formatted_output = simple_ast_analysis(code)

            print("AST generated successfully")  # Debug output

            return {
                'success': True,
                'formatted_output': formatted_output
            }

        except Exception as e:
            print(f"Error during parsing: {e}")  # Debug output
            import traceback
            traceback.print_exc()

            return {
                'success': False,
                'error': str(e),
                'formatted_output': f"Error during AST generation: {str(e)}"
            }

    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))

    def send_error_response(self, message):
        """Send error response."""
        error_data = {
            'success': False,
            'error': message,
            'formatted_output': f"Error: {message}"
        }
        self.send_json_response(error_data)

    def send_404(self):
        """Send 404 response."""
        self.send_response(404)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'404 Not Found')

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8002):
    """Run the AST HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ASTHandler)
    print(f"Starting AST server on port {port}")
    print(f"API endpoint: http://localhost:{port}/parse")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8002
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8002.")

    run_server(port)
