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
    }

    parse(code) {
        const tokenizer = new CTokenizer();
        this.tokens = tokenizer.tokenize(code);
        this.position = 0;

        // Create proper parse tree following C grammar
        const parseTree = {
            type: 'program',
            rule: 'program → translation_unit',
            children: [],
            metadata: {
                totalLines: code.split('\n').length,
                totalTokens: this.tokens.length,
                productions: 0
            }
        };

        const translationUnit = this.parseTranslationUnit();
        if (translationUnit) {
            parseTree.children.push(translationUnit);
        }

        return parseTree;
    }

    parseTranslationUnit() {
        // translation_unit → external_declaration*
        const node = {
            type: 'translation_unit',
            rule: 'translation_unit → external_declaration*',
            children: []
        };

        while (this.position < this.tokens.length) {
            const externalDecl = this.parseExternalDeclaration();
            if (externalDecl) {
                node.children.push(externalDecl);
            } else {
                this.nextToken(); // Skip unrecognized tokens
            }
        }

        return node;
    }

    parseExternalDeclaration() {
        // external_declaration → function_definition | declaration | preprocessor_directive
        const token = this.currentToken();
        if (!token) return null;

        if (token.type === 'PREPROCESSOR') {
            return this.parsePreprocessorDirective();
        } else if (token.type === 'KEYWORD' && this.isTypeSpecifier(token.value)) {
            // Look ahead to determine if it's a function or variable declaration
            return this.parseDeclarationOrFunction();
        }

        return null;
    }

    isTypeSpecifier(value) {
        return ['int', 'float', 'char', 'double', 'void', 'long', 'short', 'unsigned', 'signed'].includes(value);
    }

    parsePreprocessorDirective() {
        // preprocessor_directive → '#' directive_name [arguments]
        const node = {
            type: 'preprocessor_directive',
            rule: 'preprocessor_directive → # directive_name [arguments]',
            children: []
        };

        // Add '#' terminal
        node.children.push(this.createTerminal('#'));
        this.nextToken();

        // Add directive name
        if (this.currentToken()) {
            node.children.push(this.createTerminal(this.currentToken().value));
            this.nextToken();

            // Add header file if present
            if (this.currentToken() && this.currentToken().type === 'HEADER_FILE') {
                node.children.push(this.createTerminal(this.currentToken().value));
                this.nextToken();
            }
        }

        return node;
    }

    parseDeclarationOrFunction() {
        // Look ahead to determine if it's a function or variable
        const savedPosition = this.position;

        // Skip type specifier
        this.nextToken();

        // Check for identifier
        if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
            this.nextToken();

            // Check for opening parenthesis (function) or other (variable)
            if (this.currentToken() && this.currentToken().value === '(') {
                // It's a function
                this.position = savedPosition;
                return this.parseFunctionDefinition();
            } else {
                // It's a variable declaration
                this.position = savedPosition;
                return this.parseDeclaration();
            }
        }

        this.position = savedPosition;
        return null;
    }

    currentToken() {
        return this.tokens[this.position];
    }

    nextToken() {
        this.position++;
        return this.currentToken();
    }

    createTerminal(value) {
        // Create a terminal node for the parse tree
        return {
            type: 'terminal',
            value: value,
            children: []
        };
    }

    parseFunctionDefinition() {
        // function_definition → type_specifier declarator compound_statement
        const node = {
            type: 'function_definition',
            rule: 'function_definition → type_specifier declarator compound_statement',
            children: []
        };

        // Parse type specifier
        const typeSpec = this.parseTypeSpecifier();
        if (typeSpec) {
            node.children.push(typeSpec);
        }

        // Parse declarator (function name and parameters)
        const declarator = this.parseDeclarator();
        if (declarator) {
            node.children.push(declarator);
        }

        // Parse compound statement (function body)
        const compoundStmt = this.parseCompoundStatement();
        if (compoundStmt) {
            node.children.push(compoundStmt);
        }

        return node;
    }

    parseTypeSpecifier() {
        // type_specifier → 'int' | 'float' | 'char' | 'double' | 'void'
        const token = this.currentToken();
        if (token && this.isTypeSpecifier(token.value)) {
            const node = {
                type: 'type_specifier',
                rule: `type_specifier → '${token.value}'`,
                children: [this.createTerminal(token.value)]
            };
            this.nextToken();
            return node;
        }
        return null;
    }

    parseDeclarator() {
        // declarator → identifier '(' parameter_list? ')'
        const node = {
            type: 'declarator',
            rule: 'declarator → identifier ( parameter_list? )',
            children: []
        };

        // Parse identifier
        if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
            node.children.push(this.createTerminal(this.currentToken().value));
            this.nextToken();

            // Parse '('
            if (this.currentToken() && this.currentToken().value === '(') {
                node.children.push(this.createTerminal('('));
                this.nextToken();

                // Parse parameter list (optional)
                const paramList = this.parseParameterList();
                if (paramList) {
                    node.children.push(paramList);
                }

                // Parse ')'
                if (this.currentToken() && this.currentToken().value === ')') {
                    node.children.push(this.createTerminal(')'));
                    this.nextToken();
                }
            }
        }

        return node;
    }

    parseParameterList() {
        // parameter_list → parameter_declaration (',' parameter_declaration)*
        const node = {
            type: 'parameter_list',
            rule: 'parameter_list → parameter_declaration (, parameter_declaration)*',
            children: []
        };

        // Check if we have parameters (not just void or empty)
        if (this.currentToken() && this.currentToken().value !== ')') {
            const param = this.parseParameterDeclaration();
            if (param) {
                node.children.push(param);

                // Parse additional parameters
                while (this.currentToken() && this.currentToken().value === ',') {
                    node.children.push(this.createTerminal(','));
                    this.nextToken();

                    const nextParam = this.parseParameterDeclaration();
                    if (nextParam) {
                        node.children.push(nextParam);
                    }
                }
            }
        }

        return node.children.length > 0 ? node : null;
    }

    parseParameterDeclaration() {
        // parameter_declaration → type_specifier identifier?
        const node = {
            type: 'parameter_declaration',
            rule: 'parameter_declaration → type_specifier identifier?',
            children: []
        };

        // Parse type specifier
        const typeSpec = this.parseTypeSpecifier();
        if (typeSpec) {
            node.children.push(typeSpec);

            // Parse optional identifier
            if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
                node.children.push(this.createTerminal(this.currentToken().value));
                this.nextToken();
            }
        }

        return node.children.length > 0 ? node : null;
    }

    parseCompoundStatement() {
        // compound_statement → '{' statement* '}'
        const node = {
            type: 'compound_statement',
            rule: 'compound_statement → { statement* }',
            children: []
        };

        // Parse '{'
        if (this.currentToken() && this.currentToken().value === '{') {
            node.children.push(this.createTerminal('{'));
            this.nextToken();

            // Parse statements
            while (this.currentToken() && this.currentToken().value !== '}') {
                const stmt = this.parseStatement();
                if (stmt) {
                    node.children.push(stmt);
                } else {
                    this.nextToken(); // Skip unrecognized tokens
                }
            }

            // Parse '}'
            if (this.currentToken() && this.currentToken().value === '}') {
                node.children.push(this.createTerminal('}'));
                this.nextToken();
            }
        }

        return node;
    }

    parseStatement() {
        // statement → compound_statement | expression_statement | selection_statement | iteration_statement | jump_statement | declaration
        const token = this.currentToken();
        if (!token) return null;

        switch (token.type) {
            case 'KEYWORD':
                if (this.isTypeSpecifier(token.value)) {
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
                    return this.parseJumpStatement();
                } else if (token.value === 'continue') {
                    return this.parseJumpStatement();
                }
                break;
            case 'IDENTIFIER':
                return this.parseExpressionStatement();
            case 'DELIMITER':
                if (token.value === '{') {
                    return this.parseCompoundStatement();
                }
                break;
        }

        // Skip unrecognized tokens
        this.nextToken();
        return null;
    }

    parseDeclaration() {
        // declaration → type_specifier init_declarator_list ';'
        const node = {
            type: 'declaration',
            rule: 'declaration → type_specifier init_declarator_list ;',
            children: []
        };

        // Parse type specifier
        const typeSpec = this.parseTypeSpecifier();
        if (typeSpec) {
            node.children.push(typeSpec);

            // Parse init declarator list
            const initDeclList = this.parseInitDeclaratorList();
            if (initDeclList) {
                node.children.push(initDeclList);
            }

            // Parse ';'
            if (this.currentToken() && this.currentToken().value === ';') {
                node.children.push(this.createTerminal(';'));
                this.nextToken();
            }
        }

        return node;
    }

    parseInitDeclaratorList() {
        // init_declarator_list → init_declarator (',' init_declarator)*
        const node = {
            type: 'init_declarator_list',
            rule: 'init_declarator_list → init_declarator (, init_declarator)*',
            children: []
        };

        // Parse first init declarator
        const initDecl = this.parseInitDeclarator();
        if (initDecl) {
            node.children.push(initDecl);

            // Parse additional declarators
            while (this.currentToken() && this.currentToken().value === ',') {
                node.children.push(this.createTerminal(','));
                this.nextToken();

                const nextInitDecl = this.parseInitDeclarator();
                if (nextInitDecl) {
                    node.children.push(nextInitDecl);
                }
            }
        }

        return node.children.length > 0 ? node : null;
    }

    parseInitDeclarator() {
        // init_declarator → declarator ('=' initializer)?
        const node = {
            type: 'init_declarator',
            rule: 'init_declarator → declarator (= initializer)?',
            children: []
        };

        // Parse identifier (simple declarator)
        if (this.currentToken() && this.currentToken().type === 'IDENTIFIER') {
            node.children.push(this.createTerminal(this.currentToken().value));
            this.nextToken();

            // Parse optional initializer
            if (this.currentToken() && this.currentToken().value === '=') {
                node.children.push(this.createTerminal('='));
                this.nextToken();

                const initializer = this.parseInitializer();
                if (initializer) {
                    node.children.push(initializer);
                }
            }
        }

        return node.children.length > 0 ? node : null;
    }

    parseInitializer() {
        // initializer → assignment_expression
        const node = {
            type: 'initializer',
            rule: 'initializer → assignment_expression',
            children: []
        };

        // Parse simple expression (literal or identifier)
        if (this.currentToken()) {
            node.children.push(this.createTerminal(this.currentToken().value));
            this.nextToken();
        }

        return node;
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

    parseIfStatement() {
        // selection_statement → 'if' '(' expression ')' statement ('else' statement)?
        const node = {
            type: 'selection_statement',
            rule: 'selection_statement → if ( expression ) statement (else statement)?',
            children: []
        };

        // Parse 'if'
        node.children.push(this.createTerminal('if'));
        this.nextToken();

        // Parse '('
        if (this.currentToken() && this.currentToken().value === '(') {
            node.children.push(this.createTerminal('('));
            this.nextToken();

            // Parse expression (simplified)
            const expr = this.parseExpression();
            if (expr) {
                node.children.push(expr);
            }

            // Parse ')'
            if (this.currentToken() && this.currentToken().value === ')') {
                node.children.push(this.createTerminal(')'));
                this.nextToken();
            }
        }

        // Parse statement
        const stmt = this.parseStatement();
        if (stmt) {
            node.children.push(stmt);
        }

        // Parse optional 'else' clause
        if (this.currentToken() && this.currentToken().value === 'else') {
            node.children.push(this.createTerminal('else'));
            this.nextToken();

            const elseStmt = this.parseStatement();
            if (elseStmt) {
                node.children.push(elseStmt);
            }
        }

        return node;
    }

    parseWhileStatement() {
        // iteration_statement → 'while' '(' expression ')' statement
        const node = {
            type: 'iteration_statement',
            rule: 'iteration_statement → while ( expression ) statement',
            children: []
        };

        // Parse 'while'
        node.children.push(this.createTerminal('while'));
        this.nextToken();

        // Parse condition
        this.parseParenthesizedExpression(node);

        // Parse body
        const body = this.parseStatement();
        if (body) {
            node.children.push(body);
        }

        return node;
    }

    parseForStatement() {
        // iteration_statement → 'for' '(' expression? ';' expression? ';' expression? ')' statement
        const node = {
            type: 'iteration_statement',
            rule: 'iteration_statement → for ( expression? ; expression? ; expression? ) statement',
            children: []
        };

        // Parse 'for'
        node.children.push(this.createTerminal('for'));
        this.nextToken();

        // Skip the entire for condition for simplicity
        let parenCount = 0;
        while (this.currentToken()) {
            if (this.currentToken().value === '(') parenCount++;
            if (this.currentToken().value === ')') parenCount--;
            node.children.push(this.createTerminal(this.currentToken().value));
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

    parseReturnStatement() {
        // jump_statement → 'return' expression? ';'
        const node = {
            type: 'jump_statement',
            rule: 'jump_statement → return expression? ;',
            children: []
        };

        // Parse 'return'
        node.children.push(this.createTerminal('return'));
        this.nextToken();

        // Parse optional expression
        if (this.currentToken() && this.currentToken().value !== ';') {
            const expr = this.parseExpression();
            if (expr) {
                node.children.push(expr);
            }
        }

        // Parse ';'
        if (this.currentToken() && this.currentToken().value === ';') {
            node.children.push(this.createTerminal(';'));
            this.nextToken();
        }

        return node;
    }

    parseJumpStatement() {
        // jump_statement → 'break' ';' | 'continue' ';'
        const node = {
            type: 'jump_statement',
            rule: `jump_statement → ${this.currentToken().value} ;`,
            children: []
        };

        // Parse 'break' or 'continue'
        node.children.push(this.createTerminal(this.currentToken().value));
        this.nextToken();

        // Parse ';'
        if (this.currentToken() && this.currentToken().value === ';') {
            node.children.push(this.createTerminal(';'));
            this.nextToken();
        }

        return node;
    }

    parseExpressionStatement() {
        // expression_statement → expression? ';'
        const node = {
            type: 'expression_statement',
            rule: 'expression_statement → expression? ;',
            children: []
        };

        // Parse expression if present
        if (this.currentToken() && this.currentToken().value !== ';') {
            const expr = this.parseExpression();
            if (expr) {
                node.children.push(expr);
            }
        }

        // Parse ';'
        if (this.currentToken() && this.currentToken().value === ';') {
            node.children.push(this.createTerminal(';'));
            this.nextToken();
        }

        return node;
    }

    parseExpression() {
        // expression → assignment_expression
        const node = {
            type: 'expression',
            rule: 'expression → assignment_expression',
            children: []
        };

        // Simple expression parsing - collect tokens until delimiter
        const tokens = [];
        while (this.currentToken() &&
               ![')', ';', ',', '}'].includes(this.currentToken().value)) {
            tokens.push(this.currentToken().value);
            this.nextToken();
        }

        if (tokens.length > 0) {
            // Create a simple expression node
            node.children.push(this.createTerminal(tokens.join(' ')));
        }

        return node.children.length > 0 ? node : null;
    }

    parseParenthesizedExpression(parentNode) {
        // Helper to parse '(' expression ')'
        if (this.currentToken() && this.currentToken().value === '(') {
            parentNode.children.push(this.createTerminal('('));
            this.nextToken();

            const expr = this.parseExpression();
            if (expr) {
                parentNode.children.push(expr);
            }

            if (this.currentToken() && this.currentToken().value === ')') {
                parentNode.children.push(this.createTerminal(')'));
                this.nextToken();
            }
        }
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

    formatAST(parseTree, indent = 0) {
        let output = "🌳 Parse Tree (Syntax Analysis)\n";
        output += "=".repeat(50) + "\n\n";

        // Add metadata summary
        if (parseTree.metadata) {
            output += "📊 Grammar Analysis Summary:\n";
            output += "─".repeat(30) + "\n";
            output += `📄 Total Lines: ${parseTree.metadata.totalLines}\n`;
            output += `🔤 Total Tokens: ${parseTree.metadata.totalTokens}\n`;
            output += `📝 Grammar Productions Used: ${this.countProductions(parseTree)}\n\n`;
        }

        output += "🏗️ Parse Tree Structure:\n";
        output += "─".repeat(30) + "\n";
        output += "Grammar: C Language Context-Free Grammar\n\n";
        output += this.formatNode(parseTree, indent);

        return output;
    }

    countProductions(node) {
        let count = node.rule ? 1 : 0;
        if (node.children) {
            node.children.forEach(child => {
                count += this.countProductions(child);
            });
        }
        return count;
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

        // Display grammar productions for non-terminals
        if (node.type === 'terminal') {
            output += `"${node.value}"\n`;
        } else {
            // Non-terminal with grammar rule
            output += `${node.type}`;
            if (node.rule) {
                output += ` [${node.rule}]`;
            }
            output += "\n";
        }

        // Format children with proper tree structure
        if (node.children && node.children.length > 0) {
            node.children.forEach((child, childIndex) => {
                const isLastChild = childIndex === node.children.length - 1;
                const childSpaces = isLast ? "    " : "│   ";
                const childOutput = this.formatNode(child, indent + 1, isLastChild);

                // Properly indent child output
                const lines = childOutput.split('\n');
                lines.forEach((line, lineIndex) => {
                    if (line.trim() && lineIndex === 0) {
                        output += spaces + childSpaces + line.substring(spaces.length + 4) + "\n";
                    } else if (line.trim() && lineIndex > 0) {
                        output += spaces + (isLast ? "    " : "│   ") + line.substring(spaces.length + 4) + "\n";
                    }
                });
            });
        }

        return output;
    }
}

// Export for use in main script
window.CTokenizer = CTokenizer;
window.CParser = CParser;
