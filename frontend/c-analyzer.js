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
        let output = "Lexical Analysis Results:\n";
        output += "=".repeat(50) + "\n\n";

        // Token summary
        const tokenCounts = {};
        tokens.forEach(token => {
            tokenCounts[token.type] = (tokenCounts[token.type] || 0) + 1;
        });

        output += "Token Summary:\n";
        output += "-".repeat(20) + "\n";
        Object.entries(tokenCounts).forEach(([type, count]) => {
            output += `${type}: ${count}\n`;
        });

        output += `\nTotal Tokens: ${tokens.length}\n\n`;

        // Detailed token list
        output += "Detailed Token List:\n";
        output += "-".repeat(30) + "\n";
        tokens.forEach((token, index) => {
            output += `${index + 1}. ${token.type}: "${token.value}" (Line ${token.line}, Col ${token.column})\n`;
        });

        return output;
    }
}

class CParser {
    constructor() {
        this.tokens = [];
        this.position = 0;
    }

    parse(code) {
        const tokenizer = new CTokenizer();
        this.tokens = tokenizer.tokenize(code);
        this.position = 0;

        const ast = {
            type: 'Program',
            children: []
        };

        while (this.position < this.tokens.length) {
            const node = this.parseStatement();
            if (node) {
                ast.children.push(node);
            }
        }

        return ast;
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
                if (['int', 'float', 'char', 'double', 'void'].includes(token.value)) {
                    return this.parseDeclaration();
                } else if (token.value === 'if') {
                    return this.parseIfStatement();
                } else if (token.value === 'while') {
                    return this.parseWhileStatement();
                } else if (token.value === 'for') {
                    return this.parseForStatement();
                } else if (token.value === 'return') {
                    return this.parseReturnStatement();
                }
                break;
            case 'IDENTIFIER':
                return this.parseExpression();
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
                    children: []
                };

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

    parseFunction(returnType, name) {
        const node = {
            type: 'FunctionDeclaration',
            returnType: returnType,
            name: name,
            children: []
        };

        // Skip parameters for now
        let braceCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') braceCount++;
            if (this.currentToken().value === ')') braceCount--;
            this.nextToken();
            if (braceCount === 0) break;
        }

        // Parse function body
        if (this.currentToken() && this.currentToken().value === '{') {
            const body = this.parseBlock();
            if (body) {
                node.children.push(body);
            }
        }

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

    parseExpression() {
        // Simple expression parsing - just skip to next statement
        while (this.currentToken() && this.currentToken().value !== ';') {
            this.nextToken();
        }
        if (this.currentToken() && this.currentToken().value === ';') {
            this.nextToken();
        }
        return null;
    }

    formatAST(ast, indent = 0) {
        let output = "Abstract Syntax Tree (AST):\n";
        output += "=".repeat(40) + "\n\n";
        output += this.formatNode(ast, indent);
        return output;
    }

    formatNode(node, indent = 0) {
        const spaces = "  ".repeat(indent);
        let output = "";

        if (indent === 0) {
            output += "└── ";
        } else {
            output += spaces + "├── ";
        }

        switch (node.type) {
            case 'Program':
                output += "Program\n";
                break;
            case 'Preprocessor':
                output += `Preprocessor: ${node.directive}\n`;
                break;
            case 'HeaderFile':
                output += `Header: ${node.value}\n`;
                break;
            case 'FunctionDeclaration':
                output += `Function: ${node.returnType} ${node.name}()\n`;
                break;
            case 'VariableDeclaration':
                output += `Variable: ${node.dataType} ${node.name}\n`;
                break;
            case 'Block':
                output += `Block (${node.children.length} statements)\n`;
                break;
            case 'IfStatement':
                output += "If Statement\n";
                break;
            case 'WhileStatement':
                output += "While Loop\n";
                break;
            case 'ForStatement':
                output += "For Loop\n";
                break;
            case 'ReturnStatement':
                output += "Return Statement\n";
                break;
            default:
                output += `${node.type}\n`;
        }

        // Format children
        if (node.children && node.children.length > 0) {
            node.children.forEach((child, index) => {
                output += this.formatNode(child, indent + 1);
            });
        }

        return output;
    }
}

// Export for use in main script
window.CTokenizer = CTokenizer;
window.CParser = CParser;
