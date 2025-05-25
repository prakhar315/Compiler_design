"""
Simple Flowchart Server
Standalone server for generating flowcharts from C code.
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class FlowchartHandler(BaseHTTPRequestHandler):
    """HTTP request handler for flowchart API."""

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
            flowchart_text = self.generate_simple_flowchart(code)

            return {
                'success': True,
                'formatted_output': flowchart_text
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'formatted_output': f"Error during flowchart generation: {str(e)}"
            }

    def generate_simple_flowchart(self, code):
        """Generate a flowchart with proper shapes."""
        lines = code.strip().split('\n')

        flowchart = "Control Flow Graph:\n"
        flowchart += "=" * 50 + "\n\n"

        # Simple analysis
        has_include = any('#include' in line for line in lines)
        has_main = any('main' in line for line in lines)
        has_if = any('if' in line for line in lines)
        has_while = any('while' in line for line in lines)
        has_for = any('for' in line for line in lines)
        has_return = any('return' in line for line in lines)
        has_printf = any('printf' in line for line in lines)
        has_scanf = any('scanf' in line for line in lines)

        # Build flowchart with proper shapes
        # START (Oval shape)
        flowchart += "        ╭─────────────╮\n"
        flowchart += "       ╱     START     ╲\n"
        flowchart += "      ╱                 ╲\n"
        flowchart += "     ╱___________________╲\n"
        flowchart += "                │\n"
        flowchart += "                ▼\n"

        if has_include:
            # Process (Rectangle)
            flowchart += "     ┌─────────────────────┐\n"
            flowchart += "     │   Include Headers   │\n"
            flowchart += "     │   #include <stdio.h>│\n"
            flowchart += "     └─────────┬───────────┘\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        if has_main:
            # Process (Rectangle)
            flowchart += "     ┌─────────────────────┐\n"
            flowchart += "     │   Function main()   │\n"
            flowchart += "     │   Entry Point       │\n"
            flowchart += "     └─────────┬───────────┘\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        # Variable declarations
        declarations = [line.strip() for line in lines if any(dtype in line for dtype in ['int ', 'float ', 'char ', 'double ']) and '=' in line]
        if declarations:
            # Process (Rectangle)
            flowchart += "     ┌─────────────────────┐\n"
            flowchart += "     │  Declare Variables  │\n"
            flowchart += "     │  Initialize Values  │\n"
            flowchart += "     └─────────┬───────────┘\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        if has_scanf:
            # Input (Parallelogram)
            flowchart += "      ╱─────────────────────╲\n"
            flowchart += "     ╱   Input from User    ╲\n"
            flowchart += "    ╱     scanf() function   ╲\n"
            flowchart += "   ╱_________________________╲\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        if has_if:
            # Decision (Diamond)
            flowchart += "               ╱╲\n"
            flowchart += "              ╱  ╲\n"
            flowchart += "             ╱    ╲\n"
            flowchart += "            ╱ IF   ╲\n"
            flowchart += "           ╱ Cond? ╲\n"
            flowchart += "          ╱        ╲\n"
            flowchart += "         ╱__________╲\n"
            flowchart += "        ╱            ╲\n"
            flowchart += "       ╱              ╲\n"
            flowchart += "   YES │                │ NO\n"
            flowchart += "       ▼                ▼\n"
            flowchart += " ┌─────────┐      ┌─────────┐\n"
            flowchart += " │ Process │      │ Process │\n"
            flowchart += " │ True    │      │ False   │\n"
            flowchart += " │ Branch  │      │ Branch  │\n"
            flowchart += " └────┬────┘      └────┬────┘\n"
            flowchart += "      │                │\n"
            flowchart += "      └────────┬───────┘\n"
            flowchart += "               ▼\n"

        if has_while or has_for:
            # Loop Decision (Diamond)
            flowchart += "               ╱╲\n"
            flowchart += "              ╱  ╲\n"
            flowchart += "             ╱    ╲\n"
            flowchart += "            ╱ LOOP ╲\n"
            flowchart += "           ╱ Cond? ╲\n"
            flowchart += "          ╱        ╲\n"
            flowchart += "         ╱__________╲\n"
            flowchart += "        ╱            ╲\n"
            flowchart += "       ╱              ╲\n"
            flowchart += "   YES │                │ NO\n"
            flowchart += "       ▼                ▼\n"
            flowchart += " ┌─────────┐             │\n"
            flowchart += " │ Loop    │             │\n"
            flowchart += " │ Body    │             │\n"
            flowchart += " │ Process │             │\n"
            flowchart += " └────┬────┘             │\n"
            flowchart += "      │                  │\n"
            flowchart += "      └──────────────────┘\n"
            flowchart += "               ▼\n"

        if has_printf:
            # Output (Parallelogram)
            flowchart += "      ╱─────────────────────╲\n"
            flowchart += "     ╱   Display Output     ╲\n"
            flowchart += "    ╱    printf() function   ╲\n"
            flowchart += "   ╱_________________________╲\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        if has_return:
            # Process (Rectangle)
            flowchart += "     ┌─────────────────────┐\n"
            flowchart += "     │   Return Statement  │\n"
            flowchart += "     │   Exit Function     │\n"
            flowchart += "     └─────────┬───────────┘\n"
            flowchart += "               │\n"
            flowchart += "               ▼\n"

        # END (Oval shape)
        flowchart += "        ╭─────────────╮\n"
        flowchart += "       ╱      END      ╲\n"
        flowchart += "      ╱                 ╲\n"
        flowchart += "     ╱___________________╲\n"

        # Add legend
        flowchart += "\n\nFlowchart Legend:\n"
        flowchart += "=" * 30 + "\n"
        flowchart += "╭─────╮  Oval: Start/End\n"
        flowchart += "╱     ╲\n"
        flowchart += "╲_____╱\n\n"
        flowchart += "┌─────┐  Rectangle: Process\n"
        flowchart += "│     │\n"
        flowchart += "└─────┘\n\n"
        flowchart += "   ╱╲    Diamond: Decision\n"
        flowchart += "  ╱  ╲\n"
        flowchart += " ╱____╲\n\n"
        flowchart += "╱─────╲  Parallelogram: Input/Output\n"
        flowchart += "╲_____╱\n\n"
        flowchart += "   │     Arrow: Flow Direction\n"
        flowchart += "   ▼\n"

        # Add code analysis
        flowchart += "\nCode Analysis Summary:\n"
        flowchart += "=" * 30 + "\n"
        flowchart += f"• Lines of code: {len([l for l in lines if l.strip()])}\n"
        flowchart += f"• Has includes: {'✓' if has_include else '✗'}\n"
        flowchart += f"• Has main function: {'✓' if has_main else '✗'}\n"
        flowchart += f"• Has conditionals: {'✓' if has_if else '✗'}\n"
        flowchart += f"• Has loops: {'✓' if (has_while or has_for) else '✗'}\n"
        flowchart += f"• Has input: {'✓' if has_scanf else '✗'}\n"
        flowchart += f"• Has output: {'✓' if has_printf else '✗'}\n"

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
    print(f"API endpoint: http://localhost:{port}/flowchart")
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
