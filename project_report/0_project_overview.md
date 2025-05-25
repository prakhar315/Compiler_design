# Project Overview
## C Code Analyzer - Complete Documentation

### Project Summary
The C Code Analyzer is a web-based application that provides comprehensive analysis of C programming language source code. It offers three types of analysis: lexical analysis (tokenization), Abstract Syntax Tree (AST) generation, and flowchart visualization.

---

## 1. Project Architecture

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Lexer Server  │    │   AST Server    │
│   (HTML/CSS/JS) │◄──►│   Port 8001     │    │   Port 8005     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ Flowchart Server│
│   Port 8003     │
│                 │
└─────────────────┘
```

### Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.6+
- **Lexer Engine**: PLY (Python Lex-Yacc)
- **Web Servers**: Python HTTP Server
- **Communication**: REST APIs with JSON

---

## 2. File Structure
```
C-Code-Analyzer/
├── frontend/
│   ├── index.html              # Main web interface
│   ├── script.js               # Frontend logic and API calls
│   └── style.css               # Styling and layout
├── lexer/
│   ├── c_lexer.py              # PLY-based C language lexer
│   ├── web_interface.py        # HTTP server for lexer API
│   └── __init__.py             # Package initialization
├── parser/                     # (Legacy - not used in current version)
│   ├── ast_nodes.py            # AST node definitions
│   ├── c_parser.py             # C language parser
│   ├── ast_formatter.py        # AST formatting utilities
│   ├── web_interface.py        # Parser HTTP server
│   └── __init__.py             # Package initialization
├── flowchart/                  # (Legacy - not used in current version)
│   ├── cfg_nodes.py            # Control flow graph nodes
│   ├── cfg_generator.py        # CFG generation logic
│   ├── graphviz_renderer.py    # Graphviz visualization
│   ├── web_interface.py        # Flowchart HTTP server
│   └── __init__.py             # Package initialization
├── ast_server.py               # Standalone AST analysis server
├── flowchart_server.py         # Standalone flowchart generation server
├── project_report/             # Complete project documentation
│   ├── 0_project_overview.md   # This file
│   ├── 1_dataflow_documentation.md
│   ├── 2_function_class_documentation.md
│   ├── 3_api_documentation.md
│   ├── 4_ui_dataflow_documentation.md
│   ├── 5_quick_reference_guide.md
│   ├── 6_server_implementation_documentation.md
│   └── 7_frontend_implementation_documentation.md
└── README.md                   # Quick start guide
```

---

## 3. Core Features

### 3.1 Lexical Analysis
- **Purpose**: Tokenizes C source code into meaningful components
- **Technology**: PLY (Python Lex-Yacc) library
- **Output**: Detailed token breakdown with types, values, line numbers
- **Supported Tokens**: Keywords, identifiers, operators, literals, delimiters, comments

### 3.2 Abstract Syntax Tree (AST)
- **Purpose**: Analyzes program structure and generates hierarchical representation
- **Technology**: Custom pattern-matching analysis
- **Output**: Tree structure showing program hierarchy
- **Detected Elements**: Functions, variables, conditionals, loops, I/O operations

### 3.3 Flowchart Generation
- **Purpose**: Creates visual representation of program control flow
- **Technology**: Unicode-based flowchart drawing
- **Output**: Visual flowchart with proper shapes and flow arrows
- **Shapes Used**: Ovals (start/end), diamonds (decisions), rectangles (processes), parallelograms (I/O)

---

## 4. Server Configuration

### Active Servers
1. **Lexer Server** (Port 8001)
   - File: `lexer/web_interface.py`
   - Endpoint: `/analyze`
   - Purpose: Tokenization and lexical analysis

2. **AST Server** (Port 8005)
   - File: `ast_server.py`
   - Endpoint: `/parse`
   - Purpose: Abstract syntax tree generation

3. **Flowchart Server** (Port 8003)
   - File: `flowchart_server.py`
   - Endpoint: `/flowchart`
   - Purpose: Control flow visualization

### Server Dependencies
- **Python 3.6+**: Required for all servers
- **PLY Library**: Required for lexer server (`pip install ply`)
- **No Database**: All servers are stateless

---

## 5. Quick Start Guide

### Prerequisites
```bash
# Install Python 3.6 or higher
# Install PLY library
pip install ply
```

### Starting the System
```bash
# Terminal 1: Start lexer server
cd lexer
python web_interface.py 8001

# Terminal 2: Start AST server
python ast_server.py 8005

# Terminal 3: Start flowchart server
python flowchart_server.py 8003

# Open frontend/index.html in web browser
```

### Using the Application
1. Open `frontend/index.html` in a web browser
2. Enter C source code in the textarea
3. Select analysis type from dropdown
4. Click "Analyze Code" button
5. View results in the output area

---

## 6. Documentation Structure

This project report contains seven detailed documentation files:

### 1. Data Flow Documentation (`1_dataflow_documentation.md`)
- Complete system data flow from input to output
- Data transformation stages
- Error handling flow
- Performance and security considerations

### 2. Function and Class Documentation (`2_function_class_documentation.md`)
- Detailed documentation of all functions and classes
- Input/output specifications for each function
- Function call chains and dependencies
- Error handling in each component

### 3. API Documentation (`3_api_documentation.md`)
- Complete REST API reference for all three services
- Request/response formats and examples
- Error codes and handling
- Integration examples and testing procedures

### 4. UI Data Flow Documentation (`4_ui_dataflow_documentation.md`)
- Complete user interface interaction flow
- DOM manipulation and event handling
- Frontend-backend communication details
- User experience and error handling

### 5. Quick Reference Guide (`5_quick_reference_guide.md`)
- Essential commands for daily development
- Key files and their purposes summary
- API endpoints quick reference table
- Common code patterns and debugging checklist

### 6. Server Implementation Documentation (`6_server_implementation_documentation.md`)
- Detailed server code explanations
- PLY lexer implementation deep dive
- Server architecture and request lifecycle
- Error handling and debugging strategies

### 7. Frontend Implementation Documentation (`7_frontend_implementation_documentation.md`)
- Complete HTML, CSS, and JavaScript analysis
- Frontend architecture patterns
- User experience design principles
- Performance and accessibility features

---

## 7. Development Guidelines

### Code Organization
- **Separation of Concerns**: Frontend, lexer, AST, and flowchart are separate modules
- **Stateless Design**: No persistent data storage
- **API-First**: All functionality exposed through REST APIs
- **Error Handling**: Comprehensive error handling at all levels

### Adding New Features
1. **Backend**: Add new analysis logic to appropriate server
2. **API**: Expose functionality through REST endpoint
3. **Frontend**: Add UI controls and API integration
4. **Documentation**: Update relevant documentation files

### Testing Strategy
- **Unit Testing**: Test individual functions and classes
- **Integration Testing**: Test API endpoints with sample data
- **UI Testing**: Test frontend functionality in browsers
- **End-to-End Testing**: Test complete user workflows

---

## 8. Troubleshooting

### Common Issues
1. **Server Not Starting**: Check Python installation and dependencies
2. **Port Conflicts**: Ensure ports 8001, 8003, 8005 are available
3. **CORS Errors**: Servers include CORS headers for cross-origin requests
4. **Import Errors**: Ensure all Python files are in correct directories

### Debug Mode
- All servers include console logging for debugging
- Error messages are detailed and user-friendly
- Network requests can be monitored in browser developer tools

---

## 9. Future Enhancements

### Planned Features
- **Syntax Error Detection**: Highlight syntax errors in code
- **Code Formatting**: Automatic code beautification
- **Export Functionality**: Save analysis results to files
- **Multiple Language Support**: Support for other programming languages

### Scalability Considerations
- **Database Integration**: For storing analysis history
- **User Authentication**: For personalized experiences
- **Load Balancing**: For handling multiple concurrent users
- **Caching**: For improved performance

---

## 10. Team Collaboration

### Working with the Codebase
1. **Read Documentation**: Start with this overview and relevant detailed docs
2. **Understand Data Flow**: Review data flow documentation before making changes
3. **Test Changes**: Use API documentation to test modifications
4. **Update Documentation**: Keep documentation current with code changes

### Best Practices
- **Follow Existing Patterns**: Maintain consistency with current code structure
- **Test Thoroughly**: Verify changes work with all three analysis types
- **Document Changes**: Update relevant documentation files
- **Use Version Control**: Commit changes with descriptive messages

This documentation provides a complete reference for understanding and working with the C Code Analyzer project. Each team member should familiarize themselves with the relevant sections based on their role and responsibilities.
