#include <stdio.h>
int main()
{char ch, letter_flag = 0, count = 0;
    while((ch = getchar()) != '.') {
        if ('A' <= ch && ch <='Z' || 'a' <= ch && ch <= 'z') {
            if (letter_flag != 0) continue;
            count++;
            letter_flag = 1;
            continue;
        }
        if ( ch == ' ' || ch == ',' || ch == '.') letter_flag = 0;
    }
    printf("%d\n", count);
 
    return 0;
}

