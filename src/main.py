import lexer

if __name__ == "__main__":
    lexer = lexer.tokenize("int main() { return 0; }")      # Insert the code here
    print(lexer)