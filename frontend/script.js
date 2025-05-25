document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('codeInput');
    const outputDisplay = document.getElementById('outputDisplay');
    const outputType = document.getElementById('outputType');
    const clearBtn = document.getElementById('clearBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // Clear button functionality
    clearBtn.addEventListener('click', function() {
        codeInput.value = '';
        showPlaceholder();
    });

    // Analyze button functionality
    analyzeBtn.addEventListener('click', async function() {
        const code = codeInput.value.trim();
        if (!code) {
            alert('Please enter some C code to analyze');
            return;
        }

        await generateOutput(code, outputType.value);
    });

    // Output type selector change
    outputType.addEventListener('change', async function() {
        const code = codeInput.value.trim();
        if (code) {
            await generateOutput(code, outputType.value);
        }
    });

    function showPlaceholder() {
        outputDisplay.innerHTML = `
            <div class="placeholder">
                <p>Enter C code and click "Analyze Code" to see the results</p>
                <div class="analysis-info">
                    <h3>Analysis Types:</h3>
                    <ul>
                        <li><strong>Lexical Analysis:</strong> Breaks code into tokens (keywords, identifiers, operators, etc.)</li>
                        <li><strong>AST:</strong> Shows the hierarchical structure of your code</li>
                        <li><strong>Flowchart:</strong> Visual representation of program flow</li>
                    </ul>
                    <div style="margin-top: 15px; padding: 10px; background-color: #e8f4fd; border-radius: 5px; border-left: 4px solid #3498db;">
                        <strong>Note:</strong> Make sure to start the lexer server first.<br>
                        <small>Run: <code>python lexer/web_interface.py 8001</code></small>
                    </div>
                </div>
            </div>
        `;
    }

    async function generateOutput(code, type) {
        // Show loading message
        outputDisplay.innerHTML = `<div class="output-content">Analyzing code...</div>`;

        let output = '';

        try {
            switch(type) {
                case 'lexical':
                    output = await generateLexicalAnalysis(code);
                    break;
                case 'ast':
                    output = await generateAST(code);
                    break;
                case 'flowchart':
                    output = await generateFlowchart(code);
                    break;
            }
        } catch (error) {
            output = `Error generating analysis: ${error.message}`;
        }

        outputDisplay.innerHTML = `<div class="output-content">${output}</div>`;
    }

    async function generateLexicalAnalysis(code) {
        try {
            // Call the lexer API
            const response = await fetch('http://localhost:8001/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                return data.formatted_output;
            } else {
                return `Error during lexical analysis: ${data.error}`;
            }
        } catch (error) {
            return `Error: Could not connect to lexer server. Please start the server first.

Run: python lexer/web_interface.py 8001

Error details: ${error.message}`;
        }
    }

    async function generateAST(code) {
        try {
            // Call the parser API
            const response = await fetch('http://localhost:8005/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                return data.formatted_output;
            } else {
                return `Error during AST generation: ${data.error}`;
            }
        } catch (error) {
            return `Error: Could not connect to parser server. Please start the server first.

Run: python ast_server.py 8005

Error details: ${error.message}`;
        }
    }

    async function generateFlowchart(code) {
        try {
            // Call the flowchart API
            const response = await fetch('http://localhost:8003/flowchart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: code })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                // If SVG content is available, display it
                if (data.svg_content) {
                    return `Control Flow Graph:
========================================

${data.formatted_output}

Visual Flowchart:
-----------------
${data.svg_content}`;
                } else {
                    return data.formatted_output;
                }
            } else {
                return `Error during flowchart generation: ${data.error}`;
            }
        } catch (error) {
            return `Error: Could not connect to flowchart server. Please start the server first.

Run: python flowchart/web_interface.py 8003

Error details: ${error.message}`;
        }
    }

    // Initialize with placeholder
    showPlaceholder();
});
