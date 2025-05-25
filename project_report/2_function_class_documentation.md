# Function and Class Documentation
## C Code Analyzer Project

### Overview
This document provides detailed documentation of all functions and classes used in the project, their flow, descriptions, and outputs.

---

## 1. Frontend Components (frontend/script.js)

### 1.1 Main Event Handlers

#### `analyzeBtn.addEventListener('click', async function())`
- **Purpose**: Handles the "Analyze Code" button click
- **Input**: User click event
- **Process**: 
  1. Gets code from textarea
  2. Validates input (checks if code is not empty)
  3. Calls generateOutput() with selected analysis type
- **Output**: Triggers analysis process
- **Error Handling**: Shows alert if no code provided

#### `outputType.addEventListener('change', async function())`
- **Purpose**: Handles analysis type dropdown change
- **Input**: Change event from select element
- **Process**: 
  1. Gets current code from textarea
  2. If code exists, calls generateOutput() with new type
- **Output**: Re-analyzes code with new analysis type

### 1.2 Core Analysis Functions

#### `async function generateOutput(code, type)`
- **Purpose**: Main orchestrator for all analysis types
- **Input**: 
  - `code` (string): C source code
  - `type` (string): 'lexical', 'ast', or 'flowchart'
- **Process**:
  1. Shows "Analyzing code..." message
  2. Calls appropriate analysis function based on type
  3. Handles errors with try-catch
  4. Updates DOM with results
- **Output**: Updates outputDisplay element
- **Error Handling**: Displays error messages in output area

#### `async function generateLexicalAnalysis(code)`
- **Purpose**: Performs lexical analysis via API call
- **Input**: `code` (string): C source code
- **Process**:
  1. Creates POST request to http://localhost:8001/analyze
  2. Sends JSON payload: `{"code": code}`
  3. Waits for response
  4. Extracts formatted_output from response
- **Output**: Returns formatted lexical analysis string
- **Error Handling**: Returns connection error message if server unavailable

#### `async function generateAST(code)`
- **Purpose**: Performs AST generation via API call
- **Input**: `code` (string): C source code
- **Process**:
  1. Creates POST request to http://localhost:8005/parse
  2. Sends JSON payload: `{"code": code}`
  3. Waits for response
  4. Extracts formatted_output from response
- **Output**: Returns formatted AST tree string
- **Error Handling**: Returns connection error message if server unavailable

#### `async function generateFlowchart(code)`
- **Purpose**: Performs flowchart generation via API call
- **Input**: `code` (string): C source code
- **Process**:
  1. Creates POST request to http://localhost:8003/flowchart
  2. Sends JSON payload: `{"code": code}`
  3. Waits for response
  4. Extracts formatted_output from response
- **Output**: Returns formatted flowchart string
- **Error Handling**: Returns connection error message if server unavailable

---

## 2. Lexer Components (lexer/)

### 2.1 CLexer Class (lexer/c_lexer.py)

#### `class CLexer`
- **Purpose**: Main lexical analyzer for C language
- **Inheritance**: None
- **Dependencies**: PLY (Python Lex-Yacc)

#### `__init__(self)`
- **Purpose**: Initialize lexer instance
- **Process**:
  1. Sets up token list and counters
  2. Calls build() to create lexer
- **Output**: Ready-to-use lexer instance

#### `tokenize(self, code)`
- **Purpose**: Convert C code into tokens
- **Input**: `code` (string): C source code
- **Process**:
  1. Feeds code to PLY lexer
  2. Iterates through tokens
  3. Creates token dictionaries with type, value, line, position
- **Output**: List of token dictionaries
- **Example Output**:
```python
[
    {'type': 'INT', 'value': 'int', 'line': 1, 'position': 0},
    {'type': 'IDENTIFIER', 'value': 'main', 'line': 1, 'position': 4}
]
```

#### `get_formatted_output(self, code)`
- **Purpose**: Generate human-readable lexical analysis
- **Input**: `code` (string): C source code
- **Process**:
  1. Calls tokenize() to get tokens
  2. Counts tokens by type
  3. Formats output with summary and detailed list
- **Output**: Formatted string with token analysis
- **Usage**: Called by web interface for display

### 2.2 Web Interface (lexer/web_interface.py)

#### `class LexerHandler(BaseHTTPRequestHandler)`
- **Purpose**: HTTP request handler for lexer API

#### `do_POST(self)`
- **Purpose**: Handle POST requests to /analyze endpoint
- **Input**: HTTP POST request with JSON body
- **Process**:
  1. Reads request body
  2. Parses JSON to extract code
  3. Calls analyze_code()
  4. Sends JSON response
- **Output**: HTTP response with analysis results

#### `analyze_code(self, code)`
- **Purpose**: Perform lexical analysis and format response
- **Input**: `code` (string): C source code
- **Process**:
  1. Creates CLexer instance
  2. Calls tokenize() and get_formatted_output()
  3. Builds response dictionary
- **Output**: Dictionary with success status and results

---

## 3. AST Components (ast_server.py)

### 3.1 AST Analysis Functions

#### `simple_ast_analysis(code)`
- **Purpose**: Generate AST-like analysis of C code
- **Input**: `code` (string): C source code
- **Process**:
  1. Splits code into lines
  2. Analyzes patterns for language constructs
  3. Builds hierarchical tree representation
  4. Generates analysis summary
- **Output**: Formatted AST tree string
- **Pattern Detection**:
  - `#include` for preprocessor directives
  - `main` for function detection
  - Data types for variable declarations
  - `if` for conditionals
  - `printf` for function calls
  - `return` for return statements

### 3.2 Web Interface

#### `class ASTHandler(BaseHTTPRequestHandler)`
- **Purpose**: HTTP request handler for AST API

#### `parse_code(self, code)`
- **Purpose**: Parse C code and return AST results
- **Input**: `code` (string): C source code
- **Process**:
  1. Calls simple_ast_analysis()
  2. Handles exceptions
  3. Builds response dictionary
- **Output**: Dictionary with success status and AST tree

---

## 4. Flowchart Components (flowchart_server.py)

### 4.1 Flowchart Generation

#### `generate_simple_flowchart(self, code)`
- **Purpose**: Generate visual flowchart representation
- **Input**: `code` (string): C source code
- **Process**:
  1. Analyzes code for control structures
  2. Builds flowchart with proper shapes
  3. Adds legend and analysis summary
- **Output**: Formatted flowchart string with Unicode graphics
- **Shape Mapping**:
  - Ovals (╭─╮) for START/END
  - Diamonds (╱╲) for decisions
  - Parallelograms (╱─╲) for I/O
  - Rectangles (┌─┐) for processes

### 4.2 Web Interface

#### `class FlowchartHandler(BaseHTTPRequestHandler)`
- **Purpose**: HTTP request handler for flowchart API

#### `generate_flowchart(self, code)`
- **Purpose**: Generate flowchart and format response
- **Input**: `code` (string): C source code
- **Process**:
  1. Calls generate_simple_flowchart()
  2. Handles exceptions
  3. Builds response dictionary
- **Output**: Dictionary with success status and flowchart

---

## 5. Data Flow Through Functions

### Lexical Analysis Flow:
```
User Input → generateLexicalAnalysis() → HTTP POST → LexerHandler.do_POST() 
→ analyze_code() → CLexer.tokenize() → CLexer.get_formatted_output() 
→ JSON Response → Frontend Display
```

### AST Analysis Flow:
```
User Input → generateAST() → HTTP POST → ASTHandler.do_POST() 
→ parse_code() → simple_ast_analysis() → JSON Response → Frontend Display
```

### Flowchart Analysis Flow:
```
User Input → generateFlowchart() → HTTP POST → FlowchartHandler.do_POST() 
→ generate_flowchart() → generate_simple_flowchart() → JSON Response → Frontend Display
```

---

## 6. Error Handling in Functions

### Frontend Error Handling:
- Network errors caught in try-catch blocks
- Connection failures show user-friendly messages
- Invalid responses handled gracefully

### Backend Error Handling:
- All server functions wrapped in try-catch
- Exceptions logged to console
- Error responses sent to client with details

### Common Error Scenarios:
1. **Server Unavailable**: Connection refused errors
2. **Invalid JSON**: Malformed request data
3. **Empty Code**: No input provided
4. **Processing Errors**: Analysis failures
