"""
Web Interface for C Parser
Provides a simple HTTP server to serve AST generation results.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.parse
from c_parser import CParser
from ast_formatter import format_ast_simple

class ParserHandler(BaseHTTPRequestHandler):
    """HTTP request handler for parser API."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/parse':
            # Parse query parameters
            query_params = parse_qs(parsed_path.query)
            code = query_params.get('code', [''])[0]
            
            if code:
                # URL decode the code
                code = urllib.parse.unquote_plus(code)
                result = self.parse_code(code)
                self.send_json_response(result)
            else:
                self.send_error_response("No code provided")
        
        elif parsed_path.path == '/':
            self.send_html_response()
        
        else:
            self.send_404()
    
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
        else:
            self.send_404()
    
    def parse_code(self, code):
        """Parse C code and return AST results."""
        try:
            parser = CParser()
            ast = parser.parse(code)
            formatted_output = format_ast_simple(ast)
            
            return {
                'success': True,
                'ast': self.ast_to_dict(ast),
                'formatted_output': formatted_output
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'formatted_output': f"Error during AST generation: {str(e)}"
            }
    
    def ast_to_dict(self, node):
        """Convert AST node to dictionary for JSON serialization."""
        if node is None:
            return None
        
        result = {
            'node_type': node.node_type,
            'attributes': node.attributes,
            'children': []
        }
        
        for child in node.children:
            child_dict = self.ast_to_dict(child)
            if child_dict:
                result['children'].append(child_dict)
        
        return result
    
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
    
    def send_html_response(self):
        """Send simple HTML test page."""
        html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>C Parser API</title>
</head>
<body>
    <h1>C Parser API</h1>
    <p>This is a simple API for C AST generation.</p>
    <h2>Usage:</h2>
    <ul>
        <li>GET /parse?code=YOUR_C_CODE</li>
        <li>POST /parse with JSON: {"code": "YOUR_C_CODE"}</li>
    </ul>
    
    <h2>Test Form:</h2>
    <form id="testForm">
        <textarea id="codeInput" rows="10" cols="50" placeholder="Enter C code here...">
#include <stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}</textarea><br><br>
        <button type="submit">Parse Code</button>
    </form>
    
    <h2>Results:</h2>
    <pre id="results"></pre>
    
    <script>
        document.getElementById('testForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const code = document.getElementById('codeInput').value;
            
            fetch('/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code: code})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').textContent = data.formatted_output;
            })
            .catch(error => {
                document.getElementById('results').textContent = 'Error: ' + error;
            });
        });
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
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
    """Run the parser HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ParserHandler)
    print(f"Starting C Parser server on port {port}")
    print(f"Visit http://localhost:{port} to test the API")
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
