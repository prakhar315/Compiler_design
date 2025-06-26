/**
 * C Code Analyzer - Client-side Implementation
 * Lexical Analysis and Parse Tree Generation for C Code
 */

class CTokenizer {
    constructor() {
        // C language keywords
        this.keywords = new Set([
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
            'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
            'void', 'volatile', 'while', 'include', 'define'
        ]);

        // Token patterns
        this.tokenPatterns = [
            { type: 'PREPROCESSOR', pattern: /^#\s*(include|define|ifdef|ifndef|endif|if|else|elif)\b/ },
            { type: 'HEADER_FILE', pattern: /^<[^>]+>/ },
            { type: 'STRING_LITERAL', pattern: /^"([^"\\]|\\.)*"/ },
            { type: 'CHAR_LITERAL', pattern: /^'([^'\\]|\\.)*'/ },
            { type: 'FLOAT_LITERAL', pattern: /^\d+\.\d+([eE][+-]?\d+)?[fF]?/ },
            { type: 'INTEGER_LITERAL', pattern: /^\d+[uUlL]*/ },
            { type: 'IDENTIFIER', pattern: /^[a-zA-Z_][a-zA-Z0-9_]*/ },
            { type: 'COMMENT_MULTI', pattern: /^\/\*[\s\S]*?\*\// },
            { type: 'COMMENT_SINGLE', pattern: /^\/\/.*/ },
            { type: 'OPERATOR', pattern: /^(\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||->|\+=|-=|\*=|\/=|%=|&=|\|=|\^=|<<=|>>=)/ },
            { type: 'OPERATOR', pattern: /^[+\-*\/%=<>!&|^~]/ },
            { type: 'DELIMITER', pattern: /^[(){}\[\];,.]/ },
            { type: 'WHITESPACE', pattern: /^\s+/ }
        ];
    }

    tokenize(code) {
        const tokens = [];
        let position = 0;
        let line = 1;
        let column = 1;

        while (position < code.length) {
            let matched = false;

            for (const { type, pattern } of this.tokenPatterns) {
                const match = code.slice(position).match(pattern);
                if (match) {
                    const value = match[0];
                    
                    if (type !== 'WHITESPACE') {
                        let tokenType = type;
                        
                        // Check if identifier is a keyword
                        if (type === 'IDENTIFIER' && this.keywords.has(value)) {
                            tokenType = 'KEYWORD';
                        }

                        tokens.push({
                            type: tokenType,
                            value: value,
                            line: line,
                            column: column,
                            position: position
                        });
                    }

                    // Update position and line/column tracking
                    for (let i = 0; i < value.length; i++) {
                        if (value[i] === '\n') {
                            line++;
                            column = 1;
                        } else {
                            column++;
                        }
                    }
                    
                    position += value.length;
                    matched = true;
                    break;
                }
            }

            if (!matched) {
                // Skip unknown character
                position++;
                column++;
            }
        }

        return tokens;
    }

    formatTokens(tokens) {
        let output = "🔍 Lexical Analysis Results\n";
        output += "=".repeat(50) + "\n\n";

        // Token summary with emojis
        const tokenCounts = {};
        const tokenEmojis = {
            'KEYWORD': '🔑',
            'IDENTIFIER': '🏷️',
            'INTEGER_LITERAL': '🔢',
            'FLOAT_LITERAL': '🔢',
            'STRING_LITERAL': '📝',
            'CHAR_LITERAL': '📝',
            'OPERATOR': '⚡',
            'DELIMITER': '🔗',
            'PREPROCESSOR': '🔧',
            'HEADER_FILE': '📁',
            'COMMENT_SINGLE': '💬',
            'COMMENT_MULTI': '💬'
        };

        tokens.forEach(token => {
            tokenCounts[token.type] = (tokenCounts[token.type] || 0) + 1;
        });

        output += "📊 Token Summary:\n";
        output += "─".repeat(25) + "\n";
        Object.entries(tokenCounts).forEach(([type, count]) => {
            const emoji = tokenEmojis[type] || '❓';
            output += `${emoji} ${type}: ${count}\n`;
        });

        output += `\n📈 Total Tokens: ${tokens.length}\n`;
        output += `📄 Lines Analyzed: ${Math.max(...tokens.map(t => t.line))}\n\n`;

        // Categorized token display
        const categories = {
            'Keywords': ['KEYWORD'],
            'Identifiers': ['IDENTIFIER'],
            'Literals': ['INTEGER_LITERAL', 'FLOAT_LITERAL', 'STRING_LITERAL', 'CHAR_LITERAL'],
            'Operators': ['OPERATOR'],
            'Delimiters': ['DELIMITER'],
            'Preprocessor': ['PREPROCESSOR', 'HEADER_FILE'],
            'Comments': ['COMMENT_SINGLE', 'COMMENT_MULTI']
        };

        output += "🗂️  Detailed Token Analysis:\n";
        output += "─".repeat(35) + "\n";

        Object.entries(categories).forEach(([category, types]) => {
            const categoryTokens = tokens.filter(token => types.includes(token.type));
            if (categoryTokens.length > 0) {
                output += `\n${category} (${categoryTokens.length}):\n`;
                categoryTokens.forEach((token, index) => {
                    const emoji = tokenEmojis[token.type] || '❓';
                    output += `  ${emoji} "${token.value}" (Line ${token.line}, Col ${token.column})\n`;
                });
            }
        });

        return output;
    }
}

class CParser {
    constructor() {
        this.tokens = [];
        this.position = 0;
        this.currentFunction = null;
    }

    parse(code) {
        const tokenizer = new CTokenizer();
        this.tokens = tokenizer.tokenize(code);
        this.position = 0;
        this.currentFunction = null;

        const ast = {
            type: 'Program',
            children: [],
            metadata: {
                totalLines: code.split('\n').length,
                totalTokens: this.tokens.length,
                functions: 0,
                variables: 0,
                controlStructures: 0
            }
        };

        while (this.position < this.tokens.length) {
            const node = this.parseStatement();
            if (node) {
                ast.children.push(node);
                this.updateMetadata(ast.metadata, node);
            }
        }

        return ast;
    }

    updateMetadata(metadata, node) {
        switch (node.type) {
            case 'FunctionDeclaration':
                metadata.functions++;
                break;
            case 'VariableDeclaration':
                metadata.variables++;
                break;
            case 'IfStatement':
            case 'WhileStatement':
            case 'ForStatement':
                metadata.controlStructures++;
                break;
        }
    }

    currentToken() {
        return this.tokens[this.position];
    }

    nextToken() {
        this.position++;
        return this.currentToken();
    }

    parseStatement() {
        const token = this.currentToken();
        if (!token) return null;

        switch (token.type) {
            case 'PREPROCESSOR':
                return this.parsePreprocessor();
            case 'KEYWORD':
                if (['int', 'float', 'char', 'double', 'void', 'long', 'short', 'unsigned', 'signed'].includes(token.value)) {
                    return this.parseDeclaration();
                } else if (token.value === 'if') {
                    return this.parseIfStatement();
                } else if (token.value === 'while') {
                    return this.parseWhileStatement();
                } else if (token.value === 'for') {
                    return this.parseForStatement();
                } else if (token.value === 'return') {
                    return this.parseReturnStatement();
                } else if (token.value === 'break') {
                    return this.parseBreakStatement();
                } else if (token.value === 'continue') {
                    return this.parseContinueStatement();
                } else if (token.value === 'switch') {
                    return this.parseSwitchStatement();
                } else {
                    this.nextToken();
                    return null;
                }
            case 'IDENTIFIER':
                return this.parseExpressionStatement();
            default:
                this.nextToken();
                return null;
        }
    }

    parsePreprocessor() {
        const node = {
            type: 'Preprocessor',
            directive: this.currentToken().value,
            children: []
        };

        this.nextToken();
        
        // Parse header file if present
        if (this.currentToken() && this.currentToken().type === 'HEADER_FILE') {
            node.children.push({
                type: 'HeaderFile',
                value: this.currentToken().value,
                children: []
            });
            this.nextToken();
        }

        return node;
    }

    parseDeclaration() {
        const type = this.currentToken().value;
        this.nextToken();

        if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
            const name = this.currentToken().value;
            this.nextToken();

            // Check if it's a function declaration
            if (this.currentToken() && this.currentToken().value === '(') {
                return this.parseFunction(type, name);
            } else {
                // Variable declaration
                const node = {
                    type: 'VariableDeclaration',
                    dataType: type,
                    name: name,
                    value: null,
                    children: [],
                    line: this.currentToken() ? this.currentToken().line : 1
                };

                // Check for initialization
                if (this.currentToken() && this.currentToken().value === '=') {
                    this.nextToken(); // Skip '='
                    const valueToken = this.currentToken();
                    if (valueToken) {
                        node.value = valueToken.value;
                        node.children.push({
                            type: 'Initializer',
                            value: valueToken.value,
                            valueType: this.getValueType(valueToken),
                            children: []
                        });
                        this.nextToken();
                    }
                }

                // Skip to semicolon
                while (this.currentToken() && this.currentToken().value !== ';') {
                    this.nextToken();
                }
                if (this.currentToken() && this.currentToken().value === ';') {
                    this.nextToken();
                }

                return node;
            }
        }

        return null;
    }

    getValueType(token) {
        switch (token.type) {
            case 'INTEGER_LITERAL': return 'integer';
            case 'FLOAT_LITERAL': return 'float';
            case 'STRING_LITERAL': return 'string';
            case 'CHAR_LITERAL': return 'character';
            case 'IDENTIFIER': return 'variable';
            default: return 'unknown';
        }
    }

    parseFunction(returnType, name) {
        const node = {
            type: 'FunctionDeclaration',
            returnType: returnType,
            name: name,
            parameters: [],
            children: [],
            line: this.currentToken() ? this.currentToken().line : 1
        };

        this.currentFunction = name;

        // Parse parameters
        if (this.currentToken() && this.currentToken().value === '(') {
            this.nextToken(); // Skip '('

            while (this.currentToken() && this.currentToken().value !== ')') {
                if (this.currentToken().type === 'KEYWORD' &&
                    ['int', 'float', 'char', 'double', 'void'].includes(this.currentToken().value)) {
                    const paramType = this.currentToken().value;
                    this.nextToken();

                    if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
                        const paramName = this.currentToken().value;
                        node.parameters.push({
                            type: paramType,
                            name: paramName
                        });
                        this.nextToken();
                    }
                }

                if (this.currentToken() && this.currentToken().value === ',') {
                    this.nextToken(); // Skip comma
                }

                // Safety check to avoid infinite loop
                if (this.currentToken() &&
                    this.currentToken().type !== 'KEYWORD' &&
                    this.currentToken().value !== ')' &&
                    this.currentToken().value !== ',') {
                    this.nextToken();
                }
            }

            if (this.currentToken() && this.currentToken().value === ')') {
                this.nextToken(); // Skip ')'
            }
        }

        // Add parameters as children for display
        if (node.parameters.length > 0) {
            node.children.push({
                type: 'ParameterList',
                parameters: node.parameters,
                children: []
            });
        }

        // Parse function body
        if (this.currentToken() && this.currentToken().value === '{') {
            const body = this.parseBlock();
            if (body) {
                node.children.push(body);
            }
        }

        this.currentFunction = null;
        return node;
    }

    parseBlock() {
        if (!this.currentToken() || this.currentToken().value !== '{') {
            return null;
        }

        const node = {
            type: 'Block',
            children: []
        };

        this.nextToken(); // Skip '{'

        while (this.currentToken() && this.currentToken().value !== '}') {
            const stmt = this.parseStatement();
            if (stmt) {
                node.children.push(stmt);
            }
        }

        if (this.currentToken() && this.currentToken().value === '}') {
            this.nextToken(); // Skip '}'
        }

        return node;
    }

    parseIfStatement() {
        const node = {
            type: 'IfStatement',
            children: []
        };

        this.nextToken(); // Skip 'if'

        // Skip condition for now
        let parenCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') parenCount++;
            if (this.currentToken().value === ')') parenCount--;
            this.nextToken();
            if (parenCount === 0) break;
        }

        // Parse body
        const body = this.parseStatement();
        if (body) {
            node.children.push(body);
        }

        return node;
    }

    parseWhileStatement() {
        const node = {
            type: 'WhileStatement',
            children: []
        };

        this.nextToken(); // Skip 'while'

        // Skip condition and parse body similar to if statement
        let parenCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') parenCount++;
            if (this.currentToken().value === ')') parenCount--;
            this.nextToken();
            if (parenCount === 0) break;
        }

        const body = this.parseStatement();
        if (body) {
            node.children.push(body);
        }

        return node;
    }

    parseForStatement() {
        const node = {
            type: 'ForStatement',
            children: []
        };

        this.nextToken(); // Skip 'for'

        // Skip condition and parse body
        let parenCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') parenCount++;
            if (this.currentToken().value === ')') parenCount--;
            this.nextToken();
            if (parenCount === 0) break;
        }

        const body = this.parseStatement();
        if (body) {
            node.children.push(body);
        }

        return node;
    }

    parseReturnStatement() {
        const node = {
            type: 'ReturnStatement',
            children: []
        };

        this.nextToken(); // Skip 'return'

        // Skip to semicolon
        while (this.currentToken() && this.currentToken().value !== ';') {
            this.nextToken();
        }
        if (this.currentToken() && this.currentToken().value === ';') {
            this.nextToken();
        }

        return node;
    }

    parseExpressionStatement() {
        const node = {
            type: 'ExpressionStatement',
            children: []
        };

        // Simple expression parsing - collect tokens until semicolon
        const expression = [];
        while (this.currentToken() && this.currentToken().value !== ';') {
            expression.push(this.currentToken().value);
            this.nextToken();
        }

        if (expression.length > 0) {
            node.expression = expression.join(' ');

            // Detect assignment
            if (expression.includes('=')) {
                node.type = 'Assignment';
                const assignIndex = expression.indexOf('=');
                node.variable = expression.slice(0, assignIndex).join(' ').trim();
                node.value = expression.slice(assignIndex + 1).join(' ').trim();
            }
            // Detect function call
            else if (expression.some(token => token.includes('('))) {
                node.type = 'FunctionCall';
                node.function = expression[0];
            }
        }

        if (this.currentToken() && this.currentToken().value === ';') {
            this.nextToken();
        }

        return expression.length > 0 ? node : null;
    }

    parseBreakStatement() {
        const node = {
            type: 'BreakStatement',
            children: []
        };

        this.nextToken(); // Skip 'break'

        if (this.currentToken() && this.currentToken().value === ';') {
            this.nextToken();
        }

        return node;
    }

    parseContinueStatement() {
        const node = {
            type: 'ContinueStatement',
            children: []
        };

        this.nextToken(); // Skip 'continue'

        if (this.currentToken() && this.currentToken().value === ';') {
            this.nextToken();
        }

        return node;
    }

    parseSwitchStatement() {
        const node = {
            type: 'SwitchStatement',
            children: []
        };

        this.nextToken(); // Skip 'switch'

        // Skip condition
        let parenCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') parenCount++;
            if (this.currentToken().value === ')') parenCount--;
            this.nextToken();
            if (parenCount === 0) break;
        }

        // Parse body
        const body = this.parseBlock();
        if (body) {
            node.children.push(body);
        }

        return node;
    }

    formatAST(ast, indent = 0) {
        let output = "🌳 Parse Tree (Abstract Syntax Tree)\n";
        output += "=".repeat(50) + "\n\n";

        // Add metadata summary
        if (ast.metadata) {
            output += "📊 Code Analysis Summary:\n";
            output += "─".repeat(25) + "\n";
            output += `📄 Total Lines: ${ast.metadata.totalLines}\n`;
            output += `🔤 Total Tokens: ${ast.metadata.totalTokens}\n`;
            output += `⚙️  Functions: ${ast.metadata.functions}\n`;
            output += `📦 Variables: ${ast.metadata.variables}\n`;
            output += `🔀 Control Structures: ${ast.metadata.controlStructures}\n\n`;
        }

        output += "🏗️  Program Structure:\n";
        output += "─".repeat(25) + "\n";
        output += this.formatNode(ast, indent);

        return output;
    }

    formatNode(node, indent = 0, isLast = true) {
        const spaces = "  ".repeat(indent);
        let output = "";

        // Better tree formatting with proper connectors
        if (indent === 0) {
            output += "└── ";
        } else {
            output += spaces + (isLast ? "└── " : "├── ");
        }

        switch (node.type) {
            case 'Program':
                output += "📋 Program\n";
                break;
            case 'Preprocessor':
                output += `🔧 Preprocessor: ${node.directive}\n`;
                break;
            case 'HeaderFile':
                output += `📁 Header: ${node.value}\n`;
                break;
            case 'FunctionDeclaration':
                const params = node.parameters && node.parameters.length > 0
                    ? node.parameters.map(p => `${p.type} ${p.name}`).join(', ')
                    : 'void';
                output += `⚙️  Function: ${node.returnType} ${node.name}(${params})\n`;
                break;
            case 'ParameterList':
                output += `📝 Parameters (${node.parameters.length})\n`;
                break;
            case 'VariableDeclaration':
                const valueInfo = node.value ? ` = ${node.value}` : '';
                output += `📦 Variable: ${node.dataType} ${node.name}${valueInfo}\n`;
                break;
            case 'Initializer':
                output += `🔢 Value: ${node.value} (${node.valueType})\n`;
                break;
            case 'Block':
                output += `🏗️  Block (${node.children.length} statements)\n`;
                break;
            case 'IfStatement':
                output += "🔀 If Statement\n";
                break;
            case 'WhileStatement':
                output += "🔄 While Loop\n";
                break;
            case 'ForStatement':
                output += "🔁 For Loop\n";
                break;
            case 'ReturnStatement':
                output += "↩️  Return Statement\n";
                break;
            case 'ExpressionStatement':
                output += `💭 Expression: ${node.expression || 'unknown'}\n`;
                break;
            case 'Assignment':
                output += `📝 Assignment: ${node.variable} = ${node.value}\n`;
                break;
            case 'FunctionCall':
                output += `📞 Function Call: ${node.function}()\n`;
                break;
            case 'BreakStatement':
                output += "🛑 Break Statement\n";
                break;
            case 'ContinueStatement':
                output += "⏭️  Continue Statement\n";
                break;
            case 'SwitchStatement':
                output += "🔀 Switch Statement\n";
                break;
            default:
                output += `❓ ${node.type}\n`;
        }

        // Format children with proper tree structure
        if (node.children && node.children.length > 0) {
            node.children.forEach((child, childIndex) => {
                const isLastChild = childIndex === node.children.length - 1;
                const childSpaces = isLast ? "    " : "│   ";
                output += spaces + childSpaces.substring(0, 2) +
                         this.formatNode(child, indent + 1, isLastChild).substring(spaces.length + 4);
            });
        }

        return output;
    }
}

// Export for use in main script
window.CTokenizer = CTokenizer;
window.CParser = CParser;
