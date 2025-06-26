document.addEventListener('DOMContentLoaded', function() {
    const codeInput = document.getElementById('codeInput');
    const outputDisplay = document.getElementById('outputDisplay');
    const outputType = document.getElementById('outputType');
    const clearBtn = document.getElementById('clearBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // Initialize analyzers
    const tokenizer = new CTokenizer();
    const parser = new CParser();

    // Clear button functionality
    clearBtn.addEventListener('click', function() {
        codeInput.value = '';
        showPlaceholder();
    });

    // Analyze button functionality
    analyzeBtn.addEventListener('click', function() {
        const code = codeInput.value.trim();
        if (!code) {
            alert('Please enter some C code to analyze');
            return;
        }

        generateOutput(code, outputType.value);
    });

    // Output type selector change
    outputType.addEventListener('change', function() {
        const code = codeInput.value.trim();
        if (code) {
            generateOutput(code, outputType.value);
        }
    });

    function showPlaceholder() {
        outputDisplay.innerHTML = `
            <div class="placeholder">
                <p>Enter C code and click "Analyze Code" to see the results</p>
                <div class="analysis-info">
                    <h3>Analysis Types:</h3>
                    <ul>
                        <li><strong>Lexical Analysis:</strong> Breaks code into tokens (keywords, identifiers, operators, literals, etc.)</li>
                        <li><strong>Parse Tree (AST):</strong> Shows the hierarchical structure of your code with functions, variables, and control structures</li>
                    </ul>
                    <div style="margin-top: 15px; padding: 10px; background-color: #e8f4fd; border-radius: 5px; border-left: 4px solid #3498db;">
                        <strong>✨ Client-side Analysis:</strong> No server required! Analysis runs directly in your browser.
                    </div>
                </div>
            </div>
        `;
    }

    function generateOutput(code, type) {
        // Show loading message
        outputDisplay.innerHTML = `<div class="output-content">Analyzing code...</div>`;

        let output = '';

        try {
            switch(type) {
                case 'lexical':
                    output = generateLexicalAnalysis(code);
                    break;
                case 'ast':
                    output = generateAST(code);
                    break;
                default:
                    output = 'Unknown analysis type selected.';
            }
        } catch (error) {
            output = `Error generating analysis: ${error.message}`;
        }

        outputDisplay.innerHTML = `<div class="output-content">${output}</div>`;
    }

    function generateLexicalAnalysis(code) {
        try {
            const tokens = tokenizer.tokenize(code);
            return tokenizer.formatTokens(tokens);
        } catch (error) {
            return `Error during lexical analysis: ${error.message}`;
        }
    }

    function generateAST(code) {
        try {
            const ast = parser.parse(code);
            return parser.formatAST(ast);
        } catch (error) {
            return `Error during AST generation: ${error.message}`;
        }
    }



    // Initialize with placeholder
    showPlaceholder();
});
