# C Code Analyzer

A client-side web-based C code analyzer with lexical analysis and parse tree (AST) generation. No backend servers required!

## 🚀 Live Demo

**Deployed on Vercel**: [https://your-app.vercel.app](https://your-app.vercel.app)

## ✨ Features

- **Client-side Processing**: Runs entirely in your browser - no servers needed
- **Lexical Analysis**: Complete C language tokenization with detailed token information
- **Parse Tree (AST)**: Abstract Syntax Tree generation showing code structure
- **Real-time Analysis**: Instant results as you type
- **Mobile Friendly**: Responsive design works on all devices
- **No Installation**: Just open and use

## 🎯 Quick Start

### Option 1: Use Online (Recommended)
Simply visit the live demo link above - no setup required!

### Option 2: Run Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/prakhar315/Code_analyzer.git
   cd Code_analyzer
   ```

2. **Open the frontend:**
   Open `frontend/index.html` in your web browser

3. **Analyze C code:**
   - Enter your C code in the textarea
   - Select analysis type (Lexical Analysis or Parse Tree)
   - Click "Analyze Code"
   - View detailed results instantly

### Option 3: Deploy to Vercel
1. **Fork this repository**
2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your forked repository
   - Deploy automatically

## 📁 Project Structure

```
C-Code-Analyzer/
├── frontend/
│   ├── index.html          # Main web interface
│   ├── script.js           # Main application logic
│   ├── c-analyzer.js       # C language analyzer (tokenizer & parser)
│   └── style.css           # Styling and responsive design
├── vercel.json             # Vercel deployment configuration
├── project_report/         # Comprehensive documentation
└── README.md               # This file
```

## 🛠️ Technical Details

### Client-side Implementation
- **No Backend Required**: All analysis runs in the browser using JavaScript
- **Custom Tokenizer**: Implements C language lexical analysis
- **Recursive Descent Parser**: Generates Abstract Syntax Trees
- **Real-time Processing**: Instant analysis without server calls

### Supported C Language Features
- **Keywords**: All C keywords (int, float, if, while, etc.)
- **Operators**: Arithmetic, logical, comparison, assignment operators
- **Literals**: Integer, float, string, and character literals
- **Identifiers**: Variable and function names
- **Comments**: Single-line (//) and multi-line (/* */) comments
- **Preprocessor**: #include, #define directives
- **Control Structures**: if/else, while, for loops
- **Functions**: Function declarations and definitions
- **Variables**: Variable declarations and assignments

## 🎨 Features

- **Lexical Analysis**:
  - Complete tokenization with token types and positions
  - Line and column number tracking
  - Token count summaries
  - Detailed token listings

- **Parse Tree (AST)**:
  - Hierarchical code structure visualization
  - Function and variable identification
  - Control flow structure detection
  - Tree-formatted output with Unicode characters

- **User Experience**:
  - Clean, modern interface
  - Responsive design for mobile devices
  - Real-time analysis
  - Sample code included
  - Error handling and user feedback

## 🌐 Deployment

### Vercel Deployment (Recommended)
This project is optimized for Vercel deployment:

1. **Automatic Deployment**: Push to main branch triggers deployment
2. **Static Site**: No server-side processing required
3. **Fast CDN**: Global content delivery network
4. **Custom Domain**: Easy custom domain setup

### Other Hosting Options
- **GitHub Pages**: Works with static hosting
- **Netlify**: Drag and drop deployment
- **Any Static Host**: No special requirements

## 📖 Documentation

Comprehensive documentation is available in the `project_report/` folder:
- Complete system architecture
- Function and class documentation
- Development guidelines
- API reference (for the original server-based version)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
