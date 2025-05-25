# Quick Reference Guide
## C Code Analyzer Project

### Overview
This is a quick reference for developers working on the C Code Analyzer project. For detailed information, refer to the specific documentation files.

---

## 1. Essential Commands

### Start All Servers
```bash
# Terminal 1: Lexer Server
cd lexer
python web_interface.py 8001

# Terminal 2: AST Server  
python ast_server.py 8005

# Terminal 3: Flowchart Server
python flowchart_server.py 8003
```

### Test Servers
```bash
# Test lexer
curl -X POST http://localhost:8001/analyze -H "Content-Type: application/json" -d '{"code":"int x;"}'

# Test AST
curl -X POST http://localhost:8005/parse -H "Content-Type: application/json" -d '{"code":"int x;"}'

# Test flowchart
curl -X POST http://localhost:8003/flowchart -H "Content-Type: application/json" -d '{"code":"int x;"}'
```

---

## 2. Key Files and Their Purpose

| File | Purpose | Port | Key Functions |
|------|---------|------|---------------|
| `frontend/index.html` | Main UI | - | User interface |
| `frontend/script.js` | Frontend logic | - | `generateOutput()`, `generateLexicalAnalysis()` |
| `lexer/web_interface.py` | Lexer API | 8001 | `analyze_code()` |
| `lexer/c_lexer.py` | Tokenization | - | `tokenize()`, `get_formatted_output()` |
| `ast_server.py` | AST API | 8005 | `simple_ast_analysis()` |
| `flowchart_server.py` | Flowchart API | 8003 | `generate_simple_flowchart()` |

---

## 3. API Endpoints Quick Reference

### Lexer API
- **URL**: `http://localhost:8001/analyze`
- **Method**: POST
- **Input**: `{"code": "C source code"}`
- **Output**: Token analysis with counts and details

### AST API
- **URL**: `http://localhost:8005/parse`
- **Method**: POST
- **Input**: `{"code": "C source code"}`
- **Output**: Hierarchical tree structure

### Flowchart API
- **URL**: `http://localhost:8003/flowchart`
- **Method**: POST
- **Input**: `{"code": "C source code"}`
- **Output**: Visual flowchart with shapes

---

## 4. Common Code Patterns

### Frontend API Call Pattern
```javascript
async function callAPI(endpoint, code) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });
        const data = await response.json();
        return data.success ? data.formatted_output : data.error;
    } catch (error) {
        return `Connection error: ${error.message}`;
    }
}
```

### Backend Response Pattern
```python
def generate_response(success, output, error=None):
    return {
        'success': success,
        'formatted_output': output,
        'error': error
    }
```

---

## 5. Debugging Checklist

### Server Issues
- [ ] Python 3.6+ installed
- [ ] PLY library installed (`pip install ply`)
- [ ] Ports 8001, 8003, 8005 available
- [ ] No firewall blocking ports
- [ ] Servers started in correct directories

### Frontend Issues
- [ ] All servers running
- [ ] Browser supports fetch API
- [ ] No CORS errors in console
- [ ] JavaScript enabled
- [ ] Network connectivity

### Common Error Messages
| Error | Cause | Solution |
|-------|-------|----------|
| "Could not connect to server" | Server not running | Start the appropriate server |
| "No code provided" | Empty input | Enter C code in textarea |
| "Invalid JSON" | Malformed request | Check API call format |
| "Port already in use" | Port conflict | Kill existing process or use different port |

---

## 6. File Modification Guidelines

### Adding New Analysis Features
1. **Backend**: Add logic to appropriate server file
2. **API**: Ensure endpoint returns standard JSON format
3. **Frontend**: Add UI controls and API integration
4. **Test**: Verify with sample C code

### Modifying Existing Features
1. **Identify**: Which server handles the feature
2. **Locate**: Find the relevant function
3. **Modify**: Make changes carefully
4. **Test**: Verify all analysis types still work

---

## 7. Testing Procedures

### Manual Testing
1. Start all three servers
2. Open `frontend/index.html`
3. Test each analysis type with sample code
4. Verify error handling with invalid input

### Sample Test Code
```c
#include <stdio.h>

int main() {
    int x = 5;
    if (x > 0) {
        printf("Positive");
    }
    return 0;
}
```

### Expected Outputs
- **Lexical**: Token list with counts
- **AST**: Tree structure with program hierarchy  
- **Flowchart**: Visual diagram with shapes

---

## 8. Performance Tips

### Frontend
- Use async/await for all API calls
- Show loading messages during processing
- Handle errors gracefully

### Backend
- Keep analysis functions lightweight
- Avoid storing state between requests
- Use efficient string processing

---

## 9. Documentation Files Reference

| File | Content | When to Read |
|------|---------|--------------|
| `0_project_overview.md` | Complete project overview | First time setup |
| `1_dataflow_documentation.md` | System data flow | Understanding architecture |
| `2_function_class_documentation.md` | Function details | Modifying specific functions |
| `3_api_documentation.md` | API reference | API integration work |
| `4_ui_dataflow_documentation.md` | Frontend details | UI modifications |
| `5_quick_reference_guide.md` | This file | Daily development |

---

## 10. Emergency Procedures

### System Not Working
1. **Check Servers**: Ensure all three servers are running
2. **Check Ports**: Verify no port conflicts
3. **Check Logs**: Look at server console output
4. **Restart**: Kill all Python processes and restart servers

### Reset Everything
```bash
# Kill all Python processes
taskkill /f /im python.exe

# Restart servers
cd lexer && python web_interface.py 8001
python ast_server.py 8005  
python flowchart_server.py 8003
```

### Get Help
1. **Check Documentation**: Review relevant documentation file
2. **Check Console**: Look for error messages in browser/server
3. **Test APIs**: Use curl commands to isolate issues
4. **Ask Team**: Share specific error messages and steps to reproduce

---

## 11. Development Workflow

### Making Changes
1. **Understand**: Read relevant documentation
2. **Plan**: Identify which files need modification
3. **Implement**: Make changes following existing patterns
4. **Test**: Verify functionality with all analysis types
5. **Document**: Update documentation if needed

### Code Review Checklist
- [ ] Follows existing code patterns
- [ ] Includes error handling
- [ ] Tested with sample C code
- [ ] Documentation updated if needed
- [ ] No breaking changes to APIs

This quick reference should help team members work efficiently with the C Code Analyzer project. For detailed information, always refer to the specific documentation files in the `project_report/` folder.
