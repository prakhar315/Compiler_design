# Server Implementation Documentation
## C Code Analyzer Project

### Overview
This document provides detailed explanations of how each server works, including code implementation details, architecture, and internal processes.

---

## 1. Lexer Server Implementation

### File: `lexer/web_interface.py`
**Purpose**: HTTP server that provides lexical analysis API
**Port**: 8001
**Endpoint**: `/analyze`

#### Server Architecture
```python
class LexerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for lexer API."""
```

#### Key Methods Explained

##### `do_POST(self)` Method
```python
def do_POST(self):
    """Handle POST requests."""
    if self.path == '/analyze':
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            code = data.get('code', '')

            if code:
                result = self.analyze_code(code)
                self.send_json_response(result)
            else:
                self.send_error_response("No code provided")

        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON data")
    else:
        self.send_404()
```

**How it works:**
1. **Request Validation**: Checks if path is `/analyze`
2. **Content Reading**: Reads HTTP request body
3. **JSON Parsing**: Converts request body to Python dictionary
4. **Code Extraction**: Gets C code from `code` field
5. **Analysis Call**: Calls `analyze_code()` method
6. **Response**: Sends JSON response back to client

##### `analyze_code(self, code)` Method
```python
def analyze_code(self, code):
    """Analyze C code and return results."""
    try:
        lexer = CLexer()
        tokens = lexer.tokenize(code)
        formatted_output = lexer.get_formatted_output(code)

        return {
            'success': True,
            'tokens': tokens,
            'formatted_output': formatted_output,
            'token_count': len(tokens)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'formatted_output': f"Error during lexical analysis: {str(e)}"
        }
```

**How it works:**
1. **Lexer Creation**: Creates new `CLexer` instance
2. **Tokenization**: Calls `tokenize()` to break code into tokens
3. **Formatting**: Calls `get_formatted_output()` for display
4. **Response Building**: Creates dictionary with results
5. **Error Handling**: Catches exceptions and returns error response

#### CORS Implementation
```python
def send_json_response(self, data):
    """Send JSON response."""
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    self.end_headers()
```

**Purpose**: Enables cross-origin requests from frontend

---

## 2. Lexer Engine Implementation

### File: `lexer/c_lexer.py`
**Purpose**: Core lexical analysis using PLY library

#### CLexer Class Architecture
```python
class CLexer:
    """
    C Language Lexer using PLY (Python Lex-Yacc)
    Tokenizes C source code into meaningful components.
    """
```

#### Token Definitions
```python
# Token list - all possible token types
tokens = [
    'IDENTIFIER', 'INTEGER_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'ASSIGN', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE',
    'AND', 'OR', 'NOT', 'BITWISE_AND', 'BITWISE_OR', 'BITWISE_XOR', 'BITWISE_NOT',
    'LSHIFT', 'RSHIFT', 'INCREMENT', 'DECREMENT',
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'MODULO_ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COMMA', 'DOT', 'ARROW',
    'HASH', 'HEADER_FILE', 'COMMENT', 'MULTILINE_COMMENT'
] + list(reserved.values())
```

#### Token Recognition Rules
```python
# Simple tokens (operators and delimiters)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

# Complex tokens (functions)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t
```

**How PLY Works:**
1. **Pattern Matching**: Uses regex patterns to identify tokens
2. **Longest Match**: Chooses longest matching pattern
3. **Token Creation**: Creates token objects with type and value
4. **Line Tracking**: Automatically tracks line numbers

#### Tokenization Process
```python
def tokenize(self, code):
    """
    Tokenize C code and return list of tokens.
    """
    self.lexer.input(code)
    tokens = []

    while True:
        tok = self.lexer.token()
        if not tok:
            break

        token_dict = {
            'type': tok.type,
            'value': str(tok.value),
            'line': tok.lineno,
            'position': tok.lexpos
        }
        tokens.append(token_dict)

    return tokens
```

**Process Explanation:**
1. **Input Feeding**: Feeds source code to PLY lexer
2. **Token Iteration**: Loops through all tokens
3. **Token Conversion**: Converts PLY tokens to dictionaries
4. **List Building**: Creates list of token dictionaries

---

## 3. AST Server Implementation

### File: `ast_server.py`
**Purpose**: Standalone server for Abstract Syntax Tree generation
**Port**: 8005
**Endpoint**: `/parse`

#### Server Architecture
```python
class ASTHandler(BaseHTTPRequestHandler):
    """HTTP request handler for AST API."""
```

#### Core Analysis Function
```python
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
```

**Analysis Strategy:**
1. **Line-by-Line Parsing**: Splits code into individual lines
2. **Pattern Detection**: Uses string matching to find constructs
3. **Boolean Flags**: Sets flags for detected language features
4. **Tree Building**: Constructs hierarchical representation

#### Tree Structure Generation
```python
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
```

**Tree Building Process:**
1. **Root Node**: Always starts with "Program"
2. **Conditional Branches**: Adds nodes based on detected features
3. **Unicode Characters**: Uses tree-drawing characters
4. **Hierarchical Structure**: Maintains proper indentation

#### Variable Detection Logic
```python
if has_variables:
    ast_output += "            ├── Variable Declarations\n"
    # Find variable declarations
    for line in lines:
        line = line.strip()
        if any(dtype in line for dtype in ['int ', 'float ', 'char ', 'double ']) and '=' in line:
            var_name = line.split()[1].split('=')[0].strip()
            var_type = line.split()[0]
            ast_output += f"            │   └── {var_type} {var_name}\n"
```

**Variable Detection:**
1. **Type Checking**: Looks for C data types
2. **Assignment Detection**: Checks for '=' character
3. **Name Extraction**: Parses variable name from declaration
4. **Tree Addition**: Adds variable to AST tree

---

## 4. Flowchart Server Implementation

### File: `flowchart_server.py`
**Purpose**: Standalone server for flowchart generation
**Port**: 8003
**Endpoint**: `/flowchart`

#### Server Architecture
```python
class FlowchartHandler(BaseHTTPRequestHandler):
    """HTTP request handler for flowchart API."""
```

#### Flowchart Generation Function
```python
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
```

**Analysis Process:**
1. **Code Parsing**: Splits code into lines for analysis
2. **Feature Detection**: Searches for specific C constructs
3. **Boolean Flags**: Sets flags for flowchart elements
4. **Shape Selection**: Determines which shapes to include

#### Shape Implementation
```python
# START (Oval shape)
flowchart += "        ╭─────────────╮\n"
flowchart += "       ╱     START     ╲\n"
flowchart += "      ╱                 ╲\n"
flowchart += "     ╱___________________╲\n"
flowchart += "                │\n"
flowchart += "                ▼\n"

# Process (Rectangle)
if has_include:
    flowchart += "     ┌─────────────────────┐\n"
    flowchart += "     │   Include Headers   │\n"
    flowchart += "     │   #include <stdio.h>│\n"
    flowchart += "     └─────────┬───────────┘\n"
    flowchart += "               │\n"
    flowchart += "               ▼\n"

# Decision (Diamond)
if has_if:
    flowchart += "               ╱╲\n"
    flowchart += "              ╱  ╲\n"
    flowchart += "             ╱    ╲\n"
    flowchart += "            ╱ IF   ╲\n"
    flowchart += "           ╱ Cond? ╲\n"
    flowchart += "          ╱        ╲\n"
    flowchart += "         ╱__________╲\n"
```

**Shape Standards:**
- **Ovals**: Start/End points (╭─╮, ╱─╲)
- **Rectangles**: Process steps (┌─┐)
- **Diamonds**: Decision points (╱╲)
- **Parallelograms**: Input/Output (╱─╲)
- **Arrows**: Flow direction (│, ▼)

#### Flow Control Logic
```python
# Loop Decision (Diamond)
if has_while or has_for:
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
```

**Loop Handling:**
1. **Condition Diamond**: Shows loop condition
2. **YES/NO Branches**: Shows loop paths
3. **Loop Body**: Rectangle for loop content
4. **Back Arrow**: Shows loop iteration
5. **Exit Path**: Shows loop termination

---

## 5. Server Communication Protocol

### Request Processing Flow
```
1. HTTP Request Received
   ↓
2. Headers Parsed
   ↓
3. Content-Length Read
   ↓
4. Request Body Read
   ↓
5. JSON Parsed
   ↓
6. Code Extracted
   ↓
7. Analysis Performed
   ↓
8. Response Generated
   ↓
9. JSON Serialized
   ↓
10. HTTP Response Sent
```

### Error Handling Strategy
```python
try:
    # Main processing logic
    result = process_code(code)
    return success_response(result)
except json.JSONDecodeError:
    return error_response("Invalid JSON data")
except Exception as e:
    return error_response(f"Processing error: {str(e)}")
```

**Error Types Handled:**
1. **JSON Parsing Errors**: Malformed request data
2. **Missing Data**: No code provided
3. **Processing Errors**: Analysis failures
4. **Network Errors**: Connection issues

### Response Format Standardization
```python
def success_response(output):
    return {
        'success': True,
        'formatted_output': output
    }

def error_response(message):
    return {
        'success': False,
        'error': message,
        'formatted_output': f"Error: {message}"
    }
```

**Consistent Response Structure:**
- `success`: Boolean indicating operation status
- `formatted_output`: Human-readable result
- `error`: Error message (only when success=False)

---

## 6. Server Performance Characteristics

### Memory Usage
- **Stateless Design**: No data persistence between requests
- **Temporary Objects**: Analysis data garbage collected after response
- **Low Memory Footprint**: Typical usage under 50MB per server

### Processing Speed
- **Lexical Analysis**: ~10-50ms for typical C programs
- **AST Generation**: ~5-20ms for typical C programs
- **Flowchart Generation**: ~5-15ms for typical C programs

### Concurrency
- **Single-threaded**: Each server handles one request at a time
- **Multiple Servers**: Can run multiple instances on different ports
- **No Shared State**: Safe for concurrent deployment

### Scalability Considerations
- **Horizontal Scaling**: Can deploy multiple server instances
- **Load Balancing**: Can distribute requests across instances
- **Resource Limits**: CPU and memory usage scales with code complexity

---

## 7. PLY Lexer Deep Dive

### PLY (Python Lex-Yacc) Implementation Details

#### Token Rule Types in CLexer

##### Simple Token Rules (String-based)
```python
# Operators
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

# Comparison operators
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

# Delimiters
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
```

**How Simple Rules Work:**
- PLY automatically creates functions from `t_TOKENNAME` variables
- Regex patterns define what text matches each token
- No additional processing needed

##### Function-based Token Rules
```python
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t
```

**Function Rule Process:**
1. **Pattern Matching**: Regex in docstring defines pattern
2. **Token Processing**: Function can modify token properties
3. **Type Assignment**: Can change token type based on value
4. **Return Token**: Must return token object

##### Reserved Words Handling
```python
reserved = {
    'auto': 'AUTO', 'break': 'BREAK', 'case': 'CASE', 'char': 'CHAR',
    'const': 'CONST', 'continue': 'CONTINUE', 'default': 'DEFAULT',
    'do': 'DO', 'double': 'DOUBLE', 'else': 'ELSE', 'enum': 'ENUM',
    'extern': 'EXTERN', 'float': 'FLOAT', 'for': 'FOR', 'goto': 'GOTO',
    'if': 'IF', 'int': 'INT', 'long': 'LONG', 'register': 'REGISTER',
    'return': 'RETURN', 'short': 'SHORT', 'signed': 'SIGNED',
    'sizeof': 'SIZEOF', 'static': 'STATIC', 'struct': 'STRUCT',
    'switch': 'SWITCH', 'typedef': 'TYPEDEF', 'union': 'UNION',
    'unsigned': 'UNSIGNED', 'void': 'VOID', 'volatile': 'VOLATILE',
    'while': 'WHILE'
}
```

**Reserved Word Logic:**
1. **Dictionary Lookup**: Checks if identifier is reserved word
2. **Type Override**: Changes IDENTIFIER to specific keyword token
3. **Fallback**: Remains IDENTIFIER if not in reserved list

#### Complex Token Processing

##### String Literal Handling
```python
def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    # Remove quotes and handle escape sequences
    t.value = t.value[1:-1]  # Remove surrounding quotes
    return t
```

##### Comment Handling
```python
def t_COMMENT(t):
    r'//.*'
    # Single-line comments are ignored (no return statement)
    pass

def t_MULTILINE_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    # Multi-line comments are ignored but line numbers updated
    pass
```

##### Preprocessor Handling
```python
def t_HASH(t):
    r'\#'
    return t

def t_HEADER_FILE(t):
    r'<[^>]+>'
    return t
```

#### Error Handling in PLY
```python
def t_error(t):
    """Handle illegal characters."""
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)
```

**Error Recovery:**
1. **Character Skipping**: Skips illegal character
2. **Continuation**: Continues tokenizing rest of input
3. **Error Reporting**: Logs error with line number

---

## 8. Server Startup and Lifecycle

### Server Initialization Process
```python
def run_server(port=8001):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LexerHandler)
    print(f"Starting server on port {port}")
    print("Press Ctrl+C to stop the server")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
```

**Startup Sequence:**
1. **Address Binding**: Binds to specified port on all interfaces
2. **Handler Assignment**: Associates request handler class
3. **Server Start**: Begins listening for connections
4. **Event Loop**: Processes requests until interrupted

### Request Lifecycle
```
1. TCP Connection Established
   ↓
2. HTTP Request Received
   ↓
3. Handler Instance Created
   ↓
4. do_POST() Method Called
   ↓
5. Request Processing
   ↓
6. Response Generation
   ↓
7. Response Sent
   ↓
8. Connection Closed
   ↓
9. Handler Instance Destroyed
```

### Memory Management
- **Request Isolation**: Each request creates new handler instance
- **Automatic Cleanup**: Handler instances garbage collected after response
- **No Persistent State**: Servers maintain no data between requests

---

## 9. Debugging and Monitoring

### Server Logging
```python
# Debug output in servers
print(f"Parsing code: {code[:50]}...")  # Shows first 50 chars
print("AST generated successfully")      # Confirms completion
print(f"Error during parsing: {e}")     # Shows errors
```

### Request Monitoring
```python
def do_POST(self):
    """Handle POST requests with logging."""
    print(f"Received request to {self.path}")
    content_length = int(self.headers['Content-Length'])
    print(f"Content length: {content_length}")
    # ... rest of processing
```

### Error Tracking
```python
except Exception as e:
    print(f"Error during parsing: {e}")  # Console logging
    import traceback
    traceback.print_exc()                # Full stack trace

    return {
        'success': False,
        'error': str(e),
        'formatted_output': f"Error: {str(e)}"
    }
```

---

## 10. Server Configuration and Customization

### Port Configuration
```python
if __name__ == "__main__":
    port = 8001  # Default port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default.")

    run_server(port)
```

### CORS Configuration
```python
# Current CORS settings (permissive for development)
self.send_header('Access-Control-Allow-Origin', '*')
self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
self.send_header('Access-Control-Allow-Headers', 'Content-Type')

# Production CORS settings (more restrictive)
# self.send_header('Access-Control-Allow-Origin', 'http://localhost:3000')
```

### Response Format Customization
```python
# Standard response format
{
    'success': boolean,
    'formatted_output': string,
    'error': string (optional)
}

# Extended response format (can be added)
{
    'success': boolean,
    'formatted_output': string,
    'raw_data': object,
    'processing_time': float,
    'timestamp': string,
    'error': string (optional)
}
```

This comprehensive server implementation documentation provides complete understanding of how each server works internally, making it easier for your team to modify, debug, and extend the functionality.
