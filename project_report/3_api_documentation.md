# API Documentation
## C Code Analyzer Project

### Overview
This document provides comprehensive API documentation for all three analysis services in the C Code Analyzer system.

---

## 1. API Architecture

### Base URLs
- **Lexer Service**: `http://localhost:8001`
- **AST Service**: `http://localhost:8005`
- **Flowchart Service**: `http://localhost:8003`

### Common Headers
```http
Content-Type: application/json
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### Common Request Format
All APIs accept POST requests with JSON payload:
```json
{
    "code": "C source code as string"
}
```

### Common Response Format
All APIs return JSON responses:
```json
{
    "success": boolean,
    "formatted_output": "string",
    "error": "string (only if success=false)"
}
```

---

## 2. Lexical Analysis API

### Endpoint: `/analyze`
**URL**: `http://localhost:8001/analyze`
**Method**: `POST`
**Content-Type**: `application/json`

#### Request Body
```json
{
    "code": "int main() { return 0; }"
}
```

#### Success Response (200 OK)
```json
{
    "success": true,
    "tokens": [
        {
            "type": "INT",
            "value": "int",
            "line": 1,
            "position": 0
        },
        {
            "type": "IDENTIFIER", 
            "value": "main",
            "line": 1,
            "position": 4
        }
    ],
    "formatted_output": "Lexical Analysis Results:\n==================================================\n\nToken Summary:\n--------------------\nINT: 1\nIDENTIFIER: 1\n...",
    "token_count": 8
}
```

#### Error Response (200 OK with error)
```json
{
    "success": false,
    "error": "No code provided",
    "formatted_output": "Error: No code provided"
}
```

#### Token Types Recognized
- **Keywords**: `INT`, `FLOAT`, `IF`, `WHILE`, `RETURN`, etc.
- **Identifiers**: `IDENTIFIER`
- **Literals**: `INTEGER_LITERAL`, `STRING_LITERAL`, `CHAR_LITERAL`
- **Operators**: `PLUS`, `MINUS`, `ASSIGN`, `EQ`, `LT`, etc.
- **Delimiters**: `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`, `SEMICOLON`
- **Comments**: `COMMENT`, `MULTILINE_COMMENT`
- **Preprocessor**: `HASH`, `INCLUDE`, `HEADER_FILE`

#### Example cURL Request
```bash
curl -X POST http://localhost:8001/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "int main() { return 0; }"}'
```

---

## 3. AST Generation API

### Endpoint: `/parse`
**URL**: `http://localhost:8005/parse`
**Method**: `POST`
**Content-Type**: `application/json`

#### Request Body
```json
{
    "code": "#include <stdio.h>\nint main() {\n    int x = 5;\n    return x;\n}"
}
```

#### Success Response (200 OK)
```json
{
    "success": true,
    "formatted_output": "Abstract Syntax Tree (AST):\n========================================\n\n└── Program\n    ├── Preprocessor Directive\n    │   └── #include <stdio.h>\n    └── Function Declaration\n        ├── Return Type: int\n        ├── Name: main\n        ├── Parameters: ()\n        └── Function Body\n            ├── Variable Declarations\n            │   └── int x\n            └── Return Statement\n                └── Value: x\n\nAST Analysis Summary:\n==============================\n• Program structure: ✓\n• Preprocessor directives: ✓\n• Variable declarations: ✓\n• Control structures: ✗\n• Function calls: ✗\n• Return statements: ✓"
}
```

#### Error Response (200 OK with error)
```json
{
    "success": false,
    "error": "Invalid JSON data",
    "formatted_output": "Error during AST generation: Invalid JSON data"
}
```

#### AST Node Types Detected
- **Program**: Root node
- **Preprocessor Directive**: `#include`, `#define`
- **Function Declaration**: Function definitions
- **Variable Declarations**: Variable definitions with types
- **Conditional Statement**: `if` statements
- **Function Call**: Function invocations
- **Return Statement**: Return statements with values

#### Example cURL Request
```bash
curl -X POST http://localhost:8005/parse \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <stdio.h>\nint main() { return 0; }"}'
```

---

## 4. Flowchart Generation API

### Endpoint: `/flowchart`
**URL**: `http://localhost:8003/flowchart`
**Method**: `POST`
**Content-Type**: `application/json`

#### Request Body
```json
{
    "code": "#include <stdio.h>\nint main() {\n    int x;\n    scanf(\"%d\", &x);\n    if (x > 0) {\n        printf(\"Positive\");\n    }\n    return 0;\n}"
}
```

#### Success Response (200 OK)
```json
{
    "success": true,
    "formatted_output": "Control Flow Graph:\n==================================================\n\n        ╭─────────────╮\n       ╱     START     ╲\n      ╱                 ╲\n     ╱___________________╲\n                │\n                ▼\n     ┌─────────────────────┐\n     │   Include Headers   │\n     │   #include <stdio.h>│\n     └─────────┬───────────┘\n               │\n               ▼\n     ┌─────────────────────┐\n     │   Function main()   │\n     │   Entry Point       │\n     └─────────┬───────────┘\n               │\n               ▼\n..."
}
```

#### Error Response (200 OK with error)
```json
{
    "success": false,
    "error": "No code provided",
    "formatted_output": "Error: No code provided"
}
```

#### Flowchart Elements Generated
- **START/END**: Oval shapes (╭─╮)
- **Process**: Rectangle shapes (┌─┐)
- **Decision**: Diamond shapes (╱╲)
- **Input/Output**: Parallelogram shapes (╱─╲)
- **Flow**: Arrows (│, ▼)

#### Detected Constructs
- Include statements
- Function definitions
- Variable declarations
- Input operations (`scanf`)
- Output operations (`printf`)
- Conditional statements (`if`)
- Loop statements (`while`, `for`)
- Return statements

#### Example cURL Request
```bash
curl -X POST http://localhost:8003/flowchart \
  -H "Content-Type: application/json" \
  -d '{"code": "#include <stdio.h>\nint main() { printf(\"Hello\"); return 0; }"}'
```

---

## 5. Error Codes and Handling

### HTTP Status Codes
- **200 OK**: Request processed (check `success` field for actual result)
- **404 Not Found**: Invalid endpoint
- **500 Internal Server Error**: Server error

### Error Types
1. **No Code Provided**: Empty or missing code field
2. **Invalid JSON**: Malformed request body
3. **Server Error**: Internal processing error
4. **Connection Error**: Server unavailable

### Error Response Structure
```json
{
    "success": false,
    "error": "Descriptive error message",
    "formatted_output": "User-friendly error description"
}
```

---

## 6. Rate Limiting and Performance

### Current Limitations
- **No Rate Limiting**: APIs accept unlimited requests
- **No Authentication**: Open access to all endpoints
- **Synchronous Processing**: Requests processed sequentially

### Performance Characteristics
- **Lexical Analysis**: ~10ms for typical programs
- **AST Generation**: ~5ms for typical programs  
- **Flowchart Generation**: ~5ms for typical programs
- **Memory Usage**: Minimal, no persistent storage

### Recommended Usage
- **Max Code Size**: 10KB per request
- **Concurrent Requests**: Up to 10 simultaneous
- **Timeout**: 30 seconds per request

---

## 7. Integration Examples

### JavaScript Fetch API
```javascript
async function analyzeCode(code, type) {
    const endpoints = {
        'lexical': 'http://localhost:8001/analyze',
        'ast': 'http://localhost:8005/parse', 
        'flowchart': 'http://localhost:8003/flowchart'
    };
    
    const response = await fetch(endpoints[type], {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    });
    
    return await response.json();
}
```

### Python Requests
```python
import requests

def analyze_code(code, analysis_type):
    endpoints = {
        'lexical': 'http://localhost:8001/analyze',
        'ast': 'http://localhost:8005/parse',
        'flowchart': 'http://localhost:8003/flowchart'
    }
    
    response = requests.post(
        endpoints[analysis_type],
        json={'code': code}
    )
    
    return response.json()
```

---

## 8. Testing the APIs

### Health Check
Test if servers are running:
```bash
curl http://localhost:8001/analyze -X POST -H "Content-Type: application/json" -d '{"code":"int x;"}'
curl http://localhost:8005/parse -X POST -H "Content-Type: application/json" -d '{"code":"int x;"}'
curl http://localhost:8003/flowchart -X POST -H "Content-Type: application/json" -d '{"code":"int x;"}'
```

### Sample Test Cases
1. **Simple Program**: `int main() { return 0; }`
2. **With Variables**: `int main() { int x = 5; return x; }`
3. **With Conditionals**: `int main() { if (1) return 0; }`
4. **With I/O**: `int main() { printf("Hello"); return 0; }`
