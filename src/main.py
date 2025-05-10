import lexer

if __name__ == "__main__":
    lexer = lexer.tokenize("""
    #include <stdio.h>
    int main(){
	int i;
	scanf("%d",&i);
	switch(i)
	{
		case(1):{
			printf("one");
			break;
		}
		case(2):{
			printf("two");
			break;
		}
		case(3):{
			printf("three");
			break;
		}
		case(4):{
			printf("four");
			break;
		}
		case(5):{
			printf("five");
			break;
		}
		case(6):{
			printf("six");
			break;
		}
		default:printf("Please enter value in range of 1-6");
	}
}
""")      # Insert the code here
    for tokens in lexer:
        print(tokens)