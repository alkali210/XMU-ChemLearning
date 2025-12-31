#include <stdio.h>
int main()
{ char ch;
  int count = 0;
    scanf(" %c", &ch);
    while (ch != 'e') {
        if (ch == '1') 
            printf("one\n");
        else if (ch == '2')
            printf("two\n");
        else if (ch == '3')
            printf("three\n");
        else if (ch == '4')
            printf("four\n");
        else if (ch == '5')
            printf("five\n");
        scanf(" %c", &ch);
    }
    return 0;
}
