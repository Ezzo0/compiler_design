#include <stdio.h>
#include <ctype.h>
#include <string.h>

typedef enum {
    KEYWORD, IDENTIFIER, NUMBER, OPERATOR, DELIMITER, TOKEN_EOF, UNKNOWN
} TokenType;

const char *keywords[] = {"int", "return", "if", "else", "while", "for", "void", "char"};
int num_keywords = 8;

int isKeyword(const char *str) {
    for (int i = 0; i < num_keywords; i++) {
        if (strcmp(str, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

TokenType classifyToken(const char *token) {
    if (isKeyword(token)) return KEYWORD;
    if (isdigit(token[0])) return NUMBER;
    if (isalpha(token[0])) return IDENTIFIER;
    return UNKNOWN;
}

void scanFile(FILE *file) {
    char c;
    char buffer[100];
    int bufferIndex = 0;
    
    while ((c = fgetc(file)) != EOF) {
        if (isspace(c)) continue;
        
        if (isalpha(c)) {
            buffer[bufferIndex++] = c;
            while (isalnum(c = fgetc(file))) {
                buffer[bufferIndex++] = c;
            }
            buffer[bufferIndex] = '\0';
            bufferIndex = 0;
            ungetc(c, file);
            printf("Lexeme: %s ==> Token: %s\n\n", buffer, classifyToken(buffer) == KEYWORD ? "Keyword" : "Identifier");
        }
        else if (isdigit(c)) {
            buffer[bufferIndex++] = c;
            while (isdigit(c = fgetc(file))) {
                buffer[bufferIndex++] = c;
            }
            buffer[bufferIndex] = '\0';
            bufferIndex = 0;
            ungetc(c, file);
            printf("Lexeme: %s ==> Token: Number\n\n", buffer);
        }
        else if (ispunct(c)) {
            printf("Lexeme: %c ==> Token: Special Character\n\n", c);
        }
    }
}

int main() {
    FILE *file = fopen("source.c", "r");
    if (file == NULL) {
        printf("Error: Cannot open file\n");
        return 1;
    }

    scanFile(file);
    fclose(file);

    char c = 0;
    printf("Press enter to exit");
    scanf("%c", &c);

    return 0;
}
