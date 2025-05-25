# Data Flow Documentation
## C Code Analyzer Project

### Overview
This document describes the complete data flow in the C Code Analyzer system, from user input to final output display.

---

## 1. High-Level Data Flow

```
User Input (C Code) 
    ↓
Frontend (HTML/CSS/JS)
    ↓
HTTP API Calls (JSON)
    ↓
Backend Servers (Python)
    ↓
Processing Engines
    ↓
Formatted Output
    ↓
Frontend Display
```

---

## 2. Detailed Data Flow by Analysis Type

### 2.1 Lexical Analysis Flow

```
1. User enters C code in textarea
   ↓
2. Frontend JavaScript (script.js)
   - Function: generateLexicalAnalysis()
   - Sends POST request to http://localhost:8001/analyze
   ↓
3. Lexer Server (lexer/web_interface.py)
   - Receives JSON: {"code": "C source code"}
   - Calls analyze_code() method
   ↓
4. C Lexer Engine (lexer/c_lexer.py)
   - CLexer class processes the code
   - tokenize() method breaks code into tokens
   - get_formatted_output() creates readable output
   ↓
5. Token Processing
   - Each token has: type, value, line, position
   - Tokens categorized: keywords, operators, literals, etc.
   ↓
6. Response Generation
   - JSON response: {"success": true, "formatted_output": "..."}
   ↓
7. Frontend Display
   - JavaScript receives response
   - Updates outputDisplay element with formatted text
```

### 2.2 AST Generation Flow

```
1. User selects "AST" and clicks "Analyze Code"
   ↓
2. Frontend JavaScript (script.js)
   - Function: generateAST()
   - Sends POST request to http://localhost:8005/parse
   ↓
3. AST Server (ast_server.py)
   - Receives JSON: {"code": "C source code"}
   - Calls parse_code() method
   ↓
4. AST Processing Engine
   - simple_ast_analysis() function
   - Analyzes code structure patterns
   - Identifies: includes, functions, variables, conditionals
   ↓
5. Tree Structure Generation
   - Creates hierarchical tree representation
   - Uses Unicode characters for tree visualization
   - Generates analysis summary with checkmarks
   ↓
6. Response Generation
   - JSON response: {"success": true, "formatted_output": "tree structure"}
   ↓
7. Frontend Display
   - JavaScript receives AST tree
   - Displays formatted tree structure
```

### 2.3 Flowchart Generation Flow

```
1. User selects "Flowchart" and clicks "Analyze Code"
   ↓
2. Frontend JavaScript (script.js)
   - Function: generateFlowchart()
   - Sends POST request to http://localhost:8003/flowchart
   ↓
3. Flowchart Server (flowchart_server.py)
   - Receives JSON: {"code": "C source code"}
   - Calls generate_flowchart() method
   ↓
4. Flowchart Processing Engine
   - generate_simple_flowchart() function
   - Analyzes code for control structures
   - Identifies: includes, main, variables, conditionals, loops, I/O
   ↓
5. Visual Flowchart Generation
   - Creates flowchart with proper shapes:
     * Ovals for START/END
     * Diamonds for decisions
     * Parallelograms for I/O
     * Rectangles for processes
   - Adds arrows for flow direction
   ↓
6. Response Generation
   - JSON response: {"success": true, "formatted_output": "flowchart"}
   ↓
7. Frontend Display
   - JavaScript receives flowchart
   - Displays visual flowchart with legend
```

---

## 3. Data Transformation Stages

### Stage 1: Input Processing
- **Input**: Raw C source code (string)
- **Processing**: Validation, encoding, JSON wrapping
- **Output**: HTTP POST request with JSON payload

### Stage 2: Server Reception
- **Input**: HTTP request with JSON data
- **Processing**: Request parsing, data extraction
- **Output**: C code string for analysis

### Stage 3: Analysis Processing
- **Input**: C source code string
- **Processing**: 
  - Lexical: Tokenization using PLY patterns
  - AST: Pattern matching and tree building
  - Flowchart: Control flow analysis
- **Output**: Structured analysis data

### Stage 4: Formatting
- **Input**: Raw analysis data
- **Processing**: Text formatting, tree generation, visual layout
- **Output**: Human-readable formatted strings

### Stage 5: Response Generation
- **Input**: Formatted analysis results
- **Processing**: JSON serialization, HTTP response creation
- **Output**: HTTP response with JSON payload

### Stage 6: Frontend Display
- **Input**: JSON response from server
- **Processing**: JSON parsing, DOM manipulation
- **Output**: Visual display in browser

---

## 4. Error Handling Flow

```
Error Occurs
    ↓
Server Catches Exception
    ↓
Error Response Generated
    {"success": false, "error": "message", "formatted_output": "error details"}
    ↓
Frontend Receives Error
    ↓
Error Message Displayed to User
```

---

## 5. Data Persistence

- **No Database**: System is stateless
- **Session Data**: Only in browser memory during analysis
- **Server State**: Servers maintain no persistent data
- **File System**: Only source code files, no data storage

---

## 6. Performance Considerations

- **Concurrent Requests**: Each server handles multiple requests
- **Memory Usage**: Analysis data is temporary and garbage collected
- **Network Traffic**: JSON payloads are lightweight
- **Processing Time**: Real-time analysis for typical C programs

---

## 7. Security Data Flow

- **Input Validation**: Servers validate JSON structure
- **Code Execution**: No code execution, only analysis
- **CORS Headers**: Enabled for cross-origin requests
- **Error Exposure**: Minimal error information exposed to client
