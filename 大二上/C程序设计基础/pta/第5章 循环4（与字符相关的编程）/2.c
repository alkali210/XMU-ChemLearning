#include <stdio.h>
int main()
{ char ch;
    do {
        scanf("%c", &ch);
        if('A' <= ch && ch <= 'Z')
            putchar(ch + 3);
        else if('a' <= ch && ch <= 'z')
            putchar(ch - 3);
        else
            putchar(ch);
    }while(ch != '.');
 
    return 0;    
}
