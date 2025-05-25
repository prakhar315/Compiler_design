"""
Web Interface for Flowchart Generator
Provides HTTP server for control flow graph generation.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.parse

class FlowchartHandler(BaseHTTPRequestHandler):
    """HTTP request handler for flowchart API."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/flowchart':
            # Parse query parameters
            query_params = parse_qs(parsed_path.query)
            code = query_params.get('code', [''])[0]

            if code:
                # URL decode the code
                code = urllib.parse.unquote_plus(code)
                result = self.generate_flowchart(code)
                self.send_json_response(result)
            else:
                self.send_error_response("No code provided")

        elif parsed_path.path == '/':
            self.send_html_response()

        else:
            self.send_404()

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/flowchart':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                code = data.get('code', '')

                if code:
                    result = self.generate_flowchart(code)
                    self.send_json_response(result)
                else:
                    self.send_error_response("No code provided")

            except json.JSONDecodeError:
                self.send_error_response("Invalid JSON data")
        else:
            self.send_404()

    def generate_flowchart(self, code):
        """Generate flowchart from C code."""
        try:
            # Simple flowchart generation based on code analysis
            flowchart_text = self.generate_simple_flowchart(code)

            return {
                'success': True,
                'formatted_output': flowchart_text,
                'svg_content': None  # SVG generation disabled for simplicity
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'formatted_output': f"Error during flowchart generation: {str(e)}"
            }

    def generate_simple_flowchart(self, code):
        """Generate a simple text-based flowchart."""
        lines = code.strip().split('\n')

        flowchart = "Control Flow Graph:\n"
        flowchart += "=" * 40 + "\n\n"

        # Simple analysis
        has_include = any('#include' in line for line in lines)
        has_main = any('main' in line for line in lines)
        has_if = any('if' in line for line in lines)
        has_while = any('while' in line for line in lines)
        has_for = any('for' in line for line in lines)
        has_return = any('return' in line for line in lines)
        has_printf = any('printf' in line for line in lines)

        # Build flowchart
        flowchart += "┌─────────────┐\n"
        flowchart += "│    START    │\n"
        flowchart += "└─────┬───────┘\n"
        flowchart += "      │\n"

        if has_include:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Include     │\n"
            flowchart += "│ Libraries   │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        if has_main:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Function    │\n"
            flowchart += "│ main()      │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        # Variable declarations
        declarations = [line.strip() for line in lines if any(dtype in line for dtype in ['int ', 'float ', 'char ', 'double ']) and '=' in line]
        if declarations:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Declare     │\n"
            flowchart += "│ Variables   │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        if has_if:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Decision    │\n"
            flowchart += "│ (if stmt)   │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        if has_while or has_for:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Loop        │\n"
            flowchart += "│ Processing  │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        if has_printf:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Output      │\n"
            flowchart += "│ (printf)    │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        if has_return:
            flowchart += "┌─────▼───────┐\n"
            flowchart += "│ Return      │\n"
            flowchart += "│ Statement   │\n"
            flowchart += "└─────┬───────┘\n"
            flowchart += "      │\n"

        flowchart += "┌─────▼───────┐\n"
        flowchart += "│     END     │\n"
        flowchart += "└─────────────┘\n"

        # Add code analysis
        flowchart += "\nCode Analysis:\n"
        flowchart += "-" * 20 + "\n"
        flowchart += f"Lines of code: {len([l for l in lines if l.strip()])}\n"
        flowchart += f"Has includes: {'Yes' if has_include else 'No'}\n"
        flowchart += f"Has main function: {'Yes' if has_main else 'No'}\n"
        flowchart += f"Has conditionals: {'Yes' if has_if else 'No'}\n"
        flowchart += f"Has loops: {'Yes' if (has_while or has_for) else 'No'}\n"
        flowchart += f"Has output: {'Yes' if has_printf else 'No'}\n"

        return flowchart



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
    <title>Flowchart Generator API</title>
</head>
<body>
    <h1>Flowchart Generator API</h1>
    <p>This is a simple API for C code flowchart generation.</p>
    <h2>Usage:</h2>
    <ul>
        <li>GET /flowchart?code=YOUR_C_CODE</li>
        <li>POST /flowchart with JSON: {"code": "YOUR_C_CODE"}</li>
    </ul>

    <h2>Test Form:</h2>
    <form id="testForm">
        <textarea id="codeInput" rows="10" cols="50" placeholder="Enter C code here...">
#include <stdio.h>

int main() {
    int x = 5;
    if (x > 0) {
        printf("Positive");
    } else {
        printf("Non-positive");
    }
    return 0;
}</textarea><br><br>
        <button type="submit">Generate Flowchart</button>
    </form>

    <h2>Results:</h2>
    <pre id="results"></pre>
    <div id="svgContainer"></div>

    <script>
        document.getElementById('testForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const code = document.getElementById('codeInput').value;

            fetch('/flowchart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code: code})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').textContent = data.formatted_output;

                // Display SVG if available
                const svgContainer = document.getElementById('svgContainer');
                if (data.svg_content) {
                    svgContainer.innerHTML = data.svg_content;
                } else {
                    svgContainer.innerHTML = '<p>SVG rendering not available</p>';
                }
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

def run_server(port=8003):
    """Run the flowchart HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, FlowchartHandler)
    print(f"Starting Flowchart server on port {port}")
    print(f"Visit http://localhost:{port} to test the API")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == "__main__":
    port = 8003
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8003.")

    run_server(port)
