# C Code Analyzer

A web-based C code analyzer with lexical analysis and AST generation.

## Quick Start

1. **Start the lexer server:**
   ```bash
   cd lexer
   python web_interface.py 8001
   ```

2. **Start the AST server:**
   ```bash
   python ast_server.py 8005
   ```

3. **Start the flowchart server:**
   ```bash
   python flowchart_server.py 8003
   ```

   **Note**: For Windows PowerShell, use semicolons instead of &&:
   ```powershell
   cd lexer; python web_interface.py 8001
   python ast_server.py 8005
   python flowchart_server.py 8003
   ```

4. **Open the frontend:**
   Open `frontend/index.html` in your web browser

5. **Analyze C code:**
   - Enter your C code in the textarea
   - Select analysis type (Lexical Analysis, AST, or Flowchart)
   - Click "Analyze Code"
   - View detailed results

## Project Structure

```
C-Code-Analyzer/
├── frontend/
│   ├── index.html          # Main web interface
│   ├── script.js           # Frontend logic
│   └── style.css           # Styling
├── lexer/
│   ├── c_lexer.py          # PLY-based C lexer
│   ├── web_interface.py    # Lexer HTTP API server
│   └── __init__.py         # Package file
├── parser/
│   ├── ast_nodes.py        # AST node definitions
│   ├── c_parser.py         # C language parser
│   ├── ast_formatter.py    # AST formatting utilities
│   ├── web_interface.py    # Parser HTTP API server
│   └── __init__.py         # Package file
├── flowchart/
│   ├── cfg_nodes.py        # Control flow graph nodes
│   ├── cfg_generator.py    # CFG generation logic
│   ├── graphviz_renderer.py # Graphviz visualization
│   ├── web_interface.py    # Flowchart HTTP API server
│   └── __init__.py         # Package file
├── flowchart_server.py     # Standalone flowchart server
└── README.md               # This file
```

## Requirements

- Python 3.6+
- PLY library: `pip install ply`

## Features

- **Lexical Analysis**: Complete C language tokenization
- **AST Generation**: Abstract Syntax Tree creation and visualization
- **Flowchart Generation**: Control flow graph visualization
- **Token identification**: Keywords, operators, literals, etc.
- **Tree structure**: Hierarchical code representation
- **Visual flowcharts**: Text-based control flow diagrams
- **Clean web interface**: Easy-to-use frontend
- **Real-time analysis**: Instant results

## API Endpoints

- **Lexer**: `http://localhost:8001/analyze`
- **AST Parser**: `http://localhost:8005/parse`
- **Flowchart**: `http://localhost:8003/flowchart`

Simple and functional!
