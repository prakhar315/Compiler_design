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
            <div class="welcome-message">
                <div class="welcome-icon">🎯</div>
                <h3>Welcome to C Code Analyzer</h3>
                <p>Enter your C code and select an analysis type to get started</p>

                <div class="quick-info">
                    <div class="info-card">
                        <div class="info-icon">🔍</div>
                        <h4>Lexical Analysis</h4>
                        <p>Tokenizes code into keywords, operators, identifiers, and literals with detailed categorization</p>
                    </div>
                    <div class="info-card">
                        <div class="info-icon">🌳</div>
                        <h4>Parse Tree</h4>
                        <p>Generates syntax tree following C grammar productions and compiler design principles</p>
                    </div>
                </div>

                <div class="tech-note">
                    <strong>✨ Client-side Analysis:</strong> No server required! Analysis runs directly in your browser using advanced JavaScript parsing algorithms.
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
